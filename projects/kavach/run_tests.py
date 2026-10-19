#!/usr/bin/env python
"""
Root convenience wrapper for KAVACH test suite.
Executes the test runner located in important/kavach/run_tests.py.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "01_KAVACH_Platform" / "run_tests.py"

if not TARGET.exists():
    TARGET = ROOT / "important" / "kavach" / "run_tests.py"

if not TARGET.exists():
    TARGET = ROOT / "kavach" / "run_tests.py"

if not TARGET.exists():
    print(f"Error: run_tests.py not found at {TARGET}")
    sys.exit(1)

result = subprocess.run([sys.executable, str(TARGET)] + sys.argv[1:])
sys.exit(result.returncode)
