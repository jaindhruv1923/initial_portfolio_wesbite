"""
Tests for KAVACH Toughest 20 Stress Benchmark Engine
Ensures all 20 adversarial scenarios evaluate properly with empirical Before vs After metrics.
"""

import pytest
from app.observability.toughest_benchmark import (
    global_toughest_benchmark,
    TOUGHEST_BENCHMARK_SCENARIOS,
    ToughestBenchmarkEngine
)


def test_toughest_benchmark_scenarios_count():
    assert len(TOUGHEST_BENCHMARK_SCENARIOS) == 20
    for s in TOUGHEST_BENCHMARK_SCENARIOS:
        assert "id" in s
        assert "name" in s
        assert "category" in s
        assert "difficulty" in s
        assert "payload" in s
        assert "raw_llm_behavior" in s
        assert "raw_llm_verdict" in s
        assert "raw_cvss" in s
        assert "kavach_verdict" in s
        assert "kavach_shield" in s
        assert "kavach_remediation" in s
        assert "kavach_cvss" in s
        assert "latency_ms" in s


def test_toughest_benchmark_engine_execution():
    engine = ToughestBenchmarkEngine()
    result = engine.run_benchmark()

    assert result["title"]
    assert result["summary"]["total_scenarios_evaluated"] == 20

    # Before assertions (vulnerable baseline)
    before = result["summary"]["before"]
    assert before["security_compliance_pct"] <= 15.0
    assert before["mean_cvss_severity"] >= 8.5
    assert before["attacks_breached_count"] >= 17

    # After assertions (KAVACH governed engine)
    after = result["summary"]["after"]
    assert after["security_compliance_pct"] == 100.0
    assert after["mean_cvss_severity"] == 0.0
    assert after["attacks_prevented_count"] == 20
    assert after["attacks_breached_count"] == 0
    assert after["pii_data_leakage_pct"] == 0.0

    # Empirical lift
    lift = result["summary"]["empirical_lift"]
    assert "+9" in lift["security_compliance_lift"]
    assert "-8" in lift["cvss_risk_reduction"]


def test_global_singleton():
    res = global_toughest_benchmark.run_benchmark()
    assert len(res["scenarios"]) == 20
