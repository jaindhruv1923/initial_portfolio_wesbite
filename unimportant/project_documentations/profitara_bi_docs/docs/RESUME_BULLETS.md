# Resume Bullets: Profitara

Use these tailored resume bullets depending on whether you are applying for **Data Analyst** or **Machine Learning / Data Scientist** roles. Every number is traceable directly to an executed script in this repository.

---

## 📊 Data Analyst (DA-Flavored) Bullets

> **Data Disclosure Note**: Built on a 10,000-row synthetic Indian quick-commerce dataset for operational dashboarding and a 541,909-row real public UCI retail dataset for machine learning benchmarking.

- **End-to-End Retail Intelligence Platform**: Designed and deployed a 13-page interactive Streamlit dashboard and Power BI report analyzing ₹66.95L in revenue across 4,918 quick-commerce orders and 1,448 customers, modeling delivery SLA unit economics (Instant 10–15 min vs. Scheduled).  
  *Source: `01_Dataset/Profitara_India_Dataset.csv`, `05_Streamlit_Dashboard/app.py`*

- **Embedded Analytical SQL Layer**: Engineered 11 production-grade SQL queries in DuckDB utilizing Common Table Expressions (CTEs) and window functions (`LAG()`, `DENSE_RANK()`, rolling frames) to compute monthly cohort retention matrices (0–11 months), repeat purchase conversion rates, and 30-day trailing revenue averages.  
  *Source: `sql/analytic_queries.sql`, `tests/test_data_integrity.py`*

- **Revenue Concentration & Leakage Diagnostics**: Conducted Pareto 80/20 customer concentration analysis and identified 299 high-discount orders (≥30%) averaging a -19.2% net margin loss; built an interactive price-elasticity simulator to model profit-maximizing discount caps per sub-category.  
  *Source: `sql/analytic_queries.sql:Query 3 & Query 8`, `reports/figures/clv_decile_calibration.png`*

- **Cross-Sell Market Basket Analysis**: Applied the Apriori algorithm across 17,512 retail transaction baskets, isolating 248 statistically significant association rules with lift ratios up to 27.86× (73.7% confidence) to power evidence-based promotional product bundling.  
  *Source: `reports/apriori_surviving_rules.csv`, `ml_pipeline/segmentation_basket.py`*

---

## 🤖 Machine Learning / Data Science (ML-Flavored) Bullets

> **Data Disclosure Note**: Predictive models, time-series forecasting, and decision optimization were trained and evaluated strictly on the real public UCI Online Retail dataset (541,909 rows, 4,372 customers).

- **Leakage-Free Time-Split CLV Modeling**: Implemented an out-of-time customer lifetime value pipeline (9-month observation vs. 90-day prediction window), benchmarking Linear Regression, BG/NBD + Gamma-Gamma (MAE £755.28), Random Forest, and Gradient Boosting ($R^2 = 0.093$) with 95% bootstrap confidence intervals and 10-decile calibration.  
  *Source: `reports/clv_model_benchmarks.csv`, `reports/clv_decile_calibration.csv`, `ml_pipeline/clv_engine.py`*

- **Decision-Theoretic Churn & Win-Back Policy**: Developed an out-of-time churn prediction model (ROC-AUC = 0.764, Brier score = 0.1928) integrated into an Expected Value optimization framework ($EV = P(\text{churn}) \times \text{CLV} \times \text{margin} - \text{cost}$); demonstrated a simulated net return of +£720.03 under a £1,500 budget, outperforming naive recency outreach (+£31.60) and random marketing (-£19.19).  
  *Source: `reports/churn_policy_backtest.csv`, `config/business_assumptions.yaml`, `ml_pipeline/churn_decision_engine.py`*

- **Customer Behavioral Segmentation**: Evaluated K-Means clustering across $k \in [2, 7]$ on standardized log-transformed RFM features; selected $k=4$ based on silhouette score (0.330) and multi-seed stability (0.947 across 5 seeds), profiling Champions (64.2% revenue share), Loyalists, At-Risk, and Hibernating accounts.  
  *Source: `reports/kmeans_k_evaluation.csv`, `reports/customer_segment_profiles.csv`, `ml_pipeline/segmentation_basket.py`*

- **Rolling-Origin Time-Series Forecasting**: Evaluated 4-week revenue forecasts across a 3-fold walk-forward backtest; established that a 4-week moving average naive baseline achieved the lowest overall error (17.71% mean MAPE), while Holt-Winters exponential smoothing decisively won during holiday peak season (4.10% MAPE, £12,259 RMSE).  
  *Source: `reports/forecast_model_summary.csv`, `reports/forecast_rolling_eval.csv`, `ml_pipeline/forecasting_engine.py`*

- **Safe Text-to-SQL Retail Analyst Agent**: Built an automated analytics agent over DuckDB with schema-aware prompting, query structure validation (SELECT/WITH only), toxic keyword rejection, row-limit clamping, and automated chart recommendation; validated with an automated test suite and continuous integration via GitHub Actions.  
  *Source: `agent/analyst_agent.py`, `tests/test_agent_guard.py`, `.github/workflows/ci.yml`*
