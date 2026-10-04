"""
Planner (Phase 2 — see docs/AGENT_SPEC.md).

IMPORTANT — honest note for the report/viva: this is currently a simple, rule-based
planner, NOT an LLM call. Building the orchestrator's plumbing (state machine, RAG
wiring, security gating) doesn't require an LLM to be working yet, so this stub lets
Phase 2 be built and tested independently of API/Ollama setup.

Swap `plan_request()`'s body for a real LLM call (local via Ollama, or cloud) once
that's set up — the function signature and return shape are designed so nothing else
in the orchestrator needs to change when you do.
"""

import re


# Very simple keyword-based task decomposition. This is intentionally naive —
# it exists to prove the workflow end-to-end, not to be the final planning logic.
_TASK_KEYWORDS = {
    "auth": ["Identify authentication-related files", "Review existing auth logic"],
    "password": ["Locate password handling code", "Check password reset flow if present"],
    "test": ["Identify existing test files", "Determine what new tests are needed"],
    "api": ["Locate relevant API route definitions", "Review request/response schemas"],
    "database": ["Identify affected database models/schema", "Check for migration needs"],
}


def plan_request(request_text: str) -> list[str]:
    """
    Break a natural-language developer request into a structured list of
    sub-tasks. Currently rule-based (see module docstring) — replace with an
    LLM call for real planning once an LLM is available.
    """
    text_lower = request_text.lower()
    tasks = ["Understand the request and identify its scope"]

    matched_any = False
    for keyword, keyword_tasks in _TASK_KEYWORDS.items():
        if re.search(rf"\b{keyword}\b", text_lower):
            tasks.extend(keyword_tasks)
            matched_any = True

    if not matched_any:
        tasks.append("Retrieve relevant repository context for this request (general search)")

    tasks.append("Retrieve grounding evidence from the repository (RAG)")
    tasks.append("Run security/policy checks on the request and any retrieved context")

    return tasks
