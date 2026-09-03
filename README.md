# AnyModel Frontier Benchmark (AFB) v1.0

AFB is a provider-neutral evaluation framework for **language models, tool-using models, agents, and larger cognitive systems**.

Its goal is not to produce one opaque "intelligence score." AFB measures:

- **Capability** — can the system solve difficult tasks?
- **Reliability** — does it solve them consistently?
- **Autonomy** — how long and complex a task can it sustain?
- **Control** — does it respect scope, authority, uncertainty, and constraints?
- **Efficiency** — what time / action / output budget does success require?

## What AFB tells model teams

AFB is designed to tell testers, model organizations, and independent developers **far more than whether a model is simply "smart."** It characterizes the system's operating envelope: where it performs reliably, where it becomes brittle, how it behaves when conditions change, and why failures occur.

### Valuable outputs for frontier teams

- **Capability:** which classes of tasks the system can actually complete.
- **Reliability:** whether it succeeds consistently on the first attempt or depends on retries.
- **Autonomy:** how much task complexity and duration the system can sustain before performance deteriorates or human intervention becomes necessary.
- **Control:** whether the system respects scope, authority, uncertainty, and operational constraints.
- **Efficiency:** how much time, compute, output, tool use, and ultimately cost are required for successful outcomes.
- **Failure diagnosis:** whether weaknesses originate in reasoning, planning, tool selection, tool execution, state tracking, verification, recovery, hallucination, premature completion, authority violations, or other failure classes.
- **Calibration:** whether confidence tracks correctness and whether the system recognizes when available information is insufficient.
- **Recovery and adaptation:** whether the system can correct an error, recover from failure, or re-plan after the environment changes.
- **System-vs-model contribution:** whether measured gains come from the base model itself or from tools, memory, scaffolding, retries, inference budget, or a larger runtime around it.

For a model lab, AFB is intended to answer questions such as:

> **Our new model is better overall—but where did that improvement actually come from?**

> **The model has excellent reasoning performance, but why is it still unreliable in agentic workloads?**

> **Does a new memory, planning, or tool-use system materially improve performance over the same base model?**

> **At what task duration does autonomous performance begin to deteriorate?**

### Task horizons: H80 and H50

When a benchmark pack contains adequate human completion-time data, AFB can estimate task-duration capability horizons.

For example:

- **H80 = ~45 minutes** — the system completes tasks comparable to roughly 45 minutes of measured human professional work with about 80% modeled success.
- **H50 = ~3.5 hours** — around this measured task-duration range, modeled success falls toward 50%.

These are **task-duration equivalence measures**, not claims that the model has human cognition. They are intended to make long-horizon performance easier to interpret than a single benchmark score.

### Failure analysis as engineering telemetry

AFB's failure taxonomy is designed to function like profiling instrumentation for model and agent development.

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

A team can therefore measure not only whether a new model or architecture scores higher, but **which failure modes actually improved, which remained unchanged, and whether the gain introduced new tradeoffs elsewhere.**

For example, if a planning intervention changes planning failures from 18% to 7% while state-tracking failures remain nearly unchanged, the benchmark provides evidence that the intervention improved the intended capability rather than merely shifting an aggregate score.

### Three roles for model organizations

AFB is designed to support three complementary uses:

1. **R&D diagnostics** — identify architectural weaknesses and measure whether model, training, inference, memory, tool-use, or agent changes actually fix them.
2. **Release qualification** — determine whether a new release is genuinely better than its predecessor across capability, reliability, autonomy, control, and efficiency rather than only selected headline benchmarks.
3. **Market evidence** — translate technical evaluation into interpretable claims backed by disclosed configurations, raw task outcomes, confidence intervals, and reproducible scoring.

A mature AFB result could therefore support statements such as:

> **Model X achieves 92% boundary adherence, 81% first-pass professional-task completion, and an H50 task horizon of approximately 2.8 measured human-hours under the declared evaluation configuration.**

**AFB does not just rank AI systems. It characterizes their operating envelope:** what they can do, how dependable they are, where they break, how they behave when things go wrong, and what actually produced an improvement.

AFB supports four evaluation levels:

1. **Core Model** — no tools
2. **Tool Model** — standardized tools
3. **Agent** — interactive environments and action loops
4. **Autonomous System** — long-running tasks, dynamic state, recovery, and changing constraints

## Included in v1.0

This package includes a **reference Core/Agent diagnostic suite** plus the full benchmark framework:

- formal task schemas
- run manifests
- provider-neutral adapters
- deterministic graders
- rubric graders
- recovery/adaptation scoring
- boundary/scope scoring
- fault-injection hooks
- confidence intervals
- per-domain and per-level reporting
- human-time task horizons (H50/H80)
- market-readable AI Capability Cards
- extension APIs for real repository, browser, terminal, computer-use, and robotics packs

The built-in reference suite is intentionally compact and procedural. It is suitable for:
- framework validation,
- smoke testing,
- model comparisons during development,
- adapter validation,
- regression testing.

It is **not a replacement** for large external environments such as SWE-bench, OSWorld, Terminal-Bench, BrowseComp, or expert-authored frontier math/science sets. AFB is designed to normalize those into the same reporting standard.

## Core architecture

```
TASK PACK
   ↓
TASK INSTANCE + INITIAL WORLD STATE
   ↓
SYSTEM MANIFEST
   ↓
MODEL / AGENT ADAPTER
   ↓
OBSERVE → REASON → ACT → OBSERVE ...
   ↓
TERMINAL STATE
   ↓
GRADER STACK
   ↓
FAILURE TAXONOMY
   ↓
STATISTICS
   ↓
CAPABILITY CARD
```

## Quick start

Harness validator:

```bash
python -m afb.cli run --adapter oracle --seed 20260903
```

Weak reference model:

```bash
python -m afb.cli run --adapter weak --seed 20260903
```

CLI model:

```bash
python -m afb.cli run \
  --adapter command \
  --command "python my_model.py" \
  --seed 20260903
```

OpenAI-compatible endpoint:

```bash
export MODEL_API_KEY=...
python -m afb.cli run \
  --adapter openai-compatible \
  --base-url http://localhost:8000/v1 \
  --model my-model \
  --seed 20260903
```

## Fair comparison rule

AFB compares **systems**, not just model names.

Every public result must declare:

- base model/version
- system/developer prompt
- tools
- external memory
- harness/scaffold
- inference/reasoning budget
- retry allowance
- context policy
- network policy
- runtime/action/token limits

If these differ, the runs are different systems.

## Built-in capability domains

- A1 Abstract Reasoning
- A2 Quantitative & Mathematical Reasoning
- A3 Scientific Reasoning
- A4 Knowledge / Calibration
- A5 Software / Structured Transformation
- A6 Research / Evidence Selection
- A7 Long Context / State Tracking
- A8 Tool Use
- A9 Planning / Execution
- A10 Recovery / Adaptation
- A11 Professional Work
- A12 Judgment / Authority / Safety

## Output metrics

AFB reports:

- pass@1
- eventual success
- pass^k consistency estimate
- recovery rate
- adaptation success
- boundary adherence
- calibration score
- format reliability
- verification behavior
- action efficiency
- latency
- output size
- per-domain confidence intervals
- H50 and H80 task horizons
- failure taxonomy
- Capability / Reliability / Autonomy / Control / Efficiency indexes
- AFB Frontier Score (geometric aggregate)

## Benchmark philosophy

AFB prefers, in order:

1. exact / cryptographic grading
2. programmatic state grading
3. deterministic rubric grading
4. validated model grading
5. human expert adjudication

Never use a model judge when a deterministic grader can decide the task.

See:
- `docs/BENCHMARK_SPEC.md`
- `docs/TASK_SCHEMA.md`
- `docs/SCORING.md`
- `docs/EXTENSIONS.md`
