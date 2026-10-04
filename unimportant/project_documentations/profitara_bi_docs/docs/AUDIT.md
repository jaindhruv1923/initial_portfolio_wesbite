# Project Audit: Profitara — Retail BI & Customer Analytics

**Audit Date**: October 2026  
**Auditor**: Senior Data Scientist & Analytics Engineer  
**Workspace**: `Project-Profitara-Retail-BI-Pipeline-main`  
**Git Commit Audited**: `2c244f1` (branch: `upgrade`)

---

## 1. Executive Summary & What the Project Does Plainly

Profitara is presented as a retail business intelligence platform and customer analytics pipeline modeling an Indian quick-commerce / grocery retail business (order ID prefix `BLK-`, reminiscent of Blinkit / Zepto). 

The repository consists of:
- A transaction dataset (`01_Dataset/Profitara_India_Dataset.csv`) with 10,000 rows spanning 2023–2025.
- A Jupyter notebook (`04_ML_Pipeline/Profitara_ML_Pipeline.ipynb`) executing 6 ML modules: RFM feature engineering, K-Means clustering, Random Forest regression for CLV, Logistic Regression for churn classification, Apriori market basket analysis, Isolation Forest for discount-abuse detection, and Holt-Winters revenue forecasting.
- Business analyst documentation (`07_BA_Documentation/`) including a Business Requirements Document (BRD), Executive Summary, and Process Flow.
- A standalone HTML dashboard (`06_Standalone_HTML_Dashboard/Profitara_Golden_Dashboard__3_.html`).
- An Excel workbook (`02_Excel_Workbook/Profitara_Golden_Excel__1_.xlsx`).
- A SQL file (`03_SQL/Profitara_Complete.sql`).
- A Streamlit dashboard folder (`05_Streamlit_Dashboard/`) where `app.py` was previously overwritten by an unrelated upload, leaving `READ_THIS_MISSING_FILE.txt`.
- Power BI artifacts (`Power_BI/Profitara_BIDashBoard.pbix` and `Power_BI/README.md`).

---

## 2. Dataset Audit: Real vs. Synthetic Analysis

### 2.1 File & Schema
- **File**: `01_Dataset/Profitara_India_Dataset.csv`
- **Dimensions**: Exactly 10,000 rows × 21 columns.
- **Date Range**: January 1, 2023 to December 31, 2025 (3 calendar years).
- **Core Entities**: 4,918 unique orders, 1,448 unique customer IDs, 9 product categories, 17 sub-categories, 66 product names.
- **Financial Totals**: Total Sales = ₹6,695,229.31 (₹66.95 Lakhs); Total Profit = ₹278,183.93; Aggregate Net Margin = 4.1549%.

### 2.2 Proof of Synthetic Generation
The dataset is **unquestionably synthetic**. Multiple statistical signatures confirm programmatic generation:
1. **Postal Code Artifact**: Gurugram has 680 rows and 680 distinct postal codes; Pune has 660 rows and 660 distinct postal codes; New Delhi has 1,288 rows and 1,287 distinct postal codes. In reality, an Indian city contains a discrete set of postal PIN codes. Here, postal codes were generated via random integers for almost every transaction.
2. **Customer ID vs Name Disparity**: There are 1,448 unique `Customer ID` entries (`CUST-10000` to `CUST-11799`), but only 668 unique `Customer Name` strings. The generator cycled through a name list with replacement.
3. **Product ID vs Name Disparity**: There are 9,950 unique `Product ID` strings for only 66 unique `Product Name` entries. Nearly every transaction row was assigned a newly minted Product ID.
4. **Deterministic Discount Margins**: Across all 10,000 rows, discount is restricted to exactly 7 discrete values: `{0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4}`. Margin is a linear decay function of discount:
   - Discount 0.00: Mean margin +10.53%
   - Discount 0.05: Mean margin +4.68%
   - Discount 0.10: Mean margin +0.08%
   - Discount 0.15: Mean margin -4.66%
   - Discount 0.20: Mean margin -8.29%
   - Discount 0.30: Mean margin -14.95%
   - Discount 0.40: Mean margin -19.20%
5. **Discrete Quantities**: Quantities are strictly integers from 1 to 5 (`{1: 4501, 2: 2685, 3: 1515, 4: 825, 5: 474}`).
6. **Synthetic Benford & Festival Injection**: First-digit sales distribution adheres tightly to Benford's Law (digit 1: 30.37% vs 30.1% theoretical), and monthly volumes artificially spike every October/November (Diwali seasonality injection).

---

## 3. Reported Metrics & Exact Code Source

| Metric Claimed | Value | Source File | Cell / Line | Method / Formula |
|---|---|---|---|---|
| **Total Orders** | 4,918 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 5 | `df["Order ID"].nunique()` |
| **Unique Customers** | 1,448 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 5, 11 | `df["Customer ID"].nunique()` |
| **Total Revenue** | ₹6,695,229.31 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 5 | `df["Sales"].sum()` |
| **Total Profit** | ₹278,183.93 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 5 | `df["Profit"].sum()` |
| **Profit Margin %** | 4.15% | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 5 | `(Total Profit / Total Sales) * 100` |
| **CLV Model $R^2$** | 0.930 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 16 | Random Forest Regressor on customer RFM table |
| **CLV Model MAE** | ₹1,171.95 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 16 | `mean_absolute_error(y_test, preds)` |
| **Churn Model ROC-AUC**| 0.91 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 18 | Balanced Logistic Regression on RFM + margin |
| **Churn Model Accuracy**| 85% | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 18 | `accuracy_score(yc_test, churn_pred)` |
| **K-Means Silhouette** | 0.611 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 13 | Scikit-learn `silhouette_score` for $k=2$ |
| **Champion Customers** | 119 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 14 | Cluster 1 of K-Means ($k=2$) |
| **At-Risk Customers** | 361 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 18, 33 | `cust["Recency"] > cust["Recency"].quantile(0.75)` |
| **Cross-Sell Rules** | 52 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 20 | Mlxtend Apriori (min_support=0.01, min_lift=1.0) |
| **Top Rule Lift** | 9.576 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 20 | Baby Food → Diapers & Wipes |
| **Anomalies Flagged** | 300 (3.0%) | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 22 | Isolation Forest (contamination=0.03) |
| **Business Health Score**| 50.2 / 100 | `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb` | Cell 31 | Composite index of 4 heuristic components |

---

## 4. Methodological & Validity Risks

### 4.1 Fatal Target Leakage in CLV ($R^2 = 0.930$)
In Cell 16 of `Profitara_ML_Pipeline.ipynb`:
- Features used: `["Recency", "Frequency", "AvgDiscount", "AvgOrderValue", "Tenure"]`
- Target: `Monetary`
- **Leakage mechanism**: By definition, `Monetary` is total customer spend, and `AvgOrderValue` is computed in Cell 11 as `Sales.mean()`, which is identical to `Monetary / Frequency`. Therefore:
  $$\text{Target} = \text{Frequency} \times \text{AvgOrderValue}$$
  The model was given $A$ and $B$ to predict $A \times B$. An ensemble of decision trees easily learns this multiplication, yielding an inflated $R^2 = 0.930$.
- **Split invalidity**: Evaluated on a random `train_test_split(test_size=0.2)`. Features and target were computed over the exact same time window (the entire 3 years). No future time window was withheld. In production, an analyst never predicts historical spend from historical spend; one predicts *future* window spend from *past* window features.

### 4.2 Circular Leakage in Churn Prediction (AUC = 0.91)
In Cell 18:
- Target definition: `cust["Churned"] = (cust["Recency"] > quantile(0.75)).astype(int)`
- Features: `["Frequency", "Monetary", "AvgDiscount", "AvgOrderValue", "Tenure", "Margin"]`
- **Leakage mechanism**: `Tenure` is defined as `snapshot_date - first_order_date`, and `Recency` is `snapshot_date - last_order_date`. For one-time buyers (which comprise the majority of churned customers), $\text{Tenure} = \text{Recency}$. When a customer has low frequency and high tenure, their recency is algebraically guaranteed to exceed the 75th percentile.
- **Split invalidity**: Random train/test split across customers over the same static snapshot. There is no out-of-time validation or cohort split.

### 4.3 Degenerate Clustering ($k=2$, Silhouette 0.611)
- The notebook selects $k=2$ purely because silhouette peaks at 2 clusters.
- Looking at Cell 14:
  - Cluster 0: 1,329 customers ("Loyal", avg spend ₹3,228, frequency 2.48)
  - Cluster 1: 119 customers ("Champions", avg spend ₹20,205, frequency 13.65)
- Selecting $k=2$ merely separates 119 heavy outliers from the remaining 92% of the customer base. It offers zero operational segmentation for "At-Risk", "Need Attention", "Promising", or "Hibernating" customers.
- The claim of "361 at-risk customers" came from the recency 75th percentile heuristic in Cell 18, NOT from the K-Means clustering.

### 4.4 Disconnected SQL & Superstore Contamination
- `03_SQL/Profitara_Complete.sql` contains 9,994 hardcoded `INSERT` statements for the **US Superstore** dataset (2014–2017, USD amounts, US states like California and Texas, customer Sean Miller). It does NOT query or contain the Indian dataset!
- `02_Excel_Workbook/Profitara_Golden_Excel__1_.xlsx` also contains US Superstore data ($2,297,200.86 revenue, $286,397.02 profit, 793 customers, XGBoost R²).
- `06_Standalone_HTML_Dashboard/Profitara_Golden_Dashboard__3_.html` contains embedded Javascript running AlaSQL over 9,994 rows of US Superstore data with 241 dollar signs (`$`), mixed with copy referring to Indian numbers.

---

## 5. Audit of Resume Claims

| Resume Claim | Audit Status | Evidence / Analysis |
|---|---|---|
| **10,000 transactions** | **VERIFIED** | Exactly 10,000 rows in `01_Dataset/Profitara_India_Dataset.csv`. Note: `03_SQL` has 9,994 (Superstore). |
| **4,918 orders** | **VERIFIED** | Exactly 4,918 distinct `Order ID`s in Indian CSV. |
| **1,448 customers** | **VERIFIED** | Exactly 1,448 distinct `Customer ID`s in Indian CSV. |
| **9 categories** | **VERIFIED** | Exactly 9 categories in Indian CSV. |
| **₹66.95L revenue at 4.15% margin** | **VERIFIED** | Sum of Sales = ₹66,95,229.31; Profit = ₹278,183.93; Margin = 4.1549%. |
| **Random Forest CLV $R^2 = 0.930$** | **VERIFIED BUT FATALLY LEAKED** | Exact code output in Cell 16, but completely invalid due to `Monetary = Frequency * AvgOrderValue` identity leakage and random split. Must be replaced with honest time-split CLV. |
| **Churn AUC 0.91 with 85% accuracy** | **VERIFIED BUT LEAKED** | Exact output in Cell 18, but circular definition and static snapshot split. Must be replaced with honest time-split churn. |
| **361 at-risk customers** | **WRONG / MISREPRESENTED** | Not an ML cluster. 361 is strictly $1,448 \times 0.25$ (the arbitrary 75th percentile recency cutoff used as the churn target). K-Means found only 2 clusters ($k=2$). |
| **K-Means silhouette 0.611** | **VERIFIED BUT DEGENERATE** | Exact output in Cell 13 for $k=2$, which only separates 119 outliers from 1,329 customers. A 4- or 5-segment RFM model is required for business utility. |
| **52 cross-sell rules** | **VERIFIED** | Exactly 52 rules generated by `association_rules(metric="lift", min_threshold=1.0)` in Cell 20. |
| **Isolation Forest** | **VERIFIED** | IsolationForest with contamination=0.03 flagged 300 transactions (3.0%) in Cell 22. |

---

## 6. What is Strong and Should Be Kept

1. **Business Problem Framing & Aesthetics**: The visual styling, Atkinson Hyperlegible typography, color scheme (`#146B5E`, `#C98A2E`), and 13-page narrative structure in the HTML dashboard and README are compelling and tailored for retail analytics.
2. **Business Requirements Document (BRD) & Process Flow**: The documentation structure in `07_BA_Documentation/` demonstrates strong analytical maturity and business understanding.
3. **Market Basket Association Rules**: The Apriori setup at the sub-category level works cleanly and produces logical quick-commerce pairings (Baby Food → Diapers & Wipes, Bread & Eggs → Milk & Curd).
4. **Discount-Elasticity Concept**: The idea of evaluating margin decay across discount bands and searching for optimal discount thresholds is sound business analysis.
5. **Quick-Commerce Storytelling**: The Indian dataset is a great storytelling vehicle for an India-based candidate targeting domestic analytics firms (e.g. Zepto, Blinkit, Swiggy Instamart, Flipkart).
