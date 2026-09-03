# AFB Benchmark Specification v1.0

## Evaluation object

AFB evaluates a **system-under-test**:

`model + prompts + harness + tools + memory + inference budget + environment`

A result is not a "model score" unless all non-model factors are held constant.

## Evaluation levels

### Level 1 — Core
No external tools. Tests reasoning, mathematics, abstraction, structure, calibration, knowledge, and instruction following.

### Level 2 — Tool
Standardized tool affordances. Measures tool choice, tool execution, synthesis, and verification.

### Level 3 — Agent
Interactive environments. Measures planning, action, state tracking, recovery, and terminal-state success.

### Level 4 — Autonomous
Long-running dynamic environments with changing constraints, fault injection, persistent state, and authority boundaries.

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

## Required benchmark tiers

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
- measured human difficulty
- reproducible initialization

## Repetition

For low-cost tasks:
- minimum 3 independent rollouts

For high-cost tasks:
- 1 rollout may be acceptable if the benchmark reports that limitation.

AFB distinguishes:
- pass@1
- eventual success
- repeated consistency
- recovery

## Fault injection

Agent/autonomous packs should support controlled disruptions such as:

- tool failure
- stale information
- conflicting updates
- dependency outage
- changed constraint
- corrupted artifact
- delayed external event

Fault timing must be randomized or sealed for serious runs.
