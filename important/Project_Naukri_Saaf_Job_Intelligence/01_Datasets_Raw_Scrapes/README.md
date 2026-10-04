# 01 — Raw Datasets & Multi-Portal Scrapes

## 📦 Ingestion Overview

This module houses the raw multi-platform job postings collected across **Glassdoor, Indeed, and LinkedIn** via Apify scrapers, along with combined and deduplicated corpora.

---

## 🗂️ File Inventory

| File | Records | Description |
|---|:---:|---|
| `dataset_linkedin-job-scraper_*.csv` | 1,000 | Raw scrape of Indian tech roles on LinkedIn |
| `dataset_indeed-job-scraper_*.csv` | 1,000 | Raw scrape of Indian tech roles on Indeed |
| `dataset_glassdoor-jobs-scraper-*.csv`| 1,000 | Raw scrape of Indian tech roles on Glassdoor |
| `naukri_saaf_combined_raw.csv` | 3,000 | Concatenated un-deduplicated multi-portal raw records |
| `naukri_saaf_v3_dataset.csv` | **2,851** | Cleaned, deduplicated master analytical dataset (149 duplicate rows dropped) |
| `unified_job_listings.csv` | 2,851 | Schema-normalized export formatted for cross-portal ingestion |

---

## 📖 Data Dictionary

For the exhaustive schema definition, data types, null percentage profiles, and field descriptions:
👉 **[DATA_DICTIONARY.md](DATA_DICTIONARY.md)**
