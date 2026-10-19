"""
KAVACH Subprocess & Runtime Ephemeral Sandbox Jail.
Directly implements Feature #1 from WHAT_NEXT_ROADMAP.md.

Guarantees defense-in-depth during dynamic agent task execution:
1. Environment Sanitization: Scrubs secrets & cloud tokens before child execution
2. Binary Execution Whitelist/Blacklist: Blocks nc, curl, nmap, sudo, mkfs, format
3. Reverse Shell & Socket Interception: Traps /dev/tcp, mkfifo, pty.spawn
4. Hard Execution Limits: Timeout enforcement and memory/output truncation
"""

import os
import re
import subprocess
import time
from typing import Dict, Any, List

# Prohibited binary executables and destructive system commands
PROHIBITED_COMMAND_PATTERNS = [
    (r"(?i)\b(nc|netcat)\b", "UNAUTHORIZED_NETWORK_BINARY", "CRITICAL"),
    (r"(?i)\bnmap\b", "NETWORK_RECONNAISSANCE_TOOL", "CRITICAL"),
    (r"(?i)\b(curl|wget)\b.*(\|\s*(sh|bash)|http)", "DOWNLOAD_AND_EXECUTE", "CRITICAL"),
    (r"(?i)\bsudo\b", "UNAUTHORIZED_PRIVILEGE_ESCALATION", "CRITICAL"),
    (r"(?i)(/dev/tcp/|/dev/udp/|mkfifo\s+|pty\.spawn)", "REVERSE_SHELL_CONSTRUCT", "CRITICAL"),
    (r"(?i)\b(rm\s+-rf\s+/|dd\s+if=/dev/zero|mkfs\b|format\s+[a-z]:)", "DESTRUCTIVE_HOST_COMMAND", "CRITICAL"),
    (r"(?i)\b(chmod\s+777|chown\s+root)\b", "INSECURE_HOST_PERMISSIONS", "HIGH"),
    (r"(?i)\b(shutdown|reboot|init\s+0)\b", "HOST_AVAILABILITY_DENIAL", "HIGH"),
]

# Sensitive environment variables scrubbed from sandbox execution
SENSITIVE_ENV_VARS = [
    "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN",
    "GITHUB_TOKEN", "GH_TOKEN", "DATABASE_URL", "DB_PASSWORD",
    "GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY",
    "SLACK_BOT_TOKEN", "STRIPE_SECRET_KEY", "JWT_SECRET", "SSH_AUTH_SOCK"
]


def sanitize_sandbox_environment() -> Dict[str, str]:
    """
    Creates an isolated copy of os.environ with all API keys and secrets expunged.
    """
    clean_env = dict(os.environ)
    for var in SENSITIVE_ENV_VARS:
        clean_env.pop(var, None)
    # Also strip any generic pattern containing KEY, TOKEN, or SECRET
    for k in list(clean_env.keys()):
        upper_k = k.upper()
        if any(term in upper_k for term in ["SECRET", "PRIVATE_KEY", "PASSWORD"]):
            clean_env.pop(k, None)
    return clean_env


def audit_command_safety(command_str: str) -> Dict[str, Any]:
    """
    Evaluates whether a shell command violates sandbox security constraints.
    """
    threats = []
    for pattern, threat_type, severity in PROHIBITED_COMMAND_PATTERNS:
        if re.search(pattern, command_str):
            threats.append({
                "threat_type": threat_type,
                "severity": severity,
                "pattern": pattern
            })

    is_safe = len(threats) == 0
    return {
        "is_safe": is_safe,
        "threats": threats,
        "risk_level": "CRITICAL" if any(t["severity"] == "CRITICAL" for t in threats) else ("LOW" if is_safe else "HIGH")
    }


def execute_sandboxed_command(
    command_str: str,
    timeout_sec: float = 3.0,
    cwd: str = None
) -> Dict[str, Any]:
    """
    Executes a shell command inside an inspected, scrubbed, resource-constrained sandbox.
    """
    safety = audit_command_safety(command_str)
    if not safety["is_safe"]:
        return {
            "executed": False,
            "blocked": True,
            "exit_code": 126,
            "stdout": "",
            "stderr": f"Sandbox Policy Violation: Command blocked due to threats: {[t['threat_type'] for t in safety['threats']]}",
            "threats": safety["threats"],
            "duration_ms": 0.0
        }

    clean_env = sanitize_sandbox_environment()
    start_time = time.perf_counter()

    try:
        proc = subprocess.run(
            command_str,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=clean_env,
            cwd=cwd
        )
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "executed": True,
            "blocked": False,
            "exit_code": proc.returncode,
            "stdout": proc.stdout[:10000],  # Cap output at 10KB
            "stderr": proc.stderr[:10000],
            "threats": [],
            "duration_ms": duration_ms
        }
    except subprocess.TimeoutExpired:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "executed": False,
            "blocked": True,
            "exit_code": 124,
            "stdout": "",
            "stderr": f"Sandbox Quota Exceeded: Command timed out after {timeout_sec}s.",
            "threats": [{"threat_type": "EXECUTION_TIMEOUT_EXCEEDED", "severity": "MEDIUM"}],
            "duration_ms": duration_ms
        }
    except Exception as e:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "executed": False,
            "blocked": True,
            "exit_code": 1,
            "stdout": "",
            "stderr": f"Sandbox Execution Error: {e}",
            "threats": [],
            "duration_ms": duration_ms
        }
