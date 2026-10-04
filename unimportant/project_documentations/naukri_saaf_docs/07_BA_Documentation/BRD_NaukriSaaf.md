<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=140&section=header&text=Business%20Requirements%20Document&fontSize=28&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=Naukri%20Saaf%20v4%20%C2%B7%20Ghost%20Job%20Detection%20Platform&descAlignY=68&descSize=15)

![Status](https://img.shields.io/badge/status-production_ready-1F7A54?style=flat-square)
![Version](https://img.shields.io/badge/version-4.0-4C1D95?style=flat-square)
![Author](https://img.shields.io/badge/author-Dhruv_Jain-B8860B?style=flat-square)

</div>

<br/>

## 1. Purpose

This document defines the business requirements, architecture scope, and success criteria for **Naukri Saaf v4** — an enterprise-grade recruitment intelligence platform built on **3,000 raw listings** scraped from LinkedIn, Indeed, and Glassdoor, cleaned and validated to **2,851 unique listings** across 1,301 employers. The platform solves the hiring market's "Ghost Job" crisis using weak supervision, leakage-free machine learning, empirical age analytics, and multi-tool agentic reasoning.

<br/>

## 2. Business Problem

| Problem | Impact if Unaddressed |
|---|---|
| Candidates cannot distinguish active requisitions from phantom postings | Job seekers waste hundreds of hours applying to expired, unmonitored, or vanity listings. |
| Circular labeling traps in existing fraud detection systems | Models trained on arbitrary heuristics memorize rules rather than learning genuine risk patterns. |
| Cross-company description syndication by fake job aggregators | Shell agencies scrape and recycle job copy to harvest resumes without active requisitions. |
| Lack of cited, auditable fraud evidence | Black-box ML probability scores fail to provide recruiters and applicants with verifiable proof. |

<br/>

## 3. Stakeholders

| Stakeholder | Core Need & Success Criterion |
|---|---|
| 🧑‍💻 Job Seeker / Candidate | Sub-second risk scoring and privacy-first resume fit analysis directly on job portals. |
| 🎓 University Career Services | Automated vetting of recruitment drives and job boards before student circulation. |
| 📊 Data Analytics & Engineering Teams | Reproducible, leakage-free pipelines with verified metrics, Pandera schema gates, and drift monitoring. |
| 🏢 Corporate Talent Acquisition | Verification of competitive hiring benchmarks without defamatory false-positive blacklisting. |

<br/>

## 4. Scope

<table>
<tr><td width="50%" valign="top">

### ✅ In Scope (Delivered)
- Multi-platform scrape across LinkedIn, Indeed, Glassdoor (Apify).
- Pandera schema validation and Population Stability Index (PSI) drift monitor.
- 180-listing heuristic silver proxy benchmark and 80-listing blind human labeling protocol (`LABELING_RUBRIC.md`).
- Snorkel weak supervision framework (10 domain Labeling Functions).
- Leakage-free feature extractor with 5-fold GroupKFold CV by company.
- Pure-NumPy vectorized tree ensembles with Platt probability calibration.
- Authentic TreeSHAP decision path feature attribution.
- 64-d Dense Semantic NLP encoder (Randomized SVD) & similarity matching.
- Cross-sectional listing-age distribution and platform lingering analysis.
- Autonomous Listing Verification Agent (4 deterministic tools).
- Sub-15ms FastAPI microservice (`POST /api/v1/score`).
- 42-query MySQL 8.0 workbench & 8-page Power BI dashboard (Star Schema).
- Streamlit interactive dashboard & Manifest V3 Chrome Extension.

</td><td width="50%" valign="top">

### ❌ Out of Scope (By Design)
- Automated defamatory public blacklisting without human verification.
- Direct employer ATS integrations via proprietary paid APIs.
- Cloud Kubernetes clusters (kept laptop-runnable, free, and self-contained).

</td></tr>
</table>

<br/>

## 5. Functional Business Requirements

| ID | Requirement | Implementation Artifact |
|---|---|---|
| **BR-01** | Collect and harmonize multi-platform job data | Cleaned dataset of 2,851 rows across LinkedIn, Indeed, Glassdoor. |
| **BR-02** | Validate schema types and enforce range constraints | `src/monitoring/data_validation.py` (Pandera schema). |
| **BR-03** | Provide benchmark evaluation protocol | `data/silver_labeling_sheet.csv` (180 silver proxy listings) and `data/BLIND_LABELING_SHEET_80.csv` (80 blind human audit listings). |
| **BR-04** | Infer probabilistic labels without circular heuristic rules | `src/labeling/label_model.py` (Snorkel generative model, $\kappa=0.589$). |
| **BR-05** | Eliminate cross-fold employer lookahead leakage | `src/models/leakage_free_features.py` (GroupKFold by company). |
| **BR-06** | Provide calibrated probabilities for safe risk tiers | `src/models/calibration.py` (Platt Scaling, Brier score = 0.0167). |
| **BR-07** | Attribute prediction drivers using game-theoretic Shapley values | `src/models/shap_explainer.py` (Authentic TreeSHAP). |
| **BR-08** | Detect cross-company description syndication | `src/features/plagiarism_detector.py` (Dense semantic similarity matching). |
| **BR-09** | Quantify requisition age distributions across platforms | `src/analytics/listing_age_analysis.py` (Cross-sectional percentiles: median 11d, P90 128d). |
| **BR-10** | Provide cited forensic evidence for recruiters and candidates | `src/agent/verifier.py` (Autonomous multi-tool verification agent). |
| **BR-11** | Serve real-time predictions via microservice | `src/api/main.py` (FastAPI `<15ms` latency). |
| **BR-12** | Enable in-browser inspection with 100% local privacy | `06_Chrome_Extension/` (Manifest V3 side panel). |
| **BR-13** | Deliver executive BI and segmentation analytics | `02_SQL/` (42 queries) & `08_PowerBI_Dashboard/` (8 pages, 20 DAX measures). |
