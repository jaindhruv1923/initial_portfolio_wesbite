<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=KPI%20%26%20Success%20Metrics&fontSize=28&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf%20%C2%B7%20Analytics%20Validation&descAlignY=78&descSize=15)

</div>

This document tracks **verified build-time engineering metrics** against baseline targets, and outlines **operational service-level metrics** for production deployment.

<br/>

## 1. Verified Build-Time Engineering Metrics

Metrics below are computed from executable code against our **180-listing silver proxy set** (`data/silver_labeling_sheet.csv`) and GroupKFold cross-validation:

| Metric Category | Target Baseline | Actual Value | Verified Artifact / Code | Status |
|---|:---:|:---:|---|:---:|
| **Weak Supervision Cohen's $\kappa$** | > 0.35 | **0.5890** (+131% gain) | `src/labeling/evaluate_labels.py` | ✅ Verified |
| **Weak Supervision Silver F1** | > 0.50 | **0.7130** (+57% gain) | `data/gold_evaluation_results.csv` | ✅ Verified |
| **GroupKFold Out-of-Fold AUC** | > 0.80 | **0.9961** (Unseen Employers) | `data/model_benchmark_group_cv.csv` | ✅ Verified |
| **Silver Benchmark ROC-AUC** | > 0.80 | **0.9200** (Calibrated RF) | `data/model_benchmark_gold_test.csv` | 🟡 Silver Proxy |
| **Silver Benchmark F1 Score** | > 0.60 | **0.7080** (GBM) / **0.6949** (RF) | `data/model_benchmark_gold_test.csv` | 🟡 Silver Proxy |
| **Silver Benchmark Ghost Recall** | > 0.75 | **0.9318** (RF) | `data/model_benchmark_gold_test.csv` | 🟡 Silver Proxy |
| **Platt Calibrated Brier Score** | < 0.025 | **0.0167** (+11.2% gain) | `data/calibration_metrics_v4.csv` | ✅ Verified |
| **Expected Calibration Error (ECE)** | < 0.050 | **0.0220** (-40% error) | `data/calibration_metrics_v4.csv` | ✅ Verified |
| **Cross-Sectional Mean Age** | — | **32.7 Days** (Median 11.0d) | `data/listing_age_distribution.csv` | ✅ Verified |
| **High Cosine Similarity Rate (64-d LSA)**| — | **54.47%** ($\ge 0.85$ sim) | `data/cross_company_plagiarism.csv` | ⚠️ LSA Overlap |
| **FastAPI Real-Time Latency** | < 50ms | **< 15ms** | `src/api/main.py` | ✅ Verified |
| **Pytest Quality Gate Pass Rate** | 100% | **100% (11 / 11 tests passed)** | `tests/` | ✅ Verified |
| **SQL Forensic Queries** | ≥ 25 | **42 queries across 9 categories** | `02_SQL/naukri_saaf_sql_workbench.sql` | ✅ Verified |

<br/>

## 2. Operational Service-Level Metrics (Production Plan)

| Metric | Purpose | Measurement Mechanism | SLA / Threshold |
|---|---|---|---|
| **API Availability & Uptime** | Service reliability for extension | `/health` endpoint probe | $\ge 99.9\%$ uptime |
| **Population Stability Index (PSI)** | Early detection of portal hiring and salary shifts | `src/monitoring/drift_detector.py` | $\text{PSI} < 0.25$ (Alert if $\ge 0.25$) |
| **Data Quality Gate** | Prevents malformed scrapes from corrupting pipeline | `src/monitoring/data_validation.py` | 0 SchemaErrors allowed |
| **Client-Side Privacy Guarantee** | Guarantees zero resume leakage | Local in-browser PDF.js tokenization | 0 external network transmissions |
| **Agent Forensic Audit Speed** | Provides multi-source evidence summary | `src/agent/verifier.py` (4 tools) | $< 5.0\text{s}$ per listing audit |

<br/>

## 3. Continuous Improvement Backlog

| Priority | Enhancement | Target Milestone | Purpose |
|:---:|---|:---:|---|
| **P1** | Complete Human Ground Truth Benchmark (`GOLD_LABELS_DONE.csv`) | Immediate | Rigorous evaluation against 80 human-verified listings |
| **P2** | Automated Daily Scraping Delta Pipeline | Next Phase | Real-time monitoring and automated drift tracking |
| **P3** | Direct ATS Verification (Greenhouse, Lever) | Next Phase | Cross-verification against public company careers portals |
