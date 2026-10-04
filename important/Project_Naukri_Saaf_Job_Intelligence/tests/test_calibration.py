"""
Unit Tests for Platt Probability Calibration and Calibration Metrics
"""

import pytest
import numpy as np
from src.models.calibration import PlattCalibrator, compute_calibration_metrics

def test_platt_calibrator_bounds_and_monotonicity():
    y_raw = np.array([0.05, 0.15, 0.35, 0.65, 0.85, 0.95])
    y_true = np.array([0, 0, 0, 1, 1, 1])
    
    cal = PlattCalibrator()
    cal.fit(y_raw, y_true)
    
    cal_probs = cal.predict_proba(y_raw)
    
    # 1. Bounds check: all in [0, 1]
    assert np.all(cal_probs >= 0.0)
    assert np.all(cal_probs <= 1.0)
    
    # 2. Monotonicity: higher raw risk produces higher calibrated risk
    assert np.all(np.diff(cal_probs) >= 0)

def test_calibration_metrics_brier_and_ece():
    y_true = np.array([0, 0, 1, 1])
    y_raw = np.array([0.1, 0.2, 0.8, 0.9])
    y_cal = np.array([0.05, 0.1, 0.9, 0.95])
    
    metrics = compute_calibration_metrics(y_true, y_raw, y_cal)
    assert "Brier Score (Raw)" in metrics
    assert "Brier Score (Calibrated)" in metrics
    assert "ECE (Raw)" in metrics
    assert "ECE (Calibrated)" in metrics
    assert metrics["Brier Score (Calibrated)"] < metrics["Brier Score (Raw)"]
