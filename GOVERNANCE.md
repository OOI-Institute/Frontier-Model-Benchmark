# AFB Governance

AFB is intended to remain provider-neutral and methodologically transparent.

## Maintainer responsibilities

Maintainers are responsible for:

- versioning benchmark behavior and task packs,
- reviewing scoring and statistical changes,
- preventing unsupported benchmark claims,
- documenting task repairs/retirements,
- separating public diagnostics from sealed/live evaluation material,
- disclosing conflicts that could materially affect evaluation design.

## Benchmark changes

Changes that alter task semantics, grader behavior, scoring formulas, system manifests, or leaderboard interpretation require a version change and changelog entry.

## Task lifecycle

Tasks may be:

- development,
- public evaluation,
- semi-private,
- sealed,
- live/post-cutoff,
- retired.

A task can be retired for contamination, ambiguity, broken environment state, scoring flaws, saturation, or exploitable shortcuts.

## Official results

An official result should include the benchmark version, task-pack version, system manifest, evaluation claim type, trial count, retry policy, and sufficient raw result metadata for audit.

AFB does not endorse a model provider. Identical evaluation rules should apply to closed, open, fine-tuned, and independently developed systems within the same comparison class.
