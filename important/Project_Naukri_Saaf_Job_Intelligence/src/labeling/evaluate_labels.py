"""
Weak Supervision Execution & Gold Set Evaluation Engine
======================================================
1. Runs all 10 Labeling Functions across the full 2,851 dataset.
2. Computes and displays the programmatic LF summary (Coverage, Overlap, Conflict).
3. Fits the Generative Label Model and Majority Vote baseline.
4. If human gold annotations are present in `data/gold_labeling_sheet.csv`,
   calculates Cohen's Kappa, Precision, Recall, F1, and AUC against ground truth.
"""

import os
import sys
import argparse

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath("."))

import pandas as pd
import numpy as np
from sklearn.metrics import (
    cohen_kappa_score, accuracy_score, precision_score,
    recall_score, f1_score, roc_auc_score
)

from src.labeling.labeling_functions import apply_lfs, LF_NAMES, LABELING_FUNCTIONS, ABSTAIN, GHOST, GENUINE
from src.labeling.label_model import compute_lf_summary, MajorityVoteModel, GenerativeLabelModel


def run_weak_supervision(
    dataset_path: str = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv",
    output_labels_path: str = "data/weak_supervision_labels.csv",
    gold_sheet_path: str = "data/gold_labeling_sheet.csv"
):
    print("=" * 75)
    print("  NAUKRI SAAF — PROGRAMMATIC WEAK SUPERVISION PIPELINE (SNORKEL PARADIGM)")
    print("=" * 75)
    
    df = pd.read_csv(dataset_path)
    print(f"Loaded {len(df):,} listings from {dataset_path}")
    
    # Apply LFs
    print("\n[Step 1/4] Evaluating 10 Domain-Heuristic Labeling Functions...")
    L = apply_lfs(df)
    
    # Compute summary
    summary_df = compute_lf_summary(L, LF_NAMES)
    print("\n--- Programmatic LF Diagnostic Summary ---")
    print(summary_df.to_string(index=False))
    
    total_covered = np.mean((L != ABSTAIN).any(axis=1)) * 100
    avg_lfs_per_row = np.mean((L != ABSTAIN).sum(axis=1))
    print(f"\nOverall LF Dataset Coverage: {total_covered:.1f}% ({int(total_covered/100*len(df)):,}/{len(df):,} listings)")
    print(f"Average Active LFs per Listing: {avg_lfs_per_row:.2f}")
    
    # Fit Label Models
    print("\n[Step 2/4] Training Generative Label Model (Expectation-Maximization)...")
    gen_model = GenerativeLabelModel(n_lfs=len(LABELING_FUNCTIONS), prior=0.28)
    gen_model.fit(L)
    gen_probs = gen_model.predict_proba(L)
    gen_labels = gen_model.predict(L, threshold=0.5)
    
    mv_model = MajorityVoteModel(prior=0.28)
    mv_probs = mv_model.predict_proba(L)
    mv_labels = mv_model.predict(L, threshold=0.5)
    
    # Save weak labels
    out_df = pd.DataFrame({
        "listing_id": df["listing_id"],
        "source": df["source"],
        "job_title": df["job_title"],
        "company_name": df["company_name"],
        "legacy_rule_label": df.get("ghost_label", np.nan),
        "weak_prob_ghost": gen_probs.round(4),
        "weak_label_ghost": gen_labels,
        "mv_prob_ghost": mv_probs.round(4),
        "mv_label_ghost": mv_labels,
        "lf_active_count": (L != ABSTAIN).sum(axis=1)
    })
    
    os.makedirs(os.path.dirname(output_labels_path), exist_ok=True)
    out_df.to_csv(output_labels_path, index=False)
    print(f"\n[Step 3/4] Saved calibrated weak labels to: {output_labels_path}")
    print(f"Generative Model Ghost Rate: {gen_labels.mean()*100:.1f}% ({gen_labels.sum():,} flagged)")
    print(f"Majority Vote Model Ghost Rate: {mv_labels.mean()*100:.1f}% ({mv_labels.sum():,} flagged)")
    
    # Evaluate on Gold Ground Truth if available
    print("\n[Step 4/4] Checking Human-Annotated Gold Set Status...")
    if not os.path.exists(gold_sheet_path):
        print(f"  Gold sheet not found at {gold_sheet_path}. Run sample_gold_set.py first.")
        return
        
    gold_df = pd.read_csv(gold_sheet_path)
    # Check non-empty annotations
    annotated = gold_df["gold_label"].astype(str).str.strip()
    valid_mask = annotated.isin(["0", "1", "0.0", "1.0"])
    
    n_annotated = valid_mask.sum()
    print(f"  Gold sheet rows: {len(gold_df)} total | Valid human annotations found: {n_annotated}")
    
    if n_annotated < 30:
        print("\n" + "!" * 75)
        print("  NOTICE: Gold set is currently unannotated (or < 30 entries labeled).")
        print("  Please open `data/gold_labeling_sheet.csv` and enter 0 (Genuine) or 1 (Ghost)")
        print("  for the 180 listings using the rubric in `data/ANNOTATION_GUIDE.md`.")
        print("  Once saved, re-run this script to calculate exact Cohen's Kappa and F1!")
        print("!" * 75)
        return summary_df, out_df, None

    # Proceed with Gold Set Benchmark
    gold_eval = gold_df[valid_mask].copy()
    y_true = gold_eval["gold_label"].astype(int).values
    eval_ids = gold_eval["listing_id"].values
    
    # Extract corresponding predictions
    sub_preds = out_df.set_index("listing_id").loc[eval_ids]
    
    results = []
    
    def calc_metrics(name, y_pred, y_prob=None):
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        kappa = cohen_kappa_score(y_true, y_pred)
        auc = roc_auc_score(y_true, y_prob) if y_prob is not None and len(np.unique(y_true)) > 1 else np.nan
        
        return {
            "Method / Model": name,
            "Cohen's Kappa": round(kappa, 4),
            "F1 Score": round(f1, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "Accuracy": round(acc, 4),
            "ROC-AUC": round(auc, 4) if pd.notna(auc) else "—"
        }
        
    # 1. Legacy Heuristic Rule Label
    if "_legacy_weak_label" in gold_eval.columns:
        y_leg = gold_eval["_legacy_weak_label"].fillna(0).astype(int).values
        results.append(calc_metrics("Legacy Heuristic Rule", y_leg))
        
    # 2. Majority Vote LFs
    y_mv = sub_preds["mv_label_ghost"].values
    p_mv = sub_preds["mv_prob_ghost"].values
    results.append(calc_metrics("Majority Vote Labeling", y_mv, p_mv))
    
    # 3. Generative Label Model (Snorkel)
    y_gen = sub_preds["weak_label_ghost"].values
    p_gen = sub_preds["weak_prob_ghost"].values
    results.append(calc_metrics("Generative Label Model (Snorkel)", y_gen, p_gen))
    
    # Compile benchmark table
    bench_df = pd.DataFrame(results).sort_values("F1 Score", ascending=False).reset_index(drop=True)
    bench_df.index += 1
    
    print("\n" + "=" * 75)
    print("  GOLD STANDARD BENCHMARK: WEAK LABELS VS. HUMAN GROUND TRUTH")
    print(f"  Evaluated on {n_annotated} hand-verified holdout listings")
    print("=" * 75)
    print(bench_df.to_string())
    
    eval_csv = "data/gold_evaluation_results.csv"
    bench_df.to_csv(eval_csv, index=False)
    print(f"\nSaved benchmark results to {eval_csv}")
    
    return summary_df, out_df, bench_df

if __name__ == "__main__":
    run_weak_supervision()
