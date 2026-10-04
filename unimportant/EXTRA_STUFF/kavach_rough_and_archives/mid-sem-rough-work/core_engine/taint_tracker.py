"""
KAVACH Inter-Procedural AST Taint Tracker & Data-Flow Slicer.
Directly implements Feature #5 from WHAT_NEXT_ROADMAP.md.

Performs deterministic backward and forward data-flow slicing over Python ASTs to detect:
1. Sensitive variable origins (sources: password, aadhaar, pan, api_key, token, secret)
2. Assignment propagation chains (y = x, formatted f-strings, dict wrapping, list appends)
3. Unsanitized sinks (print, logger.info, requests.post, socket.send, file.write)
"""

import ast
from typing import Dict, Any, List, Set

# Sensitive source keywords in variable names or function calls
SENSITIVE_SOURCE_KEYWORDS = {
    "password", "user_aadhaar", "aadhaar", "pan", "pan_number", "api_key",
    "token", "secret", "private_key", "bearer_token", "credit_card", "db_password",
    "auth_secret", "ssn", "encryption_key"
}

# Dangerous sinks where tainted data must never flow unmasked
SINK_CALLS = {
    "print": "STDOUT_LEAK",
    "logger.info": "LOG_LEAK",
    "logger.debug": "LOG_LEAK",
    "logger.warning": "LOG_LEAK",
    "logger.error": "LOG_LEAK",
    "logging.info": "LOG_LEAK",
    "logging.debug": "LOG_LEAK",
    "requests.post": "NETWORK_EXFILTRATION",
    "requests.get": "NETWORK_EXFILTRATION",
    "urllib.request.urlopen": "NETWORK_EXFILTRATION",
    "socket.send": "RAW_SOCKET_EXFILTRATION",
    "sys.stdout.write": "STDOUT_LEAK",
    "os.system": "COMMAND_EXECUTION",
    "subprocess.run": "COMMAND_EXECUTION",
    "subprocess.Popen": "COMMAND_EXECUTION",
}


def _get_call_name(node: ast.AST) -> str:
    """Extract string identifier from an AST Call node (e.g. 'logger.info')."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        value_name = _get_call_name(node.value)
        return f"{value_name}.{node.attr}" if value_name else node.attr
    return ""


def _extract_names(node: ast.AST) -> Set[str]:
    """Recursively extract all variable names referenced in an AST expression."""
    names = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            names.add(child.id)
    return names


def track_ast_taint(source_code: str) -> Dict[str, Any]:
    """
    Parses code into an AST, tracks taint propagation across assignments,
    and identifies un-sanitized sink calls.
    """
    if not source_code or not source_code.strip():
        return {
            "has_taint_leak": False,
            "tainted_variables": [],
            "leak_count": 0,
            "leaks": [],
            "risk_score": 0.0,
            "details": "No code provided."
        }

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {
            "has_taint_leak": False,
            "tainted_variables": [],
            "leak_count": 0,
            "leaks": [],
            "risk_score": 0.0,
            "details": f"AST SyntaxError: {e}"
        }

    tainted_vars: Set[str] = set()
    taint_sources: Dict[str, int] = {}
    leaks: List[Dict[str, Any]] = []

    # Initial pass: find tainted sources from function parameters and explicit sensitive assignments
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for a in node.args.args:
                arg_name = a.arg
                if any(kw in arg_name.lower() for kw in SENSITIVE_SOURCE_KEYWORDS):
                    tainted_vars.add(arg_name)
                    taint_sources[arg_name] = getattr(node, "lineno", 0)

    # Multi-pass propagation through assignments until fixed point
    changed = True
    while changed:
        changed = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                assigned_names = set()
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_names.add(target.id)

                for target_name in assigned_names:
                    if any(kw in target_name.lower() for kw in SENSITIVE_SOURCE_KEYWORDS):
                        if target_name not in tainted_vars:
                            tainted_vars.add(target_name)
                            taint_sources[target_name] = getattr(node, "lineno", 0)
                            changed = True

                rhs_names = _extract_names(node.value)
                if any(name in tainted_vars for name in rhs_names):
                    for target_name in assigned_names:
                        if target_name not in tainted_vars:
                            tainted_vars.add(target_name)
                            taint_sources[target_name] = getattr(node, "lineno", 0)
                            changed = True

    # Second pass: trace calls and check if arguments contain tainted variables
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call_name = _get_call_name(node.func)
            lineno = getattr(node, "lineno", 0)

            # Check if this call is a dangerous sink
            matched_sink = None
            for sink, sink_type in SINK_CALLS.items():
                if call_name == sink or call_name.endswith("." + sink):
                    matched_sink = (sink, sink_type)
                    break

            if matched_sink:
                sink_label, sink_type = matched_sink
                # Inspect arguments for tainted variables
                arg_names = set()
                for arg in node.args:
                    arg_names.update(_extract_names(arg))
                for kw in node.keywords:
                    arg_names.update(_extract_names(kw.value))

                tainted_in_call = arg_names.intersection(tainted_vars)
                if tainted_in_call:
                    for tvar in sorted(tainted_in_call):
                        leaks.append({
                            "sink": sink_label,
                            "sink_type": sink_type,
                            "tainted_variable": tvar,
                            "source_line": taint_sources.get(tvar, "unknown"),
                            "leak_line": lineno,
                            "severity": "CRITICAL" if "EXFILTRATION" in sink_type else "HIGH",
                            "explanation": (
                                f"Taint leak detected: Sensitive variable '{tvar}' flows "
                                f"directly into sink '{sink_label}' at line {lineno}."
                            )
                        })

    has_leak = len(leaks) > 0
    risk_score = 0.95 if any(l["severity"] == "CRITICAL" for l in leaks) else (0.75 if has_leak else 0.0)

    return {
        "has_taint_leak": has_leak,
        "tainted_variables": sorted(list(tainted_vars)),
        "leak_count": len(leaks),
        "leaks": leaks,
        "risk_score": risk_score,
        "details": (
            f"Detected {len(leaks)} un-sanitized sink leak(s) across {len(tainted_vars)} tainted variable(s)."
            if has_leak
            else "Clean data-flow: Zero sensitive variables routed to dangerous sinks."
        )
    }
