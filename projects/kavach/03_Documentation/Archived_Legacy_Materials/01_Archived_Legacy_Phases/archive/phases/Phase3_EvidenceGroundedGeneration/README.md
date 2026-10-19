# Phase 3 — Evidence-Grounded Generation

## What was built
- `backend/app/generation/llm_client.py` — pluggable LLM caller using
  Google Gemini's free tier (`GEMINI_API_KEY` in `backend/.env`, model
  `gemini-3.5-flash`). Falls back to a labeled stub if no key is set.
- `backend/app/generation/generator.py` — builds an evidence-grounded
  prompt from RAG-retrieved repository context before calling the LLM
  (Professor Idea #4 — don't let the LLM guess, feed it real evidence).
- `backend/app/generation/validator.py` — extracts code from the LLM
  response and runs a Python syntax check.

## Status
Tested end-to-end with a real Gemini API key: correctly generated a working
FastAPI endpoint grounded in actual repository code, and correctly refused
to hallucinate a feature (password reset) when no supporting evidence
existed in the repo yet.

## Setup required
`backend/.env` (never commit this):
```
GEMINI_API_KEY=your_free_key_from_aistudio.google.com/apikey
```

## Note
`orchestrator.py` and `main.py` (which wire this in) are not duplicated
here — see Complete_Merged_Project.
