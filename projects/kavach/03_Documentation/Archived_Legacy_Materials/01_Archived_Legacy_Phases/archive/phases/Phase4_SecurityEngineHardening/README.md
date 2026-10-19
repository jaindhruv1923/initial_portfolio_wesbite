# Phase 4 — Kavach Security Engine Hardening

## What was built
- `backend/app/security/patterns.py` — regex patterns (PAN, Aadhaar-like,
  phone, email, generic long-digit candidate for bank accounts) plus
  multilingual context-word lists (Hindi/Marathi/Tamil/Telugu/Hinglish).
- `backend/app/security/detector.py` (rewritten) — adds Aadhaar-like and
  bank-account detection (context-gated), severity tiers, confidence
  scores, and an explanation string per finding.
- `data/test_corpus.json` — 50-sentence multilingual test corpus for
  automated evaluation.
- `backend/app/security/evaluator.py` — computes precision/recall/F1,
  overall and per language.

## Status — evaluation results (corrected)

**Update:** the first evaluation run showed a recall gap in Marathi/Tamil/
Telugu (0.833 recall, 1 false negative each). Root-cause investigation
found this was a **test corpus authoring bug**, not a detector bug — three
sentences (MR-10, TA-10, TE-10) about a lost PAN card were missing the
actual PAN value in the text (unlike their Hindi/Hinglish equivalents,
which correctly included `ABCDE1234F`). The detector was correctly
reporting "no PAN found" because there genuinely was no PAN pattern in
those three test sentences.

After fixing the three corpus entries to include the PAN value (matching
the pattern of the other languages):

```
Overall:  precision 1.0, recall 1.0, F1 1.0 (zero false positives, zero false negatives)
Hindi:    precision 1.0, recall 1.0, f1 1.0
Marathi:  precision 1.0, recall 1.0, f1 1.0
Tamil:    precision 1.0, recall 1.0, f1 1.0
Telugu:   precision 1.0, recall 1.0, f1 1.0
Hinglish: precision 1.0, recall 1.0, f1 1.0
```

This is a good story for the report/viva: the evaluation process itself
caught a data-quality issue, the root cause was correctly diagnosed (data,
not code), and the fix was verified with a re-run — exactly the kind of
rigor `docs/EVALUATION_PLAN.md` asks for.

## Note
`main.py` (which exposes `/evaluate`) is not duplicated here — see
Complete_Merged_Project.
