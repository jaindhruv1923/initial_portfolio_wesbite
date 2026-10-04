# Recruiter One-Pager: Profitara

**Candidate**: Dhruv Jain | B.Tech CSE (AI & Data Science), BML Munjal University  
**Target Roles**: Data Analyst (Immediate) → Data Scientist / ML Engineer (1–2 Years)  
**Core Stack**: SQL (DuckDB, PostgreSQL), Python (Pandas, Scikit-Learn, SciPy), Power BI, Streamlit, Git

---

## 1. The Business Problem

Retail businesses and quick-commerce platforms struggle to translate high-volume raw transaction logs into profitable daily operations:
- **Quiet Margin Erosion**: Over-discounting reduces net margin below viability without operational visibility.
- **Reactive Churn Management**: Customers are only addressed after months of inactivity, when win-back costs are highest.
- **Intuition-Based Merchandising**: Cross-sell bundles and stock allocations are made on gut feel rather than co-purchase evidence.

---

## 2. What I Built

Profitara is a complete, laptop-runnable retail analytics and machine learning pipeline operating on a dual-dataset architecture:
1. **Interactive Storytelling Layer**: A 10,000-row synthetic Indian quick-commerce dataset powering a 13-page Streamlit dashboard and Power BI report modeling fast-delivery unit economics (Instant 10–15 min vs Express).
2. **Machine Learning Core**: A real public transaction dataset from the UCI Machine Learning Repository (541,909 rows, 4,372 customers) used for leakage-free, time-split predictive modeling.
3. **Embedded OLAP Layer**: A local DuckDB database powering 11 production analytical queries and an automated Retail Analyst Agent.

---

## 3. Top 3 Verified Headline Results

| Metric | Verified Value | Business Meaning |
|---|:---:|---|
| **Optimized Win-Back Return** | **+£720.03** | Under a fixed £1,500 marketing budget, our Expected Value policy ($EV = P(\text{churn}) \times \text{CLV} \times \text{margin} - \text{cost}$) generates **+£720.03** simulated net return, significantly outperforming naive recency outreach (+£31.60) and random marketing (-£19.19). |
| **Holiday Forecast Accuracy** | **4.10% MAPE** | In a 3-fold rolling-origin backtest, Holt-Winters exponential smoothing achieved **4.10% MAPE** during holiday peak demand, outperforming autoregressive machine learning models. |
| **High-Lift Cross-Sell Pairs** | **27.86× Lift** | Market basket analysis on 17,512 real retail baskets isolated 248 actionable cross-sell rules with statistical lift up to 27.86× (73.7% confidence), enabling evidence-based promotional bundling. |

---

## 4. How to Run the Demo in 60 Seconds

The entire project is laptop-runnable with fixed random seeds and zero paid cloud dependencies:

```bash
# 1. Clone repository and install dependencies
pip install -r requirements.txt

# 2. Run the complete pipeline (models, SQL, benchmarks, tests)
python run_all.py

# 3. Launch the 13-page interactive dashboard
streamlit run 05_Streamlit_Dashboard/app.py
```
*(Opens live in browser at `http://localhost:8501`)*
