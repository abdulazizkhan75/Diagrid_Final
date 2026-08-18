# Test Failure Triage Agent

A durable AI agent for diagnosing failed automated tests and CI jobs using **Dapr Agents** and **Diagrid Catalyst**.

The project is designed as a Solutions Engineer take-home: the demo is intentionally small enough to understand quickly, but it exposes production concerns such as durable execution, observability, workload identity, auditability, safe failure behavior, and pluggable integrations.

## Business problem

A red CI job creates an investigation problem, not an answer. Teams lose engineering time deciding whether a failure is caused by:

- a product defect
- test automation/flakiness
- an unhealthy environment
- an upstream dependency or contract change
- configuration or secret drift

This agent gathers evidence, searches historical incidents, classifies the failure, recommends a next action, and saves an audit record.

## Agent scenario

The agent accepts a failed run ID such as `run-1001` and autonomously:

1. retrieves run metadata and logs
2. extracts the strongest failure signals
3. searches a known-incident knowledge base
4. classifies the likely root-cause category
5. produces a confidence score and recommended action
6. persists the final triage decision for auditability

The demo uses deterministic local JSON fixtures so a live interview does not depend on GitHub/Jenkins/Datadog availability. Those files represent clean integration seams for production APIs or MCP tools.

## Why Catalyst

The LLM can classify a failure without Catalyst. The production problem is making the *whole process* reliable and operable.

Catalyst adds:

- durable agent/workflow execution so progress can survive process restarts
- application identity and authenticated access to Dapr APIs
- centralized topology and execution visibility
- observable tool inputs/outputs for debugging and audit
- pluggable Dapr components so providers can be changed without rewriting the agent's business logic
- a path to policy-controlled access for production tools and data

## Architecture

```text
CI / Engineer
     |
     v
POST /agent/run
     |
     v
Diagrid Catalyst ---- durable execution / identity / observability
     |
     v
Dapr DurableAgent
  |       |        |
  v       v        v
Evidence  Incident  Audit
Tool      Search    Write
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the detailed diagram and design trade-offs.

## Tech stack

- Python 3.11–3.13
- Dapr Agents 1.0.0
- Dapr Conversation API via `DaprChatClient`
- Diagrid Catalyst
- OpenAI conversation component
- Pytest for deterministic tool tests

## Repository structure

```text
.
├── main.py                         # Durable agent and Dapr Agent tools
├── triage_tools.py                 # Deterministic integration/business helpers
├── dapr.yaml                       # Catalyst/local application definition
├── resources/
│   └── agent-llm-provider.yaml     # Dapr Conversation component
├── data/
│   ├── failures.json               # Demo CI failures
│   └── known_incidents.json        # Demo historical incidents
├── tests/
│   └── test_triage_tools.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── DEMO.md
├── scripts/demo.sh
└── test.http
```

## Prerequisites

- Diagrid Catalyst account
- Diagrid CLI
- Python 3.11, 3.12, or 3.13
- `uv`
- OpenAI API key

## Run with Catalyst

### 1. Configure the model

Edit `resources/agent-llm-provider.yaml` and replace:

```yaml
value: "YOUR_OPENAI_API_KEY"
```

with a valid key. For a production implementation, do not commit a credential; inject it from a managed secret/component configuration.

### 2. Install dependencies

```bash
uv sync
```

### 3. Authenticate

```bash
diagrid login
diagrid whoami
```

### 4. Start the agent

```bash
diagrid dev run -f dapr.yaml --project test-triage-take-home --approve
```

Wait until the console prints:

```text
Test Triage Agent is running on http://localhost:8001
```

### 5. Trigger a triage run

macOS/Linux:

```bash
curl -i -X POST http://localhost:8001/agent/run \
  -H "Content-Type: application/json" \
  -d '{"task":"Triage run-1001 and tell me the most likely cause and next action."}'
```

Windows PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri 'http://localhost:8001/agent/run' -ContentType 'application/json' -Body '{"task":"Triage run-1001 and tell me the most likely cause and next action."}'
```

Or use `test.http` with the VS Code REST Client extension.

## Demo data

| Run | Primary signal | Expected category |
|---|---|---|
| `run-1001` | DB connection refused + unhealthy DB | `environment_failure` |
| `run-1002` | UI timeout; retry passed; cookie overlay | `test_automation_defect` |
| `run-1003` | Provider introduced new enum | `dependency_change` |
| `run-1004` | OAuth secret version drift | `configuration_failure` |

These expected categories are not hard-coded into the agent. They make the demo evaluable and give the presenter a known baseline.

## Testing

The unit tests exercise deterministic integration logic without requiring an LLM or Catalyst connection:

```bash
uv run --extra dev pytest -q
```

## What to show in Catalyst

After triggering a run, open the Catalyst console and show:

1. the `test-triage-agent` application
2. its topology and Dapr component relationship
3. the workflow/agent execution history
4. the `get_failure_context` tool step
5. the `search_known_incidents` tool step
6. the `save_triage_record` step
7. LLM inputs/outputs and execution timing

The final tool writes a local demo audit record under `.demo-output/` as an explicit side effect. In production this would be a ticket, state store, database, or event.

## Failure and recovery demo

Because the agent uses the Dapr Agents durable execution model with Catalyst, a strong demo is to start an execution, interrupt the local process, restart it, and inspect execution state/history in Catalyst. This demonstrates the production distinction between a normal LLM script and a durable agent runtime.

Also test a hallucination-safe failure:

```bash
./scripts/demo.sh run-does-not-exist
```

The agent is instructed to stop rather than fabricate evidence when a run ID does not exist.

## Production evolution

A production version would replace the fixture-backed tools with:

- GitHub Actions/Jenkins/Azure DevOps API or webhook for run metadata
- Datadog/Splunk/CloudWatch/OpenTelemetry for logs and traces
- Jira/ServiceNow/GitHub Issues for similar-incident retrieval and escalation
- Dapr state or a durable database for triage records
- MCP servers for governed access to CI, observability, or ticketing tools

Additional controls:

- redact credentials/PII before model calls
- least-privilege identity per tool/integration
- confidence threshold before any automated remediation
- human approval for release-blocking or mutating actions
- idempotency keys for issue creation and notifications
- retry/backoff, circuit breaking, and dead-letter handling
- offline evaluation dataset for classification quality and regression testing
- prompt/model versioning and audit retention

## Architectural trade-offs

**Why one agent?** The workflow is cohesive and sequential. Splitting it into multiple agents would add coordination cost without demonstrating additional business value. Multi-agent decomposition becomes justified when evidence collection, ownership routing, or remediation require independently scaled/security-isolated workers.

**Why mock integrations?** A take-home demo should be deterministic. The interfaces are intentionally written so the mocks can be replaced by real APIs without changing the agent's reasoning contract.

**Why save the diagnosis as a tool call?** It makes the mutation explicit, independently observable, and a natural point for authorization/idempotency controls.

## Demo runbook

See [docs/DEMO.md](docs/DEMO.md) for a complete 20–30 minute presentation flow.
