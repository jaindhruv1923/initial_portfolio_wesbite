"""
Generative Label Model for Programmatic Weak Supervision
========================================================
Combines noisy, overlapping, and conflicting Labeling Functions (LFs) into
calibrated probabilistic training labels without ground truth.
Includes:
  1. LF Diagnostic Summary (Coverage, Overlaps, Conflicts)
  2. Majority Vote Baseline
  3. Dawid-Skene / Naive Bayes Generative Label Model
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple

ABSTAIN = -1
GENUINE = 0
GHOST = 1

def compute_lf_summary(L: np.ndarray, lf_names: list) -> pd.DataFrame:
    """Computes Coverage, Overlap, and Conflict statistics for each LF."""
    n_samples, n_lfs = L.shape
    stats = []
    
    for j in range(n_lfs):
        col = L[:, j]
        non_abstain = col != ABSTAIN
        coverage = np.mean(non_abstain)
        
        # Overlaps: fired together with another LF
        other_non_abstain = np.delete(L != ABSTAIN, j, axis=1).any(axis=1)
        overlap = np.mean(non_abstain & other_non_abstain)
        
        # Conflicts: fired opposite to another LF
        conflicts = 0
        for i in range(n_samples):
            if non_abstain[i]:
                vote = col[i]
                other_votes = np.delete(L[i, :], j)
                other_active = other_votes[other_votes != ABSTAIN]
                if len(other_active) > 0 and (other_active != vote).any():
                    conflicts += 1
        conflict_rate = conflicts / max(1, n_samples)
        
        # Positive / Negative breakdown
        pos_rate = np.mean(col == GHOST)
        neg_rate = np.mean(col == GENUINE)
        
        stats.append({
            "LF Name": lf_names[j],
            "Polarity": "Ghost (1)" if pos_rate > 0 and neg_rate == 0 else ("Genuine (0)" if neg_rate > 0 and pos_rate == 0 else "Both"),
            "Coverage": round(coverage, 4),
            "Overlaps": round(overlap, 4),
            "Conflicts": round(conflict_rate, 4),
            "Num Votes": int(np.sum(non_abstain))
        })
        
    summary_df = pd.DataFrame(stats)
    return summary_df


class MajorityVoteModel:
    """Baseline label aggregator using unweighted majority vote."""
    def __init__(self, prior: float = 0.25):
        self.prior = prior

    def predict_proba(self, L: np.ndarray) -> np.ndarray:
        n_samples = L.shape[0]
        probs = np.zeros(n_samples)
        
        for i in range(n_samples):
            row = L[i, :]
            pos_votes = np.sum(row == GHOST)
            neg_votes = np.sum(row == GENUINE)
            total = pos_votes + neg_votes
            
            if total == 0:
                probs[i] = self.prior
            else:
                probs[i] = pos_votes / total
                
        return probs

    def predict(self, L: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(L) >= threshold).astype(int)


class GenerativeLabelModel:
    """
    Snorkel-style Generative Label Model.
    Computes class-conditional emission probabilities P(Lambda_j = v | Y = y)
    and estimates optimal log-likelihood ratio weights:
       w_j = log( P(Lambda_j = v | Y = 1) / P(Lambda_j = v | Y = 0) )
    Produces calibrated posterior probabilities P(Y = 1 | L).
    """
    def __init__(self, n_lfs: int, prior: float = 0.293, max_iter: int = 25, tol: float = 1e-4):
        self.n_lfs = n_lfs
        self.prior = prior
        self.max_iter = max_iter
        self.tol = tol
        self.weights = np.zeros(n_lfs)

    def fit(self, L: np.ndarray) -> "GenerativeLabelModel":
        n_samples, n_lfs = L.shape
        
        # 1. Consensus initial pseudo-labels from majority vote
        pos_votes = np.sum(L == GHOST, axis=1)
        neg_votes = np.sum(L == GENUINE, axis=1)
        total_votes = pos_votes + neg_votes
        
        q = np.where(total_votes > 0, pos_votes / np.maximum(total_votes, 1), self.prior)
        q = np.clip(q, 0.05, 0.95)

        # 2. EM Iteration to estimate conditional emission probabilities
        for iteration in range(self.max_iter):
            prev_weights = self.weights.copy()
            sum_q = np.sum(q)
            sum_not_q = np.sum(1.0 - q)
            
            for j in range(n_lfs):
                col = L[:, j]
                pos_mask = col == GHOST
                neg_mask = col == GENUINE
                
                if np.sum(pos_mask) > 0:
                    p_v1_given_1 = (np.sum(q[pos_mask]) + 1e-3) / (sum_q + 2e-3)
                    p_v1_given_0 = (np.sum((1.0 - q)[pos_mask]) + 1e-3) / (sum_not_q + 2e-3)
                    self.weights[j] = np.log(p_v1_given_1 / p_v1_given_0)
                elif np.sum(neg_mask) > 0:
                    p_v0_given_0 = (np.sum((1.0 - q)[neg_mask]) + 1e-3) / (sum_not_q + 2e-3)
                    p_v0_given_1 = (np.sum(q[neg_mask]) + 1e-3) / (sum_q + 2e-3)
                    self.weights[j] = -np.log(p_v0_given_0 / p_v0_given_1)
                else:
                    self.weights[j] = 0.0
                    
            # E-step: update q
            q = self.predict_proba(L)
            
            if np.max(np.abs(self.weights - prev_weights)) < self.tol:
                break
                
        return self

    def predict_proba(self, L: np.ndarray) -> np.ndarray:
        n_samples, n_lfs = L.shape
        logit_0 = np.log(self.prior / (1.0 - self.prior))
        
        scores = np.zeros(n_samples)
        for j in range(n_lfs):
            active = L[:, j] != ABSTAIN
            scores[active] += self.weights[j]
            
        total_logit = logit_0 + scores
        probs = np.where(
            total_logit >= 0,
            1.0 / (1.0 + np.exp(-total_logit)),
            np.exp(total_logit) / (1.0 + np.exp(total_logit))
        )
        return probs

    def predict(self, L: np.ndarray, threshold: float = 0.50) -> np.ndarray:
        return (self.predict_proba(L) >= threshold).astype(int)


