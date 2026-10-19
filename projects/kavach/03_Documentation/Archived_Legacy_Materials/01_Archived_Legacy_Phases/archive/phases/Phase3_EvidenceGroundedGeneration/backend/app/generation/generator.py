"""
Evidence-grounded code generation (Phase 3 — Professor Idea #4, see docs/RAG_SPEC.md).

Core idea (from docs/RAG_SPEC.md): don't let the LLM guess at the project's
structure — feed it the actual retrieved repository evidence first, so it
generates code consistent with what already exists instead of inventing
APIs/libraries that aren't there.
"""

from app.generation.llm_client import call_llm, is_llm_configured


def build_grounded_prompt(request_text: str, retrieved_context: list[dict]) -> str:
    """
    Construct a prompt that grounds the LLM in real repository evidence
    before asking it to generate anything.
    """
    if retrieved_context:
        evidence_block = "\n\n".join(
            f"--- From {chunk['file_path']} ---\n{chunk['text']}"
            for chunk in retrieved_context
        )
    else:
        evidence_block = "(No repository evidence was retrieved for this request.)"

    prompt = f"""You are a careful software engineer working inside an existing project.
Use ONLY the repository evidence below to inform your answer — do not invent
libraries, APIs, or file structures that aren't shown here. If the evidence
is insufficient to safely implement the request, say so explicitly instead
of guessing.

REPOSITORY EVIDENCE:
{evidence_block}

DEVELOPER REQUEST:
{request_text}

Provide the code change needed to satisfy this request, consistent with the
evidence above. Keep the response focused and include a one-line comment
explaining any assumption you had to make.
"""
    return prompt


def generate_code(request_text: str, retrieved_context: list[dict]) -> dict:
    """
    Run the evidence-grounded generation step and return both the raw
    output and metadata about how it was produced (for transparency and
    for the evaluation plan in docs/EVALUATION_PLAN.md — comparing
    LLM-without-RAG vs LLM-with-RAG later).
    """
    prompt = build_grounded_prompt(request_text, retrieved_context)
    output = call_llm(prompt)
    return {
        "llm_configured": is_llm_configured(),
        "evidence_chunks_used": len(retrieved_context),
        "prompt": prompt,
        "generated_output": output,
    }
