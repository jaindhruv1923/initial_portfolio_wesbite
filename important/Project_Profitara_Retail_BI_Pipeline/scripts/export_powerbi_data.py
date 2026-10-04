import os
import duckdb
import pandas as pd

DB_PATH = os.path.join("data", "profitara.duckdb")
EXPORT_DIR = os.path.join("Power_BI", "clean_csv_export")
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_powerbi_tables():
    print(f"[Power BI Export] Connecting to {DB_PATH}...")
    con = duckdb.connect(DB_PATH, read_only=True)

    tables = {
        "fact_india_orders.csv": "SELECT * FROM india_orders",
        "dim_customer_segments.csv": "SELECT * FROM customer_segments",
        "dim_clv_predictions.csv": "SELECT * FROM clv_predictions",
        "dim_winback_queue.csv": "SELECT * FROM winback_targets",
        "dim_association_rules.csv": "SELECT * FROM association_rules",
        "summary_monthly_kpis.csv": """
            SELECT 
                STRFTIME(order_date, '%Y-%m') AS order_month,
                ROUND(SUM(sales), 2) AS total_sales,
                ROUND(SUM(profit), 2) AS total_profit,
                ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS net_margin_pct,
                COUNT(DISTINCT order_id) AS total_orders,
                COUNT(DISTINCT customer_id) AS active_customers
            FROM india_orders
            GROUP BY STRFTIME(order_date, '%Y-%m')
            ORDER BY order_month
        """
    }

    for fname, query in tables.items():
        out_p = os.path.join(EXPORT_DIR, fname)
        df = con.execute(query).fetchdf()
        df.to_csv(out_p, index=False)
        print(f"  Exported {fname}: {len(df):,} rows -> {out_p}")

    con.close()
    print("[Power BI Export] Clean CSV exports ready for Power BI refresh.")

if __name__ == "__main__":
    export_powerbi_tables()
