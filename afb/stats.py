from __future__ import annotations
import math, statistics


def wilson_interval(successes: int, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 0.0)
    phat = successes / n
    den = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / den
    half = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / den
    return max(0, center - half), min(1, center + half)


def geometric_mean(scores, weights=None):
    xs = [max(1e-9, float(x)) for x in scores]
    if weights is None:
        weights = [1 / len(xs)] * len(xs)
    return math.exp(sum(w * math.log(x) for x, w in zip(xs, weights)))


def efficiency_score(records):
    """
    Budget-relative efficiency score for completed attempts.

    Each record may contain latency_s/action_count/token_count/cost_usd and
    corresponding budgets. Missing dimensions are ignored rather than awarded a
    perfect score. Returns None when no usable budgeted dimension is available.
    """
    attempt_scores = []
    for r in records:
        ratios = []
        dimensions = (
            (r.get("latency_s"), r.get("budget_runtime_s")),
            (r.get("action_count"), r.get("budget_actions")),
            (r.get("token_count"), r.get("budget_tokens")),
            (r.get("cost_usd"), r.get("budget_cost_usd")),
        )
        for used, budget in dimensions:
            if used is None or budget is None or budget <= 0:
                continue
            used = max(float(used), 1e-9)
            ratios.append(min(1.0, float(budget) / used))
        if ratios:
            attempt_scores.append(geometric_mean(ratios))
    return statistics.mean(attempt_scores) if attempt_scores else None


def fit_horizon(points, target=0.5):
    """Fit success over log measured-human task duration using a simple grid search."""
    pts = [(max(1.0, float(t)), 1.0 if y else 0.0) for t, y in points if t]
    if len(pts) < 4 or len({y for _, y in pts}) < 2:
        return None
    xs = [math.log(t) for t, _ in pts]
    ys = [y for _, y in pts]
    best = None
    for a in [x / 4 for x in range(-40, 41)]:
        for b in [x / 4 for x in range(-24, 1) if x != 0]:
            loss = 0
            for x, y in zip(xs, ys):
                p = 1 / (1 + math.exp(-(a + b * x)))
                p = min(max(p, 1e-9), 1 - 1e-9)
                loss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
            if best is None or loss < best[0]:
                best = (loss, a, b)
    _, a, b = best
    logt = (math.log(target / (1 - target)) - a) / b
    return math.exp(logt)


def brier(pairs):
    vals = [(p - y) ** 2 for p, y in pairs if p is not None]
    return statistics.mean(vals) if vals else None
