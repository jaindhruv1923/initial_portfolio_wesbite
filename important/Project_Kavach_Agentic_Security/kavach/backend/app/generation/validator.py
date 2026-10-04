"""
Basic generated-code validation (Phase 3 — first step toward "Build & tests"
in docs/ARCHITECTURE.md; full test execution comes later as the pipeline
matures).

Starts with a syntax check — the cheapest possible signal that generated
code isn't garbage — before anything more expensive (actual test execution,
CI) runs on it.
"""

import re


def extract_python_code_block(text: str) -> str | None:
    """
    Pull the first ```python ... ``` fenced block out of an LLM response,
    if present. Falls back to the raw text if no fenced block is found
    (some responses come back as plain code with no markdown fencing).
    """
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip() if text.strip() else None


def check_python_syntax(code: str) -> dict:
    """
    Attempt to compile the given code string. This does NOT execute it —
    compile() alone only checks syntax validity, which is a safe, cheap
    first check before anything runs.
    """
    if not code:
        return {"valid_syntax": False, "error": "No code to check."}
    try:
        compile(code, "<generated>", "exec")
        return {"valid_syntax": True, "error": None}
    except SyntaxError as e:
        return {"valid_syntax": False, "error": str(e)}


def validate_generated_output(raw_output: str) -> dict:
    """Extract code from a raw LLM response and run the syntax check on it."""
    code = extract_python_code_block(raw_output)
    if code is None:
        return {"valid_syntax": False, "error": "No code found in output.", "extracted_code": None}
    result = check_python_syntax(code)
    result["extracted_code"] = code
    return result
