# Changelog

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

### Interpretation

The sidecar sandbox is a real isolated execution test, but it remains a compact reference safety environment rather than a publication-grade adversarial corpus. Official frontier safety claims require broader attack families, sealed/live adversarial tasks, and stronger independent validation.

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

### Interpretation

AFB v1.1 should be described as a benchmark framework plus public diagnostic suite. Frontier-capability claims require harder validated packs, real execution environments or established benchmark adapters, measured human baselines where task horizons are reported, and stronger real-model validation.

## 1.0.0

Initial public framework and reference diagnostic implementation.
