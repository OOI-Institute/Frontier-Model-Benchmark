# AnyModel Frontier Benchmark (AFB)

AFB is an open, provider-neutral evaluation framework for **AI models and AI systems**. It characterizes what a submitted system can do, how reliably and safely it does it, where it fails, how it behaves under changing state and constraints, and what resources successful performance requires.

AFB does **not** treat a bare model and a tool-augmented agent as the same evaluation object. Every result is tied to a declared system configuration: model, prompts, tools, memory, scaffold, inference budget, retry policy, runtime limits, sampling, network policy, and evaluation claim.

## What AFB evaluates

AFB separates evaluation into three layers.

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
- **Trajectory diagnostics** — inferred causal signals from recorded agent step sequences. These are explicitly labeled as inferred diagnostics, not definitive root causes.

**AFB does not just rank AI systems. It characterizes their operating envelope.**

## `run` is an experiment

`afb run` supports **independent trials per task**. A trial is a new rollout. A retry is an attempt inside one rollout. They are never merged.

AFB reports pass@1, eventual success, recovery rate, independent-trial consistency, mixed trial outcomes, adaptation success, per-domain confidence intervals, and trajectory/action telemetry for interactive tasks.

AFB does **not** emit a Frontier Score from a one-pass run or from a run without observed recovery evidence.

```bash
python -m afb.cli run \
  --pack frontier \
  --trials 8 \
  --adapter openai-compatible \
  --base-url http://localhost:8000/v1 \
  --model my-model \
  --system-name my-frontier-run
```

Every run log includes a deterministic SHA-256 fingerprint over the complete canonical payload. Verify a saved result with:

```bash
python -m afb.cli verify-result --input runs/<run>.json
```

The fingerprint is tamper-evidence for the serialized AFB result. It is not a claim that AFB independently witnessed or certified the underlying model execution.

## Public packs

### Smoke-48
Four procedural instances across twelve domains. Intended for CI, adapter validation, and harness regression.

### Diagnostic-300
Twenty-five procedural instances across twelve domains. Intended for repeatable development diagnostics. **Diagnostic-300 is not by itself evidence of frontier capability.**

### Frontier — open execution profile

The public `frontier` pack combines longer-state/multi-constraint tasks with interactive execution. A8/A9/A10 act through the environment loop, A10 receives a mid-task world-state change, and A12 runs adversarial sidecar testing. Interactive tasks are graded from terminal state rather than claims in prose.

The Frontier pack is **public and reproducible**, not sealed or contamination-resistant.

## Grading

AFB prefers the strongest objective grader available:

1. **G0 — Exact / cryptographic** — implemented
2. **G1 — Programmatic terminal-state verification** — implemented
3. **G2 — Deterministic rubric / multi-grader aggregation** — implemented
4. **G3 — Validated model judge** — planned opt-in extension
5. **G4 — Human expert adjudication** — planned external review protocol

Tasks may declare multiple named graders with weights and required/optional status. The reference grader set includes exact, numeric, JSON, rubric, calibration, and citation-fidelity scoring. Never use a model judge when deterministic/programmatic grading can decide the outcome.

## Safety and reward-hacking signals

AFB includes an isolated sidecar-injection environment. Safe success requires legitimate task completion and no prohibited-resource access.

v1.3.x also includes a conservative F15 detector for **explicit** grader/test probing visible in action trajectories. It catches obvious attempts to access or manipulate grading assets; it is not presented as complete reward-hacking detection.

## Official manifest gate

A normal development run may leave optional metadata unspecified. An `--official` run may not. Publication-critical fields include model/provider identity, model version, system prompt hash, scaffold/version, reasoning budget, retry policy, network/context policy, sampling, declared resource budget, and independent trials. Frontier official runs must also declare tools.

An official manifest plus a valid result fingerprint means the run is reproducibly described and the saved payload has not changed since generation. It does **not** by itself create third-party certification; organizations may layer signatures, attestations, sealed packs, or verified leaderboards on top of the open format.

## Measured human baselines

AFB never treats author-estimated times as measured human data. H50/H80 remains unavailable unless a task has `source=measured` timing evidence.

The public tooling supports collecting and compiling measured baselines:

```bash
python -m afb.cli baseline-record ...
python -m afb.cli baseline-compile ...
```

Organizations may run their own timing studies and pass the resulting baseline file to `afb run`.

## External interoperability and extension ecosystem

AFB is open source so organizations can bring their own evaluations instead of waiting for AFB to centrally own every benchmark environment.

Implemented today:
- terminal/Harbor-style **result normalization** via `afb import-terminal`
- common system manifest, telemetry, statistics, diagnostics, reporting, and result-provenance schema

The framework is intentionally designed for labs and contributors to add:
- SWE-bench-style repository/patch/test-loop packs
- OSWorld-style computer-use environments
- deeper containerized terminal execution packs
- BrowseComp/research packs using correctness + citation-fidelity grading
- frontier math/science packs
- robotics/embodied packs
- proprietary internal evaluations, private tools, red-team suites, and human studies

AFB does **not** need to own the private or sealed assets. A lab can keep those entirely internal while producing AFB-compatible results.

## Current maturity

```text
AFB CORE — PROVIDED PUBLICLY
────────────────────────────
Framework                    DONE
Diagnostic benchmark          DONE
Agent execution               DONE
Independent trials            DONE
Telemetry/reporting           DONE
Manifest discipline           DONE
Adversarial safety            DONE
External result adapter       DONE
Public Frontier pack          DONE
Multiple deterministic graders DONE
Trajectory diagnostic signals DONE
Baseline collection tooling   DONE
Tamper-evident result fingerprints DONE

AFB EXTENSION LAYER — USER/LAB PROVIDED
───────────────────────────────────────
Real-model validation
Measured human baselines
Private professional tasks
Broader frontier task depth
Domain-specific environments
Internal safety evaluations
Proprietary tool ecosystems
Custom graders

OPTIONAL ADVANCED INFRASTRUCTURE
───────────────────────────────
Sealed/live/post-cutoff task sets
Validated model-judge protocol
Formal human adjudication
Signed third-party attestations
Verified leaderboards
Independent certification
Institution-scale governance
```

## Validation status

AFB has automated validation across Python 3.10–3.12 covering oracle/negative controls, independent trials, interactive execution, adaptation, sidecar safety, efficiency, manifest checks, baseline loading, terminal-result normalization, multi-grader behavior, trajectory diagnostics, and result-fingerprint integrity.

AFB does **not** include fabricated real-model traces or fabricated human measurements. Organizations can and should validate the framework against their own weak/mid/frontier model classes and measured baselines. If a pack does not discriminate their systems cleanly, the pack should be improved rather than the score reinterpreted.

## Project files

- `docs/VNEXT_PLAN.md` — architecture, implemented baseline, and extension ecosystem
- `docs/BENCHMARK_SPEC.md` — benchmark protocol
- `docs/METHODS.md` — methodology
- `docs/TASK_SCHEMA.md` — task format
- `docs/SCORING.md` — scoring and statistics
- `docs/AGENT_PROTOCOL.md` — environment protocol
- `docs/EXTENSIONS.md` — interoperability and extension design
- `CONTRIBUTING.md` — contribution process
- `GOVERNANCE.md` — benchmark governance
- `SECURITY.md` — vulnerability reporting

**AFB characterizes what a system can do, how dependable and safe it is, where it breaks, how it behaves when things go wrong, and what actually produced an improvement.**
