from afb.packs.reference import generate_reference_suite
from afb.oracle import OracleAdapter, WeakAdapter
from afb.schema import SystemManifest
from afb.runner import run_suite
from afb.stats import efficiency_score
import tempfile


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
    score = efficiency_score([{"latency_s": 2.0, "budget_runtime_s": 4.0}])
    assert score == 1.0


def test_efficiency_penalizes_budget_overrun():
    score = efficiency_score([{"latency_s": 8.0, "budget_runtime_s": 4.0}])
    assert abs(score - 0.5) < 1e-9


def test_evaluation_claim_is_serialized():
    with tempfile.TemporaryDirectory() as d:
        manifest = SystemManifest("oracle", evaluation_claim="maximum_elicitation")
        p, _ = run_suite(OracleAdapter(), generate_reference_suite(321, 1), manifest, d)
        assert p["manifest"]["evaluation_claim"] == "maximum_elicitation"
