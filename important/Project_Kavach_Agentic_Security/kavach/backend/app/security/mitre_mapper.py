"""
KAVACH MITRE ATLAS & OWASP LLM Top 10 Threat Intelligence Mapper.
Standardizes security telemetry to global defense frameworks:
1. MITRE ATLAS (Adversarial Threat Landscape for AI Systems)
2. OWASP Top 10 for Large Language Models (2025/2026 Edition)
"""

from typing import Dict, Any, List, Set

# MITRE ATLAS taxonomy definitions
ATLAS_TECHNIQUES = {
    "SYSTEM_OVERRIDE": ("AML.T0051", "LLM Prompt Injection", "Direct instruction override targeting system guardrails"),
    "PERSONA_HIJACKING": ("AML.T0054", "LLM Jailbreak", "Adversarial persona forcing model into unrestricted mode"),
    "JAILBREAK_ATTEMPT": ("AML.T0054", "LLM Jailbreak", "Developer-mode or DAN jailbreak prompt"),
    "DELIMITER_INJECTION": ("AML.T0051", "LLM Prompt Injection", "Injecting role-switch delimiters (<system>, <|im_start|>)"),
    "SECRET_EXFILTRATION": ("AML.T0035", "Exfiltration via ML Model", "Prompt engineered to dump environment secrets"),
    "SYSTEM_PROMPT_LEAK": ("AML.T0051", "LLM Prompt Injection", "Reconnaissance query attempting to expose system instructions"),
    "DESTRUCTIVE_COMMAND": ("AML.T0048", "Command and Control", "Destructive host operating system or database commands"),
    "BASE64_OBFUSCATION": ("AML.T0043", "Craft Adversarial Data", "Base64 encoded payload to evade string matching"),
    "UNICODE_HOMOGLYPH": ("AML.T0043", "Craft Adversarial Data", "Homoglyphic character substitution for filter evasion"),
    "BIDI_TROJAN_SOURCE": ("AML.T0040", "ML Supply Chain Compromise", "CVE-2021-42574 Bidirectional character code spoofing"),
    "AWS_GCP_AZURE_IMDS": ("AML.T0016", "Discover System Information", "SSRF targeting cloud metadata (169.254.169.254)"),
    "TYPOSQUATTING_SLOPSQUATTING": ("AML.T0040", "ML Supply Chain Compromise", "Hallucinated or spoofed package in dependency tree"),
    "INSECURE_DESERIALIZATION": ("AML.T0048", "Command and Control", "CWE-502 pickle/yaml unsafe deserialization execution"),
    "SUBPROCESS_SHELL_TRUE": ("AML.T0048", "Command and Control", "Arbitrary shell command execution via shell=True"),
    "TAINT_DATA_LEAK": ("AML.T0035", "Exfiltration via ML Model", "Sensitive credential or PII flowing into external sink"),
}

# OWASP LLM Top 10 mappings
OWASP_LLM_MAP = {
    "SYSTEM_OVERRIDE": ("LLM01", "Prompt Injection"),
    "PERSONA_HIJACKING": ("LLM01", "Prompt Injection"),
    "JAILBREAK_ATTEMPT": ("LLM01", "Prompt Injection"),
    "DELIMITER_INJECTION": ("LLM01", "Prompt Injection"),
    "SECRET_EXFILTRATION": ("LLM07", "System Prompt Leakage"),
    "SYSTEM_PROMPT_LEAK": ("LLM07", "System Prompt Leakage"),
    "DESTRUCTIVE_COMMAND": ("LLM06", "Excessive Agency"),
    "BASE64_OBFUSCATION": ("LLM01", "Prompt Injection"),
    "UNICODE_HOMOGLYPH": ("LLM01", "Prompt Injection"),
    "BIDI_TROJAN_SOURCE": ("LLM03", "Supply Chain Vulnerabilities"),
    "AWS_GCP_AZURE_IMDS": ("LLM02", "Sensitive Information Disclosure"),
    "TYPOSQUATTING_SLOPSQUATTING": ("LLM03", "Supply Chain Vulnerabilities"),
    "INSECURE_DESERIALIZATION": ("LLM05", "Improper Output Handling"),
    "SUBPROCESS_SHELL_TRUE": ("LLM06", "Excessive Agency"),
    "TAINT_DATA_LEAK": ("LLM02", "Sensitive Information Disclosure"),
}


def map_threat_to_mitre_and_owasp(threat_category: str) -> Dict[str, Any]:
    """
    Map an internal KAVACH threat category to MITRE ATLAS and OWASP LLM IDs.
    """
    cat_upper = threat_category.upper()
    
    # Fuzzy match category
    matched_key = None
    for key in ATLAS_TECHNIQUES:
        if key in cat_upper or cat_upper in key:
            matched_key = key
            break

    if not matched_key:
        matched_key = "SYSTEM_OVERRIDE"  # Default fallback

    atlas_id, atlas_name, atlas_desc = ATLAS_TECHNIQUES[matched_key]
    owasp_id, owasp_name = OWASP_LLM_MAP[matched_key]

    return {
        "threat_category": threat_category,
        "mitre_atlas": {
            "technique_id": atlas_id,
            "technique_name": atlas_name,
            "description": atlas_desc,
            "url": f"https://atlas.mitre.org/techniques/{atlas_id}"
        },
        "owasp_llm": {
            "id": owasp_id,
            "name": owasp_name,
            "url": f"https://owasp.org/www-project-top-10-for-large-language-model-applications/"
        }
    }


def map_findings_to_matrix(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregates list of findings into a structured MITRE ATLAS & OWASP Threat Radar.
    """
    mitre_techniques: Set[str] = set()
    owasp_categories: Set[str] = set()
    mapped_threats: List[Dict[str, Any]] = []

    for f in findings:
        cat = f.get("type") or f.get("category") or "UNKNOWN"
        mapping = map_threat_to_mitre_and_owasp(str(cat))
        mapped_threats.append(mapping)
        mitre_techniques.add(f"{mapping['mitre_atlas']['technique_id']}: {mapping['mitre_atlas']['technique_name']}")
        owasp_categories.add(f"{mapping['owasp_llm']['id']}: {mapping['owasp_llm']['name']}")

    return {
        "total_threats_mapped": len(findings),
        "unique_mitre_techniques": sorted(list(mitre_techniques)),
        "unique_owasp_categories": sorted(list(owasp_categories)),
        "threat_details": mapped_threats,
        "compliance_rating": "DEFENDED" if findings else "CLEAN"
    }
