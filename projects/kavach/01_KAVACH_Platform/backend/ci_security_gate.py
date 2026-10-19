"""
Kavach CI security gate (Phase 7 — see docs/CICD_SPEC.md).

Runs the security engine's evaluation (Phase 4) and the impact analyzer's
evaluation (Phase 5) directly against their known test corpora, and FAILS
the CI job (non-zero exit code) if either quality metric drops below an
acceptable threshold. This is what actually gives CI/CD "teeth" here —
it's not just running tests, it's enforcing a quality bar on every change.

Run standalone (no server needed — calls the evaluator functions directly,
matching the pattern already used by GET /evaluate and GET /impact/evaluate):
    cd backend
    python ci_security_gate.py

Exit code 0 = gate passed. Exit code 1 = gate failed (thresholds not met).
"""

import json
import sys

# Minimum acceptable scores — see docs/EVALUATION_PLAN.md for why these
# specific metrics matter. Thresholds set slightly below the last verified
# result (security: precision 1.0/recall 1.0) so genuinely small, expected
# fluctuations don't fail the build, while real regressions still do.
SECURITY_MIN_PRECISION = 0.9
SECURITY_MIN_RECALL = 0.85
IMPACT_MIN_AVG_PRECISION = 0.4
IMPACT_MIN_AVG_RECALL = 0.5


def run_security_gate() -> dict:
    from app.security.evaluator import evaluate as evaluate_security

    result = evaluate_security()
    overall = result["overall"]
    passed = (
        overall["precision"] >= SECURITY_MIN_PRECISION
        and overall["recall"] >= SECURITY_MIN_RECALL
    )
    return {
        "check": "security_engine",
        "passed": passed,
        "precision": overall["precision"],
        "recall": overall["recall"],
        "f1": overall["f1"],
        "thresholds": {"min_precision": SECURITY_MIN_PRECISION, "min_recall": SECURITY_MIN_RECALL},
    }


def run_impact_gate() -> dict:
    from app.impact.evaluator import evaluate as evaluate_impact

    result = evaluate_impact()
    overall = result["overall"]
    passed = (
        overall["avg_precision"] >= IMPACT_MIN_AVG_PRECISION
        and overall["avg_recall"] >= IMPACT_MIN_AVG_RECALL
    )
    return {
        "check": "impact_analyzer",
        "passed": passed,
        "avg_precision": overall["avg_precision"],
        "avg_recall": overall["avg_recall"],
        "avg_f1": overall["avg_f1"],
        "thresholds": {
            "min_avg_precision": IMPACT_MIN_AVG_PRECISION,
            "min_avg_recall": IMPACT_MIN_AVG_RECALL,
        },
    }


def main():
    print("Kavach CI security gate — running evaluations...\n")

    results = []
    overall_passed = True

    try:
        security_result = run_security_gate()
        results.append(security_result)
        status = "PASS" if security_result["passed"] else "FAIL"
        print(f"[{status}] Security engine — precision={security_result['precision']}, "
              f"recall={security_result['recall']}, f1={security_result['f1']}")
        if not security_result["passed"]:
            overall_passed = False
    except Exception as e:
        print(f"[ERROR] Security gate could not run: {e}")
        results.append({"check": "security_engine", "passed": False, "error": str(e)})
        overall_passed = False

    try:
        impact_result = run_impact_gate()
        results.append(impact_result)
        status = "PASS" if impact_result["passed"] else "FAIL"
        print(f"[{status}] Impact analyzer — avg_precision={impact_result['avg_precision']}, "
              f"avg_recall={impact_result['avg_recall']}, avg_f1={impact_result['avg_f1']}")
        if not impact_result["passed"]:
            overall_passed = False
    except Exception as e:
        print(f"[ERROR] Impact gate could not run: {e}")
        results.append({"check": "impact_analyzer", "passed": False, "error": str(e)})
        overall_passed = False

    report = {"overall_passed": overall_passed, "checks": results}
    with open("security_gate_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\nGate result: {'PASSED' if overall_passed else 'FAILED'}")
    sys.exit(0 if overall_passed else 1)


if __name__ == "__main__":
    main()
