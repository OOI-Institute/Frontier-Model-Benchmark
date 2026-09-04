from __future__ import annotations
import argparse, json
from afb.schema import SystemManifest
from afb.packs.reference import generate_reference_suite
from afb.adapters.standard import CommandAdapter, OpenAICompatibleAdapter
from afb.oracle import OracleAdapter, WeakAdapter
from afb.runner import run_suite
from afb.report import capability_card
from afb.safety import run_sidecar_safety_suite


def _build_adapter(a, p):
    if a.adapter == "oracle": return OracleAdapter(), "oracle-validator"
    if a.adapter == "weak": return WeakAdapter(), "weak-control"
    if a.adapter == "command":
        if not a.command: p.error("--command required")
        return CommandAdapter(a.command), a.system_name
    if not a.base_url or not a.model: p.error("--base-url and --model required")
    return OpenAICompatibleAdapter(a.base_url, a.model, a.api_key), a.system_name


def _add_adapter_args(parser):
    parser.add_argument("--adapter", choices=["oracle", "weak", "command", "openai-compatible"], required=True)
    parser.add_argument("--command")
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--api-key")
    parser.add_argument("--system-name", default="unnamed-system")


def main():
    p = argparse.ArgumentParser(prog="afb")
    sp = p.add_subparsers(dest="cmd", required=True)

    r = sp.add_parser("run", help="Run the public diagnostic suite")
    _add_adapter_args(r)
    r.add_argument("--seed", type=int, default=20260903)
    r.add_argument("--per-domain", type=int, default=25, help="25 = AFB Diagnostic-300; use 4 for Smoke-48")
    r.add_argument("--out-dir", default="runs")
    r.add_argument("--evaluation-claim", choices=["controlled_comparison", "maximum_elicitation", "safeguard_evaluation"], default="controlled_comparison")

    s = sp.add_parser("safety", help="Run the isolated adversarial sidecar-injection sandbox")
    _add_adapter_args(s)
    s.add_argument("--seed", type=int, default=20260903)
    s.add_argument("--trials", type=int, default=8)
    s.add_argument("--max-actions", type=int, default=8)

    a = p.parse_args()
    adapter, name = _build_adapter(a, p)

    if a.cmd == "safety":
        seeds = [a.seed + i for i in range(a.trials)]
        result = run_sidecar_safety_suite(adapter, seeds, max_actions=a.max_actions)
        print(json.dumps({"system_name": name, "benchmark": "AFB Sidecar Safety Sandbox", **result}, indent=2))
        return

    tasks = generate_reference_suite(a.seed, a.per_domain)
    manifest = SystemManifest(
        system_name=name,
        base_model=a.model or "n/a",
        evaluation_claim=a.evaluation_claim,
    )
    payload, path = run_suite(adapter, tasks, manifest, a.out_dir)
    print(capability_card(payload))
    print(f"\nFull run log: {path}")


if __name__ == "__main__":
    main()
