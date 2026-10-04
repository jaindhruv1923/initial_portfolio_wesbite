<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Functional%20Specification&fontSize=28&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf&descAlignY=78&descSize=15)

</div>

Detailed inputs → processing → outputs → business rules for each functional component, the level of detail a BA hands to engineering for build.

<br/>

## FR-01 — SQL Staging & Cleaning Layer

| | |
|---|---|
| **Trigger** | New raw CSV export from the scraper (`naukri_saaf_combined_raw.csv`) |
| **Input** | Raw text fields — mixed date formats, salary as free text, applicant counts as phrases (e.g. "Over 200 applicants") |
| **Process** | Load as-is into `naukri_jobs_raw` (all VARCHAR/TEXT, mirrors source exactly) → transform into a typed, analysis-ready table in Section 2 of the SQL workbook |
| **Output** | A clean, typed table ready for the 32 analytical queries across 8 categories (profiling, joins, CTEs, window functions, stored procedures, triggers) |
| **Business rule** | Raw data is never cleaned in-place — the raw staging table is preserved so any cleaning logic bug can be re-run from source, not from already-transformed data |

<br/>

## FR-02 — Weak-Supervision Ghost Labeling

| | |
|---|---|
| **Trigger** | Cleaned dataset ready for labeling |
| **Input** | Behavioral fields: days_live, posting_velocity_per_week, employer_repost_count, salary_disclosed_num, description quality metrics |
| **Process** | Combine behavioral signals into a rule-based ghost-probability proxy label, since no ground truth exists |
| **Output** | A `ghost_label` field usable as a training target |
| **Business rule** | The label is documented as an engineered proxy, not verified truth — every downstream metric (AUC, F1) is reported with this caveat |

<br/>

## FR-03 — Model Training & Benchmarking

| | |
|---|---|
| **Trigger** | Labeled dataset ready |
| **Input** | 26 engineered features per listing (`feature_importance_v3.csv` schema) |
| **Process** | Train and benchmark 5 classifiers (Gradient Boosting, Stacking Ensemble, Random Forest, Logistic Regression, MLP); evaluate via temporal cross-validation (not random split, to avoid leakage across time) |
| **Output** | Trained model artifacts (`gbm_model_v3.pkl`, `rf_model_v3.pkl`, `mlp_model_v3.pkl`, `stacking_model_v3.pkl`, `scaler_v3.pkl`); `model_comparison_v3.csv` |
| **Business rule** | Best model selected by AUC on held-out temporal folds, not training-set performance — GBM selected at AUC 0.716 |

<br/>

## FR-04 — Explainability & Employer Clustering

| | |
|---|---|
| **Trigger** | Final model selected |
| **Input** | Trained GBM model + full feature set |
| **Process** | Compute SHAP values per listing per feature (`shap_values_v3.csv`); run behavioral clustering on employer-level aggregates |
| **Output** | Per-listing feature attribution; 6 employer clusters (`cluster_profiles_v3.csv`) with ghost rate, avg. days live, avg. repost count per cluster |
| **Business rule** | Every "ghost" flag must be traceable to specific contributing features — no unexplained flags are surfaced to the dashboard or extension |

<br/>

## FR-05 — Streamlit Dashboard

| | |
|---|---|
| **Trigger** | User launches `app.py` |
| **Input** | `predictions_v3.csv`, model comparison, feature importance, cluster profiles, bootstrap CI, temporal CV results |
| **Process** | Render 7 tabs: Overview, Platforms, Ghost Detection, Employers, Model Performance, Cluster, Explore |
| **Output** | Interactive dashboard, dark theme (`#8B5CF6` accent), Plotly visualizations |
| **Business rule** | Every chart must be traceable to a specific CSV/model artifact — no numbers are hardcoded in the UI layer |

<br/>

## FR-06 — Chrome Extension: Job Reading (content.js)

| | |
|---|---|
| **Trigger** | User clicks ↻ on a supported job-portal page |
| **Input** | Live DOM of the current tab |
| **Process** | Portal-specific selector matching (LinkedIn/Naukri/Indeed/Glassdoor) → generic largest-text-block fallback if selectors fail |
| **Output** | `{ portal, title, company, meta, description, url }` object |
| **Business rule** | If site-specific selectors return nothing, fallback must still attempt extraction — never fail silently |

<br/>

## FR-07 — Chrome Extension: Legitimacy Scoring (legitimacy.js)

| | |
|---|---|
| **Trigger** | Job data successfully read |
| **Input** | Job data object + `MODEL_WEIGHTS` (sourced from `feature_importance_v3.csv`) |
| **Process** | Evaluate ~16 of 26 signals directly from page text (regex/heuristic rules); flag remaining ~10 as manual-check |
| **Output** | Per-signal status (good/bad/neutral/manual), a risk score (0–100), a coverage percentage, and a verdict label |
| **Business rule** | Risk score computed **only** from signals with status good/bad/neutral — manual-check signals are excluded from the score, not defaulted to any value |

<br/>

## FR-08 — Chrome Extension: Resume Match (nlp.js + sidepanel.js)

| | |
|---|---|
| **Trigger** | Resume saved AND job data available |
| **Input** | Resume text, job title + description |
| **Process** | Tokenize both texts (stopword-filtered) → TF-based cosine similarity + skill-dictionary overlap → blended score: `0.6 × skill_ratio + 0.4 × min(1, cosine_sim × 2.5)` |
| **Output** | 0–10 fit score, matched/missing skill lists, 3 tailored next-step suggestions |
| **Business rule** | Advice text must reference the *specific* matched/missing skills for this listing — never generic boilerplate |

<br/>

## FR-09 — Chrome Extension: Verification Links

| | |
|---|---|
| **Trigger** | Legitimacy tab rendered |
| **Input** | Company name, job title |
| **Process** | Build pre-formatted Google search URLs for Glassdoor reviews, AmbitionBox reviews, LinkedIn company page, duplicate-posting check, funding/news check, scam-complaint check |
| **Output** | 6 one-click search links |
| **Business rule** | Links open in a new tab; the extension itself makes no request to any of these — the user performs the actual lookup |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
