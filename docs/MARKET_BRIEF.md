# AnyModel Frontier Benchmark — Market Brief

## What AFB answers

Most AI benchmarks answer a narrow question:

**"How many test questions did the model get right?"**

AFB answers five business-relevant questions:

1. **Capability — What can it actually do?**
2. **Reliability — Will it do it consistently?**
3. **Autonomy — How much work can it complete before a human needs to intervene?**
4. **Control — Does it stay inside scope and know when not to act?**
5. **Efficiency — What does successful work cost in time, actions, and compute?**

## The output

Every evaluated system receives an **AI Capability Card**.

Example:

| Measure | Result |
|---|---:|
| Frontier Score | 82.4 / 100 |
| Capability | 88 |
| Reliability | 76 |
| Autonomy | 81 |
| Control | 94 |
| Efficiency | 73 |
| First-attempt success | 79% |
| Eventual success | 91% |
| H50 task horizon | 4.2 human-hours |
| Median successful-task cost | $1.42 |

The scorecard is market-readable.

Every number remains backed by:
- task-level raw outputs,
- system configuration,
- grader results,
- confidence intervals,
- failure classifications,
- runtime metadata.

## Why system configuration matters

AFB labels the thing actually tested.

A bare model and the same model inside a sophisticated agent are different systems.

This prevents misleading claims such as attributing gains from:
- browsing,
- external memory,
- retries,
- subagents,
- large compute budgets

solely to the base model.

## Where AFB fits

AFB is not intended to replace specialized benchmarks.

It provides a common evaluation and reporting layer capable of incorporating:
- software engineering benchmarks,
- computer-use environments,
- terminal tasks,
- research tasks,
- expert mathematics/science,
- professional domain tasks,
- embodied/robotic environments.

That makes it useful for:
- model developers,
- agent companies,
- enterprise procurement,
- investors,
- researchers,
- autonomy platforms,
- robotics and embodied AI teams.
