# KAVACH — "work" folder

This is the final consolidated package: the cleaned Phase 1-9 baseline
PLUS the Part 2 security-hardening additions built in this session.

## Start Here
1. **`Complete_Merged_Project/`** — the canonical, runnable application.
   Read **`Complete_Merged_Project/KAVACH_LIMITATIONS.md` first** — it
   honestly documents exactly what was implemented from the 17-limitation
   blueprint and what wasn't, plus the verification steps you must run
   locally before treating this as final.
2. `Phase1_RAG_Foundation/` through `Phase5_ChangeImpactAnalysis/` —
   historical phase-by-phase reference material (kept per the "don't
   destroy academic history" rule).
3. `project_documentation/` — the PPTX/DOCX deliverables from Phase 9.

## What's New in This Package (Part 2 additions)
- `backend/app/security/secret_detector.py` — credential/API-key detection
- `backend/app/security/policy_engine.py` — risk-adaptive ALLOW/REDACT/REVIEW/BLOCK
- `backend/app/security/audit_redaction.py` — redacts audit/history entries
- `backend/app/security/evaluator_v2.py` + `data/security_v2_test_cases.json`
- `backend/eval_rag.py` — path-normalization bug fixed
- `backend/app/agent/orchestrator.py` — rewritten to use the above at every checkpoint
- New endpoint: `GET /evaluate/v2`
- `KAVACH_LIMITATIONS.md` — the honest scope document

## Critical Next Step (cannot be skipped)
This session's sandbox ran out of disk space installing ML dependencies,
so **the full test suite was not re-run after these changes**. Before
treating this as final:
```
cd Complete_Merged_Project/backend
pip install -r requirements.txt
python setup_env.py
python -m pytest tests -q
```
Report the real result — do not assume it matches the old 164/0 baseline
until you've actually seen it.
