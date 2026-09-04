from afb.packs.reference import generate_reference_suite
from afb.packs.frontier import generate_frontier_suite
from afb.oracle import OracleAdapter, WeakAdapter
from afb.schema import SystemManifest
from afb.runner import run_suite
from afb.stats import efficiency_score
from afb.diagnostics import strategic_breakdown
from afb.attribution import contribution_delta
from afb.safety import run_sidecar_safety_suite
from afb.baselines import load_human_baselines, apply_human_baselines
from afb.external.terminal import normalize_terminal_results
import tempfile, json, re
from pathlib import Path


def test_reproducible():
    a = generate_reference_suite(123, 2)
    b = generate_reference_suite(123, 2)
    assert [(x.task_id, x.prompt, x.grader) for x in a] == [(x.task_id, x.prompt, x.grader) for x in b]


def test_oracle():
    with tempfile.TemporaryDirectory() as d:
        p, _ = run_suite(OracleAdapter(), generate_reference_suite(123, 2), SystemManifest("oracle"), d)
        assert p["metrics"]["pass_at_1"] == 1.0
        assert p["metrics"]["horizon_status"] == "unavailable_no_measured_human_baseline"
        assert p["metrics"]["indexes"]["efficiency"] is None
        assert p["metrics"]["frontier_score"] is None


def test_multitrial_experiment_separates_trials_from_retries():
    with tempfile.TemporaryDirectory() as d:
        tasks = generate_reference_suite(123, 1)
        p, _ = run_suite(OracleAdapter(), tasks, SystemManifest("oracle"), d, trials=3)
        assert p["manifest"]["trial_count"] == 3
        assert p["manifest"]["rollout_count"] == len(tasks) * 3
        assert p["metrics"]["trial_consistency"] == 1.0
        assert all(x["trial_index"] in {0, 1, 2} for x in p["results"])


def test_weak_discriminates():
    with tempfile.TemporaryDirectory() as d:
        p, _ = run_suite(WeakAdapter(), generate_reference_suite(123, 2), SystemManifest("weak"), d, trials=2)
        assert p["metrics"]["pass_at_1"] < 0.5


def test_reference_baselines_are_estimated_not_measured():
    tasks = generate_reference_suite(123, 1)
    assert all(t.human_baseline.source == "estimated" for t in tasks)
    assert not any(t.human_baseline.horizon_eligible for t in tasks)


def test_efficiency_requires_budget():
    assert efficiency_score([{"latency_s": 1.0, "budget_runtime_s": None}]) is None


def test_efficiency_scores_budget_compliance():
    assert efficiency_score([{"latency_s": 2.0, "budget_runtime_s": 4.0}]) == 1.0


def test_efficiency_penalizes_budget_overrun():
    score = efficiency_score([{"latency_s": 8.0, "budget_runtime_s": 4.0}])
    assert abs(score - 0.5) < 1e-9


def test_evaluation_claim_is_serialized():
    with tempfile.TemporaryDirectory() as d:
        manifest = SystemManifest("oracle", evaluation_claim="maximum_elicitation")
        p, _ = run_suite(OracleAdapter(), generate_reference_suite(321, 1), manifest, d)
        assert p["manifest"]["evaluation_claim"] == "maximum_elicitation"


def test_official_manifest_detects_missing_fields():
    m = SystemManifest("unnamed-system", official=True)
    missing = m.official_missing_fields()
    assert "provider" in missing
    assert "system_prompt_hash" in missing
    assert "at_least_one_budget" in missing


def test_strategic_breakdown_normalizes():
    out = strategic_breakdown({"F03": 3, "F04": 1})
    assert out["Reasoning"]["share"] == 0.75
    assert out["Planning"]["share"] == 0.25


def test_contribution_delta():
    base = {"manifest": {"system_name": "base"}, "metrics": {"frontier_score": 60.0}}
    full = {"manifest": {"system_name": "full"}, "metrics": {"frontier_score": 72.0}}
    r = contribution_delta(base, full, "tools")
    assert r.absolute_delta == 12.0
    assert r.relative_delta == 0.2


class SafeSidecarAdapter:
    def __init__(self):
        self.step = 0
        self.status = None
    def generate(self, prompt):
        if self.status is None:
            m = re.search(r"supplier_status=([a-z]+)", prompt)
            self.status = m.group(1) if m else "pending"
        self.step += 1
        if self.step == 1: return json.dumps({"op": "read_supplier_status"})
        if self.step == 2: return json.dumps({"op": "report", "status": self.status})
        return json.dumps({"op": "finish"})


class UnsafeSidecarAdapter:
    def generate(self, prompt):
        return json.dumps({"op": "access_protected"})


def test_sidecar_safety_sandbox_rewards_safe_completion():
    r = run_sidecar_safety_suite(SafeSidecarAdapter(), [1])
    assert r["safe_success_rate"] == 1.0
    assert r["injection_resistance"] == 1.0


def test_sidecar_safety_sandbox_detects_violation():
    r = run_sidecar_safety_suite(UnsafeSidecarAdapter(), [1])
    assert r["safe_success_rate"] == 0.0
    assert r["violation_rate"] == 1.0


class EnvironmentAgent:
    """Deterministic positive control for public interactive AFB environments."""
    def generate(self, prompt):
        state_match = re.search(r"State:\n(\{.*\})", prompt, re.S)
        state = json.loads(state_match.group(1)) if state_match else {}
        if "supplier_status" in state:
            if state.get("reported_status") is None:
                return json.dumps({"op": "report", "status": state["supplier_status"]})
            return json.dumps({"op": "finish"})
        target = state.get("target")
        if target is None:
            return json.dumps({"op": "read", "asset": "inventory"})
        if state.get("inventory") != target:
            return json.dumps({"op": "set_inventory", "value": target})
        if not state.get("verified"):
            return json.dumps({"op": "verify"})
        return json.dumps({"op": "finish"})


def test_frontier_pack_uses_real_environment_loops():
    tasks = [t for t in generate_frontier_suite(77, 1) if t.primary_domain in {"A8", "A9", "A10", "A12"}]
    assert all(t.metadata.get("execution") == "environment" for t in tasks)
    with tempfile.TemporaryDirectory() as d:
        manifest = SystemManifest("env-positive-control", pack="frontier", max_actions=12)
        p, _ = run_suite(EnvironmentAgent(), tasks, manifest, d, trials=3)
        assert p["metrics"]["pass_at_1"] == 1.0
        assert p["metrics"]["trial_consistency"] == 1.0
        assert p["metrics"]["adaptation_rate"] == 1.0
        assert p["metrics"]["safe_success_rate"] == 1.0
        assert all(x["result"]["trajectory"] for x in p["results"])


def test_measured_baseline_loader():
    tasks = generate_reference_suite(55, 1)
    target = tasks[0].task_id
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "baselines.json"
        path.write_text(json.dumps({target: {"n": 5, "median_seconds": 120, "p80_seconds": 180, "population": "testers"}}))
        baselines = load_human_baselines(str(path))
        assert apply_human_baselines(tasks, baselines) == 1
        assert tasks[0].human_baseline.source == "measured"
        assert tasks[0].human_baseline.horizon_eligible


def test_terminal_results_adapter():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "terminal.jsonl"
        path.write_text('\n'.join([
            json.dumps({"task_id": "t1", "passed": True, "duration_s": 10, "agent_steps": 4}),
            json.dumps({"task_id": "t2", "reward": 0, "duration_s": 20, "agent_steps": 6}),
        ]))
        out = normalize_terminal_results(str(path))
        assert out["n"] == 2
        assert out["pass_rate"] == 0.5
        assert out["mean_actions"] == 5.0
