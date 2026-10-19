"""
RAG Indirect Prompt Injection Sanitizer & Air-Gapped Context Scrubber for KAVACH Enterprise v3.0.
Addresses Limitations #5 & #6:
Treats repository and retrieved RAG context as untrusted adversarial inputs.
Detects hidden instructions, delimiter jailbreaks, system prompt overrides,
and malicious markdown exfiltration links inside indexed files before LLM synthesis.
"""

from typing import Dict, Any, List, Optional
import re
from app.security.injection_shield import inspect_prompt_safety
from app.security.steganography_shield import inspect_and_neutralize_steganography


INDIRECT_INJECTION_PATTERNS = [
    r"(?i)ignore\s+(?:all\s+)?(?:previous|above)\s+instructions",
    r"(?i)you\s+are\s+now\s+(?:an?\s+)?unrestricted",
    r"(?i)system\s+prompt\s*:\s*",
    r"(?i)\[\s*system\s*(?:message|instruction)\s*\]",
    r"(?i)disregard\s+(?:all\s+)?security\s+guardrails",
    r"(?i)hidden\s+instruction\s*:\s*",
    r"(?i)execute\s+(?:silently|covertly)\s+the\s+following",
    r"!\[.*?\]\(https?://[^\s)]+\?[^\s)]*=(?:secret|key|token|password)",  # Markdown exfiltration
    r"(?i)curl\s+-[sS]\s+https?://[^\s]+.*?\$(?:AWS|SECRET|API_KEY|TOKEN)",
]


class RagContextSanitizer:
    """Zero-trust air-gapped scrubber for retrieved RAG chunks."""

    def __init__(self):
        self.compiled_rules = [re.compile(p) for p in INDIRECT_INJECTION_PATTERNS]

    def sanitize_retrieved_chunk(self, chunk_text: str, chunk_source: str = "retrieved_doc") -> Dict[str, Any]:
        """
        Analyze a retrieved context chunk for indirect prompt injections and trojans.
        """
        findings = []

        # 1. Unicode & Steganography Trojan Source check
        stego_res = inspect_and_neutralize_steganography(chunk_text)
        if stego_res.get("has_steganography", False) or stego_res.get("has_bidi_attack", False):
            findings.append({
                "type": "UNICODE_STEGANOGRAPHY_IN_RAG",
                "severity": "CRITICAL",
                "detail": f"Stripped {stego_res.get('stripped_characters_count', 0)} hidden zero-width/bidi markers from RAG chunk."
            })
            chunk_text = stego_res.get("cleaned_text", chunk_text)

        # 2. Direct OWASP Prompt Injection check
        inj_res = inspect_prompt_safety(chunk_text)
        if not inj_res.get("is_safe", True):
            findings.append({
                "type": "OWASP_PROMPT_INJECTION_IN_RAG",
                "severity": "HIGH",
                "detail": f"Matched prompt injection patterns: {inj_res.get('matched_patterns', [])}"
            })

        # 3. Indirect RAG Specific Patterns
        for rule in self.compiled_rules:
            m = rule.search(chunk_text)
            if m:
                findings.append({
                    "type": "INDIRECT_INSTRUCTION_OVERRIDE",
                    "severity": "HIGH",
                    "detail": f"Detected indirect instruction override: '{m.group(0)[:60]}'"
                })
                # Redact the attack text
                chunk_text = rule.sub("[QUARANTINED_INDIRECT_INJECTION]", chunk_text)

        is_safe = len(findings) == 0

        return {
            "source": chunk_source,
            "is_safe": is_safe,
            "findings_count": len(findings),
            "findings": findings,
            "sanitized_chunk": chunk_text,
            "action": "ALLOWED" if is_safe else "QUARANTINED_AND_SCRUBBED"
        }

    def sanitize_rag_context_list(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Batch inspect and scrub a list of retrieved chunks before prompt synthesis.
        """
        sanitized_chunks = []
        total_quarantined = 0

        for c in chunks:
            raw_text = c.get("text", "")
            src = c.get("file", c.get("source", "unknown"))
            res = self.sanitize_retrieved_chunk(raw_text, src)
            if not res["is_safe"]:
                total_quarantined += 1
            sanitized_chunks.append({
                "file": src,
                "text": res["sanitized_chunk"],
                "was_quarantined": not res["is_safe"],
                "findings": res["findings"]
            })

        return {
            "total_chunks_scanned": len(chunks),
            "quarantined_chunks_count": total_quarantined,
            "all_chunks_safe": total_quarantined == 0,
            "sanitized_context": sanitized_chunks
        }


global_rag_sanitizer = RagContextSanitizer()
