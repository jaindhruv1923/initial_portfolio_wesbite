<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Requirements%20Traceability%20Matrix&fontSize=24&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf%20v4%20Production&descAlignY=78&descSize=15)

</div>

Traces every BRD requirement through to its design artifact, production build component, and automated verification method.

<br/>

| Req ID | Business Requirement | Design Specification | Production Build Component | Verification / CI Gate |
|---|---|---|---|---|
| `BR-01` | Unified multi-portal staging & deduplication | Functional Spec FR-01 | `02_SQL/naukri_saaf_sql_workbench.sql` (42 queries) | `UAT-01` (SQL schema validation) |
| `BR-02` | Silver proxy annotation & Snorkel weak supervision | Functional Spec FR-02 | `src/models/weak_supervision.py`, `data/ANNOTATION_GUIDE.md` | `UAT-02` ($\kappa \ge 0.55$) |
| `BR-03` | Leakage-free GroupKFold ML & Platt calibration | Functional Spec FR-03 | `src/models/train_leakage_free_model.py` | `UAT-03` (Silver Proxy ROC-AUC $\ge 0.9000$) |
| `BR-04` | Additive local feature attribution (TreeSHAP) | Functional Spec FR-04 | `src/models/tree_shap.py` | `UAT-04` ($\sum \phi_i + \phi_0 = f(x)$) |
| `BR-05` | Cross-company semantic plagiarism detection | Functional Spec FR-04 | `src/features/dense_semantic_encoder.py` (64-d LSA) | `UAT-05` (Cosine similarity cluster test) |
| `BR-06` | Requisition age distributions & lingering metrics | Functional Spec FR-06 | `src/analytics/listing_age_analysis.py` | `UAT-06` (Cross-sectional percentiles: median 11d, P90 128d) |
| `BR-07` | Autonomous multi-tool verification agent | Functional Spec FR-07 | `src/agent/verifier.py` | `UAT-07` (Multi-tool audit trail) |
| `BR-08` | Executive Streamlit analytics portal (8 tabs) | Functional Spec FR-05 | `05_Streamlit_Dashboard/app.py` | `UAT-08` (Zero UI exceptions) |
| `BR-09` | Zero-knowledge privacy resume matching | Functional Spec FR-08 | `06_Chrome_Extension/` (`pdf.js` + `chrome.storage.local`) | `UAT-09` (0 network egress requests) |
| `BR-10` | Low-latency scoring microservice & extension bridge | Functional Spec FR-08 | `src/api/main.py` (FastAPI `POST /api/v1/score`) | `UAT-10` (<15ms latency test) |
| `BR-11` | Automated data quality & Pandera schema gates | Functional Spec FR-01 | `src/monitoring/data_validation.py` | `UAT-11` (100% Pandera schema pass) |
| `BR-12` | Automated CI entity leakage & regression testing | Functional Spec FR-03 | `tests/`, `.github/workflows/ci.yml` | `UAT-12` (11/11 pytest modules pass) |

<br/>

## Coverage & Audit Sign-Off

| Audit Dimension | Status | Verification Detail |
|---|:---:|---|
| **Specification Completeness** | 100% | Every BRD requirement maps to a functional specification in `Functional_Specification.md`. |
| **Code Implementation** | 100% | Every requirement is implemented by executable Python/SQL code in `src/` and `02_SQL/`. |
| **Verification Coverage** | 100% | 12/12 requirements are verified by automated UAT test cases and CI test suites. |
| **Orphan Feature Audit** | 0 Orphans | Zero undocumented or disconnected scripts exist in the production tree. |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README_BA_package.md">← Back to BA Package Index</a></i></div>
