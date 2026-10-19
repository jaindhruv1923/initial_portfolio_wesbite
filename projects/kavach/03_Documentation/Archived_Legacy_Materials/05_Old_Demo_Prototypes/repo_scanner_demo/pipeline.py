import time
from typing import Dict, Any, List
from ingestor import ingest_repository
from scanner import call_gemini
from governance import (
    detect_input_risks,
    evaluate_input_guardrail,
    evaluate_output_governance
)

def run_governed_pipeline(repo_data: Dict[str, Any], user_request: str) -> Dict[str, Any]:
    """
    Executes the 5-Phase Kavach Governed DevOps Pipeline:
    Phase 1: Ingestion & Indexing
    Phase 2: Security Check & Policy Gate (Input Guardrail)
    Phase 3: Context Retrieval & Intent Planning
    Phase 4: LLM Generation & Reasoning
    Phase 5: Output Validation & Governance Gate
    """
    start_total = time.time()
    phases = []
    
    # -------------------------------------------------------------
    # PHASE 1: Repository Ingestion & Code Indexing
    # -------------------------------------------------------------
    p1_start = time.time()
    files_count = repo_data.get("files_count", 0)
    total_lines = repo_data.get("total_lines", 0)
    chunks_count = repo_data.get("chunks_count", 0)
    
    phases.append({
        "phase_number": 1,
        "name": "Phase 1: Repository Ingestion & Indexing",
        "status": "PASSED",
        "duration_ms": round((time.time() - p1_start) * 1000, 2),
        "details": f"Parsed {files_count} files ({total_lines} lines), created {chunks_count} searchable code chunks."
    })

    # -------------------------------------------------------------
    # PHASE 2: Security Check & Policy Gate (Input Guardrail)
    # -------------------------------------------------------------
    p2_start = time.time()
    input_findings = detect_input_risks(user_request)
    input_policy = evaluate_input_guardrail(user_request, input_findings)
    p2_duration = round((time.time() - p2_start) * 1000, 2)

    if not input_policy["allowed"]:
        phases.append({
            "phase_number": 2,
            "name": "Phase 2: Security Check & Policy Gate",
            "status": input_policy["verdict"],
            "duration_ms": p2_duration,
            "details": input_policy["explanation"],
            "findings": input_findings
        })
        # Short-circuit execution if BLOCKED or hard-stopped
        return {
            "user_request": user_request,
            "final_stage": input_policy["stage"],
            "verdict": input_policy["verdict"],
            "phases": phases,
            "duration_ms": round((time.time() - start_total) * 1000, 2),
            "output": f"🛑 Request halted by Kavach Security Gate: {input_policy['explanation']}",
            "findings": input_findings,
            "code_generated": None
        }

    phases.append({
        "phase_number": 2,
        "name": "Phase 2: Security Check & Policy Gate",
        "status": input_policy["verdict"],
        "duration_ms": p2_duration,
        "details": input_policy["explanation"],
        "findings": input_findings
    })

    # -------------------------------------------------------------
    # PHASE 3: Context Retrieval & Intent Planning
    # -------------------------------------------------------------
    p3_start = time.time()
    req_lower = user_request.lower()
    
    # Classify intent
    is_code_gen = any(k in req_lower for k in [
        "give me code", "give me the code", "write code", "implement", "create function",
        "prime", "uber", "algorithm", "generate function", "class for", "snippet"
    ])
    is_devops = any(k in req_lower for k in [
        "devops", "docker", "dockerfile", "pipeline", "ci/cd", "github action",
        "deploy", "kubernetes", "k8s", "helm"
    ])

    intent = "CODE_GENERATION" if is_code_gen else ("DEVOPS_AUTOMATION" if is_devops else "REPOSITORY_SCAN")
    
    # Filter relevant chunks
    keywords = [w.lower() for w in user_request.replace("?", " ").replace(",", " ").replace(".", " ").split() if len(w) > 2]
    chunks = repo_data.get("chunks", [])
    scored_chunks = []
    for c in chunks:
        content_lower = c["content"].lower()
        file_lower = c["file"].lower()
        score = sum(3 for k in keywords if k in file_lower) + sum(1 for k in keywords if k in content_lower)
        scored_chunks.append((score, c))
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    selected_chunks = [c for _, c in scored_chunks[:6]] if scored_chunks else []
    context_str = "\n".join([f"[{c['file']}:L{c['start_line']}-{c['end_line']}]\n{c['content']}" for c in selected_chunks])

    phases.append({
        "phase_number": 3,
        "name": "Phase 3: Context Retrieval & Intent Planning",
        "status": "PASSED",
        "duration_ms": round((time.time() - p3_start) * 1000, 2),
        "details": f"Intent identified: '{intent}'. Retrieved {len(selected_chunks)} contextual code blocks from repository."
    })

    # -------------------------------------------------------------
    # PHASE 4: LLM Generation & Reasoning (Gemini)
    # -------------------------------------------------------------
    p4_start = time.time()
    
    prompt = f"""You are an expert AI DevOps and Code Generation Assistant adhering to the Kavach security-governed framework.

Repository Ingested Context ({files_count} files):
{context_str if context_str else "No direct file context needed for this query."}

User Request:
"{user_request}"

Execution Guidelines:
- If the user asks for code (e.g. prime numbers, Uber surge pricing, algorithms, helpers):
  Provide production-ready, clean, well-documented code with time complexity, input validation, and example test cases.
- If the user asks for DevOps (e.g. Dockerfile, CI/CD, Kubernetes, deployment):
  Provide secure, production-grade configurations adhering to safe DevOps best practices (non-root users, pin versions, minimal base images).
- If the user asks to scan/audit repository code:
  Detail vulnerabilities, exact file and line references, severity levels (CRITICAL, HIGH, MEDIUM, LOW), and fixes.

Deliver your response clearly and concisely.
"""
    try:
        llm_response = call_gemini(prompt)
        llm_status = "PASSED"
        details_msg = "Successfully received response from Gemini."
    except Exception as e:
        llm_response = f"[LLM call failed: {e}]"
        llm_status = "FAILED"
        details_msg = f"LLM error: {e}"

    phases.append({
        "phase_number": 4,
        "name": "Phase 4: LLM Generation & Reasoning",
        "status": llm_status,
        "duration_ms": round((time.time() - p4_start) * 1000, 2),
        "details": details_msg
    })

    if llm_status == "FAILED":
        return {
            "user_request": user_request,
            "final_stage": "NEEDS_REVIEW",
            "verdict": "NEEDS_REVIEW",
            "phases": phases,
            "duration_ms": round((time.time() - start_total) * 1000, 2),
            "output": llm_response,
            "findings": input_findings
        }

    # -------------------------------------------------------------
    # PHASE 5: Output Validation & Governance Gate
    # -------------------------------------------------------------
    p5_start = time.time()
    gov_eval = evaluate_output_governance(llm_response, input_policy["verdict"])
    p5_duration = round((time.time() - p5_start) * 1000, 2)

    phases.append({
        "phase_number": 5,
        "name": "Phase 5: Output Validation & Governance Gate",
        "status": gov_eval["verdict"],
        "duration_ms": p5_duration,
        "details": gov_eval["reason"],
        "syntax": gov_eval.get("syntax"),
        "findings": gov_eval.get("findings", [])
    })

    return {
        "user_request": user_request,
        "final_stage": gov_eval["stage"],
        "verdict": gov_eval["verdict"],
        "intent": intent,
        "phases": phases,
        "duration_ms": round((time.time() - start_total) * 1000, 2),
        "output": llm_response,
        "syntax_validation": gov_eval.get("syntax"),
        "findings": input_findings + gov_eval.get("findings", [])
    }
