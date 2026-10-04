"""
Evaluation Benchmark: Autonomous Agent vs. Supervised ML Model Alone
=====================================================================
Benchmarks the Multi-Tool Verification Agent against the Pure Supervised
ML Model on the 180 Holdout Gold Standard Listings.

Produces rigorous quantitative comparison (F1, Precision, Recall, Accuracy,
Cohen's Kappa) and exports `data/agent_benchmark_results.csv`.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, Any

sys.path.insert(0, os.path.abspath("."))

from src.agent.verifier import ListingVerificationAgent

def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    
    acc = (tp + tn) / max(1, len(y_true))
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2.0 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
    
    # Cohen's Kappa
    po = acc
    p_true = np.mean(y_true == 1)
    p_pred = np.mean(y_pred == 1)
    pe = (p_true * p_pred) + ((1.0 - p_true) * (1.0 - p_pred))
    kappa = (po - pe) / (1.0 - pe) if pe < 1.0 else 1.0
    
    return {
        "Accuracy": round(float(acc), 4),
        "F1 Score": round(float(f1), 4),
        "Precision": round(float(prec), 4),
        "Recall": round(float(rec), 4),
        "Cohen's Kappa": round(float(kappa), 4)
    }

def run_agent_benchmark():
    print("=" * 80)
    print("  NAUKRI SAAF — AGENT BENCHMARK ON 180 HOLDOUT GOLD LISTINGS")
    print("=" * 80)
    
    gold_path = "data/gold_labeling_sheet.csv"
    raw_path = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
    
    df_gold = pd.read_csv(gold_path)
    df_raw = pd.read_csv(raw_path)
    
    merged = df_gold.merge(df_raw, on="listing_id", suffixes=("", "_raw"))
    y_true = merged["gold_label"].astype(int).values
    
    agent = ListingVerificationAgent()
    
    agent_preds = []
    ml_preds = []
    sample_reports = []
    
    print(f"Running agentic multi-tool investigation across {len(merged)} holdout listings...")
    
    for idx, row in merged.iterrows():
        job_dict = row.to_dict()
        res = agent.investigate(job_dict)
        
        # Agent prediction: 1 if Ghost or Suspect with prob >= 0.50
        is_agent_ghost = 1 if res["agent_verdict"] == "Ghost" or (res["agent_verdict"] == "Suspect" and res["calibrated_ml_prob"] >= 0.50) else 0
        agent_preds.append(is_agent_ghost)
        
        # Pure ML model prediction
        is_ml_ghost = 1 if res["calibrated_ml_prob"] >= 0.50 else 0
        ml_preds.append(is_ml_ghost)
        
        if idx in [10, 45, 90]:
            sample_reports.append(res)
            
    agent_arr = np.array(agent_preds)
    ml_arr = np.array(ml_preds)
    
    m_agent = compute_metrics(y_true, agent_arr)
    m_agent["System"] = "Listing Verification Agent (Multi-Tool)"
    
    m_ml = compute_metrics(y_true, ml_arr)
    m_ml["System"] = "Calibrated Random Forest (Model Alone)"
    
    bench_df = pd.DataFrame([m_agent, m_ml])[["System", "F1 Score", "Recall", "Precision", "Accuracy", "Cohen's Kappa"]]
    
    print("\n--- Quantitative Benchmark on 180 Gold Standard Listings ---")
    print(bench_df.to_string(index=False))
    
    os.makedirs("data", exist_ok=True)
    out_path = "data/agent_benchmark_results.csv"
    bench_df.to_csv(out_path, index=False)
    print(f"\nBenchmark results saved to: {out_path}")
    
    print("\n" + "=" * 80)
    print("  EXEMPLAR AGENT FORENSIC REPORT")
    print("=" * 80)
    eg = sample_reports[0]
    print(f"Listing ID     : {eg['listing_id']}")
    print(f"Company        : {eg['company_name']}")
    print(f"Job Title      : {eg['job_title']}")
    print(f"Verdict        : {eg['agent_verdict']} (Confidence: {eg['confidence']})")
    print(f"ML Calibrated  : {eg['calibrated_ml_prob']*100:.1f}%")
    print("Cited Evidence :")
    for b in eg["evidence_bullets"]:
        print(f"  * {b}")
    print(f"Actionable Advice : {eg['actionable_advice']}")
    print("=" * 80)

if __name__ == "__main__":
    run_agent_benchmark()
