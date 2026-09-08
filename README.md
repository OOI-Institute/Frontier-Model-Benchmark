# AnyModel Frontier Benchmark (AFB)

**Provider-Neutral Evaluation for AI Models and AI Systems**

AFB is a standalone evaluation framework for characterizing what an AI model or AI system can do, how reliably and safely it does it, where it fails, how it behaves under changing state and constraints, and what resources successful performance requires.

AFB evaluates the declared system that was actually run. A bare model, a tool-augmented agent, and a scaffolded autonomous system are different evaluation objects and should not be reported as if they were equivalent.

> AFB does not just rank AI systems. It characterizes their operating envelope.

## Core flow

```text
MODEL / SYSTEM CONFIGURATION
+ TASK PACK
+ RUNTIME / TOOL / BUDGET POLICY
        ↓
       AFB
        ↓
independent trials
+ deterministic / programmatic grading
+ telemetry + trajectory diagnostics
+ safety / reliability / recovery analysis
        ↓
NORMALIZED RESULT
+ MANIFEST
+ PROVENANCE FINGERPRINT
        ↓
COMPARISON / REPORTING / EXTERNAL ANALYSIS
```

## What AFB evaluates

```text
AFB
├─ capability
├─ reliability
├─ safety
├─ autonomy
├─ control / constraint adherence
├─ efficiency
├─ calibration
├─ recovery / adaptation
├─ system-vs-model attribution
├─ failure-class diagnostics
└─ trajectory diagnostics
```

## Core concepts

### System manifest

Every result is tied to a declared configuration that can include model/provider identity, prompts, tools, memory, scaffold, inference budget, retry policy, runtime limits, sampling, network/context policy, and resource budget.

### Independent trials

A **trial** is a new rollout. A **retry** is an attempt inside one rollout. AFB keeps them separate so pass@1, eventual success, recovery, and consistency are not conflated.

### Task packs

AFB ships public task packs for harness validation and reproducible diagnostics, while allowing organizations to bring private or domain-specific evaluations through the same result schema.

### Grading

AFB prefers the strongest objective grader available:

```text
G0  exact / cryptographic
G1  programmatic terminal-state verification
G2  deterministic rubric / multi-grader aggregation
G3  validated model judge                  planned opt-in
G4  human expert adjudication              external protocol
```

### Result provenance

Saved AFB results include a deterministic SHA-256 fingerprint over the canonical payload. This provides tamper evidence for the serialized result; it is not a claim of independent certification of the underlying run.

## Minimal usage

```bash
python -m afb.cli run \
  --pack frontier \
  --trials 8 \
  --adapter openai-compatible \
  --base-url http://localhost:8000/v1 \
  --model my-model \
  --system-name my-frontier-run
```

Verify a saved result:

```bash
python -m afb.cli verify-result --input runs/<run>.json
```

## Installation

```bash
python -m pip install -e .
```

Python 3.10+ is required.

## MVP scope

This repository contains the standalone AFB benchmark framework and public reference packs:

```text
afb/         benchmark runtime + schemas + graders + adapters
tests/       automated regression and validation tests
examples/    integration examples
docs/        benchmark protocol, methods, schemas, scoring, extensions
.github/     CI and repository automation
```

The public MVP provides:

- experiment-oriented `afb run`,
- independent trials,
- deterministic and programmatic graders,
- interactive execution support,
- system manifests,
- telemetry and diagnostics,
- adversarial safety testing,
- baseline collection tooling,
- external result normalization,
- tamper-evident result fingerprints,
- public reproducible packs.

AFB does not require any proprietary orchestration platform, private model provider, internal benchmark service, or company-specific runtime. Labs and product teams can embed it independently or extend it with private evaluations.

See [`docs/MVP_SCOPE.md`](docs/MVP_SCOPE.md).

## What AFB is not

AFB is not itself:

- a model provider,
- a model leaderboard service,
- an inference runtime,
- an agent framework,
- a claim of independent certification,
- a sealed benchmark authority,
- or a substitute for domain-specific expert evaluation.

Those systems can integrate with AFB through its task, adapter, grader, manifest, and result interfaces.

## Public packs

### Smoke-48

Small procedural pack for CI, adapter validation, and harness regression.

### Diagnostic-300

Repeatable development diagnostics across twelve domains. Diagnostic-300 alone is not evidence of frontier capability.

### Frontier

Open execution profile combining longer-state, multi-constraint, interactive, adaptive, and adversarial tasks. It is public and reproducible rather than sealed or contamination-resistant.

## Evaluation integrity

AFB reports observed evidence rather than manufacturing prestige metrics. Official runs require stronger manifest completeness, and AFB does not emit a Frontier Score from a one-pass run or from a run without observed recovery evidence.

Measured human baselines are treated as measured only when supported by timing evidence. Real-model validation and private professional tasks remain external inputs rather than fabricated repository fixtures.

## Extension surface

AFB is designed for additional evaluation packs such as:

- repository / patch / test-loop tasks,
- computer-use environments,
- containerized terminal tasks,
- research and citation-fidelity tasks,
- frontier math/science,
- robotics / embodied systems,
- proprietary internal evaluations,
- private red-team suites and human studies.

AFB does not need to own private or sealed assets to normalize and analyze compatible results.

## Project documentation

- [`docs/BENCHMARK_SPEC.md`](docs/BENCHMARK_SPEC.md) — benchmark protocol
- [`docs/METHODS.md`](docs/METHODS.md) — methodology
- [`docs/TASK_SCHEMA.md`](docs/TASK_SCHEMA.md) — task format
- [`docs/SCORING.md`](docs/SCORING.md) — scoring and statistics
- [`docs/AGENT_PROTOCOL.md`](docs/AGENT_PROTOCOL.md) — environment protocol
- [`docs/EXTENSIONS.md`](docs/EXTENSIONS.md) — interoperability and extensions
- [`docs/VNEXT_PLAN.md`](docs/VNEXT_PLAN.md) — current architecture and forward work

## License

Apache-2.0. See `LICENSE`.
