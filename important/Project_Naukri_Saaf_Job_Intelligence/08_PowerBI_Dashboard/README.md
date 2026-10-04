# 08 — Power BI Executive Analytics Dashboard

## 🎯 Executive BI Overview

The **Naukri Saaf Executive Power BI Dashboard** provides an enterprise-grade reporting and forensic auditing solution for job listing authenticity across LinkedIn, Indeed, and Glassdoor.

- **Dashboard File**: [`Naukri_Saaf_Executive_Dashboard.pbix`](Naukri_Saaf_Executive_Dashboard.pbix)
- **Theme**: [`NaukriSaaf_Theme.json`](NaukriSaaf_Theme.json) (Custom curated dark/purple analytics aesthetic)
- **DAX Specifications**: [`DAX_DOCUMENTATION.md`](DAX_DOCUMENTATION.md) (Complete measure catalog)

---

## 🏛️ Star Schema Architecture

The data model follows an optimized Star Schema with 1 Central Fact table and 4 Dimension tables:

```
                  ┌───────────────────────┐
                  │     Dim_Platform      │
                  └───────────────────────┘
                  │  source (PK)          │
                  └───────────┬───────────┘
                              │ 1
                              │
                              │ *
┌───────────────────┐     ┌───┴───────────────────┐     ┌───────────────────┐
│    Dim_Company    │     │   Fact_JobListings    │     │   Dim_JobCategory │
├───────────────────┤     ├───────────────────────┤     ├───────────────────┤
│ company_name (PK) │ 1-* │ listing_id (PK)       │ *-1 │ job_category (PK) │
│ employer_tier     │     │ company_name (FK)     │     │ sector_group      │
│ company_rating    │     │ source (FK)           │     └───────────────────┘
└───────────────────┘     │ job_category (FK)     │
                          │ location_city (FK)    │
                          │ date_published (FK)   │
                          │ days_live             │
                          │ salary_min            │
                          │ salary_max            │
                          │ calibrated_ghost_prob │
                          │ ghost_status          │
                          │ is_syndicated         │
                          │ jd_vagueness_index    │
                          └───────────┬───────────┘
                                      │ *
                                      │
                                      │ 1
                          ┌───────────┴───────────┐
                          │      Dim_Location     │
                          ├───────────────────────┤
                          │ location_city (PK)    │
                          │ tier_classification   │
                          │ tech_hub_flag         │
                          └───────────────────────┘
```

---

## 📑 8-Page Dashboard Navigation

1. **Executive Overview**: Total postings (2,851), Ghost rate (15.0%), Suspect rate (25.0%), and market exposure KPIs.
2. **Platform Risk Matrix**: Head-to-head comparison of Glassdoor, Indeed, and LinkedIn across listing lifespans and transparency.
3. **Employer Risk Analysis**: Top serial ghost posters, vacancy volume vs. fulfillment ratios, and entity risk scoring.
4. **Salary Opacity & Compensation**: Gap analysis between undisclosed pay and ghost probability.
5. **Geographic Risk Distribution**: Tier-1 tech hubs (Bengaluru, Hyderabad, Pune, Mumbai, Delhi-NCR) vs. Tier-2 disparities.
6. **Syndication & JD Plagiarism**: Cross-company description copying clusters and syndicated posting rings.
7. **Requisition Staleness Cohorts**: Half-life decay and zombie listing concentrations (>90 days).
8. **Candidate Defense & Action Plan**: Remediation advice and candidate protection playbooks.

---

## 📐 DAX Measures Library

The semantic model implements 20 verified production DAX measures across 5 analytical categories:
- **Core Volume**: `[Total Listings]`, `[Confirmed Ghost Count]`, `[Suspect Count]`, `[Genuine Count]`
- **Rates & Proportions**: `[Ghost Rate %]`, `[Suspect Rate %]`, `[Genuine Rate %]`, `[At-Risk Exposure %]`
- **Forensic Ratios**: `[Salary Opacity %]`, `[Syndication Exposure %]`, `[High-Spread Outlier Count]`
- **Temporal & Lifespan**: `[Mean Requisition Days]`, `[Median Requisition Days]`, `[Requisition Half-Life Ratio]`
- **Employer Risk**: `[Employer Risk Index]`, `[Cumulative Market Exposure %]`, `[Top 10 Employer Concentration]`

For full formula syntax and performance notes, see [DAX_DOCUMENTATION.md](DAX_DOCUMENTATION.md).
