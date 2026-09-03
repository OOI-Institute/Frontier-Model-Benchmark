# AFB Agent Protocol

AFB Level 3 and Level 4 environments use an explicit observe–act loop.

## Canonical loop

1. `reset(seed)` establishes a reproducible initial world.
2. Environment returns an observation and machine-readable state.
3. System emits an action.
4. Environment executes the action.
5. Environment returns:
   - observation,
   - validity,
   - authority/scope violation status,
   - new state.
6. Optional fault/event injection changes the world.
7. Loop continues until:
   - terminal success,
   - terminal failure,
   - violation,
   - action/time budget exhaustion.

## Why JSON actions are included

Provider-native function calling differs across APIs.

AFB's reference loop supports JSON actions so any text model can participate. Specialized connectors may translate native tool calls into the same environment action representation.

## Production environments

The included `VirtualOpsEnvironment` is an integration test, not a frontier environment.

Serious packs should use:
- Docker containers,
- virtual machines,
- browser sandboxes,
- application snapshots,
- simulators,
- hardware-in-loop systems

with reproducible initial states and programmatic terminal-state graders.
