"""
Naukri Saaf — Full End-to-End API Verification Script
======================================================
Works in any Windows shell (CMD, PowerShell, Bash) without Unicode encoding issues.
Tests all 11 endpoints with detailed response telemetry.

Usage:
  python test_live_api.py
"""

import sys
import os

# Ensure UTF-8 output on Windows CMD / PowerShell
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def test_via_testclient():
    print("=" * 80)
    print("  NAUKRI SAAF - IN-PROCESS TESTCLIENT VERIFICATION")
    print("=" * 80)
    from fastapi.testclient import TestClient
    from src.api.main import app

    client = TestClient(app)

    tests = [
        ("GET", "/", None),
        ("GET", "/health", None),
        ("GET", "/api/v1/model-info", None),
        ("POST", "/api/v1/score", {
            "job_title": "Senior Data Scientist",
            "company_name": "TechStaff Solutions",
            "source": "Indeed",
            "description_text": "Urgent hiring! Send CV to hr@gmail.com on WhatsApp. Deposit registration fee 3500.",
            "days_live": 95.0
        }),
        ("POST", "/api/v1/verify-ats", {
            "company_name": "Razorpay",
            "job_title": "Lead Backend Engineer"
        }),
        ("POST", "/api/v1/counterfactual", {
            "current_prob": 0.85,
            "days_live": 90.0,
            "salary_disclosed": False,
            "desc_length_words": 120,
            "employer_repost_count": 4,
            "company_completeness": 30.0
        }),
        ("POST", "/api/v1/lifecycle-telemetry", {
            "applications_count": 120.0,
            "days_live": 75.0,
            "ghost_prob": 0.80
        }),
        ("POST", "/api/v1/recommend-alternatives", {
            "job_title": "Data Scientist",
            "company_name": "TechStaff",
            "location_city": "Bangalore",
            "top_k": 2
        }),
        ("POST", "/api/v1/audit-recruiter", {
            "company_name": "Uber",
            "description_text": "Selected! Send registration deposit 3000 to careers@uber-jobs.in on WhatsApp: 9876543210"
        }),
        ("POST", "/api/v1/estimate-salary", {
            "job_title": "Machine Learning Engineer",
            "location_city": "Bangalore",
            "years_experience": 4.0,
            "salary_min": 400000.0,
            "salary_max": 4500000.0
        }),
        ("POST", "/api/v1/defense-playbook", {
            "job_title": "Backend Engineer",
            "company_name": "Acme Corp",
            "days_live": 45.0
        }),
    ]

    all_passed = True
    for method, path, body in tests:
        if method == "GET":
            res = client.get(path)
        else:
            res = client.post(path, json=body)
        
        status = res.status_code
        is_ok = 200 <= status < 300
        icon = "[PASS]" if is_ok else "[FAIL]"
        print(f"  {icon} {method:4s} {path:32s} -> Status: {status}")
        if not is_ok:
            all_passed = False
            print(f"         Error: {res.text[:200]}")
        else:
            data = res.json()
            if isinstance(data, dict):
                sample_keys = list(data.keys())[:4]
                print(f"         Response keys: {sample_keys}")
            elif isinstance(data, list):
                print(f"         Returned {len(data)} items")

    print("\n" + ("=" * 80))
    if all_passed:
        print("  ALL 11 API ENDPOINTS PASSED WITH 100% SUCCESS!")
    else:
        print("  SOME ENDPOINTS FAILED")
    print("=" * 80)
    return all_passed

if __name__ == "__main__":
    test_via_testclient()
