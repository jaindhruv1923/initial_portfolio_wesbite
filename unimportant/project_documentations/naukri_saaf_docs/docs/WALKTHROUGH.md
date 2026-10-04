# Naukri Saaf — Project Walkthrough & Technical Defense Guide

> **Prepared for Student Technical Interviews (Data Analyst, Data Scientist, ML Engineer)**  
> *Objective: Plain-language explanations of every component, why it was designed that way, and how to defend its limitations honestly when questioned.*

---

## Overview & Core Narrative

**The Problem**: Job seekers spend hours tailoring resumes and applying to postings that may no longer be actively monitored, are reposted continuously to build passive talent pipelines, or conceal basic compensation details.

**The Solution**: An open-source analytics and machine learning pipeline that analyzes 2,851 job postings across LinkedIn, Indeed, and Glassdoor, evaluates posting quality, provides calibrated risk probabilities, and surfaces explainable feature contributions.

---

## Module-by-Module Defense

### Module 1: Data Ingestion & Cleaning (`01_Datasets_Raw_Scrapes/`)

* **What it does**:
  * Ingested 3,000 raw scraped job postings (1,000 each from Glassdoor, Indeed, and LinkedIn) using Apify scrapers.
  * Standardized column schemas, parsed dates, extracted salary figures, and deduplicated records on `(job_title, company_name, location_city, date_published)`.
  * Result: **2,851 clean, unique job listings** (149 duplicate rows dropped).
* **Why it was built this way**:
  * Job boards frequently display the same opening across multiple search keywords or regional pages. Deduplication prevents identical listings from inflating counts or leaking across train/test splits.
* **What could go wrong (Interview Defense)**:
  * **Trap**: *"Did you track when these jobs were closed or filled?"*
  * **Honest Answer**: *"No. This dataset represents a single point-in-time cross-sectional snapshot scraped on 2026-07-07. `days_live` measures the age of the listing at the scrape timestamp. We did not follow listings longitudinally over time, so we do not observe actual job closure events."*

---

### Module 2: SQL Workbench & Staging Layer (`02_SQL/`)

* **What it does**:
  * Provides 42 structured queries across 9 analytical categories in `naukri_saaf_sql_workbench.sql`.
  * Covers staging schema design, type casting, window functions (`DENSE_RANK()`), Common Table Expressions (CTEs), salary opacity metrics, and employer repost frequencies.
* **Why it was built this way**:
  * Demonstrates production data analyst fundamentals: extracting business insights directly in the database before feeding downstream ML models.
* **What could go wrong (Interview Defense)**:
  * **Limitation**: Free-text salary strings and relative dates ("30+ days ago") require careful string parsing. If scraping formats shift, SQL transformation regexes must be updated.

---

### Module 3: Weak Supervision & Labeling Strategy (`src/labeling/`, `src/models/weak_supervision.py`)

* **What it does**:
  * Public job boards do not come with ground truth labels indicating whether a posting is real or a ghost job.
  * Implemented 10 domain Labeling Functions (LFs) capturing observable heuristics: extreme age (>90 days), high repost frequency ($\ge 4$), personal contact bypass (WhatsApp/Gmail in text), skeletal descriptions (<65 words), and talent pool phrasing.
  * Used a Snorkel-style Generative LabelModel to estimate LF accuracies unsupervised and generate probabilistic training targets.
* **Why it was built this way**:
  * Avoids treating a single hand-crafted rule as ground truth. Snorkel models the agreement and overlap between multiple noisy rules.
* **What could go wrong (Interview Defense)**:
  * **Trap**: *"Where did your training labels come from? Is there ground truth?"*
  * **Honest Answer**: *"There is no public ground truth for ghost postings. We used weak supervision as a proxy training target. The 180-sample set in `data/silver_labeling_sheet.csv` was generated using rule-based heuristics (`src/labeling/expert_annotate.py`), so it is a silver proxy set, not true human ground truth. To obtain real ground truth, we created a blind 80-listing sample in `data/BLIND_LABELING_SHEET_80.csv` for independent manual verification."*

---

### Module 4: Feature Engineering & Leakage Prevention (`src/features/`, `src/models/train_leakage_free_model.py`)

* **What it does**:
  * Engineered 73 features spanning text statistics, company disclosure scores, location tiers, and repost counts.
  * Implemented `LeakageFreeFeatureExtractor`: company-level statistics (e.g. historical ghost rate, posting frequency) are calculated **strictly inside training folds**.
  * Evaluated models using **5-Fold GroupKFold partitioned strictly by `company_name`**.
* **Why it was built this way**:
  * If listings from the same company appear in both training and test folds, the model simply memorizes company names rather than learning generalizable signals about job postings.
* **What could go wrong (Interview Defense)**:
  * For unseen companies with only one posting, company-level features default to global priors. The model must rely primarily on description text and posting attributes rather than company history.

---

### Module 5: Probability Calibration via Platt Scaling (`src/models/calibrator.py`)

* **What it does**:
  * Raw output scores from tree models (Random Forest, Gradient Boosting) are not true probabilities.
  * Fitted a Platt scaling logistic calibrator on out-of-fold predictions.
  * Reduced Brier score from **0.0188** to **0.0167** and Expected Calibration Error (ECE) from **0.0366** to **0.0220**.
* **Why it was built this way**:
  * If an application flags a job as having a 70% risk, users and recruiters need that 70% to reflect empirical risk, not an uncalibrated tree margin.
* **What could go wrong (Interview Defense)**:
  * Platt scaling assumes a monotonic sigmoidal relationship between raw log-odds and true probability. If the underlying distortion is non-monotonic, isotonic regression would fit more flexibly, but requires larger validation samples to avoid overfitting.

---

### Module 6: NLP Semantic Analysis & Text Similarity (`src/features/text_embeddings.py`)

* **What it does**:
  * Vectorized job descriptions using sublinear TF-IDF and projected them into a 64-dimensional latent semantic space via Randomized SVD (LSA).
  * Evaluated cross-company text similarity and extracted vagueness/buzzword density metrics.
* **Why it was built this way**:
  * Captures conceptual vocabulary overlap without requiring heavy, platform-dependent deep learning dependencies.
* **What could go wrong (Interview Defense)**:
  * **Trap**: *"You noticed high cosine similarity between descriptions across companies. Does that prove fraud or plagiarism?"*
  * **Honest Answer**: *"Not necessarily. In a 64-dimensional LSA projection, standard boilerplate language common to tech roles (e.g. 'agile environment', 'unit testing', 'collaborate with cross-functional teams') naturally compresses documents closer together. High similarity indicates boilerplate overlap, but should not be asserted as verified fraudulent copy-pasting without manual sentence-level diff checks."*

---

### Module 7: Local Explainability via TreeSHAP (`src/models/shap_explainer.py`)

* **What it does**:
  * Implemented additive TreeSHAP attribution: decomposes a prediction into baseline expectation $\phi_0$ plus per-feature contributions $\sum \phi_i = f(x)$.
  * Surfaces the top-3 risk factors (e.g. high listing age, skeletal description) and protective factors (e.g. detailed requirements, disclosed compensation) for any individual listing.
* **Why it was built this way**:
  * Single risk numbers without explanation frustrate users. SHAP values guarantee additive consistency and local accuracy.
* **What could go wrong (Interview Defense)**:
  * When features are correlated (e.g. `days_live` and `listing_age_bucket`), tree algorithms can split on either feature, distributing attribution across both.

---

### Module 8: Multi-Tool Verification Agent (`src/agent/verifier.py`)

* **What it does**:
  * An automated script that inspects a listing by invoking 4 tools: (1) ML Scorer, (2) Text Overlap Scanner, (3) Company Posting History, and (4) Salary Benchmark Lookup.
  * Produces a structured JSON audit report with evidence notes for human review.
* **Why it was built this way**:
  * For borderline cases ($0.40 \le P < 0.70$), relying on a single probability threshold is risky. Gathering multi-source evidence provides transparent context.
* **What could go wrong (Interview Defense)**:
  * **Trap**: *"Can the agent replace human verification?"*
  * **Honest Answer**: *"No. The agent automates heuristic data gathering. If the underlying data sources lack external validation (e.g., if we cannot ping the live company careers portal dynamically), the agent can only aggregate internal signals. It serves as an audit assistant, not an oracle."*

---

### Module 9: Production Serving & Chrome Extension (`src/api/main.py`, `06_Chrome_Extension/`)

* **What it does**:
  * A FastAPI service (`src/api/main.py`) exposes `/api/v1/score` with `<15ms` response latency.
  * The Chrome Extension (`06_Chrome_Extension/`) extracts live page metadata from LinkedIn, Indeed, Glassdoor, and Naukri.
  * **Zero-Knowledge Resume Privacy**: Resume matching is computed **100% locally in the browser** using client-side TF-IDF and PDF.js in `chrome.storage.local`. No resume text is ever sent over the network.
* **Why it was built this way**:
  * Respects candidate data privacy while delivering real-time utility directly within the browsing workflow.
* **What could go wrong (Interview Defense)**:
  * Job board DOM layouts update frequently. When site-specific selectors fail, the content script falls back to extracting the largest readable text block, which may occasionally capture header or navigation text.

---

### Module 10: Data Validation & Drift Monitoring (`src/monitoring/`)

* **What it does**:
  * `data_validation.py` uses Pandera to enforce strict schemas, valid ranges, and nullability constraints on datasets.
  * `drift_detector.py` computes Population Stability Index (PSI) between baseline and incoming scrape batches to detect data and concept drift.
* **Why it was built this way**:
  * Ensures that automated scrapers do not silently ingest corrupted or missing fields into production models.

---

## Summary of Key Factual Numbers (From `CLAIMS_LEDGER.csv`)

| Metric | Factual Value | How It Was Derived |
| :--- | :---: | :--- |
| **Analyzed Universe** | **2,851** | Deduplicated from 3,000 raw Apify scrapes across 3 portals. |
| **Cross-Sectional Mean Age** | **32.7 Days** | Average `days_live` at time of scrape (Median = 11.0 days, P90 = 128.0 days). |
| **Glassdoor Mean Age** | **63.8 Days** | Median = 41.0 days (older postings linger more on Glassdoor). |
| **Indeed Mean Age** | **0.3 Days** | Median = 0.0 days (scraped freshly posted listings). |
| **LinkedIn Mean Age** | **37.2 Days** | Median = 12.0 days. |
| **Platt Calibrated Brier Score** | **0.0167** | Evaluated on out-of-fold predictions (vs. 0.0188 raw). |
| **Calibrated ECE** | **0.0220** | Expected Calibration Error (vs. 0.0366 raw). |
| **GroupKFold OOF ROC-AUC** | **0.9961** | 5-Fold GroupKFold by employer evaluated on weak-supervision target. |
| **Test Suite** | **11 / 11 Passing** | Automated pytest suite covering API, leakage, calibration, and NLP. |
| **SQL Workbench** | **42 Queries** | Staging, cleaning, CTEs, and window ranking across 9 categories. |
| **Human Gold Sample** | **80 Listings** | Blind sheet prepared in `data/BLIND_LABELING_SHEET_80.csv` for true manual verification. |
