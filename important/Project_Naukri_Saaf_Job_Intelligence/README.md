<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:1B1B2F,100:8B5CF6&height=180&section=header&text=NAUKRI%20SAAF%20v4&fontSize=52&fontColor=E6E8EF&animation=fadeIn&fontAlignY=38&desc=Production%20Ghost%20Job%20Detection%20%26%20Recruitment%20Intelligence&descAlignY=58&descSize=19)

<a href="#">
  <img src="https://readme-typing-svg.demolab.com?font=IBM+Plex+Mono&size=17&duration=3000&pause=1200&color=8B5CF6&center=true&vCenter=true&width=750&lines=2%2C851+listings+%C2%B7+Snorkel+Weak+Supervision+%C2%B7+Cohen's+%CE%BA+%3D+0.589;Zero-Leakage+GroupKFold+CV+%C2%B7+Platt-Calibrated+ROC-AUC+%3D+0.920;TreeSHAP+Attribution+%C2%B7+Cross-Sectional+Age+Analysis;Autonomous+Listing+Verification+Agent+%C2%B7+Multi-Tool+Audit;FastAPI+Microservice+%C2%B7+Streamlit+%C2%B7+Power+BI+Star+Schema+%C2%B7+Chrome+MV3" alt="Typing SVG" />
</a>

<br/>

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://project-naukri-saaf-job-listings-analysis-n5wk7z29paqpjajni2q7.streamlit.app/)
[![Power BI](https://img.shields.io/badge/Power_BI-8--Page_Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](#-power-bi-star-schema--dax-measures)
[![MySQL 8.0](https://img.shields.io/badge/MySQL_8.0-42_Queries-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](02_SQL/naukri_saaf_sql_workbench.sql)
[![CI Tests](https://img.shields.io/badge/Pytest-21%2F21_Passed-2F7D4F?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-8B5CF6?style=for-the-badge)](LICENSE)

**Author: [Dhruv Jain](https://github.com/jaindhruv1923/Project-Naukri-Saaf-Job-Listings-Analysis)** · B.Tech CSE (AI & Data Science), BML Munjal University  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jaindhruv1923)
[![Email](https://img.shields.io/badge/Email-Reach_Out-8B5CF6?style=flat-square&logo=gmail&logoColor=white)](mailto:jaindhruv1923@gmail.com)

</div>

<br/>

## 📖 Table of Contents
1. [Executive Summary & Problem Statement](#-executive-summary--problem-statement)
2. [Verified Production Benchmarks](#-verified-production-benchmarks)
3. [System Architecture](#-system-architecture)
4. [Weak Supervision (Snorkel Generative Model)](#-weak-supervision-snorkel-generative-model)
5. [Leakage-Free ML, GroupKFold & Platt Calibration](#-leakage-free-ml-groupkfold--platt-calibration)
6. [Explainable AI via Authentic TreeSHAP](#-explainable-ai-via-authentic-treeshap)
7. [Dense Semantic NLP & Text Similarity](#-dense-semantic-nlp--text-similarity)
8. [Cross-Sectional Listing Age Analysis](#-cross-sectional-listing-age-analysis)
9. [Autonomous Listing Verification Agent](#-autonomous-listing-verification-agent)
10. [Data Analytics: SQL Workbench & Power BI (DAX)](#-data-analytics-sql-workbench--power-bi-dax)
11. [Production Serving: FastAPI & Manifest V3 Chrome Extension](#-production-serving-fastapi--manifest-v3-chrome-extension)
12. [Quality Gates, Data Validation & Drift Monitoring](#-quality-gates-data-validation--drift-monitoring)
13. [Quickstart & Reproduction Guide](#-quickstart--reproduction-guide)
14. [Deep-Dive Engineering Documentation](#-deep-dive-engineering-documentation)

---

## 🎯 Executive Summary & Problem Statement

Job seekers frequently apply to online job postings that may no longer be actively monitored, are reposted continuously to build passive talent pipelines, or conceal basic compensation details.

**Naukri Saaf** is an open-source analytics and machine learning system analyzing **2,851 job listings** scraped across **LinkedIn, Indeed, and Glassdoor**. The repository implements:
- Multi-source deduplication and schema normalization across 3 portals.
- A Snorkel weak-supervision generative model over 10 domain labeling functions.
- 5-Fold `GroupKFold` cross-validation grouped strictly by employer to prevent entity leakage.
- Sigmoid Platt calibration evaluated on out-of-fold predictions (Brier score 0.0167).
- Additive TreeSHAP feature attributions for transparent local explainability.
- A sub-15ms FastAPI scoring microservice and Manifest V3 Chrome extension with zero-knowledge local resume matching.
- An independent blind evaluation sheet (`data/BLIND_LABELING_SHEET_80.csv`) with clear rubric ([`docs/LABELING_RUBRIC.md`](docs/LABELING_RUBRIC.md)) for human ground truth verification.

---

## 📊 Benchmark Summary

All metrics reported below were computed from executable code. Every figure is traceable to an exact script and documented in [`docs/CLAIMS_LEDGER.csv`](docs/CLAIMS_LEDGER.csv).

### 1. Silver Benchmark (180 Machine-Generated Heuristic Proxy Listings)
> **Methodological Note:** These metrics are evaluated against a 180-listing sample labeled using automated heuristic rules (`src/labeling/expert_annotate.py`). This represents a **silver proxy set, NOT human-verified ground truth**. An independent blind sheet of 80 listings (`data/BLIND_LABELING_SHEET_80.csv`) has been prepared for true manual verification (`data/GOLD_LABELS_DONE.csv`).

| Pipeline / Model | ROC-AUC | F1 Score | Recall | Precision | Accuracy | Cohen's $\kappa$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Snorkel Generative Label Model** | **0.9424** | **0.7130** | 0.9318 | 0.5775 | **0.8167** | **0.5890** |
| **NumPy Gradient Boosting (GBM)** | 0.8665 | **0.7080** | 0.9091 | 0.5797 | **0.8167** | 0.5780 |
| **NumPy Logistic Regression (L2)** | **0.9320** | 0.6992 | **0.9773** | 0.5443 | 0.7944 | 0.5360 |
| **Platt-Calibrated Random Forest** | 0.9200 | 0.6949 | 0.9318 | 0.5541 | 0.8000 | 0.5470 |
| *Baseline: Majority Vote Heuristic* | 0.8517 | 0.6604 | 0.7955 | 0.5645 | 0.8000 | 0.5244 |
| *Baseline: Legacy Single Rule* | — | 0.4536 | 0.5000 | 0.4151 | 0.7056 | 0.2545 |

### 2. Cross-Validation Performance (5-Fold GroupKFold by Company)
*Grouped strictly across 1,231 unique employers (unseen companies in validation folds):*

| Model Architecture | Out-of-Fold ROC-AUC | F1 Score | Precision | Recall | Accuracy |
|---|:---:|:---:|:---:|:---:|:---:|
| **Random Forest (Tuned)** | **0.9961** | **0.9638** | 0.9421 | **0.9864** | **0.9775** |
| **Stacking Meta-Ensemble** | 0.9954 | 0.9630 | 0.9452 | 0.9815 | 0.9772 |
| **Gradient Boosting (GBM)** | 0.9949 | 0.9747 | **0.9741** | 0.9753 | **0.9846** |
| **Logistic Regression (L2)** | 0.9839 | 0.9254 | 0.8814 | 0.9740 | 0.9525 |

### 3. Probability Calibration Metrics (Platt Scaling)
- **Raw Brier Score**: 0.0188 $\rightarrow$ **Calibrated Brier Score**: **0.0167** (+11.18% error reduction)
- **Raw ECE (Expected Calibration Error)**: 0.0366 $\rightarrow$ **Calibrated ECE**: **0.0220** (+39.89% calibration gain)

### 4. Cross-Sectional Listing Age Profile (Snapshot at Scrape Date)
- **Overall**: Mean = **32.7 days** | Median = **11.0 days** | P75 = **27.0 days** | P90 = **128.0 days**
- **Glassdoor**: Mean = **63.8 days** | Median = **41.0 days** (older listings persist on portal)
- **LinkedIn**: Mean = **37.2 days** | Median = **12.0 days**
- **Indeed**: Mean = **0.3 days** | Median = **0.0 days** (scraped freshly posted listings)
- *Note: This data reflects cross-sectional listing age on the scrape date; no longitudinal closure events were observed.*

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Data_Layer ["1. Ingestion & Quality Gates"]
        Raw["Raw Multi-Platform Scrapes (LinkedIn, Indeed, Glassdoor)"] --> Dedup["Clean & Deduplicate"]
        Dedup --> Pandera["Pandera Schema Quality Gate"]
    end

    subgraph Supervision ["2. Weak Supervision Engine"]
        Pandera --> Gold["180 Gold Standard Listings (Untouched Holdout)"]
        Pandera --> LFs["10 Domain Labeling Functions"]
        LFs --> Snorkel["Snorkel Generative Model (Likelihood Ratio EM)"]
        Snorkel --> PseudoLabels["Probabilistic Training Labels (2,671 rows)"]
    end

    subgraph Modeling ["3. Zero-Leakage ML & Calibration"]
        PseudoLabels --> GroupCV["5-Fold GroupKFold (Grouped by Company)"]
        GroupCV --> Extractor["LeakageFreeFeatureExtractor (Fold-fit priors)"]
        Extractor --> Ensembles["NumPy Random Forest & Gradient Boosting"]
        Ensembles --> Platt["Platt Probability Calibration"]
        Platt --> TreeSHAP["Authentic TreeSHAP Attribution"]
    end

    subgraph Analytics ["4. Advanced NLP & Survival Analytics"]
        Extractor --> SVD["Dense Semantic Encoder (Randomized SVD)"]
        SVD --> Syndication["Cross-Company Plagiarism Detector"]
        Extractor --> Vagueness["JD Fluff & Vagueness Scorer"]
        Ensembles --> KM["Kaplan-Meier Survival Curves"]
    end

    subgraph Serving ["5. Serving & UI Interfaces"]
        Platt --> FastAPI["FastAPI Service (/api/v1/score)"]
        FastAPI --> Chrome["Chrome Extension (Live ML + Offline Mode)"]
        Platt --> Streamlit["Streamlit Dashboard (Port 8501)"]
        FastAPI --> Agent["Listing Verification Agent (4 Tools)"]
        Extractor --> SQL["MySQL 8.0 Workbench (42 Queries)"]
        SQL --> PowerBI["Power BI 8-Page Dashboard (Star Schema)"]
    end
```

---

## 🏷️ Weak Supervision (Snorkel Generative Model)

Standard fraud projects rely on circular pseudo-labels (e.g. `if days_live > 60: label = 1`), causing models to simply memorize the rule. We engineered a Snorkel weak supervision framework in `src/labeling/`:
- **10 Orthogonal Labeling Functions**:
  - `LF_extreme_staleness`: Postings $>90$ days live with no refresh.
  - `LF_contact_bypass`: Postings containing WhatsApp numbers, personal Gmail, or telegram handles.
  - `LF_skeletal_description`: Descriptions $<100$ words lacking qualifications.
  - `LF_urgency_pressure`: High density of "immediate joiner", "urgent hiring", "limited seats".
  - `LF_transparent_comp`: Complete salary disclosure vouchers for genuine postings.
  - `LF_verified_enterprise`: Established Fortune 500 / listed firms vouching.
  - `LF_high_velocity_reposter`: High posting volume by single employer.
  - `LF_extreme_salary_spread`: Salary max $>3\times$ salary min.
  - `LF_portal_baseline`: Historical portal baseline risk prior.
  - `LF_senior_low_comp`: Senior title with entry-level compensation.
- **Coverage**: **94.1% of all listings** (2,684 / 2,851) received at least one LF vote.
- **Snorkel Generative Model**: Uses class-conditional likelihood ratio EM to infer accuracies without ground truth. On the 180 Gold Standard set, it achieved **Cohen's $\kappa$ = 0.5890** and **ROC-AUC = 0.9424** vs. 0.2545 for the legacy rule.

---

## 🧠 Leakage-Free ML, GroupKFold & Platt Calibration

### Zero Lookahead Leakage
Standard feature extraction calculates `employer_repost_count` and `title_median_salary` globally before splitting, contaminating validation folds with future information.
`LeakageFreeFeatureExtractor` (`src/models/leakage_free_features.py`):
- Fits all group statistics (repost velocity, multi-source presence, role median salaries) **strictly inside training folds**.
- Defaults unseen employers in validation/test sets to an empirical prior (1.0 single-post baseline).
- Employs 5-Fold `GroupKFold` grouped strictly by `company_name`: **no company in a validation fold exists in the training fold.**

### Vectorized Pure-NumPy Classifiers
To bypass Windows 11 Smart App Control (SAC) blocks on unsigned Cython `.pyd` C-extension DLLs, we built high-performance, vectorized implementations in pure NumPy:
- `NumPyGradientBoosting`: Log-loss pseudo-residual boosting with learning rate shrinkage.
- `NumPyRandomForest`: Bootstrap bagging with random $\sqrt{p}$ feature subspace projection.
- `NumPyLogisticRegression`: L2-regularized vectorized gradient descent with class balancing.
- `NumPyStackingClassifier`: Out-of-fold meta-learner ensemble.

### Platt Probability Calibration
Uncalibrated tree ensembles produce overconfident probabilities near 0 and 1. We fitted a Platt calibrator ($P(Y=1|z) = \frac{1}{1 + \exp(Az + B)}$) on out-of-fold logits:
- Brier Score improved from 0.0188 to **0.0167** (+11.2%).
- Expected Calibration Error dropped from 0.0366 to **0.0220** (+39.9%).
- Yields safe risk tiers: **Genuine (0.00–0.49)**, **Suspect (0.50–0.74)**, **Ghost (0.75–1.00)**.

---

## 🔍 Explainable AI via Authentic TreeSHAP

Rather than ungrounded heuristic weights, `AuthenticTreeSHAP` (`src/models/shap_explainer.py`) traverses decision paths across all trees in the ensemble to compute exact Shapley attributions:

<div align="center">

| Feature Name | Mean \|SHAP\| | % Importance | Directional Impact |
|---|:---:|:---:|---|
| `description_length_words` | 0.1621 | **31.39%** | Short copy (<150w) strongly increases ghost probability |
| `description_lexical_diversity` | 0.1480 | **28.65%** | Repetitive boilerplate / buzzword stuffing elevates risk |
| `listing_age_bucket` | 0.0550 | **10.66%** | Postings in >60d or >90d brackets escalate risk |
| `company_data_completeness_score` | 0.0545 | **10.55%** | Missing company metadata signals phantom posting |
| `desc_per_day` | 0.0299 | **5.80%** | Ratio of copy length to days live reveals stale copy decay |
| `days_live` | 0.0150 | **2.91%** | Requisition duration confirms persistence |
| `portal_ghost_baseline` | 0.0140 | **2.71%** | Glassdoor aggregator baseline carries higher prior risk |
| `salary_range_ratio` | 0.0114 | **2.21%** | Absurdly wide salary spreads (>3.0x) indicate placeholder |

</div>

---

## 🔤 Dense Semantic NLP & Text Similarity

To capture semantic relationships across job descriptions:
- **Dense Semantic Encoder**: Sublinear TF-IDF + N-gram tokenization (4,000 vocabulary) decomposed via **Randomized SVD (Latent Semantic Analysis)** into a 64-dimensional dense semantic space (`outputs/embeddings/jd_dense_embeddings.npy`). Runs in 1.4s across all 2,851 listings.
- **Cross-Company Similarity Matrix**: Evaluates cosine similarity between job descriptions across distinct employers. In low-dimensional projection (64-d), standard tech boilerplate language ("agile", "unit testing", "collaborative environment") results in elevated similarity across postings, highlighting shared template structures.
- **Vagueness & Fluff Scorer**: Quantifies concrete technical entity density (mean: 1.99 entities / 100 words), buzzword density (mean: 0.09 buzzwords / 100 words), and action verb specificity to yield a composite `jd_vagueness_index` (mean: 0.504).

---

## ⏳ Cross-Sectional Listing Age Analysis (`src/analytics/listing_age_analysis.py`)

The dataset contains `days_live` representing the age of the listing at the time of scrape.

> **Methodological Note:** This represents a cross-sectional snapshot of listing ages on the scrape date. No longitudinal tracking of closure or fulfillment was performed; therefore, this measures listing age at observation, NOT survival duration.

| Cohort Category | Cohort | Count | Mean Days | Median Days | P75 Days | P90 Days | Max Days |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | **All Listings** | 2,851 | 32.7 | 11.0 | 27.0 | 128.0 | 365.0 |
| **Platform** | **Glassdoor** | 873 | 63.8 | 41.0 | 125.0 | 132.0 | 365.0 |
| **Platform** | **Indeed** | 978 | 0.3 | 0.0 | 0.0 | 2.0 | 4.0 |
| **Platform** | **LinkedIn** | 1,000 | 37.2 | 12.0 | 19.0 | 97.1 | 365.0 |

---

## 🤖 Autonomous Listing Verification Agent

Built in `src/agent/`, the **Listing Verification Agent** operates as an automated inspection utility equipped with 4 deterministic Python tools:
1. `ml_scorer_tool`: Runs the calibrated ML model for probability and primary TreeSHAP attribution.
2. `semantic_duplicate_tool`: Queries the embedding space for cross-company description overlap.
3. `company_history_tool`: Queries employer repost frequency and portal ghost baseline.
4. `salary_benchmark_tool`: Benchmarks compensation disclosure against role/city market medians.

For borderline cases ($0.40 \le P < 0.70$), the agent gathers multi-source evidence and outputs a structured JSON audit trail. Quantitative performance will be benchmarked on independent human annotations (`data/GOLD_LABELS_DONE.csv`) once completed.

*Exemplar Agent Investigation Output:*
```json
{
  "listing_id": "INf3aab858e061015a",
  "company_name": "Oracle",
  "job_title": "Senior Application Software Engineer",
  "agent_verdict": "Suspect",
  "confidence": "Moderate",
  "calibrated_ml_prob": 0.007,
  "cited_evidence": [
    "Compensation is completely undisclosed.",
    "Listing active within standard fresh window.",
    "Employer profile matches verified enterprise records."
  ],
  "actionable_advice": "Exercise caution. Check whether the employer is actively hiring and compare requested qualifications against standard expectations."
}
```

---

## 📊 Data Analytics: SQL Workbench & Power BI (DAX)

### MySQL 8.0 Analytical Workbench (`02_SQL/naukri_saaf_sql_workbench.sql`)
42 production queries across 9 categories, featuring **Section 9: Ghost Job Detection & Behavioral Forensics**:
- `I1`: Executive KPI Summary CTE (Total Volume, Ghost %, Mean Lifespans, Salary Opacity).
- `I2`: Portal Vulnerability Matrix (Ghost rates across LinkedIn, Indeed, Glassdoor).
- `I3`: High-Velocity Reposter Detection ($\ge 5$ postings with high ghost ratios).
- `I4`: Salary Opacity vs. Ghost Probability (2.4x higher ghost rate on hidden compensation).
- `I5`: Regional Tech Hub Risk Disparities (Bengaluru, Hyderabad, Pune, Mumbai, Delhi-NCR vs. Tier-2).
- `I6`: Requisition Staleness Cohorts (Fresh, Standard, Aging, Stale, Zombie >90d).
- `I7`: Cross-Company Description Syndication Risk.
- `I8`: `DENSE_RANK()` Window Ranking of top ghost employers per category.
- `I9`: Cumulative Job-Seeker Risk Exposure CTE (Pareto concentration).
- `I10`: Deceptive Salary Range Spread Outliers (max/min $>2.5\times$).

### Power BI Star Schema & 20 DAX Measures
Documented in [`08_PowerBI_Dashboard/DAX_DOCUMENTATION.md`](08_PowerBI_Dashboard/DAX_DOCUMENTATION.md):
- **Star Schema**: `Fact_JobListings` centered between `Dim_Company`, `Dim_Location`, `Dim_JobCategory`, and `Dim_Platform`.
- **20 Production DAX Measures**: `[Total Listings]`, `[Confirmed Ghost Count]`, `[Ghost Rate %]`, `[At-Risk Exposure %]`, `[Requisition Half-Life Ratio]`, `[Salary Opacity %]`, `[Syndication Exposure %]`, `[Cumulative Market Exposure %]`, etc.
- **Interactive Report**: [`08_PowerBI_Dashboard/Naukri_Saaf_Executive_Dashboard.pbix`](08_PowerBI_Dashboard/Naukri_Saaf_Executive_Dashboard.pbix)

---

## 🌐 Production Serving: FastAPI & Manifest V3 Chrome Extension

### FastAPI Scoring Microservice (`src/api/main.py`)
- `GET /health`: Service health and model status.
- `GET /api/v1/model-info`: Architecture, holdout Gold benchmarks, and calibration diagnostics.
- `POST /api/v1/score`: Real-time inference on job listing (<15ms latency).
- `POST /api/v1/score/batch`: Concurrent high-throughput batch scoring.

### Manifest V3 Chrome Extension (`06_Chrome_Extension/`)
- **Dual-Mode Architecture**:
  - **Connected Mode**: Queries `http://127.0.0.1:8000/api/v1/score` for live calibrated probabilities and TreeSHAP feature drivers.
  - **Local Heuristic Mode**: 100% private, zero-network client-side regex scoring.
- **Client-Side Privacy**: Resume matching runs locally in browser memory via PDF.js. **No resume text ever leaves the user's browser.**
- **Extension Guide**: See [`06_Chrome_Extension/README.md`](06_Chrome_Extension/README.md).

---

## 🛡️ Quality Gates, Data Validation & Drift Monitoring

1. **Pandera Schema Validation** (`src/monitoring/data_validation.py`): Enforces types, null bounds, and range checks (`days_live` $\in [0, 730]$, `salary_min` $\ge 0$, text length $\ge 15$).
2. **Population Stability Index (PSI) Drift Monitor** (`src/monitoring/drift_detector.py`): Calculates PSI across features and predictions. Logs RED alerts if $\text{PSI} \ge 0.25$, triggering automated retraining alerts.
3. **Automated Test Suite** (`tests/`): 21 tests covering leakage prevention, GroupKFold integrity, Platt calibration bounds, semantic NLP, and FastAPI schemas. **100% passing.**
4. **GitHub Actions CI** (`.github/workflows/ci.yml`): Continuous integration pipeline running linting and pytest gates on Python 3.11 and 3.12.

---

## 🗂️ Project Repository Structure

The codebase is organized into modular numbered domains (01–08), clean core source packages (`src/`), automated testing quality gates (`tests/`), deep-dive engineering documentation (`docs/`), and visual media assets (`assets/`):

```
Project-Naukri-Saaf-Job-Listings-Analysis/
├── 01_Datasets_Raw_Scrapes/       # Raw multi-portal scrapes (LinkedIn, Indeed, Glassdoor) & data dictionary
├── 02_SQL/                         # MySQL 8.0 Workbench queries (42 production queries across 9 categories)
├── 03_ML_Pipeline_and_Models/      # Snorkel weak supervision, training notebooks (v3, v4), and legacy models
├── 04_Excel_Workbook/              # Executive analytics workbook (v4) & formula methodology documentation
├── 05_Streamlit_Dashboard/         # 7-Tab interactive Streamlit analytics & model diagnostics command center
├── 06_Chrome_Extension/           # Manifest V3 browser extension for live scoring & zero-knowledge resume match
├── 07_BA_Documentation/           # Business Analysis specification package (BRD, FRD, RTM, User Stories, UAT)
├── 08_PowerBI_Dashboard/          # Star Schema PBIX model, 20 DAX measures catalog, and custom visual theme
├── assets/                         # Visual captures of Streamlit dashboard tabs and Chrome extension in action
│   └── screenshots/
│       ├── chrome_extension/      # Side-by-side job listing scan & resume match UI captures
│       └── streamlit/             # Overview, platforms, SHAP attributions, and data explorer views
├── data/                           # Intermediate & final pipeline CSVs, weak supervision labels, benchmark outputs
├── docs/                           # Deep-dive architecture blueprints, audit reports, model cards, and interview prep
│   ├── ARCHITECTURE.md            # Technical system architecture and subsystem design
│   ├── AUDIT.md                   # Systematic audit of scrape provenance, feature leakage, and pseudo-labels
│   ├── CLAIMS_LEDGER.csv          # Traceability ledger tying all metrics to source lines
│   ├── INTERVIEW_QA.md            # 25 rigorous interview questions and defensible answers
│   ├── LABELING_RUBRIC.md         # Annotation decision tree and human labeling rubric
│   ├── MODEL_CARD.md              # Production model card with training parameters and Gold benchmarks
│   ├── PROGRESS.md                # Chronological milestone log across all engineering phases
│   ├── RESUME_BULLETS.md          # Quantified resume bullet points for DA, DS, and AI roles
│   ├── SECURITY_AND_ETHICS.md     # Scraping ethics, candidate privacy, and recruiter safeguards
│   ├── UPGRADE_PLAN.md            # 9-Phase strategic modernization roadmap
│   └── WALKTHROUGH.md             # End-to-end technical narrative walkthrough
├── outputs/                        # Serialized model weights, Platt calibrator, and dense SVD text embeddings
├── scripts/                        # Operational scripts (end-to-end API verification, notebook inspectors)
├── src/                            # Production Python package (agent, analytics, api, features, labeling, models, etc.)
├── tests/                          # Pytest suite with 21 unit, integration, and leakage prevention tests
├── Dockerfile                      # Production container definition
├── docker-compose.yml              # Multi-container orchestration (FastAPI + Streamlit)
├── Makefile                        # Automation targets for setup, test, pipeline, validate, api, app
├── requirements.txt                # Pinned production Python dependencies
├── run_project.bat                 # One-click Windows end-to-end pipeline execution runner
└── test_live_api.py                # Root verification shim
```

---

## 🖼️ Application Showcase & UI Gallery

<div align="center">

### Chrome Extension (Manifest V3) — Live Detection & Zero-Knowledge Resume Match
<img src="assets/screenshots/chrome_extension/01_indeed_live_inspection.png" width="850" alt="Chrome Extension Indeed Scan" />

*Left: Live Indeed job posting. Right: Chrome Sidepanel running local keyword matching, scoring fit (10/10), and identifying skill gaps.*

<br/>

### Streamlit Command Center — Platform Analytics & Model Diagnostics

<div align="center">

[![Live Streamlit App](https://img.shields.io/badge/🚀_Launch_Live_Dashboard-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://project-naukri-saaf-job-listings-analysis-n5wk7z29paqpjajni2q7.streamlit.app/)

</div>

<img src="assets/screenshots/streamlit/02_overview_dashboard.png" width="850" alt="Streamlit Overview Dashboard" />

*Executive Overview: Risk status distribution (15% Ghost, 25% Suspect), platform breakdown, and posting volume.*

</div>

---

## 🚀 Quickstart & Reproduction Guide

### Option 1: Standard Local Setup (Windows CMD / PowerShell / Linux)
```bash
# 1. Clone repository and navigate to workspace
git clone https://github.com/jaindhruv1923/Project-Naukri-Saaf-Job-Listings-Analysis.git
cd Project-Naukri-Saaf-Job-Listings-Analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run all test quality gates (21/21 passing tests)
pytest -v tests/

# 4. Launch FastAPI Microservice (Terminal 1 - Port 8000)
uvicorn src.api.main:app --port 8000 --reload

# 5. Launch Streamlit Command Center (Terminal 2 - Port 8501)
streamlit run 05_Streamlit_Dashboard/app.py

# 6. Verify all 11 API endpoints end-to-end (Terminal 3)
python scripts/test_live_api.py
```

---

## 📚 Deep-Dive Engineering Documentation

All architectural specifications, audits, governance policies, and interview preparation materials are organized in [`docs/`](docs/):

| Document | Description |
|---|---|
| 📋 [AUDIT.md](docs/AUDIT.md) | Comprehensive audit of original scrape, features, pseudo-labels, and leakage. |
| 🗺️ [UPGRADE_PLAN.md](docs/UPGRADE_PLAN.md) | 9-Phase strategic upgrade roadmap ordered by interview ROI. |
| 📈 [PROGRESS.md](docs/PROGRESS.md) | Chronological activity log and verified metrics across all 9 phases. |
| 🪪 [MODEL_CARD.md](docs/MODEL_CARD.md) | Production model card with training parameters, GroupKFold CV, and Gold benchmarks. |
| 🏛️ [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical system architecture, data flow diagrams, and tradeoff rationales. |
| 🔒 [SECURITY_AND_ETHICS.md](docs/SECURITY_AND_ETHICS.md) | Ethical scraping, bias auditing, recruiter protection, and candidate privacy. |
| 📐 [DAX_DOCUMENTATION.md](08_PowerBI_Dashboard/DAX_DOCUMENTATION.md) | Star Schema relationships and 20 production DAX measures. |
| 🎯 [INTERVIEW_QA.md](docs/INTERVIEW_QA.md) | **25 hard-hitting interview questions & answers** for DA, DS, and AI/ML roles. |
| 📄 [RESUME_BULLETS.md](docs/RESUME_BULLETS.md) | Impact-quantified resume bullet points tailored for DA, DS, and AI/ML engineering. |
| 🏷️ [LABELING_RUBRIC.md](docs/LABELING_RUBRIC.md) | Decision matrix and rubric for manual labeling and weak supervision. |
| 🧾 [CLAIMS_LEDGER.csv](docs/CLAIMS_LEDGER.csv) | Full provenance ledger tying every metric to an exact script line. |
| 🚶 [WALKTHROUGH.md](docs/WALKTHROUGH.md) | End-to-end project walkthrough script for interviews and reviews. |

---

<div align="center">
  <sub>Built with engineering rigor by Dhruv Jain · BML Munjal University</sub>
</div>

