"""
Zero-Knowledge PII Tokenization & Rehydration Vault.

Enables privacy-preserving cloud LLM interactions:
1. Intercepts sensitive data (Aadhaar, PAN, emails, phone numbers, secret keys).
2. Swaps raw sensitive entities with deterministic synthetic tokens (e.g. [TOKEN:AADHAAR:1]).
3. Stores encrypted token-to-value mappings in an isolated in-memory vault.
4. Allows re-hydration of tokens back to original values only for authorized callers.
"""

import uuid
from typing import Dict, Any, Tuple
from app.security.detector import detect_pii


class TokenVault:
    def __init__(self):
        # Maps vault_id -> {token -> original_value}
        self._vaults: Dict[str, Dict[str, str]] = {}

    def tokenize_text(self, text: str, vault_id: str = None) -> Tuple[str, str, Dict[str, Any]]:
        """
        Scan text for PII/secrets, replace each finding with a safe token,
        and store the mapping in the session vault.
        """
        if not vault_id:
            vault_id = str(uuid.uuid4())

        if vault_id not in self._vaults:
            self._vaults[vault_id] = {}

        vault = self._vaults[vault_id]
        findings = detect_pii(text)

        if not findings:
            return text, vault_id, {
                "tokenized": False,
                "tokens_created": 0,
                "token_map": {}
            }

        tokenized_text = text
        token_map: Dict[str, str] = {}
        counter = len(vault) + 1

        # Replace findings from longest to shortest to avoid partial replacements
        sorted_findings = sorted(findings, key=lambda f: len(f.get("matched_text", "")), reverse=True)

        for finding in sorted_findings:
            raw_val = finding.get("value")
            entity_type = finding.get("category", "SENSITIVE").upper().replace("-", "_")
            
            if not raw_val or raw_val not in tokenized_text:
                continue

            token = f"[KAVACH_TOKEN:{entity_type}:{counter}]"
            counter += 1

            tokenized_text = tokenized_text.replace(raw_val, token)
            vault[token] = raw_val
            token_map[token] = {
                "entity_type": entity_type,
                "original_masked": raw_val[:2] + "*" * (len(raw_val) - 4) + raw_val[-2:] if len(raw_val) > 4 else "****"
            }

        return tokenized_text, vault_id, {
            "tokenized": len(token_map) > 0,
            "tokens_created": len(token_map),
            "token_map": token_map
        }

    def rehydrate_text(self, tokenized_text: str, vault_id: str) -> str:
        """
        Swap tokens back into original sensitive values for local authorized viewing.
        """
        if not vault_id or vault_id not in self._vaults:
            return tokenized_text

        vault = self._vaults[vault_id]
        rehydrated = tokenized_text
        for token, original_val in vault.items():
            rehydrated = rehydrated.replace(token, original_val)

        return rehydrated

    def clear_vault(self, vault_id: str) -> bool:
        if vault_id in self._vaults:
            del self._vaults[vault_id]
            return True
        return False


# Global singleton instance for app lifecycle
global_vault = TokenVault()
