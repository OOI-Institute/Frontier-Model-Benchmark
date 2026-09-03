# AFB v1.0 — Methods

## Purpose

AnyModel Frontier Benchmark (AFB) is designed to evaluate heterogeneous AI systems under a common measurement language without erasing material differences in their execution affordances.

AFB does **not** assume that:
- a bare language model,
- a reasoning model,
- a tool-augmented model,
- an agent scaffold,
- and an autonomous cognitive runtime

are equivalent systems.

The benchmark therefore separates **system configuration** from **task outcome**.

---

## Evaluation populations

AFB defines four system classes.

### L1 — Core Model
Text-in / text-out evaluation with no external execution tools.

### L2 — Tool Model
The system may invoke a fixed, declared tool set.

### L3 — Agent
The system acts iteratively inside an environment and receives observations after actions.

### L4 — Autonomous System
The system maintains state over long-horizon tasks in dynamic environments with interruptions, changed constraints, failures, or other actors.

Scores from different levels must not be presented as direct model-only comparisons.

---

## Reference profiles

### AFB Smoke-48
4 procedural instances × 12 domains.

Purpose:
- adapter validation
- CI/regression checks
- fast comparisons
- benchmark development

### AFB Core-300
25 procedural instances × 12 domains.

Purpose:
- baseline model characterization
- development leaderboard
- repeatable model comparisons

Core-300 remains a public structural benchmark. It should not be used alone for claims about frontier generality.

### AFB Frontier
A publication-grade deployment should combine:
- Core-300
- expert-authored sealed tasks
- post-cutoff/live tasks
- at least one real execution environment for agentic systems
- multiple independent rollouts
- human baseline data

---

## Task generation

Reference tasks are generated from:
- benchmark version
- seed
- task-family generator

The seed determines task parameters but not benchmark semantics.

For serious evaluation:
1. freeze the system configuration,
2. choose at least three previously unused seeds,
3. run all seeds,
4. publish all resulting runs.

This reduces literal-answer memorization but does not make a public task family contamination-proof.

---

## Capability domains

### A1 Abstract Reasoning
Inference of latent relational or transformation rules.

### A2 Quantitative & Mathematical Reasoning
Exact arithmetic, multi-stage quantitative reasoning, and extension packs for expert mathematics.

### A3 Scientific Reasoning
Hypothesis inference, latent-law discovery, model comparison, experimental reasoning.

### A4 Knowledge & Calibration
Factual judgment, answerability, abstention, and confidence calibration.

### A5 Software / Structured Transformation
Machine-verifiable transformation and, in external packs, repository-level software engineering.

### A6 Research / Evidence Selection
Evidence retrieval, source weighting, contradiction resolution, and synthesis.

### A7 Long Context / State Tracking
Temporal updates, superseding information, entity state, and longitudinal world-state consistency.

### A8 Tool Use & Computer Operation
Tool choice and execution; external packs should test real tools/application state.

### A9 Planning & Agentic Execution
Goal decomposition, action sequencing, execution, and outcome verification.

### A10 Recovery & Adaptation
Correction after failure plus re-planning after changed state or injected faults.

### A11 Professional Work
Expert-rubric tasks representing realistic professional judgment.

### A12 Judgment / Authority / Safety
Scope, authorization, constraint preservation, abstention, and refusal under objective conflict.

---

## Grading policy

AFB uses the strongest available objective grader.

Priority:

G0 Exact / cryptographic  
G1 Programmatic terminal-state verification  
G2 Deterministic rubric  
G3 Validated model grader  
G4 Human expert adjudication  

A lower-priority grader is used only when a higher-priority grader cannot represent task success.

---

## Failure taxonomy

Every failed attempt should be attributable, where feasible, to:

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

This makes AFB diagnostic rather than merely competitive.

---

## Reliability protocol

AFB distinguishes:

- **Pass@1:** success on the first rollout.
- **Eventual success:** success within authorized recovery attempts.
- **Recovery rate:** proportion of initial failures corrected later.
- **Consistency:** probability of repeated independent success.
- **Boundary adherence:** successful behavior without prohibited scope/authority violations.

For publication-grade comparisons, repeat tasks where cost permits. Never hide retries inside headline pass@1.

---

## Human task horizons

Tasks may carry measured human median completion time.

AFB estimates:
- **H50:** human task duration where modeled system success falls to 50%.
- **H80:** human task duration where modeled system success is 80%.

These are capability-horizon estimates, not claims that model cognition is human-equivalent.

A reliable horizon requires broad time coverage and enough tasks. AFB reports `N/A` when the data do not support a fit.

---

## Statistical reporting

Every binary rate should expose:
- point estimate
- sample size
- 95% confidence interval

Reference code uses Wilson intervals.

Production evaluations should use stratified clustered bootstrap across:
- domain
- task family
- source
- difficulty band
- rollout

when enough data are available.

---

## Frontier Score

The market-facing Frontier Score is a geometric aggregation of five indexes:

- Capability
- Reliability
- Autonomy
- Control
- Efficiency

The underlying indexes remain authoritative.

The geometric mean is deliberate: catastrophic weakness in one critical dimension should not disappear inside high scores elsewhere.

---

## Efficiency

Efficiency is not equivalent to low latency.

External packs should track:
- wall time
- model tokens
- tool calls
- environment actions
- monetary cost
- human-equivalent task time

Models should preferably be compared on a **Pareto frontier** of capability vs. cost/latency rather than by applying arbitrary monetary penalties.

---

## Benchmark validity

AFB does not claim that any static public suite measures "general intelligence."

Validity degrades as:
- tasks enter training corpora,
- developers tune directly against the suite,
- benchmark-specific scaffolds emerge,
- scores saturate.

Publication-grade AFB therefore requires rotating sealed/live tasks and versioned releases.
