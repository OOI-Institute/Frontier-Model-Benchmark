# AFB Task Schema

Every task is represented by the executable `Task` dataclass in `afb/schema.py`. A publication-grade task should declare enough metadata to reproduce the evaluation object, grading rule, safety boundary, budgets, and human-baseline provenance.

```yaml
task_id: AFB-A9-0001
version: "1.2"
level: agent

primary_domain: A9
secondary_domains: [A7, A10]

prompt: ...
difficulty_tier: 4

human_baseline:
  source: measured        # measured | estimated | none
  n: 7
  median_seconds: 5640
  p80_seconds: 7100
  population: professional operators
  methodology: timed independent completion

affordances:
  - terminal
  - filesystem

max_attempts: 2
recovery_feedback: null

boundary_sensitive: true
calibration_required: false
verification_required: true

fault:
  enabled: true
  kind: dependency_failure
  trigger_step: 4
  payload: {}

safety:
  enabled: true
  family: indirect_injection
  protected_resources:
    - synthetic_admin_resource
  legitimate_goal_required: true
  metadata: {}

budget_runtime_s: 1800
budget_actions: 200
budget_tokens: 120000
budget_cost_usd: 5.00

grader:
  type: programmatic_state
  ...

metadata:
  visibility: sealed
  authored_date: 2026-11-14
  task_family: repository_repair
```

## Safety fields

`SafetySpec` identifies tasks that contribute to the Safety Index. A safety-sensitive task should declare the attack family and any protected synthetic resources. Safe success requires successful legitimate-task completion without prohibited behavior.

Supported reference families include:

- `direct_injection`
- `indirect_injection`
- `tool_output_injection`
- `authority_spoofing`
- `goal_hijacking`
- `privilege_escalation`
- `sensitive_resource_access`
- `memory_poisoning`
- `retrieval_poisoning`

A task may declare a family before a corresponding public benchmark pack exists; public reports must distinguish implemented packs from planned coverage.

## Human baseline provenance

Only `source: measured` baselines are eligible for official H50/H80 horizon fitting. Estimated author times may be useful metadata but are not treated as empirical human-performance measurements.

## Retries and trials

`max_attempts` controls retries/recovery **inside one rollout**. Independent trials are represented separately and must not be conflated with recovery attempts.
