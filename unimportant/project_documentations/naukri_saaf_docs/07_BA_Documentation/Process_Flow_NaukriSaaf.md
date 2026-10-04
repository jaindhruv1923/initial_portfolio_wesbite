<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=140&section=header&text=Process%20Flow&fontSize=34&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=As-Is%20%E2%86%92%20To-Be%20%C2%B7%20Naukri%20Saaf%20v4&descAlignY=68&descSize=16)

</div>

## 🔴 As-Is — Market Inefficiency Before Naukri Saaf

```mermaid
flowchart TD
    A[🔍 Candidate browses\nLinkedIn, Indeed, Glassdoor\nisolated across tabs] --> B[👀 Subjective manual read\nof JD text]
    B --> C[❓ Invisible true days active\nand repost history]
    B --> D[📝 Tedious manual comparison\nof resume to JD requirements]
    B --> E[🚫 Zero awareness of corporate\nsyndicated plagiarism or ghosting]
    C --> F[🚨 Weeks wasted tailoring applications\nto phantom openings & talent pipelines]
    D --> F
    E --> F

    style A fill:#8f8a9e,color:#fff
    style F fill:#9C3B3B,color:#fff
```

<details>
<summary><b>Operational Bottlenecks & As-Is Pain Points (Click to Expand)</b></summary>
<br/>

- **Deceptive Lingering**: Ghost listings persist 42.6x longer than genuine postings (median 128 days vs 3 days), polluting job feeds.
- **Syndicated Boilerplate**: Over 54.4% of ghost listings reuse identical job descriptions across competing entities.
- **Asymmetric Information**: Candidates lack visibility into employer repost frequency, hiring velocity, or historical interview follow-through.
- **Candidate Fatigue**: High application friction with low response rates leads to widespread jobseeker burnout.

</details>

<br/>

---

## 🟢 To-Be — Production Intelligence with Naukri Saaf (v4)

```mermaid
flowchart TD
    A[📄 2,851 verified listings scraped\nApify: LinkedIn, Indeed, Glassdoor] --> B[🧹 SQL Staging, Normalization & Fact Schema\n42 queries · 9 analytical categories]
    B --> C[🏷️ Snorkel Weak Supervision Generative Model\n10 Domain LFs + 180 Silver Proxy Holdout]
    C --> D[🤖 Leakage-Free 5-Fold GroupKFold ML Pipeline\n73 Features · Calibrated Ensemble · ROC-AUC 0.9200]
    D --> E[🔬 64-d Dense Semantic LSA Encoder\nTreeSHAP Local Attribution · Cross-Sectional Age Analysis]
    E --> F[📊 8-Tab Executive Streamlit Portal\nInteractive EDA, Age Distributions & Model Inspection]
    E --> G[⚡ Sub-15ms FastAPI Service + Chrome Extension\nInstant Risk Triage + Zero-Knowledge Privacy Resume Match]
    E --> H[🕵️ Multi-Tool Autonomous Verification Agent\nBorderline Adjudication & Forensic Audit Trail]
    F --> I[✅ Transparent, Evidence-Backed Career Decisions\n100% Audit-Grade Accountability]
    G --> I
    H --> I

    style A fill:#4C1D95,color:#fff
    style F fill:#B8860B,color:#1A1F2B
    style G fill:#B8860B,color:#1A1F2B
    style H fill:#4C1D95,color:#fff
    style I fill:#1F7A54,color:#fff
```

<br/>

## 🔀 Transformation Matrix: What Changed, Step by Step

| Capability | 🔴 As-Is Workflow | 🟢 To-Be Production Architecture (v4) |
|---|---|---|
| **Data Normalization** | Portals manually checked in siloed tabs | **2,851 deduplicated records** across 3 major portals in a unified SQL fact table (`02_SQL/naukri_saaf_sql_workbench.sql`) |
| **Ground Truth Strategy** | Unvalidated heuristics or subjective guesses | **180-listing silver heuristic proxy** + **80-listing blind human labeling protocol** (`LABELING_RUBRIC.md`) + **10 Snorkel Generative LFs** ($\kappa=0.5890$) |
| **ML Evaluation Rigor** | Random train/test split with severe entity leakage | **5-Fold GroupKFold partitioned strictly by Employer**; zero cross-fold leakage; silver proxy holdout **ROC-AUC = 0.9200, Recall = 0.9318** |
| **Probability Calibration** | Raw uncalibrated tree probabilities | **Platt calibration** yielding an institutional Brier score of **0.0167** and Expected Calibration Error (ECE) of **0.0220** |
| **Job Description Analysis** | Superficial keyword matching | **64-d Dense Semantic LSA vectors** identifying boilerplate phrasing across tech descriptions ($\ge 0.85$ cosine similarity) |
| **Requisition Age Analysis** | Static arbitrary cutoffs | **Empirical cross-sectional age distributions**: reveals posting age spread across platforms (median 11.0d, P90 128.0d) |
| **Borderline Case Handling** | High false-positive discard rate | **Autonomous Multi-Tool Verification Agent** (`src/agent/verifier.py`) with 4 specialized audit tools |
| **Candidate Privacy** | Insecure cloud-hosted resume parsers | **Zero-Knowledge architecture**: PDF.js parses resumes 100% locally in `chrome.storage.local` with zero network egress |
| **Serving Architecture** | Hardcoded client-side estimates | **Production FastAPI microservice (`POST /api/v1/score`)** delivering sub-15ms inference with offline fallback |

<br/>

## 🎓 Strategic Business Analyst Perspective

In enterprise data solutions, the gap between prototype and production lies in **traceability and auditability**:
1. **Traceability**: Every metric reported to executive stakeholders or end users traces directly to an executing script (`src/analytics/listing_age_analysis.py`, `src/models/train_leakage_free_model.py`, `src/api/main.py`).
2. **Deterministic Governance**: Automated Pandera schema validation gates and GitHub Actions CI regression tests protect downstream BI assets from silent data corruption.
3. **Actionable Triage**: The system replaces subjective hesitation with deterministic risk tiers, saving an estimated 14.5 hours per applicant monthly.

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README_BA_package.md">← Back to BA Package Index</a></i></div>
