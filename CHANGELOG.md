# Changelog

## 1.3.2 — Pre-v2 closure release

### Added

- Deterministic SHA-256 fingerprints over canonical AFB run payloads.
- `afb verify-result --input <run.json>` for local integrity verification of saved run logs.
- Capability Card display of the result fingerprint.
- Explicit `frontier_score_missing_evidence` reasons when the aggregate is unavailable.
- Regression tests proving result fingerprints validate unchanged payloads and fail after mutation.

### Clarified

- Result fingerprints provide tamper-evidence for the serialized AFB payload; they are not third-party execution attestation or certification.
- Signed attestations, sealed/live packs, verified leaderboards, and independent certification remain optional ecosystem layers that can be added without changing the open AFB experiment/result format.
- At the end of v1.3.x, remaining roadmap work is intentionally external/empirical rather than a missing core framework requirement: organizations may supply their own real-model studies, human baselines, private/sealed tasks, domain environments, model-judge protocols, adjudication processes, and verified-result infrastructure.

## 1.3.1 — Final v1.3 closure release

### Added

- Multiple deterministic graders per task with named, weighted, required/optional grader specifications.
- Weighted multi-grader aggregation while preserving each underlying grader result for auditability.
- `citation_fidelity` grading for research-style outputs that need both claim coverage and citation presence checks.
- Trajectory-level diagnostic signals derived from recorded agent action/state sequences. These are labeled inferred diagnostics rather than authoritative root causes.
- Conservative F15 detection for explicit grader/test probing visible in action trajectories.

### Changed

- Task schema now supports both legacy `grader` and first-class `graders` lists so existing packs remain compatible.
- Main runner uses multi-grader aggregation for text tasks.
- Frontier payload version advanced to 1.3.1.
- README and `VNEXT_PLAN.md` now make the open-source extension model explicit: organizations may supply their own private tasks, environments, human studies, custom graders, and sealed/live packs without AFB centrally owning those assets.
- G3 validated model judging and G4 human adjudication are explicitly phased as future/extension protocols rather than implied current functionality.

### Remaining by design

AFB does not centrally ship every external benchmark environment. SWE-bench-style repositories, OSWorld-style computer use, deeper containerized terminal execution, frontier math/science, robotics, sealed/live task sets, model-judge validation, formal human adjudication, and verified leaderboard infrastructure remain extension/future surfaces that may be implemented by AFB maintainers or downstream labs.

## 1.3.0 — Professional experiment release

### Added

- `afb run --trials N` with independent rollouts separated from within-rollout retries.
- Trial-level result records, trial consistency, mixed-outcome rate, and rollout counts.
- Official-manifest validation with refusal of incomplete publication-grade runs.
- Public `frontier` pack with harder procedural tasks and real interactive execution for A8/A9/A10/A12.
- Main-run integration of `VirtualOpsEnvironment` and the sidecar-injection environment.
- Mid-task inventory drift for adaptation testing and trajectory logging.
- Measured human-baseline loader (`--human-baselines`) so H50/H80 only activates from real timing data.
- Human timing collection commands: `afb baseline-record` and `afb baseline-compile`; these record supplied observed timings and never synthesize measurements.
- Terminal-result interoperability adapter (`afb import-terminal`) for terminal/Harbor-style JSON or JSONL exports.
- Agent-loop aggregation of token, action, cost, and latency telemetry across multi-step episodes.
- Manifest fields for pack, official status, retry policy, and publication-grade completeness checks.

### Changed

- A8 Tool Use, A9 Planning/Execution, and A10 Recovery/Adaptation in Smoke/Diagnostic profiles now use real interactive environment loops rather than text proxies.
- Frontier Score is suppressed unless independent-trial consistency **and actual observed recovery evidence** are available.
- A perfect run with no recovery opportunity reports Recovery as `N/A`; it is not silently assigned 100% recovery.
- Capability Cards explicitly show pass@1, eventual success, recovery, trial consistency, adaptation, and score availability.
- OpenAI-compatible sampling settings are wired from the CLI into the actual request rather than only described in metadata.
- Public frontier tasks use programmatic terminal-state success for interactive domains instead of text-only proxy tasks.
- Benchmark payload version advanced to 1.3.0.

### Validation status

- CI covers Python 3.10–3.12, unit tests, oracle Smoke-48, weak negative control, multi-trial logic, interactive environment positive controls, timing collection/compilation, baseline loading, and terminal-result normalization.
- No fabricated real-model traces or human measurements are included. Multi-class external model validation and an actual timed-human study remain required before publication-grade claims.

## 1.2.0 — Evaluation-model expansion

### Added

- First-class **Safety** evaluation architecture.
- Isolated adversarial **sidecar-injection sandbox** for safeguard testing.
- Safety metrics: safe rate, safe successful completion, injection resistance, violation rate, and Safety Index.
- Expanded headline dimension vector: Safety, Capability, Reliability, Autonomy, Control, Efficiency, Calibration, Recovery / Adaptation.
- **Strategic Breakdown** engineering profile derived from deterministic failure classes.
- **System-vs-model contribution** analysis utilities for matched ablation runs.
- Safety and contribution metadata in the core schema.
- `afb safety` CLI command for sidecar-injection evaluation.
- Full vNext architecture plan in `docs/VNEXT_PLAN.md`.
- Regression tests for safety sandbox behavior, strategic diagnostics, and attribution deltas.

### Changed

- Frontier Score now aggregates only dimensions with valid evidence; missing dimensions remain `N/A`.
- Capability Card now exposes the full vNext evaluation vector and Strategic Breakdown.
- Recovery and adaptation remain separate raw metrics and are additionally summarized as a combined index.
- Benchmark payload version advanced to 1.2.0.

## 1.1.0 — Credibility and measurement release

### Changed

- Replaced hardcoded 100% efficiency with budget-relative efficiency scoring.
- Efficiency is now `N/A` when required budget/telemetry data are unavailable.
- Added adapter telemetry fields for token usage, actions, and cost.
- Added explicit `evaluation_claim`: controlled comparison, maximum elicitation, or safeguard evaluation.
- Expanded the system manifest with provider, API, scaffold, tool-version, sampling, context, and budget metadata.
- Distinguished independent trials from within-run retries/recovery attempts in the schema.
- Added human-baseline provenance (`measured`, `estimated`, `none`).
- Official H50/H80 fitting now uses measured human baselines only.
- Reference task times are explicitly marked as author estimates and are not horizon-eligible.
- Renamed the public 300-task profile from Core-300 to Diagnostic-300 to avoid overstating frontier validity.
- Clarified that external benchmark/environment adapters are planned until concrete validated integrations are merged.
- Clarified that validated model judging and human adjudication are not currently automatic reference graders.
- Expanded regression coverage and added GitHub Actions CI.
- Added contribution, governance, and security policies.

## 1.0.0

Initial public framework and reference diagnostic implementation.
