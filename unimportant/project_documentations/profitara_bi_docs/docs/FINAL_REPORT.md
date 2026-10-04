# Profitara Final Engineering Report

**Audit & Upgrade Date**: October 2026  
**Auditor & Lead Analytics Engineer**: Antigravity (Google DeepMind)  
**Branch**: `upgrade` | **Initial Commit**: `2c244f1` | **Final State**: Tested & Verified

---

## 1. Before vs. After Metric Comparison Table

| Metric / Claim | Initial State (Audit) | Upgraded State (Verified) | Status | Rationale / Engineering Correction |
|---|---|---|:---:|---|
| **Data Nature** | 10,000 retail rows (implied real) | Dual-dataset: 10k synthetic Indian quick-commerce + 541k real UCI Online Retail | **VERIFIED** | Transparency. Removed false claims of real Indian quick-commerce data; benchmarked all ML models on genuine human transactions. |
| **CLV Model $R^2$** | $R^2 = 0.930$ (Random Forest) | $R^2 = 0.093$ (Gradient Boosting), $R^2 = 0.091$ (Random Forest) | **CORRECTED** | Fatal target identity leakage eliminated ($\text{Monetary} = \text{Frequency} \times \text{AvgOrderValue}$). Replaced random split with strict 9-month observation vs. 90-day future spend holdout. |
| **CLV Benchmark MAE** | ₹1,171.95 (in-sample leaked) | **£755.28** (BG/NBD + Gamma-Gamma), **£811.88** (Gradient Boosting) | **VERIFIED** | Probabilistic BG/NBD model established as superior low-error baseline on out-of-time evaluation. |
| **Churn Classification** | $\text{AUC} = 0.91$, Accuracy 85% | **$\text{ROC-AUC} = 0.764$** (95% CI: [0.736, 0.793]), Brier = 0.1928 | **CORRECTED** | Circular recency quantile cutoff removed. Replaced with true non-contractual definition: 0 orders in subsequent 90 days. |
| **At-Risk Customer Definition**| 361 "at-risk customers" (misrepresented as an ML cluster) | 274 prioritized win-back targets based on Expected Value optimization | **CORRECTED** | 361 was merely $1,448 \times 0.25$ (the recency 75th percentile). Replaced with decision-theoretic targeting combining risk, CLV, margin, and cost. |
| **Win-Back Impact Claim** | ₹823K "recoverable revenue" (unverified arbitrary assumption) | **+£720.03** simulated net return under £1,500 budget (declared assumptions) | **VERIFIED** | Stated assumptions clearly in `config/business_assumptions.yaml`; backtested against naive recency (+£31.60) and random marketing (-£19.19). |
| **K-Means Clustering** | $k=2$ (Silhouette 0.611, 119 Champions) | **$k=4$** (Silhouette 0.330, Seed Stability 0.947 across 5 seeds) | **CORRECTED** | $k=2$ was degenerate (merely separated 119 outliers from 1,329 customers). $k=4$ provides actionable tiers: Champions (64.2% rev), Loyalists (24.5%), At-Risk (4.9%), Hibernating (6.5%). |
| **Market Basket Rules** | 52 rules on synthetic categories | **248 rules** on 17,512 real retail baskets (Top Lift: **27.86×**) | **VERIFIED** | Real-world co-purchases discovered (Scandinavian Christmas wooden items, Regency teacups). |
| **Forecasting Method** | Holt-Winters without backtesting | 3-Fold Rolling-Origin Walk-Forward Backtest (4-week horizon) | **VERIFIED** | Established that Seasonal Naive wins overall (MAPE 17.71%), while Holt-Winters decisively wins holiday peak demand (MAPE 4.10%, RMSE £12,259). |
| **SQL Data Integrity** | Hardcoded US Superstore data (9,994 rows, USD, Sean Miller) | Real DuckDB database (`profitara.duckdb`) reconciling 10,000 Indian rows and 397k real rows | **CORRECTED** | Completely eliminated foreign US Superstore queries; added 11 production queries (cohorts, Pareto, MoM growth via `LAG()`). |
| **Streamlit Dashboard** | Missing `app.py` (`READ_THIS_MISSING_FILE.txt`) | Fully reconstructed 13-page application in `05_Streamlit_Dashboard/app.py` | **RESTORED** | Restored all 13 pages, integrated live DuckDB SQL lab, and styled in Atkinson Hyperlegible palette. |
| **Power BI Integration** | Copied PhonePe README with `#5F259F` colors | Clean CSV exports in `Power_BI_Work/clean_csv_export/` + `POWERBI_REFRESH_STEPS.md` | **CORRECTED** | Reconciled data sources and wrote manual refresh instructions without touching `.pbix` binary. |
| **Automated Test Suite** | 0 tests | **10 automated tests** passing in `pytest` (Leakage, Data Integrity, SQL Guardrails) | **DELIVERED** | Enforced continuous integration via GitHub Actions (`.github/workflows/ci.yml`). |
| **Retail Analyst Agent** | None | Schema-aware DuckDB text-to-SQL agent with security validation | **GATED** | Enforced gate: 40 QA pairs generated in `QA_PAIRS_TO_REVIEW.csv`; evaluation runner halts until human review. |

---

## 2. Why "Worse" Numbers are Better Engineering

In data science interviews, claiming an $R^2$ of 0.930 on retail transaction spend or an AUC of 0.91 on static customer churn instantly alerts experienced interviewers to target leakage. When questioned, a candidate defending 0.930 cannot explain why their model fails in production.

By contrast, reporting an out-of-time $R^2$ of 0.093 and an AUC of 0.764 demonstrates:
1. **Methodological Rigor**: You understand that future non-contractual purchasing is stochastic.
2. **Leakage Awareness**: You know how to prevent algebraic identity traps ($\text{Spend} = \text{Freq} \times \text{AOV}$).
3. **Business Decision Framing**: You understand that models serve decisions (ranking accounts by expected net value under budget constraints), not Kaggle metric chasing.

---

## 3. What Remains (Gated Action)

As specified in Hard Rule 1 and the Phase 7 instructions:
- **`QA_PAIRS_TO_REVIEW.csv`** contains 40 machine-generated question-SQL pairs.
- To maintain 100% data honesty, execution accuracy cannot be reported until the candidate/user reviews and marks these pairs as `correct` or `incorrect`.
- Once reviewed, running `python agent/evaluate_agent.py` will execute the evaluation and output the final verified agent accuracy.
