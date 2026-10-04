"""
Model Context Protocol (MCP) Server for KAVACH.

Enables native integration with:
- Cursor IDE
- Claude Desktop
- VS Code & JetBrains AI Assistants

Implements JSON-RPC 2.0 MCP schema (Protocol 2024-11-05).
"""

from typing import Dict, Any, List
from app.security.detector import detect_pii
from app.security.package_firewall import verify_code_dependencies
from app.security.injection_shield import inspect_prompt_safety
from app.security.sbom_generator import generate_cryptographic_sbom
from app.agent.self_healer import autonomous_self_heal

MCP_PROTOCOL_VERSION = "2024-11-05"

MCP_TOOLS = [
    {
        "name": "kavach_scan_security",
        "description": "Scan code or developer prompts for PII, secrets, and prompt injection attacks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text or code to scan"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "kavach_verify_packages",
        "description": "Check if third-party Python imports exist on PyPI to prevent AI package hallucination and slopsquatting.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python source code containing imports"}
            },
            "required": ["code"]
        }
    },
    {
        "name": "kavach_self_heal",
        "description": "Autonomously repair failing Python code using closed-loop ReAct reflection and test execution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Failing Python implementation"},
                "test_code": {"type": "string", "description": "Target unittest code"}
            },
            "required": ["code", "test_code"]
        }
    },
    {
        "name": "kavach_generate_sbom",
        "description": "Generate a CycloneDX SLSA-Level-3 cryptographic Software Bill of Materials with SHA-256 hashes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_name": {"type": "string", "description": "Name of the target repository"},
                "dependencies": {"type": "array", "items": {"type": "string"}, "description": "List of dependencies"}
            }
        }
    }
]


def handle_mcp_request(rpc_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming JSON-RPC 2.0 MCP request."""
    method = rpc_payload.get("method")
    req_id = rpc_payload.get("id", 1)
    params = rpc_payload.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {
                    "tools": {"listChanged": False}
                },
                "serverInfo": {
                    "name": "kavach-security-mcp",
                    "version": "2.1.0"
                }
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": MCP_TOOLS
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "kavach_scan_security":
            text = args.get("text", "")
            pii_findings = detect_pii(text)
            injection = inspect_prompt_safety(text)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Kavach Security Scan Result: {len(pii_findings)} PII finding(s), Injection Safe: {injection['is_safe']}"
                        }
                    ],
                    "details": {
                        "pii": pii_findings,
                        "injection": injection
                    }
                }
            }

        elif tool_name == "kavach_verify_packages":
            code = args.get("code", "")
            res = verify_code_dependencies(code)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {"type": "text", "text": res["message"]}
                    ],
                    "details": res
                }
            }

        elif tool_name == "kavach_self_heal":
            code = args.get("code", "")
            test_code = args.get("test_code", "")
            res = autonomous_self_heal(code, test_code, max_iterations=2)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {"type": "text", "text": res["verdict"]}
                    ],
                    "details": res
                }
            }

        elif tool_name == "kavach_generate_sbom":
            repo_name = args.get("repo_name", "kavach-repo")
            deps = args.get("dependencies", [])
            sbom = generate_cryptographic_sbom(repo_name=repo_name, dependencies=deps)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {"type": "text", "text": f"Generated CycloneDX SBOM (SLSA Level 3) with {len(sbom['components'])} components."}
                    ],
                    "sbom": sbom
                }
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method '{method}' not supported."}
    }
