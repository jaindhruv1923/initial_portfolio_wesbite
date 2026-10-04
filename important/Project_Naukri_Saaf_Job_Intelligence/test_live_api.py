"""
Naukri Saaf — API Verification Runner (Root Shim)
Delegates execution to scripts/test_live_api.py.
"""
import os
import sys
import subprocess

if __name__ == "__main__":
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "test_live_api.py")
    result = subprocess.run([sys.executable, script_path] + sys.argv[1:])
    sys.exit(result.returncode)
