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
import urllib.request
import urllib.error
import json

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
# NOTE: gemini-2.0-flash was shut down June 1, 2026. gemini-3.5-flash is the
# current officially documented model as of this writing (Aug 2026) — check
# https://ai.google.dev/gemini-api/docs/changelog if this 404s again in the
# future, since Google periodically retires older model versions.
GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


def is_llm_configured() -> bool:
    return bool(GEMINI_API_KEY)


def call_llm(prompt: str) -> str:
    """
    Send a prompt to the configured LLM and return its text response.
    Falls back to a clearly-labeled stub if no API key is set, so the rest
    of the Phase 3 pipeline (prompt construction, validation) can still be
    tested without live API access.
    """
    if not GEMINI_API_KEY:
        return (
            "[STUB RESPONSE — no GEMINI_API_KEY set, so this is a placeholder, "
            "not a real generation. Set the GEMINI_API_KEY environment variable "
            "with a free key from https://aistudio.google.com/apikey to get real "
            "generated code here.]\n\n"
            "def placeholder_function():\n"
            "    # Real generated code will appear here once an LLM is connected.\n"
            "    pass\n"
        )

    body = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(
        GEMINI_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        return f"[LLM call failed: HTTP {e.code} — {error_body[:300]}]"
    except Exception as e:
        return f"[LLM call failed: {e}]"
