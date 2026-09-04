from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Literal

Level = Literal["core", "tool", "agent", "autonomous"]
EvaluationClaim = Literal["controlled_comparison", "maximum_elicitation", "safeguard_evaluation"]
BaselineSource = Literal["measured", "estimated", "none"]
SafetyFamily = Literal[
    "direct_injection", "indirect_injection", "tool_output_injection",
    "authority_spoofing", "goal_hijacking", "privilege_escalation",
    "sensitive_resource_access", "memory_poisoning", "retrieval_poisoning"
]


@dataclass
class SystemManifest:
    system_name: str
    provider: str = "unknown"
    base_model: str = "unknown"
    model_version: str = "unknown"
    api_version: str = "unknown"
    evaluation_claim: EvaluationClaim = "controlled_comparison"
    level: Level = "core"
    pack: str = "diagnostic"
    official: bool = False
    system_prompt_hash: str = ""
    tools: list[str] = field(default_factory=list)
    tool_versions: dict[str, str] = field(default_factory=dict)
    external_memory: bool = False
    scaffold: str = "none"
    scaffold_version: str = "unknown"
    harness_commit_sha: str = ""
    reasoning_budget: str = "standard"
    retry_policy: str = "task_defined"
    temperature: float | None = 0.0
    top_p: float | None = None
    inference_seed: int | None = None
    max_output_tokens: int | None = None
    max_total_tokens: int | None = None
    max_calls: int | None = None
    max_actions: int | None = None
    max_runtime_s: float | None = None
    max_cost_usd: float | None = None
    network_policy: str = "none"
    context_policy: str = "provider_default"
    component_label: str = "full_system"
    parent_configuration: str | None = None
    notes: str = ""

    def official_missing_fields(self) -> list[str]:
        required = {
            "system_name": self.system_name,
            "provider": self.provider,
            "base_model": self.base_model,
            "model_version": self.model_version,
            "system_prompt_hash": self.system_prompt_hash,
            "scaffold": self.scaffold,
            "scaffold_version": self.scaffold_version,
            "reasoning_budget": self.reasoning_budget,
            "retry_policy": self.retry_policy,
            "network_policy": self.network_policy,
            "context_policy": self.context_policy,
        }
        missing = [
            key for key, value in required.items()
            if value is None or str(value).strip() in {"", "unknown", "unnamed-system"}
        ]
        if self.temperature is None:
            missing.append("temperature")
        if not any(v is not None for v in (
            self.max_runtime_s, self.max_actions, self.max_total_tokens, self.max_cost_usd
        )):
            missing.append("at_least_one_budget")
        return missing


@dataclass
class HumanBaseline:
    source: BaselineSource = "none"
    n: int = 0
    median_seconds: float | None = None
    p80_seconds: float | None = None
    population: str = "unspecified"
    methodology: str = ""

    @property
    def horizon_eligible(self) -> bool:
        return self.source == "measured" and self.n > 0 and self.median_seconds is not None


@dataclass
class FaultSpec:
    enabled: bool = False
    kind: str | None = None
    trigger_step: int | None = None
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetySpec:
    enabled: bool = False
    family: SafetyFamily | None = None
    protected_resources: list[str] = field(default_factory=list)
    legitimate_goal_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GraderSpec:
    spec: dict[str, Any]
    name: str = "primary"
    weight: float = 1.0
    required: bool = True


@dataclass
class Task:
    task_id: str
    version: str
    level: Level
    primary_domain: str
    secondary_domains: list[str]
    prompt: str
    grader: dict[str, Any] | None = None
    difficulty_tier: int = 1
    human_baseline: HumanBaseline = field(default_factory=HumanBaseline)
    affordances: list[str] = field(default_factory=list)
    max_attempts: int = 1
    recovery_feedback: str | None = None
    boundary_sensitive: bool = False
    calibration_required: bool = False
    verification_required: bool = False
    fault: FaultSpec = field(default_factory=FaultSpec)
    safety: SafetySpec = field(default_factory=SafetySpec)
    budget_runtime_s: float | None = None
    budget_actions: int | None = None
    budget_tokens: int | None = None
    budget_cost_usd: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    # Appended at the end to preserve the legacy positional Task constructor used by
    # public packs while enabling first-class named/weighted multi-grader tasks.
    graders: list[GraderSpec] = field(default_factory=list)

    def grader_specs(self) -> list[GraderSpec]:
        if self.graders:
            return self.graders
        if self.grader is not None:
            return [GraderSpec(spec=self.grader)]
        return []


@dataclass
class Attempt:
    attempt: int
    output: str
    latency_s: float
    passed: bool
    partial_credit: float
    gradeable: bool
    violation: bool
    verified: bool
    confidence: float | None
    failure_code: str | None
    grader_detail: str
    action_count: int = 0
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None
    grader_results: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class TaskResult:
    task_id: str
    primary_domain: str
    level: Level
    difficulty_tier: int
    human_seconds: float | None
    human_baseline_source: BaselineSource
    passed_first: bool
    passed_eventually: bool
    recovered: bool
    adapted: bool
    violation: bool
    verified: bool
    gradeable_first: bool
    attempts: list[Attempt]
    safety_sensitive: bool = False
    safety_family: SafetyFamily | None = None
    safe_success: bool | None = None
    trajectory: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


@dataclass
class TrialResult:
    """One independent rollout. Retries inside a rollout remain Attempt records."""
    task_id: str
    trial_index: int
    seed: int
    result: TaskResult

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "trial_index": self.trial_index,
            "seed": self.seed,
            "result": self.result.to_dict(),
        }


@dataclass
class ContributionResult:
    component: str
    baseline_system: str
    comparison_system: str
    baseline_score: float
    comparison_score: float
    absolute_delta: float
    relative_delta: float | None
    metric: str = "frontier_score"
