"""
Security v2 evaluator — secrets + hard negatives + action-risk classification
(Part 2 — addresses Limitations #2, #7, #11: false positives, dedicated
secret detection, and dataset size, evaluated together honestly).
"""

import json
import os

from app.security.detector import detect_pii
from app.security.secret_detector import detect_secrets
from app.security.policy_engine import classify_action_risk

CORPUS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "security_v2_test_cases.json")


def load_corpus() -> list[dict]:
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_v2() -> dict:
    corpus = load_corpus()
    tp = fp = fn = tn = 0
    per_case = []
    action_risk_correct = 0
    action_risk_total = 0

    for case in corpus:
        findings = detect_pii(case["text"]) + detect_secrets(case["text"])
        flagged = len(findings) > 0
        actually_sensitive = case["sensitive"]

        if actually_sensitive and flagged:
            tp += 1
            outcome = "TP"
        elif actually_sensitive and not flagged:
            fn += 1
            outcome = "FN"
        elif not actually_sensitive and flagged:
            fp += 1
            outcome = "FP"
        else:
            tn += 1
            outcome = "TN"

        entry = {"id": case["id"], "category": case["category"], "outcome": outcome}

        if "expected_action_risk" in case:
            action_risk_total += 1
            predicted = classify_action_risk(case["text"])
            correct = predicted == case["expected_action_risk"]
            if correct:
                action_risk_correct += 1
            entry["action_risk_expected"] = case["expected_action_risk"]
            entry["action_risk_predicted"] = predicted
            entry["action_risk_correct"] = correct

        per_case.append(entry)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "overall": {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn,
        },
        "action_risk_classification_accuracy": round(action_risk_correct / action_risk_total, 3) if action_risk_total else None,
        "total_cases": len(corpus),
        "per_case": per_case,
        "note": (
            "This corpus intentionally includes 'hard negative' cases (e.g. NEG-03) "
            "that the current PAN regex is known to false-positive on, since it has no "
            "negative-context suppression yet. This is a documented, honest limitation — "
            "see KAVACH_LIMITATIONS.md item #2 — not a hidden failure."
        ),
    }
