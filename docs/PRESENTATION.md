# Presentation Outline (20–30 minutes)

## Slide 1 — Test Failure Triage Agent
**Message:** Turn a red CI signal into an evidence-backed next action.

- Dapr Agents + Diagrid Catalyst
- Classifies failures, finds similar incidents, recommends remediation
- Designed for durable, observable production execution

## Slide 2 — The business problem
**Message:** A failed test is an investigation queue, not automatically a software bug.

- Failures come from product, automation, environment, dependency, and configuration causes
- Manual triage consumes engineering time and slows releases
- Incorrect attribution creates noise and unnecessary handoffs

## Slide 3 — Desired outcome
**Message:** Reduce mean time to triage while keeping humans in control of consequential actions.

Input: failed run ID

Output:
- classification
- confidence
- strongest evidence
- similar historical incident
- recommended next action
- rerun decision

## Slide 4 — Architecture
Show `docs/ARCHITECTURE.md`.

Explain the separation between:
- agent reasoning
- tools/integrations
- Catalyst runtime capabilities

## Slide 5 — Why Dapr Agents
**Message:** Use an agent framework for autonomous tool selection and reasoning, not a fixed if/else classifier.

- tool calling
- model-driven reasoning
- structured tool inputs
- durable execution model

## Slide 6 — Why Catalyst
**Message:** Catalyst addresses the operational gap between an agent prototype and a production system.

Show in the console:
- app identity
- topology/components
- execution history
- individual workflow/tool steps
- persisted execution state / recovery story

## Slide 7 — Live demo: environment failure
Run `run-1001`.

Narrate:
1. evidence retrieval
2. historical-incident search
3. classification
4. audit write
5. resulting recommendation

Then inspect the execution in Catalyst.

## Slide 8 — Live demo: different root cause
Run `run-1003`.

Contrast the evidence with `run-1001`. Emphasize that the same agent adapts its reasoning and does not assume all test failures are application bugs.

## Slide 9 — Failure and recovery
Demonstrate or explain killing/restarting the local process during execution.

Also show `run-does-not-exist` to demonstrate refusal to fabricate missing evidence.

## Slide 10 — Production architecture
Replace fixtures with:
- CI event ingestion
- observability/log API
- incident/ticket knowledge source
- durable audit store
- optional MCP servers for governed tool access

Add:
- redaction
- least privilege
- idempotency
- retry/backoff
- evaluation dataset
- human approval thresholds

## Slide 11 — Trade-offs
- One agent vs multi-agent: simpler until ownership/security/scaling requires decomposition
- Deterministic fixtures vs real integrations: reliable interview demo with production-shaped interfaces
- Autonomous diagnosis vs autonomous remediation: diagnosis can be automated broadly; mutation requires higher confidence and approval

## Slide 12 — Closing
**Agent:** decides what the evidence most likely means.

**Catalyst:** makes the process durable, observable, governable, and production-operable.
