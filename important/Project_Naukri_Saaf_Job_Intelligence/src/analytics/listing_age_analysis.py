"""
Cross-Sectional Listing Age Analysis
====================================
Analyzes the distribution of `days_live` (listing age at the time of scrape)
across platforms and risk categories.

IMPORTANT METHODOLOGICAL NOTE:
This data is a single cross-sectional snapshot collected on a specific date.
No longitudinal delisting, closure, or fulfillment events were observed.
Therefore, this measures cross-sectional listing age, NOT survival times or
delisting hazard rates.
"""

import os
import sys
import numpy as np
import pandas as pd

def compute_age_distribution():
    print("=" * 80)
    print("  NAUKRI SAAF — CROSS-SECTIONAL LISTING AGE ANALYSIS")
    print("  (Snapshot age at scrape time; no delisting events observed)")
    print("=" * 80)
    
    data_path = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}")
        return
        
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df):,} listings for age distribution profiling.")
    
    days = pd.to_numeric(df.get("days_live"), errors="coerce").dropna()
    
    overall_stats = {
        "Cohort Category": "Overall",
        "Cohort": "All Listings",
        "Count": int(len(days)),
        "Mean Days": round(float(days.mean()), 1),
        "Median Days": round(float(days.median()), 1),
        "P25 Days": round(float(days.quantile(0.25)), 1),
        "P75 Days": round(float(days.quantile(0.75)), 1),
        "P90 Days": round(float(days.quantile(0.90)), 1),
        "Max Days": round(float(days.max()), 1)
    }
    
    records = [overall_stats]
    
    # By platform
    portal_col = "source" if "source" in df.columns else "job_portal"
    if portal_col in df.columns:
        for portal in ["Glassdoor", "Indeed", "LinkedIn"]:
            subset = df[df[portal_col] == portal]["days_live"].dropna()
            if len(subset) == 0: continue
            records.append({
                "Cohort Category": "Platform",
                "Cohort": portal,
                "Count": int(len(subset)),
                "Mean Days": round(float(subset.mean()), 1),
                "Median Days": round(float(subset.median()), 1),
                "P25 Days": round(float(subset.quantile(0.25)), 1),
                "P75 Days": round(float(subset.quantile(0.75)), 1),
                "P90 Days": round(float(subset.quantile(0.90)), 1),
                "Max Days": round(float(subset.max()), 1)
            })
            
    # By salary disclosure
    has_sal = df["salary_disclosed"] == "Yes" if "salary_disclosed" in df.columns else df["salary_max"].notna()
    for name, mask in [("Salary Disclosed", has_sal), ("Salary Hidden/Missing", ~has_sal)]:
        subset = df[mask]["days_live"].dropna()
        if len(subset) == 0: continue
        records.append({
            "Cohort Category": "Salary Disclosure",
            "Cohort": name,
            "Count": int(len(subset)),
            "Mean Days": round(float(subset.mean()), 1),
            "Median Days": round(float(subset.median()), 1),
            "P25 Days": round(float(subset.quantile(0.25)), 1),
            "P75 Days": round(float(subset.quantile(0.75)), 1),
            "P90 Days": round(float(subset.quantile(0.90)), 1),
            "Max Days": round(float(subset.max()), 1)
        })
        
    out_df = pd.DataFrame(records)
    out_path = "data/listing_age_distribution.csv"
    out_df.to_csv(out_path, index=False)
    
    print("\nSummary Table:")
    print(out_df.to_string(index=False))
    print(f"\nExported to: {out_path}")
    print("=" * 80)
    return out_df

if __name__ == "__main__":
    compute_age_distribution()
