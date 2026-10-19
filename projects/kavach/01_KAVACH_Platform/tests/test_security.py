"""
Phase 4 - Security Engine Tests
Tests for PII detection, universal sensitive number detection, and security evaluation.
"""

import pytest
from app.security.detector import detect_pii
from app.security.evaluator import evaluate as evaluate_security


class TestPIIDetection:
    """Test PII detection for various entity types."""

    def test_pan_detection(self):
        """Test PAN number detection."""
        text = "My PAN is ABCDE1234F"
        findings = detect_pii(text)
        
        assert len(findings) > 0
        pan_findings = [f for f in findings if f["category"] == "PAN"]
        assert len(pan_findings) > 0
        assert pan_findings[0]["value"] == "ABCDE1234F"
        assert pan_findings[0]["action"] == "BLOCK"
        assert pan_findings[0]["severity"] == "high"
        assert pan_findings[0]["confidence"] > 0.7

    def test_phone_number_detection(self):
        """Test phone number detection."""
        text = "Call me at 9876543210"
        findings = detect_pii(text)
        
        phone_findings = [f for f in findings if f["category"] == "phone_number"]
        assert len(phone_findings) > 0
        assert phone_findings[0]["value"] == "9876543210"
        assert phone_findings[0]["action"] == "REDACT"
        assert phone_findings[0]["severity"] == "medium"

    def test_phone_with_country_code(self):
        """Test phone number with +91 prefix."""
        text = "Contact +91-9876543210 for support"
        findings = detect_pii(text)
        
        phone_findings = [f for f in findings if f["category"] == "phone_number"]
        assert len(phone_findings) > 0

    def test_email_detection(self):
        """Test email address detection."""
        text = "Email me at user@example.com"
        findings = detect_pii(text)
        
        email_findings = [f for f in findings if f["category"] == "email"]
        assert len(email_findings) > 0
        assert email_findings[0]["value"] == "user@example.com"
        assert email_findings[0]["action"] == "REDACT"
        assert email_findings[0]["severity"] == "medium"

    def test_aadhaar_with_context(self):
        """Test Aadhaar detection with context words."""
        text = "My Aadhaar is 1234 5678 9012"
        findings = detect_pii(text)
        
        aadhaar_findings = [f for f in findings if f["category"] == "Aadhaar-like"]
        assert len(aadhaar_findings) > 0
        assert aadhaar_findings[0]["action"] == "BLOCK"
        assert aadhaar_findings[0]["severity"] == "high"

    def test_bare_aadhaar_detection(self):
        """Test that a bare 12-digit number is detected as Aadhaar-like or sensitive number."""
        text = "123456789012"
        findings = detect_pii(text)
        assert len(findings) > 0
        assert any(f["category"] in ("Aadhaar-like", "sensitive_number") for f in findings)

    def test_bare_sensitive_number_detection(self):
        """Test bare sensitive number detection."""
        text = "12454323454"
        findings = detect_pii(text)
        assert len(findings) > 0
        assert any(f["category"] in ("sensitive_number", "Aadhaar-like") for f in findings)

    def test_aadhaar_with_arbitrary_number(self):
        """Test that entering 'my aadhar card number is 12454323454' flags it with Aadhaar context."""
        text = "my aadhar card number is 12454323454"
        findings = detect_pii(text)
        
        assert len(findings) > 0
        assert any(f["category"] in ("Aadhaar-like", "sensitive_number") for f in findings)
        assert findings[0]["severity"] == "high"
        assert findings[0]["action"] == "BLOCK"

    def test_bank_account_with_context(self):
        """Test bank account detection with context."""
        text = "My bank account number is 112233445566"
        findings = detect_pii(text)
        
        bank_findings = [f for f in findings if f["category"] == "bank_account"]
        assert len(bank_findings) > 0
        assert bank_findings[0]["action"] == "BLOCK"

    def test_empty_text(self):
        """Test detection on empty text."""
        findings = detect_pii("")
        assert len(findings) == 0

    def test_safe_text(self):
        """Test that safe text produces no findings."""
        text = "The meeting is tomorrow at 2 PM in the conference room"
        findings = detect_pii(text)
        assert len(findings) == 0

    def test_safe_devops_prompts_not_flagged(self):
        """Test that normal developer prompts with ports, versions, or timeouts are NOT flagged."""
        safe_prompts = [
            "Add a health check endpoint to backend on port 8080 returning JSON status",
            "Set connection pool timeout to 30 seconds and retries to 3",
            "Upgrade backend to Python 3.12 and FastAPI version 0.110",
            "Return HTTP status code 200 on success and 404 on not found",
        ]
        for prompt in safe_prompts:
            findings = detect_pii(prompt)
            assert len(findings) == 0, f"Safe prompt was falsely flagged: {prompt} -> {findings}"

    def test_multiple_findings(self):
        """Test detection of multiple PII entities."""
        text = "Contact ABCDE1234F or call 9876543210 or email test@example.com"
        findings = detect_pii(text)
        
        assert len(findings) >= 3, "Should find multiple entities"
        categories = {f["category"] for f in findings}
        assert "PAN" in categories
        assert "phone_number" in categories
        assert "email" in categories

    def test_confidence_scores(self):
        """Test that findings have reasonable confidence scores."""
        text = "My PAN is ABCDE1234F and phone is 9876543210"
        findings = detect_pii(text)
        
        for finding in findings:
            assert 0 <= finding["confidence"] <= 1, "Confidence should be 0-1"
            assert isinstance(finding["confidence"], float)

    def test_finding_has_explanation(self):
        """Test that all findings have explanations."""
        text = "My email is test@example.com"
        findings = detect_pii(text)
        
        for finding in findings:
            assert "reason" in finding
            assert len(finding["reason"]) > 0
            assert isinstance(finding["reason"], str)


class TestGovernmentIdContextCoverage:
    """
    Regression matrix: Sensitive numbers (12-digit, 11-digit, ID phrasing)
    must be flagged when context identifies them, while arbitrary numbers remain unflagged.
    """

    @pytest.mark.parametrize("text,should_flag", [
        ("123456789012", True),
        ("12454323454", True),
        ("My order number is 123456789012.", True),
        ("Transaction reference: 123456789012.", True),
        ("My Aadhaar number is 123456789012.", True),
        ("Government ID: 123456789012", True),
        ("National identification number: 123456789012", True),
        ("Identity document number: 123456789012", True),
        ("my aadhar card number is 12454323454", True),
        ("Add a health check endpoint on port 8080", False),
        ("Timeout is set to 60 seconds", False),
    ])
    def test_government_id_regression_matrix(self, text, should_flag):
        findings = detect_pii(text)
        flagged = len(findings) > 0
        assert flagged == should_flag, (
            f"Expected flagged={should_flag} for {text!r}, got {flagged}. "
            f"Findings: {findings}"
        )


class TestSecurityEvaluation:
    """Test security engine evaluation metrics."""

    def test_evaluate_returns_correct_structure(self):
        """Test that evaluate returns expected structure."""
        result = evaluate_security()
        
        assert "overall" in result
        assert "per_category" in result
        assert "total_cases" in result
        
        assert "precision" in result["overall"]
        assert "recall" in result["overall"]
        assert "f1" in result["overall"]

    def test_evaluate_metrics_in_range(self):
        """Test that all metrics are in valid range [0, 1]."""
        result = evaluate_security()
        
        for metric in ["precision", "recall", "f1"]:
            assert 0 <= result["overall"][metric] <= 1, f"{metric} should be in [0, 1]"
            
            for cat_metrics in result["per_category"].values():
                assert 0 <= cat_metrics[metric] <= 1

    def test_evaluate_coverage_all_categories(self):
        """Test that evaluation covers key entity categories."""
        result = evaluate_security()
        
        found_categories = set(result["per_category"].keys())
        expected_subset = {"PAN", "Aadhaar-like", "phone_number", "bank_account", "email"}
        assert expected_subset.issubset(found_categories), f"Missing categories: {expected_subset - found_categories}"

    def test_evaluate_tp_fp_fn_tn(self):
        """Test that confusion matrix components exist."""
        result = evaluate_security()
        
        assert "true_positives" in result["overall"]
        assert "false_positives" in result["overall"]
        assert "false_negatives" in result["overall"]
        assert "true_negatives" in result["overall"]

    def test_evaluate_total_matches_counts(self):
        """Test that total cases matches the sum of counts."""
        result = evaluate_security()
        
        total = result["total_cases"]
        tp = result["overall"]["true_positives"]
        fp = result["overall"]["false_positives"]
        fn = result["overall"]["false_negatives"]
        tn = result["overall"]["true_negatives"]
        
        assert total == tp + fp + fn + tn, "Total should equal sum of confusion matrix"
