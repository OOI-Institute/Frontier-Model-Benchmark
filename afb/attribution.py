from __future__ import annotations
from afb.schema import ContributionResult


def contribution_delta(baseline_payload, comparison_payload, component: str, metric: str = "frontier_score"):
    """Compare two matched AFB run payloads and attribute the delta to a declared component.

    This function does not infer causality. The caller is responsible for ensuring the
    configurations are matched except for the declared component change.
    """
    bman = baseline_payload["manifest"]
    cman = comparison_payload["manifest"]
    b = float(baseline_payload["metrics"][metric])
    c = float(comparison_payload["metrics"][metric])
    delta = c - b
    rel = None if b == 0 else delta / abs(b)
    return ContributionResult(
        component=component,
        baseline_system=bman.get("system_name", "baseline"),
        comparison_system=cman.get("system_name", "comparison"),
        baseline_score=b,
        comparison_score=c,
        absolute_delta=round(delta, 4),
        relative_delta=None if rel is None else round(rel, 6),
        metric=metric,
    )


def contribution_series(payloads, components, metric: str = "frontier_score"):
    """Create sequential ablation deltas for base -> component-added configurations."""
    if len(payloads) < 2:
        return []
    if len(components) != len(payloads) - 1:
        raise ValueError("components must describe each transition between payloads")
    return [
        contribution_delta(payloads[i], payloads[i + 1], components[i], metric)
        for i in range(len(components))
    ]
