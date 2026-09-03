from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Observation:
    text: str
    state: dict[str,Any] = field(default_factory=dict)
    terminal: bool = False

@dataclass
class ActionResult:
    observation: Observation
    valid: bool = True
    violation: bool = False
    detail: str = ""

class Environment:
    """
    Interface for AFB Level 3/4 execution packs.

    A real environment must support reproducible reset and observable terminal state.
    """
    name="environment"

    def reset(self, seed:int) -> Observation:
        raise NotImplementedError

    def step(self, action:dict[str,Any]) -> ActionResult:
        raise NotImplementedError

    def terminal_state(self) -> dict[str,Any]:
        raise NotImplementedError

    def inject_fault(self, spec:dict[str,Any]) -> None:
        """Optional controlled environment mutation."""
        return None
