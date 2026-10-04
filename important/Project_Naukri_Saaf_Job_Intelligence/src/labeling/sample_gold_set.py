"""
Sample Gold Set for Human Annotation
====================================
Selects a stratified, balanced sample of 180 listings from the unified dataset
(60 LinkedIn, 60 Indeed, 60 Glassdoor) across risk strata (low, medium, high)
to create an unbiased evaluation set for ground-truth verification.
"""

import os
import pandas as pd
import numpy as np

RANDOM_SEED = 42

def create_gold_sample(
    input_path: str = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv",
    output_csv: str = "data/gold_labeling_sheet.csv",
    sample_size_per_platform: int = 60
):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df = pd.read_csv(input_path)
    
    print(f"Total available listings: {len(df):,}")
    
    # Create risk strata based on existing ghost_risk_score tertiles/quantiles
    df["risk_stratum"] = pd.qcut(
        df["ghost_risk_score"],
        q=3,
        labels=["Low Risk", "Medium Risk", "High Risk"]
    )
    
    samples = []
    rng = np.random.RandomState(RANDOM_SEED)
    
    for platform in ["Glassdoor", "Indeed", "LinkedIn"]:
        plat_df = df[df["source"] == platform]
        for stratum in ["Low Risk", "Medium Risk", "High Risk"]:
            stratum_df = plat_df[plat_df["risk_stratum"] == stratum]
            n_samples = sample_size_per_platform // 3  # 20 per stratum per platform
            
            # If available, stratify by salary disclosure
            sal_yes = stratum_df[stratum_df["salary_disclosed_num"] == 1]
            sal_no = stratum_df[stratum_df["salary_disclosed_num"] == 0]
            
            n_yes = min(len(sal_yes), n_samples // 2)
            n_no = n_samples - n_yes
            
            sampled_yes = sal_yes.sample(n=n_yes, random_state=rng) if n_yes > 0 else pd.DataFrame()
            sampled_no = sal_no.sample(n=n_no, random_state=rng) if len(sal_no) >= n_no else sal_no
            
            combined_sample = pd.concat([sampled_yes, sampled_no])
            # If still short, sample remainder without replacement
            if len(combined_sample) < n_samples:
                remaining = stratum_df.drop(combined_sample.index, errors="ignore")
                extra = remaining.sample(n=min(len(remaining), n_samples - len(combined_sample)), random_state=rng)
                combined_sample = pd.concat([combined_sample, extra])
                
            samples.append(combined_sample)
            
    gold_df = pd.concat(samples).drop_duplicates(subset=["listing_id"]).reset_index(drop=True)
    
    # Shuffle so labeler does not see contiguous blocks of one platform/risk
    gold_df = gold_df.sample(frac=1.0, random_state=rng).reset_index(drop=True)
    
    # Clean and format output columns for human annotator
    # We deliberately hide the old heuristic label from the primary view to prevent anchoring bias,
    # but store it in a verification column for automated post-labeling comparison.
    def clean_snippet(text, max_len=300):
        if pd.isna(text):
            return ""
        s = " ".join(str(text).split())
        return s[:max_len] + ("..." if len(s) > max_len else "")

    export_df = pd.DataFrame({
        "sample_id": range(1, len(gold_df) + 1),
        "listing_id": gold_df["listing_id"],
        "source": gold_df["source"],
        "job_title": gold_df["job_title"],
        "company_name": gold_df["company_name"],
        "location_city": gold_df["location_city"].fillna("Not Specified"),
        "days_live": gold_df["days_live"].fillna(0).astype(int),
        "salary_disclosed": gold_df["salary_disclosed_num"].map({1: "Yes", 0: "No"}),
        "salary_range": gold_df.apply(
            lambda r: f"{r['salary_min']:,.0f} - {r['salary_max']:,.0f} {r['salary_currency']}"
            if pd.notna(r.get("salary_min")) and pd.notna(r.get("salary_max")) else "Undisclosed",
            axis=1
        ),
        "repost_count": gold_df["employer_repost_count"].fillna(1).astype(int),
        "description_snippet": gold_df["description_text"].apply(clean_snippet),
        "full_description": gold_df["description_text"].fillna(""),
        
        # Human Annotation Columns to be filled:
        "gold_label": "",          # 1 = Ghost / Low-Quality Fake, 0 = Genuine Job, -1 = Unsure
        "confidence": "",          # High / Medium / Low
        "primary_red_flags": "",   # e.g., Stale, No Salary, Generic JD, Contact Bypass, Unrealistic Stack
        "annotator_notes": "",
        
        # Baseline reference (hidden in analysis, preserved for programmatic audit):
        "_legacy_weak_label": gold_df["ghost_label"],
        "_legacy_risk_score": gold_df["ghost_risk_score"]
    })
    
    export_df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Successfully generated gold labeling sheet: {output_csv}")
    print(f"Sample size: {len(export_df)} listings")
    print("\nBreakdown by Source:")
    print(export_df["source"].value_counts())
    print("\nBreakdown by Legacy Risk Stratum:")
    print(gold_df["risk_stratum"].value_counts())
    print("\nSalary Disclosure Breakdown:")
    print(export_df["salary_disclosed"].value_counts())
    return export_df

if __name__ == "__main__":
    create_gold_sample()
