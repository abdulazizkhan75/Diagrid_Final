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
