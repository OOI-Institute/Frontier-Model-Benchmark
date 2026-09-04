from __future__ import annotations


def capability_card(payload):
    m = payload["metrics"]
    man = payload["manifest"]
    idx = m["indexes"]

    def dur(sec):
        if sec is None: return "N/A"
        if sec < 60: return f"{sec:.0f}s"
        if sec < 3600: return f"{sec/60:.1f}m"
        return f"{sec/3600:.1f}h"

    def score(v):
        return "N/A" if v is None else f"{v:.1f}"

    dimensions = [
        ("Safety", idx.get("safety")),
        ("Capability", idx.get("capability")),
        ("Reliability", idx.get("reliability")),
        ("Autonomy", idx.get("autonomy")),
        ("Control", idx.get("control")),
        ("Efficiency", idx.get("efficiency")),
        ("Calibration", idx.get("calibration")),
        ("Recovery / Adaptation", idx.get("recovery_adaptation")),
    ]

    lines = [
        f"# AFB AI Capability Card — {man['system_name']}", "",
        f"**Evaluation claim:** {man.get('evaluation_claim', 'controlled_comparison')}",
        f"**Frontier Score:** {m['frontier_score']:.1f}/100", "",
        "| Dimension | Score |", "|---|---:|",
    ]
    lines.extend(f"| {name} | {score(value)} |" for name, value in dimensions)
    lines.extend([
        "",
        f"**Pass@1:** {100*m['pass_at_1']:.1f}% (95% CI {100*m['pass_at_1_ci95'][0]:.1f}–{100*m['pass_at_1_ci95'][1]:.1f}%)",
        f"**Eventual success:** {100*m['eventual_success']:.1f}%",
        f"**Boundary adherence:** {100*m['boundary_adherence']:.1f}%",
    ])
    if m.get("safe_success_rate") is not None:
        lines.append(f"**Safe successful completion:** {100*m['safe_success_rate']:.1f}%")
    if m.get("horizon_status") == "measured":
        lines.extend([f"**H50 task horizon:** {dur(m['h50_seconds'])}", f"**H80 task horizon:** {dur(m['h80_seconds'])}"])
    else:
        lines.append("**Task horizon:** N/A — no eligible measured human baseline data")

    lines.extend(["", "## Strategic Breakdown"])
    sb = m.get("strategic_breakdown") or {}
    if not sb:
        lines.append("No categorized failures in this run.")
    else:
        for label, v in sb.items():
            lines.append(f"- {label}: {100*v['share']:.1f}% ({v['count']})")

    lines.extend(["", "## Domain scores"])
    for d, v in sorted(m["by_domain"].items()):
        lines.append(f"- {d}: {100*v['pass_at_1']:.1f}%")
    return "\n".join(lines)
