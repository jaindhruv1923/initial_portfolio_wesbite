"""
Secret / credential detector (Part 2 — addresses Limitation #7:
"Secrets and Credentials Require a Dedicated Detector").

PII detection (detector.py) and secret detection are deliberately kept as
separate modules with separate categories — a leaked API key is a
different risk shape than a leaked phone number (different severity
reasoning, different remediation: rotate the credential vs. redact the PII).

Approach: combine keyword/structural signals (assignment patterns like
`API_KEY=`, known provider prefixes) with a Shannon-entropy check, since
neither signal alone is reliable — a keyword alone catches placeholder
text like `API_KEY=your_key_here`, and entropy alone flags any random-
looking string (UUIDs, hashes) as a false positive.
"""

import math
import re

# Assignment-style patterns: NAME = value, NAME: value, NAME="value" — the
# keyword tells us this is *meant* to be a credential, regardless of format.
CREDENTIAL_KEYWORDS = [
    "api_key", "apikey", "api-key",
    "secret_key", "secretkey", "secret", "aws_secret_key",
    "access_token", "auth_token", "token",
    "password", "passwd", "pwd",
    "private_key", "client_secret",
    "aws_secret_access_key", "aws_access_key_id", "aws_access_key", "aws_key",
    "bearer",
]

ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(" + "|".join(CREDENTIAL_KEYWORDS) + r")\b\s*[:=]\s*['\"]?([A-Za-z0-9_\-/.+]{8,})['\"]?"
)

# Known provider key prefixes — high-confidence structural signals.
# NOTE: providers change key formats over time; verify current formats
# before relying on this list in a real deployment (see PII_PATTERNS.md's
# own caution about this).
PROVIDER_PREFIX_PATTERN = re.compile(
    r"\b(sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_\-]{20,}|AKIA[A-Z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9\-]{10,})\b"
)

# Placeholder text that looks like a credential assignment but isn't one —
# without this, "API_KEY=your_key_here" would be flagged, which is noise.
PLACEHOLDER_VALUES = {
    "your_key_here", "your_api_key", "changeme", "xxx", "todo",
    "placeholder", "example", "insert_key_here", "<your_key>",
    "your_key_yahan", "tumhari_key_yahan",  # honest nod to this project's own .env.example history
}


def _shannon_entropy(s: str) -> float:
    """Higher entropy = more random-looking = more likely a real secret
    rather than a readable word or placeholder."""
    if not s:
        return 0.0
    prob = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in prob)


# Public alias for core_engine and tests
calculate_shannon_entropy = _shannon_entropy


def detect_secrets(text: str) -> list[dict]:
    """
    Scan text for likely credentials/secrets.
    Returns findings in the same shape as security/detector.py's
    detect_pii(), so both can feed the same policy engine.
    """
    findings = []
    if not text:
        return findings

    # --- Provider-prefixed keys: high confidence, no entropy check needed ---
    for match in PROVIDER_PREFIX_PATTERN.finditer(text):
        findings.append({
            "category": "credential",
            "value": match.group(),
            "action": "BLOCK",
            "severity": "critical",
            "confidence": 0.95,
            "reason": "Matches a known credential prefix format (e.g. sk-, AIza, AKIA, ghp_, xox*)",
        })

    # --- Keyword + assignment pattern, gated by entropy to skip placeholders ---
    for match in ASSIGNMENT_PATTERN.finditer(text):
        keyword, value = match.group(1), match.group(2)
        if value.lower() in PLACEHOLDER_VALUES:
            continue
        entropy = _shannon_entropy(value)
        # Threshold chosen empirically: real API keys/tokens are typically
        # >3.5 bits/char; short English words sit lower. This is a
        # deliberately simple heuristic, not a calibrated ML model — see
        # KAVACH_LIMITATIONS.md for the honest scope of this check.
        if entropy < 3.0:
            continue
        already_found = any(f["value"] == value for f in findings)
        if already_found:
            continue
        findings.append({
            "category": "credential",
            "value": value,
            "action": "BLOCK",
            "severity": "critical",
            "confidence": round(min(0.6 + (entropy - 3.0) * 0.1, 0.9), 2),
            "reason": f"Assignment to '{keyword}' with a high-entropy value (entropy={entropy:.2f})",
        })

    return findings
