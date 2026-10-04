"""
Kavach security engine evaluation (Phase 4 / Phase 9 groundwork — see
docs/EVALUATION_PLAN.md).

Runs the multilingual test corpus (data/test_corpus.json) through
detect_pii() and computes precision, recall, and F1 — both overall and
per language — so claims about detection quality are backed by real
numbers rather than assertions (per EVALUATION_PLAN.md's core rule).

Definition used here: a test case counts as a "hit" if the detector found
at least one finding for a case labeled sensitive=true, and a "correct
rejection" if it found zero findings for a case labeled sensitive=false.
This is a message-level evaluation (did we flag the message at all), not
an entity-level evaluation (exact category/value match) — a reasonable
first pass; entity-level precision is a natural extension for Phase 9.
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
    per_language: dict[str, dict[str, int]] = {}
    overall = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}

    for case in corpus:
        lang = case["language"]
        per_language.setdefault(lang, {"tp": 0, "fp": 0, "fn": 0, "tn": 0})

        findings = detect_pii(case["text"])
        flagged = len(findings) > 0
        actually_sensitive = case["sensitive"]

        if actually_sensitive and flagged:
            per_language[lang]["tp"] += 1
            overall["tp"] += 1
        elif actually_sensitive and not flagged:
            per_language[lang]["fn"] += 1
            overall["fn"] += 1
        elif not actually_sensitive and flagged:
            per_language[lang]["fp"] += 1
            overall["fp"] += 1
        else:
            per_language[lang]["tn"] += 1
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
        "per_language": {lang: compute_metrics(counts) for lang, counts in per_language.items()},
        "total_cases": len(corpus),
    }
    return result
