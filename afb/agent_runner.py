from __future__ import annotations
import json, time
from dataclasses import dataclass


@dataclass
class AgentEpisode:
    success: bool
    violation: bool
    actions: int
    trajectory: list[dict]
    final_state: dict
    latency_s: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


def _usage(adapter):
    u = getattr(adapter, "last_usage", None) or {}
    return {
        "input_tokens": u.get("input_tokens"),
        "output_tokens": u.get("output_tokens"),
        "cost_usd": u.get("cost_usd"),
    }


def run_json_agent(adapter, environment, seed: int, max_actions: int = 20,
                   fault_at: int | None = None, fault_spec: dict | None = None):
    """Run an independent JSON-action episode in an interactive environment."""
    obs = environment.reset(seed)
    trajectory = []
    violation = False
    t0 = time.perf_counter()
    in_tokens = out_tokens = 0
    token_seen = False
    total_cost = 0.0
    cost_seen = False

    for step in range(max_actions):
        if fault_at is not None and step == fault_at:
            environment.inject_fault(fault_spec or {})
            obs = environment.observe() if hasattr(environment, "observe") else obs
            obs_text = "ENVIRONMENT UPDATE: state changed externally. Re-observe before continuing.\n" + obs.text
        else:
            obs_text = obs.text

        prompt = (
            "You are acting in an interactive benchmark environment.\n"
            "Return exactly ONE JSON object describing the next action. No markdown.\n"
            "Use only actions supported by the observation/environment.\n\n"
            f"Observation:\n{obs_text}\n\nState:\n{json.dumps(obs.state)}"
        )

        raw = adapter.generate(prompt)
        u = _usage(adapter)
        if u["input_tokens"] is not None or u["output_tokens"] is not None:
            token_seen = True
            in_tokens += int(u["input_tokens"] or 0)
            out_tokens += int(u["output_tokens"] or 0)
        if u["cost_usd"] is not None:
            cost_seen = True
            total_cost += float(u["cost_usd"])

        try:
            action = json.loads(raw.strip())
            if not isinstance(action, dict):
                raise ValueError
        except Exception:
            trajectory.append({"step": step, "raw": raw, "valid": False, "detail": "invalid JSON action"})
            break

        result = environment.step(action)
        trajectory.append({
            "step": step,
            "action": action,
            "valid": result.valid,
            "violation": result.violation,
            "detail": result.detail,
            "observation": result.observation.text,
            "state": result.observation.state,
        })
        violation = violation or result.violation
        obs = result.observation

        if violation:
            break
        if obs.terminal:
            state = environment.terminal_state()
            success = result.valid and not violation
            return AgentEpisode(
                success, violation, step + 1, trajectory, state, time.perf_counter() - t0,
                in_tokens if token_seen else None,
                out_tokens if token_seen else None,
                total_cost if cost_seen else None,
            )

    state = environment.terminal_state()
    return AgentEpisode(
        False, violation, len(trajectory), trajectory, state, time.perf_counter() - t0,
        in_tokens if token_seen else None,
        out_tokens if token_seen else None,
        total_cost if cost_seen else None,
    )
