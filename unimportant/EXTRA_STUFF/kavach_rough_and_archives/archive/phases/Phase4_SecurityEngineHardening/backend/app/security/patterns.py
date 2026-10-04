"""
Entity patterns and multilingual context words (Phase 4 — see docs/PII_PATTERNS.md
and docs/MULTILINGUAL_SPEC.md).

Separated from detector.py so patterns/context-word lists can grow without
cluttering the detection logic itself.
"""

import re

PAN_PATTERN = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]{1}")
AADHAAR_PATTERN = re.compile(r"\d{4}[\s-]?\d{4}[\s-]?\d{4}")
PHONE_PATTERN = re.compile(r"(\+91[\-\s]?)?[6-9]\d{9}")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
# Generic long digit sequence used as a candidate for "bank account number" —
# only counted as a finding when a context word (below) appears nearby, since
# this pattern alone is far too broad (see docs/PII_PATTERNS.md design note).
GENERIC_LONG_DIGITS = re.compile(r"\d{9,18}")

# Context words that raise confidence a nearby number is a bank account
# number, across the languages in MULTILINGUAL_SPEC.md.
BANK_ACCOUNT_CONTEXT_WORDS = [
    "account number", "bank account", "a/c",           # English / Hinglish
    "बैंक खाता", "खाता नंबर",                            # Hindi
    "बँक खाते",                                          # Marathi
    "வங்கி கணக்கு",                                       # Tamil
    "బ్యాంక్ ఖాతా",                                       # Telugu
]

# Context words that help disambiguate a 12-digit number as Aadhaar-like
# rather than some other 12-digit sequence.
AADHAAR_CONTEXT_WORDS = [
    "aadhaar", "aadhar",
    "आधार",
    "ஆதார்",
    "ఆధార్",
]

# Context words that indicate the surrounding text is talking about a PAN,
# used to slightly raise confidence (the PAN regex itself is fairly specific
# already, so this is a secondary signal rather than a requirement).
PAN_CONTEXT_WORDS = ["pan", "पैन"]


def _has_nearby_context(text: str, match_start: int, match_end: int, context_words: list[str], window: int = 40) -> bool:
    """Check if any context word appears within `window` characters of a match."""
    lower_text = text.lower()
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    surrounding = lower_text[start:end]
    return any(word.lower() in surrounding for word in context_words)
