# PII_PATTERNS.md — Kavach

> Reference sheet for the entity formats the security engine needs to recognize. This is a
> starting point for Phase 4 (Kavach engine) — actual detection may combine these patterns with
> a trained model rather than relying on regex alone, especially for code-mixed text.

## PAN (Permanent Account Number)
- Format: 5 letters + 4 digits + 1 letter, e.g. `ABCDE1234F`
- Regex starting point: `[A-Z]{5}[0-9]{4}[A-Z]{1}`
- Note: this pattern alone will over-match random strings — context words nearby ("PAN",
  "pan card", "पैन") should raise confidence.

## Aadhaar-like Number
- Format: 12 digits, often shown in groups of 4: `1234 5678 9012`
- Regex starting point: `\d{4}[\s-]?\d{4}[\s-]?\d{4}`
- Note: this heavily overlaps with generic 12-digit numbers (phone-like patterns, order IDs).
  Context words ("आधार", "aadhaar", "ஆதார்") are important disambiguators.

## Indian Phone Number
- Format: 10 digits, often starting with 6-9; may have `+91` prefix
- Regex starting point: `(\+91[\-\s]?)?[6-9]\d{9}`

## Bank Account Number
- Format: highly variable (9-18 digits depending on bank) — no single reliable regex.
- Rely primarily on context words ("account number", "खाता नंबर", "बँक खाते", "வங்கி கணக்கு",
  "బ్యాంక్ ఖాతా") near a digit sequence of plausible length (9-18 digits).

## Email Address
- Format: standard email regex
- Regex starting point: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`

## Secrets / Credentials (API keys, tokens, passwords)
- No universal pattern — common heuristics:
  - Long random-looking alphanumeric strings (20+ chars) near words like "key", "token",
    "secret", "password", "api_key".
  - Known provider key prefixes if applicable (e.g. `sk-`, `AKIA` for some cloud providers) —
    verify current formats before relying on these, they change over time.

## Context-Word Reference (multilingual)
| Concept | Hindi | Marathi | Tamil | Telugu | Hinglish |
|---------|-------|---------|-------|--------|----------|
| PAN | पैन | PAN | PAN | PAN | PAN |
| Aadhaar | आधार | आधार | ஆதார் | ఆధార్ | Aadhaar |
| Bank account | बैंक खाता | बँक खाते | வங்கி கணக்கு | బ్యాంక్ ఖాతా | account |
| Phone number | फ़ोन नंबर | फोन नंबर | தொலைபேசி எண் | ఫోన్ నంబర్ | number |

## Design Note
Pure regex will produce both false positives (matching random 12-digit numbers) and false
negatives (missing obfuscated or spaced-out entities). The evaluation plan in
`EVALUATION_PLAN.md` exists specifically to measure this trade-off honestly rather than assume
regex alone is "done." A hybrid approach — regex/pattern candidates + a lightweight classifier
using surrounding context — is the intended direction; finalize during Phase 4.
