# Profitara Technical Walkthrough & Defense Manual

This walkthrough explains every module in the repository: what it does, why it was implemented this way, mathematical formulas, and what edge cases or failure modes to be aware of.

---

## Module 1: Dual-Dataset Architecture

### What It Does
- Separates user-facing business intelligence from predictive machine learning.
- **Storytelling Layer**: `01_Dataset/Profitara_India_Dataset.csv` (10,000 synthetic rows, ₹66.95L revenue, 4,918 orders, 1,448 customers). Powers regional quick-commerce metrics (Instant 10–15 min vs Express delivery).
- **Machine Learning Core**: `data/real/online_retail_II.csv` (541,909 real transactions from UCI Machine Learning Repository). Powers time-split predictive modeling.

### Why This Design
- The Indian dataset is a compelling storytelling vehicle for Indian quick-commerce firms (Blinkit, Zepto, Swiggy Instamart), but its synthetic generation causes severe artifacts in ML models (over-inflated $R^2$).
- Training on the real UCI dataset ensures models reflect genuine human purchase distributions, stochastic inter-purchase times, and real return behavior.

### What Could Go Wrong
- *Confusion between datasets*: Interviewers might ask why some numbers are in ₹ and others in £.
- *Defense*: Explain the intentional dual-dataset architecture: INR for quick-commerce operational storytelling, GBP for real-world academic ML benchmarking.

---

## Module 2: Time-Split Customer Lifetime Value (`ml_pipeline/clv_engine.py`)

### What It Does
- Predicts future 90-day spend of customers active during the prior 9-month observation period.
- Benchmarks: Predict Mean, Linear Regression (OLS), BG/NBD + Gamma-Gamma (`lifetimes`), Random Forest Regressor, Gradient Boosting Regressor.
- Computes 95% bootstrap confidence intervals, 10-decile calibration, and permutation feature importance.

### Key Equations
- **Time Cutoff**: $T_{\text{split}} = \text{2011-09-01}$. Features computed strictly on $t < T_{\text{split}}$. Target $y = \sum \text{Spend}$ on $t \ge T_{\text{split}}$.
- **Decile Calibration**: Sort test customers by $\hat{y}$ into deciles $D_1 \dots D_{10}$, compute $\bar{y}_{\text{actual}}$ vs $\bar{y}_{\text{predicted}}$.
- **Bootstrap CI**: Sample with replacement $B=1,000$ times, calculate metric on each sample, take 2.5th and 97.5th percentiles.

### What Could Go Wrong
- *Zero-Inflation*: 41.2% of customers spend £0 in the future window, pulling $R^2$ down to 0.08–0.09.
- *Defense*: Explain that an $R^2$ of ~0.09 is mathematically normal in non-contractual retail. The earlier $R^2 = 0.930$ was an artifact of identity leakage ($\text{Monetary} = \text{Frequency} \times \text{AvgOrderValue}$).

---

## Module 3: Churn as a Decision & Win-Back Optimization (`ml_pipeline/churn_decision_engine.py`)

### What It Does
- Formulates churn as an out-of-time classification problem: *Did an active customer place 0 orders in the subsequent 90 days?* (Base rate: 41.2%).
- Fits a calibrated Logistic Regression model (ROC-AUC = 0.764, Brier score = 0.1928).
- Implements an Expected Value (EV) decision framework to rank win-back outreach under a £1,500 budget.
- Backtests against naive rules (contact everyone, contact top recency, contact top historic spenders).
- Performs sensitivity analysis across contact costs and response rates.

### Key Equations
- **Expected Net Value**:
  $$\text{EV}_i = \left(P(\text{Churn}_i) \times \text{Response Rate} \times \widehat{\text{CLV}}_i \times \text{Gross Margin}\right) - \text{Campaign Cost}$$
- **Assumptions**: Campaign Cost = £5.00, Gross Margin = 20%, Response Rate = 15%, Budget = £1,500.

### What Could Go Wrong
- *Presenting assumptions as measured reality*: Claiming "I generated £720 in profit".
- *Defense*: Always emphasize that these are *simulated decision policies under declared operational assumptions* (`config/business_assumptions.yaml`), not field-measured results.

---

## Module 4: Customer Segmentation & Market Basket Analysis (`ml_pipeline/segmentation_basket.py`)

### What It Does
- Evaluates K-Means clustering across $k \in [2, 7]$ using inertia, silhouette score, and stability across 5 random seeds (42, 100, 2024, 7, 999).
- Rejects $k=2$ (which only splits 119 outliers from 1,329 customers) and justifies $k=4$ for operational business segmentation (stability = 0.947).
- Mines 248 association rules using Apriori on 17,512 real retail baskets at min_support = 0.015 and min_lift = 1.2.

### What Could Go Wrong
- *Extreme Outliers distorting clusters*: Unusually large wholesale buyers skewing centroids.
- *Defense*: Log-transform features ($\log(1 + x)$) prior to standard scaling to normalize heavy tails.

---

## Module 5: Rolling-Origin Time-Series Forecasting (`ml_pipeline/forecasting_engine.py`)

### What It Does
- Aggregates real retail transactions into 53 weekly observations (£160,430 mean weekly revenue).
- Evaluates forecasting models across a 3-fold rolling-origin backtest (4-week forecast horizon):
  1. Seasonal Naive 4-Week Moving Average
  2. Holt-Winters Double Exponential Smoothing
  3. Autoregressive Random Forest with lag and rolling features
- Reports honest fold-by-fold metrics (RMSE, MAE, MAPE).

### Key Finding
- **Naive wins overall** (Mean MAPE = 17.71%) during transitional weeks.
- **Holt-Winters decisively wins Fold 3** (Holiday peak season, MAPE = **4.10%**).
- Random Forest overfits (Mean MAPE = 29.49%).

---

## Module 6: SQL & DuckDB Analytics Layer (`sql/analytic_queries.sql`, `sql/init_duckdb.py`)

### What It Does
- Loads clean tables into an embedded DuckDB database (`data/profitara.duckdb`).
- Contains 11 production analytical queries featuring:
  - Cohort retention matrices
  - Repeat purchase conversion rates
  - Pareto 80/20 customer concentration with running totals
  - Month-over-month growth via `LAG()`
  - Moving 30-day trailing revenue
  - Delivery SLA performance
  - Regional state rankings via `DENSE_RANK()`

---

## Module 7: Retail Analyst Agent (`agent/analyst_agent.py`, `agent/evaluate_agent.py`)

### What It Does
- Provides natural-language-to-SQL question answering over DuckDB.
- Enforces strict security:
  - Query must begin with `SELECT` or `WITH`.
  - Rejects destructive keywords (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `EXEC`, `PRAGMA`).
  - Clamps row limits to $\le 100$.
- Recommends chart types based on query result schema.
- **Gate Enforcement**: Generates 40 QA pairs into `QA_PAIRS_TO_REVIEW.csv` marked *machine-generated, unreviewed*. The evaluation runner strictly halts until human review is completed.

---

## Module 8: Quality Assurance (`tests/`, `run_all.py`, `.github/workflows/ci.yml`)

### What It Does
- 10 automated `pytest` tests verifying:
  - Temporal cutoff integrity (zero future timestamps in training feature window)
  - Feature-target isolation
  - Financial total reconciliation between pandas and DuckDB
  - SQL security validation and limit clamping
- Single-command reproduction script: `python run_all.py`.
- Automated GitHub Actions continuous integration workflow.
