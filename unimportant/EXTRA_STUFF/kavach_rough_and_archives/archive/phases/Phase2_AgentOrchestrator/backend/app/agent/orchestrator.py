"""
Agent Orchestrator (Phase 2 — see docs/AGENT_SPEC.md and docs/ARCHITECTURE.md).

Coordinates a workflow run through: planning -> RAG retrieval -> security check.
Later phases (generation, test generation, build/test, CI/CD, impact analysis)
will slot into this same state machine as they're built — see WorkflowStage in
state.py for the full intended sequence.
"""

from app.agent.state import WorkflowRun, WorkflowStage, save_run
from app.agent.planner import plan_request
from app.rag.embed_store import search
from app.security.detector import detect_pii
from app.generation.generator import generate_code
from app.generation.validator import validate_generated_output
from app.impact.analyzer import analyze_impact
import os


def run_workflow(request_text: str) -> WorkflowRun:
    """
    Execute the currently-implemented portion of the Kavach workflow for a
    single developer request, and return the resulting WorkflowRun (with
    full stage history for transparency/debugging/demo purposes).
    """
    run = WorkflowRun(request_text=request_text)
    save_run(run)

    # --- Stage: Kavach security check on the raw input first ---
    # (Checking the input itself, before any planning/retrieval happens, is
    # deliberate — see docs/SECURITY_SPEC.md: "Where checks happen" includes
    # developer input as the first checkpoint.)
    input_findings = detect_pii(request_text)
    run.security_findings.extend(input_findings)
    if any(f["action"] == "BLOCK" for f in input_findings):
        run.advance(WorkflowStage.BLOCKED, "sensitive data detected in the raw request")
        save_run(run)
        return run

    # --- Stage: Planning ---
    run.advance(WorkflowStage.PLANNING)
    run.plan = plan_request(request_text)
    save_run(run)

    # --- Stage: Context retrieval (RAG) ---
    run.advance(WorkflowStage.CONTEXT_RETRIEVAL)
    try:
        run.retrieved_context = search(request_text, top_k=5)
    except Exception as e:
        # RAG index may not exist yet if /ingest hasn't been run — degrade
        # gracefully rather than crash the whole workflow.
        run.retrieved_context = []
        run.history.append(f"RAG retrieval skipped/failed: {e}")
    save_run(run)

    # --- Stage: Security check on retrieved context ---
    run.advance(WorkflowStage.SECURITY_CHECK)
    for chunk in run.retrieved_context:
        chunk_findings = detect_pii(chunk.get("text", ""))
        run.security_findings.extend(chunk_findings)
    if any(f["action"] == "BLOCK" for f in run.security_findings):
        run.advance(WorkflowStage.NEEDS_REVIEW, "sensitive data found in retrieved context")
        save_run(run)
        return run

    # --- Stage: Change-impact analysis (Phase 5, Professor Idea #1 focused slice) ---
    run.advance(WorkflowStage.IMPACT_ANALYSIS)
    try:
        repo_root = os.path.join(os.path.dirname(__file__), "..")  # backend/app
        run.impact_report = analyze_impact(request_text, repo_root, top_k=5)
    except Exception as e:
        run.impact_report = []
        run.history.append(f"Impact analysis skipped/failed: {e}")
    save_run(run)

    # --- Stage: Evidence-grounded generation (Phase 3, Professor Idea #4) ---
    run.advance(WorkflowStage.GENERATION)
    generation_result = generate_code(request_text, run.retrieved_context)
    run.generation_result = generation_result
    save_run(run)

    generated_output = generation_result.get("generated_output", "")
    generation_failed = generated_output.startswith("[LLM call failed:")

    if generation_failed:
        # Don't hand an API error message to the syntax validator as if it
        # were code — report it as a generation failure instead.
        run.validation_result = {"valid_syntax": False, "error": "LLM generation failed — see generation_result", "extracted_code": None}
        run.advance(WorkflowStage.NEEDS_REVIEW, "LLM generation call failed — see generation_result for details")
        save_run(run)
        return run

    # --- Security check on generated output (see docs/SECURITY_SPEC.md: checks
    # apply to generated code too, not just the original request) ---
    generation_findings = detect_pii(generated_output)
    run.security_findings.extend(generation_findings)
    if any(f["action"] == "BLOCK" for f in generation_findings):
        run.advance(WorkflowStage.BLOCKED, "sensitive data detected in generated output")
        save_run(run)
        return run

    # --- Basic syntax validation of the generated code ---
    validation_result = validate_generated_output(generation_result.get("generated_output", ""))
    run.validation_result = validation_result
    save_run(run)

    # --- Remaining stages (test generation, build/test, CI/CD, impact
    # analysis) are not implemented yet — mark complete for the portion of
    # the pipeline that exists so far. ---
    run.advance(WorkflowStage.COMPLETE, "Phase 3 scope complete (planning + RAG + generation + security + syntax check)")
    save_run(run)
    return run
