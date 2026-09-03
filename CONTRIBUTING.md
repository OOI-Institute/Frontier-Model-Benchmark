# Contributing to AFB

AFB welcomes contributions to the benchmark engine, adapters, graders, documentation, statistical methods, and task packs.

## Principles

Contributions should preserve:

- provider neutrality
- reproducibility
- transparent system configuration
- objective grading where possible
- honest distinction between implemented and planned capability
- separation of public diagnostics from sealed/live evaluation claims

## Code contributions

Before opening a pull request:

1. add or update tests,
2. run `pytest -q`,
3. run Smoke-48 with the oracle and weak negative-control adapters,
4. document any result-schema or scoring change,
5. avoid silently changing the meaning of an existing benchmark version.

## Task contributions

A proposed benchmark task should document:

- target construct/capability
- realistic use case
- task difficulty
- deterministic or programmatic success criteria where possible
- alternate valid solutions
- anti-shortcut considerations
- environment requirements
- human-baseline provenance
- contamination/visibility status

Public task contributions are not automatically eligible for future sealed or live sets.

## Human baselines

Do not submit invented sample sizes or present estimated completion times as measured. Measured baselines should include methodology, population, sample count, and timing procedure.

## Model judges

Model-judge grading should only be proposed where objective grading is not feasible. Any judge must be versioned, auditable, validated against human labels, and reported as part of the evaluation configuration.
