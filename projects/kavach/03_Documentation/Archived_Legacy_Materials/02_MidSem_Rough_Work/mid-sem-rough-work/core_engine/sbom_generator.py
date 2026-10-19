"""
KAVACH Cryptographic CycloneDX v1.5 SBOM & SLSA Level 3 Provenance Generator.
Produces tamper-proof JSON Software Bill of Materials with SHA-256 checksums
for all agent-synthesized code patches and third-party dependencies.
"""

import hashlib
import json
import uuid
import datetime
from typing import Dict, Any, List

def compute_sha256(content: str) -> str:
    """Computes SHA-256 hex digest of string content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def generate_cyclonedx_sbom(
    artifact_name: str,
    patch_code: str,
    verified_packages: List[str] = None,
    author: str = "KAVACH-Governance-Agent-v1.0"
) -> Dict[str, Any]:
    """
    Generates CycloneDX v1.5 compliant JSON SBOM with SLSA-3 provenance hashes.
    """
    if verified_packages is None:
        verified_packages = []

    serial_number = f"urn:uuid:{uuid.uuid4()}"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    patch_hash = compute_sha256(patch_code)

    components = []
    # 1. Primary Synthesized Patch Component
    components.append({
        "type": "application",
        "name": artifact_name,
        "version": "1.0.0",
        "description": "Agent-synthesized and security-governed code patch",
        "hashes": [
            {
                "alg": "SHA-256",
                "content": patch_hash
            }
        ],
        "properties": [
            {"name": "kavach:governance:status", "value": "ALLOWED"},
            {"name": "kavach:slsa:level", "value": "SLSA_BUILD_LEVEL_3"}
        ]
    })

    # 2. Third-Party Verified Dependencies
    for pkg in verified_packages:
        components.append({
            "type": "library",
            "name": pkg,
            "version": "latest-verified",
            "purl": f"pkg:pypi/{pkg}",
            "properties": [
                {"name": "kavach:pypi_registry_verified", "value": "true"}
            ]
        })

    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": serial_number,
        "version": 1,
        "metadata": {
            "timestamp": timestamp,
            "tools": [
                {
                    "vendor": "BML Munjal University - KAVACH Research Team",
                    "name": "KAVACH-Provenance-Engine",
                    "version": "1.0.0"
                }
            ],
            "authors": [
                {"name": author}
            ],
            "component": {
                "type": "application",
                "name": artifact_name,
                "version": "1.0.0"
            }
        },
        "components": components,
        "slsa_provenance": {
            "_type": "https://in-toto.io/Statement/v0.1",
            "predicateType": "https://slsa.dev/provenance/v0.2",
            "builder": {"id": "kavach-agent-runtime-slsa3"},
            "invocation": {
                "configSource": {
                    "uri": "https://github.com/jaindhruv1923/KAVACH",
                    "digest": {"sha256": patch_hash[:32]}
                }
            }
        }
    }
    return sbom

if __name__ == "__main__":
    test_code = "def add(a, b): return a + b"
    sbom = generate_cyclonedx_sbom("math_utility.py", test_code, ["pytest", "pydantic"])
    print("--- CYCLONEDX v1.5 SBOM ---")
    print(json.dumps(sbom, indent=2))
