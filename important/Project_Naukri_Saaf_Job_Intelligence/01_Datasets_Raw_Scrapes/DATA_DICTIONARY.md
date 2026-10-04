# Data Dictionary & Provenance Specification
## Project: Naukri Saaf — Multi-Platform Job Listing Intelligence

---

## 1. Data Collection & Provenance

The primary dataset consists of **3,000 raw job listings** collected on July 7, 2026 using dedicated Apify cloud scrapers targeting three major employment platforms:

| Raw Scrape File Name | Platform Source | Raw Count | Platform-Specific Fields & Notes |
|---|:---:|:---:|---|
| `dataset_glassdoor-jobs-scraper-remove-duplicate-jobs_...csv` | Glassdoor | 1,000 | Rich company metadata (ratings, revenue, employee size); estimated salary bands. |
| `dataset_indeed-job-scraper_...csv` | Indeed | 1,000 | High employer velocity; salary ranges provided in text; rapid expiration. |
| `dataset_linkedin-job-scraper_...csv` | LinkedIn | 1,000 | High applicant count metadata ("Over 200 applicants"); unlisted salary fields. |

### Data Cleaning & Deduplication Pipeline
1. **Raw Ingestion**: Merged into `naukri_saaf_combined_raw.csv` (3,000 records).
2. **Malformed & Duplicate Filtering**:
   - Dropped 149 records: exact URL duplicates, headless scraper timeouts, and corrupted HTML descriptions.
3. **Validated Production Corpus**: **2,851 unique job postings** across **1,301 distinct companies** (`naukri_saaf_v3_dataset.csv`).

---

## 2. Core Column Schema & Data Types

| Column Name | Data Type | Null % | Description & Business Meaning | Sample Values |
|---|:---:|:---:|---|---|
| `listing_id` | String (PK) | 0.0% | Unique identifier formatted as `{platform_prefix}_{hex_hash}` | `INf3aab858e061015a`, `GLb18a2f4c90e` |
| `source` | String (Cat) | 0.0% | Sponsoring job portal | `LinkedIn`, `Indeed`, `Glassdoor` |
| `job_title` | String | 0.0% | Raw job title extracted from page `<h1>` | `Senior Data Analyst`, `Lead Python Engineer` |
| `normalized_title` | String | 0.0% | Lowercased, stripped title mapped to standard role taxonomy | `data analyst`, `python developer` |
| `company_name` | String | 0.0% | Legal hiring employer name | `Oracle`, `Amazon`, `Apex Talent Solutions` |
| `location_city` | String | 2.4% | Primary employment city | `Bangalore`, `Hyderabad`, `Pune`, `Mumbai` |
| `location_state` | String | 8.1% | Primary employment state | `Karnataka`, `Telangana`, `Maharashtra` |
| `location_country` | String | 0.0% | Country code or name | `India`, `IN` |
| `date_published` | DateTime | 1.8% | Date requisition was originally published | `2026-05-14`, `2026-06-20` |
| `date_scraped` | DateTime | 0.0% | Timestamp of Apify scrape execution | `2026-07-07` |
| `days_live` | Integer | 0.0% | Requisition lifespan in days (`date_scraped - date_published`) | `12`, `45`, `128` |
| `salary_min` | Float | 83.1% | Lower bound of compensation (standardized to annual INR) | `600000.0`, `1200000.0` |
| `salary_max` | Float | 83.1% | Upper bound of compensation (standardized to annual INR) | `900000.0`, `1800000.0` |
| `salary_currency` | String | 83.1% | Currency code | `INR` |
| `salary_period` | String | 83.1% | Payment period | `yearly`, `monthly` |
| `description_text` | String (Text) | 0.0% | Full text of job description, requirements, and responsibilities | Full text copy |
| `job_category` | String (Cat) | 0.0% | Standardized industry sector | `Data & Analytics`, `Software Engineering` |
| `job_type` | String | 4.2% | Employment type | `Full-time`, `Contract`, `Internship` |
| `remote_type` | String | 12.0% | Workplace policy | `On-site`, `Hybrid`, `Remote` |
| `company_overall_rating` | Float | 38.2% | Employer rating on 1.0 - 5.0 scale (from Glassdoor / Indeed) | `3.8`, `4.2`, `4.5` |
| `applications_count` | Integer | 64.0% | Number of applicants who applied via portal | `42`, `180`, `250` |

---

## 3. Downstream Engineered Datasets (v4 Production)

| Artifact Path | Record Count | Purpose & Description |
|---|:---:|---|
| `data/gold_labeling_sheet.csv` | 180 | **Holdout Gold Standard Test Set**: Stratified sample (60 LinkedIn, 60 Indeed, 60 Glassdoor) hand-verified with ground truth labels. |
| `data/weak_supervision_labels.csv` | 2,851 | **Snorkel Generative Model Output**: Probabilistic weak labels (`weak_label_ghost`, posterior probabilities) from 10 domain LFs. |
| `outputs/embeddings/jd_dense_embeddings.npy` | 2,851 x 64 | **Dense Latent Semantic Vectors**: 64-dimensional unit-normalized embeddings via Randomized SVD (LSA). |
| `data/cross_company_plagiarism.csv` | 2,851 | **Description Syndication Matrix**: Pairwise cross-company cosine similarities and plagiarism flags. |
| `data/jd_vagueness_metrics.csv` | 2,851 | **Syntactic & Lexical Quality**: Concrete tech entity density, corporate buzzword density, and composite vagueness index. |
| `data/predictions_v4.csv` | 2,851 | **Calibrated Model Inference**: Final Platt-calibrated ghost risk probabilities, status tiers, and top TreeSHAP driver. |
| `data/survival_curve_estimates.csv` | 740 | **Kaplan-Meier Survival Curves**: Step-by-step product-limit coordinates and Greenwood standard errors. |
| `data/survival_summary_metrics.csv` | 8 | **Lifespan & Half-Life Summary**: Median survival half-lives across cohorts. |
