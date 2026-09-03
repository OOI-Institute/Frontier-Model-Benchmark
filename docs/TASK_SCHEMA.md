# AFB Task Schema

Every task contains:

```yaml
task_id: AFB-A9-0001
version: "1.0"
level: agent

domain:
  primary: A9
  secondary: [A7, A10]

prompt: ...

difficulty_tier: 4

human_baseline:
  n: 7
  median_seconds: 5640
  p80_seconds: 7100
  population: professional operators

affordances:
  - terminal
  - filesystem

max_attempts: 2

boundary_sensitive: false
calibration_required: false
verification_required: true

fault:
  enabled: true
  kind: dependency_failure
  trigger_step: randomized

grader:
  type: programmatic_state
  ...

metadata:
  visibility: sealed
  authored_date: 2026-11-14
```

The Python `Task` dataclass in `afb/schema.py` is the executable reference representation.
