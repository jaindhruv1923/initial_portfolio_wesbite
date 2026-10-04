# Comprehensive Technical Audit: Project Naukri Saaf (Ghost Job Listing Detection)

**Auditor Role:** Senior Data Scientist + ML Engineer + Analytics Lead  
**Evaluation Standard:** Production readiness, statistical validity, interview defensibility, and data integrity  
**Branch:** `upgrade` (Commit base: `61a7c91`)  
**Date:** October 2026  

---

## 1. Executive Summary & End-to-End System Walkthrough

### 1.1 What the Project Does in Plain Language
"Naukri Saaf" ("Clean Jobs") is a full-stack data analytics and machine learning portfolio project designed to identify "ghost jobs" (job postings that collect resumes without active hiring intent) across three major Indian hiring portals: LinkedIn, Indeed, and Glassdoor.

The project attempts to bridge data collection, exploratory analytics, classical supervised and unsupervised ML, explainability, dashboarding, and client-side browser integration:
1. **Data Ingestion:** 3,000 raw job listings (1,000 per platform) scraped using Apify.
2. **Data Wrangling:** Harmonization into a 46-column unified schema (`unified_job_listings.csv`, 2,851 rows retained after filtering junk records).
3. **Feature Engineering & Pseudo-Labeling:** 25 tabular features engineered across posting velocity, text length/lexical diversity, salary disclosure, and employer repost patterns. Because no verified real-world ground-truth exists, a heuristic composite risk score (0–100) was computed from 13 rules; listings above the 80th percentile (risk score 35.1) underwent probabilistic logistic sampling with random noise to assign binary labels (`ghost_label` = 1 or 0; 29.3% ghost rate).
4. **Machine Learning Pipeline:** Benchmark of 5 classification models (Gradient Boosting, Random Forest, Stacking Ensemble, Logistic Regression, MLP Neural Network) on an 80/20 chronological split with synthetic oversampling (manual SMOTE).
5. **Diagnostics & Unsupervised Modeling:** Feature importances (calculated as z-score $\times$ Gini importance), 5-fold temporal cross-validation, 200-iteration bootstrap confidence intervals, Isolation Forest anomaly detection (10% contamination), K-Means clustering (5 employer archetypes), and DBSCAN clustering (ghost contagion rings).
6. **Delivery & Downstream Interfaces:**
   - **Streamlit Web Application (`app.py`):** 7 interactive tabs utilizing Plotly.
   - **MySQL Analytical Workbook (`naukri_saaf_sql_workbench.sql`):** 32 SQL queries covering data profiling, window functions, and cross-source comparisons.
   - **Power BI Dashboard (`Final PowerBI Dashboard Work.pbix`):** 8-page analytical report.
   - **Excel Companion Workbook (`Naukri_Saaf_Master_Workbook_Legacy.xlsx`):** 11 sheets of pivot tables, formulas, and dashboards.
   - **Chrome Extension (Manifest V3):** Client-side DOM scraper and heuristic scorecard that attempts to mirror model weights directly inside the job seeker's browser.

---

## 2. Data Provenance, Schemas & Label Derivation

### 2.1 Data Collection & Volume
- **Platforms:** Glassdoor, Indeed, LinkedIn via Apify scrapers.
- **Scrape Dates:** Raw files generated around July 7, 2026. The `date_published` values across listings span **June 5, 2023 to July 8, 2026**.
- **Raw Volume:** 1,000 rows per portal $\rightarrow$ 3,000 total rows (`01_Datasets_Raw_Scrapes/naukri_saaf_combined_raw.csv`).
- **Cleaning Loss:** 149 records dropped due to null/empty `job_title` or `company_name`:
  - Glassdoor: 127 dropped (1,000 $\rightarrow$ 873)
  - Indeed: 22 dropped (1,000 $\rightarrow$ 978)
  - LinkedIn: 0 dropped (1,000 $\rightarrow$ 1,000)
  - **Retained Total:** 2,851 rows representing 1,301 unique employers.

### 2.2 Feature Engineering (25 Total Features)
Features are grouped across 3 iterations in the codebase:
- **Base Features (9):** `salary_disclosed_num`, `days_live`, `description_length_words`, `posting_velocity_per_week`, `data_quality_score`, `experience_range`, `portal_ghost_baseline`, `city_tier`, `keyword_match_pct`.
- **v2 Engineered Features (6):** `desc_per_day`, `velocity_x_no_salary`, `salary_range_ratio`, `listing_age_bucket`, `glassdoor_salary_combo`, `city_opportunity_score`.
- **v3 New Features (10):** `employer_repost_count`, `cross_platform_duplicate_flag`, `keyword_stuffing_ratio`, `description_lexical_diversity`, `applications_per_day`, `contact_bypass_flag`, `urgency_language_score`, `company_data_completeness_score`, `remote_ambiguity_flag`, `salary_vs_market_gap`.

### 2.3 The Exact Weak-Supervision Labeling Mechanism (Cell 7 of Notebook)
No human ground truth or verified hiring outcome was used. The label was generated synthetically via the following mathematical procedure:

#### Step 1: Raw Signal Accumulation
Thirteen heuristic rules add weights to `raw_score` and `max_possible`:

| # | Signal / Condition | Applicable Platform | Points | Rationale |
|---|---|---|:---:|---|
| 1 | `salary_disclosed_num == 0` | Glassdoor, Indeed | +18 | Lack of salary transparency |
| 2 | `days_live > 90` | All | +22 | Extremely stale listing |
| 3 | `45 < days_live <= 90` | All | +12 | Moderately stale listing |
| 4 | `description_length_words < 150` | All | +15 | Skeletal job description |
| 5 | `keyword_stuffing_ratio > 0.8` AND `matched_kw_count == 0` | All | +8 | Generic keyword stuffing |
| 6 | `glassdoor_rating < 3.2` | Glassdoor | +12 | Low employee rating |
| 7 | `easy_apply == False` | Glassdoor, LinkedIn | +6 | High friction application |
| 8 | `company_data_completeness_score < 30` | All | +10 | Opaque employer identity |
| 9 | `employer_repost_count >= 3` | All | +15 | Serial reposting |
| 10 | `expired == True` | Glassdoor | +10 | Stale/expired status |
| 11 | `applications_per_day < 0.05` | LinkedIn | +12 | Abnormally low applicant interest |
| 12 | `contact_bypass_flag == 1` | All | +5 | Direct WhatsApp/personal email in JD |
| 13 | `description_lexical_diversity < 0.35` | All | +6 | Highly repetitive vocabulary |

#### Step 2: Normalization
$$\text{ghost\_risk\_score} = \left(\frac{\text{raw\_score}}{\max(\text{max\_possible}, 1)}\right) \times 100$$
Evaluates to: Mean = 26.3, Std = 9.7, Range = [0.0, 68.5].

#### Step 3: Probabilistic Soft-Boundary Sampling
- Threshold set at the 80th percentile: $\tau = 35.1$.
- Logistic transformation with temperature scaling ($T = 6.0$):
  $$\text{logit} = \frac{\text{ghost\_risk\_score} - 35.1}{6.0}$$
  $$p = \frac{1}{1 + e^{-\text{logit}}}$$
- Probability squashing to ensure stochasticity:
  $$p_{\text{ghost}} = 0.90 \times p + 0.05 \quad (\text{bounded in } [0.05, 0.95])$$
- Bernoulli trial with fixed seed (`RandomState(42)`):
  $$\text{ghost\_label} \sim \text{Bernoulli}(p_{\text{ghost}})$$
- Result: **834 positive labels (29.3% ghost rate)**.

---

## 3. Comprehensive Verification of Every Metric

Every numerical claim in the repository has been traced directly to its generating source code, notebook output cell, or CSV file:

| Category | Metric Name | Reported Value | Exact Source File & Line / Cell | Verification Status & Notes |
|---|---|:---:|---|---|
| **Data** | Raw scraped listings | 3,000 | Notebook Cell 3; `naukri_saaf_combined_raw.csv` | **Verified.** Exactly 1,000 rows per scraper. |
| **Data** | Cleaned unified rows | 2,851 | Notebook Cell 3; `unified_job_listings.csv` | **Verified.** 149 junk rows dropped. |
| **Data** | Unique employers | 1,301 | `README.md` Line 71; `predictions_v3.csv` | **Verified.** `company_name.nunique()` = 1,301. |
| **Data** | Weak-label ghost rate | 29.3% | Notebook Cell 7; `naukri_saaf_v3_dataset.csv` | **Verified.** 834 / 2,851 = 29.25%. |
| **Data** | Label threshold | 35.1 | Notebook Cell 7 output | **Verified.** 80th percentile of `ghost_risk_score`. |
| **ML Split** | Train set size | 2,280 | Notebook Cell 10 | **Verified.** Exactly 80.0% of 2,851. |
| **ML Split** | Test set size | 571 | Notebook Cell 10 | **Verified.** Exactly 20.0% of 2,851. |
| **ML Split** | Train class balance | 28.7% ghost | Notebook Cell 10 output | **Verified.** 654 positive in train set. |
| **ML Split** | Post-SMOTE train size | 3,250 | Notebook Cell 10 output | **Verified.** 1,625 majority $\times$ 2. |
| **Model** | GBM Test AUC | **0.7183** vs **0.7161** | Notebook Cell 10 output vs `model_comparison_v3.csv` | ⚠️ **Discrepancy:** Notebook output shows 0.7183, while CSV on disk contains 0.7161. |
| **Model** | GBM Test F1 | **0.5372** vs **0.5266** | Notebook Cell 10 output vs `model_comparison_v3.csv` | ⚠️ **Discrepancy:** Notebook output shows 0.5372, while CSV on disk contains 0.5266. |
| **Model** | Stacking AUC | 0.7094 vs 0.7086 | Notebook Cell 10 output vs `model_comparison_v3.csv` | ⚠️ Notebook output shows 0.7094; CSV shows 0.7086. |
| **Model** | Random Forest AUC | 0.7080 vs 0.7085 | Notebook Cell 10 output vs `model_comparison_v3.csv` | ⚠️ Notebook output shows 0.7080; CSV shows 0.7085. |
| **Model** | Logistic Reg AUC | 0.7067 vs 0.7066 | Notebook Cell 10 output vs `model_comparison_v3.csv` | Consistent (~0.707). |
| **Model** | MLP Neural Net AUC | 0.6705 vs 0.6713 | Notebook Cell 10 output vs `model_comparison_v3.csv` | Consistent (~0.671). |
| **CV** | Temporal CV Folds | 5 folds | `temporal_cv_results_v3.csv` | **Verified.** GBM AUCs: 0.5848, 0.7137, 0.7171, 0.6911, 0.7233. Mean = 0.6860. |
| **Expl.** | Top feature importance | `days_live` (9.8%), `listing_age_bucket` (9.7%) | `feature_importance_v3.csv` | **Verified.** Sum of top two = 19.55%. |
| **Unsup.** | Isolation Forest Anomalies | 285 listings (10.0%) | Notebook Cell 10; `predictions_v3.csv` | **Verified.** Exactly 10% contamination rate. |
| **Unsup.** | DBSCAN Contagion Rings | 41 rings, 1,631 noise | Notebook Cell 10; `predictions_v3.csv` | **Verified.** Clusters $\ge$ 0 count to 41; noise = 1,631. |
| **Unsup.** | K-Means Archetypes | 5 clusters | `cluster_profiles_v3.csv` | **Verified.** 5 clusters profiles defined. |
| **Preds** | Final Classification | 1,708 Genuine, 715 Suspect, 428 Ghost | Notebook Cell 16; `predictions_v3.csv` | **Verified.** Cutoffs at 60th (0.310) and 85th (0.703) percentiles of `predicted_ghost_prob`. |
| **Stats** | Bootstrap 95% CI width | 0.7245 | Notebook Cell 10 output; `bootstrap_ci_v3.csv` | **Verified.** Mean difference between upper and lower bounds. |

---

## 4. In-Depth Methodological & Statistical Validity Risks

### 4.1 Label Circularity (The Critical Flaw)
- **Mechanism:** The target `ghost_label` is generated by evaluating 13 rules over features like `days_live`, `salary_disclosed_num`, `description_length_words`, `keyword_stuffing_ratio`, and `employer_repost_count`.
- **Consequence:** The supervised models (GBM, RF, LogReg) are trained on these **exact same features** to predict this synthetic label.
- **Why AUC is ~0.718:** An interviewer will ask: *"If the model is learning the rules, why isn't AUC 0.99?"*  
  The reason AUC is bounded at ~0.718 is **solely because artificial Bernoulli noise and temperature scaling ($T=6.0$) were injected during label generation** ($p_{\text{ghost}} = 0.90 \times \sigma(\text{logit}) + 0.05$). The model is not detecting real ghost jobs in the Indian economy; it is partially recovering a noisy logistic function of its own input features.

### 4.2 Massive Pre-Split Data Leakage
Several aggregated features were calculated across the **entire dataset** prior to the 80/20 train/test split:
1. `employer_repost_count`: Calculated by grouping across all 2,851 rows. Test set listings artificially inflated the repost counts of training set records.
2. `posting_velocity_per_week`: Total company count divided by 4 weeks across the whole dataset.
3. `cross_platform_duplicate_flag`: Multi-source presence computed globally.
4. `salary_vs_market_gap`: `title_median` calculated across all rows, leaking future salary statistics into the training fold.
5. `ghost_risk_score` threshold (35.1): 80th percentile calculated on full data.

### 4.3 Flawed Synthetic Oversampling ("Random Pair Convex Mixing" vs. SMOTE)
The manual SMOTE function in Cell 10 does not calculate $k$-nearest neighbors:
```python
i = rng.choice(minority_idx)
neighbour = rng.choice(minority_idx) # Arbitrary random choice, NOT nearest neighbor!
synthetic.append(X[i] + alpha * (X[neighbour] - X[i]))
```
- **Risk:** Standard SMOTE interpolates between an instance and its nearest topological neighbors in feature space. Picking two arbitrary minority indices creates synthetic records that cut across disjoint regions of the manifold (e.g., interpolating between a 0-experience intern in Indore and a 15-year VP in Mumbai), generating synthetic points that violate real-world joint distributions.

### 4.4 Pseudocode "SHAP" is Not SHAP
Cell 10 claims to compute "TreeSHAP approximation", but implements:
```python
z_scores = (X_vals - means) / stds
contributions = z_scores * importances
```
- **Risk:** This is simply standardized feature values multiplied by global Random Forest Gini feature importances. It completely ignores tree path traversal, feature interactions, and the Shapley axiomatic foundation. Calling this "SHAP" in an interview will immediately disqualify the candidate in front of a senior ML engineer.

### 4.5 The Final Model Bait-and-Switch
- On the leaderboard, **Gradient Boosting (GBM)** is crowned the best model (AUC ~0.718).
- However, the actual predictions stored in `predictions_v3.csv` and served in the Streamlit dashboard are generated by `calibrated_rf` (**Random Forest**)!
- Furthermore, Platt scaling calibration was fitted on the **SMOTE-oversampled training set (`X_train_res`)**. Calibrating probabilities on an artificially balanced 50:50 distribution skews the posterior odds ratio away from the natural 29.3% prior distribution.

### 4.6 Impossibly Wide Bootstrap Confidence Intervals
- The reported average 95% bootstrap confidence interval width is **0.7245** on a probability range of $[0.0, 1.0]$.
- **Risk:** An average confidence interval spanning 72% of the probability space means a listing predicted with probability 0.50 has a CI roughly spanning $[0.14, 0.86]$. The model has essentially no statistical certainty on individual predictions.

### 4.7 Platform Scraping & Structural Missingness Bias
- **LinkedIn:** 0% salary disclosure, 0% company ratings, 100% applicant count availability.
- **Indeed:** Partial salary disclosure, 0% ratings, 0% applicant counts.
- **Glassdoor:** 100% company rating availability, 0% applicant counts.
- While the author attempted to handle this by normalizing `max_possible` in the rule weighting, the models still train on these features with zero-imputation. A tree split on `glassdoor_rating` or `applications_per_day` is essentially acting as an implicit portal discriminator rather than a pure ghost signal.

---

## 5. Repository-Wide Discrepancies & Broken Components

### 5.1 Critical Mismatch: 125,457 Scraped Listings Claim
- **The Issue:** `07_BA_Documentation/Executive_Summary_NaukriSaaf.md` repeatedly claims:
  - Header: `125,457 scraped · 2,852 modeled`
  - Headline metric table: `125,457 Raw Listings Scraped`
  - Section 2: Claims `1,361 High-Risk Poster Employers` (when there are only 1,301 total employers in the entire dataset; 1,361 is the listing count of that cluster!).
  - Section 2: Claims `6 distinct profiles` (K-Means used $k=5$).
- **The Reality:** The actual scrape in the repository has exactly **3,000 raw rows** and **2,851 modeled rows**. Presenting numbers off by a factor of 42x is catastrophic in an interview.

### 5.2 Folder Structure & File References Mismatch
- `README.md` documents a flat repository structure (`data/`, `models/`, `diagnostics/`, `naukri-saaf-extension/`, `app.py`).
- The actual disk structure uses numbered folders:
  - `01_Datasets_Raw_Scrapes/`
  - `02_SQL/`
  - `03_ML_Pipeline_and_Models/`
  - `04_Excel_Workbook/`
  - `05_Streamlit_Dashboard/`
  - `06_Chrome_Extension/`
  - `07_BA_Documentation/`
  - `08_PowerBI_Dashboard/`

### 5.3 Chrome Extension Runtime Failure
- In `06_Chrome_Extension/sidepanel.html`, the script tags expect a subdirectory:
  ```html
  <script src="lib/pdfjs/pdf.min.js"></script>
  <script src="lib/nlp.js"></script>
  <script src="lib/legitimacy.js"></script>
  <script src="sidepanel.js"></script>
  ```
- In reality, `pdf_min.js`, `nlp.js`, and `legitimacy.js` reside directly in the root of `06_Chrome_Extension/` without a `lib/` directory. Loading the unpacked extension in Chrome throws script loading errors immediately.
- `manifest.json` references `"icons": { "16": "icons/icon16.png", ... }`, but the `icons/` folder is missing in `06_Chrome_Extension/` (only `icon48.png` is at the root).

### 5.4 SQL Script Disconnection from Ghost Detection
- `02_SQL/naukri_saaf_sql_workbench.sql` contains 32 excellent data profiling and exploratory queries.
- **However:** It queries `naukri_jobs_raw` from `naukri_saaf_combined_raw.csv`. It contains **zero** queries analyzing ghost jobs, ghost probabilities, model errors, or employer ghost rates! It does not load `predictions_v3.csv`. For an analyst portfolio, the SQL workbook completely misses the primary analytical question.

### 5.5 Streamlit Usability Friction
- `05_Streamlit_Dashboard/app.py` halts execution with `st.stop()` if the user does not manually upload `predictions_v3.csv`. It does not fall back to the existing file on disk in `03_ML_Pipeline_and_Models/predictions_v3.csv`. Anyone running `streamlit run app.py` gets an empty landing screen.

---

## 6. What is Strong and Must Be Preserved

Despite the methodological validity flaws in the pseudo-labeling, the engineering foundation is exceptional for an undergraduate portfolio:
1. **End-to-End Scope:** Very few student portfolios span web scraping, unified schema design, 5 ML models, unsupervised clustering, interactive Streamlit, SQL, Excel, Power BI, and a Chrome extension.
2. **Multi-Source Scraping Realism:** Working with messy, real scraped data from three distinct portals (handling nulls, currency variations, and nested fields) demonstrates genuine data engineering competence.
3. **Streamlit UI Aesthetics:** Dark ghost-detective theme, polished CSS, Plotly integrations, and responsive metric cards.
4. **SQL Proficiency:** Clean, MariaDB/MySQL 8.0 compliant queries with window functions (`DENSE_RANK`, `NTILE`, `LAG`/`LEAD`), CTEs, and string parsing.
5. **Business & Requirements Documentation:** The BA suite (`BRD`, `RTM`, `Data Dictionary`, `User Stories`) demonstrates professional lifecycle awareness rare among engineering students.
6. **Chrome Extension Vision:** Evaluating DOM elements against model weights locally with zero external network requests is a brilliant product concept.

---

## 7. Audit Verdict & Upgrade Priority
The current project is a **Tier-1 UI/Portfolio shell** built around a **Tier-3 synthetic labeling loop**. In an interview with a senior practitioner, the candidate would be exposed on label circularity and pre-split leakage within 5 minutes. 

By fixing the ground truth (gold standard hand labeling + Snorkel weak supervision), eliminating data leakage, introducing real NLP embeddings, unifying the analytics layer across SQL/PowerBI/Streamlit, and adding an Agentic verification flow, this can be transformed into a **top 1% production-grade portfolio project**.
