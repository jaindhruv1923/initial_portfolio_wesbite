# Implementation Plan: Multilingual Removal & Universal Number Detection

Remove the impractical multilingual features across KAVACH and upgrade the security engine and frontend dashboard to automatically read and flag **any** sensitive number (12-digit Aadhaar/National ID, 11-digit numbers like `12454323454`, 10-digit phone numbers, and 9-18 digit account/card numbers) without requiring rigid prefix phrases like `"my aadhar card number is ..."`.

## User Review Required

> [!IMPORTANT]
> **Multilingual Removal**: Non-English context keyword dictionaries (Hindi, Marathi, Tamil, Telugu, Hinglish) in [patterns.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/backend/app/security/patterns.py) and multilingual test sets will be cleanly replaced with realistic, production-ready English DevOps test cases.
>
> **Universal Number Detection**: Previously, 12-digit numbers and long digit sequences were ignored unless preceded by the exact keyword "aadhaar" or "bank account". We are decoupling detection from mandatory keywords so **any** sensitive number sequence entered into the frontend dashboard (e.g. `12454323454`, `123456789012`, `1234 5678 9012`, etc.) is immediately parsed, classified, and flagged.

## Proposed Changes

### Backend Security Engine

#### [MODIFY] [patterns.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/backend/app/security/patterns.py)
- Remove all non-English script keywords (Hindi, Marathi, Tamil, Telugu) from context word lists.
- Refine `AADHAAR_PATTERN` to match formatted and unformatted 12-digit numbers (`\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b`).
- Define `GENERIC_SENSITIVE_NUMBER_PATTERN` to recognize standalone numeric sequences between 10 and 18 digits (including 11-digit numbers like `12454323454` and account numbers) even when no context keyword is present.
- Retain standard English context keywords as confidence boosters (e.g., "aadhaar", "id", "account", "pan"), but not as strict blockers for detection.

#### [MODIFY] [detector.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/backend/app/security/detector.py)
- Update `detect_pii`:
  - Flag any 12-digit number as `Aadhaar-like` / `National ID` (confidence 0.95 with context, 0.85 without context).
  - Flag any 10-digit number matching mobile format as `phone_number`.
  - Flag any 10-18 digit numeric sequence (including 11-digit numbers like `12454323454`, credit card numbers, or bank accounts) as `sensitive_number` or `bank_account`.
  - Include the actual detected value and a human-friendly reason (e.g., `"Detected 11-digit sensitive number sequence (12454323454)"`).
- Update `SEVERITY_MAP` to ensure `sensitive_number` is classified as `high` severity with default action `BLOCK` or `REVIEW`.

#### [MODIFY] [evaluator.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/backend/app/security/evaluator.py)
- Remove `per_language` dictionary breakdown (Hindi, Marathi, Tamil, Telugu, Hinglish).
- Report overall and category-level precision, recall, and F1 metrics on the updated English corpus.

#### [MODIFY] [test_corpus.json](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/data/test_corpus.json)
- Replace non-English cases with realistic English DevOps prompts, sensitive queries, bare number inputs, and edge cases.

#### [MODIFY] [main.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/backend/app/main.py)
- Update FastAPI title and description to remove "Multilingual".
- Clean up docstrings referencing multilingual features.

---

### Frontend Dashboard

#### [MODIFY] [index.html](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/frontend/index.html)
- Update header subtitle to remove "Multilingual".
- Update textarea placeholder to reflect realistic requests and sensitive number testing.

#### [MODIFY] [app.js](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/frontend/app.js)
- Enhance `renderSecurityStatus`:
  - Clearly display detected sensitive numbers with partial masking for privacy (e.g., `1245****454` or `XXXX-XXXX-9012`).
  - Highlight the exact category, severity, and explanation so the user immediately sees that their entered number was read and flagged.
- Ensure the pipeline accurately halts and marks `BLOCKED` or `NEEDS_REVIEW` whenever any number or sensitive data is provided.

#### [MODIFY] [style.css](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/frontend/style.css)
- Add styling for masked value badges and high-visibility alert cards for flagged numbers.

---

### Test Suite

#### [MODIFY] [test_security.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/tests/test_security.py)
- Remove multilingual tests (`test_pan_detection_hindi`, `test_aadhaar_hindi_context`, `test_bank_account_hindi_context`, `test_multilingual_safe_text`, `test_evaluate_coverage_all_languages`).
- Add comprehensive test cases verifying that bare numbers (e.g., `12454323454`, `123456789012`, `1234 5678 9012`, `9876543210`) are flagged without requiring "my aadhar card number is" or other context words.
- Update regression tests to verify that sensitive numbers are properly caught while normal English developer prompts (e.g., "Add a health check endpoint on port 8080") remain safe.

#### [MODIFY] [test_rag.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/tests/test_rag.py)
- Replace Hindi query test with standard English semantic retrieval test.

#### [MODIFY] [test_impact.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/tests/test_impact.py)
- Replace Hindi change description with standard English change description.

#### [MODIFY] [test_integration.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/tests/test_integration.py)
- Replace Hindi and Marathi end-to-end workflow requests with English requests.

#### [MODIFY] [conftest.py](file:///e:/PRJ-IV%20Work/codebase/Complete_Merged_Project/tests/conftest.py)
- Remove multilingual fixtures.

## Verification Plan

### Automated Tests
- Run full pytest suite across `Complete_Merged_Project`:
  ```bash
  cd "e:\PRJ-IV Work\codebase\Complete_Merged_Project"
  python -m pytest tests -v
  ```
- Run the security evaluation endpoint test:
  ```bash
  python -c "from app.security.evaluator import evaluate; print(evaluate())"
  ```
- Verify specific number detection:
  ```bash
  python -c "from app.security.detector import detect_pii; print(detect_pii('12454323454')); print(detect_pii('123456789012')); print(detect_pii('my aadhar card number is 12454323454'))"
  ```

### Manual Verification
- Start FastAPI backend:
  ```bash
  uvicorn app.main:app --reload --app-dir backend
  ```
- Open frontend dashboard in browser.
- Test input with `12454323454` -> verify immediate detection, masked preview, and flagged security status.
- Test input with `123456789012` -> verify Aadhaar / National ID detection and blocking.
- Test input with standard safe developer prompt `Add a health check endpoint returning JSON status` -> verify SAFE verdict and workflow completion.
