<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Functional%20Specification&fontSize=28&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf%20%C2%B7%20Functional%20Design&descAlignY=78&descSize=15)

</div>

Detailed inputs → processing → outputs → business rules for each functional component of Naukri Saaf.

<br/>

## FR-01 — SQL Staging, Transformation & Analytical Workbench

| Component | Specification |
|---|---|
| **Trigger** | Raw scrape ingestion from Apify (`glassdoor_jobs_scraped.csv`, `indeed_jobs_scraped.csv`, `linkedin_jobs_scraped.csv`) |
| **Input** | 3,000 raw text records with mixed date formats, unstructured salary strings, and dirty applicant counts. |
| **Process** | Ingestion into raw staging tables (`naukri_jobs_raw`), deduplication on `(title, company, location, date)` yielding 2,851 unique records, schema normalization, and execution of **42 production analytical queries across 9 analytical categories** in `02_SQL/naukri_saaf_sql_workbench.sql`. |
| **Output** | Fact table `naukri_jobs_fact`, dimensional tables, and analytical views (profiling, CTEs, window functions, and employer repost indexing). |
| **Business rule** | Raw staging tables are strictly immutable. Stored procedures and window functions must be deterministic and fully reproducible across MySQL and SQLite. |

<br/>

## FR-02 — Weak Supervision & Human Ground-Truth Benchmark

| Component | Specification |
|---|---|
| **Trigger** | Deduplicated dataset of 2,851 listings prepared for labeling. |
| **Input** | Behavioral signals (listing age, repost counts, application velocity) and textual metrics (semantic vagueness, lexical diversity). |
| **Process** | Implementation of **10 domain Labeling Functions (LFs)** combining behavioral and linguistic heuristics. A **Snorkel Generative LabelModel** estimates LF class conditional accuracies without ground truth. Concurrently, a **180-sample Silver Proxy Set** is generated via heuristic rules for pipeline smoke-testing, and a **blind 80-listing sample** (`data/BLIND_LABELING_SHEET_80.csv`) is generated with rubric (`LABELING_RUBRIC.md`) for independent human ground-truth verification. |
| **Output** | Probabilistic training labels ($P(\text{Ghost}) \in [0, 1]$) with Snorkel generative agreement ($\kappa=0.5890$ on silver set). |
| **Business rule** | Automated silver labels are explicitly documented as machine-generated proxies, not true human ground truth. |

<br/>

## FR-03 — Leakage-Free Feature Engineering & Grouped Model Evaluation

| Component | Specification |
|---|---|
| **Trigger** | Weak-supervised training corpus partitioned. |
| **Input** | 73 engineered features spanning listing age, compensation disclosure, 64-dimensional Dense Semantic LSA vectors, and lexical diversity scores. |
| **Process** | Target encoding and employer historical aggregations are fit strictly inside training folds via `LeakageFreeFeatureExtractor`. Evaluation performed using **5-Fold GroupKFold partitioned strictly by Employer** to prevent cross-fold entity leakage. Vectorized NumPy classifiers (GBM, Calibrated Random Forest, Logistic Regression, Stacking Ensemble) are trained and Platt-calibrated. |
| **Output** | Calibrated models achieving **ROC-AUC = 0.9200 on the silver proxy benchmark** with Platt calibration Brier score of 0.0167 (ECE = 0.0220). |
| **Business rule** | Zero employer-level aggregates may cross training/validation folds. Unseen test employers receive global single-post priors. |

<br/>

## FR-04 — Text Semantic Analysis & TreeSHAP Attribution

| Component | Specification |
|---|---|
| **Trigger** | Candidate listing processed for scoring. |
| **Input** | Raw JD text, title, company metadata, and trained ensemble tree models. |
| **Process** | 64-d Dense Semantic LSA embedding calculates cosine similarity across postings to inspect vocabulary overlap. Additive TreeSHAP computes feature contributions ($f(x) = \phi_0 + \sum \phi_i$). |
| **Output** | Auditable per-feature attribution vectors detailing top positive and negative risk contributors. |
| **Business rule** | Every high-risk prediction must expose top-3 positive and top-3 negative SHAP contributors to the client interface. |

<br/>

## FR-05 — Interactive Streamlit Dashboard

| Component | Specification |
|---|---|
| **Trigger** | Analyst or recruiter launches `streamlit run 05_Streamlit_Dashboard/app.py`. |
| **Input** | Model artifacts, SHAP matrices, and listing feature tables. |
| **Process** | Interactive dashboard featuring 7 core tabs: Overview, Platforms, Ghost Detection, Employers, Model Performance, Clustering, and Data Explorer with Single-Listing SHAP Inspector. |
| **Output** | Real-time interactive visualizations, dark-theme styling, and responsive filtering. |
| **Business rule** | Fallback-resilient: if server APIs are unreachable, app defaults smoothly to local offline data without throwing unhandled exceptions. |

<br/>

## FR-06 — Cross-Sectional Listing Age Profiling

| Component | Specification |
|---|---|
| **Trigger** | Listing freshness analysis trigger on posting metadata. |
| **Input** | `days_live` snapshot values at scrape time. |
| **Process** | Profiling distribution percentiles (P25, Median, P75, P90) across platforms and salary disclosure cohorts via `src/analytics/listing_age_analysis.py`. |
| **Output** | Empirical distribution showing overall mean age of **32.7 days** (median **11.0 days**), with Glassdoor exhibiting significantly older postings (mean **63.8 days**) than Indeed (mean **0.3 days**). |
| **Business rule** | Strictly reported as cross-sectional snapshot age at scrape time. No survival or delisting claims are permitted without longitudinal tracking. |

<br/>

## FR-07 — Listing Verification Agent

| Component | Specification |
|---|---|
| **Trigger** | Listing scores in borderline ambiguity tier ($0.40 \le P(\text{Ghost}) < 0.70$) or user requests deep-scan. |
| **Input** | Listing metadata, JD text, company name, salary range. |
| **Process** | Multi-tool automated agent (`src/agent/verifier.py`) executes 4 specialized tools: (1) ML Scorer, (2) Text Overlap Scanner, (3) Employer Historical Risk Profiler, (4) Market Salary Benchmark Validator. |
| **Output** | Structured JSON inspection report containing confidence score, risk level, tool evidence log, and actionable advice. |
| **Business rule** | Operates as an evidence-gathering audit assistant, not a definitive human oracle. |

<br/>

## FR-08 — Chrome Extension & FastAPI Scoring Service

| Component | Specification |
|---|---|
| **Trigger** | Jobseeker views job posting on LinkedIn, Indeed, Glassdoor, or Naukri. |
| **Input** | Live DOM extracted via `content.js`. |
| **Process** | Extension communicates via `POST /api/v1/score` with local FastAPI inference service (`src/api/main.py`), with offline heuristic fallback (`legitimacy.js`) if service is unreachable. |
| **Output** | Non-intrusive sidepanel detailing calibrated probability, SHAP risk drivers, and verification links. |
| **Business rule** | Sub-15ms response latency; candidate resumes parsed 100% locally via PDF.js into `chrome.storage.local` with zero network egress. |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README_BA_package.md">← Back to BA Package Index</a></i></div>
