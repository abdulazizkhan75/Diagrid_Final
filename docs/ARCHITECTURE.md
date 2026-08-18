# Architecture

```text
                     +--------------------------+
                     | Engineer / CI system     |
                     +------------+-------------+
                                  |
                                  | POST /agent/run
                                  v
+------------------------------------------------------------------+
| Diagrid Catalyst                                                 |
|                                                                  |
|  +----------------------+      +-------------------------------+  |
|  | Application identity |----->| Durable workflow execution    |  |
|  +----------------------+      | + execution history/recovery |  |
|                                +---------------+---------------+  |
|                                                |                  |
|  +----------------------+                      |                  |
|  | Conversation/OpenAI  |<---------------------+                  |
|  | Dapr component       |                                         |
|  +----------------------+                                         |
+-------------------------------+----------------------------------+
                                |
                                v
                   +--------------------------+
                   | Dapr DurableAgent        |
                   | test-triage-agent        |
                   +------------+-------------+
                                |
              +-----------------+------------------+
              |                 |                  |
              v                 v                  v
 +----------------------+ +----------------+ +----------------------+
 | Failure evidence     | | Incident KB    | | Audit write          |
 | get_failure_context  | | search_known_  | | save_triage_record   |
 |                      | | incidents      | |                      |
 +----------+-----------+ +--------+-------+ +----------+-----------+
            |                      |                    |
            v                      v                    v
   demo failures.json     known_incidents.json    .demo-output/*.json

Production replacements:
- CI provider API / webhook -> failure evidence
- log platform (Datadog/Splunk/CloudWatch) -> evidence retrieval
- incident/ticket system -> historical incident search
- Dapr state/MCP/issue tracker -> audited triage record and escalation
```

## Design decisions

1. **Dapr Agents instead of a hand-rolled LLM loop** — demonstrates the required agent framework while exposing each tool call as an observable durable execution step.
2. **Deterministic mock integrations** — the live interview is reliable and reproducible. The tool interfaces mirror production boundaries.
3. **Evidence before diagnosis** — the agent cannot classify a run until it retrieves source evidence and searches related incidents.
4. **Explicit audit write** — the final diagnosis is persisted as a separate tool call so the execution graph shows the decision and side effect.
5. **One agent, multiple tools** — intentionally avoids gratuitous multi-agent complexity. A production version could split evidence collection and remediation only if ownership or scaling justified it.
