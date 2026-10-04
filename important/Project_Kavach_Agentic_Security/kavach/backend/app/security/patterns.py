"""
Entity patterns and context words for security detection.
"""

import re

PAN_PATTERN = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b")
# Matches formatted (1234 5678 9012, 1234-5678-9012) and unformatted (123456789012) 12-digit numbers
AADHAAR_PATTERN = re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
# Generic long digit sequence (9 to 18 digits) for sensitive numeric identifiers,
# bank accounts, card numbers, or bare ID sequences (e.g. 12454323454).
GENERIC_LONG_DIGITS = re.compile(r"\b\d{9,18}\b")

# Context words that indicate a nearby number is a bank account number
BANK_ACCOUNT_CONTEXT_WORDS = [
    "account number", "bank account", "a/c", "account no", "acc no", "acct",
]

# Context words that help disambiguate government / national identity numbers
AADHAAR_CONTEXT_WORDS = [
    "aadhaar", "aadhar", "uid", "uidai",
    "government id", "govt id", "national id", "national identification",
    "identity document", "identification number", "id number",
    "identity card", "national identity", "aadhar card", "aadhaar card",
]

# Context words that indicate the surrounding text refers to a PAN
PAN_CONTEXT_WORDS = ["pan", "pan card", "pan number"]


def _has_nearby_context(text: str, match_start: int, match_end: int, context_words: list[str], window: int = 40) -> bool:
    """Check if any context word appears within `window` characters of a match."""
    lower_text = text.lower()
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    surrounding = lower_text[start:end]
    return any(word.lower() in surrounding for word in context_words)
