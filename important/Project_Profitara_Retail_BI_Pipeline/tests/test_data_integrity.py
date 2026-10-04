import os
import sys
import duckdb
import pandas as pd
import numpy as np
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

DB_PATH = os.path.join(PROJECT_ROOT, "data", "profitara.duckdb")
INDIA_CSV = os.path.join(PROJECT_ROOT, "data", "raw", "Profitara_India_Dataset.csv")
if not os.path.exists(INDIA_CSV):
    INDIA_CSV = os.path.join(PROJECT_ROOT, "01_Dataset", "Profitara_India_Dataset.csv")

def test_sql_vs_pandas_reconciliation():
    """Verify exact financial and volume reconciliation between pandas CSV and DuckDB table."""
    df_pd = pd.read_csv(INDIA_CSV)
    
    con = duckdb.connect(DB_PATH, read_only=True)
    res = con.execute("""
        SELECT 
            COUNT(*) AS row_count,
            COUNT(DISTINCT order_id) AS total_orders,
            COUNT(DISTINCT customer_id) AS total_customers,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit
        FROM india_orders
    """).fetchdf().iloc[0]
    con.close()

    # Reconcile row counts
    assert len(df_pd) == res["row_count"] == 10000, "Row count mismatch between pandas and DuckDB"
    # Reconcile orders
    assert df_pd["Order ID"].nunique() == res["total_orders"] == 4918, "Order count mismatch"
    # Reconcile customers
    assert df_pd["Customer ID"].nunique() == res["total_customers"] == 1448, "Customer count mismatch"
    # Reconcile total sales
    assert np.isclose(df_pd["Sales"].sum(), res["total_sales"], atol=1e-2), "Sales sum mismatch"
    # Reconcile total profit
    assert np.isclose(df_pd["Profit"].sum(), res["total_profit"], atol=1e-2), "Profit sum mismatch"

def test_unique_customer_identifiers_in_segments():
    """Ensure no duplicate customer IDs in segmentation tables."""
    con = duckdb.connect(DB_PATH, read_only=True)
    seg_counts = con.execute("SELECT customerid, COUNT(*) AS cnt FROM customer_segments GROUP BY customerid HAVING cnt > 1").fetchall()
    con.close()
    assert len(seg_counts) == 0, f"Found duplicate customer IDs in segmentation table: {seg_counts[:5]}"

def test_positive_financial_values():
    """Ensure sales amounts in fact tables are strictly positive."""
    con = duckdb.connect(DB_PATH, read_only=True)
    neg_sales = con.execute("SELECT COUNT(*) FROM india_orders WHERE sales <= 0").fetchone()[0]
    con.close()
    assert neg_sales == 0, f"Found {neg_sales} non-positive sales rows in india_orders"
