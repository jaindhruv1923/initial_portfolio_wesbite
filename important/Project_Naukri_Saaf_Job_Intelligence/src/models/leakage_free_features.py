"""
Leakage-Free Feature Engineering Transformer
============================================
Implements a strict scikit-learn BaseEstimator + TransformerMixin to ensure all
group-level and market-level statistics (repost velocity, multi-source presence,
and title median salaries) are calculated strictly on the training fold.
When transforming validation or test folds, unseen companies and titles default
to baseline priors, preventing data leakage across folds.
"""

import re
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

TIER1_CITIES = {
    "mumbai", "delhi", "bengaluru", "bangalore", "hyderabad", "chennai",
    "kolkata", "pune", "ahmedabad", "new delhi", "gurugram", "gurgaon", "noida"
}
TIER2_CITIES = {
    "jaipur", "lucknow", "kanpur", "nagpur", "indore", "thane", "bhopal",
    "visakhapatnam", "patna", "vadodara", "coimbatore", "surat", "nashik",
    "chandigarh", "kochi", "mysuru", "mysore", "gandhinagar"
}

EXP_MAP = {
    "Internship": 0, "Entry level": 1, "Associate": 2, "Mid-Senior level": 5,
    "Director": 10, "Executive": 15, "Not Applicable": 2,
}

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(?:\+91[\-\s]?)?[6-9]\d{9}\b")
URGENCY_TERMS = [
    "urgent", "immediate joining", "immediately", "walk-in", "walk in",
    "hiring fast", "apply now", "limited seats", "fast hire", "instant hire"
]

class LeakageFreeFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.feature_names_ = []
        # Learned statistics from train fold only
        self.train_repost_counts_ = {}
        self.train_company_velocity_ = {}
        self.train_multiplatform_keys_ = set()
        self.train_title_medians_ = {}
        self.train_overall_salary_median_ = 0.0

    def fit(self, X: pd.DataFrame, y=None):
        df = X.copy()
        
        # 1. Learn company + title repost counts strictly on train fold
        df["_key"] = df["company_name"].astype(str).str.lower().str.strip() + "||" + \
                     df["job_title"].astype(str).str.lower().str.strip()
        self.train_repost_counts_ = df["_key"].value_counts().to_dict()
        
        # 2. Learn company posting velocity strictly on train fold
        comp_clean = df["company_name"].astype(str).str.lower().str.strip()
        comp_counts = comp_clean.value_counts().to_dict()
        self.train_company_velocity_ = {k: round(v / 4.0, 2) for k, v in comp_counts.items()}
        
        # 3. Learn multiplatform duplicate keys strictly on train fold
        multi = df.groupby("_key")["source"].nunique()
        self.train_multiplatform_keys_ = set(multi[multi >= 2].index)
        
        # 4. Learn median salary by normalized role title strictly on train fold
        sal_mid = df[["salary_min", "salary_max"]].mean(axis=1)
        self.train_overall_salary_median_ = float(sal_mid.median()) if pd.notna(sal_mid.median()) else 500000.0
        
        valid_sal = df[sal_mid.notna()].copy()
        valid_sal["_sal_mid"] = sal_mid[sal_mid.notna()]
        title_norm = valid_sal["job_title"].astype(str).str.lower().str.strip()
        self.train_title_medians_ = valid_sal.groupby(title_norm)["_sal_mid"].median().to_dict()
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        feats = pd.DataFrame(index=df.index)
        
        # --- Base Text & Formatting Signals ---
        desc_text = df["description_text"].fillna("").astype(str)
        words = desc_text.apply(lambda t: len(t.split()))
        feats["description_length_words"] = words
        
        def calc_lex_div(t):
            w = re.findall(r"[a-zA-Z']+", str(t).lower())
            return round(len(set(w)) / len(w), 4) if len(w) >= 5 else 0.0
        feats["description_lexical_diversity"] = desc_text.apply(calc_lex_div)
        
        feats["contact_bypass_flag"] = desc_text.apply(
            lambda t: int(bool(EMAIL_RE.search(t)) or bool(PHONE_RE.search(t)))
        )
        
        feats["urgency_language_score"] = desc_text.apply(
            lambda t: sum(str(t).lower().count(term) for term in URGENCY_TERMS)
        )
        
        def check_remote_ambig(r):
            rt = str(r.get("remote_type", "")).lower()
            dt = str(r.get("description_text", "")).lower()
            claims = ("remote" in rt) or ("work from home" in rt) or ("remote" in dt)
            infra = any(k in dt for k in ["laptop provided", "vpn", "wfh setup", "equipment provided"])
            return int(claims and not infra)
        feats["remote_ambiguity_flag"] = df.apply(check_remote_ambig, axis=1)
        
        # --- Days Live & Age Buckets ---
        days = pd.to_numeric(df.get("days_live", 0), errors="coerce").fillna(0).clip(lower=0, upper=365)
        feats["days_live"] = days
        feats["desc_per_day"] = (words / (days + 1.0)).round(4)
        feats["listing_age_bucket"] = pd.cut(days, bins=[-1, 15, 60, 90, 999], labels=[0, 1, 2, 3]).astype(int)
        
        # --- Salary Disclosures & Ratios ---
        has_min = pd.to_numeric(df.get("salary_min", np.nan), errors="coerce")
        has_max = pd.to_numeric(df.get("salary_max", np.nan), errors="coerce")
        sal_disc = (has_min.notna() | has_max.notna()).astype(int)
        feats["salary_disclosed_num"] = sal_disc
        
        sal_min_val = has_min.fillna(0)
        sal_max_val = has_max.fillna(0)
        feats["salary_range_ratio"] = np.where(
            sal_min_val > 0,
            ((sal_max_val - sal_min_val) / sal_min_val.clip(lower=1)).round(3),
            3.0
        )
        
        # --- Company Transparency & Demographics ---
        company_fields = ["company_industry", "company_size_category", "company_employee_count", "company_revenue", "company_overall_rating"]
        present_cols = [c for c in company_fields if c in df.columns]
        if present_cols:
            feats["company_data_completeness_score"] = (df[present_cols].notna().sum(axis=1) / len(company_fields) * 100).round(1)
        else:
            feats["company_data_completeness_score"] = 0.0
            
        def get_city_tier(c):
            if pd.isna(c): return 3
            city = str(c).strip().lower()
            if city in TIER1_CITIES: return 1
            if city in TIER2_CITIES: return 2
            return 3
        city_series = df["location_city"] if "location_city" in df.columns else pd.Series([""] * len(df), index=df.index)
        feats["city_tier"] = city_series.apply(get_city_tier)
        
        exp_series = df["experience_level"] if "experience_level" in df.columns else pd.Series([""] * len(df), index=df.index)
        feats["experience_range"] = exp_series.map(EXP_MAP).fillna(2.0)
        
        src_series = df["source"] if "source" in df.columns else pd.Series(["LinkedIn"] * len(df), index=df.index)
        portal_map = {"Glassdoor": 0.24, "Indeed": 0.27, "LinkedIn": 0.19}
        feats["portal_ghost_baseline"] = src_series.map(portal_map).fillna(0.24)
        
        # --- LEAKAGE-FREE FOLD TRANSFORMATIONS ---
        # 1. Employer Repost Count
        key = df["company_name"].astype(str).str.lower().str.strip() + "||" + \
              df["job_title"].astype(str).str.lower().str.strip()
        feats["employer_repost_count"] = key.map(self.train_repost_counts_).fillna(1.0).astype(float)
        
        # 2. Posting Velocity
        comp_name = df["company_name"].astype(str).str.lower().str.strip()
        feats["posting_velocity_per_week"] = comp_name.map(self.train_company_velocity_).fillna(0.25).astype(float)
        
        # 3. Cross-Platform Duplicates
        feats["cross_platform_duplicate_flag"] = key.apply(lambda k: int(k in self.train_multiplatform_keys_))
        
        # 4. Salary vs Market Gap
        sal_mid_eval = df[["salary_min", "salary_max"]].mean(axis=1)
        title_lower = df["job_title"].astype(str).str.lower().str.strip()
        learned_medians = title_lower.map(self.train_title_medians_).fillna(self.train_overall_salary_median_)
        
        feats["salary_vs_market_gap"] = np.where(
            sal_mid_eval.notna(),
            ((sal_mid_eval - learned_medians) / learned_medians.replace(0, np.nan)).round(3),
            0.0
        )
        feats["salary_vs_market_gap"] = feats["salary_vs_market_gap"].fillna(0.0)
        
        # Interaction terms
        feats["velocity_x_no_salary"] = feats["posting_velocity_per_week"] * (1.0 - feats["salary_disclosed_num"])
        
        self.feature_names_ = feats.columns.tolist()
        return feats.fillna(0.0)

    def get_feature_names_out(self):
        return self.feature_names_
