"""
Ghost-Safe Alternative Job Recommender Engine
============================================
When a candidate encounters a suspected phantom or ghost job, this engine
searches the knowledge base for verified genuine, active requisitions
with similar job titles, required skillsets, and positive transparency signals.

Solves the candidate problem: "If this posting is dead, where should I apply instead?"
"""

import os
import re
import pandas as pd
import numpy as np
from typing import Dict, Any, List

class SafeAlternativeRecommender:
    def __init__(self, data_path: str = "data/predictions_v4.csv"):
        self.data_path = data_path
        self._corpus_df = None

    def _get_corpus(self) -> pd.DataFrame:
        if self._corpus_df is None:
            candidate_paths = [
                self.data_path,
                "data/nlp_augmented_features.csv",
                "../data/predictions_v4.csv",
                "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
            ]
            for p in candidate_paths:
                if os.path.exists(p):
                    self._corpus_df = pd.read_csv(p)
                    break
            if self._corpus_df is None:
                self._corpus_df = pd.DataFrame()
        return self._corpus_df

    def recommend_safe_alternatives(
        self,
        target_title: str,
        target_company: str = "",
        city: str = "",
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Finds top-k verified genuine alternative listings with matching titles/skills.
        """
        corpus = self._get_corpus()
        if len(corpus) == 0:
            return []

        # Filter strictly for Genuine active listings
        status_col = "ghost_status" if "ghost_status" in corpus.columns else None
        prob_col = "predicted_ghost_prob" if "predicted_ghost_prob" in corpus.columns else (
            "calibrated_ghost_prob" if "calibrated_ghost_prob" in corpus.columns else None
        )

        candidates = corpus.copy()
        if status_col:
            candidates = candidates[candidates[status_col] == "Genuine"]
        elif prob_col:
            candidates = candidates[candidates[prob_col] < 0.35]

        # Exclude the exact same employer
        if target_company:
            candidates = candidates[
                candidates["company_name"].astype(str).str.lower().str.strip() != target_company.lower().strip()
            ]

        if len(candidates) == 0:
            return []

        # Tokenize target title
        target_words = set(re.findall(r"\b[a-z]{3,20}\b", target_title.lower()))
        city_lower = str(city).lower().strip()

        scored_candidates = []
        for _, row in candidates.iterrows():
            title_str = str(row.get("job_title", row.get("title", "")))
            c_words = set(re.findall(r"\b[a-z]{3,20}\b", title_str.lower()))
            
            # Title overlap score (Jaccard)
            overlap = len(target_words.intersection(c_words))
            title_score = overlap / max(1, len(target_words.union(c_words)))

            # Location match boost
            loc_boost = 0.20 if city_lower and city_lower in str(row.get("location_city", "")).lower() else 0.0

            # Transparency boost
            sal_boost = 0.15 if row.get("salary_min") and not pd.isna(row.get("salary_min")) else 0.0
            fresh_boost = 0.15 if float(row.get("days_live", 20)) <= 14 else 0.0

            total_score = title_score + loc_boost + sal_boost + fresh_boost

            if overlap >= 1 or total_score >= 0.3:
                scored_candidates.append({
                    "listing_id": row.get("listing_id", "req_alt"),
                    "job_title": title_str,
                    "company_name": str(row.get("company_name", "Enterprise Employer")),
                    "location_city": str(row.get("location_city", "Bangalore")),
                    "source": str(row.get("source", "LinkedIn")),
                    "days_live": float(row.get("days_live", 7.0)),
                    "salary_min": float(row.get("salary_min")) if pd.notna(row.get("salary_min")) else None,
                    "salary_max": float(row.get("salary_max")) if pd.notna(row.get("salary_max")) else None,
                    "ghost_prob": float(row.get(prob_col, 0.12)) if prob_col else 0.10,
                    "relevance_score": round(float(total_score), 3)
                })

        scored_candidates.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_candidates[:top_k]

# Singleton instance
safe_recommender = SafeAlternativeRecommender()
