from afb.packs.reference import generate_reference_suite
from afb.oracle import OracleAdapter,WeakAdapter
from afb.schema import SystemManifest
from afb.runner import run_suite
import tempfile

def test_reproducible():
    a=generate_reference_suite(123,2)
    b=generate_reference_suite(123,2)
    assert [(x.task_id,x.prompt,x.grader) for x in a]==[(x.task_id,x.prompt,x.grader) for x in b]

def test_oracle():
    with tempfile.TemporaryDirectory() as d:
        p,_=run_suite(OracleAdapter(),generate_reference_suite(123,2),SystemManifest("oracle"),d)
        assert p["metrics"]["pass_at_1"]==1.0

def test_weak_discriminates():
    with tempfile.TemporaryDirectory() as d:
        p,_=run_suite(WeakAdapter(),generate_reference_suite(123,2),SystemManifest("weak"),d)
        assert p["metrics"]["pass_at_1"] < 0.5
