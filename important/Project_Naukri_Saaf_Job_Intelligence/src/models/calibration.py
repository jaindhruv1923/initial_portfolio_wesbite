"""
Probability Calibration & Reliability Diagnostics (Platt Scaling)
================================================================
Fits sigmoid calibration P(Y=1 | f(x)) = sigmoid(A * f(x) + B) using
out-of-fold cross-validation predictions.
Computes Brier Score and Expected Calibration Error (ECE).
"""

import numpy as np
import pandas as pd

class PlattCalibrator:
    def __init__(self, max_iter: int = 150, lr: float = 0.05):
        self.max_iter = max_iter
        self.lr = lr
        self.a = 1.0
        self.b = 0.0

    def fit(self, probs: np.ndarray, y: np.ndarray) -> "PlattCalibrator":
        # Convert raw probabilities to log-odds (logits)
        eps = 1e-4
        p_clipped = np.clip(probs, eps, 1.0 - eps)
        logits = np.log(p_clipped / (1.0 - p_clipped))
        
        # Target optimization using gradient descent
        a, b = 1.0, 0.0
        n = len(y)
        for _ in range(self.max_iter):
            lin = a * logits + b
            p_cal = np.where(lin >= 0, 1.0 / (1.0 + np.exp(-lin)), np.exp(lin) / (1.0 + np.exp(lin)))
            err = p_cal - y
            
            da = np.mean(err * logits)
            db = np.mean(err)
            
            a -= self.lr * da
            b -= self.lr * db
            
        self.a = a
        self.b = b
        return self

    def predict_proba(self, probs: np.ndarray) -> np.ndarray:
        eps = 1e-4
        p_clipped = np.clip(probs, eps, 1.0 - eps)
        logits = np.log(p_clipped / (1.0 - p_clipped))
        lin = self.a * logits + self.b
        return np.where(lin >= 0, 1.0 / (1.0 + np.exp(-lin)), np.exp(lin) / (1.0 + np.exp(lin)))

def compute_calibration_metrics(y_true: np.ndarray, probs_raw: np.ndarray, probs_cal: np.ndarray) -> dict:
    brier_raw = np.mean((probs_raw - y_true)**2)
    brier_cal = np.mean((probs_cal - y_true)**2)
    
    # Expected Calibration Error (ECE) across 10 bins
    bins = np.linspace(0, 1, 11)
    ece_raw, ece_cal = 0.0, 0.0
    
    for i in range(len(bins) - 1):
        # Raw
        mask_r = (probs_raw >= bins[i]) & (probs_raw < bins[i+1])
        if np.sum(mask_r) > 0:
            acc_r = np.mean(y_true[mask_r])
            conf_r = np.mean(probs_raw[mask_r])
            ece_raw += (np.sum(mask_r) / len(y_true)) * np.abs(acc_r - conf_r)
            
        # Calibrated
        mask_c = (probs_cal >= bins[i]) & (probs_cal < bins[i+1])
        if np.sum(mask_c) > 0:
            acc_c = np.mean(y_true[mask_c])
            conf_c = np.mean(probs_cal[mask_c])
            ece_cal += (np.sum(mask_c) / len(y_true)) * np.abs(acc_c - conf_c)
            
    return {
        "Brier Score (Raw)": round(brier_raw, 4),
        "Brier Score (Calibrated)": round(brier_cal, 4),
        "Brier Improvement (%)": round((brier_raw - brier_cal) / brier_raw * 100, 2),
        "ECE (Raw)": round(ece_raw, 4),
        "ECE (Calibrated)": round(ece_cal, 4)
    }
