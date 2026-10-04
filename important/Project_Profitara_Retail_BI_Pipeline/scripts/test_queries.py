import duckdb
import re

con = duckdb.connect("data/profitara.duckdb", read_only=True)
with open("sql/analytic_queries.sql", "r", encoding="utf-8") as f:
    sql_text = f.read()

# Remove multi-line comments and single line comments to get pure queries
cleaned_blocks = [b.strip() for b in sql_text.split(";") if b.strip()]

print(f"Total query blocks found: {len(cleaned_blocks)}")
for i, block in enumerate(cleaned_blocks, 1):
    # Strip leading comments
    query = re.sub(r'--[^\n]*\n', '\n', block).strip()
    if not query:
        continue
    try:
        df = con.execute(query).fetchdf()
        print(f"Query {i} executed successfully! Rows returned: {len(df):,}")
    except Exception as e:
        print(f"Query {i} failed: {e}")

con.close()
