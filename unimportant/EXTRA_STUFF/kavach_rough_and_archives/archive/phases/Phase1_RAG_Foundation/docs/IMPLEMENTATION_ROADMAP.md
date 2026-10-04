# IMPLEMENTATION_ROADMAP.md — Kavach

| Phase | Focus | Exit criterion |
|-------|-------|------------------|
| 0 | Requirements | Architecture, research questions, datasets, metrics, threat model frozen |
| 1 | Repository foundation | Repository ingestion, chunking/indexing, metadata, retrieval, baseline search working |
| 2 | Agent workflow | Planner, tool interface, workflow state, controlled execution — end-to-end dry-run works |
| 3 | Evidence-grounded generation | RAG-conditioned code generation + automated build/test validation |
| 4 | Kavach engine | PII/SPDI, secrets, policies, severity, redaction/block/review, audit — unsafe artifacts consistently gated |
| 5 | Impact analysis | Semantic affected-component prediction + reporting, evaluable against known cases |
| 6 | Multilingual | Language/code-mix handling, normalization, test corpus — supported languages have measurable results |
| 7 | CI/CD | GitHub Actions, security gates, artifacts, reports — PR triggers automated validation |
| 8 | Dashboard | Live findings, workflow status, audit, metrics — full demo understandable without a developer narrating |
| 9 | Evaluation | Baselines, experiments, metrics, error analysis, ablations — reproducible and defensible |
| 10 | Hardening | Failure handling, security review, documentation, demo rehearsal |

## Suggested Timeline (adjust as reality dictates)
| Period | Target |
|--------|--------|
| Days 1–2 | Master specs (this folder), repo setup, architecture skeleton |
| Days 2–5 | Backend, repository ingestion, RAG |
| Days 5–8 | Agent planning, evidence-grounded generation, tests |
| Days 8–11 | Kavach security engine, policies, audit, explainability |
| Days 11–14 | Multilingual layer + impact analysis |
| Days 14–17 | CI/CD + dashboard + integration |
| Weeks 3–5 | Bug fixing, regression tests, security/RAG/multilingual tuning, evaluation |
| Weeks 4–6 | Final experiments, documentation, hardening, demo prep |

**Mid-semester checkpoint target:** Phases 0–4 complete and demonstrable (agent workflow +
RAG + generation + core security engine working end-to-end, even if multilingual/impact-
analysis/dashboard are still in progress).

This is an estimate, not a guarantee — adjust based on actual weekly progress.
