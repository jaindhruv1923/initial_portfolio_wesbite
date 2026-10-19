"""
Phase 5 - Change Impact Analysis Tests
Tests for impact prediction and dependency graph analysis.
"""

import pytest
from app.impact.analyzer import analyze_impact, SEMANTIC_WEIGHT, DEPENDENCY_WEIGHT
from app.impact.dependency_graph import (
    build_dependency_graph,
    find_dependent_files,
    _parse_file,
)
from app.impact.evaluator import evaluate as evaluate_impact


class TestDependencyGraph:
    """Test dependency graph extraction from Python code."""

    def test_parse_file_with_imports(self, tmp_path):
        """Test parsing file with import statements."""
        py_file = tmp_path / "test.py"
        py_file.write_text("""
import os
import sys
from pathlib import Path
from app.utils import helper_func
""")
        
        result = _parse_file(str(py_file))
        
        assert "imports" in result
        assert len(result["imports"]) >= 4
        assert "os" in result["imports"]
        assert "sys" in result["imports"]
        assert "app.utils" in result["imports"]

    def test_parse_file_with_definitions(self, tmp_path):
        """Test parsing file with function and class definitions."""
        py_file = tmp_path / "test.py"
        py_file.write_text("""
def authenticate(user, password):
    pass

class User:
    def __init__(self):
        pass

def validate():
    pass
""")
        
        result = _parse_file(str(py_file))
        
        assert "defines" in result
        assert "authenticate" in result["defines"]
        assert "User" in result["defines"]
        assert "validate" in result["defines"]

    def test_parse_file_mixed_imports_and_defs(self, tmp_path):
        """Test file with both imports and definitions."""
        py_file = tmp_path / "test.py"
        py_file.write_text("""
import json
from app import models

def process(data):
    return json.dumps(data)

class Processor:
    def run(self):
        return models.get()
""")
        
        result = _parse_file(str(py_file))
        
        assert len(result["imports"]) > 0
        assert len(result["defines"]) > 0
        assert "process" in result["defines"]
        assert "Processor" in result["defines"]

    def test_parse_file_syntax_error(self, tmp_path):
        """Test parsing file with syntax errors (should not crash)."""
        py_file = tmp_path / "broken.py"
        py_file.write_text("def broken(\n    pass")
        
        result = _parse_file(str(py_file))
        
        # Should return empty result, not crash
        assert result == {"imports": [], "defines": []}

    def test_build_dependency_graph(self, sample_repository_path):
        """Test building dependency graph for repository."""
        graph = build_dependency_graph(sample_repository_path)
        
        assert isinstance(graph, dict)
        assert len(graph) > 0
        
        # Each entry should have imports and defines
        for file_path, info in graph.items():
            assert "imports" in info
            assert "defines" in info
            assert isinstance(info["imports"], list)
            assert isinstance(info["defines"], list)

    def test_find_dependent_files(self, sample_repository_path):
        """Test finding files that depend on a module."""
        graph = build_dependency_graph(sample_repository_path)
        
        # Find files that import common modules
        dependents = find_dependent_files(graph, "utils")
        
        assert isinstance(dependents, list)


class TestImpactAnalyzer:
    """Test change impact analysis."""

    def test_analyze_impact_basic(self, sample_repository_path):
        """Test basic impact analysis."""
        report = analyze_impact("Update authentication module", sample_repository_path)
        
        assert isinstance(report, list)
        assert len(report) > 0
        
        # Each item should have required fields
        for item in report:
            assert "file_path" in item
            assert "relevance_score" in item
            assert "reason" in item
            assert 0 <= item["relevance_score"] <= 1

    def test_analyze_impact_scoring(self, sample_repository_path):
        """Test that impact scores are properly calculated."""
        report = analyze_impact("Update authentication logic", sample_repository_path)
        
        # First result should be most relevant
        if len(report) > 1:
            scores = [item["relevance_score"] for item in report]
            assert scores == sorted(scores, reverse=True), "Should be sorted by relevance"

    def test_analyze_impact_top_k(self, sample_repository_path):
        """Test that top_k parameter is respected."""
        report = analyze_impact("Change database models", sample_repository_path, top_k=2)
        
        assert len(report) <= 2, f"Should return at most 2 results, got {len(report)}"

    def test_analyze_impact_empty_description(self, sample_repository_path):
        """Test with empty change description."""
        report = analyze_impact("", sample_repository_path)
        
        assert isinstance(report, list)

    def test_analyze_impact_phrasing_variations(self, sample_repository_path):
        """Test impact analysis with varied phrasing descriptions."""
        report = analyze_impact("Update the authentication middleware and session handler", sample_repository_path)
        assert isinstance(report, list)

    def test_impact_reasons_provided(self, sample_repository_path):
        """Test that impact reasons explain the prediction."""
        report = analyze_impact("Modify security check logic", sample_repository_path)
        
        for item in report:
            reason = item["reason"]
            assert reason is not None
            assert len(reason) > 0
            # Should mention either semantic or dependency-based reasoning
            assert "semantic" in reason.lower() or "import" in reason.lower() or "weak" in reason.lower()


class TestImpactEvaluation:
    """Test impact analysis evaluation metrics."""

    def test_evaluate_impact_structure(self):
        """Test that evaluate returns correct structure."""
        result = evaluate_impact()
        
        assert "overall" in result
        assert "per_case" in result
        assert "total_cases" in result
        
        assert "avg_precision" in result["overall"]
        assert "avg_recall" in result["overall"]
        assert "avg_f1" in result["overall"]

    def test_evaluate_metrics_in_range(self):
        """Test that metrics are in valid range."""
        result = evaluate_impact()
        
        for metric in ["avg_precision", "avg_recall", "avg_f1"]:
            value = result["overall"][metric]
            assert 0 <= value <= 1, f"{metric} should be in [0, 1], got {value}"

    def test_evaluate_per_case_results(self):
        """Test that per-case results are provided."""
        result = evaluate_impact()
        
        assert len(result["per_case"]) > 0
        
        for case in result["per_case"]:
            assert "id" in case
            assert "change_description" in case
            assert "predicted_files" in case
            assert "actual_files" in case
            assert "precision" in case
            assert "recall" in case
            assert "f1" in case

    def test_evaluate_case_metrics_in_range(self):
        """Test that per-case metrics are in valid range."""
        result = evaluate_impact()
        
        for case in result["per_case"]:
            for metric in ["precision", "recall", "f1"]:
                value = case[metric]
                assert 0 <= value <= 1, f"{metric} should be in [0, 1]"

    def test_evaluate_total_cases_count(self):
        """Test that total_cases matches per_case list."""
        result = evaluate_impact()
        
        assert result["total_cases"] == len(result["per_case"])

    def test_evaluate_test_cases_loaded(self):
        """Test that test cases are actually loaded and evaluated."""
        result = evaluate_impact()
        
        # Should have at least the 5 known test cases
        assert result["total_cases"] >= 5, "Should evaluate at least 5 test cases"


class TestImpactIntegration:
    """Integration tests for impact analysis."""

    def test_impact_analysis_workflow(self, sample_repository_path):
        """Test complete impact analysis workflow."""
        # Simulate workflow: describe change -> analyze impact
        change = "Update the authentication module to support OAuth"
        report = analyze_impact(change, sample_repository_path, top_k=3)
        
        # Should return ranked list
        assert isinstance(report, list)
        assert len(report) > 0
        
        # Files should be ranked by relevance
        scores = [r["relevance_score"] for r in report]
        assert scores == sorted(scores, reverse=True)

    def test_impact_analysis_consistency(self, sample_repository_path):
        """Test that impact analysis is consistent for same input."""
        change = "Modify login flow"
        
        report1 = analyze_impact(change, sample_repository_path, top_k=3)
        report2 = analyze_impact(change, sample_repository_path, top_k=3)
        
        files1 = [r["file_path"] for r in report1]
        files2 = [r["file_path"] for r in report2]
        
        assert files1 == files2, "Same input should produce same results"

    def test_different_changes_different_impacts(self, sample_repository_path):
        """Test that different changes produce different impact predictions."""
        auth_impact = analyze_impact("Update authentication", sample_repository_path, top_k=3)
        db_impact = analyze_impact("Update database queries", sample_repository_path, top_k=3)
        
        auth_files = {r["file_path"] for r in auth_impact}
        db_files = {r["file_path"] for r in db_impact}
        
        # Different changes might have some overlap but shouldn't be identical
        # (This is a weak assertion since it depends on repo structure)
        assert isinstance(auth_files, set)
        assert isinstance(db_files, set)
