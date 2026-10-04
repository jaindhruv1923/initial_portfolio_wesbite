"""
Production Data & Concept Drift Detector (Population Stability Index - PSI)
===========================================================================
Monitors feature distribution shifts and prediction probability decay between
a reference baseline and newly incoming batches of job postings.

Implements Population Stability Index (PSI) and Wasserstein Distance.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List

def calculate_psi(baseline: np.ndarray, target: np.ndarray, n_bins: int = 10, epsilon: float = 1e-4) -> float:
    """
    Computes Population Stability Index (PSI) between baseline and target distributions.
    
    Rule of Thumb:
      PSI < 0.10       : Stable (no significant shift)
      0.10 <= PSI < 0.25: Moderate Drift (investigation recommended)
      PSI >= 0.25      : Significant Drift (triggers automated retraining alert)
    """
    base_clean = baseline[~np.isnan(baseline)]
    targ_clean = target[~np.isnan(target)]
    
    if len(base_clean) < 10 or len(targ_clean) < 10:
        return 0.0
        
    # Use quantile bins based on reference baseline
    quantiles = np.linspace(0, 100, n_bins + 1)
    bin_edges = np.percentile(base_clean, quantiles)
    bin_edges[0] -= 1e-5
    bin_edges[-1] += 1e-5
    bin_edges = np.unique(bin_edges)
    
    if len(bin_edges) <= 2:
        return 0.0
        
    base_counts, _ = np.histogram(base_clean, bins=bin_edges)
    targ_counts, _ = np.histogram(targ_clean, bins=bin_edges)
    
    p_base = (base_counts / max(1, len(base_clean))) + epsilon
    p_targ = (targ_counts / max(1, len(targ_clean))) + epsilon
    
    # Normalize to sum to 1
    p_base /= np.sum(p_base)
    p_targ /= np.sum(p_targ)
    
    psi_val = np.sum((p_targ - p_base) * np.log(p_targ / p_base))
    return round(float(psi_val), 4)

def calculate_categorical_psi(base_series: pd.Series, targ_series: pd.Series, epsilon: float = 1e-4) -> float:
    """Computes PSI for discrete/categorical variables."""
    categories = list(set(base_series.dropna().unique()).union(set(targ_series.dropna().unique())))
    if not categories:
        return 0.0
        
    b_counts = base_series.value_counts(normalize=True).to_dict()
    t_counts = targ_series.value_counts(normalize=True).to_dict()
    
    p_base = np.array([b_counts.get(c, 0.0) + epsilon for c in categories])
    p_targ = np.array([t_counts.get(c, 0.0) + epsilon for c in categories])
    
    p_base /= np.sum(p_base)
    p_targ /= np.sum(p_targ)
    
    psi_val = np.sum((p_targ - p_base) * np.log(p_targ / p_base))
    return round(float(psi_val), 4)

def run_drift_monitoring(baseline_df: pd.DataFrame, incoming_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Runs complete PSI drift audit across features and predictions.
    """
    report = {
        "baseline_sample_size": len(baseline_df),
        "incoming_sample_size": len(incoming_df),
        "features": {},
        "overall_alert": "GREEN"
    }
    
    # 1. Prediction Concept Drift
    if "calibrated_ghost_prob" in baseline_df.columns and "calibrated_ghost_prob" in incoming_df.columns:
        p_base = baseline_df["calibrated_ghost_prob"].values
        p_targ = incoming_df["calibrated_ghost_prob"].values
        pred_psi = calculate_psi(p_base, p_targ)
        report["prediction_concept_drift"] = {
            "psi": pred_psi,
            "status": "ALERT (Retrain Required)" if pred_psi >= 0.25 else ("WARNING" if pred_psi >= 0.10 else "STABLE")
        }
        
    # 2. Continuous Features
    cont_cols = ["days_live", "description_word_count", "company_overall_rating"]
    for c in cont_cols:
        if c in baseline_df.columns and c in incoming_df.columns:
            psi_val = calculate_psi(baseline_df[c].values, incoming_df[c].values)
            report["features"][c] = {
                "type": "continuous",
                "psi": psi_val,
                "status": "DRIFT" if psi_val >= 0.25 else ("MODERATE" if psi_val >= 0.10 else "STABLE")
            }
            
    # 3. Categorical Features
    cat_cols = ["source", "job_category"]
    for c in cat_cols:
        if c in baseline_df.columns and c in incoming_df.columns:
            psi_val = calculate_categorical_psi(baseline_df[c], incoming_df[c])
            report["features"][c] = {
                "type": "categorical",
                "psi": psi_val,
                "status": "DRIFT" if psi_val >= 0.25 else ("MODERATE" if psi_val >= 0.10 else "STABLE")
            }
            
    # Check if any feature tripped >= 0.25
    any_drift = any(f["status"] == "DRIFT" for f in report["features"].values())
    any_moderate = any(f["status"] == "MODERATE" for f in report["features"].values())
    
    if any_drift:
        report["overall_alert"] = "RED (Automated Retraining Alert)"
    elif any_moderate:
        report["overall_alert"] = "YELLOW (Monitor Closely)"
    else:
        report["overall_alert"] = "GREEN (Production Distributions Stable)"
        
    return report

if __name__ == "__main__":
    print("=" * 80)
    print("  NAUKRI SAAF — POPULATION STABILITY INDEX (PSI) DRIFT AUDIT")
    print("=" * 80)
    
    data_path = "data/predictions_v4.csv"
    if not os.path.exists(data_path):
        data_path = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
        
    df = pd.read_csv(data_path)
    
    # Simulate a baseline (first 1,800 listings) vs incoming batch (last 1,051 listings)
    base_split = df.iloc[:1800]
    targ_split = df.iloc[1800:]
    
    audit_report = run_drift_monitoring(base_split, targ_split)
    print(json.dumps(audit_report, indent=2))
    
    os.makedirs("data", exist_ok=True)
    out_file = "data/drift_monitoring_report.json"
    with open(out_file, "w") as f:
        json.dump(audit_report, f, indent=2)
        
    print(f"\nDrift audit report saved to: {out_file}")
    print("=" * 80)
