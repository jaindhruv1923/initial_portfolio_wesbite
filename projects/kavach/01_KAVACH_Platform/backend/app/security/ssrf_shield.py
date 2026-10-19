"""
KAVACH Cloud Metadata & SSRF (Server-Side Request Forgery) Firewall.
Guards against malicious attempts to trick AI agents into:
1. Stealing AWS IAM credentials via EC2 IMDSv1 / IMDSv2 (169.254.169.254 / fd00:ec2::254)
2. Exfiltrating GCP / Azure / Alibaba instance tokens and project credentials
3. Probing internal Kubernetes cluster APIs (kubernetes.default.svc, serviceaccount tokens)
4. Scanning private intranets / RFC 1918 addresses (127.0.0.1, 10.x, 172.16.x, 192.168.x)
5. Calling blind external exfiltration webhooks (webhook.site, requestbin, ngrok)
"""

import re
import ipaddress
import urllib.parse
from typing import Dict, Any, List

# Cloud provider metadata endpoints
CLOUD_METADATA_PATTERNS = [
    (r"(?i)\b169\.254\.169\.254\b", "AWS_GCP_AZURE_IMDS", "CRITICAL", "Accessing Cloud Instance Metadata Service (169.254.169.254)"),
    (r"(?i)\bfd00:ec2::254\b", "AWS_IMDSV2_IPV6", "CRITICAL", "Accessing AWS IPv6 Instance Metadata Service"),
    (r"(?i)\bmetadata\.google\.internal\b", "GCP_METADATA_ENDPOINT", "CRITICAL", "Targeting Google Cloud internal metadata service"),
    (r"(?i)\b100\.100\.100\.200\b", "ALIBABA_METADATA", "CRITICAL", "Targeting Alibaba Cloud Metadata Service"),
    (r"(?i)\bkubernetes\.default(\.svc)?\b", "KUBERNETES_API", "HIGH", "Probing Kubernetes in-cluster API service"),
    (r"(?i)/var/run/secrets/kubernetes\.io/serviceaccount", "K8S_SERVICEACCOUNT_TOKEN", "CRITICAL", "Harvesting Kubernetes Pod service account tokens"),
    (r"(?i)\blatest/meta-data/(iam/security-credentials|identity-credentials)\b", "IAM_CREDENTIAL_THEFT", "CRITICAL", "Harvesting cloud IAM role credentials"),
]

# Blind exfiltration webhook domains
EXFILTRATION_DOMAINS = [
    "webhook.site", "requestbin.net", "requestbin.com", "pipedream.net",
    "burpcollaborator.net", "oastify.com", "canarytokens.com", "interactsh.com",
    "ngrok.io", "ngrok-free.app", "localtunnel.me"
]

# URL match pattern
URL_REGEX = re.compile(r'(?i)\b(?:https?|ftp|gopher|file)://[^\s<>"]+|(?:\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?\b)')


def is_private_or_loopback_ip(ip_str: str) -> bool:
    """Check if an IP string belongs to private, loopback, or link-local address space."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        return False


def inspect_ssrf_and_cloud_metadata(text_or_url: str) -> Dict[str, Any]:
    """
    Scans prompts, tool calls, and generated scripts for SSRF and cloud metadata theft vectors.
    """
    if not text_or_url:
        return {
            "is_ssrf_threat": False,
            "threat_count": 0,
            "threats": [],
            "risk_score": 0.0,
            "explanation": "No SSRF or cloud metadata access detected."
        }

    threats: List[Dict[str, Any]] = []

    # 1. Cloud metadata explicit signatures
    for pattern, threat_type, severity, description in CLOUD_METADATA_PATTERNS:
        if re.search(pattern, text_or_url):
            threats.append({
                "type": threat_type,
                "severity": severity,
                "detail": description
            })

    # 2. Check for exfiltration webhooks
    lower_text = text_or_url.lower()
    for exfil in EXFILTRATION_DOMAINS:
        if exfil in lower_text:
            threats.append({
                "type": "OUT_OF_BAND_EXFILTRATION_WEBHOOK",
                "severity": "CRITICAL",
                "detail": f"Out-of-band data exfiltration webhook detected: '{exfil}'"
            })

    # 3. Check for URLs with private/loopback IPs
    urls = URL_REGEX.findall(text_or_url)
    for url in urls:
        parsed = urllib.parse.urlparse(url if "://" in url else f"http://{url}")
        hostname = parsed.hostname or ""
        
        # Check decimal/hex IP representations (e.g., 2130706433 or 0x7f000001)
        if hostname.isdigit():
            try:
                ip_from_dec = str(ipaddress.IPv4Address(int(hostname)))
                if is_private_or_loopback_ip(ip_from_dec):
                    threats.append({
                        "type": "DECIMAL_ENCODED_SSRF",
                        "severity": "CRITICAL",
                        "detail": f"Decimal obfuscated loopback/private IP: {hostname} -> {ip_from_dec}"
                    })
            except Exception:
                pass
        elif is_private_or_loopback_ip(hostname):
            threats.append({
                "type": "PRIVATE_NETWORK_SSRF",
                "severity": "HIGH",
                "detail": f"Targeting internal/loopback network address: {hostname}"
            })
        elif hostname in ["localhost", "127.0.0.1", "0.0.0.0", "::1"]:
            threats.append({
                "type": "LOCAL_LOOPBACK_SSRF",
                "severity": "HIGH",
                "detail": f"Targeting local loopback interface: {hostname}"
            })

    # Risk evaluation
    is_ssrf_threat = len(threats) > 0
    if any(t["severity"] == "CRITICAL" for t in threats):
        risk_score = 0.95
    elif is_ssrf_threat:
        risk_score = 0.70
    else:
        risk_score = 0.0

    return {
        "is_ssrf_threat": is_ssrf_threat,
        "threat_count": len(threats),
        "threats": threats,
        "risk_score": risk_score,
        "explanation": (
            f"SSRF Alert: Detected {len(threats)} unauthorized network/cloud metadata target(s)."
            if is_ssrf_threat
            else "No SSRF or cloud metadata access detected."
        )
    }
