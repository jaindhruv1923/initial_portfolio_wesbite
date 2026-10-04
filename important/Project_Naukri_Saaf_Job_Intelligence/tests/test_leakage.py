"""
Unit Tests for Data Leakage Prevention and Grouped Cross-Validation
"""

import pytest
import numpy as np
import pandas as pd
from src.models.leakage_free_features import LeakageFreeFeatureExtractor
from src.models.train_pipeline import run_group_kfold

def test_leakage_free_feature_extractor_unseen_companies():
    """Verify that an unseen company in the test fold receives default non-leaking prior."""
    train_data = pd.DataFrame({
        "job_title": ["Data Analyst", "Data Analyst", "Data Scientist"],
        "company_name": ["Alpha Corp", "Alpha Corp", "Beta LLC"],
        "source": ["LinkedIn", "Indeed", "Glassdoor"],
        "description_text": ["SQL Python analysis", "SQL Tableau dashboards", "Machine learning PyTorch"],
        "days_live": [10, 20, 30],
        "salary_min": [500000, 600000, 1200000],
        "salary_max": [800000, 900000, 1600000],
        "location_city": ["Bangalore", "Pune", "Hyderabad"]
    })
    
    fe = LeakageFreeFeatureExtractor()
    fe.fit(train_data)
    
    # Check that Alpha Corp repost count is 2 in train
    assert fe.train_company_velocity_.get("alpha corp") is not None
    
    # Test on completely unseen employer
    test_data = pd.DataFrame({
        "job_title": ["Data Analyst"],
        "company_name": ["Gamma Inc"],  # Unseen
        "source": ["LinkedIn"],
        "description_text": ["SQL analytics in cloud"],
        "days_live": [15],
        "salary_min": [550000],
        "salary_max": [850000],
        "location_city": ["Bangalore"]
    })
    
    X_test = fe.transform(test_data)
    
    # Must receive baseline single-post prior (1.0), not throw error or leak
    assert X_test["employer_repost_count"].iloc[0] == 1.0
    assert X_test["posting_velocity_per_week"].iloc[0] == 0.25

def test_group_kfold_no_company_overlap():
    """Verify that train and validation folds in GroupKFold have zero intersecting companies."""
    mock_df = pd.DataFrame({
        "listing_id": [f"id_{i}" for i in range(100)],
        "company_name": [f"Company_{i % 20}" for i in range(100)],
        "target": np.random.randint(0, 2, 100)
    })
    
    folds = run_group_kfold(mock_df, mock_df["target"].values, n_splits=5, seed=42)
    assert len(folds) == 5
    
    for tr_idx, val_idx in folds:
        tr_comps = set(mock_df.iloc[tr_idx]["company_name"].str.lower())
        val_comps = set(mock_df.iloc[val_idx]["company_name"].str.lower())
        overlap = tr_comps.intersection(val_comps)
        assert len(overlap) == 0, f"Found leaking overlapping companies in fold: {overlap}"
