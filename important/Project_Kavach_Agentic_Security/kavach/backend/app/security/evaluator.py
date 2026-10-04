"""
Kavach security engine evaluation.

Runs the test corpus (data/test_corpus.json) through
detect_pii() and computes precision, recall, and F1 — overall and per category.
"""

import json
import os

from app.security.detector import detect_pii

CORPUS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "test_corpus.json")


def load_corpus() -> list[dict]:
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate() -> dict:
    corpus = load_corpus()
    per_category: dict[str, dict[str, int]] = {}
    overall = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}

    for case in corpus:
        cat = case.get("entity_type") or "safe"

        per_category.setdefault(cat, {"tp": 0, "fp": 0, "fn": 0, "tn": 0})

        findings = detect_pii(case["text"])
        flagged = len(findings) > 0
        actually_sensitive = case["sensitive"]

        if actually_sensitive and flagged:
            per_category[cat]["tp"] += 1
            overall["tp"] += 1
        elif actually_sensitive and not flagged:
            per_category[cat]["fn"] += 1
            overall["fn"] += 1
        elif not actually_sensitive and flagged:
            per_category[cat]["fp"] += 1
            overall["fp"] += 1
        else:
            per_category[cat]["tn"] += 1
            overall["tn"] += 1

    def compute_metrics(counts: dict[str, int]) -> dict:
        tp, fp, fn = counts["tp"], counts["fp"], counts["fn"]
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        return {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": counts["tn"],
        }

    result = {
        "overall": compute_metrics(overall),
        "per_category": {cat: compute_metrics(counts) for cat, counts in per_category.items() if cat != "safe"},
        "total_cases": len(corpus),
    }
    return result

