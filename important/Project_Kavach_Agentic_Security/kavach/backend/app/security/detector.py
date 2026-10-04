"""
Kavach security detection engine.

Detects sensitive PII and identifiers:
  - PAN (Permanent Account Number)
  - Aadhaar / National ID (12-digit formatted or unformatted)
  - Phone numbers (10 digits)
  - Email addresses
  - Bank account numbers & generic sensitive numeric identifiers (9-18 digits)
"""

import re
from app.security.patterns import (
    PAN_PATTERN,
    AADHAAR_PATTERN,
    PHONE_PATTERN,
    EMAIL_PATTERN,
    GENERIC_LONG_DIGITS,
    BANK_ACCOUNT_CONTEXT_WORDS,
    AADHAAR_CONTEXT_WORDS,
    PAN_CONTEXT_WORDS,
    _has_nearby_context,
)

# Severity + default action per category
SEVERITY_MAP = {
    "PAN": {"severity": "high", "action": "BLOCK"},
    "Aadhaar-like": {"severity": "high", "action": "BLOCK"},
    "bank_account": {"severity": "high", "action": "BLOCK"},
    "sensitive_number": {"severity": "high", "action": "BLOCK"},
    "phone_number": {"severity": "medium", "action": "REDACT"},
    "email": {"severity": "medium", "action": "REDACT"},
}


def _make_finding(category: str, value: str, confidence: float, reason: str) -> dict:
    meta = SEVERITY_MAP.get(category, {"severity": "high", "action": "BLOCK"})
    return {
        "category": category,
        "value": value,
        "action": meta["action"],
        "severity": meta["severity"],
        "confidence": round(confidence, 2),
        "reason": reason,
    }


def detect_pii(text: str) -> list[dict]:
    """
    Scan text for PAN, Aadhaar-like, phone, email, bank-account, and sensitive numeric patterns.
    Returns a list of finding dicts: {category, value, action, severity, confidence, reason}.
    """
    findings = []
    if not text:
        return findings

    # --- PAN: 5 letters + 4 digits + 1 letter ---
    for match in PAN_PATTERN.finditer(text):
        has_context = _has_nearby_context(text, match.start(), match.end(), PAN_CONTEXT_WORDS)
        confidence = 0.95 if has_context else 0.85
        reason = (
            "Matches PAN format (5 letters + 4 digits + 1 letter)"
            + (", with PAN context nearby" if has_context else "")
        )
        findings.append(_make_finding("PAN", match.group(), confidence, reason))

    # --- Aadhaar-like / 12-digit number ---
    for match in AADHAAR_PATTERN.finditer(text):
        val = match.group()
        # Ensure it is a 12-digit number (formatted or plain)
        digits_only = re.sub(r"\D", "", val)
        if len(digits_only) == 12:
            has_bank_ctx = _has_nearby_context(text, match.start(), match.end(), BANK_ACCOUNT_CONTEXT_WORDS)
            if has_bank_ctx:
                findings.append(_make_finding(
                    "bank_account", val, 0.90,
                    f"12-digit number with bank/account context: {val}"
                ))
            else:
                has_context = _has_nearby_context(text, match.start(), match.end(), AADHAAR_CONTEXT_WORDS)
                confidence = 0.95 if has_context else 0.85
                reason = (
                    f"12-digit national identifier (Aadhaar format: {val})"
                    + (", with identity context nearby" if has_context else "")
                )
                findings.append(_make_finding("Aadhaar-like", val, confidence, reason))

    # --- Phone number: 10 digits (with optional +91) ---
    for match in PHONE_PATTERN.finditer(text):
        val = match.group()
        # Avoid double-counting if part of an already detected entity
        if any(val in f["value"] for f in findings):
            continue
        findings.append(_make_finding(
            "phone_number", val, 0.85,
            f"Matches mobile phone number format: {val}"
        ))

    # --- Email: standard format ---
    for match in EMAIL_PATTERN.finditer(text):
        findings.append(_make_finding("email", match.group(), 0.95, "Matches email address format"))

    # --- Generic Long Digits / Sensitive numbers / Bank accounts (9-18 digits) ---
    for match in GENERIC_LONG_DIGITS.finditer(text):
        val = match.group()
        digits_only = re.sub(r"\D", "", val)

        # Skip if this digit sequence was already claimed by Aadhaar or phone above
        already_claimed = any(
            digits_only == re.sub(r"\D", "", f["value"]) or val in f["value"] or f["value"] in val
            for f in findings
        )
        if already_claimed:
            continue

        has_aadhaar_ctx = _has_nearby_context(text, match.start(), match.end(), AADHAAR_CONTEXT_WORDS)
        has_bank_ctx = _has_nearby_context(text, match.start(), match.end(), BANK_ACCOUNT_CONTEXT_WORDS)

        if has_aadhaar_ctx:
            findings.append(_make_finding(
                "Aadhaar-like", val, 0.90,
                f"Sensitive numeric identifier with Aadhaar/ID context: {val}"
            ))
        elif has_bank_ctx:
            findings.append(_make_finding(
                "bank_account", val, 0.85,
                f"9-18 digit number with bank/account context: {val}"
            ))
        else:
            findings.append(_make_finding(
                "sensitive_number", val, 0.85,
                f"Sensitive numeric identifier / sequence: {val}"
            ))

    return findings

