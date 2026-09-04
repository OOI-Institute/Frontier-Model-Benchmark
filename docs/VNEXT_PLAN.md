# AFB vNext Upgrade Plan

AFB vNext expands the benchmark from five headline dimensions into a three-layer characterization system.

## 1. Performance layer

AFB evaluates eight primary dimensions:

1. **Safety** — adversarial sidecar-injection resistance in isolated sandbox environments.
2. **Capability** — task classes successfully completed.
3. **Reliability** — first-pass success, repeatability, and recovery dependence.
4. **Autonomy** — sustained success over complex or long-horizon tasks.
5. **Control** — scope, authority, uncertainty, and operational-constraint adherence.
6. **Efficiency** — runtime/action/token/cost use relative to declared budgets.
7. **Calibration** — confidence-quality and recognition of insufficient information.
8. **Recovery / Adaptation** — correction after failure and re-planning after changed state.

Headline results should preserve this vector rather than hide major weaknesses inside a single score.

## 2. Attribution layer

**System-vs-model contribution** is not inferred from one run. It requires matched ablations of the same base model and task set.

Supported comparison pattern:

- base model
- + tools
- + memory
- + scaffold/planning
- + recovery
- + additional inference budget

AFB computes absolute and relative deltas between declared configurations. Attribution claims must identify the changed component and preserve all other material settings.

## 3. Diagnostic layer

**Strategic Breakdown** maps failures into actionable engineering classes:

- reasoning
- planning
- tool selection
- tool execution
- state tracking
- memory
- verification
- recovery
- calibration
- authority/control
- environment
- format/communication
- reward hacking / grader gaming
- resource/runtime

The reference harness reports observed deterministic failure classes. Rich agent packs may add trajectory-level causal analysis, but inferred root causes must be labeled separately from observed terminal failures.

## 4. Safety architecture

AFB adds an isolated sidecar-injection sandbox that can test:

- direct prompt injection
- indirect/document injection
- tool-output injection
- authority spoofing
- goal hijacking
- privilege-escalation attempts
- sensitive-resource access attempts
- memory/retrieval poisoning hooks in future packs

Safety scoring separates:

- task success
- safe task success
- injection resistance
- prohibited-resource access
- violation rate

A system does not receive safe-success credit merely for refusing everything; it must continue the legitimate task where possible.

## 5. Reliability architecture

AFB preserves the distinction:

- **retry** = another attempt inside one execution after failure feedback
- **trial** = an independent rollout

vNext reporting should expose pass@1, eventual success, recovery rate, and independent-trial consistency when multiple trials exist.

## 6. Recovery vs adaptation

Internally these remain separate:

- **Recovery:** correct a failure while the world/goal is materially unchanged.
- **Adaptation:** re-plan after the world, constraints, tools, or available information change.

The public capability card may present a combined Recovery / Adaptation index while retaining both submetrics in raw results.

## 7. Calibration architecture

Calibration includes:

- confidence calibration
- answerability recognition
- abstention quality
- escalation behavior when human input or authority is required

## 8. Aggregate scoring

The AFB Frontier Score remains secondary to the dimension vector. It is computed only from dimensions with valid evidence. Missing dimensions remain N/A rather than receiving implicit perfect scores.

## 9. Implementation phases

### v1.2 — evaluation-model upgrade
- first-class Safety metadata and sandbox
- safe-success metrics
- Recovery / Adaptation index
- Strategic Breakdown output
- ablation/contribution analyzer
- capability-card expansion
- CLI safety command
- tests and documentation

### v1.3 — benchmark depth
- multiple independent trials in the main runner
- multiple graders per task
- stronger agent-environment packs
- one external benchmark adapter
- trajectory-level diagnostics

### v2.0 — publication-grade frontier evaluation
- expert-authored sealed tasks
- live/post-cutoff sets
- measured human baselines
- reward-hacking detection infrastructure
- validated external benchmark packs
- official verified result protocol / leaderboard

## 10. Validation principle

AFB must distinguish what is implemented from what is planned. Public claims should only use dimensions supported by observable telemetry, qualified tasks, and declared evaluation configuration.