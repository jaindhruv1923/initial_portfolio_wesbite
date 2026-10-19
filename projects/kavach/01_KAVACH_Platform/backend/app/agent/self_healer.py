"""
Autonomous Self-Healing Code Loop (ReAct / Reflexion Engine).

Iterative test-driven repair cycle:
1. Executes candidate code against target unit tests in an isolated sandbox.
2. If tests fail, captures stdout/stderr and exact traceback.
3. Formulates a ReAct reflection prompt identifying root causes.
4. Invokes the LLM to generate an autonomous patch.
5. Re-executes the test suite and iterates until tests pass or max attempts reached.
"""

import os
import sys
import tempfile
import ast
import subprocess
from typing import Dict, Any, List, Optional
from app.generation.llm_client import call_llm
from app.generation.validator import extract_python_code_block, check_python_syntax


FORBIDDEN_SANDBOX_MODULES = {"os", "subprocess", "socket", "shutil", "ctypes", "pty", "winreg", "posix"}
FORBIDDEN_SANDBOX_CALLS = {"system", "popen", "spawn", "rmtree", "unlink", "remove", "kill"}


def verify_sandbox_ast_safety(code: str) -> tuple[bool, str]:
    """Pre-execution AST sandbox security verification to prevent host syscall attacks."""
    try:
        tree = ast.parse(code)
    except Exception:
        return True, "Valid"

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_pkg = alias.name.split(".")[0]
                if root_pkg in FORBIDDEN_SANDBOX_MODULES:
                    return False, f"Prohibited module '{root_pkg}' cannot be imported inside sandbox"
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in FORBIDDEN_SANDBOX_MODULES:
                return False, f"Prohibited module '{node.module}' cannot be imported inside sandbox"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
                return False, f"Prohibited dynamic code evaluation: {node.func.id}()"
            elif isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_SANDBOX_CALLS:
                return False, f"Prohibited syscall/attribute: {node.func.attr}()"

    return True, "Safe"


def run_sandboxed_test(code: str, test_code: str, timeout: float = 6.0) -> Dict[str, Any]:
    """
    Execute code and unit test in an isolated subprocess.
    Returns exit code, stdout, stderr, and whether tests passed.
    """
    # 0. Pre-execution AST security verification
    is_safe, sec_reason = verify_sandbox_ast_safety(code)
    if not is_safe:
        return {
            "passed": False,
            "error_type": "SecuritySandboxViolation",
            "error_message": f"Pre-execution AST sandbox violation: {sec_reason}",
            "stdout": "",
            "stderr": f"SECURITY SHIELD BLOCKED: {sec_reason}",
            "returncode": 1
        }

    # 1. Syntax check first
    syntax_code = check_python_syntax(code)
    if not syntax_code["valid_syntax"]:
        return {
            "passed": False,
            "error_type": "SyntaxError",
            "error_message": f"Syntax error in implementation: {syntax_code['error']}",
            "stdout": "",
            "stderr": str(syntax_code["error"]),
            "returncode": 1
        }

    combined_script = f"""# Autonomous Self-Healing Sandbox Execution
import sys
import unittest

# === IMPLEMENTATION CODE ===
{code}

# === TEST SUITE ===
{test_code}

if __name__ == '__main__':
    # Run tests with clean output
    unittest.main(exit=False)
"""

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(combined_script)
        temp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        passed = (result.returncode == 0) and ("FAILED" not in result.stderr) and ("ERROR" not in result.stderr)
        
        # Extract error summary
        err_msg = ""
        err_type = "ExecutionFailure"
        if not passed:
            output = result.stderr or result.stdout or "Test execution failed."
            lines = [l for l in output.splitlines() if l.strip()]
            err_msg = lines[-1] if lines else "Unknown test failure"
            for line in lines:
                if "AssertionError" in line:
                    err_type = "AssertionError"
                    break
                elif "TypeError" in line:
                    err_type = "TypeError"
                    break
                elif "KeyError" in line:
                    err_type = "KeyError"
                    break
                elif "IndexError" in line:
                    err_type = "IndexError"
                    break
                elif "NameError" in line:
                    err_type = "NameError"
                    break

        return {
            "passed": passed,
            "error_type": err_type if not passed else None,
            "error_message": err_msg if not passed else None,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "error_type": "TimeoutError",
            "error_message": f"Execution timed out after {timeout} seconds (potential infinite loop)",
            "stdout": "",
            "stderr": "TimeoutExpired",
            "returncode": -1
        }
    except Exception as e:
        return {
            "passed": False,
            "error_type": "SandboxError",
            "error_message": str(e),
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


def autonomous_self_heal(
    code: str,
    test_code: str,
    max_iterations: int = 3,
    custom_llm_fn=None
) -> Dict[str, Any]:
    """
    Autonomous closed-loop ReAct repair cycle.
    Continuously tests, diagnoses, and repairs code until all tests pass.
    """
    llm_fn = custom_llm_fn or call_llm
    current_code = code
    history: List[Dict[str, Any]] = []

    for attempt in range(1, max_iterations + 1):
        # 1. Execute sandbox test
        test_run = run_sandboxed_test(current_code, test_code)

        if test_run["passed"]:
            # Success!
            history.append({
                "iteration": attempt,
                "status": "PASSED",
                "code": current_code,
                "error": None,
                "action": "All test assertions passed successfully."
            })
            return {
                "success": True,
                "healed": attempt > 1,
                "iterations_required": attempt,
                "final_code": current_code,
                "status": "HEALED" if attempt > 1 else "PASSED_FIRST_TRY",
                "history": history,
                "verdict": f"Code verified. Passed after {attempt} iteration(s)."
            }

        # 2. Failure: record diagnostic details
        history.append({
            "iteration": attempt,
            "status": "FAILED",
            "code": current_code,
            "error_type": test_run["error_type"],
            "error_message": test_run["error_message"],
            "stderr_snippet": (test_run["stderr"] or "")[-400:],
            "action": f"Diagnosed {test_run['error_type']}. Generating autonomous repair patch."
        })

        if attempt >= max_iterations:
            break

        # 3. Formulate ReAct Reflection Prompt
        repair_prompt = f"""You are the KAVACH Autonomous Self-Healing Agent.
The following Python implementation failed its unit test suite.

--- CURRENT IMPLEMENTATION ---
{current_code}

--- TARGET UNIT TEST ---
{test_code}

--- FAILURE DIAGNOSTICS ---
Error Type: {test_run['error_type']}
Error Message: {test_run['error_message']}
Full Traceback:
{test_run['stderr']}

Analyze the exact root cause of the error. Fix the implementation so that all assertions pass.
Output ONLY the complete, corrected Python code inside a ```python ``` block without explanations.
"""
        raw_response = llm_fn(repair_prompt)
        extracted = extract_python_code_block(raw_response)

        if extracted and check_python_syntax(extracted)["valid_syntax"]:
            current_code = extracted
        else:
            # If LLM failed to produce valid syntax, keep code and try simpler heuristic
            pass

    return {
        "success": False,
        "healed": False,
        "iterations_required": max_iterations,
        "final_code": current_code,
        "status": "MAX_ITERATIONS_EXCEEDED",
        "history": history,
        "verdict": f"Self-healing exhausted {max_iterations} attempts without passing all test cases."
    }
