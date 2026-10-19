# KAVACH_LIMITATIONS.md — Part 2 Implementation Status

This documents exactly what was implemented from the 17-limitation
blueprint, and what genuinely was not — honestly, per the blueprint's own
principle: "Target After scores are goals... must not be presented as
achieved performance until implementation and evaluation are completed."

## Polish Round 3 (live-dashboard bug fixes)
- [x] **Fixed genuine false negative**: "Government ID: 123456789012",
      "National identification number...", "Identity document number..."
      were NOT being flagged, only the literal word "Aadhaar"/"आधार" was
      recognized as context. Expanded `AADHAAR_CONTEXT_WORDS` in
      `patterns.py` to include generic government/national-ID phrasing.
      Verified against a 9-case regression matrix (all pass) — now locked
      in permanently as `tests/test_security.py::TestGovernmentIdContextCoverage`.
      **Still a fixed keyword list, not semantic understanding** — a
      phrasing not in this list (e.g. "SSN", "passport number") still
      won't be caught. This is consistent with Limitation #1/#3's known scope.
- [x] **Permanent fix for the recurring Gemini `.env` problem**: rather than
      recreating `.env` after every new folder/zip extraction, set
      `GEMINI_API_KEY` once as a persistent Windows user environment
      variable via `setx GEMINI_API_KEY "your_key"` (new terminal required
      after running it). `load_dotenv()` in `main.py` uses the default
      `override=False`, so it will never overwrite an already-set system
      variable — meaning this survives across any future folder replacement,
      with or without a `.env` file present.

## Polish Round 2

- [x] Unit tests added for all Part 2 modules — `tests/test_security_v2.py`
      (16 assertions, manually verified passing without needing the heavy
      RAG/ML dependencies, since these modules have no such dependency).
      This satisfies the blueprint's own rule: "Every Part 2 feature must
      map to a limitation, have a test."
- [x] Frontend now displays the policy engine's decision (`policy-card` in
      `index.html`/`app.js`) — risk score, action-risk classification, and
      plain explanation — previously only computed server-side and unused
      by the UI.
- [x] New `GET /agent/runs/{run_id}/explain` endpoint — plain-English,
      non-technical explanation of why a run was allowed/blocked/reviewed,
      built from the same `policy_decision` data (not a new decision source).
- [x] Explicit Hinglish gap documented as a test case (`SEC-06` in
      `data/security_v2_test_cases.json` + a dedicated test in
      `test_security_v2.py`) — the secret detector currently only matches
      English keyword+assignment patterns; a natural-language Hinglish
      credential mention is NOT caught. This is asserted as a **known,
      currently-true limitation**, not silently ignored.
- [x] `backend/requirements.txt` — pinned versions (exact `==` for
      qdrant-client/sentence-transformers, matching what was confirmed
      working in this project's environment; range pins `>=,<` for
      fastapi/pydantic/uvicorn/pytest/httpx to allow patch updates without
      risking a breaking major-version bump).

## Implemented Earlier This Pass

| # | Limitation | Status | What was built |
|---|---|---|---|
| 4 | Binary decisions need risk-adaptive policy | **Implemented** | `security/policy_engine.py` — combines data-sensitivity + action-risk into a 0.0-1.0 score, maps to ALLOW/REDACT/REVIEW/BLOCK. Wired into `orchestrator.py` at all three checkpoints (input, retrieved context, generated output). |
| 7 | Secrets/credentials need dedicated detector | **Implemented** | `security/secret_detector.py` — keyword+assignment pattern + Shannon-entropy gating, plus known provider-prefix matching (sk-, AIza, AKIA, ghp_, xox*). |
| 8 | Generated output needs a security gate | **Implemented** | Orchestrator now runs `_scan()` (PII + secrets) on `generated_output` before COMPLETE, routes through the same policy engine. |
| 10 | RAG evaluation path-normalization failure | **Fixed** | `backend/eval_rag.py` — both retrieved and ground-truth paths now normalized (backslash→forward-slash) before comparison. |
| 12 | Audit logs can leak sensitive data | **Implemented** | `security/audit_redaction.py` — `redact_text()` replaces detected values with `[REDACTED:category]`. Wired into orchestrator's error-history entries; `WorkflowRun.redacted_request_text` computed at request start and exposed via API instead of raw text where audit-safety matters. |
| 2, 11 | False positives / small eval dataset | **Partially addressed** | `data/security_v2_test_cases.json` adds credential cases + explicit hard-negative cases (order IDs, SKUs, transaction refs that superficially resemble PAN/Aadhaar patterns) + action-risk test cases. `security/evaluator_v2.py` reports real, honest results — **including a known remaining false positive** (case NEG-03: a PAN-shaped string in an unrelated sentence is still flagged, because negative-context suppression was not implemented this pass). |

## NOT Implemented This Pass — Genuine Remaining Gaps

Per the blueprint's own Limitation #17 ("Over-Engineering and Feature-Creep
Risk"), the following were deliberately **not** attempted in this session,
because each is a substantial standalone engineering effort (days, not
hours) that would risk destabilizing the verified v1.0 baseline if rushed:

- **#1 Unknown/novel identifier detection** — still pattern-based; an
  organization-specific identifier with no matching rule will not be
  caught. No ML-based semantic PII classifier was added.
- **#3 Full PII category coverage** — categories remain PAN/Aadhaar-like/
  phone/email/bank-account/credential; categories like health records,
  biometric identifiers, or org-specific secrets are not covered.
- **#5, #6 Secure/policy-aware RAG + prompt-injection isolation** —
  retrieved context is scanned for PII/secrets (as before), but there is
  no security-metadata tagging at ingestion time, no policy-aware
  retrieval filtering, and no isolation treating repository content as
  untrusted/potentially-adversarial input. This is the largest remaining
  architectural gap.
- **#9 Impact analyzer precision** — unchanged from v1.0 (~0.51-0.57
  precision, ~0.90-1.0 recall on 5 test cases). No ranking/precision
  improvement was attempted this pass.
- **#13 LLM output correctness** — validation remains Python syntax-only
  (`compile()`), not semantic/behavioral correctness checking.
- **#14 Authorization/resource-level access control** — no auth/RBAC layer
  exists; this is a genuinely new subsystem, not an extension of existing code.
- **#15 Broader multilingual/semantic coverage** — unchanged from Phase 4
  (Hindi/Marathi/Tamil/Telugu/Hinglish context-word matching).
- **#16 Production scalability/reliability/ops security** — this remains
  an academic/applied prototype (in-memory workflow store, local Qdrant,
  no deployment hardening), consistent with the blueprint's own framing.

## Honest Verification Status

- ✅ All 37 Python files (v1.0 + Part 2 additions) compile with 0 syntax errors.
- ✅ RAG path-normalization bug fix verified by code inspection (logic now
  matches on forward-slash-normalized paths on both sides).
- ⚠️ **Full pytest suite (164 tests) was NOT re-run in this session** —
  this environment ran out of disk space installing ML dependencies
  (torch/sentence-transformers). Run `python -m pytest tests -q` from
  `kavach/backend` on your own machine to get the real,
  current pass/fail count before treating this as final.
- ⚠️ `/evaluate/v2` and the new policy-engine behavior have **not** been
  exercised against a live server in this session, for the same reason —
  test them with `GET /evaluate/v2` and a few `/agent/request` calls
  after installing dependencies locally.

## Recommended Immediate Next Step

Run, on your own machine, in `kavach/backend`:
```
pip install -r requirements.txt
python -m pytest tests -q
python -c "from app.security.evaluator_v2 import evaluate_v2; import json; print(json.dumps(evaluate_v2(), indent=2))"
```
Report the actual numbers before claiming any of this is "done" in a
report or resume — consistent with the blueprint's own non-negotiable
regression rule.
