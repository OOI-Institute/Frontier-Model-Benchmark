# External Benchmark Integration

AFB is intended to normalize real frontier evaluation environments rather than duplicate them.

## Terminal results adapter — implemented in v1.3

`afb.external.terminal` accepts terminal/Harbor-style JSON or JSONL result exports and normalizes:

- task identity
- pass/fail or reward-derived success
- duration
- agent/action count
- token telemetry
- cost telemetry
- seed
- raw source record for auditability

CLI:

```bash
python -m afb.cli import-terminal --input terminal-results.jsonl --output afb-terminal.json
```

This is an **interoperability adapter**, not a reimplementation of an external terminal benchmark runner. The external benchmark remains responsible for its own environment construction and authoritative task grading; AFB normalizes the resulting telemetry into its reporting layer.

## SWE-bench-style pack — planned

Map repository tasks into AFB:
- level = agent
- domain = A5
- grader = unit/integration test terminal state
- actions = shell/editor/tool calls
- human baseline = professional developer time
- recovery = patch/test/repatch loop

## OSWorld-style pack — planned

Map computer workflows:
- level = agent/autonomous
- domains = A8/A9/A7
- grader = application state / filesystem / UI outcome
- record action count and verification
- use reproducible initial state snapshots

## Deeper terminal execution pack — planned

Beyond result normalization, a future pack may directly orchestrate containerized terminal tasks with:
- outcome-based grading
- explicit tool/runtime budgets
- anti-shortcut validation
- reproducible container images

## BrowseComp-style pack — planned

Map research tasks:
- domain = A6
- browser/search affordances
- grade answer correctness + citation fidelity + source support
- track search/tool call efficiency

## Frontier math/science pack — planned

Use expert-authored post-cutoff tasks:
- A2/A3
- sealed answers
- deterministic or formally checkable graders where possible
- human expert time measurements

## Robotics / embodied systems — planned

For robotics and other embodied AI systems:
- level = autonomous
- environment = simulator or hardware-in-loop
- terminal state = world-state achievement
- fault injection = sensor/tool/actor/environment changes
- control score = authority/safety constraints
- state-tracking accuracy = correctness of maintained environment state across time
