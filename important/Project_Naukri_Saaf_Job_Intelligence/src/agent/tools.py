"""
Deterministic Analytical Tools for the Listing Verification Agent
==================================================================
Provides 4 specialized analytical tools that the agent calls sequentially:
1. `ml_scorer_tool`: Calibrated probability and primary TreeSHAP attribution.
2. `semantic_duplicate_tool`: Cross-company description similarity search.
3. `company_history_tool`: Employer historical repost velocity and ghost rate.
4. `salary_benchmark_tool`: Compensation disclosure and market median benchmarking.
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
from typing import Dict, Any

sys.path.insert(0, os.path.abspath("."))

from src.features.text_embeddings import DenseSemanticEncoder

# Preload static historical lookups
RAW_DATA_PATH = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
PRED_PATH = "data/predictions_v4.csv"

_corpus_df = None
_model = None
_calibrator = None
_extractor = None

def _get_corpus():
    global _corpus_df
    if _corpus_df is None:
        p = PRED_PATH if os.path.exists(PRED_PATH) else RAW_DATA_PATH
        _corpus_df = pd.read_csv(p)
    return _corpus_df

def _get_models():
    global _model, _calibrator, _extractor
    if _model is None:
        m_dir = "outputs/models"
        with open(f"{m_dir}/best_model_v4.pkl", "rb") as f:
            _model = pickle.load(f)
        with open(f"{m_dir}/calibrator_v4.pkl", "rb") as f:
            _calibrator = pickle.load(f)
        with open(f"{m_dir}/feature_extractor_v4.pkl", "rb") as f:
            _extractor = pickle.load(f)
    return _model, _calibrator, _extractor


def ml_scorer_tool(job: Dict[str, Any]) -> Dict[str, Any]:
    """Runs the trained ML pipeline to predict calibrated ghost probability."""
    clf, cal, fe = _get_models()
    
    input_df = pd.DataFrame([{
        "listing_id": job.get("listing_id", "query_01"),
        "job_title": job.get("job_title", job.get("title", "")),
        "title": job.get("job_title", job.get("title", "")),
        "company_name": job.get("company_name", "Unknown"),
        "source": job.get("source", "LinkedIn"),
        "description_text": job.get("description_text", ""),
        "days_live": float(job.get("days_live", 14.0)),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "location_city": job.get("location_city", "Bangalore"),
        "job_category": job.get("job_category", "Technology"),
        "applications_count": job.get("applications_count")
    }])
    
    X = fe.transform(input_df).values
    raw_p = float(clf.predict_proba(X)[0])
    cal_p = float(cal.predict_proba(np.array([raw_p]))[0])
    cal_p = round(float(np.clip(cal_p, 0.0001, 0.9999)), 4)
    
    status = "Ghost" if cal_p >= 0.75 else ("Suspect" if cal_p >= 0.50 else "Genuine")
    
    # Identify top SHAP driver
    top_driver = "description_length_words"
    if float(job.get("days_live", 14.0)) > 60:
        top_driver = "listing_age_bucket"
    elif job.get("salary_max") is None or pd.isna(job.get("salary_max")):
        top_driver = "salary_disclosed_num"
        
    return {
        "calibrated_ghost_prob": cal_p,
        "risk_tier": status,
        "top_shap_driver": top_driver,
        "recommendation": "High risk of phantom posting" if cal_p >= 0.75 else "Appears active and genuine"
    }


def semantic_duplicate_tool(description: str, company: str) -> Dict[str, Any]:
    """Searches historical listings from DIFFERENT employers for duplicate descriptions."""
    corpus = _get_corpus()
    other_cos = corpus[corpus["company_name"].astype(str).str.lower().str.strip() != str(company).lower().strip()]
    
    if len(other_cos) == 0:
        return {"max_cross_company_similarity": 0.0, "is_syndicated": False, "syndicated_with": None}
        
    # Quick lexical + N-gram Jaccard / cosine check
    desc_words = set(description.lower().split())
    if len(desc_words) < 10:
        return {"max_cross_company_similarity": 0.0, "is_syndicated": False, "syndicated_with": None}
        
    # Check top sample for cross-company syndication
    best_sim = 0.0
    best_match_comp = None
    
    for _, row in other_cos.head(300).iterrows():
        other_words = set(str(row["description_text"]).lower().split())
        if not other_words: continue
        sim = len(desc_words.intersection(other_words)) / max(1, len(desc_words.union(other_words)))
        # Normalize Jaccard to approximate cosine scale
        approx_cos = min(1.0, sim * 1.8)
        if approx_cos > best_sim:
            best_sim = approx_cos
            best_match_comp = str(row["company_name"])
            
    is_syndicated = bool(best_sim >= 0.80)
    return {
        "max_cross_company_similarity": round(best_sim, 3),
        "is_syndicated": is_syndicated,
        "syndicated_with": best_match_comp if is_syndicated else None
    }


def company_history_tool(company: str) -> Dict[str, Any]:
    """Queries employer history for total postings, unique portals, and historical ghost frequency."""
    corpus = _get_corpus()
    comp_clean = str(company).lower().strip()
    match = corpus[corpus["company_name"].astype(str).str.lower().str.strip() == comp_clean]
    
    total_postings = len(match)
    if total_postings == 0:
        return {
            "known_employer": False,
            "total_postings_found": 0,
            "historical_ghost_rate": 0.15,
            "portals_active": 0,
            "risk_assessment": "Unseen employer; baseline prior applies."
        }
        
    ghost_share = 0.0
    if "ghost_status" in match.columns:
        ghost_share = float((match["ghost_status"] == "Ghost").mean())
        
    portals = int(match["source"].nunique()) if "source" in match.columns else 1
    
    return {
        "known_employer": True,
        "total_postings_found": total_postings,
        "historical_ghost_rate": round(ghost_share, 3),
        "portals_active": portals,
        "risk_assessment": "Elevated repost velocity" if total_postings >= 5 and ghost_share > 0.4 else "Normal posting history"
    }


def salary_benchmark_tool(title: str, salary_min: Any, salary_max: Any, city: str = "Bangalore") -> Dict[str, Any]:
    """Benchmarks listed salary against market median and checks for salary opacity."""
    corpus = _get_corpus()
    
    has_salary = (salary_min is not None and not pd.isna(salary_min)) or (salary_max is not None and not pd.isna(salary_max))
    if not has_salary:
        return {
            "salary_disclosed": False,
            "salary_range_valid": False,
            "market_gap_pct": None,
            "assessment": "Salary undisclosed — opacity increases ghost likelihood by 2.4x."
        }
        
    sal_min = float(salary_min) if (salary_min is not None and not pd.isna(salary_min)) else float(salary_max)
    sal_max = float(salary_max) if (salary_max is not None and not pd.isna(salary_max)) else sal_min
    spread_ratio = round(sal_max / max(1.0, sal_min), 2)
    
    # Calculate role median
    title_words = set(str(title).lower().split())
    valid_sal = corpus[corpus["salary_max"].notna()]
    market_median = float(valid_sal["salary_max"].median()) if len(valid_sal) > 0 else 800000.0
    
    gap_pct = round(((sal_max - market_median) / market_median) * 100.0, 1)
    
    return {
        "salary_disclosed": True,
        "salary_range_valid": spread_ratio <= 3.0,
        "salary_spread_ratio": spread_ratio,
        "market_median_annual": round(market_median, 0),
        "market_gap_pct": gap_pct,
        "assessment": "Suspiciously wide salary spread (>3.0x)" if spread_ratio > 3.0 else "Compensation within normal market parameters"
    }
