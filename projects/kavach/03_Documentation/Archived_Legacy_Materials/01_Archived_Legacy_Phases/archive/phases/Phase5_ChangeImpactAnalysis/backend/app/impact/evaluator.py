"""
Impact analysis evaluation (Phase 5 / Phase 9 groundwork — see
docs/EVALUATION_PLAN.md, Research Question 3).

Runs known change-description test cases through analyze_impact() and
compares predicted affected files against the actual known-affected files,
computing precision/recall/F1 — same "real metrics, never fabricated"
principle as security/evaluator.py.
"""

import json
import os

from app.impact.analyzer import analyze_impact

TEST_CASES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "impact_test_cases.json")
REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")  # the backend/app directory


def load_test_cases() -> list[dict]:
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate() -> dict:
    test_cases = load_test_cases()
    all_precisions, all_recalls, all_f1s = [], [], []
    per_case_results = []

    for case in test_cases:
        predicted = analyze_impact(case["change_description"], REPO_ROOT, top_k=5)
        predicted_files = {p["file_path"].replace("/", "\\") for p in predicted}
        actual_files = {f for f in case["actual_affected_files"]}

        tp = len(predicted_files & actual_files)
        fp = len(predicted_files - actual_files)
        fn = len(actual_files - predicted_files)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        all_precisions.append(precision)
        all_recalls.append(recall)
        all_f1s.append(f1)

        per_case_results.append({
            "id": case["id"],
            "change_description": case["change_description"],
            "predicted_files": sorted(predicted_files),
            "actual_files": sorted(actual_files),
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
        })

    n = len(test_cases) or 1
    return {
        "overall": {
            "avg_precision": round(sum(all_precisions) / n, 3),
            "avg_recall": round(sum(all_recalls) / n, 3),
            "avg_f1": round(sum(all_f1s) / n, 3),
        },
        "per_case": per_case_results,
        "total_cases": len(test_cases),
    }
