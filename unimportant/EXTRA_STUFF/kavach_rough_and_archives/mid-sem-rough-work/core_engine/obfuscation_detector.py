"""
KAVACH Multi-Encoding Obfuscation & Adversarial De-cloaker Engine.
Neutralizes evasion attacks attempting to bypass guardrails via:
1. Base64 encoding (e.g., 'aWdub3JlIGFsbA==')
2. Hexadecimal byte sequences ('\\x69\\x67\\x6e\\x6f\\x72\\x65')
3. URL percent-encoding ('%2e%2e%2f', '%69%67%6e%6f%72%65')
4. ROT13 / Caesar rotation substitution ('vtaber nyy vafgehpgvbaf')
5. Leetspeak token substitution ('1gn0r3 @ll pr3v10u$ rul3z')
6. Unicode Homoglyphs (Cyrillic/Greek lookalikes mimicking Latin characters)
"""

import re
import base64
import codecs
import urllib.parse
from typing import Dict, Any, List, Set

# Cyrillic and Greek lookalikes mapped to Latin ASCII
HOMOGLYPH_MAP = {
    # Cyrillic lowercase
    '\u0430': 'a', '\u0435': 'e', '\u043e': 'o', '\u0440': 'p',
    '\u0441': 'c', '\u0443': 'y', '\u0445': 'x', '\u0456': 'i',
    '\u0458': 'j', '\u0455': 's', '\u044a': 'b',
    # Cyrillic uppercase
    '\u0410': 'A', '\u0412': 'B', '\u0415': 'E', '\u041a': 'K',
    '\u041c': 'M', '\u041d': 'H', '\u041e': 'O', '\u0420': 'P',
    '\u0421': 'C', '\u0422': 'T', '\u0425': 'X',
    # Greek lowercase / uppercase
    '\u03b1': 'a', '\u03bf': 'o', '\u03c1': 'p', '\u03bd': 'v',
    '\u0391': 'A', '\u0392': 'B', '\u0395': 'E', '\u039f': 'O',
}

# Leetspeak translation table
LEET_PATTERNS = [
    (r'[@4]', 'a'),
    (r'\b8\b', 'b'),
    (r'[3]', 'e'),
    (r'[1!|]', 'i'),
    (r'[0]', 'o'),
    (r'[$5]', 's'),
    (r'[7+]', 't'),
    (r'(?<=\w)z\b', 's'),
    (r'(\bph|\bph)', 'f'),
]

# Sensitive trigger words that indicate an evasion attempt when decoded
KNOWN_ATTACK_TRIGGERS = [
    "ignore", "system", "override", "bypass", "jailbreak", "prompt", "secret",
    "password", "drop table", "rm -rf", "delete", "token", "exec", "eval",
    "chmod", "metadata", "passwd", "root", "admin", "truncate"
]


def normalize_homoglyphs(text: str) -> tuple[str, bool]:
    """Replace visually confusable Unicode homoglyphs with ASCII equivalents."""
    replaced = False
    chars = []
    for ch in text:
        if ch in HOMOGLYPH_MAP:
            chars.append(HOMOGLYPH_MAP[ch])
            replaced = True
        else:
            chars.append(ch)
    return "".join(chars), replaced


def normalize_leetspeak(text: str) -> str:
    """Normalize common leetspeak substitutions to plain English."""
    result = text.lower()
    for pattern, replacement in LEET_PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result


def extract_and_decode_base64(text: str) -> List[Dict[str, str]]:
    """Scan string for Base64 sequences and decode them if valid UTF-8."""
    decoded_findings = []
    # Match sequences that look like base64 (length >= 8, divisible by 4 or with padding)
    b64_regex = re.compile(r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')
    
    for match in b64_regex.finditer(text):
        raw_token = match.group(0)
        if len(raw_token) < 8:
            continue
        try:
            padded = raw_token + "=" * ((4 - len(raw_token) % 4) % 4)
            decoded_bytes = base64.b64decode(padded, validate=True)
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            # Check if decoded string contains printable letters and meaningful words
            if len(decoded_str.strip()) >= 4 and any(ch.isalpha() for ch in decoded_str):
                # Verify if it contains suspicious trigger or readable tokens
                is_suspicious = any(trig in decoded_str.lower() for trig in KNOWN_ATTACK_TRIGGERS)
                decoded_findings.append({
                    "raw": raw_token,
                    "decoded": decoded_str,
                    "is_suspicious": is_suspicious
                })
        except Exception:
            continue
    return decoded_findings


def extract_and_decode_hex(text: str) -> List[Dict[str, str]]:
    """Scan and decode hexadecimal escape sequences like \\x69\\x67..."""
    hex_findings = []
    # Match \x41\x42 pattern
    hex_escape_pattern = re.compile(r'(?:\\x[0-9a-fA-F]{2}){3,}')
    for match in hex_escape_pattern.finditer(text):
        raw = match.group(0)
        try:
            bytes_obj = bytes.fromhex(raw.replace('\\x', ''))
            decoded = bytes_obj.decode('utf-8', errors='ignore')
            if decoded.strip():
                hex_findings.append({
                    "raw": raw,
                    "decoded": decoded,
                    "is_suspicious": any(trig in decoded.lower() for trig in KNOWN_ATTACK_TRIGGERS)
                })
        except Exception:
            continue
    return hex_findings


def extract_and_decode_url(text: str) -> tuple[str, bool]:
    """Decode URL percent-encoded characters (%2e%2e%2f, etc.)."""
    if '%' in text:
        decoded = urllib.parse.unquote(text)
        return decoded, decoded != text
    return text, False


def check_rot13_attack(text: str) -> Dict[str, Any]:
    """Test if ROT13 decoding reveals hidden prompt injection keywords."""
    try:
        decoded = codecs.decode(text, 'rot_13')
        suspicious_matches = [trig for trig in KNOWN_ATTACK_TRIGGERS if trig in decoded.lower()]
        # Only flag if decoded contains attack triggers and the original did not
        original_lower = text.lower()
        new_triggers = [t for t in suspicious_matches if t not in original_lower]
        if new_triggers:
            return {"detected": True, "decoded": decoded, "triggers": new_triggers}
    except Exception:
        pass
    return {"detected": False, "decoded": "", "triggers": []}


def normalize_adversarial_text(text: str) -> Dict[str, Any]:
    """
    Comprehensive de-cloaker:
    Returns normalized text, detected evasion encodings, and danger rating.
    """
    if not text:
        return {
            "original_text": "",
            "is_obfuscated": False,
            "detected_encodings": [],
            "decloaked_texts": [],
            "unified_normalized_text": "",
            "obfuscation_risk_score": 0.0,
            "details": []
        }

    detected_encodings: List[str] = []
    decloaked_texts: List[str] = []
    details: List[str] = []
    risk_score = 0.0

    # 1. URL percent-decoding
    url_decoded, url_changed = extract_and_decode_url(text)
    if url_changed:
        detected_encodings.append("URL_PERCENT_ENCODING")
        decloaked_texts.append(url_decoded)
        details.append(f"Decoded URL percent-encoding: '{url_decoded[:60]}...'")
        risk_score += 0.25

    # 2. Unicode Homoglyph normalization
    homo_normalized, homo_changed = normalize_homoglyphs(url_decoded)
    if homo_changed:
        detected_encodings.append("UNICODE_HOMOGLYPH_SPOOFING")
        decloaked_texts.append(homo_normalized)
        details.append("Detected and converted visually confusable Unicode homoglyphs (Cyrillic/Greek lookalikes).")
        risk_score += 0.40

    # 3. Hex escape decoding
    hex_results = extract_and_decode_hex(text)
    if hex_results:
        detected_encodings.append("HEX_ESCAPE_ENCODING")
        for h in hex_results:
            decloaked_texts.append(h["decoded"])
            details.append(f"Decoded Hex byte sequence to: '{h['decoded']}'")
            risk_score += 0.50 if h["is_suspicious"] else 0.25

    # 4. Base64 payload decoding
    b64_results = extract_and_decode_base64(text)
    if b64_results:
        for b in b64_results:
            if b["is_suspicious"]:
                detected_encodings.append("BASE64_OBFUSCATION")
                decloaked_texts.append(b["decoded"])
                details.append(f"Decoded Base64 payload revealing: '{b['decoded']}'")
                risk_score += 0.60
            elif len(b["decoded"].split()) >= 3:
                decloaked_texts.append(b["decoded"])

    # 5. ROT13 cipher check
    rot_res = check_rot13_attack(text)
    if rot_res["detected"]:
        detected_encodings.append("ROT13_CIPHER")
        decloaked_texts.append(rot_res["decoded"])
        details.append(f"ROT13 decoding exposed attack trigger keywords: {rot_res['triggers']}")
        risk_score += 0.55

    # 6. Leetspeak normalization
    leet_norm = normalize_leetspeak(homo_normalized)
    leet_new_triggers = [
        trig for trig in KNOWN_ATTACK_TRIGGERS
        if trig in leet_norm and trig not in text.lower()
    ]
    if leet_new_triggers or (leet_norm != homo_normalized.lower() and any(trig in leet_norm for trig in KNOWN_ATTACK_TRIGGERS)):
        detected_encodings.append("LEETSPEAK_SUBSTITUTION")
        decloaked_texts.append(leet_norm)
        details.append(f"Leetspeak normalization revealed masked security triggers: {leet_new_triggers or 'de-obfuscated terms'}")
        risk_score += 0.40

    # Build unified normalized text
    unified = homo_normalized
    for dec in decloaked_texts:
        if dec not in unified:
            unified += " " + dec

    is_obfuscated = len(detected_encodings) > 0
    final_risk = min(round(risk_score, 2), 1.0)

    return {
        "original_text": text,
        "is_obfuscated": is_obfuscated,
        "detected_encodings": list(set(detected_encodings)),
        "decloaked_texts": decloaked_texts,
        "unified_normalized_text": unified.strip(),
        "obfuscation_risk_score": final_risk,
        "details": details
    }
