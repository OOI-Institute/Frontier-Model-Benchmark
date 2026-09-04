from __future__ import annotations
import json
from pathlib import Path
from afb.schema import HumanBaseline


def load_human_baselines(path: str):
    """Load measured human baseline metadata keyed by task_id.

    File format:
    {
      "TASK-ID": {
        "n": 8,
        "median_seconds": 900,
        "p80_seconds": 1200,
        "population": "professional operators",
        "methodology": "timed independent completions"
      }
    }
    """
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("human baseline file must be a JSON object keyed by task_id")
    out = {}
    for task_id, row in obj.items():
        if not isinstance(row, dict):
            raise ValueError(f"baseline {task_id} must be an object")
        n = int(row.get("n", 0))
        median = row.get("median_seconds")
        if n < 1 or median is None or float(median) <= 0:
            raise ValueError(f"baseline {task_id} requires n>=1 and median_seconds>0")
        out[str(task_id)] = HumanBaseline(
            source="measured",
            n=n,
            median_seconds=float(median),
            p80_seconds=None if row.get("p80_seconds") is None else float(row["p80_seconds"]),
            population=str(row.get("population", "unspecified")),
            methodology=str(row.get("methodology", "measured human timing study")),
        )
    return out


def apply_human_baselines(tasks, baselines):
    applied = 0
    for task in tasks:
        if task.task_id in baselines:
            task.human_baseline = baselines[task.task_id]
            applied += 1
    return applied
