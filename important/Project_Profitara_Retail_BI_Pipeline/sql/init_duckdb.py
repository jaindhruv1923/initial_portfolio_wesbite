import os
import sys
import duckdb
import pandas as pd

DB_PATH = os.path.join("data", "profitara.duckdb")
INDIA_CSV = os.path.join("data", "raw", "Profitara_India_Dataset.csv")
if not os.path.exists(INDIA_CSV):
    INDIA_CSV = os.path.join("01_Dataset", "Profitara_India_Dataset.csv")
REAL_CSV = os.path.join("data", "real", "online_retail_II.csv")
SEG_CSV = os.path.join("reports", "rfm_segmented_customers.csv")
CLV_CSV = os.path.join("reports", "clv_test_predictions.csv")
WINBACK_CSV = os.path.join("reports", "winback_priority_targets.csv")
RULES_CSV = os.path.join("reports", "apriori_surviving_rules.csv")

def init_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    print(f"[DuckDB Init] Initializing database at: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    # 1. Load India Quick-Commerce Dataset
    print(f"[DuckDB Init] Loading india_orders from {INDIA_CSV}...")
    df_india = pd.read_csv(INDIA_CSV)
    df_india["Order Date"] = pd.to_datetime(df_india["Order Date"])
    df_india["Ship Date"] = pd.to_datetime(df_india["Ship Date"])
    df_india.columns = [c.lower().replace(" ", "_").replace("-", "_") for c in df_india.columns]
    con.execute("CREATE TABLE india_orders AS SELECT * FROM df_india")
    count_india = con.execute("SELECT COUNT(*) FROM india_orders").fetchone()[0]
    print(f"  india_orders table created with {count_india:,} rows.")

    # 2. Load Real Retail Transactions
    if os.path.exists(REAL_CSV):
        print(f"[DuckDB Init] Loading real_transactions from {REAL_CSV}...")
        df_real = pd.read_csv(REAL_CSV)
        df_real = df_real.dropna(subset=["CustomerID"]).copy()
        df_real["CustomerID"] = df_real["CustomerID"].astype(int).astype(str)
        df_real["InvoiceDate"] = pd.to_datetime(df_real["InvoiceDate"])
        df_real = df_real[(df_real["Quantity"] > 0) & (df_real["UnitPrice"] > 0)].copy()
        df_real["TotalAmount"] = df_real["Quantity"] * df_real["UnitPrice"]
        df_real.columns = [c.lower() for c in df_real.columns]
        con.execute("CREATE TABLE real_transactions AS SELECT * FROM df_real")
        count_real = con.execute("SELECT COUNT(*) FROM real_transactions").fetchone()[0]
        print(f"  real_transactions table created with {count_real:,} rows.")

    # 3. Load Customer Segments
    if os.path.exists(SEG_CSV):
        print(f"[DuckDB Init] Loading customer_segments from {SEG_CSV}...")
        df_seg = pd.read_csv(SEG_CSV)
        con.execute("CREATE TABLE customer_segments AS SELECT * FROM df_seg")
        print(f"  customer_segments table created with {len(df_seg):,} rows.")

    # 4. Load CLV Test Predictions
    if os.path.exists(CLV_CSV):
        print(f"[DuckDB Init] Loading clv_predictions from {CLV_CSV}...")
        df_clv = pd.read_csv(CLV_CSV)
        con.execute("CREATE TABLE clv_predictions AS SELECT * FROM df_clv")
        print(f"  clv_predictions table created with {len(df_clv):,} rows.")

    # 5. Load Priority Win-Back Targets
    if os.path.exists(WINBACK_CSV):
        print(f"[DuckDB Init] Loading winback_targets from {WINBACK_CSV}...")
        df_win = pd.read_csv(WINBACK_CSV)
        con.execute("CREATE TABLE winback_targets AS SELECT * FROM df_win")
        print(f"  winback_targets table created with {len(df_win):,} rows.")

    # 6. Load Association Rules
    if os.path.exists(RULES_CSV):
        print(f"[DuckDB Init] Loading association_rules from {RULES_CSV}...")
        df_rules = pd.read_csv(RULES_CSV)
        con.execute("CREATE TABLE association_rules AS SELECT * FROM df_rules")
        print(f"  association_rules table created with {len(df_rules):,} rows.")

    con.close()
    print("[DuckDB Init] DuckDB initialization completed successfully.")

if __name__ == "__main__":
    init_database()
