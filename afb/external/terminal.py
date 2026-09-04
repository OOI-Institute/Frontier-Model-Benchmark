from __future__ import annotations
import json
from pathlib import Path
from statistics import mean


def _load_records(path: str):
    p = Path(path)
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("["):
        obj = json.loads(text)
        if not isinstance(obj, list):
            raise ValueError("terminal result JSON must be a list")
        return obj
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def normalize_terminal_results(path: str):
    """Normalize terminal-style benchmark result JSON/JSONL into AFB telemetry.

    Accepted record fields are intentionally permissive so exporters can map from
    Terminal-Bench/Harbor-like runners without changing AFB internals:
      task_id|id, passed|success, reward, duration_s|latency_s,
      actions|agent_steps, input_tokens, output_tokens, cost_usd, seed.

    If passed/success is absent, reward >= 1.0 is treated as success. Raw records are
    preserved for auditability.
    """
    raw = _load_records(path)
    rows = []
    for i, r in enumerate(raw):
        task_id = str(r.get("task_id") or r.get("id") or f"terminal-{i:04d}")
        passed = r.get("passed")
        if passed is None:
            passed = r.get("success")
        if passed is None:
            reward = r.get("reward")
            passed = bool(reward is not None and float(reward) >= 1.0)
        rows.append({
            "task_id": task_id,
            "passed": bool(passed),
            "duration_s": r.get("duration_s", r.get("latency_s")),
            "actions": r.get("actions", r.get("agent_steps")),
            "input_tokens": r.get("input_tokens"),
            "output_tokens": r.get("output_tokens"),
            "cost_usd": r.get("cost_usd"),
            "seed": r.get("seed"),
            "raw": r,
        })
    n = len(rows)
    durations = [float(x["duration_s"]) for x in rows if x["duration_s"] is not None]
    actions = [float(x["actions"]) for x in rows if x["actions"] is not None]
    costs = [float(x["cost_usd"]) for x in rows if x["cost_usd"] is not None]
    return {
        "adapter": "afb.external.terminal",
        "schema_version": "1.0",
        "n": n,
        "pass_rate": None if not n else round(sum(x["passed"] for x in rows) / n, 4),
        "mean_duration_s": None if not durations else round(mean(durations), 6),
        "mean_actions": None if not actions else round(mean(actions), 3),
        "mean_cost_usd": None if not costs else round(mean(costs), 6),
        "records": rows,
    }
