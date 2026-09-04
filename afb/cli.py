from __future__ import annotations
import argparse, json
from afb.schema import SystemManifest
from afb.packs.reference import generate_reference_suite
from afb.packs.frontier import generate_frontier_suite
from afb.adapters.standard import CommandAdapter, OpenAICompatibleAdapter
from afb.oracle import OracleAdapter, WeakAdapter
from afb.runner import run_suite
from afb.report import capability_card
from afb.safety import run_sidecar_safety_suite
from afb.baselines import (
    load_human_baselines, apply_human_baselines,
    record_human_timing, compile_human_baselines,
)
from afb.external.terminal import normalize_terminal_results


def _parse_tool_versions(items):
    out = {}
    for item in items or []:
        if "=" not in item: raise ValueError("--tool-version must use NAME=VERSION")
        k,v=item.split("=",1); out[k.strip()]=v.strip()
    return out


def _build_adapter(a,p):
    if a.adapter=="oracle": return OracleAdapter(),"oracle-validator"
    if a.adapter=="weak": return WeakAdapter(),"weak-control"
    if a.adapter=="command":
        if not a.command: p.error("--command required")
        return CommandAdapter(a.command,timeout_s=a.timeout_s),a.system_name
    if not a.base_url or not a.model: p.error("--base-url and --model required")
    return OpenAICompatibleAdapter(a.base_url,a.model,a.api_key,timeout_s=a.timeout_s,
        temperature=a.temperature,top_p=a.top_p,max_output_tokens=a.max_output_tokens,seed=a.inference_seed),a.system_name


def _add_adapter_args(parser):
    parser.add_argument("--adapter",choices=["oracle","weak","command","openai-compatible"],required=True)
    parser.add_argument("--command"); parser.add_argument("--base-url"); parser.add_argument("--model"); parser.add_argument("--api-key")
    parser.add_argument("--system-name",default="unnamed-system"); parser.add_argument("--timeout-s",type=float,default=120)
    parser.add_argument("--temperature",type=float,default=0.0); parser.add_argument("--top-p",type=float)
    parser.add_argument("--inference-seed",type=int); parser.add_argument("--max-output-tokens",type=int)


def _add_manifest_args(parser):
    parser.add_argument("--official",action="store_true",help="Require a publication-grade manifest before running")
    parser.add_argument("--provider",default="unknown"); parser.add_argument("--model-version",default="unknown"); parser.add_argument("--api-version",default="unknown")
    parser.add_argument("--level",choices=["core","tool","agent","autonomous"],default="core")
    parser.add_argument("--system-prompt-hash",default=""); parser.add_argument("--tools",default="",help="Comma-separated declared tools")
    parser.add_argument("--tool-version",action="append",default=[],help="NAME=VERSION; repeat as needed")
    parser.add_argument("--external-memory",action="store_true"); parser.add_argument("--scaffold",default="none"); parser.add_argument("--scaffold-version",default="unknown")
    parser.add_argument("--harness-commit-sha",default=""); parser.add_argument("--reasoning-budget",default="standard"); parser.add_argument("--retry-policy",default="task_defined")
    parser.add_argument("--network-policy",default="none"); parser.add_argument("--context-policy",default="provider_default")
    parser.add_argument("--max-runtime-s",type=float); parser.add_argument("--max-actions",type=int); parser.add_argument("--max-total-tokens",type=int)
    parser.add_argument("--max-calls",type=int); parser.add_argument("--max-cost-usd",type=float)
    parser.add_argument("--component-label",default="full_system"); parser.add_argument("--parent-configuration")


def _manifest(a,name,pack):
    tools=[x.strip() for x in a.tools.split(",") if x.strip()]
    return SystemManifest(system_name=name,provider=a.provider,
        base_model=a.model or ("oracle" if a.adapter=="oracle" else "weak" if a.adapter=="weak" else "command-adapter"),
        model_version=a.model_version,api_version=a.api_version,evaluation_claim=a.evaluation_claim,level=a.level,pack=pack,official=a.official,
        system_prompt_hash=a.system_prompt_hash,tools=tools,tool_versions=_parse_tool_versions(a.tool_version),external_memory=a.external_memory,
        scaffold=a.scaffold,scaffold_version=a.scaffold_version,harness_commit_sha=a.harness_commit_sha,reasoning_budget=a.reasoning_budget,
        retry_policy=a.retry_policy,temperature=a.temperature,top_p=a.top_p,inference_seed=a.inference_seed,max_output_tokens=a.max_output_tokens,
        max_total_tokens=a.max_total_tokens,max_calls=a.max_calls,max_actions=a.max_actions,max_runtime_s=a.max_runtime_s,max_cost_usd=a.max_cost_usd,
        network_policy=a.network_policy,context_policy=a.context_policy,component_label=a.component_label,parent_configuration=a.parent_configuration)


def _validate_official(manifest,trials,p):
    if not manifest.official: return
    missing=manifest.official_missing_fields()
    if trials<2: missing.append("trials>=2")
    if manifest.pack=="frontier" and not manifest.tools: missing.append("tools")
    if missing: p.error("official AFB output refused; incomplete manifest: "+", ".join(sorted(set(missing))))


def main():
    p=argparse.ArgumentParser(prog="afb"); sp=p.add_subparsers(dest="cmd",required=True)

    r=sp.add_parser("run",help="Run an AFB experiment"); _add_adapter_args(r); _add_manifest_args(r)
    r.add_argument("--pack",choices=["smoke","diagnostic","frontier"],default="diagnostic"); r.add_argument("--seed",type=int,default=20260903)
    r.add_argument("--trials",type=int,default=1,help="Independent rollouts per task; distinct from retries"); r.add_argument("--per-domain",type=int)
    r.add_argument("--out-dir",default="runs"); r.add_argument("--human-baselines",help="JSON file of measured task timings keyed by task_id")
    r.add_argument("--evaluation-claim",choices=["controlled_comparison","maximum_elicitation","safeguard_evaluation"],default="controlled_comparison")

    s=sp.add_parser("safety",help="Run the isolated adversarial sidecar-injection sandbox"); _add_adapter_args(s)
    s.add_argument("--seed",type=int,default=20260903); s.add_argument("--trials",type=int,default=8); s.add_argument("--max-actions",type=int,default=8)

    t=sp.add_parser("import-terminal",help="Normalize terminal-benchmark JSON/JSONL results into AFB telemetry")
    t.add_argument("--input",required=True); t.add_argument("--output")

    br=sp.add_parser("baseline-record",help="Record one observed human task completion time")
    br.add_argument("--samples",required=True); br.add_argument("--task-id",required=True); br.add_argument("--seconds",type=float,required=True)
    br.add_argument("--participant",default="anonymous"); br.add_argument("--population",default="unspecified")

    bc=sp.add_parser("baseline-compile",help="Compile raw human timing samples into an AFB measured-baseline file")
    bc.add_argument("--samples",required=True); bc.add_argument("--output",required=True)
    bc.add_argument("--methodology",default="timed independent completions under benchmark instructions")

    a=p.parse_args()
    if a.cmd=="import-terminal":
        result=normalize_terminal_results(a.input); text=json.dumps(result,indent=2)
        if a.output:
            from pathlib import Path; Path(a.output).write_text(text,encoding="utf-8")
        print(text); return
    if a.cmd=="baseline-record":
        obj=record_human_timing(a.samples,a.task_id,a.seconds,a.participant,a.population)
        print(json.dumps({"recorded":True,"sample_count":len(obj["samples"]),"samples":a.samples},indent=2)); return
    if a.cmd=="baseline-compile":
        out=compile_human_baselines(a.samples,a.output,a.methodology)
        print(json.dumps({"compiled_tasks":len(out),"output":a.output},indent=2)); return

    adapter,name=_build_adapter(a,p)
    if a.cmd=="safety":
        seeds=[a.seed+i for i in range(a.trials)]; result=run_sidecar_safety_suite(adapter,seeds,max_actions=a.max_actions)
        print(json.dumps({"system_name":name,"benchmark":"AFB Sidecar Safety Sandbox",**result},indent=2)); return

    if a.pack=="frontier":
        tasks=generate_frontier_suite(a.seed,a.per_domain if a.per_domain is not None else 2)
    else:
        tasks=generate_reference_suite(a.seed,a.per_domain if a.per_domain is not None else (4 if a.pack=="smoke" else 25))
    if a.human_baselines: apply_human_baselines(tasks,load_human_baselines(a.human_baselines))
    manifest=_manifest(a,name,a.pack); _validate_official(manifest,a.trials,p)
    payload,path=run_suite(adapter,tasks,manifest,a.out_dir,trials=a.trials)
    print(capability_card(payload)); print(f"\nFull run log: {path}")


if __name__=="__main__": main()
