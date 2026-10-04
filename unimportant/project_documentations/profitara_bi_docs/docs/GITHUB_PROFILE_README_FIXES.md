# GitHub Profile & Project README Fixes

This document provides replacement text for claims currently on your GitHub Profile README, project descriptions, or resume that are statistically invalid, methodologically leaked, or inconsistent across files.

---

## 1. Summary of Changes

| Area | Current Misleading / Flawed Claim | Honest, Defensible Replacement | Why Changed |
|---|---|---|---|
| **Data Nature** | "10,000 retail transaction dataset" (implied real) | "10,000-row synthetic Indian quick-commerce transaction dataset (used for UI & storytelling) + real UCI Online Retail II dataset (used for ML benchmarking)" | Transparency. The Indian dataset has clear synthetic signatures (e.g., 680 random PIN codes for 680 Gurugram orders). Defending it as real in an interview will fail. |
| **CLV Model** | "Random Forest CLV · $R^2 = 0.930$" | "CLV prediction via time-split regression and BG/NBD probabilistic model (honest out-of-time evaluation)" | The $R^2 = 0.930$ came from target identity leakage: features included `AvgOrderValue` and `Frequency`, while the target was `Monetary = AvgOrderValue * Frequency`. |
| **Churn Model** | "Churn classifier · AUC = 0.91, 85% accuracy, 361 at-risk customers" | "Time-based churn prediction with expected-value win-back targeting" | Churn was defined arbitrarily as Recency > 75th percentile ($1448 \times 0.25 = 361$ customers), creating circular leakage with tenure/frequency on a random split. |
| **Customer Segmentation** | "K-Means · Silhouette 0.611 → 119 Champion customers" | "RFM-based customer segmentation (evaluated across $k=2..8$ for stability and operational granularity)" | $k=2$ achieved 0.611 silhouette only because it split 119 extreme high-spenders from 1,329 customers, which is operationally degenerate for CRM actions. |
| **Phantom Tools** | References to XGBoost, Prophet, or US Superstore ($2.3M USD) | Strictly tools actually in the codebase: DuckDB, Scikit-learn, Statsmodels (Holt-Winters), Mlxtend, Streamlit | Eliminates discrepancies between SQL/Excel/notebook drafts. |

---

## 2. Replacement Blocks for GitHub Profile README

### Option A: Clean Project Card (Markdown)

```markdown
### 🛒 Profitara — Retail BI & Customer Analytics Pipeline
**Stack**: Python (Pandas, Scikit-Learn, Statsmodels), SQL (DuckDB, PostgreSQL), Streamlit, Plotly, Power BI

- **Dual-Dataset Architecture**: Modeled quick-commerce operations on a 10,000-row synthetic Indian retail dataset (₹66.95L revenue, 4.15% margin) and validated machine learning models against the public UCI Online Retail transaction dataset.
- **Leakage-Free CLV Modeling**: Built time-split customer lifetime value models (observation vs. prediction windows), benchmarking BG/NBD + Gamma-Gamma against Random Forest and Gradient Boosting with bootstrap confidence intervals.
- **Decision-Driven Churn & Win-Back**: Implemented calibrated churn probability models integrated into an expected-value decision framework ($EV = P(\text{churn}) \times \text{CLV} \times \text{margin} - \text{cost}$) to rank win-back candidates under marketing budget constraints.
- **SQL Analytics Layer**: Engineered 10+ production-grade analytic queries in DuckDB (cohort retention matrices, repeat purchase rates, Pareto concentration, window functions) powering a 13-page interactive Streamlit dashboard.
```

### Option B: Concise 2-Line Summary (for pinned repositories)

```markdown
**Profitara: Retail BI & Customer Analytics Platform**
End-to-end retail intelligence pipeline featuring time-split CLV modeling, expected-value churn win-back optimization, DuckDB analytics layer, and an interactive 13-page Streamlit dashboard.
```

---

## 3. Specific Text Replacements for Badges & Headlines

- **REMOVE**: Badge `![R2](https://img.shields.io/badge/R%C2%B2-0.930-2F7D4F)`  
  **REPLACE WITH**: Transparent benchmark metrics table in repository README once Phase 2 models execute.
- **REMOVE**: Badge `![AUC](https://img.shields.io/badge/AUC-0.91-2F7D4F)`  
  **REPLACE WITH**: Out-of-time calibrated ROC-AUC / PR-AUC.
- **REMOVE**: Any mention of `XGBoost` or `Prophet` unless implemented.
- **REMOVE**: Any reference to $2.29M / US Superstore in project descriptions.
