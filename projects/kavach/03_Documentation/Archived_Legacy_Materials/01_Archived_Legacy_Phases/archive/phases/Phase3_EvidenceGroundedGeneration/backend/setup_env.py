"""
setup_env.py — run this once to create backend/.env correctly.

This avoids the encoding issues that come from `echo ... > .env` in
Windows terminals (which can save UTF-16 instead of UTF-8, causing a
UnicodeDecodeError when python-dotenv tries to read it).

Usage (from inside the backend/ folder):
    python setup_env.py

It will prompt for your Gemini API key and write .env correctly.
Get a free key at: https://aistudio.google.com/apikey
"""

import os

env_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(env_path):
    overwrite = input(".env already exists. Overwrite it? (y/n): ").strip().lower()
    if overwrite != "y":
        print("Cancelled — .env left unchanged.")
        raise SystemExit(0)

key = input("Paste your Gemini API key (from https://aistudio.google.com/apikey): ").strip()

if not key:
    print("No key entered — .env not created.")
    raise SystemExit(1)

with open(env_path, "w", encoding="utf-8") as f:
    f.write(f"GEMINI_API_KEY={key}\n")

print(f".env created successfully at {env_path}")
print("You can now start the server with: python -m uvicorn app.main:app --reload")
