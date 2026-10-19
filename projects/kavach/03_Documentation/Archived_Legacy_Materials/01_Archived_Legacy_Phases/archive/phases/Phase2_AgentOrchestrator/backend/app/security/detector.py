"""
Kavach security detection — Phase 4 hardened version.

See docs/SECURITY_SPEC.md (severity tiers, explainability requirement) and
docs/MULTILINGUAL_SPEC.md (language scope, evaluation requirement).

Upgrades over the Phase 0 version:
  - Aadhaar-like number detection (context-gated, since a bare 12-digit
    pattern is far too broad on its own)
  - Bank account number detection (fully context-gated — no reliable regex
    exists on its own, see docs/PII_PATTERNS.md)
  - Severity tiers per docs/SECURITY_SPEC.md (low/medium/high/critical)
  - Confidence score per finding
  - Explanation string for every finding (what/why), satisfying the
    explainability requirement in SECURITY_SPEC.md
  - Multilingual context-word awareness (Hindi/Marathi/Tamil/Telugu/Hinglish)
    for disambiguating Aadhaar-like and bank-account numbers
"""

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

# Severity + default action per category, per docs/SECURITY_SPEC.md's draft table.
SEVERITY_MAP = {
    "PAN": {"severity": "high", "action": "BLOCK"},
    "Aadhaar-like": {"severity": "high", "action": "BLOCK"},
    "bank_account": {"severity": "high", "action": "BLOCK"},
    "phone_number": {"severity": "medium", "action": "REDACT"},
    "email": {"severity": "medium", "action": "REDACT"},
}


def _make_finding(category: str, value: str, confidence: float, reason: str) -> dict:
    meta = SEVERITY_MAP[category]
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
    Scan text for PAN, Aadhaar-like, phone, email, and bank-account patterns.
    Returns a list of finding dicts: {category, value, action, severity,
    confidence, reason} — see docs/SECURITY_SPEC.md's explainability
    requirement for why each field exists.
    """
    findings = []
    if not text:
        return findings

    # --- PAN: fairly specific pattern already (5 letters + 4 digits + 1 letter) ---
    for match in PAN_PATTERN.finditer(text):
        has_context = _has_nearby_context(text, match.start(), match.end(), PAN_CONTEXT_WORDS)
        confidence = 0.95 if has_context else 0.8  # pattern alone is already fairly distinctive
        reason = (
            f"Matches PAN format (5 letters + 4 digits + 1 letter)"
            + (", with 'PAN'/'पैन' mentioned nearby" if has_context else "")
        )
        findings.append(_make_finding("PAN", match.group(), confidence, reason))

    # --- Aadhaar-like: 12-digit pattern is broad, so require nearby context ---
    for match in AADHAAR_PATTERN.finditer(text):
        if _has_nearby_context(text, match.start(), match.end(), AADHAAR_CONTEXT_WORDS):
            findings.append(_make_finding(
                "Aadhaar-like", match.group(), 0.85,
                "12-digit number with 'Aadhaar'/'आधार' mentioned nearby"
            ))

    # --- Phone number: fairly specific (10 digits, starts 6-9) ---
    for match in PHONE_PATTERN.finditer(text):
        findings.append(_make_finding(
            "phone_number", match.group(), 0.75,
            "Matches Indian mobile number format (10 digits, starts with 6-9)"
        ))

    # --- Email: standard pattern, high confidence on its own ---
    for match in EMAIL_PATTERN.finditer(text):
        findings.append(_make_finding("email", match.group(), 0.95, "Matches email address format"))

    # --- Bank account: no reliable pattern alone — fully context-gated ---
    for match in GENERIC_LONG_DIGITS.finditer(text):
        # Skip if this digit sequence was already claimed by Aadhaar or phone above
        already_claimed = any(f["value"] == match.group() for f in findings)
        if already_claimed:
            continue
        if _has_nearby_context(text, match.start(), match.end(), BANK_ACCOUNT_CONTEXT_WORDS):
            findings.append(_make_finding(
                "bank_account", match.group(), 0.7,
                "9-18 digit number with a bank/account-related word mentioned nearby"
            ))

    return findings
