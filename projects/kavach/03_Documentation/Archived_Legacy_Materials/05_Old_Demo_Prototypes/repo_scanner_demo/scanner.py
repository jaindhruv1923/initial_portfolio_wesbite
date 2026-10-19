import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()

CANDIDATE_MODELS = [
    DEFAULT_MODEL,
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash"
]

def call_gemini(prompt: str, api_key: str = None) -> str:
    """Calls Gemini REST API with the provided prompt."""
    key = api_key or GEMINI_API_KEY
    if not key:
        raise ValueError("GEMINI_API_KEY is not configured in .env or environment!")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 4096
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")

    last_error = ""
    seen = set()
    models = [m for m in CANDIDATE_MODELS if not (m in seen or seen.add(m))]

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            last_error = f"Model {model} failed (HTTP {e.code}): {err_body[:200]}"
            continue
        except Exception as e:
            last_error = f"Model {model} error: {e}"
            continue

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")


def scan_repo_with_llm(repo_data: Dict[str, Any], user_request: str, api_key: str = None) -> Dict[str, Any]:
    """
    Takes ingested repository data and a user request/query,
    filters the relevant context, feeds it to the LLM, and gets the scan result.
    """
    chunks: List[Dict[str, Any]] = repo_data.get("chunks", [])
    files: List[Dict[str, Any]] = repo_data.get("files", [])

    if not chunks:
        return {
            "request": user_request,
            "error": "No code found in ingested repository."
        }

    # Keyword relevance scoring to rank most relevant chunks
    keywords = [w.lower() for w in user_request.replace("?", " ").replace(",", " ").replace(".", " ").split() if len(w) > 2]
    
    scored_chunks = []
    for c in chunks:
        content_lower = c["content"].lower()
        file_lower = c["file"].lower()
        score = sum(3 for k in keywords if k in file_lower) + sum(1 for k in keywords if k in content_lower)
        scored_chunks.append((score, c))

    # Sort chunks by score descending
    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    # Context window management (around 25,000 characters for high speed)
    selected_chunks = []
    current_chars = 0
    max_chars = 25000

    for score, chunk in scored_chunks:
        if current_chars + len(chunk["content"]) > max_chars:
            break
        selected_chunks.append(chunk)
        current_chars += len(chunk["content"])

    if not selected_chunks:
        selected_chunks = [c for _, c in scored_chunks[:8]]

    # Prepare context string
    context_parts = []
    scanned_files = set()
    for chunk in selected_chunks:
        scanned_files.add(chunk["file"])
        context_parts.append(
            f"--- FILE: {chunk['file']} (Lines {chunk['start_line']}-{chunk['end_line']}) ---\n"
            f"{chunk['content']}\n"
        )
    
    code_context = "\n".join(context_parts)
    files_overview = "\n".join([f"- {f['path']} ({f['lines']} lines)" for f in files])

    prompt = f"""You are an expert AI Code Scanner and Repository Analyst.

Repository Overview ({len(files)} files):
{files_overview}

Here is the ingested source code context:
{code_context}

User Request / Scan Prompt:
"{user_request}"

INSTRUCTIONS:
1. Scan the provided codebase specifically addressing the user's request.
2. If the user asks for security scan / vulnerabilities, list all findings, affected files, line numbers, severity (CRITICAL, HIGH, MEDIUM, LOW), and fix suggestions.
3. If the user asks an architectural, logic, or code explanation question, give a clear, precise breakdown with code references.
4. Always cite specific files and line numbers (e.g., `auth.py:L15-L25`) for all findings.
5. Provide a clear Executive Summary followed by Detailed Scan Findings and Actionable Recommendations.
"""

    llm_output = call_gemini(prompt, api_key=api_key)

    return {
        "user_request": user_request,
        "repo_path": repo_data.get("repo_path"),
        "files_scanned_count": len(scanned_files),
        "files_scanned": sorted(list(scanned_files)),
        "chunks_evaluated": len(selected_chunks),
        "total_repo_files": len(files),
        "scan_result": llm_output
    }
