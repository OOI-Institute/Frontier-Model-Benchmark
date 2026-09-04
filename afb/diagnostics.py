from __future__ import annotations

FAILURE_LABELS = {
    "F01": "Comprehension",
    "F02": "Instruction adherence",
    "F03": "Reasoning",
    "F04": "Planning",
    "F05": "Tool selection",
    "F06": "Tool execution",
    "F07": "State tracking",
    "F08": "Memory",
    "F09": "Verification",
    "F10": "Recovery",
    "F11": "Calibration / hallucination",
    "F12": "Premature completion",
    "F13": "Constraint violation",
    "F14": "Authority / control",
    "F15": "Reward hacking / grader gaming",
    "F16": "Resource / runtime",
    "F17": "Environment understanding",
    "F18": "Format / communication",
}


def strategic_breakdown(failure_counts: dict[str, int]) -> dict[str, dict[str, float | int]]:
    """Convert deterministic failure-code counts into an engineering-facing profile."""
    total = sum(max(0, int(v)) for v in failure_counts.values())
    if total == 0:
        return {}
    out = {}
    for code, count in sorted(failure_counts.items()):
        c = max(0, int(count))
        if c == 0:
            continue
        label = FAILURE_LABELS.get(code, code)
        out[label] = {
            "code": code,
            "count": c,
            "share": round(c / total, 4),
        }
    return dict(sorted(out.items(), key=lambda item: item[1]["count"], reverse=True))
