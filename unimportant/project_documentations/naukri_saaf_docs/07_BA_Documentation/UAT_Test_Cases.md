<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=UAT%20Test%20Cases&fontSize=32&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf%20v4%20Production&descAlignY=78&descSize=15)

</div>

User Acceptance Test cases mapped 1:1 to the Requirements Traceability Matrix and production engineering gates in v4.

<br/>

| Test ID | Traces to | Scenario | Test Execution Steps | Expected Result | Pass Criteria |
|---|---|---|---|---|---|
| `UAT-01` | BR-01 | Unified SQL Fact & Dimension Staging | Run staging & normalization queries in `02_SQL/naukri_saaf_sql_workbench.sql` against raw Apify scrapes | Staging table ingests 3,000 raw rows; deduplicates to **2,851 clean listings** across all 3 portals with standardized types | Zero NULLs in primary keys; exact row count matches 2,851 |
| `UAT-02` | BR-02 | Snorkel Generative Weak Supervision | Execute `src/models/weak_supervision.py` across 10 Labeling Functions | Snorkel Generative Model computes empirical LF accuracies without ground truth; generates probabilistic training targets | $\kappa \ge 0.55$ agreement with holdout labels (achieved $\kappa=0.5890$) |
| `UAT-03` | BR-03 | Silver Proxy Benchmark & Calibration | Evaluate calibrated models against the 180-listing silver proxy holdout (`data/silver_labeling_sheet.csv`) | Calibrated Random Forest and GBM achieve high discrimination and low calibration error on proxy holdout | **ROC-AUC $\ge 0.9000$ (achieved 0.9200 on silver proxy)**; Recall $\ge 0.90$ (achieved 0.9318); Brier score $\le 0.025$ (achieved 0.0167) |
| `UAT-04` | BR-04 | Additive TreeSHAP Local Explainability | Query `/api/v1/score` or Streamlit SHAP Inspector for a high-risk listing | Exact additive SHAP values computed; top-3 positive and negative risk contributors displayed with clear explanations | $\sum \phi_i + \phi_0 = f(x)$; explainability vectors render without missing weights |
| `UAT-05` | BR-05 | Cross-Company JD Plagiarism Detection | Run `src/features/dense_semantic_encoder.py` on candidate job description | 64-d Dense Semantic LSA vectors calculate cosine similarity across 2,851 postings | High similarity pairings flagged with cluster identifier and matched company list |
| `UAT-06` | BR-06 | Empirical Listing-Age Distribution Analysis | Run `src/analytics/listing_age_analysis.py` across platforms | Script computes parametric and empirical quantiles on listing age at scrape | Overall median age matches 11.0 days; P90 matches 128.0 days; Glassdoor median 61.0 days, LinkedIn 11.0 days, Indeed 0.0 days |
| `UAT-07` | BR-07 | Autonomous Multi-Tool Verification Agent | Submit a borderline listing ($P=0.55$) to `src/agent/verifier.py` | Agent activates 4 tools (ML Scorer, Semantic Plagiarism, Employer History, Salary Validator); outputs structured JSON log | Multi-tool forensic reasoning trail with structured tool invocations and findings |
| `UAT-08` | BR-08 | Production Streamlit Dashboard Integrity | Launch `streamlit run 05_Streamlit_Dashboard/app.py`, interact across all 8 tabs | All tabs render cleanly (KPIs, Platforms, Ghost Analytics, Employer Matrix, Calibration, Clusters, Listing Age, SHAP Inspector) | Zero unhandled exceptions or broken Plotly charts across entire session |
| `UAT-09` | BR-09 | Zero-Knowledge Resume Privacy in Extension | Upload sample PDF resume in Chrome Extension; monitor Chrome DevTools Network Tab | PDF parsed client-side via PDF.js; stored strictly in `chrome.storage.local`; fit score computed in browser | **0 network egress requests** containing resume text; zero cloud transmission |
| `UAT-10` | BR-10 | Dual-Mode Chrome Extension Live / Fallback Scoring | Test Chrome Extension with local FastAPI running vs server stopped | With server running: scores via `POST /api/v1/score` in <15ms. With server stopped: falls back gracefully to `legitimacy.js` | UI updates smoothly; no runtime script errors or frozen UI panels |
| `UAT-11` | BR-11 | Data Quality & Schema Integrity Gate | Run `python src/monitoring/data_validation.py` | Pandera validates 73 feature schemas, value ranges, and missingness thresholds | 100% schema validation pass; non-zero exit code if schema corrupted |
| `UAT-12` | BR-12 | GroupKFold Leakage Prevention CI Gate | Run `pytest -v tests/test_ml_pipeline.py` | Automated test verifies 0 employer overlap between GroupKFold train and validation splits | Zero cross-fold leakage; 11/11 tests pass cleanly |

<br/>

## Production Release Sign-Off Gate

A production deployment is formally approved when:
- [x] All 12 UAT test cases pass with 100% compliance.
- [x] CI pipeline (`pytest -v tests/`) passes all 11 test modules with zero warnings or errors.
- [x] Pandera schema validation confirms 2,851 dataset integrity and type invariants.
- [x] Zero network calls transmit candidate PII or resume contents outside the sandboxed browser runtime.
- [x] All reported metrics in documentation match live execution logs within $\pm 0.0001$.

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README_BA_package.md">← Back to BA Package Index</a></i></div>
