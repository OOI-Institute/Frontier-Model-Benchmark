from __future__ import annotations
import json, math, statistics
from pathlib import Path
from afb.schema import HumanBaseline


def load_human_baselines(path: str):
    """Load measured human baseline metadata keyed by task_id."""
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("human baseline file must be a JSON object keyed by task_id")
    out = {}
    for task_id, row in obj.items():
        if not isinstance(row, dict):
            raise ValueError(f"baseline {task_id} must be an object")
        n = int(row.get("n", 0)); median = row.get("median_seconds")
        if n < 1 or median is None or float(median) <= 0:
            raise ValueError(f"baseline {task_id} requires n>=1 and median_seconds>0")
        out[str(task_id)] = HumanBaseline(
            source="measured", n=n, median_seconds=float(median),
            p80_seconds=None if row.get("p80_seconds") is None else float(row["p80_seconds"]),
            population=str(row.get("population", "unspecified")),
            methodology=str(row.get("methodology", "measured human timing study")),
        )
    return out


def apply_human_baselines(tasks, baselines):
    applied = 0
    for task in tasks:
        if task.task_id in baselines:
            task.human_baseline = baselines[task.task_id]; applied += 1
    return applied


def _percentile_nearest_rank(values, q: float):
    xs = sorted(float(x) for x in values)
    if not xs: return None
    idx = max(0, min(len(xs)-1, math.ceil(q * len(xs)) - 1))
    return xs[idx]


def record_human_timing(samples_path: str, task_id: str, seconds: float,
                        participant: str = "anonymous", population: str = "unspecified"):
    """Append one genuinely observed human completion time to a local/public sample file.

    This function never invents measurements. Callers must supply an observed elapsed time.
    """
    if seconds <= 0: raise ValueError("seconds must be > 0")
    p = Path(samples_path)
    if p.exists() and p.read_text(encoding="utf-8").strip():
        obj = json.loads(p.read_text(encoding="utf-8"))
    else:
        obj = {"schema_version":"1.0", "samples":[]}
    if not isinstance(obj, dict) or not isinstance(obj.get("samples", []), list):
        raise ValueError("timing sample file must contain a samples list")
    obj.setdefault("schema_version", "1.0")
    obj.setdefault("samples", []).append({
        "task_id": str(task_id), "seconds": float(seconds),
        "participant": str(participant), "population": str(population),
    })
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return obj


def compile_human_baselines(samples_path: str, output_path: str | None = None,
                            methodology: str = "timed independent completions under benchmark instructions"):
    """Compile raw observed timing samples into the baseline file consumed by AFB."""
    obj = json.loads(Path(samples_path).read_text(encoding="utf-8"))
    samples = obj.get("samples", []) if isinstance(obj, dict) else []
    grouped = {}
    for row in samples:
        task_id = str(row["task_id"]); seconds = float(row["seconds"])
        if seconds <= 0: raise ValueError(f"invalid timing for {task_id}")
        grouped.setdefault(task_id, []).append(row)
    out = {}
    for task_id, rows in grouped.items():
        values = [float(r["seconds"]) for r in rows]
        populations = sorted({str(r.get("population", "unspecified")) for r in rows})
        out[task_id] = {
            "n": len(values),
            "median_seconds": statistics.median(values),
            "p80_seconds": _percentile_nearest_rank(values, 0.8),
            "population": populations[0] if len(populations) == 1 else "mixed: " + ", ".join(populations),
            "methodology": methodology,
        }
    if output_path:
        Path(output_path).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out
