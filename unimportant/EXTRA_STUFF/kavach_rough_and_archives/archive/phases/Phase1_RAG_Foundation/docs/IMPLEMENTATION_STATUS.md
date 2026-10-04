# IMPLEMENTATION_STATUS.md — Kavach

> Keep this file updated as work progresses. Coding agents (Copilot, Claude Code, etc.) should
> read this before starting new work and update it after completing a milestone.

## Current Phase
Phase 5 — Change-Impact Analysis (built, ready to test) → Phase 6 (Multilingual — already
substantially covered by Phase 4) or Phase 8 (Dashboard) likely next

## Completed — Phase 5
- [x] `backend/app/impact/dependency_graph.py` — parses `.py` files with Python's built-in
      `ast` module, extracts imports and top-level function/class definitions, builds a
      simple dependency graph. No new dependency required.
- [x] `backend/app/impact/analyzer.py` — combines semantic search (reuses Phase 1's
      `rag/embed_store.search()`) with the dependency graph to produce a ranked impact
      report (file, relevance score, reason).
- [x] `data/impact_test_cases.json` — 5 test cases with a change description + known
      actual-affected files, for evaluation.
- [x] `backend/app/impact/evaluator.py` — runs the test cases through the analyzer,
      computes precision/recall/F1 (same pattern as security/evaluator.py).
- [x] Orchestrator extended: new IMPACT_ANALYSIS stage runs after the security check on
      retrieved context and before generation; `impact_report` now included in
      `/agent/request` and `/agent/runs/{id}` responses.
- [x] New endpoints: `POST /impact/analyze` (standalone testing), `GET /impact/evaluate`.
- [ ] Not yet tested — do this next (see testing note below).

## Completed — Phase 4
- [x] `backend/app/security/patterns.py` — regex patterns (PAN, Aadhaar-like, phone, email,
      generic long-digit candidate for bank accounts) plus multilingual context-word lists
      (Hindi/Marathi/Tamil/Telugu/Hinglish) used to disambiguate ambiguous patterns.
- [x] `backend/app/security/detector.py` rewritten: adds Aadhaar-like and bank-account
      detection (both context-gated, since neither has a reliable standalone regex — see
      PII_PATTERNS.md), severity tiers (low/medium/high/critical per SECURITY_SPEC.md),
      a confidence score per finding, and an explanation string satisfying the
      explainability requirement in SECURITY_SPEC.md.
- [x] `data/test_corpus.json` — machine-readable version of the 50-sentence multilingual
      test corpus (mirrors data/multilingual_test_corpus.md) for automated evaluation.
- [x] `backend/app/security/evaluator.py` — runs the full test corpus through detect_pii()
      and computes precision/recall/F1, overall and per language, per
      docs/EVALUATION_PLAN.md's "real baselines and metrics, never fabricated" rule.
- [x] New endpoint: `GET /evaluate` — returns the full evaluation report on demand.
- [ ] Not yet tested — do this next (see testing note below). Expected: high precision/recall
      on PAN and email (most distinctive patterns), possibly lower on Aadhaar-like/bank-account
      since those depend on context-word proximity — investigate and tune the `window` size in
      patterns.py's `_has_nearby_context()` if recall looks low on those categories.

## Completed — Phase 3
- [x] `backend/app/generation/llm_client.py` — pluggable LLM caller. Uses Google Gemini's
      free tier (via `GEMINI_API_KEY` env var, loaded from `backend/.env`) if configured;
      falls back to a clearly-labeled stub response if not, so the pipeline stays testable
      without an API key. Swap this file alone to switch to local Ollama later.
- [x] `backend/app/generation/generator.py` — builds an evidence-grounded prompt (Professor
      Idea #4: don't let the LLM guess repo structure, feed it real retrieved RAG context
      first) and calls the LLM.
- [x] `backend/app/generation/validator.py` — extracts code from the LLM response and runs
      a Python syntax check (`compile()`) as the first automated validation step (full test
      execution/CI comes later — Phase 7).
- [x] Orchestrator extended: GENERATION stage now runs after RAG retrieval, followed by a
      security check on the *generated* output (not just the original request — per
      SECURITY_SPEC.md, checks apply to generated code too) and the syntax check.
- [x] `.env.example` added; `.env` confirmed gitignored (never commit a real API key).
- [ ] Not yet tested with a real Gemini API key — only tested with the stub fallback so far.
      Get a free key at https://aistudio.google.com/apikey, put it in `backend/.env` as
      `GEMINI_API_KEY=...`, restart the server, and re-test to see real generated code.

## Completed — Phase 2
- [x] `backend/app/agent/state.py` — WorkflowStage state machine + in-memory WorkflowRun
      store (will move to the real DB from DATABASE_SPEC.md before this needs to persist
      across restarts).
- [x] `backend/app/agent/planner.py` — rule-based task decomposition (honest note: this is
      a keyword-based stub, NOT an LLM call yet — swap this out once Ollama/cloud LLM
      access is set up; see the module's docstring for why this was built first).
- [x] `backend/app/agent/orchestrator.py` — ties together: security check on raw input ->
      planning -> RAG retrieval (reuses Phase 1's search()) -> security check on retrieved
      context -> completion/block/review outcome.
- [x] `backend/app/security/detector.py` — PII detection logic extracted out of main.py so
      both `/detect` and the orchestrator share one implementation (no duplicated logic).
- [x] New endpoints: `POST /agent/request` (run the workflow), `GET /agent/runs/{id}`,
      `GET /agent/runs` (list all runs).
- [ ] Not yet tested — do this next (see testing note below).

## Completed — Phase 1
- [x] `backend/app/rag/ingest.py` — walks a repo, reads text/code files, chunks them
      (character-based, 1200 chars with 200 overlap — refine later if needed).
- [x] `backend/app/rag/embed_store.py` — embeds chunks with a small CPU-friendly
      sentence-transformers model (all-MiniLM-L6-v2) and stores/searches them in a local
      on-disk Qdrant instance (no Docker/server needed for dev).
- [x] `/ingest` and `/search` endpoints wired into `backend/app/main.py`.
- [x] Tested end-to-end: ingested `docs/` (45 chunks indexed successfully).
- [x] Tested `/search` with real queries — confirmed genuine semantic retrieval (e.g. query
      "what is Kavach and what problem does it solve" correctly returned the relevant
      PROJECT_SPEC.md and ARCHITECTURE.md chunks, not just keyword matches).
- [x] Fixed a Qdrant client API compatibility bug (installed qdrant-client 1.19.0 deprecated
      `.search()` — replaced with `.query_points()`).
- [ ] Not yet evaluated against a baseline (keyword search) — needed for Research Question 2 /
      EVALUATION_PLAN.md. Revisit during Phase 9 (Evaluation).

## Completed — Day 1
- [x] Project spec, architecture, security spec, multilingual spec, RAG spec, agent spec,
      impact-analysis spec, CI/CD spec, dashboard spec, database spec, testing spec,
      evaluation plan, and roadmap drafted.
- [x] Folder structure created (`backend/`, `frontend/`, `docs/`, `tests/`, `data/`).
- [x] Starter multilingual test corpus (initial small version).

## Completed — Day 2
- [x] Multilingual test corpus expanded to 50 examples (10 per language: Hindi, Marathi,
      Tamil, Telugu, Hinglish), balanced sensitive/non-sensitive for meaningful precision/
      recall/F1 evaluation.
- [x] `docs/PII_PATTERNS.md` — entity pattern reference (PAN, Aadhaar-like, phone, bank
      account, email) with multilingual context-word table, to guide Phase 4 detection
      engine design.

## Completed — Day 3
- [x] `docs/COMPETITIVE_ANALYSIS.md` — honest positioning against Lyzr, Langfuse, Fiddler,
      Arize, AgentOps.ai, with defensible answers for "why not just use an LLM API" and
      "couldn't a bigger company build this."
- [x] `backend/schema.sql` — actual SQL DDL matching DATABASE_SPEC.md.
- [x] `backend/app/main.py` — minimal runnable FastAPI skeleton (health check + root route).
- [x] `backend/requirements.txt` — starter dependency list.

## In Progress
- [ ] GitHub Copilot Student verification (pending approval).
- [ ] Pushing this repo to GitHub.

## Not Started (Phase 1 onward)
- [ ] Repository ingestion / RAG pipeline (Phase 1)
- [ ] Agent orchestrator (Phase 2)
- [ ] Evidence-grounded generation (Phase 3)
- [ ] Kavach security engine — real detection logic wired to PII_PATTERNS.md (Phase 4)
- [ ] Impact analysis (Phase 5)
- [ ] Multilingual detection layer using the full test corpus (Phase 6)
- [ ] CI/CD integration (Phase 7)
- [ ] Dashboard (Phase 8)
- [ ] Evaluation / experiments (Phase 9)
- [ ] Hardening / final demo prep (Phase 10)

## Known Open Decisions
- Exact embedding model / vector DB hosting choice for RAG.
- Local (Ollama) vs. cloud split for specific sub-tasks.
- Final severity-tier thresholds for the security engine.
- Regex-only vs. regex + lightweight classifier hybrid for PII detection (see
  PII_PATTERNS.md design note).

## Note for the next coding session
The backend is runnable right now:
    pip install -r backend/requirements.txt
    uvicorn app.main:app --reload --app-dir backend

**Phase 2 testing steps:**
1. First run `/ingest` (as in Phase 1) if the Qdrant index is empty, so `/agent/request`
   has repository context to retrieve.
2. Try `POST /agent/request` with `{"request_text": "Add a password reset feature"}` —
   expect `final_stage: COMPLETE`, a plan with auth/password-related steps (from the
   keyword planner), and retrieved_context pulled from the indexed docs.
3. Try it with a request containing a fake PAN-formatted string (5 letters + 4 digits +
   1 letter) — expect `final_stage: BLOCKED` and a finding in `security_findings`.
4. Try `GET /agent/runs` to confirm workflow runs are being tracked.

**Phase 4 testing steps:**
1. Try `GET /evaluate` directly (no request body needed) — expect a JSON report with
   `overall` precision/recall/F1 and a `per_language` breakdown for Hindi, Marathi, Tamil,
   Telugu, and Hinglish.
2. Try `/detect` with a Hindi sentence containing a fake Aadhaar, e.g.
   `{"text": "मेरा आधार नंबर 1234 5678 9012 है"}` — expect an Aadhaar-like finding with
   severity "high" and a reason string.
3. Try `/detect` with a safe-looking 12-digit number with NO Aadhaar context word nearby —
   expect no finding (proves the context-gating is working, not just matching any 12 digits).

**Phase 5 testing steps:**
1. First run `/ingest` with `{"repo_path": "app"}` if not already indexed this session.
2. Try `POST /impact/analyze` with
   `{"change_description": "Modify the security detection logic for PAN numbers"}` —
   expect `security/detector.py` and `security/patterns.py` to appear near the top of
   `impact_report` with the highest relevance scores.
3. Try `GET /impact/evaluate` — expect a JSON report with `overall` avg precision/recall/F1
   across the 5 test cases, plus a `per_case` breakdown.
4. Try `POST /agent/request` with any request — confirm `impact_report` now appears in
   the response alongside plan/retrieved_context/generation_result.
