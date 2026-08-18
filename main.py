import logging

from dapr_agents import DurableAgent, tool
from dapr_agents.llm import DaprChatClient
from dapr_agents.workflow.runners import AgentRunner

from triage_tools import (
    IncidentSearchInput,
    RunIdInput,
    SaveTriageInput,
    get_failure_context_impl,
    save_triage_record_impl,
    search_known_incidents_impl,
)


@tool(args_model=RunIdInput)
def get_failure_context(run_id: str):
    """Load CI metadata, assertion details, and relevant logs for a failed test run."""
    return get_failure_context_impl(run_id)


@tool(args_model=IncidentSearchInput)
def search_known_incidents(query: str, limit: int = 3):
    """Search prior incidents for failures with similar symptoms and known resolutions."""
    return search_known_incidents_impl(query, limit)


@tool(args_model=SaveTriageInput)
def save_triage_record(
    run_id: str,
    category: str,
    confidence: float,
    summary: str,
    recommended_action: str,
    evidence: list[str],
):
    """Persist the final triage result to the demo audit store."""
    return save_triage_record_impl(
        {
            "run_id": run_id,
            "category": category,
            "confidence": confidence,
            "summary": summary,
            "recommended_action": recommended_action,
            "evidence": evidence,
        }
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    agent = DurableAgent(
        name="test-triage-agent",
        role="Senior CI Failure Triage Engineer",
        goal=(
            "Diagnose failed automated tests quickly, distinguish product defects from "
            "automation/environment/dependency/configuration failures, and produce an auditable next action."
        ),
        instructions=[
            "When given a run id, always call get_failure_context before diagnosing.",
            "If the run is unknown, stop and report the available demo run ids.",
            "Use search_known_incidents with concrete symptoms from the evidence before final classification.",
            "Classify into one of: product_defect, test_automation_defect, environment_failure, dependency_change, configuration_failure, unknown.",
            "Base the conclusion on observed evidence. Do not invent log lines or incident matches.",
            "Include a confidence score from 0.0 to 1.0 and explicitly cite the strongest evidence.",
            "Recommend the smallest safe next action and whether the failed test should be rerun.",
            "Before answering, call save_triage_record exactly once with the final diagnosis for auditability.",
            "Return a concise incident-style report with: Classification, Confidence, Evidence, Similar Incident, Recommended Action, Rerun Decision.",
        ],
        tools=[get_failure_context, search_known_incidents, save_triage_record],
        llm=DaprChatClient(component_name="agent-llm-provider"),
    )

    print("Test Triage Agent is running on http://localhost:8001")
    runner = AgentRunner()
    try:
        runner.subscribe(agent)
        runner.serve(agent, port=8001)
    finally:
        runner.shutdown()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting gracefully...")
