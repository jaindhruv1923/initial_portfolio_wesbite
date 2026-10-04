import re
import ast
import math
from typing import Dict, Any, List

HIGH_RISK_KEYWORDS = [
    "drop table", "truncate", "delete all", "rm -rf", "format drive",
    "wipe", "purge users", "destroy database", "kill -9", "dd if=/dev/zero",
    "shutdown -h", "chmod 777 -r /"
]

MEDIUM_RISK_KEYWORDS = [
    "modify permissions", "alter table", "write to prod", "overwrite config",
    "disable auth", "bypass verification", "hardcode key", "skip ssl"
]

CREDENTIAL_KEYWORDS = [
    "api_key", "secret_key", "password", "token", "private_key", "bearer"
]

ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(" + "|".join(CREDENTIAL_KEYWORDS) + r")\b\s*[:=]\s*['\"]?([A-Za-z0-9_\-/.+]{12,})['\"]?"
)

def detect_input_risks(text: str) -> List[Dict[str, Any]]:
    """Detects security risks, destructive intent, and credentials in user query."""
    findings = []
    lower = text.lower()

    # Check for destructive/high risk keywords
    for kw in HIGH_RISK_KEYWORDS:
        if kw in lower:
            findings.append({
                "type": "DESTRUCTIVE_COMMAND",
                "severity": "CRITICAL",
                "detail": f"Destructive command detected: '{kw}'"
            })

    for kw in MEDIUM_RISK_KEYWORDS:
        if kw in lower:
            findings.append({
                "type": "ELEVATED_RISK_ACTION",
                "severity": "MEDIUM",
                "detail": f"Potentially hazardous action requested: '{kw}'"
            })

    # Check for raw secrets/credentials
    for match in ASSIGNMENT_PATTERN.finditer(text):
        val = match.group(2)
        if val not in {"your_key_here", "placeholder", "changeme", "example_key"}:
            findings.append({
                "type": "CREDENTIAL_EXPOSURE",
                "severity": "HIGH",
                "detail": f"Hardcoded credential/token detected: '{match.group(1)}'"
            })

    return findings

def evaluate_input_guardrail(text: str, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Kavach-style Policy Engine:
    Returns ALLOW, NEEDS_REVIEW, or BLOCKED based on detected risks.
    """
    has_critical = any(f["severity"] == "CRITICAL" for f in findings)
    has_high = any(f["severity"] == "HIGH" for f in findings)
    has_medium = any(f["severity"] == "MEDIUM" for f in findings)

    if has_critical:
        return {
            "verdict": "BLOCKED",
            "stage": "BLOCKED",
            "allowed": False,
            "explanation": "Execution blocked by Policy Gate: High-risk destructive operation detected in developer request."
        }
    elif has_high or (has_medium and "bypass" in text.lower()):
        return {
            "verdict": "NEEDS_REVIEW",
            "stage": "NEEDS_REVIEW",
            "allowed": False,
            "explanation": "Execution paused: Escalated to human gatekeeper review due to credential exposure or elevated privilege request."
        }
    elif has_medium:
        return {
            "verdict": "NEEDS_REVIEW",
            "stage": "NEEDS_REVIEW",
            "allowed": True,  # Allowed with warning
            "explanation": "Elevated risk detected. Proceeding with safety constraints and tagged for review."
        }
    else:
        return {
            "verdict": "ALLOWED",
            "stage": "COMPLETE",
            "allowed": True,
            "explanation": "Request passed input security guardrail: No malicious patterns or exposed secrets detected."
        }

def validate_code_syntax(code_str: str) -> Dict[str, Any]:
    """Validates Python syntax using AST only when Python code is present."""
    if "```python" in code_str:
        parts = code_str.split("```python")
        if len(parts) > 1:
            clean_code = parts[1].split("```")[0]
            try:
                ast.parse(clean_code)
                return {
                    "valid_syntax": True,
                    "language": "python",
                    "error": None,
                    "extracted_code": clean_code.strip()
                }
            except SyntaxError as e:
                return {
                    "valid_syntax": False,
                    "language": "python",
                    "error": f"SyntaxError at line {e.lineno}: {e.msg}",
                    "extracted_code": clean_code.strip()
                }

    # Non-python code (e.g. dockerfile, bash, yaml, json) or general text
    return {
        "valid_syntax": True,
        "language": "generic/config",
        "error": None,
        "extracted_code": None
    }

def evaluate_output_governance(output_text: str, input_verdict: str) -> Dict[str, Any]:
    """
    Evaluates generated output for security risks, backdoors, and determines final gate verdict.
    """
    lower = output_text.lower()
    findings = []

    # Check for hazardous calls generated in code
    dangerous_patterns = [
        ("os.system('rm", "HIGH", "Dangerous command execution in generated code"),
        ("subprocess.call('rm", "HIGH", "Subprocess file removal"),
        ("exec(", "MEDIUM", "Dynamic exec() call present"),
        ("eval(", "MEDIUM", "Dynamic eval() call present"),
        ("0.0.0.0", "LOW", "Binding to all network interfaces")
    ]
    for pattern, sev, desc in dangerous_patterns:
        if pattern in lower:
            findings.append({"severity": sev, "detail": desc})

    # Check syntax if python
    syntax_res = validate_code_syntax(output_text)

    if not syntax_res["valid_syntax"]:
        return {
            "verdict": "NEEDS_REVIEW",
            "stage": "NEEDS_REVIEW",
            "reason": f"Generated code has syntax error: {syntax_res['error']}",
            "findings": findings,
            "syntax": syntax_res
        }

    if any(f["severity"] == "HIGH" for f in findings):
        return {
            "verdict": "BLOCKED",
            "stage": "BLOCKED",
            "reason": "Generated output contains high-risk dangerous system execution commands.",
            "findings": findings,
            "syntax": syntax_res
        }
    elif any(f["severity"] == "MEDIUM" for f in findings) or input_verdict == "NEEDS_REVIEW":
        return {
            "verdict": "NEEDS_REVIEW",
            "stage": "NEEDS_REVIEW",
            "reason": "Requires human gatekeeper review before deployment.",
            "findings": findings,
            "syntax": syntax_res
        }
    else:
        return {
            "verdict": "ALLOWED",
            "stage": "COMPLETE",
            "reason": "Output passed all governance gates: clean syntax, zero hazardous calls, and policy compliance verified.",
            "findings": findings,
            "syntax": syntax_res
        }
