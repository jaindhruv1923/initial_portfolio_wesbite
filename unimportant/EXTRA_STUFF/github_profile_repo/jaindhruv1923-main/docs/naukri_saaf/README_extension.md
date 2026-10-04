# Naukri Saaf — Job Fit & Ghost Check (Chrome Extension)

100% local. No API calls, no backend, no network requests of any kind — everything
(skill extraction, resume matching, legitimacy scoring) runs in JavaScript inside your
browser. Your resume text never leaves your machine.

## Install (Developer Mode — this isn't on the Chrome Web Store)

1. Open `chrome://extensions` in Chrome.
2. Turn on **Developer mode** (top-right toggle).
3. Click **Load unpacked**.
4. Select the `naukri-saaf-extension` folder (this folder).
5. Pin the extension (puzzle-piece icon in the toolbar → pin "Naukri Saaf").

## Use it

1. Click the extension icon — it opens as a **side panel** (stays open while you browse).
2. Go to any job posting on LinkedIn, Naukri, Indeed, or Glassdoor.
3. Click the **↻** button in the panel to read the page.
4. **Overview tab** — title, company, extracted skills, full JD text.
5. **Resume Match tab** — paste your resume text once (saved locally via `chrome.storage`),
   get a 0-10 fit score, matched vs. missing skills, and concrete next steps.
6. **Legitimacy tab** — a risk score built from the same signal set as your trained GBM
   model (`feature_importance_v3.csv`). Signals readable from the page itself (description
   length, salary disclosure, urgency language, contact-bypass patterns, listing age, etc.)
   are scored directly. Signals that need live web data (repost count, cross-platform
   duplicates, portal baseline rate, market salary comparison) are flagged as **manual
   check** with one-click search links, since this extension makes no network calls.

## Honest limitations

- **Site scraping is selector-based.** If LinkedIn/Naukri/Indeed change their page markup,
  the content script's selectors may need updating — there's a generic fallback (grabs the
  largest visible text block) but it's less precise.
- **This is not your trained GBM model running in the browser.** Running an actual
  scikit-learn `.pkl` model client-side would need conversion to ONNX/TF.js and a fair bit
  of extra engineering. What ships here is a rule-based scorecard weighted by your model's
  real `feature_importance_v3.csv` values — same signal set, heuristic evaluation instead of
  the trained model's learned boundaries. Treat the risk score as a fast triage flag, not a
  0.72-AUC-grade decision.
- **Resume matching is TF-based cosine similarity + a skill dictionary**, not an LLM
  reading for nuance. It will catch keyword overlap reliably; it won't catch things like
  "led a team of 5" implying seniority the JD wants.
- **~10 of the 26 model signals genuinely can't be computed from a single static page**
  (repost count, application velocity, cross-platform duplicates, etc.) — those show up in
  a separate "needs manual check" section with pre-built search links instead of being
  silently guessed at.

## Extend it

- Add more site selectors in `content.js` if you use other portals.
- Expand `SKILL_DICTIONARY` in `lib/nlp.js` as your target roles change.
- If you later want the actual trained model or live web search (SerpAPI/Google CSE) wired
  in, that needs a small local backend the extension can call — happy to build that layer
  whenever you're ready for it.
