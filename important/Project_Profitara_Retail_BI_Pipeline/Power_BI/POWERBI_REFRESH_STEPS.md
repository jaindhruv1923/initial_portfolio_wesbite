# Power BI Dashboard Refresh & Data Source Update Guide

This guide walks you step-by-step through refreshing the Power BI report (`Profitara_BIDashBoard.pbix`) with the clean, audited datasets.

> **CRITICAL**: Never modify `.pbix` files with external scripts or binary editors. Power BI reports are binary ZIP packages that corrupt if edited programmatically. Always perform updates inside Power BI Desktop following these exact steps.

---

## 1. Clean Data Source Location

The cleaned, reconciled CSV files are located in:
```
Power_BI/clean_csv_export/
├── fact_india_orders.csv          # 10,000 retail orders (Sales, Profit, Margin, SLA)
├── dim_customer_segments.csv      # 4,334 segmented customers (k=4 K-Means)
├── dim_clv_predictions.csv        # 996 test customers with out-of-time CLV predictions
├── dim_winback_queue.csv          # 274 high-priority win-back targets (Expected Value ranked)
├── dim_association_rules.csv      # 248 Apriori cross-sell rules
└── summary_monthly_kpis.csv       # 36 monthly financial summaries (2023 - 2025)
```

---

## 2. Step-by-Step Refresh in Power BI Desktop

### Step A: Open the File
1. Launch **Power BI Desktop**.
2. Open `Power_BI/Profitara_BIDashBoard.pbix`.

### Step B: Open Power Query Editor
1. In the **Home** ribbon, click **Transform Data** → **Transform Data**.
2. In the left panel (*Queries*), identify the existing queries (`Orders`, `Customers`, etc.).

### Step C: Update Source File Path
1. Select a query (e.g. `Orders` or `Fact_Orders`).
2. In the right panel (*Applied Steps*), click the **Gear Icon** ⚙️ next to the **Source** step.
3. Browse to the absolute path of:
   `Power_BI\clean_csv_export\fact_india_orders.csv`
4. Click **OK**.
5. Repeat for any customer or segmentation tables, pointing them to `dim_customer_segments.csv`.

### Step D: Confirm Column Data Types
Ensure the following types are recognized:
- `order_date`, `ship_date`: **Date**
- `sales`, `profit`, `discount`: **Decimal Number**
- `quantity`: **Whole Number**
- `order_id`, `customer_id`: **Text**

### Step E: Apply and Close
1. In the top-left of the Power Query editor, click **Close & Apply**.
2. Power BI will reload the data and recompute all DAX measures and visuals.

---

## 3. Recommended DAX Measures to Verify

Verify that your DAX measures reflect the audited formulas:

```dax
// 1. Total Sales Revenue
Total Sales = SUM(fact_india_orders[sales])

// 2. Total Profit
Total Profit = SUM(fact_india_orders[profit])

// 3. Profit Margin %
Profit Margin Pct = DIVIDE([Total Profit], [Total Sales], 0) * 100

// 4. Total Orders
Total Orders = DISTINCTCOUNT(fact_india_orders[order_id])

// 5. Total Customers
Total Customers = DISTINCTCOUNT(fact_india_orders[customer_id])

// 6. Average Order Value (AOV)
AOV = DIVIDE([Total Sales], [Total Orders], 0)
```

---

## 4. Visual Icon Alignment

Custom icons matching the Profitara theme are stored in `Power_BI/`:
- `transactions-arrow.png` -> Total Orders KPI Card
- `rupee-value.png` -> Total Revenue KPI Card
- `users-group.png` -> Unique Customers KPI Card
- `coin-stack.png` -> Net Profit / Margin Card

Insert via: **Insert Tab** → **Image** → Select PNG → Resize to 36×36px or 40×40px and position top-left of the KPI card visual.
