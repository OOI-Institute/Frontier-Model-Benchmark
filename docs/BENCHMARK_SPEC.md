# AFB Benchmark Specification v1.2

## Evaluation object

AFB evaluates a **system-under-test**:

`model + prompts + harness + tools + memory + inference budget + environment`

A result is not a "model score" unless all non-model factors are held constant.

## Evaluation outputs

AFB v1.2 separates three classes of output.

### Performance

- Safety
- Capability
- Reliability
- Autonomy
- Control
- Efficiency
- Calibration
- Recovery / Adaptation

### Attribution

- System-vs-model contribution through matched ablation runs

### Diagnostics

- Strategic Breakdown of observed failure classes

The primary dimension vector is more important than the aggregate Frontier Score.

## Safety

Safety measures whether the system maintains intended behavior under adversarial pressure while still completing legitimate work where possible.

The reference implementation includes an isolated indirect/sidecar-injection sandbox. Qualified safety packs may test:

- direct prompt injection
- indirect/document injection
- tool-output injection
- authority spoofing
- goal hijacking
- privilege escalation
- sensitive-resource access attempts
- memory poisoning
- retrieval poisoning

Safety results should separate raw task success, safe successful completion, injection resistance, and violations. Blanket refusal is not equivalent to safe task completion.

## Evaluation levels

### Level 1 — Core
No external tools. Tests reasoning, mathematics, abstraction, structure, calibration, knowledge, and instruction following.

### Level 2 — Tool
Standardized declared tool affordances. Measures tool choice, execution, synthesis, and verification.

### Level 3 — Agent
Interactive environments. Measures planning, action, state tracking, recovery, terminal-state success, and where applicable safeguard behavior.

### Level 4 — Autonomous
Long-running dynamic environments with changed constraints, fault injection, persistent state, authority boundaries, and adversarial context.

## Domains

A1 Abstract Reasoning  
A2 Quantitative & Mathematical Reasoning  
A3 Scientific Reasoning  
A4 Knowledge & Calibration  
A5 Software / Structured Transformation  
A6 Research & Evidence Acquisition  
A7 Long Context & State Tracking  
A8 Tool Use & Computer Operation  
A9 Planning & Agentic Execution  
A10 Recovery & Adaptation  
A11 Professional Work  
A12 Judgment / Authority / Safety  

Safety is also a cross-cutting dimension and may be measured across multiple task domains rather than only A12.

## Evaluation claims

Every run declares one primary claim type:

- `controlled_comparison`
- `maximum_elicitation`
- `safeguard_evaluation`

These are different experimental questions and should not be combined as though they were interchangeable.

## Benchmark visibility tiers

AFB-compatible task packs may be:

- public-dev
- public-eval
- semi-private
- sealed
- live/post-cutoff

Published frontier claims should include at least one sealed or live set.

## Task admission criteria

Every serious benchmark task should satisfy:

- realism
- construct validity
- solvability by qualified humans
- objective terminal-state determination where possible
- anti-cheat resistance
- discrimination among systems
- remaining frontier headroom
- stable/reconstructable environment
- measured human difficulty where horizon claims are made
- reproducible initialization
- explicit safety/authority boundaries where applicable

## Reliability and repetition

AFB distinguishes:

- first-attempt success
- eventual success after authorized recovery
- independent trials
- repeated consistency
- recovery
- adaptation

A retry inside one rollout is not an independent trial.

For low-cost tasks, multiple independent trials are recommended. For high-cost tasks, a single rollout may be acceptable only when the limitation is disclosed.

## Recovery and adaptation

- **Recovery:** correction after failure while the task/world is materially unchanged.
- **Adaptation:** re-planning after changed state, constraints, available tools, or information.

These are measured separately in raw results and may be summarized jointly on a public Capability Card.

## System-vs-model contribution

Attribution requires matched configurations. AFB must not claim that a gain came from a component unless the comparison controls other material changes.

Example sequence:

`base → +tools → +memory → +scaffold → +recovery`

AFB records absolute and relative score deltas for each declared transition.

## Strategic Breakdown

Observed failure codes are normalized into engineering-facing categories such as reasoning, planning, tool execution, state tracking, verification, recovery, calibration, authority, environment, format, and reward hacking.

Directly observed failure categories must remain distinguishable from inferred trajectory-level root causes.

## Fault injection

Agent/autonomous packs should support controlled disruptions such as:

- tool failure
- stale information
- conflicting updates
- dependency outage
- changed constraint
- corrupted artifact
- delayed external event
- adversarial sidecar/context injection

Fault/injection timing should be randomized or sealed for serious runs.

## Aggregate scoring

The Frontier Score is a geometric aggregate over only dimensions with valid evidence. Missing dimensions remain `N/A` and are not assigned perfect defaults.
