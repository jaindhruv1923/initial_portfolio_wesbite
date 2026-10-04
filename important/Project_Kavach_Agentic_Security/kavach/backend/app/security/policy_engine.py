"""
Risk-adaptive, action-aware policy engine (Part 2 — addresses Limitation #4:
"Binary Decisions Need Risk-Adaptive and Action-Aware Policy").

Enhanced with Defense-in-Depth Cyber Security Capabilities:
- Steganography & Trojan Source (CVE-2021-42574) Detection
- Multi-Encoding Obfuscation De-cloaking (Base64, Hex, Leetspeak, Homoglyphs)
- SSRF & Cloud Metadata (AWS IMDS, GCP, Azure, RFC-1918) Interception
- Cryptographic Merkle Tree DPDP Audit Ledger Recording
- MITRE ATLAS & OWASP Top 10 for LLMs Threat Taxonomy Mapping
"""

from enum import Enum
from typing import Dict, Any, List

try:
    from app.security.steganography_shield import inspect_and_neutralize_steganography
    from app.security.obfuscation_detector import normalize_adversarial_text
    from app.security.ssrf_shield import inspect_ssrf_and_cloud_metadata
    from app.security.merkle_ledger import global_merkle_ledger
    from app.security.mitre_mapper import map_findings_to_matrix
    from app.security.injection_shield import inspect_prompt_safety
except (ImportError, ValueError):
    try:
        from .steganography_shield import inspect_and_neutralize_steganography
        from .obfuscation_detector import normalize_adversarial_text
        from .ssrf_shield import inspect_ssrf_and_cloud_metadata
        from .merkle_ledger import global_merkle_ledger
        from .mitre_mapper import map_findings_to_matrix
        from .injection_shield import inspect_prompt_safety
    except (ImportError, ValueError):
        from steganography_shield import inspect_and_neutralize_steganography
        from obfuscation_detector import normalize_adversarial_text
        from ssrf_shield import inspect_ssrf_and_cloud_metadata
        from merkle_ledger import global_merkle_ledger
        from mitre_mapper import map_findings_to_matrix
        from injection_shield import inspect_prompt_safety


class PolicyEngine:
    """Wrapper class for Policy Engine evaluation compatible with pipeline and MCP server."""
    def __init__(self):
        pass

    def evaluate_prompt(self, prompt: str, findings: list = None) -> dict:
        return evaluate_policy(prompt, findings)

    def evaluate(self, prompt: str, findings: list = None) -> dict:
        return evaluate_policy(prompt, findings)


class PolicyAction(str, Enum):
    ALLOW = "ALLOW"
    REDACT = "REDACT"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


# Action-risk classification: what is the developer asking the agent to DO.
HIGH_RISK_ACTION_KEYWORDS = [
    "delete", "drop table", "truncate", "remove all", "wipe", "destroy",
    "rm -rf", "format", "purge",
]
MEDIUM_RISK_ACTION_KEYWORDS = [
    "modify", "update", "change", "alter", "migrate", "deploy", "write to",
    "overwrite",
]
# Anything not matching either list defaults to LOW (e.g. "explain",
# "add a new endpoint", "show me").

SEVERITY_WEIGHTS = {"critical": 1.0, "high": 0.8, "medium": 0.5, "low": 0.2}
ACTION_WEIGHTS = {"high": 0.9, "medium": 0.5, "low": 0.1}


def classify_action_risk(request_text: str) -> str:
    """Classify the requested action's inherent risk: high/medium/low."""
    lower = request_text.lower()
    if any(kw in lower for kw in HIGH_RISK_ACTION_KEYWORDS):
        return "high"
    if any(kw in lower for kw in MEDIUM_RISK_ACTION_KEYWORDS):
        return "medium"
    return "low"


def compute_risk_score(findings: list[dict], action_risk: str) -> float:
    """
    Combine data-sensitivity risk and action risk into one score, 0.0-1.0.
    A high-severity finding on a low-risk action ("explain this PAN
    format") scores lower than the same finding on a high-risk action
    ("delete records matching this PAN") — this is the "action-aware"
    part the limitations document asks for.
    """
    if not findings:
        data_risk = 0.0
    else:
        # Use the single highest-severity finding as the data-risk signal —
        # one critical finding matters more than many low-severity ones.
        data_risk = max(SEVERITY_WEIGHTS.get(f.get("severity", "low"), 0.2) for f in findings)

    action_weight = ACTION_WEIGHTS.get(action_risk, 0.1)

    # Weighted combination: data sensitivity matters more than action risk
    # alone (a low-risk action on a critical secret is still dangerous),
    # but action risk amplifies it rather than being purely additive.
    combined = data_risk * (0.7 + 0.3 * action_weight)
    return round(min(combined, 1.0), 3)


def decide_policy_action(risk_score: float, findings: list[dict]) -> PolicyAction:
    """
    Map a risk score to a policy action. Thresholds are a starting,
    documented default.
    """
    has_credential = any(f.get("category") == "credential" for f in findings)
    has_critical_threat = any(
        f.get("category") in ["prompt_injection", "adversarial_evasion"] and f.get("severity") in ["critical", "high"]
        or f.get("severity") == "critical"
        for f in findings
    )

    if has_credential or has_critical_threat or risk_score >= 0.75:
        return PolicyAction.BLOCK
    if risk_score >= 0.45:
        return PolicyAction.REVIEW
    if risk_score >= 0.15:
        return PolicyAction.REDACT
    return PolicyAction.ALLOW


def evaluate_policy(request_text: str, findings: list[dict] = None) -> dict:
    """
    Full policy evaluation:
    1. Inspects Prompt Safety, Steganography, Obfuscation, and Cloud Metadata SSRF.
    2. Classifies action risk, combines with data risk.
    3. Commits event to immutable Merkle Audit Ledger.
    4. Attaches MITRE ATLAS and OWASP LLM taxonomy tags.
    """
    active_findings = list(findings) if findings else []

    # 0. Prompt Injection & Adversarial Prompt Shield
    prompt_res = inspect_prompt_safety(request_text)
    if prompt_res["threat_detected"]:
        for t in prompt_res["threats"]:
            active_findings.append({
                "category": "prompt_injection",
                "type": t["category"],
                "severity": t["severity"].lower(),
                "explanation": f"Prompt injection / jailbreak detected: {t['category']}"
            })

    # 1. Steganography & Trojan Source scan
    steg_res = inspect_and_neutralize_steganography(request_text)
    if steg_res["has_bidi_attack"]:
        active_findings.append({
            "category": "credential",
            "type": "BIDI_TROJAN_SOURCE",
            "severity": "critical",
            "explanation": "CVE-2021-42574 Bidirectional Trojan Source compiler evasion attempt."
        })
    elif steg_res["has_steganography"] and steg_res["risk_score"] >= 0.6:
        active_findings.append({
            "category": "adversarial_evasion",
            "type": "ZERO_WIDTH_STEGANOGRAPHY",
            "severity": "high",
            "explanation": "Steganographic zero-width character evasion attempt."
        })

    # 2. Multi-encoding obfuscation scan
    obf_res = normalize_adversarial_text(request_text)
    if obf_res["is_obfuscated"] and obf_res["obfuscation_risk_score"] >= 0.5:
        active_findings.append({
            "category": "adversarial_evasion",
            "type": "OBFUSCATED_PAYLOAD",
            "severity": "high",
            "explanation": f"De-cloaked obfuscation: {', '.join(obf_res['detected_encodings'])}"
        })

    # 3. SSRF & Cloud Metadata scan
    ssrf_res = inspect_ssrf_and_cloud_metadata(request_text)
    if ssrf_res["is_ssrf_threat"]:
        for t in ssrf_res["threats"]:
            active_findings.append({
                "category": "credential" if t["severity"] == "CRITICAL" else "cloud_ssrf",
                "type": t["type"],
                "severity": t["severity"].lower(),
                "explanation": t["detail"]
            })

    action_risk = classify_action_risk(request_text)
    risk_score = compute_risk_score(active_findings, action_risk)
    decision = decide_policy_action(risk_score, active_findings)

    # 4. Record event to Cryptographic Merkle Tree Ledger
    try:
        ledger_entry = global_merkle_ledger.record_event(
            event_type="POLICY_EVALUATION",
            actor="DEVELOPER_QUERY",
            verdict=decision.value,
            details={
                "request_snippet": request_text[:80],
                "action_risk": action_risk,
                "risk_score": risk_score,
                "findings_count": len(active_findings)
            }
        )
        merkle_root = ledger_entry["merkle_root"]
    except Exception:
        merkle_root = "UNAVAILABLE"

    # 5. Map to MITRE ATLAS & OWASP Top 10 for LLMs
    try:
        radar_matrix = map_findings_to_matrix(active_findings)
    except Exception:
        radar_matrix = {"unique_mitre_techniques": [], "unique_owasp_categories": []}

    explanation = _build_explanation(decision, action_risk, active_findings)

    return {
        "decision": decision.value,
        "action": decision.value,
        "verdict": decision.value,
        "risk_score": risk_score,
        "action_risk_classification": action_risk,
        "data_findings_count": len(active_findings),
        "highest_severity": max((f.get("severity", "low") for f in active_findings), default="none",
                                  key=lambda s: SEVERITY_WEIGHTS.get(s, 0)),
        "explanation": explanation,
        "steganography": steg_res,
        "obfuscation": obf_res,
        "ssrf": ssrf_res,
        "prompt_safety": prompt_res,
        "merkle_root": merkle_root,
        "mitre_atlas": radar_matrix.get("unique_mitre_techniques", []),
        "owasp_llm": radar_matrix.get("unique_owasp_categories", [])
    }


def _build_explanation(decision: PolicyAction, action_risk: str, findings: list[dict]) -> str:
    if decision == PolicyAction.ALLOW:
        return "No significant sensitive-data or high-risk-action signal detected."
    categories = sorted(set(f.get("category", "unknown") for f in findings))
    cat_str = ", ".join(categories) if categories else "none"
    return (
        f"Decision={decision.value} based on detected categories [{cat_str}] "
        f"combined with a '{action_risk}'-risk requested action."
    )
