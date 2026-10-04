import os
import json
import duckdb
import pandas as pd

DB_PATH = os.path.join("data", "profitara.duckdb")
QA_CSV_PATH = "QA_PAIRS_TO_REVIEW.csv"
FIXTURES_PATH = os.path.join("agent", "fixtures.json")

PAIRS = [
    # Core Financial & Volume KPIs
    ("What is the total sales revenue across all orders?",
     "SELECT ROUND(SUM(sales), 2) AS total_revenue FROM india_orders",
     "india_orders", "Simple"),
    ("What is the total net profit and aggregate profit margin?",
     "SELECT ROUND(SUM(profit), 2) AS total_profit, ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS margin_pct FROM india_orders",
     "india_orders", "Simple"),
    ("How many distinct orders and unique customers are in the dataset?",
     "SELECT COUNT(DISTINCT order_id) AS total_orders, COUNT(DISTINCT customer_id) AS total_customers FROM india_orders",
     "india_orders", "Simple"),
    ("What is the overall average order value (AOV)?",
     "SELECT ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value FROM india_orders",
     "india_orders", "Simple"),
    ("What is the average discount percentage applied across all transactions?",
     "SELECT ROUND(AVG(discount) * 100, 2) AS avg_discount_pct FROM india_orders",
     "india_orders", "Simple"),

    # Category & Product Performance
    ("What are the total sales and profit by product category?",
     "SELECT category, ROUND(SUM(sales), 2) AS sales, ROUND(SUM(profit), 2) AS profit FROM india_orders GROUP BY category ORDER BY sales DESC",
     "india_orders", "Medium"),
    ("Which category has the highest profit margin percentage?",
     "SELECT category, ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS margin_pct FROM india_orders GROUP BY category ORDER BY margin_pct DESC LIMIT 1",
     "india_orders", "Medium"),
    ("What are the top 5 sub-categories by sales revenue?",
     "SELECT sub_category, ROUND(SUM(sales), 2) AS total_sales FROM india_orders GROUP BY sub_category ORDER BY total_sales DESC LIMIT 5",
     "india_orders", "Simple"),
    ("Which sub-category generates the largest operational loss?",
     "SELECT sub_category, ROUND(SUM(profit), 2) AS total_loss FROM india_orders GROUP BY sub_category ORDER BY total_loss ASC LIMIT 1",
     "india_orders", "Simple"),
    ("What are the top 10 best-selling products by sales revenue?",
     "SELECT product_name, ROUND(SUM(sales), 2) AS total_sales FROM india_orders GROUP BY product_name ORDER BY total_sales DESC LIMIT 10",
     "india_orders", "Simple"),
    ("Which 5 products have the highest total quantity sold?",
     "SELECT product_name, SUM(quantity) AS total_units FROM india_orders GROUP BY product_name ORDER BY total_units DESC LIMIT 5",
     "india_orders", "Simple"),

    # Delivery SLA & Shipping Modes
    ("What is the revenue and order breakdown by delivery SLA mode?",
     "SELECT ship_mode, COUNT(DISTINCT order_id) AS orders, ROUND(SUM(sales), 2) AS revenue FROM india_orders GROUP BY ship_mode ORDER BY revenue DESC",
     "india_orders", "Medium"),
    ("What is the profit margin for Instant delivery compared to Express and Scheduled?",
     "SELECT ship_mode, ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS margin_pct FROM india_orders GROUP BY ship_mode ORDER BY margin_pct DESC",
     "india_orders", "Medium"),
    ("What is the average order value for Instant 10-15 min delivery?",
     "SELECT ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS instant_aov FROM india_orders WHERE ship_mode = 'Instant (10-15 min)'",
     "india_orders", "Simple"),

    # Geographic & Regional Breakdown
    ("What are the total sales and profit by geographic region?",
     "SELECT region, ROUND(SUM(sales), 2) AS total_sales, ROUND(SUM(profit), 2) AS total_profit FROM india_orders GROUP BY region ORDER BY total_sales DESC",
     "india_orders", "Simple"),
    ("What are the top 5 states by sales revenue?",
     "SELECT state, ROUND(SUM(sales), 2) AS total_sales FROM india_orders GROUP BY state ORDER BY total_sales DESC LIMIT 5",
     "india_orders", "Simple"),
    ("What are the top 10 cities by order volume?",
     "SELECT city, COUNT(DISTINCT order_id) AS order_count FROM india_orders GROUP BY city ORDER BY order_count DESC LIMIT 10",
     "india_orders", "Simple"),
    ("Which state has the lowest profit margin?",
     "SELECT state, ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS margin_pct FROM india_orders GROUP BY state ORDER BY margin_pct ASC LIMIT 1",
     "india_orders", "Medium"),

    # Customer Segments & RFM Analytics
    ("What is the customer count and revenue share of each customer segment?",
     "SELECT segment_name, COUNT(*) AS customer_count, ROUND(SUM(monetary), 2) AS total_revenue FROM customer_segments GROUP BY segment_name ORDER BY total_revenue DESC",
     "customer_segments", "Medium"),
    ("What is the average spend and order frequency for Champions & VIPs?",
     "SELECT ROUND(AVG(monetary), 2) AS avg_spend, ROUND(AVG(frequency), 2) AS avg_freq FROM customer_segments WHERE segment_name = 'Champions & VIPs'",
     "customer_segments", "Simple"),
    ("How many customers belong to the Hibernating segment?",
     "SELECT COUNT(*) AS hibernating_count FROM customer_segments WHERE segment_name = 'Hibernating / Low-Value Inactive'",
     "customer_segments", "Simple"),
    ("What is the average recency in days for At-Risk customers?",
     "SELECT ROUND(AVG(recency), 1) AS avg_recency FROM customer_segments WHERE segment_name = 'At-Risk / Lapsing Spenders'",
     "customer_segments", "Simple"),

    # Discount Impact & Revenue Leakage
    ("How many orders received a discount of 30% or more?",
     "SELECT COUNT(DISTINCT order_id) AS high_discount_orders FROM india_orders WHERE discount >= 0.30",
     "india_orders", "Simple"),
    ("What is the total loss from unprofitable orders?",
     "SELECT ROUND(SUM(profit), 2) AS total_loss, COUNT(*) AS loss_items_count FROM india_orders WHERE profit < 0",
     "india_orders", "Simple"),
    ("What is the average profit margin when discount is zero versus when discount is greater than 20%?",
     "SELECT CASE WHEN discount = 0 THEN 'No Discount' ELSE 'Discount > 20%' END AS discount_group, ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS margin_pct FROM india_orders WHERE discount = 0 OR discount > 0.20 GROUP BY CASE WHEN discount = 0 THEN 'No Discount' ELSE 'Discount > 20%' END",
     "india_orders", "Complex"),

    # Customer Lifetime Value & Win-Back Optimization
    ("Who are the top 10 customers with the highest predicted future spend in CLV?",
     "SELECT customerid, predspend_rf FROM clv_predictions ORDER BY predspend_rf DESC LIMIT 10",
     "clv_predictions", "Simple"),
    ("How many customers in the test cohort have a predicted 90-day spend over £1000?",
     "SELECT COUNT(*) AS count_high_clv FROM clv_predictions WHERE predspend_rf > 1000",
     "clv_predictions", "Simple"),
    ("What is the average predicted future spend across all test customers?",
     "SELECT ROUND(AVG(predspend_rf), 2) AS avg_predicted_clv FROM clv_predictions",
     "clv_predictions", "Simple"),
    ("What is the total expected net value of contacting all prioritized win-back candidates?",
     "SELECT ROUND(SUM(expected_net_value), 2) AS total_expected_net_recovery FROM winback_targets",
     "winback_targets", "Simple"),
    ("How many win-back targets have an expected net value greater than £10?",
     "SELECT COUNT(*) AS high_roi_targets FROM winback_targets WHERE expected_net_value > 10",
     "winback_targets", "Simple"),
    ("Who are the top 5 win-back targets ranked by expected net value?",
     "SELECT customerid, prob_churn, pred_clv, expected_net_value FROM winback_targets ORDER BY expected_net_value DESC LIMIT 5",
     "winback_targets", "Simple"),

    # Market Basket Analysis (Apriori Rules)
    ("What are the top 5 association rules with the highest statistical lift?",
     "SELECT rule_expression, lift, confidence FROM association_rules ORDER BY lift DESC LIMIT 5",
     "association_rules", "Simple"),
    ("How many association rules have a confidence of at least 70%?",
     "SELECT COUNT(*) AS high_confidence_rules FROM association_rules WHERE confidence >= 0.70",
     "association_rules", "Simple"),
    ("What is the maximum lift found among the surviving cross-sell rules?",
     "SELECT ROUND(MAX(lift), 3) AS max_lift FROM association_rules",
     "association_rules", "Simple"),

    # Monthly Trends & Cohorts
    ("What was the monthly revenue in October 2025?",
     "SELECT ROUND(SUM(sales), 2) AS oct_2025_revenue FROM india_orders WHERE STRFTIME(order_date, '%Y-%m') = '2025-10'",
     "india_orders", "Simple"),
    ("What is the monthly sales and profit trend for the year 2025?",
     "SELECT STRFTIME(order_date, '%Y-%m') AS month, ROUND(SUM(sales), 2) AS sales, ROUND(SUM(profit), 2) AS profit FROM india_orders WHERE STRFTIME(order_date, '%Y') = '2025' GROUP BY STRFTIME(order_date, '%Y-%m') ORDER BY month",
     "india_orders", "Medium"),
    ("Which month had the highest total revenue across the entire dataset?",
     "SELECT STRFTIME(order_date, '%Y-%m') AS peak_month, ROUND(SUM(sales), 2) AS sales FROM india_orders GROUP BY STRFTIME(order_date, '%Y-%m') ORDER BY sales DESC LIMIT 1",
     "india_orders", "Medium"),
    ("How many customers made their first purchase in January 2023?",
     "WITH first_orders AS (SELECT customer_id, MIN(order_date) AS first_date FROM india_orders GROUP BY customer_id) SELECT COUNT(*) AS jan_2023_cohort FROM first_orders WHERE STRFTIME(first_date, '%Y-%m') = '2023-01'",
     "india_orders", "Complex"),
    ("What is the repeat buyer rate for customers who joined in 2023?",
     "WITH cust_orders AS (SELECT customer_id, MIN(order_date) AS first_date, COUNT(DISTINCT order_id) AS total_orders FROM india_orders GROUP BY customer_id) SELECT ROUND(SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS repeat_rate_pct FROM cust_orders WHERE STRFTIME(first_date, '%Y') = '2023'",
     "india_orders", "Complex"),
    ("What percentage of total revenue is contributed by the top 10 customers?",
     "WITH top10 AS (SELECT SUM(sales) AS top_sales FROM (SELECT customer_id, SUM(sales) AS sales FROM india_orders GROUP BY customer_id ORDER BY sales DESC LIMIT 10)), total AS (SELECT SUM(sales) AS grand_sales FROM india_orders) SELECT ROUND(top10.top_sales * 100.0 / total.grand_sales, 2) AS top10_revenue_share_pct FROM top10, total",
     "india_orders", "Complex")
]

def generate():
    con = duckdb.connect(DB_PATH, read_only=True)
    records = []
    fixtures = {}

    print(f"Validating and generating {len(PAIRS)} QA pairs...")
    for idx, (q, sql, table, complexity) in enumerate(PAIRS, 1):
        # Validate that SQL executes without error on DuckDB
        try:
            res = con.execute(sql).fetchdf()
            assert len(res) > 0, "Query returned 0 rows"
        except Exception as e:
            print(f"Error on pair {idx}: {q}\nSQL: {sql}\nError: {e}")
            raise e

        fixtures[q] = sql
        records.append({
            "id": idx,
            "question": q,
            "reference_sql": sql,
            "table_used": table,
            "complexity": complexity,
            "status": "machine-generated, unreviewed",
            "reviewer_notes": "Pending user review (mark correct/incorrect)"
        })

    con.close()

    # Save to QA_PAIRS_TO_REVIEW.csv
    df_qa = pd.DataFrame(records)
    df_qa.to_csv(QA_CSV_PATH, index=False)
    print(f"Saved {len(df_qa)} pairs to {QA_CSV_PATH} with status 'machine-generated, unreviewed'.")

    # Save to agent/fixtures.json
    with open(FIXTURES_PATH, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2)
    print(f"Saved {len(fixtures)} fixtures to {FIXTURES_PATH}.")

if __name__ == "__main__":
    generate()
