# External Benchmark Integration

AFB is intended to normalize real frontier evaluation environments rather than duplicate them.

## SWE-bench-style pack

Map repository tasks into AFB:
- level = agent
- domain = A5
- grader = unit/integration test terminal state
- actions = shell/editor/tool calls
- human baseline = professional developer time
- recovery = patch/test/repatch loop

## OSWorld-style pack

Map computer workflows:
- level = agent/autonomous
- domains = A8/A9/A7
- grader = application state / filesystem / UI outcome
- record action count and verification
- use reproducible initial state snapshots

## Terminal-Bench-style pack

Map terminal tasks:
- level = agent
- outcome-based grader
- containerized environment
- explicit tool/runtime budget
- anti-shortcut validation

## BrowseComp-style pack

Map research tasks:
- domain = A6
- browser/search affordances
- grade answer correctness + citation fidelity + source support
- track search/tool call efficiency

## Frontier math/science pack

Use expert-authored post-cutoff tasks:
- A2/A3
- sealed answers
- deterministic or formally checkable graders where possible
- human expert time measurements

## Robotics / embodied systems

For robotics and other embodied AI systems:
- level = autonomous
- environment = simulator or hardware-in-loop
- terminal state = world-state achievement
- fault injection = sensor/tool/actor/environment changes
- control score = authority/safety constraints
- state-tracking accuracy = correctness of maintained environment state across time
