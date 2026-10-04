# Phase 7 — CI/CD (files only, no full project)

## Where these files go in your existing Complete_Merged_Project

```
Complete_Merged_Project/
├── .github/
│   └── workflows/
│       └── kavach-ci.yml       ← put this here (create .github/workflows/ if it doesn't exist)
└── backend/
    └── ci_security_gate.py     ← put this directly in backend/, alongside main.py's parent folder
```

## What this does

1. **`test` job** — installs dependencies, runs your existing `pytest tests -q`
   suite (the 164 tests Copilot verified), uploads results as an artifact.
2. **`security-gate` job** — runs `ci_security_gate.py`, which directly calls
   your Phase 4 security evaluator and Phase 5 impact evaluator (no server
   needed) and **fails the build** if precision/recall drop below a
   threshold. This is what gives CI/CD real teeth — not just "did tests
   pass" but "is quality still acceptable."
3. **`report` job** — writes a short pass/fail summary visible on the GitHub
   Actions run page.

## One-time setup on GitHub

If you want generation-related tests to exercise the real Gemini API in CI
(optional — the stub fallback means this isn't required for tests to pass):

1. Go to your repo → **Settings → Secrets and variables → Actions**
2. Add a new repository secret named `GEMINI_API_KEY` with your key
3. The workflow already references `secrets.GEMINI_API_KEY` — no other change needed

## To trigger it

Just push to `main` or open a pull request — GitHub Actions runs automatically.
Check the **Actions** tab on your repo to watch it run and see the summary.

## Thresholds (in `ci_security_gate.py`)

Set slightly below your last verified results (security: precision 1.0/
recall 1.0) so small expected fluctuations don't fail the build, while real
regressions still do:
- Security engine: precision ≥ 0.9, recall ≥ 0.85
- Impact analyzer: avg precision ≥ 0.5, avg recall ≥ 0.5

Adjust these numbers in the script if your actual results differ — they're
deliberately conservative starting points, not something you need to hit
exactly.
