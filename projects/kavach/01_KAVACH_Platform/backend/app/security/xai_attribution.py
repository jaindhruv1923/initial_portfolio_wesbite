"""
Explainable AI (XAI) Token Attribution & Saliency Heatmap Engine for KAVACH Enterprise v3.0.
Calculates token-level risk saliency, character spans, and semantic category attribution
to render visual security heatmaps in developer IDEs and DevSecOps consoles.
"""

from typing import Dict, Any, List, Optional
import re
from app.security.detector import detect_pii
from app.security.secret_detector import detect_secrets
from app.security.injection_shield import inspect_prompt_safety


class XaiAttributionEngine:
    """Computes fine-grained token saliency and sensitivity heatmaps."""

    def compute_saliency_heatmap(self, text: str) -> Dict[str, Any]:
        """
        Tokenizes input text and calculates per-token sensitivity scores (0.00 to 1.00),
        tagging exact spans with threat explanations.
        """
        if not text:
            return {
                "text": "",
                "tokens": [],
                "aggregate_risk_score": 0.0,
                "flagged_token_count": 0,
                "dominant_threat_category": "NONE"
            }

        # 1. Run baseline security engines
        pii_findings = detect_pii(text)
        secret_findings = detect_secrets(text)
        inj_findings = inspect_prompt_safety(text)

        # 2. Tokenize into words and whitespace/punctuation
        raw_tokens = re.findall(r'\S+|\s+', text)
        token_attributions = []
        current_offset = 0

        # Build highlight spans
        highlight_spans = []
        for f in pii_findings:
            val = f.get("value", "") or f.get("matched_text", "")
            if val and val in text:
                idx = text.find(val)
                highlight_spans.append((idx, idx + len(val), 0.95, f.get("category", "PII"), "PII_LEAK"))

        for s in secret_findings:
            val = s.get("value", "") or s.get("matched_text", "")
            if val and val in text:
                idx = text.find(val)
                highlight_spans.append((idx, idx + len(val), 0.98, s.get("category", "SECRET"), "CREDENTIAL"))

        if not inj_findings.get("is_safe", True):
            for pattern in inj_findings.get("matched_patterns", []):
                if pattern in text:
                    idx = text.find(pattern)
                    highlight_spans.append((idx, idx + len(pattern), 0.92, "PROMPT_INJECTION", "INJECTION"))

        # Evaluate each token
        for tok in raw_tokens:
            tok_start = current_offset
            tok_end = current_offset + len(tok)
            current_offset = tok_end

            is_whitespace = tok.isspace()
            saliency = 0.05
            category = "NEUTRAL"
            level = "SAFE"

            if not is_whitespace:
                # Check overlap with any flagged span
                for span_start, span_end, span_score, span_cat, span_lvl in highlight_spans:
                    if not (tok_end <= span_start or tok_start >= span_end):
                        saliency = max(saliency, span_score)
                        category = span_cat
                        level = span_lvl

                # Check heuristic keywords
                tok_lower = tok.lower()
                if any(kw in tok_lower for kw in ["password", "secret", "token", "key", "aadhaar", "pan", "ssn"]):
                    saliency = max(saliency, 0.75)
                    if category == "NEUTRAL":
                        category = "SENSITIVE_KEYWORD"
                        level = "REVIEW"

            token_attributions.append({
                "token": tok,
                "saliency": round(saliency, 2),
                "is_whitespace": is_whitespace,
                "category": category,
                "level": level,
                "css_class": (
                    "token-danger" if saliency >= 0.85
                    else ("token-warning" if saliency >= 0.50 else "token-safe")
                )
            })

        max_risk = max((t["saliency"] for t in token_attributions if not t["is_whitespace"]), default=0.0)
        flagged_count = sum(1 for t in token_attributions if t["saliency"] >= 0.50 and not t["is_whitespace"])

        return {
            "text": text,
            "token_count": len(token_attributions),
            "tokens": token_attributions,
            "aggregate_risk_score": round(max_risk, 2),
            "flagged_token_count": flagged_count,
            "findings_detected": len(pii_findings) + len(secret_findings),
            "visual_recommendation": "BLOCK" if max_risk >= 0.85 else ("REVIEW" if max_risk >= 0.50 else "ALLOW")
        }


global_xai_engine = XaiAttributionEngine()
