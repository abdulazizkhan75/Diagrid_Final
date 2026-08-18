#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8001}"
RUN_ID="${1:-run-1001}"
curl -sS -X POST "$BASE_URL/agent/run" \
  -H "Content-Type: application/json" \
  -d "{\"task\":\"Triage ${RUN_ID}. Determine the category, cite evidence, find similar incidents, and recommend the next action.\"}"
echo
