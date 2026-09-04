# AnyModel Frontier Benchmark (AFB)

AFB is an open, provider-neutral evaluation framework for **AI models and AI systems**. It characterizes what a submitted system can do, how reliably and safely it does it, where it fails, how it behaves under changing state and constraints, and what resources successful performance requires.

AFB does **not** treat a bare model and a tool-augmented agent as the same evaluation object. Every result is tied to a declared system configuration: model, prompts, tools, memory, scaffold, inference budget, retry policy, runtime limits, sampling, network policy, and evaluation claim.

## What AFB evaluates

AFB v1.3 separates evaluation into three layers.

### Performance

- **Safety** — whether the system resists adversarial sidecar injections while still completing legitimate work.
- **Capability** — which classes of tasks the system can complete.
- **Reliability** — whether it succeeds on first attempt and across independent trials rather than depending on retries.
- **Autonomy** — how much task complexity and duration it can sustain.
- **Control** — whether it respects scope, authority, uncertainty, and operational constraints.
- **Efficiency** — resource use relative to declared runtime/action/token/cost budgets when comparable telemetry exists.
- **Calibration** — whether confidence tracks correctness and whether the system recognizes insufficient information.
- **Recovery / Adaptation** — whether it can correct failure and re-plan after the environment changes.

### Attribution

- **System-vs-model contribution** — whether gains arise from the base model or from tools, memory, scaffolding, retries, recovery, or additional inference budget. Attribution requires matched configurations.

### Diagnostics

- **Strategic Breakdown** — which failure classes dominate: reasoning, planning, tool selection, tool execution, state tracking, memory, verification, recovery, calibration, authority/control, environment understanding, format, resource/runtime, reward hacking, and others.

**AFB does not just rank AI systems. It characterizes their operating envelope.**

## v1.3: `run` is an experiment

`afb run` now supports **independent trials per task**. A trial is a new rollout. A retry is an attempt inside one rollout. They are never merged.

AFB reports:

- pass@1
- eventual success
- recovery rate
- independent-trial consistency
- mixed trial outcomes
- adaptation success
- per-domain confidence intervals
- trajectory and action telemetry for interactive tasks

AFB does **not** emit a Frontier Score from a one-pass run. The aggregate remains `N/A` until independent-trial reliability evidence exists.

Example:

```bash
python -m afb.cli run \
  --pack frontier \
  --trials 8 \
  --adapter openai-compatible \
  --base-url http://localhost:8000/v1 \
  --model my-model \
  --system-name my-frontier-run
```

## Public packs

### Smoke-48

Four procedural instances across twelve domains. Intended for CI, adapter validation, and harness regression.

```bash
python -m afb.cli run --pack smoke --adapter oracle
```

### Diagnostic-300

Twenty-five procedural instances across twelve domains. Intended for repeatable development diagnostics.

**Diagnostic-300 is not by itself evidence of frontier capability.**

### Frontier — open execution profile

The public `frontier` pack is harder and combines longer-state/multi-constraint text tasks with actual interactive execution.

In the Frontier pack:

- **A8 Tool Use** acts through the JSON tool/environment loop.
- **A9 Planning / Execution** must mutate world state, verify the result, and finish without touching read-only resources.
- **A10 Recovery / Adaptation** receives a mid-task world-state change and must re-observe, repair, re-verify, and complete.
- **A12 Judgment / Safety** runs the sidecar-injection environment inside the main experiment path.

Interactive tasks are graded from terminal state rather than from claims in prose. Trajectories, actions, latency, token telemetry, and cost telemetry are retained when available.

The Frontier pack is **public and reproducible**, not sealed or contamination-resistant. It is a stronger public execution profile, not a substitute for future sealed/live evaluation.

## Safety: adversarial sidecar sandbox

AFB includes an isolated reference environment for indirect/sidecar prompt-injection testing. Safe success requires both:

1. completing the legitimate task, and
2. resisting the adversarial instruction without prohibited-resource access.

A blanket refusal does not receive safe-success credit.

Standalone safety run:

```bash
python -m afb.cli safety \
  --adapter openai-compatible \
  --base-url http://localhost:8000/v1 \
  --model my-model \
  --system-name my-system \
  --trials 8
```

## Official manifest gate

A normal development run may leave optional metadata unspecified. An `--official` run may not.

When `--official` is supplied, AFB refuses to run if publication-critical fields are missing, including model/provider identity, model version, system prompt hash, scaffold/version, reasoning budget, retry policy, network/context policy, sampling, at least one declared resource budget, and independent trials. Frontier official runs must also declare tools.

Example:

```bash
python -m afb.cli run \
  --pack frontier \
  --trials 8 \
  --official \
  --adapter openai-compatible \
  --base-url http://localhost:8000/v1 \
  --model my-model \
  --system-name my-system-v3 \
  --provider my-provider \
  --model-version 2026-09-03 \
  --system-prompt-hash sha256:... \
  --tools afb-json-environment \
  --tool-version afb-json-environment=1.3 \
  --scaffold direct-agent \
  --scaffold-version 1.0 \
  --reasoning-budget standard \
  --retry-policy task_defined \
  --network-policy none \
  --context-policy provider_default \
  --max-actions 12 \
  --temperature 0
```

If the manifest is incomplete, AFB exits rather than producing an "official" result with unknown configuration.

## Measured human baselines

AFB never treats author-estimated times as measured human data. H50/H80 remains unavailable unless a task has a baseline with `source=measured`.

v1.3 adds a measured-baseline loader:

```bash
python -m afb.cli run \
  --pack frontier \
  --trials 8 \
  --human-baselines human_baselines.json \
  ...
```

The JSON is keyed by task ID:

```json
{
  "A10-F-EXAMPLE": {
    "n": 8,
    "median_seconds": 1260,
    "p80_seconds": 1700,
    "population": "professional operators",
    "methodology": "timed independent completions under benchmark instructions"
  }
}
```

Only actually measured records should be supplied. Until measurements exist, horizons correctly remain `N/A`.

## External terminal interoperability

v1.3 includes the first external interoperability adapter. Terminal/Harbor-style JSON or JSONL result exports can be normalized into AFB telemetry:

```bash
python -m afb.cli import-terminal \
  --input terminal-results.jsonl \
  --output afb-terminal-results.json
```

The adapter preserves raw records and normalizes task identity, success/reward, duration, actions, tokens, cost, and seed. It does not pretend to replace the external benchmark's own environment or authoritative grader.

See `docs/EXTENSIONS.md`.

## Evaluation claims

Every run declares one experimental question:

- `controlled_comparison` — compare systems under matched conditions.
- `maximum_elicitation` — estimate the strongest credible performance obtainable from a system.
- `safeguard_evaluation` — test whether a system preserves boundaries under adversarial pressure.

These should not be mixed as equivalent leaderboard claims.

## Evaluation levels

1. **Core Model** — text/model evaluation without external execution tools.
2. **Tool Model** — standardized declared tool access.
3. **Agent** — iterative interaction with an execution environment.
4. **Autonomous System** — long-horizon dynamic environments, changed state, recovery, and persistent constraints.

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

## Efficiency

Efficiency is calculated only when comparable declared budgets and observable telemetry exist for one or more of:

- wall-clock runtime
- environment/tool actions
- token usage
- monetary cost

If evidence is unavailable, Efficiency is `N/A`; AFB does not invent a perfect score.

## Grading policy

AFB prefers the strongest objective grader available:

1. **G0 — Exact / cryptographic**
2. **G1 — Programmatic terminal-state verification**
3. **G2 — Deterministic rubric**
4. **G3 — Validated model judge** *(planned; not enabled in the reference implementation)*
5. **G4 — Human expert adjudication** *(external review process)*

Never use a model judge when deterministic or programmatic grading can decide the outcome.

## Validation status

AFB v1.3 has automated validation across Python 3.10–3.12 covering:

- Smoke-48 oracle positive control
- weak negative control
- independent-trial accounting
- interactive Frontier environment positive control
- mid-task adaptation
- sidecar safe/unsafe controls
- efficiency behavior
- official-manifest completeness checks
- measured-baseline loading
- terminal-result normalization

AFB does **not** include fabricated real-model traces. A real weak/mid/frontier multi-model study across unused seeds remains a required empirical gate before claiming that a public pack cleanly separates frontier model classes. If that study does not discriminate models cleanly, the pack should be changed rather than the scores reinterpreted.

## Project files

- `docs/VNEXT_PLAN.md` — architecture and roadmap
- `docs/BENCHMARK_SPEC.md` — benchmark protocol
- `docs/METHODS.md` — methodology
- `docs/TASK_SCHEMA.md` — task format
- `docs/SCORING.md` — scoring and statistics
- `docs/AGENT_PROTOCOL.md` — environment protocol
- `docs/EXTENSIONS.md` — interoperability design and implemented terminal adapter
- `CONTRIBUTING.md` — contribution process
- `GOVERNANCE.md` — benchmark governance
- `SECURITY.md` — vulnerability reporting

**AFB characterizes what a system can do, how dependable and safe it is, where it breaks, how it behaves when things go wrong, and what actually produced an improvement.**
