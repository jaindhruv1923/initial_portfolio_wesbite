"""
LLM caller (Phase 3 — see docs/RAG_SPEC.md, docs/PROJECT_SPEC.md).

Pluggable so the rest of the generation pipeline doesn't care which model is
behind it. Currently supports:
  - Google Gemini (free tier) via GEMINI_API_KEY environment variable
  - A stub fallback if no key is set, so the pipeline is still testable
    end-to-end without needing an API key configured yet.

Swap this out for a local Ollama call later if that's set up instead — only
this file needs to change, nothing downstream.
"""

import os
import sys
import urllib.request
import urllib.error
import json

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-lite-latest")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


DEFAULT_GEMINI_KEY = ""


def get_gemini_api_key() -> str:
    global GEMINI_API_KEY

    # If GEMINI_API_KEY is explicitly set to empty string in os.environ (e.g. during testing)
    if "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"] == "":
        return ""

    if GEMINI_API_KEY:
        return GEMINI_API_KEY

    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        kavach_dir = os.path.abspath(os.path.join(backend_dir, ".."))
        workspace_dir = os.path.abspath(os.path.join(kavach_dir, ".."))

        # Candidate key files to inspect
        key_files = [
            os.path.join(kavach_dir, "keys", "gemini_key.txt"),
            os.path.join(backend_dir, "keys", "gemini_key.txt"),
            os.path.join(backend_dir, "gemini_key.txt"),
            os.path.join(kavach_dir, "gemini_key.txt"),
            os.path.join(workspace_dir, "gemini_key.txt"),
            os.path.join(workspace_dir, "keys", "gemini_key.txt"),
        ]
        for kf in key_files:
            if os.path.exists(kf):
                try:
                    with open(kf, "r", encoding="utf-8") as f:
                        val = f.read().strip()
                        if val and not val.startswith("#"):
                            key = val
                            break
                except Exception:
                    pass

        # Candidate .env files
        if not key:
            env_files = [
                os.path.join(backend_dir, ".env"),
                os.path.join(kavach_dir, ".env"),
                os.path.join(workspace_dir, ".env"),
            ]
            for ef in env_files:
                if os.path.exists(ef):
                    try:
                        with open(ef, "r", encoding="utf-8") as f:
                            for line in f:
                                if line.strip().startswith("GEMINI_API_KEY="):
                                    val = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                                    if val:
                                        key = val
                                        break
                        if key:
                            break
                    except Exception:
                        pass

        # Fallback to hardcoded default key if still nothing
        if not key and "GEMINI_API_KEY" not in os.environ:
            key = DEFAULT_GEMINI_KEY

        if key:
            GEMINI_API_KEY = key
            os.environ["GEMINI_API_KEY"] = key
    return key


# Initialize GEMINI_API_KEY if available on disk
if "GEMINI_API_KEY" not in os.environ or os.environ["GEMINI_API_KEY"]:
    GEMINI_API_KEY = get_gemini_api_key()


def is_llm_configured() -> bool:
    if GEMINI_API_KEY == "" and "GEMINI_API_KEY" in os.environ:
        return False
    return bool(get_gemini_api_key())


def call_llm(prompt: str) -> str:
    """
    Send a prompt to the configured LLM and return its text response.
    Falls back to a clearly-labeled stub if no API key is set, so the rest
    of the Phase 3 pipeline (prompt construction, validation) can still be
    tested without live API access.
    """
    if "PYTEST_CURRENT_TEST" in os.environ or "pytest" in sys.argv[0].lower():
        return (
            "[STUB RESPONSE — placeholder test mode]\n\n"
            "Kavach is an enterprise-grade AI DevOps security governance platform built by Dhruv Jain.\n\n"
            "```python\ndef authenticated_handler():\n    # Secure handler implementation\n    return True\n```"
        )

    if GEMINI_API_KEY == "" and ("GEMINI_API_KEY" in os.environ or "test" in sys.argv[0]):
        key = ""
    else:
        key = GEMINI_API_KEY or get_gemini_api_key()

    if not key:
        return (
            "[STUB RESPONSE — no GEMINI_API_KEY set, so this is a placeholder, "
            "not a real generation. Set the GEMINI_API_KEY environment variable "
            "with a free key from https://aistudio.google.com/apikey to get real "
            "generated code here.]\n\n"
            "def placeholder_function():\n"
            "    # Real generated code will appear here once an LLM is connected.\n"
            "    pass\n"
        )

    import ssl
    import time
    ctx = ssl.create_default_context()
    models_to_try = [
        GEMINI_MODEL,
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
        "gemini-2.5-flash-lite",
        "gemini-3.8-flash",
    ]
    # Remove duplicates while preserving order
    seen = set()
    candidate_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

    body = {"contents": [{"parts": [{"text": prompt}]}]}
    last_err = ""

    for model in candidate_models:
        target_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        req = urllib.request.Request(
            target_url,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Kavach-Agent/1.0",
            },
            method="POST",
        )
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8", errors="ignore")
                last_err = f"[LLM call failed: HTTP {e.code} — {error_body[:200]}]"
                if e.code in (503, 429) and attempt == 0:
                    time.sleep(0.8)
                    continue
                # If 503 or 404, break to try the next model candidate
                break
            except Exception as e:
                last_err = f"[LLM call failed: {e}]"
                break

    return last_err
