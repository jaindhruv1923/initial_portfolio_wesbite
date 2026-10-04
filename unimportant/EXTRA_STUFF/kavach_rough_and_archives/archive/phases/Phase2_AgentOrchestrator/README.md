# Phase 2 — Agent Orchestrator

## What was built
- `backend/app/agent/state.py` — WorkflowStage state machine + in-memory WorkflowRun store.
- `backend/app/agent/planner.py` — rule-based task decomposition (honest
  note: keyword-based stub, not an LLM call — see module docstring).
- `backend/app/agent/orchestrator.py` — ties together: security check on
  raw input → planning → RAG retrieval → security check on retrieved context.
- `backend/app/security/detector.py` — PII detection extracted out of
  `main.py` so `/detect` and the orchestrator share one implementation.

## Status
Tested end-to-end: submitted natural-language requests, confirmed correct
planning, retrieval, and blocking behavior for sensitive input.

## Note
`orchestrator.py` and `detector.py` shown here are the **current, most
evolved** versions (they gained Phase 3/4/5 integration points over time,
not full rewrites). See Complete_Merged_Project for the definitive current
state of every file.
