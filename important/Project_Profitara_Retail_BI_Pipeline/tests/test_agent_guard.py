import os
import sys
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from agent.analyst_agent import validate_and_clamp_sql, SecurityException

def test_safe_select_query_allowed():
    """Verify that standard SELECT queries pass validation."""
    query = "SELECT category, SUM(sales) FROM india_orders GROUP BY category"
    clamped = validate_and_clamp_sql(query)
    assert clamped.startswith("SELECT")
    assert "LIMIT 100" in clamped

def test_safe_with_query_allowed():
    """Verify that CTE (WITH) queries pass validation."""
    query = "WITH high_orders AS (SELECT * FROM india_orders WHERE sales > 1000) SELECT COUNT(*) FROM high_orders"
    clamped = validate_and_clamp_sql(query)
    assert clamped.startswith("WITH")
    assert "LIMIT 100" in clamped

def test_destructive_keywords_rejected():
    """Verify that destructive SQL keywords raise SecurityException."""
    destructive_queries = [
        "DROP TABLE india_orders",
        "DELETE FROM india_orders WHERE sales < 10",
        "UPDATE india_orders SET profit = 0",
        "INSERT INTO india_orders VALUES (1, 'BLK-1', '2025-01-01', ...)",
        "ALTER TABLE india_orders ADD COLUMN fake_col INT",
        "TRUNCATE TABLE india_orders",
        "PRAGMA database_list"
    ]
    for q in destructive_queries:
        with pytest.raises(SecurityException):
            validate_and_clamp_sql(q)

def test_limit_clamping():
    """Verify that excessively large row limits are clamped to 100."""
    query_with_large_limit = "SELECT * FROM india_orders LIMIT 5000"
    clamped = validate_and_clamp_sql(query_with_large_limit)
    assert "LIMIT 100" in clamped
    assert "LIMIT 5000" not in clamped

    query_with_small_limit = "SELECT * FROM india_orders LIMIT 10"
    clamped_small = validate_and_clamp_sql(query_with_small_limit)
    assert "LIMIT 10" in clamped_small
