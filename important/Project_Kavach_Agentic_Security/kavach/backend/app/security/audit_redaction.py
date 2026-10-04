"""
Audit/history redaction (Part 2 — addresses Limitation #12: "Audit Logs
Can Become a Secondary Leakage Channel").

Before: the orchestrator's `history` log stored raw request/context text
in some cases, meaning a blocked request's sensitive value could still
leak through the audit trail itself. After: any text stored in audit/
history is passed through this redactor first.
"""

from app.security.detector import detect_pii
from app.security.secret_detector import detect_secrets


def redact_text(text: str) -> str:
    """
    Replace every detected sensitive value in text with a category-labeled
    placeholder, e.g. "my PAN is ABCDE1234F" -> "my PAN is [REDACTED:PAN]".
    Used before anything is written to audit/history storage.
    """
    if not text:
        return text

    findings = detect_pii(text) + detect_secrets(text)
    redacted = text
    # Replace longest values first so a shorter value that happens to be a
    # substring of a longer one doesn't get partially redacted first.
    for finding in sorted(findings, key=lambda f: len(f["value"]), reverse=True):
        value = finding["value"]
        category = finding["category"]
        redacted = redacted.replace(value, f"[REDACTED:{category}]")

    return redacted
