# AnyModel Frontier Benchmark (AFB) v1.0

AFB is a provider-neutral evaluation framework for **language models, tool-using models, agents, and larger cognitive systems**.

Its goal is not to produce one opaque "intelligence score." AFB measures:

- **Capability** — can the system solve difficult tasks?
- **Reliability** — does it solve them consistently?
- **Autonomy** — how long and complex a task can it sustain?
- **Control** — does it respect scope, authority, uncertainty, and constraints?
- **Efficiency** — what time / action / output budget does success require?

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
