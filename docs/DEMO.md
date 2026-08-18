# 20–30 Minute Demo Runbook

## 1. Problem framing — 3 minutes

Automated test suites produce failures faster than humans can investigate them. A failed test does not necessarily mean a product defect: it may be a flaky test, environment outage, dependency contract change, or configuration error. The agent reduces time-to-triage by gathering evidence, comparing prior incidents, classifying the failure, and recommending the smallest safe next action.

## 2. Architecture — 4 minutes

Show `docs/ARCHITECTURE.md` and explain the three tool boundaries. Emphasize that Catalyst is not being used merely to host an LLM call: it supplies durable execution, identity, component abstraction, and an execution history that can be inspected operationally.

## 3. Happy-path live demo — 6 minutes

Run:

```bash
./scripts/demo.sh run-1001
```

Expected diagnosis: `environment_failure`, based on database connection refusal and unhealthy database state, with `INC-221` as a strong historical match.

Then open Catalyst and show:
- application topology
- the agent execution
- LLM and tool steps
- inputs/outputs for evidence retrieval and incident search
- the final audit write

## 4. Contrast another failure — 4 minutes

Run:

```bash
./scripts/demo.sh run-1003
```

Expected diagnosis: `dependency_change`. Explain why the agent should not automatically blame application code simply because a contract test failed.

## 5. Failure/recovery demonstration — 4 minutes

Start a run, terminate the local agent process while the durable execution is in progress, then restart with the same `diagrid dev run` command. Use Catalyst's workflow view to discuss persisted execution state and recovery. If timing makes a live crash awkward, show a previously recorded execution and explain the same mechanism.

A second safe failure scenario is an unknown run:

```bash
./scripts/demo.sh run-does-not-exist
```

The agent should refuse to invent evidence and report the available demo IDs.

## 6. Production considerations — 5 minutes

Discuss:
- event-driven ingestion from CI rather than manual REST calls
- least-privilege workload identities
- secrets held in components rather than application code
- PII/secret redaction before LLM prompts
- idempotency for issue creation or notifications
- confidence threshold for auto-action vs human review
- retry/backoff and dead-letter handling for external systems
- evaluation set measuring classification accuracy and unsafe recommendations
- cost and latency budgets
- audit retention and access controls

## Closing

The important distinction is: **the agent reasons about what to do; Catalyst makes that reasoning process durable, inspectable, governable, and operable.**
