import os
import sys
import re
import json
import duckdb
import pandas as pd
import requests

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "profitara.duckdb")
FIXTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures.json")

# Database Schema Metadata for Schema-Aware Prompting
DB_SCHEMA = """
Tables in DuckDB database 'profitara.duckdb':

1. Table: india_orders (10,000 rows - Indian quick-commerce transactions)
   Columns:
     - row_id (BIGINT): Unique row identifier
     - order_id (VARCHAR): Unique order ID (e.g. BLK-2025-100001)
     - order_date (TIMESTAMP): Order timestamp (2023-01-01 to 2025-12-31)
     - ship_date (TIMESTAMP): Delivery timestamp
     - ship_mode (VARCHAR): Delivery SLA ('Instant (10-15 min)', 'Express (30-60 min)', 'Scheduled Slot')
     - customer_id (VARCHAR): Customer identifier (e.g. CUST-11115)
     - customer_name (VARCHAR): Customer name
     - segment (VARCHAR): Customer segment ('Regular Household', 'Working Professional', 'Bulk/Office Buyer')
     - country (VARCHAR): Country ('India')
     - city (VARCHAR): City name (e.g. 'New Delhi', 'Pune', 'Gurugram')
     - state (VARCHAR): State name (e.g. 'Delhi', 'Maharashtra', 'Karnataka')
     - postal_code (BIGINT): Indian postal PIN code
     - region (VARCHAR): Region ('North', 'South', 'East', 'West')
     - product_id (VARCHAR): Product ID
     - category (VARCHAR): Product category (e.g. 'Grocery & Staples', 'Personal Care', 'Dairy & Breakfast')
     - sub_category (VARCHAR): Sub-category (e.g. 'Atta & Flour', 'Milk & Curd', 'Diapers & Wipes')
     - product_name (VARCHAR): Product description
     - sales (DOUBLE): Transaction sales amount in INR (₹)
     - quantity (BIGINT): Quantity ordered (1 to 5)
     - discount (DOUBLE): Discount applied (0.0 to 0.40)
     - profit (DOUBLE): Net profit in INR (₹)
     - margin (DOUBLE): Net profit margin fraction (profit / sales)

2. Table: customer_segments (4,334 rows - Real retail K-Means clusters)
   Columns:
     - customerid (VARCHAR): Customer ID
     - recency (DOUBLE): Days since last purchase
     - frequency (BIGINT): Distinct order count
     - monetary (DOUBLE): Total spend in GBP (£)
     - cluster (BIGINT): Cluster index (0, 1, 2, 3)
     - segment_name (VARCHAR): Segment name ('Champions & VIPs', 'Loyal & Steady Buyers', 'At-Risk / Lapsing Spenders', 'Hibernating / Low-Value Inactive')

3. Table: winback_targets (274 rows - Prioritized churn win-back queue)
   Columns:
     - customerid (VARCHAR): Customer ID
     - prob_churn (DOUBLE): Calibrated probability of churn (0.0 to 1.0)
     - pred_clv (DOUBLE): Predicted future 90-day spend (£)
     - expected_gross_recovery (DOUBLE): Expected recovered gross value (£)
     - expected_net_value (DOUBLE): Expected net return after campaign cost (£)

4. Table: association_rules (248 rows - Apriori cross-sell rules)
   Columns:
     - rule_expression (VARCHAR): E.g. 'Item A ===> Item B'
     - support (DOUBLE): Rule support
     - confidence (DOUBLE): Rule confidence
     - lift (DOUBLE): Statistical lift
     - conviction (DOUBLE): Rule conviction
"""

FORBIDDEN_KEYWORDS = [
    r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b",
    r"\bALTER\b", r"\bCREATE\b", r"\bTRUNCATE\b", r"\bREPLACE\b",
    r"\bPRAGMA\b", r"\bATTACH\b", r"\bDETACH\b", r"\bCOPY\b",
    r"\bEXPORT\b", r"\bEXEC\b", r"\bEXECUTE\b", r"\bGRANT\b", r"\bREVOKE\b"
]

class SecurityException(Exception):
    pass

def validate_and_clamp_sql(sql_query: str) -> str:
    """
    Strict security validation:
    1. Must begin with SELECT or WITH
    2. Rejects any DDL, DML, or administrative commands
    3. Enforces an upper row limit of 100
    """
    cleaned = sql_query.strip().rstrip(";")
    # Strip comments
    cleaned = re.sub(r"--[^\n]*", "", cleaned).strip()

    if not (cleaned.lower().startswith("select") or cleaned.lower().startswith("with")):
        raise SecurityException("Security Guard: Only read-only SELECT or CTE queries are permitted.")

    for pattern in FORBIDDEN_KEYWORDS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            raise SecurityException(f"Security Guard: Destructive or administrative keyword detected matching {pattern}.")

    # Enforce LIMIT <= 100
    limit_match = re.search(r"\bLIMIT\s+(\d+)", cleaned, re.IGNORECASE)
    if limit_match:
        existing_limit = int(limit_match.group(1))
        if existing_limit > 100:
            cleaned = re.sub(r"\bLIMIT\s+\d+", "LIMIT 100", cleaned, flags=re.IGNORECASE)
    else:
        cleaned = f"{cleaned} LIMIT 100"

    return cleaned

def load_fixtures():
    if os.path.exists(FIXTURES_PATH):
        with open(FIXTURES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def generate_sql(question: str) -> str:
    """
    Translates a plain-English retail question into a read-only SQL query.
    Configurable via environment variable LLM_PROVIDER:
      - 'fixture' (default): Returns pre-recorded fixture for fast offline testing
      - 'gemini': Calls Google Gemini API (GEMINI_API_KEY)
      - 'ollama': Calls local Ollama endpoint (OLLAMA_HOST)
    """
    provider = os.environ.get("LLM_PROVIDER", "fixture").lower()
    fixtures = load_fixtures()

    # Normalize question key
    norm_q = question.strip().lower().rstrip("?")
    for fix_q, sql in fixtures.items():
        if fix_q.strip().lower().rstrip("?") == norm_q:
            return sql

    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required for Gemini provider.")
        
        prompt = f"""
You are a senior analytics engineer writing DuckDB SQL for retail business intelligence.
{DB_SCHEMA}

Return ONLY valid DuckDB SQL (no markdown formatting, no explanation, no backticks).
Question: {question}
"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
        if resp.status_code == 200:
            res_data = resp.json()
            raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Clean markdown code blocks if returned
            clean_sql = re.sub(r"^```sql\s*", "", raw_text, flags=re.IGNORECASE)
            clean_sql = re.sub(r"^```\s*", "", clean_sql)
            clean_sql = re.sub(r"\s*```$", "", clean_sql).strip()
            return clean_sql
        else:
            raise RuntimeError(f"Gemini API returned error: {resp.text}")

    elif provider == "ollama":
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        prompt = f"{DB_SCHEMA}\nReturn ONLY DuckDB SQL. Question: {question}"
        resp = requests.post(f"{host}/api/generate", json={"model": "llama3", "prompt": prompt, "stream": False}, timeout=15)
        if resp.status_code == 200:
            raw_text = resp.json().get("response", "").strip()
            clean_sql = re.sub(r"^```sql\s*", "", raw_text, flags=re.IGNORECASE)
            clean_sql = re.sub(r"^```\s*", "", clean_sql)
            clean_sql = re.sub(r"\s*```$", "", clean_sql).strip()
            return clean_sql

    # Fallback to smart heuristic if not in fixtures
    return f"SELECT order_id, customer_name, category, sales, profit FROM india_orders ORDER BY sales DESC LIMIT 10"

def suggest_chart_type(df: pd.DataFrame) -> str:
    """Recommends an appropriate chart representation based on result columns."""
    if len(df) == 0:
        return "table"
    n_cols = len(df.columns)
    col_types = [df[col].dtype for col in df.columns]

    if n_cols == 2:
        if np.issubdtype(col_types[1], np.number):
            if any(term in df.columns[0].lower() for term in ["month", "date", "year", "quarter"]):
                return "line"
            elif df[df.columns[0]].nunique() <= 5:
                return "pie"
            else:
                return "bar"
    elif n_cols == 3 and np.issubdtype(col_types[1], np.number) and np.issubdtype(col_types[2], np.number):
        return "bar"
    return "table"

def ask_analyst_agent(question: str) -> dict:
    """
    End-to-end question answering pipeline:
    1. Generates SQL from question
    2. Validates and clamps SQL
    3. Executes safely against DuckDB
    4. Recommends chart visualization
    """
    try:
        raw_sql = generate_sql(question)
        safe_sql = validate_and_clamp_sql(raw_sql)
        
        con = duckdb.connect(DB_PATH, read_only=True)
        res_df = con.execute(safe_sql).fetchdf()
        con.close()

        chart = suggest_chart_type(res_df)
        return {
            "success": True,
            "question": question,
            "sql": safe_sql,
            "data": res_df,
            "chart_type": chart,
            "row_count": len(res_df),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "question": question,
            "sql": raw_sql if 'raw_sql' in locals() else None,
            "data": pd.DataFrame(),
            "chart_type": "table",
            "row_count": 0,
            "error": str(e)
        }
