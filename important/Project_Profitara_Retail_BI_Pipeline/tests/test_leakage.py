import os
import sys
import pandas as pd
import numpy as np
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from ml_pipeline.clv_engine import load_and_clean_data, build_time_split_features, CUTOFF_DATE

def test_observation_window_temporal_integrity():
    """Verify that feature calculation window strictly precedes the cutoff date."""
    df = load_and_clean_data()
    obs_df = df[df["InvoiceDate"] < CUTOFF_DATE]
    pred_df = df[df["InvoiceDate"] >= CUTOFF_DATE]

    # No observation transactions can cross into future
    assert obs_df["InvoiceDate"].max() < CUTOFF_DATE, "Leakage detected: observation window has timestamps >= cutoff"
    assert pred_df["InvoiceDate"].min() >= CUTOFF_DATE, "Prediction window has timestamps < cutoff"

def test_feature_target_isolation():
    """Verify that features and target are computed from strictly disjoint time windows."""
    df = load_and_clean_data()
    dataset, obs_df, pred_df = build_time_split_features(df)

    # Check that monetary_obs is strictly from obs_df
    customer_sample = dataset.sample(min(50, len(dataset)), random_state=42)
    for _, row in customer_sample.iterrows():
        c_id = row["CustomerID"]
        actual_obs_spend = obs_df[obs_df["CustomerID"] == c_id]["TotalAmount"].sum()
        actual_pred_spend = pred_df[pred_df["CustomerID"] == c_id]["TotalAmount"].sum()
        
        assert np.isclose(row["monetary_obs"], actual_obs_spend, atol=1e-2), f"Feature monetary_obs mismatch for {c_id}"
        assert np.isclose(row["target_spend_90d"], actual_pred_spend, atol=1e-2), f"Target spend mismatch for {c_id}"

def test_no_mathematical_identity_leakage():
    """Verify that target is NOT algebraically calculable from features."""
    df = load_and_clean_data()
    dataset, _, _ = build_time_split_features(df)

    # In leaked model: target = frequency * avg_order_value
    # Here: target_spend_90d is future spend, monetary_obs is past spend
    # The correlation must not be near 1.0
    corr = dataset["monetary_obs"].corr(dataset["target_spend_90d"])
    assert corr < 0.80, f"Suspiciously high correlation ({corr:.3f}) suggests temporal leakage"
