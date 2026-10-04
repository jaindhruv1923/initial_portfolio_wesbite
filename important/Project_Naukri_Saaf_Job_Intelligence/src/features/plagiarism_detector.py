"""
Cross-Company Job Description Plagiarism & Syndication Detector
================================================================
Identifies fake job aggregators and ghost listing syndicates by computing
cross-company semantic description overlap.

When two or more legally distinct companies post nearly identical descriptions
(cosine similarity >= 0.85), it strongly indicates:
1. Low-intent staffing agencies scraping and recycling job boards.
2. Phantom requisitions syndicated across multiple shell recruiter accounts.
3. Boilerplate job descriptions lifted from external career portals.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class CrossCompanyPlagiarismDetector:
    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold

    def detect(self, df: pd.DataFrame, embeddings: np.ndarray) -> pd.DataFrame:
        """
        Computes cross-company plagiarism metrics across all listings.
        
        Args:
            df: DataFrame containing at least 'listing_id' and 'company_name'.
            embeddings: Normalized (N, D) semantic embeddings matrix.
            
        Returns:
            DataFrame with columns:
              - listing_id
              - cross_company_max_sim
              - cross_company_plag_count
              - is_syndicated_description
              - most_similar_company
        """
        n_listings = len(df)
        companies = df["company_name"].astype(str).str.lower().str.strip().values
        listing_ids = df["listing_id"].values
        
        # Pairwise cosine similarity matrix (N, N)
        # Embeddings are already unit L2 normalized
        sim_matrix = np.dot(embeddings, embeddings.T)
        # Zero out self-diagonal
        np.fill_diagonal(sim_matrix, 0.0)
        
        max_sims = np.zeros(n_listings, dtype=np.float32)
        plag_counts = np.zeros(n_listings, dtype=np.int32)
        top_similar_companies = [""] * n_listings
        
        for i in range(n_listings):
            curr_comp = companies[i]
            # Mask out listings from the same company
            diff_comp_mask = (companies != curr_comp)
            
            if not np.any(diff_comp_mask):
                continue
                
            comp_sims = sim_matrix[i, diff_comp_mask]
            diff_comp_indices = np.where(diff_comp_mask)[0]
            
            best_idx_in_subset = np.argmax(comp_sims)
            best_sim = float(comp_sims[best_idx_in_subset])
            best_global_idx = diff_comp_indices[best_idx_in_subset]
            
            count_above = int(np.sum(comp_sims >= self.similarity_threshold))
            
            max_sims[i] = best_sim
            plag_counts[i] = count_above
            top_similar_companies[i] = str(companies[best_global_idx])
            
        results_df = pd.DataFrame({
            "listing_id": listing_ids,
            "cross_company_max_sim": np.round(max_sims, 4),
            "cross_company_plag_count": plag_counts,
            "is_syndicated_description": (max_sims >= self.similarity_threshold).astype(int),
            "most_similar_company": top_similar_companies
        })
        
        return results_df
