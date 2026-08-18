from triage_tools import get_failure_context_impl, search_known_incidents_impl


def test_loads_known_failure():
    result = get_failure_context_impl("run-1001")
    assert result["found"] is True
    assert result["service"] == "checkout-api"
    assert "connection refused" in " ".join(result["logs"])


def test_unknown_run_is_safe():
    result = get_failure_context_impl("missing-run")
    assert result["found"] is False
    assert "run-1001" in result["message"]


def test_incident_search_prioritizes_database_match():
    matches = search_known_incidents_impl("connection refused orders-db unhealthy")
    assert matches
    assert matches[0]["id"] == "INC-221"
    assert matches[0]["category"] == "environment_failure"


def test_incident_search_finds_oauth_rotation():
    matches = search_known_incidents_impl("invalid_client vault secret version")
    assert matches[0]["id"] == "INC-240"
