from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent


class RunIdInput(BaseModel):
    run_id: str = Field(description="CI/test run identifier, for example run-1001")


class IncidentSearchInput(BaseModel):
    query: str = Field(description="Concise symptoms or error text to search in prior incidents")
    limit: int = Field(default=3, ge=1, le=5, description="Maximum matches to return")


class SaveTriageInput(BaseModel):
    run_id: str
    category: str
    confidence: float = Field(ge=0, le=1)
    summary: str
    recommended_action: str
    evidence: list[str]


def _load_json(name: str) -> Any:
    with (BASE_DIR / "data" / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_failure_context_impl(run_id: str) -> dict[str, Any]:
    runs = _load_json("failures.json")["runs"]
    if run_id not in runs:
        return {
            "found": False,
            "run_id": run_id,
            "message": "Run not found. Available demo runs: " + ", ".join(sorted(runs)),
        }
    return {"found": True, "run_id": run_id, **runs[run_id]}


def search_known_incidents_impl(query: str, limit: int = 3) -> list[dict[str, Any]]:
    query_tokens = {token.lower().strip(".,:;()[]") for token in query.split() if len(token) > 2}
    scored: list[tuple[int, dict[str, Any]]] = []
    for incident in _load_json("known_incidents.json"):
        haystack = " ".join(
            [incident["title"], incident["category"], incident["resolution"], *incident["symptoms"]]
        ).lower()
        score = sum(1 for token in query_tokens if token in haystack)
        if score:
            scored.append((score, incident))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [{"match_score": score, **incident} for score, incident in scored[:limit]]


def save_triage_record_impl(record: dict[str, Any]) -> dict[str, Any]:
    out_dir = BASE_DIR / ".demo-output"
    out_dir.mkdir(exist_ok=True)
    path = out_dir / f"{record['run_id']}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return {"saved": True, "path": str(path.relative_to(BASE_DIR))}
