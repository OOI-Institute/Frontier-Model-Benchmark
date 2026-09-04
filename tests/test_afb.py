from afb.packs.reference import generate_reference_suite
from afb.oracle import OracleAdapter, WeakAdapter
from afb.schema import SystemManifest
from afb.runner import run_suite
from afb.stats import efficiency_score
from afb.diagnostics import strategic_breakdown
from afb.attribution import contribution_delta
from afb.safety import run_sidecar_safety_suite
import tempfile, json, re


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
        assert "calibration" in p["metrics"]["indexes"]
        assert "recovery_adaptation" in p["metrics"]["indexes"]
        assert "strategic_breakdown" in p["metrics"]


def test_weak_discriminates():
    with tempfile.TemporaryDirectory() as d:
        p, _ = run_suite(WeakAdapter(), generate_reference_suite(123, 2), SystemManifest("weak"), d)
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
        if self.step == 1:
            return json.dumps({"op": "read_supplier_status"})
        if self.step == 2:
            return json.dumps({"op": "report", "status": self.status})
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
