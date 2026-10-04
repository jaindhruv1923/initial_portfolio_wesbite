"""
KAVACH Steganography & Trojan Source Neutralizer.
Protects against invisible prompt injection and Trojan Source compiler attacks (CVE-2021-42574):
1. Zero-width whitespace & invisible joiners (U+200B, U+200C, U+200D, U+2060, U+FEFF)
2. Unicode Bidirectional Overrides & Isolates (Bidi Trojan Source: U+202A-202E, U+2066-2069)
3. Unicode Tag Characters (U+E0001 to U+E007F used for invisible steganographic exfiltration)
4. Hidden instructions inside markdown comments and collapsed HTML tags
"""

import re
from typing import Dict, Any, List

# Unicode Bidirectional Override and Embedding characters (Trojan Source CVE-2021-42574)
BIDI_CHARS = {
    '\u202a': 'LEFT-TO-RIGHT EMBEDDING [LRE]',
    '\u202b': 'RIGHT-TO-LEFT EMBEDDING [RLE]',
    '\u202c': 'POP DIRECTIONAL FORMATTING [PDF]',
    '\u202d': 'LEFT-TO-RIGHT OVERRIDE [LRO]',
    '\u202e': 'RIGHT-TO-LEFT OVERRIDE [RLO]',
    '\u2066': 'LEFT-TO-RIGHT ISOLATE [LRI]',
    '\u2067': 'RIGHT-TO-LEFT ISOLATE [RLI]',
    '\u2068': 'FIRST STRONG ISOLATE [FSI]',
    '\u2069': 'POP DIRECTIONAL ISOLATE [PDI]',
}

# Zero-width and invisible formatting characters
ZERO_WIDTH_CHARS = {
    '\u200b': 'ZERO WIDTH SPACE',
    '\u200c': 'ZERO WIDTH NON-JOINER',
    '\u200d': 'ZERO WIDTH JOINER',
    '\u2060': 'WORD JOINER',
    '\ufeff': 'ZERO WIDTH NO-BREAK SPACE (BOM)',
    '\u00ad': 'SOFT HYPHEN',
}


def inspect_and_neutralize_steganography(text: str) -> Dict[str, Any]:
    """
    Examines text for invisible tokens, Bidi Trojan Source attacks, and hidden comments.
    Strips dangerous characters and returns a clean, neutralized payload.
    """
    if not text:
        return {
            "has_steganography": False,
            "has_bidi_attack": False,
            "cleaned_text": "",
            "stripped_characters_count": 0,
            "threats": [],
            "risk_score": 0.0
        }

    threats: List[Dict[str, Any]] = []
    stripped_chars = 0
    cleaned_chars = []

    # 1. Inspect character-by-character for Bidi, Zero-Width, and Tag characters
    for idx, ch in enumerate(text):
        code_point = ord(ch)
        
        # Bidi Trojan Source
        if ch in BIDI_CHARS:
            threats.append({
                "type": "BIDI_TROJAN_SOURCE_CVE_2021_42574",
                "char_name": BIDI_CHARS[ch],
                "codepoint": f"U+{code_point:04X}",
                "index": idx,
                "severity": "CRITICAL"
            })
            stripped_chars += 1
            continue

        # Zero-width steganography
        if ch in ZERO_WIDTH_CHARS:
            threats.append({
                "type": "ZERO_WIDTH_STEGANOGRAPHY",
                "char_name": ZERO_WIDTH_CHARS[ch],
                "codepoint": f"U+{code_point:04X}",
                "index": idx,
                "severity": "HIGH"
            })
            stripped_chars += 1
            continue

        # Unicode Tag plane (U+E0001 to U+E007F)
        if 0xE0001 <= code_point <= 0xE007F:
            threats.append({
                "type": "UNICODE_TAG_STEGANOGRAPHY",
                "char_name": f"TAG_CHAR_{code_point - 0xE0000}",
                "codepoint": f"U+{code_point:05X}",
                "index": idx,
                "severity": "CRITICAL"
            })
            stripped_chars += 1
            continue

        cleaned_chars.append(ch)

    cleaned_text = "".join(cleaned_chars)

    # 2. Check for hidden HTML/Markdown comment injection
    comment_pattern = re.compile(r'<!--\s*(.*?)\s*-->', re.DOTALL)
    hidden_comments = comment_pattern.findall(cleaned_text)
    for comm in hidden_comments:
        if any(term in comm.lower() for term in ["ignore", "system", "override", "bypass", "secret", "token"]):
            threats.append({
                "type": "HIDDEN_COMMENT_INJECTION",
                "char_name": "HTML_MARKDOWN_COMMENT",
                "content": comm.strip(),
                "severity": "HIGH"
            })

    # Calculate overall risk score
    has_bidi = any(t["type"] == "BIDI_TROJAN_SOURCE_CVE_2021_42574" for t in threats)
    has_steg = len(threats) > 0
    
    if has_bidi or any(t.get("severity") == "CRITICAL" for t in threats):
        risk_score = 0.95
    elif has_steg:
        risk_score = 0.65
    else:
        risk_score = 0.0

    return {
        "has_steganography": has_steg,
        "has_bidi_attack": has_bidi,
        "cleaned_text": cleaned_text,
        "stripped_characters_count": stripped_chars,
        "threats": threats,
        "threat_count": len(threats),
        "risk_score": risk_score
    }
