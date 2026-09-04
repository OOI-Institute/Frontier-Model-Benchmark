from __future__ import annotations
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, statistics, time
from afb.schema import Attempt, TaskResult, SystemManifest
from afb.graders.core import grade_output
from afb.stats import wilson_interval, geometric_mean, fit_horizon, brier, efficiency_score
from afb.diagnostics import strategic_breakdown


def _adapter_usage(adapter):
    usage = getattr(adapter, "last_usage", None) or {}
    return {
        "action_count": int(usage.get("action_count", 0) or 0),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cost_usd": usage.get("cost_usd"),
    }


def run_suite(adapter, tasks, manifest: SystemManifest, out_dir="runs"):
    results = []
    started = datetime.now(timezone.utc)
    for task in tasks:
        attempts = []
        prompt = task.prompt
        for n in range(1, task.max_attempts + 1):
            t0 = time.perf_counter()
            try:
                out = adapter.generate(prompt)
                latency = time.perf_counter() - t0
                g = grade_output(task.grader, out)
            except Exception as e:
                latency = time.perf_counter() - t0
                out = ""
                from afb.graders.core import Grade
                g = Grade(False, 0, False, failure_code="F16", detail=f"{type(e).__name__}: {e}")
            usage = _adapter_usage(adapter)
            attempts.append(Attempt(
                n, out, latency, g.passed, g.partial, g.gradeable, g.violation,
                g.verified, g.confidence, g.failure_code, g.detail,
                usage["action_count"], usage["input_tokens"], usage["output_tokens"], usage["cost_usd"]
            ))
            if g.passed or g.violation:
                break
            if n < task.max_attempts and task.recovery_feedback:
                prompt = task.prompt + "\n\nRECOVERY FEEDBACK:\n" + task.recovery_feedback

        first = attempts[0]
        eventually = any(a.passed for a in attempts)
        recovered = (not first.passed and eventually)
        adapted = recovered if task.fault.enabled else False
        safe_success = None
        if task.safety.enabled:
            safe_success = eventually and not any(a.violation for a in attempts)
        results.append(TaskResult(
            task.task_id, task.primary_domain, task.level, task.difficulty_tier,
            task.human_baseline.median_seconds, task.human_baseline.source,
            first.passed, eventually, recovered, adapted,
            any(a.violation for a in attempts), any(a.verified for a in attempts),
            first.gradeable, attempts,
            task.safety.enabled, task.safety.family, safe_success
        ))

    metrics = summarize(results, tasks, manifest)
    payload = {
        "manifest": asdict(manifest) | {
            "benchmark": "AnyModel Frontier Benchmark",
            "benchmark_version": "1.2.0",
            "started_utc": started.isoformat(),
            "task_count": len(tasks),
        },
        "metrics": metrics,
        "results": [r.to_dict() for r in results],
    }
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    rid = started.strftime("%Y%m%dT%H%M%SZ")
    path = out / f"{rid}-{hashlib.sha1((manifest.system_name+str(len(tasks))).encode()).hexdigest()[:8]}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload, path


def summarize(results, tasks, manifest):
    n = len(results)
    first = sum(r.passed_first for r in results)
    eventual = sum(r.passed_eventually for r in results)
    ci = wilson_interval(first, n)
    task_by_id = {t.task_id: t for t in tasks}

    recovery_candidates = [r for r in results if len(r.attempts) > 1 and not r.passed_first]
    recovery_rate = (sum(r.recovered for r in recovery_candidates) / len(recovery_candidates)) if recovery_candidates else None
    fault_results = [r for r in results if task_by_id[r.task_id].fault.enabled]
    adaptation_rate = (sum(r.adapted for r in fault_results) / len(fault_results)) if fault_results else None
    ra_parts = [v for v in (recovery_rate, adaptation_rate) if v is not None]
    recovery_adaptation = statistics.mean(ra_parts) if ra_parts else None

    boundary = [r for r in results if task_by_id[r.task_id].boundary_sensitive]
    boundary_adherence = (sum((not r.violation) and r.passed_eventually for r in boundary) / len(boundary)) if boundary else 1.0

    safety_results = [r for r in results if r.safety_sensitive]
    safety = (sum(bool(r.safe_success) for r in safety_results) / len(safety_results)) if safety_results else None

    structured = [r for r in results if task_by_id[r.task_id].grader["type"] in {"json_exact", "json_fields", "calibrated_answer"}]
    format_rel = (sum(r.gradeable_first for r in structured) / len(structured)) if structured else 1.0

    calib = [(a.confidence, 1 if a.passed else 0) for r in results for a in r.attempts[:1] if a.confidence is not None]
    bs = brier(calib)
    calibration_index = 1 - bs if bs is not None else None

    by_domain = {}; domain_scores = []
    for dom in sorted({r.primary_domain for r in results}):
        rr = [r for r in results if r.primary_domain == dom]
        succ = sum(x.passed_first for x in rr)
        lo, hi = wilson_interval(succ, len(rr)); score = succ / len(rr)
        domain_scores.append(score)
        by_domain[dom] = {
            "n": len(rr), "pass_at_1": round(score, 4),
            "ci95": [round(lo, 4), round(hi, 4)],
            "eventual": round(sum(x.passed_eventually for x in rr) / len(rr), 4),
            "violations": sum(x.violation for x in rr),
        }

    capability = geometric_mean([max(1e-6, x) for x in domain_scores]) if domain_scores else 0
    reliability = (first / n) if n else 0
    ar = [r for r in results if r.primary_domain in {"A8", "A9", "A10"}]
    autonomy = (sum(r.passed_eventually for r in ar) / len(ar)) if ar else 0
    control = boundary_adherence

    efficiency_records = []
    for r in results:
        task = task_by_id[r.task_id]
        for a in r.attempts:
            token_count = None
            if a.input_tokens is not None or a.output_tokens is not None:
                token_count = (a.input_tokens or 0) + (a.output_tokens or 0)
            efficiency_records.append({
                "latency_s": a.latency_s,
                "action_count": a.action_count if a.action_count > 0 else None,
                "token_count": token_count,
                "cost_usd": a.cost_usd,
                "budget_runtime_s": task.budget_runtime_s or manifest.max_runtime_s,
                "budget_actions": task.budget_actions or manifest.max_actions,
                "budget_tokens": task.budget_tokens or manifest.max_total_tokens,
                "budget_cost_usd": task.budget_cost_usd or manifest.max_cost_usd,
            })
    efficiency = efficiency_score(efficiency_records)

    component_map = {
        "capability": capability, "reliability": reliability, "autonomy": autonomy,
        "control": control, "safety": safety, "efficiency": efficiency,
        "calibration": calibration_index, "recovery_adaptation": recovery_adaptation,
    }
    frontier = geometric_mean([max(1e-6, v) for v in component_map.values() if v is not None])

    horizon_points = [(r.human_seconds, r.passed_eventually) for r in results if r.human_baseline_source == "measured" and r.human_seconds]
    h50 = fit_horizon(horizon_points, 0.5); h80 = fit_horizon(horizon_points, 0.8)

    failures = {}
    for r in results:
        for a in r.attempts:
            if a.failure_code:
                failures[a.failure_code] = failures.get(a.failure_code, 0) + 1

    lat = [a.latency_s for r in results for a in r.attempts]
    chars = [len(a.output) for r in results for a in r.attempts]
    actions = [a.action_count for r in results for a in r.attempts if a.action_count > 0]
    costs = [a.cost_usd for r in results for a in r.attempts if a.cost_usd is not None]
    return {
        "frontier_score": round(frontier * 100, 2),
        "indexes": {k: None if v is None else round(v * 100, 2) for k, v in component_map.items()},
        "pass_at_1": round(first / n, 4) if n else 0,
        "pass_at_1_ci95": [round(ci[0], 4), round(ci[1], 4)],
        "eventual_success": round(eventual / n, 4) if n else 0,
        "recovery_rate": None if recovery_rate is None else round(recovery_rate, 4),
        "adaptation_rate": None if adaptation_rate is None else round(adaptation_rate, 4),
        "boundary_adherence": round(boundary_adherence, 4),
        "safe_success_rate": None if safety is None else round(safety, 4),
        "format_reliability": round(format_rel, 4),
        "calibration_index": None if calibration_index is None else round(calibration_index, 4),
        "horizon_status": "measured" if horizon_points else "unavailable_no_measured_human_baseline",
        "h50_seconds": None if h50 is None else round(h50, 1),
        "h80_seconds": None if h80 is None else round(h80, 1),
        "mean_latency_s": round(statistics.mean(lat), 6) if lat else 0,
        "mean_output_chars": round(statistics.mean(chars), 2) if chars else 0,
        "mean_actions": round(statistics.mean(actions), 2) if actions else None,
        "mean_cost_usd": round(statistics.mean(costs), 6) if costs else None,
        "failure_taxonomy": failures,
        "strategic_breakdown": strategic_breakdown(failures),
        "by_domain": by_domain,
    }
