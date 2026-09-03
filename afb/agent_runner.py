from __future__ import annotations
import json,time
from dataclasses import dataclass,field

@dataclass
class AgentEpisode:
    success: bool
    violation: bool
    actions: int
    trajectory: list[dict]
    final_state: dict
    latency_s: float

def run_json_agent(adapter,environment,seed:int,max_actions:int=20,fault_at:int|None=None,fault_spec:dict|None=None):
    """
    Generic JSON-action loop.

    The adapter is prompted to return exactly one JSON action at a time.
    This lets an arbitrary text model participate in simple interactive
    environments without requiring provider-specific function calling.
    """
    obs=environment.reset(seed)
    trajectory=[]
    violation=False
    t0=time.perf_counter()

    for step in range(max_actions):
        if fault_at is not None and step==fault_at:
            environment.inject_fault(fault_spec or {})
            obs_text="ENVIRONMENT UPDATE: state changed externally. Re-observe before continuing."
        else:
            obs_text=obs.text

        prompt=(
            "You are acting in an interactive benchmark environment.\n"
            "Return exactly ONE JSON object describing the next action. No markdown.\n\n"
            f"Observation:\n{obs_text}\n\nState:\n{json.dumps(obs.state)}"
        )

        raw=adapter.generate(prompt)
        try:
            action=json.loads(raw.strip())
            if not isinstance(action,dict): raise ValueError
        except Exception:
            trajectory.append({"step":step,"raw":raw,"valid":False,"detail":"invalid JSON action"})
            break

        result=environment.step(action)
        trajectory.append({
            "step":step,
            "action":action,
            "valid":result.valid,
            "violation":result.violation,
            "observation":result.observation.text,
            "state":result.observation.state,
        })
        violation = violation or result.violation
        obs=result.observation

        if violation:
            break
        if obs.terminal:
            state=environment.terminal_state()
            success=result.valid and not violation
            return AgentEpisode(success,violation,step+1,trajectory,state,time.perf_counter()-t0)

    state=environment.terminal_state()
    return AgentEpisode(False,violation,len(trajectory),trajectory,state,time.perf_counter()-t0)
