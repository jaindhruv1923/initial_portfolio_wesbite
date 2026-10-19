"""
KAVACH Multilingual Zero-Knowledge Token Vault.
Provides deterministic, reversible de-identification and rehydration of PII/SPDI/Secrets
under the Indian Digital Personal Data Protection (DPDP) Act 2023 & GDPR.
Integrated directly with the final-boss security detector from kavach/backend/app/security/.
"""

import re
import math
from typing import Dict, List, Tuple, Any

try:
    from .detector import detect_pii
    from .secret_detector import detect_secrets, calculate_shannon_entropy
except (ImportError, ValueError):
    from detector import detect_pii
    from secret_detector import detect_secrets, calculate_shannon_entropy


class TokenVault:
    """
    Manages Zero-Knowledge pseudonymization and rehydration of sensitive tokens.
    """
    def __init__(self):
        self._vault_store: Dict[str, str] = {}
        self._reverse_store: Dict[str, str] = {}
        self._counter: Dict[str, int] = {}

    def _generate_token_id(self, entity_type: str) -> str:
        clean_type = entity_type.upper().replace("-", "_")
        count = self._counter.get(clean_type, 0) + 1
        self._counter[clean_type] = count
        return f"<REDACTED_{clean_type}_{count:03d}>"

    def scan_and_redact(self, text: str) -> Tuple[str, List[Dict[str, Any]], Dict[str, str]]:
        """
        Scans input string using full Kavach PII, generic numeric identifier, and secret detectors.
        Redacts PII & secrets reversibly.
        Returns:
            sanitized_text (str)
            findings (list of dicts)
            session_vault (dict of token -> original)
        """
        if not text:
            return text, [], {}

        # 1. Detect both PII/numeric sequences and secrets/credentials
        raw_findings = detect_pii(text) + detect_secrets(text)
        
        findings = []
        sanitized_text = text
        session_vault: Dict[str, str] = {}

        # Sort findings from longest value to shortest to avoid substring collision
        sorted_findings = sorted(raw_findings, key=lambda f: len(f.get("value", "")), reverse=True)

        for item in sorted_findings:
            raw_val = item.get("value")
            category = item.get("category", "SENSITIVE")
            if not raw_val or raw_val not in sanitized_text:
                continue

            entropy = calculate_shannon_entropy(raw_val)

            # Assign or reuse token
            if raw_val not in self._reverse_store:
                token_id = self._generate_token_id(category)
                self._vault_store[token_id] = raw_val
                self._reverse_store[raw_val] = token_id
            else:
                token_id = self._reverse_store[raw_val]

            session_vault[token_id] = raw_val

            masked_val = (
                raw_val[:2] + "*" * (len(raw_val) - 4) + raw_val[-2:]
                if len(raw_val) > 4 else "****"
            )

            findings.append({
                "type": category,
                "category": category,
                "value": raw_val,
                "masked_value": masked_val,
                "token": token_id,
                "entropy": entropy,
                "action": item.get("action", "BLOCK"),
                "severity": item.get("severity", "high"),
                "reason": item.get("reason", f"Detected {category}")
            })

            # Replace raw value with token
            sanitized_text = sanitized_text.replace(raw_val, token_id)

        return sanitized_text, findings, session_vault

    def rehydrate(self, redacted_text: str, custom_vault: Dict[str, str] = None) -> str:
        """Restores original sensitive values from token placeholders."""
        vault = custom_vault if custom_vault is not None else self._vault_store
        result = redacted_text
        for token, original in vault.items():
            result = result.replace(token, original)
        return result

    def clear(self):
        """Wipes vault memory."""
        self._vault_store.clear()
        self._reverse_store.clear()
        self._counter.clear()


if __name__ == "__main__":
    vault = TokenVault()
    sample_text = (
        "Bhai customer ka Aadhaar 4532 8765 1092, PAN ABCDE1234F, random number 1343345655 "
        "aur AWS key AKIAIOSFODNN7EXAMPLE update krna hai."
    )
    print("--- ORIGINAL PROMPT ---")
    print(sample_text)
    
    redacted, findings, session_map = vault.scan_and_redact(sample_text)
    print("\n--- REDACTED PROMPT (DISPATCHED TO CLOUD LLM) ---")
    print(redacted)
    print("\n--- FINDINGS ---")
    for f in findings:
        print(f"[{f['type']}] val={f['value']} -> token={f['token']} | reason={f['reason']}")
    
    rehydrated = vault.rehydrate(redacted, session_map)
    print("\n--- REHYDRATED PROMPT ---")
    print(rehydrated)
    assert rehydrated == sample_text, "Rehydration check failed!"
    print("\n[SUCCESS] Vault Reversibility Verified 100%!")
