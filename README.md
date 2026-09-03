# AnyModel Frontier Benchmark (AFB) v1.1

AFB is an open, provider-neutral evaluation framework for **AI models and AI systems**. It is designed to characterize what a submitted system can do, how reliably it does it, where it fails, how it behaves under constraints, and what resources successful performance requires.

AFB does **not** treat a bare model and a tool-augmented agent as the same evaluation object. Every result is tied to a declared system configuration: model, prompts, tools, memory, scaffold, inference budget, runtime limits, and evaluation claim.

## What AFB tells model teams

AFB is intended to tell testers, model organizations, and independent developers more than whether a model is simply "smart." It characterizes the system's **operating envelope**.

- **Capability** — which classes of tasks the system can complete.
- **Reliability** — whether it succeeds consistently on first attempt or depends on recovery.
- **Autonomy** — how much task complexity and duration it can sustain.
- **Control** — whether it respects scope, authority, uncertainty, and operational constraints.
- **Efficiency** — resource use relative to declared runtime/action/token/cost budgets when those data are available.
- **Failure diagnosis** — which failure classes dominate: reasoning, planning, tool use, state tracking, verification, recovery, calibration, authority, format, and others.
- **Calibration** — whether confidence tracks correctness and whether the system recognizes insufficient information.
- **Recovery/adaptation** — whether it can correct failure or re-plan after state changes.
- **System-vs-model contribution** — whether gains arise from the base model or from tools, memory, scaffolding, retries, or additional inference budget.

AFB is designed to help answer questions such as:

> **Our new model is better overall—but where did that improvement come from?**

> **The model reasons well, but why is it unreliable in agentic workloads?**

> **Does a new memory, planning, or tool-use layer materially improve the same base model?**

> **At what task duration does performance begin to deteriorate?**

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

The built-in public reference suite contains **precursor/diagnostic tasks across all twelve domains**. It is not presented as a substitute for real browser, terminal, repository, computer-use, or embodied execution benchmarks.

## Public diagnostic profiles

### AFB Smoke-48

Four procedural instances across twelve domains. Intended for:

- harness validation
- CI
- adapter development
- regression testing

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

AFB v1.1 no longer assigns every model a default 100% efficiency score.

Efficiency is calculated only when a run has comparable declared budgets and observable telemetry for one or more of:

- wall-clock runtime
- environment/tool actions
- token usage
- monetary cost

If those data are not available, Efficiency is reported as **N/A**, and the aggregate score is calculated from the available validated dimensions rather than inventing a perfect score.

## Reliability: trials are not retries

AFB distinguishes two different concepts:

- **Retry / recovery attempt** — another attempt inside the same task execution after failure feedback.
- **Trial** — a completely independent rollout of the same task/system configuration.

Publication-grade reliability analysis should use multiple independent trials where practical. Recovery performance must not be reported as first-pass performance.

## Failure analysis as engineering telemetry

```text
Example failure profile
────────────────────────
Reasoning                 11%
Planning                  18%
Tool execution             6%
State tracking            22%
Verification              17%
Recovery                   9%
Authority violations       2%
Format                     3%
```

The current reference harness records deterministic failure categories where the grader can establish them. Rich agent environments may add trajectory-level root-cause analysis; such analysis should be labeled separately from directly observed terminal failures.

## Grading policy

AFB prefers the strongest objective grader available:

1. **G0 — Exact / cryptographic**
2. **G1 — Programmatic terminal-state verification**
3. **G2 — Deterministic rubric**
4. **G3 — Validated model judge** *(interface planned; not enabled in the current reference implementation)*
5. **G4 — Human expert adjudication** *(external review process, not an automatic grader)*

Never use a model judge when deterministic or programmatic grading can decide the outcome.

## External benchmark interoperability

AFB's environment and result schemas are intended to support adapters for established evaluation systems rather than rebuild them. Integrations for repository, terminal, browser, computer-use, and other external benchmarks are **planned extension work** and should be treated as unavailable until a concrete adapter is merged and validated.

The intended flow is:

```text
External benchmark / environment
        ↓
AFB adapter
        ↓
Normalized task + trajectory result
        ↓
AFB statistics and failure reporting
        ↓
Capability Card
```

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

AFB v1.1 is a **benchmark framework plus public diagnostic suite**. The included oracle/weak controls validate harness mechanics and basic discrimination; they are not evidence that the diagnostic suite measures frontier capability.

The next validation milestones are:

1. real-model multi-tier validation across several model classes,
2. independent-trial and seed stability studies,
3. one validated external execution-benchmark adapter,
4. measured human baselines for horizon-eligible packs,
5. sealed/live task infrastructure for stronger publication claims.

## Project files

- `docs/BENCHMARK_SPEC.md` — benchmark protocol
- `docs/METHODS.md` — methodology
- `docs/TASK_SCHEMA.md` — task format
- `docs/SCORING.md` — scoring and statistics
- `docs/AGENT_PROTOCOL.md` — environment protocol
- `docs/EXTENSIONS.md` — integration design
- `CONTRIBUTING.md` — contribution process
- `GOVERNANCE.md` — benchmark governance
- `SECURITY.md` — vulnerability reporting

**AFB does not just rank AI systems. It characterizes their operating envelope: what they can do, how dependable they are, where they break, how they behave when things go wrong, and what actually produced an improvement.**
