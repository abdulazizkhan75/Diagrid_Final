# Test Failure Triage Agent

An AI agent for diagnosing failed automated tests and CI jobs using **Dapr Agents** and **Diagrid Catalyst**.

## Business problem

A red CI job creates an investigation problem, not an answer. Teams lose engineering time deciding whether a failure is caused by:

- a product defect
- test automation/flakiness
- an unhealthy environment

The agent gathers evidence, searches historical incidents, classifies the failure, recommends a next action, and saves an audit record.

## Agent scenario

The agent accepts a failed run ID such as `run-1001` and autonomously:

1. retrieves run metadata and logs
2. extracts the strongest failure signals
3. searches a known-incident knowledge base
4. classifies the likely root-cause category
5. produces a confidence score and recommended action

The demo uses deterministic local JSON fixtures so a live interview does not depend on GitHub/Jenkins/Datadog availability. Those files represent clean integration seams for production APIs or MCP tools.

## Why Catalyst

The LLM can classify a failure without Catalyst. The production problem is making the *whole process* reliable and operable.

Catalyst adds:

- durable agent/workflow execution so progress can survive process restarts
- application identity and authenticated access to Dapr APIs

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

# Instructions to follow

Step 1.  diagrid login

Step 2.  

diagrid dev run `
  -f .\dapr.yaml `
  --project test-triage-take-home `
  --approve

Step 3

$body = @{
    task = "Triage run-1003 and tell me the most likely cause and next action."
} | ConvertTo-Json

$result = Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8001/agent/run" `
    -ContentType "application/json" `
    -Body $body

$result | ConvertTo-Json -Depth 10


## Demo data

| Run | Primary signal | Expected category |
|---|---|---|
| `run-1001` | DB connection refused + unhealthy DB | `environment_failure` |
| `run-1002` | UI timeout; retry passed; cookie overlay | `test_automation_defect` |
| `run-1003` | Provider introduced new enum | `dependency_change` |
| `run-1004` | OAuth secret version drift | `configuration_failure` |

These expected categories are not hard-coded into the agent. They make the demo evaluable and give the presenter a known baseline.
## Demo runbook

See [docs/DEMO.md](docs/DEMO.md) for a complete 20–30 minute presentation flow.
