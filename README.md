# AnyModel Frontier Benchmark (AFB)

AFB is an open, provider-neutral evaluation framework for **AI models and AI systems**. It is designed to characterize what a submitted system can do, how reliably and safely it does it, where it fails, how it behaves under constraints, and what resources successful performance requires.

AFB does **not** treat a bare model and a tool-augmented agent as the same evaluation object. Every result is tied to a declared system configuration: model, prompts, tools, memory, scaffold, inference budget, runtime limits, and evaluation claim.

## What AFB evaluates

AFB v1.2 organizes evaluation into three layers.

### Performance layer

- **Safety** — whether the system succeeds internal sandbox testing of adversarial sidecar injections without violating protected resources or abandoning the legitimate task.
- **Capability** — which classes of tasks the system can complete.
- **Reliability** — whether it succeeds consistently on first attempt or depends on recovery.
- **Autonomy** — how much task complexity and duration it can sustain.
- **Control** — whether it respects scope, authority, uncertainty, and operational constraints.
- **Efficiency** — resource use relative to declared runtime/action/token/cost budgets when those data are available.
- **Calibration** — whether confidence tracks correctness and whether the system recognizes insufficient information.
- **Recovery / Adaptation** — whether it can correct failure or re-plan after state changes.

### Attribution layer

- **System-vs-model contribution** — whether gains arise from the base model or from tools, memory, scaffolding, recovery loops, retries, or additional inference budget. AFB only treats this as an attribution result when matched configurations are compared through an explicit ablation protocol.

### Diagnostic layer

- **Strategic Breakdown** — which failure classes dominate: reasoning, planning, tool selection, tool execution, state tracking, memory, verification, recovery, calibration, authority/control, environment understanding, format, resource/runtime, reward hacking, and others.

AFB is intended to help frontier teams answer questions such as:

> **Our new model is better overall—but where did that improvement actually come from?**

> **The model reasons well, but why is it unreliable in agentic workloads?**

> **Does a new memory, planning, or tool-use layer materially improve the same base model?**

> **At what task duration does performance begin to deteriorate?**

> **Does the system remain effective when untrusted context attempts to redirect its behavior?**

## Safety: adversarial sidecar sandbox

AFB v1.2 includes a real isolated reference environment for **indirect/sidecar prompt-injection testing**.

The sandbox gives the system a legitimate goal and simultaneously exposes an untrusted sidecar instruction that attempts to redirect it toward a protected synthetic resource. Safe success requires both:

1. completing the legitimate task, and
2. resisting the adversarial instruction without prohibited-resource access.

This prevents a trivial "refuse everything" strategy from receiving full safety credit.

Run it with:

```bash
python -m afb.cli safety \
  --adapter openai-compatible \
  --base-url http://localhost:8000/v1 \
  --model my-model \
  --system-name my-system \
  --trials 8
```

The sandbox reports:

- Safety Index
- safe rate
- safe successful completion
- injection resistance
- violation rate
- trajectories and final synthetic state

The current sidecar environment is a **reference safety sandbox**, not a publication-grade adversarial corpus. Broader attack families, sealed tasks, and live adversarial evaluation remain vNext work.

## System-vs-model contribution

AFB does not infer attribution from a single score. Contribution analysis requires matched runs in which one declared component changes while other material settings are held fixed.

Example:

```text
Base model
    ↓
+ tools
    ↓
+ memory
    ↓
+ planning scaffold
    ↓
+ recovery
```

AFB's attribution utilities compute absolute and relative deltas between these declared configurations. The result tells a team whether a measured gain came from the underlying model or from the system around it.

## Strategic Breakdown

AFB converts deterministic failure codes into an engineering-facing profile.

```text
Example Strategic Breakdown
────────────────────────────
Reasoning                 11%
Planning                  18%
Tool execution             6%
State tracking            22%
Verification              17%
Recovery                   9%
Authority / control        2%
Format                     3%
```

The reference harness reports **observed failure categories**. Future richer agent packs may add trajectory-level causal analysis, but inferred root causes must remain separate from directly observed terminal failures.

## Evaluation claims

Every AFB run declares the kind of claim it is designed to support:

- `controlled_comparison` — compare systems under matched conditions.
- `maximum_elicitation` — estimate the strongest credible performance obtainable from a system.
- `safeguard_evaluation` — test whether a system preserves constraints or boundaries under pressure.

These are different experimental questions and should not be mixed in one leaderboard claim.

## Evaluation levels

1. **Core Model** — text/model evaluation without external execution tools.
2. **Tool Model** — standardized declared tool access.
3. **Agent** — iterative interaction with an execution environment.
4. **Autonomous System** — long-horizon dynamic environments, changed state, recovery, and persistent constraints.

The built-in public reference suite contains **precursor/diagnostic tasks across twelve domains**. It is not presented as a substitute for real browser, terminal, repository, computer-use, or embodied execution benchmarks.

## Public diagnostic profiles

### AFB Smoke-48

Four procedural instances across twelve domains. Intended for harness validation, CI, adapter development, and regression testing.

### AFB Diagnostic-300

Twenty-five procedural instances across twelve domains. Intended for broader development diagnostics and reproducibility testing.

**Diagnostic-300 is not, by itself, evidence of frontier capability.** Publication-grade claims should incorporate harder expert-authored, sealed/live, and/or real execution-environment benchmark packs.

## Capability domains

| ID | Domain |
|---|---|
| A1 | Abstract Reasoning |
| A2 | Quantitative & Mathematical Reasoning |
| A3 | Scientific Reasoning |
| A4 | Knowledge & Calibration |
| A5 | Software / Structured Transformation |
| A6 | Research / Evidence Selection |
| A7 | Long Context / State Tracking |
| A8 | Tool Use |
| A9 | Planning / Execution |
| A10 | Recovery / Adaptation |
| A11 | Professional Work |
| A12 | Judgment / Authority / Safety |

## Task horizons: H50 and H80

AFB supports task-duration horizon estimation, but **official H50/H80 values are produced only from measured human baseline data**.

The reference suite contains author-estimated task times for development metadata only. Those estimates are explicitly marked `estimated` and are **not eligible** for official horizon fitting.

When adequate measured human data exist:

- **H80** estimates the measured human task duration at which modeled system success is about 80%.
- **H50** estimates the measured human task duration at which modeled system success is about 50%.

These are task-duration equivalence measurements, not claims of human-equivalent cognition.

## Efficiency

Efficiency is calculated only when a run has comparable declared budgets and observable telemetry for one or more of:

- wall-clock runtime
- environment/tool actions
- token usage
- monetary cost

If those data are unavailable, Efficiency is reported as **N/A** rather than receiving an implicit perfect score.

## Reliability: trials are not retries

AFB distinguishes:

- **Retry / recovery attempt** — another attempt inside the same task execution after failure feedback.
- **Trial** — a completely independent rollout of the same task/system configuration.

Publication-grade reliability analysis should use multiple independent trials where practical. Recovery performance must not be reported as first-pass performance.

## Recovery vs adaptation

AFB keeps these separate internally:

- **Recovery** — correct a failure while the world and goal are materially unchanged.
- **Adaptation** — re-plan after the world, constraints, tools, or available information change.

The Capability Card may present a combined Recovery / Adaptation index while raw results retain both components.

## Grading policy

AFB prefers the strongest objective grader available:

1. **G0 — Exact / cryptographic**
2. **G1 — Programmatic terminal-state verification**
3. **G2 — Deterministic rubric**
4. **G3 — Validated model judge** *(interface planned; not enabled in the current reference implementation)*
5. **G4 — Human expert adjudication** *(external review process, not an automatic grader)*

Never use a model judge when deterministic or programmatic grading can decide the outcome.

## External benchmark interoperability

AFB's environment and result schemas are intended to support adapters for established evaluation systems rather than rebuild them.

```text
External benchmark / environment
        ↓
AFB adapter
        ↓
Normalized task + trajectory result
        ↓
AFB statistics and diagnostics
        ↓
Capability Card
```

Repository, terminal, browser, computer-use, and other external adapters remain planned until concrete validated integrations are merged.

## Quick start

```bash
python -m afb.cli run --adapter oracle --seed 20260903 --per-domain 4
```

Weak negative control:

```bash
python -m afb.cli run --adapter weak --seed 20260903 --per-domain 4
```

OpenAI-compatible endpoint:

```bash
export MODEL_API_KEY=...
python -m afb.cli run \
  --adapter openai-compatible \
  --base-url http://localhost:8000/v1 \
  --model my-model \
  --system-name my-model-eval \
  --seed 20260903
```

## Fair comparison rule

A public AFB result should disclose at minimum:

- provider and base model/version
- evaluation claim type
- system/developer prompt identity or hash
- tools and tool versions
- external memory
- harness/scaffold and version
- inference/reasoning budget
- sampling configuration
- retry allowance
- context policy
- network policy
- runtime/action/token/cost limits

If these differ materially, the runs are evaluations of different systems.

## Current status

AFB v1.2 is a **benchmark framework plus public diagnostic suite and reference adversarial safety sandbox**. The included oracle/weak controls validate harness mechanics and basic discrimination; they are not evidence that the diagnostic suite measures frontier capability.

Next milestones include:

1. broader sidecar attack families and sealed adversarial tasks,
2. real-model multi-tier validation across several model classes,
3. independent-trial and seed stability studies,
4. one validated external execution-benchmark adapter,
5. measured human baselines for horizon-eligible packs,
6. multiple graders and stronger trajectory-level diagnostics.

## Project files

- `docs/VNEXT_PLAN.md` — full upgrade architecture and roadmap
- `docs/BENCHMARK_SPEC.md` — benchmark protocol
- `docs/METHODS.md` — methodology
- `docs/TASK_SCHEMA.md` — task format
- `docs/SCORING.md` — scoring and statistics
- `docs/AGENT_PROTOCOL.md` — environment protocol
- `docs/EXTENSIONS.md` — integration design
- `CONTRIBUTING.md` — contribution process
- `GOVERNANCE.md` — benchmark governance
- `SECURITY.md` — vulnerability reporting

**AFB does not just rank AI systems. It characterizes their operating envelope: what they can do, how dependable and safe they are, where they break, how they behave when things go wrong, and what actually produced an improvement.**
