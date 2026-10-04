"""
KAVACH CI/CD Pre-Merge Gatekeeper & Pull Request Diff Auditor.
Directly implements Feature #2 from WHAT_NEXT_ROADMAP.md.

Analyzes Git patch diffs before merge:
1. Extracts additions (+ lines) across code, configuration, and dependencies
2. Intercepts newly introduced hardcoded secrets and unmasked PII
3. Scans for hallucinated/slopsquatted packages and insecure sinks
4. Emits GitHub/GitLab PR review markdown comments with governance badges
5. Returns deterministic exit code (0 = PASS, 1 = BLOCK) for CI/CD pipelines
"""

import re
from typing import Dict, Any, List

try:
    from app.security.detector import detect_pii
    from app.security.secret_detector import detect_secrets
    from app.security.vulnerability_scanner import scan_code_vulnerabilities
    from app.security.polyglot_firewall import audit_polyglot_manifest_or_code
    from app.security.merkle_ledger import global_merkle_ledger
except (ImportError, ValueError):
    try:
        from .detector import detect_pii
        from .secret_detector import detect_secrets
        from .vulnerability_scanner import scan_code_vulnerabilities
        from .polyglot_firewall import audit_polyglot_manifest_or_code
        from .merkle_ledger import global_merkle_ledger
    except (ImportError, ValueError):
        from detector import detect_pii
        from secret_detector import detect_secrets
        from vulnerability_scanner import scan_code_vulnerabilities
        from polyglot_firewall import audit_polyglot_manifest_or_code
        from merkle_ledger import global_merkle_ledger


def parse_git_diff_additions(diff_text: str) -> Dict[str, str]:
    """
    Parses unified git diff and groups added lines by modified filename.
    """
    files_added_lines: Dict[str, List[str]] = {}
    current_file = "unknown_file"

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            files_added_lines[current_file] = []
        elif line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:]  # strip leading '+'
            if current_file in files_added_lines:
                files_added_lines[current_file].append(added_content)
            else:
                files_added_lines[current_file] = [added_content]

    return {f: "\n".join(lines) for f, lines in files_added_lines.items()}


def audit_git_patch_diff(diff_text: str, pr_number: int = 1) -> Dict[str, Any]:
    """
    Evaluates a Git patch diff against KAVACH deterministic pre-merge policies.
    """
    if not diff_text or not diff_text.strip():
        return {
            "verdict": "ALLOWED",
            "exit_code": 0,
            "blocked_reasons": [],
            "warnings": [],
            "files_analyzed": 0,
            "pr_comment_markdown": "### 🛡️ KAVACH CI/CD Gate: Clean Diff\nNo additions detected in pull request diff."
        }

    diff_map = parse_git_diff_additions(diff_text)
    blocked_reasons: List[str] = []
    warnings: List[str] = []
    findings_summary: List[Dict[str, Any]] = []

    for filename, added_code in diff_map.items():
        if not added_code.strip():
            continue

        # 1. PII & Secret Detection on new lines
        pii_res = detect_pii(added_code)
        secret_res = detect_secrets(added_code)

        for p in pii_res:
            warnings.append(f"[{filename}] PII exposed: {p.get('type')} ('{p.get('value')}')")
            findings_summary.append({"file": filename, "type": "PII", "detail": p.get("explanation")})

        for s in secret_res:
            blocked_reasons.append(f"[{filename}] Hardcoded Secret detected: {s.get('type')}")
            findings_summary.append({"file": filename, "type": "SECRET", "detail": s.get("explanation")})

        # 2. Package & Supply-chain firewall
        if filename.endswith((".py", "requirements.txt", "package.json", "go.mod")):
            firewall_res = audit_polyglot_manifest_or_code(added_code, filename)
            if not firewall_res["is_safe"]:
                for bp in firewall_res["blocked_packages"]:
                    blocked_reasons.append(f"[{filename}] Hazardous package: {bp['package']} ({bp['reason']})")
                    findings_summary.append({"file": filename, "type": "SUPPLY_CHAIN", "detail": bp['detail']})

        # 3. Code Vulnerabilities & Dangerous Sinks (Python files)
        if filename.endswith(".py"):
            vuln_res = scan_code_vulnerabilities(added_code)
            if vuln_res["has_vulnerabilities"]:
                for v in vuln_res["vulnerabilities"]:
                    if v["severity"] == "CRITICAL":
                        blocked_reasons.append(f"[{filename}] Critical Vulnerability at line {v['line']}: {v['type']}")
                    else:
                        warnings.append(f"[{filename}] Code warning: {v['type']}")
                    findings_summary.append({"file": filename, "type": v["type"], "detail": v["description"]})

    # Verdict
    if blocked_reasons:
        verdict = "BLOCKED"
        exit_code = 1
    elif warnings:
        verdict = "NEEDS_REVIEW"
        exit_code = 0
    else:
        verdict = "ALLOWED"
        exit_code = 0

    # Log in tamper-proof Merkle Ledger
    ledger_entry = global_merkle_ledger.record_event(
        event_type="CI_CD_PRE_MERGE_AUDIT",
        actor=f"PR_BOT_#{pr_number}",
        verdict=verdict,
        details={
            "files": list(diff_map.keys()),
            "blocked_reasons": blocked_reasons,
            "warnings_count": len(warnings)
        }
    )

    # Format Markdown PR Comment
    status_icon = "🟢" if verdict == "ALLOWED" else ("🟡" if verdict == "NEEDS_REVIEW" else "🔴")
    comment_md = f"""## {status_icon} KAVACH Autonomous CI/CD Pre-Merge Gate: **{verdict}**

| Audit Metric | Verdict & Status |
|:---|:---|
| **Gate Decision** | `{verdict}` (Exit Code: `{exit_code}`) |
| **Files Inspected** | `{len(diff_map)}` modified files |
| **Blocking Violations** | `{len(blocked_reasons)}` critical issues |
| **Warnings Flagged** | `{len(warnings)}` review items |
| **Merkle Ledger Root** | `{ledger_entry['merkle_root'][:16]}...` |

### 🔍 Security Findings Breakdown:
"""
    if blocked_reasons:
        comment_md += "\n**🚨 Blocking Issues (Merge Halted):**\n"
        for r in blocked_reasons:
            comment_md += f"- ❌ {r}\n"

    if warnings:
        comment_md += "\n**⚠️ Security Warnings (Review Required):**\n"
        for w in warnings:
            comment_md += f"- ⚠️ {w}\n"

    if not blocked_reasons and not warnings:
        comment_md += "\n✅ **100% Policy Clean:** Zero credential leaks, zero package hallucinations, and zero dangerous sinks detected.\n"

    return {
        "verdict": verdict,
        "exit_code": exit_code,
        "files_analyzed": len(diff_map),
        "blocked_reasons": blocked_reasons,
        "warnings": warnings,
        "findings": findings_summary,
        "merkle_root": ledger_entry["merkle_root"],
        "pr_comment_markdown": comment_md
    }
