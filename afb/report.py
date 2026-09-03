from __future__ import annotations
def capability_card(payload):
    m=payload["metrics"]; man=payload["manifest"]
    idx=m["indexes"]
    def dur(sec):
        if sec is None: return "N/A"
        if sec<60: return f"{sec:.0f}s"
        if sec<3600: return f"{sec/60:.1f}m"
        return f"{sec/3600:.1f}h"
    lines=[
        f"# AFB AI Capability Card — {man['system_name']}",
        "",
        f"**Frontier Score:** {m['frontier_score']:.1f}/100",
        "",
        "| Dimension | Score |",
        "|---|---:|",
        f"| Capability | {idx['capability']:.1f} |",
        f"| Reliability | {idx['reliability']:.1f} |",
        f"| Autonomy | {idx['autonomy']:.1f} |",
        f"| Control | {idx['control']:.1f} |",
        f"| Efficiency | {idx['efficiency']:.1f} |",
        "",
        f"**Pass@1:** {100*m['pass_at_1']:.1f}% "
        f"(95% CI {100*m['pass_at_1_ci95'][0]:.1f}–{100*m['pass_at_1_ci95'][1]:.1f}%)",
        f"**Eventual success:** {100*m['eventual_success']:.1f}%",
        f"**Boundary adherence:** {100*m['boundary_adherence']:.1f}%",
        f"**H50 task horizon:** {dur(m['h50_seconds'])}",
        f"**H80 task horizon:** {dur(m['h80_seconds'])}",
        "",
        "## Domain scores"
    ]
    for d,v in sorted(m["by_domain"].items()):
        lines.append(f"- {d}: {100*v['pass_at_1']:.1f}%")
    return "\n".join(lines)
