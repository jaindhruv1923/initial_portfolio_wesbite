#!/usr/bin/env python
"""
Root convenience wrapper for KAVACH project verification.
Executes the comprehensive verification script located in important/kavach/verify_project.py.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "01_KAVACH_Platform" / "verify_project.py"

if not TARGET.exists():
    TARGET = ROOT / "important" / "kavach" / "verify_project.py"

if not TARGET.exists():
    TARGET = ROOT / "kavach" / "verify_project.py"

if not TARGET.exists():
    print(f"Error: verify_project.py not found at {TARGET}")
    sys.exit(1)

result = subprocess.run([sys.executable, str(TARGET)] + sys.argv[1:])
sys.exit(result.returncode)
