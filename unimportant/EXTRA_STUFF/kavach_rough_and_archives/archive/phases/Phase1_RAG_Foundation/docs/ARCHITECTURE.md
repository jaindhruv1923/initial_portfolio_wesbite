# ARCHITECTURE.md — Kavach

## One-line analogy
The AI agent is the worker, the repository is the workshop, CI/CD is the factory
quality-control line, and Kavach is the security guard plus quality gate.

## End-to-End Pipeline

| Stage | What happens | Kavach's role |
|-------|---------------|----------------|
| 1. Developer intent | Natural-language request, e.g. "Add password reset." | Inspect input; policy/security checks; open audit record |
| 2. Agent planning | LLM decomposes the request into a structured plan | Govern the plan; detect unsafe/suspicious instructions |
| 3. Repository RAG | Retrieve relevant source, docs, APIs, dependencies, constraints | Inspect retrieved context for secrets/sensitive data |
| 4. Change-impact analysis | Predict affected files/functions/APIs/tests | Highlight security-sensitive components; produce impact report |
| 5. Evidence-grounded generation | Generate code using retrieved project evidence | Scan generated code for secrets, PII/SPDI, policy violations |
| 6. Test generation | Generate/update tests | Scan test fixtures/synthetic data; enforce policy (no real secrets) |
| 7. Build & tests | Compile/build and execute tests | Collect results; prevent progression on failed gates |
| 8. CI/CD security gate | Automated validation (GitHub Actions or equivalent) | Kavach policy gate decides pass / fail / review |
| 9. Human approval | Human reviews high-risk changes | Provide explanation, evidence, and audit trail |
| 10. Deployment/report | Deploy only when required gates pass; produce final report | Record complete decision history and metrics |

## Major System Components

| Component | Purpose | Output |
|-----------|---------|--------|
| Agent Orchestrator | Coordinates planning, retrieval, generation, testing, approvals | Structured workflow state |
| Repository Ingestion / RAG | Indexes source, docs, APIs, dependencies, constraints | Relevant evidence/context |
| Change-Impact Analyzer | Finds semantically related files/functions/likely-affected tests/APIs | Impact report + ranked components |
| Code Generation Agent | Produces repository-consistent modifications from retrieved evidence | Patch / code changes |
| Kavach Security Engine | Detects PII/SPDI, secrets, and policy/security violations | Allow / block / redact / review + reason |
| Multilingual NLP Layer | Processes Indian-language and code-mixed inputs | Normalized entities + detection results |
| Policy Engine | Maps detections to severity and enforcement rules | Policy decision |
| CI/CD Integration | Runs build, tests, security checks, validation | Pass/fail evidence |
| Audit Store | Persists events, decisions, findings, workflow metrics | Traceable audit log |
| Monitoring Dashboard | Shows live findings, severity, explanations, workflow state, metrics | Human-readable control plane |

## Interfaces

### A. Agent/User Interface
- Simple chatbot-like interface for entering natural-language dev requests.
- Shows agent workflow state and final response.
- Demonstrates multilingual sensitive-data detection in real time.

### B. Kavach Monitoring Dashboard
- Live feed of flagged events.
- Severity and confidence.
- Detected category and explanation.
- Original vs. redacted/blocked representation (where safe to display).
- Workflow/CI status.
- Audit log and compliance-style event view.
- Metrics: detections, blocks, latency, workflow success, test status, policy failures.

**Design principle:** the dashboard should be clean and functional but must not consume the
semester. Engineering, evaluation, and reliability of the underlying system matter far more than
visual complexity.

## Proposed Technical Stack

| Layer | Direction | Reason |
|-------|-----------|--------|
| Backend/API | Python + FastAPI | Simple service architecture, good fit for AI tooling |
| Agent orchestration | Python-based orchestrator, modular tool/agent design | Explicit, testable workflow |
| LLM | Local (Ollama, small/medium quantized) for routine tasks; cloud model for hard reasoning | Balances cost/privacy with reasoning quality |
| RAG / vector store | Qdrant or comparable | Repository/document retrieval |
| Repository analysis | Git parsing + AST/static-analysis tooling | Grounded code understanding, impact analysis |
| Database | SQLite initially; PostgreSQL if needed | Workflow events, findings, evaluation records |
| Frontend | React or lightweight HTML/JS | Separate agent UI and monitoring dashboard |
| CI/CD | GitHub Actions | Natural fit for repository-triggered workflows/gates |
| Containers | Docker | Reproducible local/CI deployment |
| Observability | Structured logs + metrics feeding the dashboard | Latency, decisions, workflow monitoring |

These are implementation recommendations, not hard requirements from the course.
