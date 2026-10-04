"""
generate_blind_sheet.py
Generates a clean, blind labeling sheet of 80 stratified job postings for human verification.
Includes ONLY: id, platform, company, title, location, listing_url, and blank columns:
on_company_careers_page, still_live, duplicate_or_reposted, label, notes.
Saves sampling metadata strictly to a private JSON file.
"""

import json
import numpy as np
import pandas as pd

# Load datasets
df_v3 = pd.read_csv("01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv")
df_gd = pd.read_csv("01_Datasets_Raw_Scrapes/dataset_glassdoor-jobs-scraper-remove-duplicate-jobs_2026-07-07_06-52-49-521.csv")
df_in = pd.read_csv("01_Datasets_Raw_Scrapes/dataset_indeed-job-scraper_2026-07-07_06-48-09-041.csv")
df_li = pd.read_csv("01_Datasets_Raw_Scrapes/dataset_linkedin-job-scraper_2026-07-07_06-26-12-651.csv")

# Map URLs
gd_map = {}
for _, row in df_gd.iterrows():
    url = str(row.get("jobUrl", ""))
    if "jl=" in url:
        jl_id = url.split("jl=")[-1].split("&")[0]
        gd_map["GD" + jl_id] = url

in_map = {}
for _, row in df_in.iterrows():
    url = str(row.get("jobUrl", ""))
    if "jk=" in url:
        jk_id = url.split("jk=")[-1].split("&")[0]
        in_map["IN" + jk_id] = url

li_map = {}
for _, row in df_li.iterrows():
    url = str(row.get("jobUrl", ""))
    job_id = str(row.get("jobId", ""))
    if job_id and job_id != "nan":
        li_map["LI" + job_id] = url

df_v3["listing_url"] = ""
gd_mask = df_v3["source"] == "Glassdoor"
in_mask = df_v3["source"] == "Indeed"
li_mask = df_v3["source"] == "LinkedIn"

df_v3.loc[gd_mask, "listing_url"] = df_v3.loc[gd_mask, "listing_id"].map(gd_map).fillna("")
df_v3.loc[in_mask, "listing_url"] = df_v3.loc[in_mask, "listing_id"].map(in_map).fillna("")
df_v3.loc[li_mask, "listing_url"] = df_v3.loc[li_mask, "listing_id"].map(li_map).fillna("")

# Filter for rows that have valid URLs
valid_df = df_v3[df_v3["listing_url"].str.startswith("http")].copy()

# Create strata for balanced representation:
# Platform: Glassdoor (27), Indeed (27), LinkedIn (26) = 80
# Within each platform, stratify across age tertiles (fresh <= 14d, normal 15-45d, stale > 45d)
valid_df["age_stratum"] = pd.cut(
    valid_df["days_live"].fillna(14),
    bins=[-np.inf, 14, 45, np.inf],
    labels=["fresh_le14d", "normal_15_45d", "stale_gt45d"]
)

np.random.seed(42)

sampled_rows = []
private_strata = []

targets = [
    ("Glassdoor", 27),
    ("Indeed", 27),
    ("LinkedIn", 26)
]

for platform, target_n in targets:
    plat_df = valid_df[valid_df["source"] == platform].copy()
    
    # Stratified sample by age_stratum if available, else sample to reach target_n
    sampled_plat = []
    strata_counts = {"fresh_le14d": target_n // 3, "normal_15_45d": target_n // 3, "stale_gt45d": target_n - 2 * (target_n // 3)}
    
    for stratum, count in strata_counts.items():
        subset = plat_df[plat_df["age_stratum"] == stratum]
        take = min(len(subset), count)
        if take > 0:
            sampled_plat.append(subset.sample(n=take, random_state=42))
            
    current_df = pd.concat(sampled_plat) if sampled_plat else pd.DataFrame()
    needed = target_n - len(current_df)
    if needed > 0:
        remaining = plat_df[~plat_df["listing_id"].isin(current_df["listing_id"])]
        fill_sample = remaining.sample(n=needed, random_state=42)
        final_plat_df = pd.concat([current_df, fill_sample])
    else:
        final_plat_df = current_df.head(target_n)
        
    for _, r in final_plat_df.iterrows():
        # Blind row visible to the human annotator
        sampled_rows.append({
            "id": r["listing_id"],
            "platform": r["source"],
            "company": r["company_name"],
            "title": r["job_title"],
            "location": f"{r.get('location_city', '')}, {r.get('location_state', '')}".strip(", "),
            "listing_url": r["listing_url"],
            "on_company_careers_page": "",  # blank for human
            "still_live": "",               # blank for human
            "duplicate_or_reposted": "",    # blank for human
            "label": "",                    # blank for human: real / unclear / ghost
            "notes": ""                     # blank for human
        })
        
        # Private stratum metadata kept separate
        private_strata.append({
            "id": r["listing_id"],
            "platform": r["source"],
            "days_live": float(r.get("days_live", 0)),
            "age_stratum": str(r.get("age_stratum", "unknown")),
            "salary_disclosed": bool(pd.notna(r.get("salary_min")) or pd.notna(r.get("salary_max"))),
            "company_size": str(r.get("company_size_category", "Unknown"))
        })

blind_df = pd.DataFrame(sampled_rows)
# Shuffle rows so platforms and ages are randomly ordered for true blind review
blind_df = blind_df.sample(frac=1.0, random_state=123).reset_index(drop=True)

# Save blind sheet
blind_out_path = "data/BLIND_LABELING_SHEET_80.csv"
blind_df.to_csv(blind_out_path, index=False)
print(f"Generated {len(blind_df)} blind listings at: {blind_out_path}")

# Save private stratum info
private_out_path = "data/blind_sampling_strata_private.json"
with open(private_out_path, "w", encoding="utf-8") as f:
    json.dump(private_strata, f, indent=2)
print(f"Saved private stratum info to: {private_out_path}")
