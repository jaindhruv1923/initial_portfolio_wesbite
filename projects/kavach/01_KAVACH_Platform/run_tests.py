#!/usr/bin/env python
"""Simple script to run tests and report results."""

from pathlib import Path
import subprocess
import sys

project_root = Path(__file__).resolve().parent

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests", "-q", "--tb=no"],
    capture_output=True,
    text=True,
    cwd=str(project_root),
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nReturn code: {result.returncode}")
