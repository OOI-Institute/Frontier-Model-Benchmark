# AFB Benchmark Specification v1.1

## Evaluation object

AFB evaluates a declared **system-under-test**:

`model + prompts + harness + tools + memory + inference budget + environment`

A result is not a model-only score unless all non-model factors are held constant.

## Evaluation claim

Every run declares one of:

- `controlled_comparison`
- `maximum_elicitation`
- `safeguard_evaluation`

The claim type is part of the result manifest because different evaluation goals permit different harness and elicitation choices.

## Evaluation levels

### Level 1 — Core
No external execution tools.

### Level 2 — Tool
Declared standardized tool affordances.

### Level 3 — Agent
Interactive execution environments with observe/act loops and terminal-state grading.

### Level 4 — Autonomous
Long-running dynamic environments with changed state, faults, persistence, and constraint boundaries.

The public diagnostic suite may contain precursor tasks related to these domains; it should not be cited as evidence of full Level 3/4 execution capability without a real environment pack.

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

## Public profiles

- **Smoke-48** — CI, adapter, and harness validation.
- **Diagnostic-300** — procedural development diagnostics.

Neither public procedural profile alone is sufficient for frontier-capability claims.

## Benchmark visibility tiers

AFB-compatible packs may be:

- public-dev
- public-eval
- semi-private
- sealed
- live/post-cutoff

Strong frontier claims should include tasks that materially reduce contamination risk, such as sealed or live/post-cutoff evaluation, when feasible.

## Human-baseline provenance

Human baseline metadata must declare `measured`, `estimated`, or `none`.

Official H50/H80 horizon estimates require measured baseline data. Estimated times may be retained for development metadata but are not horizon-eligible.

## Task admission criteria

Serious benchmark tasks should satisfy:

- realism
- construct validity
- solvability by qualified humans
- objective terminal-state determination where possible
- anti-shortcut / anti-reward-hacking review
- discrimination among systems
- remaining frontier headroom
- stable/reconstructable environment
- documented human-difficulty provenance
- reproducible initialization

## Repetition and recovery

AFB distinguishes:

- **trial** — an independent rollout from initial state,
- **retry/attempt** — another attempt inside one rollout,
- **pass@1** — first-trial/first-attempt success as defined by the pack,
- **eventual success** — success within explicitly permitted recovery,
- **consistency** — repeated independent success,
- **recovery rate** — correction after an initial failure.

Do not collapse retries into first-pass success.

## Efficiency and budgets

Runs may declare runtime, action, token, call, and cost budgets. Efficiency is computed only from dimensions for which both comparable budget and observed telemetry exist. Missing data are reported as unavailable, not assumed perfect.

## Fault injection

Agent/autonomous packs may use controlled disruptions such as:

- tool failure
- stale information
- conflicting updates
- dependency outage
- changed constraint
- corrupted artifact
- delayed external event

Fault timing should be randomized, sealed, or otherwise protected from direct benchmark-specific optimization for serious studies.

## Result integrity

Official or publication-grade results should preserve:

- benchmark/task-pack version,
- complete system manifest,
- evaluation claim type,
- trial count,
- retry policy,
- raw outputs/trajectories where releasable,
- grader identity/version,
- task exclusions and reasons,
- confidence intervals,
- budget and telemetry availability.
