# KAVACH Project Map

Use this map when demonstrating a random part of the project.

## Runtime Entry Points

| Need | Open this file | Run / inspect |
|---|---|---|
| Start the API | `backend/app/main.py` | `python -m uvicorn app.main:app --app-dir backend --reload` |
| Open the dashboard | `frontend/index.html` | Serve with `python -m http.server 5500 --directory frontend` |
| Run the full workflow | `backend/app/agent/orchestrator.py` | `run_workflow()` |
| Configure Gemini | `backend/.env` | `GEMINI_API_KEY=...` |
| API documentation | `http://127.0.0.1:8000/docs` | FastAPI Swagger UI |

## Backend by Responsibility

### API layer

- `backend/app/main.py`: FastAPI app, routes, CORS, static dashboard serving, safe configuration status.

### Agent workflow

- `backend/app/agent/state.py`: workflow stages, run state, in-memory run store.
- `backend/app/agent/planner.py`: request-to-plan decomposition.
- `backend/app/agent/orchestrator.py`: complete request lifecycle and security checkpoints.

### Security

- `backend/app/security/detector.py`: PII and identifier detection.
- `backend/app/security/patterns.py`: format patterns and context terms.
- `backend/app/security/secret_detector.py`: credential and API-key detection.
- `backend/app/security/policy_engine.py`: Allow, Redact, Review, or Block decisions.
- `backend/app/security/audit_redaction.py`: audit-safe redaction.
- `backend/app/security/evaluator.py`: corpus metrics.

### Repository intelligence

- `backend/app/rag/ingest.py`: file discovery and text chunking.
- `backend/app/rag/embed_store.py`: embeddings, Qdrant indexing, similarity search.
- `backend/app/impact/analyzer.py`: affected-file ranking.
- `backend/app/impact/dependency_graph.py`: Python import/dependency analysis.

### Generation and validation

- `backend/app/generation/llm_client.py`: Gemini client and stub fallback.
- `backend/app/generation/generator.py`: evidence-grounded prompt and output generation.
- `backend/app/generation/validator.py`: generated-code extraction and syntax validation.

## New Product Endpoints

- `GET /config/status`: Gemini configured status without exposing the key.
- `POST /review`: standalone pasted-code PII, secret, policy, and remediation review.
- `POST /github/ingest`: public GitHub repository scanning and RAG indexing.
- `POST /agent/request`: complete governed agent workflow.
- `GET /agent/events/{run_id}`: Server-Sent Events (SSE) telemetry stream for real-time agent execution.
- `POST /webhook/github`: Inbound DevOps webhook for event-driven CI/CD pre-merge governance.
- `POST /ingest`: local repository indexing.
- `POST /detect`: direct PII detection.

## Frontend by Responsibility

- `frontend/index.html`: dashboard structure and controls.
- `frontend/app.js`: API calls, voice recognition, rendering, live metrics, activity feed.
- `frontend/style.css`: dashboard layout, responsive design, animations, interaction states.

## Tests and Evidence

- `tests/test_security.py`: PII and numeric-policy behavior.
- `tests/test_api_endpoints.py`: HTTP contracts.
- `tests/test_agent.py`: orchestration behavior.
- `tests/test_generation.py`: grounded generation and validation.
- `tests/test_rag.py`: ingestion, embeddings, and search.
- `tests/test_impact.py`: dependency and impact scoring.
- `tests/test_integration.py`: end-to-end flow.
- `run_tests.py`: compact test runner.
- `verify_project.py`: full verification script.
- `artifacts/screenshots/`: dashboard and demonstration captures.
- `artifacts/reports/`: captured test and security reports.

## Academic Compliance & Phase 1 Submission Artifacts

- `docs/submissions/PHASE_1_PROJECT_CHARTER.md`: Official 1-page Project Charter & Synopsis (C1–C5 Rubrics).
- `docs/submissions/PROJECT_TIMELINE.md`: 16-week timeline mapped to CSE3101 course weeks.
- `docs/submissions/TEAM_RESPONSIBILITY_MATRIX.md`: RACIS matrix with role rotation across Phases 1, 2, and 3.
- `docs/submissions/VIVA_DEFENSE_AND_EVALUATION_GUIDE.md`: Comprehensive viva defense questions & answers for evaluators.
- `docs/PEAS_AND_PERSONA_SPECIFICATION.md`: Formal PEAS matrix, domain state space, and agent/user persona linkage.
- `docs/CRITICAL_PLAY_AREAS_EVALUATION.md`: Empirical study for Slides 4 & 5 (LLM parameters, architectures, MCP vs P2P, latency bottlenecks).
- `docs/PROMPT_STRATEGIES_AND_RAG_STUDY.md`: Formal evaluation of ReAct vs CoT vs COTS vs Zero-Shot prompting and Qdrant RAG.
- `backend/data/workflow_runs.json`: 42 logged evaluation runs with full stage traces, latency breakdowns, and persona linkage.

## Documentation and Presentation

- `docs/PROJECT_SPEC.md`: requirements and scope.
- `docs/ARCHITECTURE.md`: system design.
- `docs/SECURITY_SPEC.md`: security behavior.
- `docs/IMPLEMENTATION_STATUS.md`: implementation tracking.
- `docs/presentations/KAVACH_Presentation.pptx`: original deck.
- `docs/presentations/KAVACH_Presentation_Updated.pptx`: corrected deck.
- `docs/presentations/new_additions.pptx`: current additions and roadmap deck.
- `docs/presentations/new_additions_report.md`: current additions report.

## Historical Snapshots

`archive/phases/Phase1_RAG_Foundation` through `archive/phases/Phase5_Change_Impact_Analysis` preserve the staged development history. Do not edit them when changing the live project; implement current changes only in `kavach`.
