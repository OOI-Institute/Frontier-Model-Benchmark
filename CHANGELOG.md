# Changelog

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
