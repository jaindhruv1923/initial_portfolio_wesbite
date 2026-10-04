"""
Kavach Security Detection Engine.
Directly ported from the final-boss implementation in kavach/backend/app/security/detector.py.

Detects sensitive PII and identifiers:
  - PAN (Permanent Account Number)
  - Aadhaar / National ID (12-digit formatted or unformatted)
  - Phone numbers (10 digits)
  - Email addresses
  - Bank account numbers & generic sensitive numeric identifiers (9-18 digits, e.g. 1343345655)
"""

import re
try:
    from .patterns import (
        PAN_PATTERN,
        AADHAAR_PATTERN,
        PHONE_PATTERN,
        UNIVERSAL_10DIGIT_PATTERN,
        EMAIL_PATTERN,
        GENERIC_LONG_DIGITS,
        BANK_ACCOUNT_CONTEXT_WORDS,
        AADHAAR_CONTEXT_WORDS,
        PAN_CONTEXT_WORDS,
        _has_nearby_context,
    )
except (ImportError, ValueError):
    from patterns import (
        PAN_PATTERN,
        AADHAAR_PATTERN,
        PHONE_PATTERN,
        UNIVERSAL_10DIGIT_PATTERN,
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
        "type": category,
        "value": value,
        "matched_text": value,
        "action": meta["action"],
        "severity": meta["severity"],
        "confidence": round(confidence, 2),
        "reason": reason,
    }


def detect_pii(text: str) -> list[dict]:
    """
    Scan text for PAN, Aadhaar-like, phone, email, bank-account, and sensitive numeric patterns.
    Returns a list of finding dicts: {category, type, value, action, severity, confidence, reason}.
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

    # --- Phone number: 10 digits starting with 6-9 (with optional +91) ---
    for match in PHONE_PATTERN.finditer(text):
        val = match.group()
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
    # Catches any arbitrary 9 to 18-digit number like 1343345655
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
                f"Sensitive numeric identifier / sequence ({len(digits_only)} digits): {val}"
            ))

    return findings


if __name__ == "__main__":
    test_inputs = [
        "1343345655",
        "Here is the customer pan ABCDE1234F and phone 9876543210",
        "bank account no 12454323454",
        "aadhaar card 4532 8765 1092"
    ]
    for inp in test_inputs:
        print(f"\n--- Testing: '{inp}' ---")
        f = detect_pii(inp)
        for item in f:
            print(f"  [{item['category']}] val={item['value']} | action={item['action']} | reason={item['reason']}")
