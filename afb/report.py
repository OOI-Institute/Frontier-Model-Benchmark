from __future__ import annotations


def capability_card(payload):
    m = payload["metrics"]
    man = payload["manifest"]
    idx = m["indexes"]

    def dur(sec):
        if sec is None:
            return "N/A"
        if sec < 60:
            return f"{sec:.0f}s"
        if sec < 3600:
            return f"{sec/60:.1f}m"
        return f"{sec/3600:.1f}h"

    def score(v):
        return "N/A" if v is None else f"{v:.1f}"

    lines = [
        f"# AFB AI Capability Card — {man['system_name']}",
        "",
        f"**Evaluation claim:** {man.get('evaluation_claim', 'controlled_comparison')}",
        f"**Frontier Score:** {m['frontier_score']:.1f}/100",
        "",
        "| Dimension | Score |",
        "|---|---:|",
        f"| Capability | {score(idx['capability'])} |",
        f"| Reliability | {score(idx['reliability'])} |",
        f"| Autonomy | {score(idx['autonomy'])} |",
        f"| Control | {score(idx['control'])} |",
        f"| Efficiency | {score(idx['efficiency'])} |",
        "",
        f"**Pass@1:** {100*m['pass_at_1']:.1f}% (95% CI {100*m['pass_at_1_ci95'][0]:.1f}–{100*m['pass_at_1_ci95'][1]:.1f}%)",
        f"**Eventual success:** {100*m['eventual_success']:.1f}%",
        f"**Boundary adherence:** {100*m['boundary_adherence']:.1f}%",
    ]

    if m.get("horizon_status") == "measured":
        lines.extend([
            f"**H50 task horizon:** {dur(m['h50_seconds'])}",
            f"**H80 task horizon:** {dur(m['h80_seconds'])}",
        ])
    else:
        lines.append("**Task horizon:** N/A — no eligible measured human baseline data")

    if idx.get("efficiency") is None:
        lines.append("**Efficiency:** N/A — no comparable runtime/action/token/cost budget was supplied")

    lines.extend(["", "## Domain scores"])
    for d, v in sorted(m["by_domain"].items()):
        lines.append(f"- {d}: {100*v['pass_at_1']:.1f}%")
    return "\n".join(lines)
