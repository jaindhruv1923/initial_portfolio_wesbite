# Phase 5 — Change-Impact Analysis

## What was built (Professor Idea #1, focused slice)
- `backend/app/impact/dependency_graph.py` — parses `.py` files with
  Python's built-in `ast` module, extracts imports and top-level
  function/class definitions. No new dependency required.
- `backend/app/impact/analyzer.py` — combines semantic search (reuses
  Phase 1's `rag/embed_store.search()`) with the dependency graph to
  produce a ranked impact report: which files a proposed change might
  affect, with a relevance score and a human-readable reason.
- `data/impact_test_cases.json` — 5 test cases pairing a change
  description with the actually-known-affected files.
- `backend/app/impact/evaluator.py` — runs the test cases through the
  analyzer, computes precision/recall/F1 against the known-correct answers.

## Orchestrator integration
A new `IMPACT_ANALYSIS` workflow stage runs after the security check on
retrieved context and before code generation. `impact_report` now appears
in `/agent/request` and `/agent/runs/{id}` responses.

## New endpoints
- `POST /impact/analyze` — standalone testing (independent of the full
  agent workflow).
- `GET /impact/evaluate` — runs the test-case evaluation, returns real
  precision/recall/F1 numbers.

## Status
Built, not yet tested — see `docs/IMPLEMENTATION_STATUS.md`'s Phase 5
testing steps in Complete_Merged_Project for how to verify this.

## Scope discipline
This is a **focused component**, not a full repository-intelligence
product (see `docs/IMPACT_ANALYSIS_SPEC.md`) — it predicts impact for a
given change description; it does not attempt full static-analysis-grade
call-graph resolution.
