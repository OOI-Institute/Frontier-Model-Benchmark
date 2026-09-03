# AFB v1.1 — Methods

## Purpose

AnyModel Frontier Benchmark (AFB) evaluates heterogeneous AI models and AI systems under a common measurement language without erasing material differences in execution affordances.

The evaluated object is the declared system configuration:

`model + prompts + tools + memory + scaffold + environment + inference budget + runtime limits`

A result should not be described as a model-only comparison unless non-model factors are held constant.

## Evaluation claim types

Each run declares one of three intended claim classes:

- **controlled_comparison** — compare systems under matched conditions,
- **maximum_elicitation** — estimate strongest credible performance obtainable from a system,
- **safeguard_evaluation** — evaluate robustness of constraints, boundaries, or refusal behavior.

These claim types answer different scientific questions and should be reported separately.

## Evaluation levels

### L1 — Core Model
Text/model evaluation without external execution tools.

### L2 — Tool Model
The system may use a fixed, declared tool set.

### L3 — Agent
The system acts iteratively inside an execution environment and receives observations after actions.

### L4 — Autonomous System
Long-horizon evaluation with dynamic state, changed constraints, failures, interruptions, or other actors.

The built-in public reference pack contains precursor/diagnostic tasks across these conceptual domains. A task labeled with an agent-related domain is not evidence of full interactive agent capability unless it actually executes through an environment.

## Public diagnostic profiles

### AFB Smoke-48
4 procedural instances × 12 domains.

Purpose:
- adapter validation,
- CI/regression checks,
- benchmark development.

### AFB Diagnostic-300
25 procedural instances × 12 domains.

Purpose:
- development diagnostics,
- reproducibility testing,
- public harness comparison.

Diagnostic-300 is a public procedural diagnostic suite and should not be used alone for claims about frontier generality.

## Publication-grade AFB evaluation

A stronger deployment should combine relevant components such as:

- hard expert-authored tasks,
- sealed or post-cutoff/live tasks,
- validated external benchmark adapters,
- real execution environments for agentic claims,
- multiple independent trials,
- measured human baselines where task horizons are reported,
- complete system manifests and budget disclosures.

## Task generation and contamination

Reference tasks are generated from benchmark version, seed, and task-family generator. Procedural generation reduces literal answer memorization but does not make a public task family contamination-proof.

For comparative studies:

1. freeze the system configuration,
2. choose unused seeds,
3. run all declared seeds,
4. preserve all runs rather than reporting only favorable seeds.

## Capability domains

A1 Abstract Reasoning  
A2 Quantitative & Mathematical Reasoning  
A3 Scientific Reasoning  
A4 Knowledge & Calibration  
A5 Software / Structured Transformation  
A6 Research / Evidence Selection  
A7 Long Context / State Tracking  
A8 Tool Use  
A9 Planning / Execution  
A10 Recovery / Adaptation  
A11 Professional Work  
A12 Judgment / Authority / Safety  

## Grading policy

AFB prefers the strongest objective grader available:

- **G0** Exact / cryptographic
- **G1** Programmatic terminal-state verification
- **G2** Deterministic rubric
- **G3** Validated model judge — planned interface; not automatic in the reference implementation
- **G4** Human expert adjudication — external review process

A lower-objectivity grader should only be used when the task cannot be validly scored by a stronger objective method.

## Trials and recovery

AFB distinguishes:

- **trial** — an independent rollout from the initial task state,
- **attempt/retry** — another attempt within one rollout after failure/recovery feedback.

Metrics such as pass@1, pass@k, consistency, and variance belong to trials. Recovery rate belongs to within-rollout attempts. The two must not be conflated.

## Human task horizons

Human baselines declare provenance:

- `measured`
- `estimated`
- `none`

Official H50/H80 estimates are fit only from `measured` baselines with actual observations. Reference-suite author estimates are development metadata and are not horizon-eligible.

## Efficiency

Efficiency is computed only from observable resource usage and declared comparable budgets. Supported dimensions include runtime, environment actions, tokens, and cost.

Missing telemetry is not interpreted as perfect efficiency. If no usable budgeted dimension is available, Efficiency is reported as `N/A`.

For mature comparisons, AFB recommends reporting capability-cost and capability-latency Pareto frontiers alongside any normalized efficiency index.

## Statistical reporting

Binary rates should expose point estimate, task count, and 95% confidence interval. The reference implementation uses Wilson intervals.

Larger studies should use stratified or clustered bootstrap across task family, domain, source, difficulty, seed, and trial when sufficient data exist.

## Failure taxonomy

F01 comprehension  
F02 instruction adherence  
F03 reasoning / solution  
F04 planning  
F05 tool selection  
F06 tool execution  
F07 state tracking  
F08 memory  
F09 verification  
F10 recovery  
F11 hallucination / calibration  
F12 premature completion  
F13 constraint violation  
F14 authority violation  
F15 reward hacking / grader gaming  
F16 resource/runtime exhaustion  
F17 environment misunderstanding  
F18 output/format communication  

Directly observed terminal failure classification should be distinguished from causal root-cause attribution inferred from trajectories.

## Benchmark validity and lifecycle

AFB does not claim that a static public suite measures general intelligence. Validity can degrade through contamination, direct tuning, saturation, benchmark-specific scaffolds, ambiguous tasks, broken graders, or exploitable shortcuts.

Tasks and packs should therefore be versioned, reviewed, repaired or retired when necessary, and documented through release notes or task changelogs.
