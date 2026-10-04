"""
KAVACH Model Context Protocol (MCP) JSON-RPC 2.0 Server.
Exposes security governance tools to Cursor IDE, Claude Desktop, and VS Code.
Protocol Specification: MCP 2024-11-05.
"""

import json
import sys
from typing import Dict, Any, List

try:
    from .token_vault import TokenVault
    from .ast_firewall import inspect_code_dependencies
    from .policy_engine import PolicyEngine
    from .impact_analyzer import ASTImpactAnalyzer
    from .self_healer import ReActSelfHealer
    from .sbom_generator import generate_cyclonedx_sbom
except (ImportError, ValueError):
    from token_vault import TokenVault
    from ast_firewall import inspect_code_dependencies
    from policy_engine import PolicyEngine
    from impact_analyzer import ASTImpactAnalyzer
    from self_healer import ReActSelfHealer
    from sbom_generator import generate_cyclonedx_sbom

MCP_TOOLS = [
    {
        "name": "kavach_scan_security",
        "description": "Scans text or code for multilingual PII, secret credentials (AWS/GitHub), and destructive injection commands.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Prompt or code string to scan"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "kavach_verify_packages",
        "description": "Statically inspects Python imports using AST to intercept AI package hallucinations and PyPI slopsquatting attacks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python source code"}
            },
            "required": ["code"]
        }
    },
    {
        "name": "kavach_blast_radius",
        "description": "Calculates downstream caller-callee regression impact and blast radius using AST dependency analysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string", "description": "Target file name"},
                "function_name": {"type": "string", "description": "Modified function name"}
            },
            "required": ["file_name"]
        }
    },
    {
        "name": "kavach_self_heal",
        "description": "Autonomously tests and repairs failing Python code using closed-loop ReAct reflection.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to test and repair"},
                "assertions": {"type": "string", "description": "Unittest assertions"}
            },
            "required": ["code"]
        }
    },
    {
        "name": "kavach_generate_sbom",
        "description": "Generates a CycloneDX v1.5 Software Bill of Materials with SLSA Level 3 cryptographic hashes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "artifact_name": {"type": "string", "description": "Target file name"},
                "code": {"type": "string", "description": "Patch source code"},
                "packages": {"type": "array", "items": {"type": "string"}, "description": "Verified dependency list"}
            },
            "required": ["artifact_name", "code"]
        }
    }
]

def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Processes an incoming JSON-RPC 2.0 MCP request."""
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "kavach-governance-mcp-server", "version": "1.0.0"},
                "capabilities": {"tools": {}}
            }
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": MCP_TOOLS}
        }

    if method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "kavach_scan_security":
            text = args.get("text", "")
            vault = TokenVault()
            sanitized, findings, _ = vault.scan_and_redact(text)
            policy = PolicyEngine().evaluate_prompt(text, findings)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "verdict": policy["verdict"],
                    "risk_score": policy["risk_score"],
                    "redacted_text": sanitized,
                    "findings": findings,
                    "reasons": policy["blocked_reasons"] or policy["review_reasons"]
                }
            }

        elif tool_name == "kavach_verify_packages":
            code = args.get("code", "")
            res = inspect_code_dependencies(code)
            return {"jsonrpc": "2.0", "id": req_id, "result": res}

        elif tool_name == "kavach_blast_radius":
            analyzer = ASTImpactAnalyzer()
            file_name = args.get("file_name", "main.py")
            func_name = args.get("function_name")
            res = analyzer.compute_blast_radius(file_name, func_name)
            return {"jsonrpc": "2.0", "id": req_id, "result": res}

        elif tool_name == "kavach_self_heal":
            code = args.get("code", "")
            assertions = args.get("assertions", "")
            healer = ReActSelfHealer()
            res = healer.autonomous_repair(code, assertions)
            return {"jsonrpc": "2.0", "id": req_id, "result": res}

        elif tool_name == "kavach_generate_sbom":
            name = args.get("artifact_name", "patch.py")
            code = args.get("code", "")
            pkgs = args.get("packages", [])
            sbom = generate_cyclonedx_sbom(name, code, pkgs)
            return {"jsonrpc": "2.0", "id": req_id, "result": sbom}

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method or tool not found: {method}"}
    }

if __name__ == "__main__":
    # Test JSON-RPC list
    print("Testing MCP tools/list:")
    req = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    resp = handle_mcp_request(req)
    print(f"Registered {len(resp['result']['tools'])} MCP tools successfully.")
    for t in resp['result']['tools']:
        print(f" - Tool: {t['name']}")
