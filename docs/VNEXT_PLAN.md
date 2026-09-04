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

The reference harness reports observed failure classes and now also emits **trajectory diagnostics** from recorded agent steps. Trajectory diagnoses are explicitly labeled inferred signals rather than authoritative root causes.

## 4. Safety architecture

AFB includes an isolated sidecar-injection sandbox that can test direct/indirect injection, tool-output injection hooks, authority spoofing, goal hijacking, privilege-escalation attempts, and sensitive-resource access. Safe-success requires legitimate task completion plus constraint preservation.

## 5. Reliability architecture

AFB preserves the distinction:

- **retry** = another attempt inside one execution after failure feedback
- **trial** = an independent rollout

v1.3 exposes pass@1, eventual success, recovery rate, and independent-trial consistency.

## 6. Recovery vs adaptation

Internally these remain separate:

- **Recovery:** correct a failure while the world/goal is materially unchanged.
- **Adaptation:** re-plan after the world, constraints, tools, or available information change.

## 7. Calibration architecture

Calibration includes confidence calibration, answerability recognition, abstention quality, and escalation behavior when human input or authority is required.

## 8. Grading architecture

v1.3.1 supports **multiple deterministic graders per task** with named, weighted, required/optional grader specifications. The reference implementation includes exact/programmatic/rubric grading plus citation-fidelity scoring for research-style outputs.

- G0 Exact / cryptographic — implemented
- G1 Programmatic terminal-state verification — implemented
- G2 Deterministic rubric / multi-grader aggregation — implemented
- G3 Validated model judge — planned extension; must log judge model/version/prompt/raw judgment and remain opt-in
- G4 Human expert adjudication — planned external review protocol

AFB continues to prefer deterministic/programmatic grading whenever possible.

## 9. Reward-hacking / grader-gaming detection

v1.3.1 adds a conservative first-pass F15 detector for explicit grading-asset probing visible in action trajectories. It is intentionally narrow and must not be interpreted as full reward-hacking coverage. Stronger sandbox instrumentation and sealed anti-gaming tests remain an extension/future area.

## 10. Aggregate scoring

The AFB Frontier Score remains secondary to the dimension vector. Missing dimensions remain N/A rather than receiving implicit perfect scores. Independent-trial evidence and observed recovery evidence are required before the aggregate is emitted.

## 11. Implementation status

### v1.3.x — open framework baseline

Implemented:
- independent trials in the main runner
- official manifest gate
- interactive A8/A9/A10/A12 execution
- public Frontier pack
- measured-baseline collection/loading infrastructure
- terminal-result interoperability adapter
- multiple graders per task
- trajectory-level diagnostic signals
- conservative explicit F15 detection

### Extension ecosystem — intentionally organization/lab supplied

The open framework is designed for labs and contributors to add:
- SWE-bench-style repository packs
- OSWorld-style computer-use packs
- deeper containerized terminal packs
- BrowseComp/research packs using correctness + citation-fidelity graders
- frontier math/science packs
- robotics/embodied packs
- proprietary internal tasks, environments, tools, red-team suites, and human baseline studies

AFB does not need to centrally own these assets for them to produce AFB-compatible results.

### Future / publication-grade optional infrastructure

- expert-authored sealed/live/post-cutoff sets
- measured human baselines at scale
- broader reward-hacking detection
- validated external benchmark execution packs
- G3 validated model-judge protocol
- G4 formal human-adjudication protocol
- official verified-result / leaderboard infrastructure

These may be built by AFB maintainers or by organizations extending the open standard.

## 12. Validation principle

AFB must distinguish what is implemented from what is planned. Public claims should only use dimensions supported by observable telemetry, qualified tasks, declared evaluation configuration, and the grader/environment actually used.