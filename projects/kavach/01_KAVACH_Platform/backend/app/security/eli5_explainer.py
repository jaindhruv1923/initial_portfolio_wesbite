"""
Explain Like I'm 5 (ELI5) Security Threat Explainer & Auto-Remediation Engine.

Translates complex security violations and PII detections into:
1. Non-technical, plain-English explanations.
2. Real-world business & legal exploit risks (DPDP Act, GDPR, OWASP).
3. Immediate remediation recommendations.
4. Auto-sanitized alternative prompts for 1-click developer recovery.
"""

from typing import Dict, Any, List
import re

THREAT_PROFILES: Dict[str, Dict[str, str]] = {
    "PAN": {
        "title": "Permanent Account Number (PAN) Card Detected",
        "eli5": "You included a real Indian Tax ID (PAN) in the prompt.",
        "risk": "Exposing PAN numbers violates India's DPDP Act 2023 and IT Act 43A. If stored in LLM training corpora or log files, it enables financial identity theft.",
        "fix": "Use a mock identifier like 'ABCDE1234F' or enable Kavach's Zero-Knowledge Tokenization Vault."
    },
    "Aadhaar-like": {
        "title": "National ID / Aadhaar Number Detected",
        "eli5": "Found a 12-digit sequence matching the national biometric ID format.",
        "risk": "Aadhaar numbers are classified as Sensitive Personal Data. Leaking them can trigger severe UIDAI regulatory penalties and account takeover risks.",
        "fix": "Mask the digits (e.g. 'XXXX-XXXX-1234') or tokenize before submitting."
    },
    "sensitive_number": {
        "title": "Unmasked Sensitive Numeric Sequence Detected",
        "eli5": "You typed an unmasked 9-18 digit number (such as an account number or national identifier).",
        "risk": "Raw numeric identifiers in AI prompts often represent bank accounts, phone numbers, or credit cards.",
        "fix": "Replace raw digits with variable placeholders like '<ACCOUNT_NUM>'."
    },
    "phone_number": {
        "title": "Direct Contact / Phone Number Detected",
        "eli5": "Found a 10-digit mobile or telephone number.",
        "risk": "Enables spam, social engineering, and violates GDPR/DPDP personal data protection clauses.",
        "fix": "Use a dummy number like '+91-99999-00000'."
    },
    "email": {
        "title": "Personal Email Address Detected",
        "eli5": "An email address was found in the text.",
        "risk": "Direct email disclosure allows targeted spear-phishing and credential stuffing attacks.",
        "fix": "Use generic placeholders like 'user@example.com'."
    },
    "SYSTEM_OVERRIDE": {
        "title": "Prompt Injection / System Override Attack",
        "eli5": "The text attempted to tell the AI to ignore its system rules and security guardrails.",
        "risk": "Ranked #1 in OWASP Top 10 for LLMs. Attackers use this to bypass safety filters and hijack the model.",
        "fix": "Remove override phrases like 'ignore previous rules' and ask directly for the technical feature."
    },
    "SECRET_EXFILTRATION": {
        "title": "Secret Exfiltration / Credential Theft Attempt",
        "eli5": "The input tried to extract system environment variables, keys, or passwords.",
        "risk": "Could compromise infrastructure secrets, cloud credentials, or database keys.",
        "fix": "Develop code using mock environment configurations without exposing production secrets."
    }
}


def explain_threat_eli5(findings: List[Dict[str, Any]], original_text: str = "") -> Dict[str, Any]:
    """
    Generate an intuitive, educational threat summary and auto-sanitized prompt.
    """
    if not findings:
        return {
            "has_threats": False,
            "headline": "No Security Threats Detected",
            "summary": "Your input is safe and passed all Kavach governance checks.",
            "explanations": [],
            "sanitized_suggestion": original_text,
            "auto_fixable": False
        }

    explanations: List[Dict[str, str]] = []
    sanitized = original_text

    for f in findings:
        cat = f.get("category", "")
        val = f.get("value", "")
        profile = THREAT_PROFILES.get(cat, {
            "title": f"Security Finding: {cat}",
            "eli5": f"Detected sensitive pattern: {cat}",
            "risk": "Violates default organizational security baseline.",
            "fix": "Remove or sanitize the sensitive string."
        })

        explanations.append({
            "category": cat,
            "title": profile["title"],
            "value_found": val[:3] + "..." if len(val) > 4 else val,
            "simple_explanation": profile["eli5"],
            "business_risk": profile["risk"],
            "recommendation": profile["fix"]
        })

        if val and val in sanitized:
            sanitized = sanitized.replace(val, f"<MOCK_{cat.upper().replace('-', '_')}>")

    return {
        "has_threats": True,
        "threat_count": len(findings),
        "headline": f"Shield Triggered: {len(findings)} Security Policy Violation(s)",
        "summary": "Kavach intercepted your request to prevent confidential data leakage or jailbreak exploitation.",
        "explanations": explanations,
        "sanitized_suggestion": sanitized,
        "auto_fixable": bool(sanitized != original_text)
    }
