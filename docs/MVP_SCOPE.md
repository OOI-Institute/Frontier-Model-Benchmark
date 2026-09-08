# AFB MVP Scope

AFB is published as a standalone, provider-neutral evaluation framework for AI models and AI systems.

## Public MVP boundary

The repository includes the components required to run, grade, normalize, and analyze reproducible evaluations:

- task and pack schemas,
- model/system adapters,
- experiment execution with independent trials,
- deterministic and programmatic graders,
- interactive environment support,
- system manifests,
- telemetry and trajectory diagnostics,
- safety and recovery evaluation,
- baseline collection tooling,
- result normalization,
- result provenance fingerprints,
- public reference packs,
- automated tests and public documentation.

## External by design

The following are integration inputs or optional extensions rather than required parts of the MVP:

- proprietary models,
- private system prompts,
- private tools or memory systems,
- proprietary agent runtimes,
- sealed or post-cutoff task sets,
- private professional evaluations,
- measured human studies,
- third-party attestations,
- external leaderboards,
- independent certification infrastructure.

AFB can describe and evaluate systems that use those components without owning or exposing them.

## Standalone contract

```text
Task Pack + Declared System
            ↓
           AFB
run + grade + measure + normalize
            ↓
Manifest + Result + Diagnostics
```

AFB does not depend on a particular AI provider, orchestration platform, company runtime, or private infrastructure. The public package should remain independently usable by researchers, labs, product teams, and evaluation engineers.

## MVP development rule

Public additions should directly strengthen at least one of:

- task execution,
- grading quality,
- reproducibility,
- statistical reliability,
- safety/recovery measurement,
- telemetry/diagnostics,
- interoperability,
- or developer usability.

Organization-specific architecture and unrelated internal system details should remain outside this repository.
