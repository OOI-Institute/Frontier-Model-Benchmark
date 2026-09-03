from __future__ import annotations
import argparse
from afb.schema import SystemManifest
from afb.packs.reference import generate_reference_suite
from afb.adapters.standard import CommandAdapter, OpenAICompatibleAdapter
from afb.oracle import OracleAdapter, WeakAdapter
from afb.runner import run_suite
from afb.report import capability_card


def main():
    p = argparse.ArgumentParser(prog="afb")
    sp = p.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run")
    r.add_argument("--adapter", choices=["oracle", "weak", "command", "openai-compatible"], required=True)
    r.add_argument("--command")
    r.add_argument("--base-url")
    r.add_argument("--model")
    r.add_argument("--provider", default="unknown")
    r.add_argument("--api-key")
    r.add_argument("--system-name", default="unnamed-system")
    r.add_argument("--evaluation-claim", choices=["controlled_comparison", "maximum_elicitation", "safeguard_evaluation"], default="controlled_comparison")
    r.add_argument("--seed", type=int, default=20260903)
    r.add_argument("--per-domain", type=int, default=25, help="25 = AFB Diagnostic-300; use 4 for Smoke-48")
    r.add_argument("--max-runtime-s", type=float)
    r.add_argument("--max-actions", type=int)
    r.add_argument("--max-total-tokens", type=int)
    r.add_argument("--max-cost-usd", type=float)
    r.add_argument("--out-dir", default="runs")
    a = p.parse_args()

    if a.adapter == "oracle":
        adapter = OracleAdapter(); name = "oracle-validator"
    elif a.adapter == "weak":
        adapter = WeakAdapter(); name = "weak-control"
    elif a.adapter == "command":
        if not a.command:
            p.error("--command required")
        adapter = CommandAdapter(a.command); name = a.system_name
    else:
        if not a.base_url or not a.model:
            p.error("--base-url and --model required")
        adapter = OpenAICompatibleAdapter(a.base_url, a.model, a.api_key); name = a.system_name

    tasks = generate_reference_suite(a.seed, a.per_domain)
    manifest = SystemManifest(
        system_name=name,
        provider=a.provider,
        base_model=a.model or "n/a",
        evaluation_claim=a.evaluation_claim,
        max_runtime_s=a.max_runtime_s,
        max_actions=a.max_actions,
        max_total_tokens=a.max_total_tokens,
        max_cost_usd=a.max_cost_usd,
    )
    payload, path = run_suite(adapter, tasks, manifest, a.out_dir)
    print(capability_card(payload))
    print(f"\nFull run log: {path}")


if __name__ == "__main__":
    main()
