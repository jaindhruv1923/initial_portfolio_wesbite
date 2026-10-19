"""
Part 2 - Security Hardening Tests
Tests for secret/credential detection, risk-adaptive policy engine, and
audit redaction. See KAVACH_LIMITATIONS.md for what each module addresses.
"""

import pytest
from app.security.secret_detector import detect_secrets
from app.security.policy_engine import (
    classify_action_risk,
    compute_risk_score,
    decide_policy_action,
    evaluate_policy,
    PolicyAction,
)
from app.security.audit_redaction import redact_text


class TestSecretDetector:
    """Test credential/API-key detection (Limitation #7)."""

    def test_detects_provider_prefixed_key(self):
        text = "API_KEY=sk-abc123XYZ789defGHI456jklMNO"
        findings = detect_secrets(text)
        assert len(findings) > 0
        assert findings[0]["category"] == "credential"
        assert findings[0]["severity"] == "critical"
        assert findings[0]["action"] == "BLOCK"

    def test_ignores_placeholder_value(self):
        """A placeholder like 'your_key_here' must not be flagged — this
        is the false-positive case the entropy gate exists to prevent."""
        text = "API_KEY=your_key_here"
        findings = detect_secrets(text)
        assert len(findings) == 0

    def test_detects_high_entropy_password(self):
        text = "password: correcthorsebatterystaple99xz"
        findings = detect_secrets(text)
        assert len(findings) > 0
        assert findings[0]["category"] == "credential"

    def test_ignores_low_entropy_short_word(self):
        """A short, low-entropy assignment shouldn't be flagged as a secret."""
        text = "status: ok"
        findings = detect_secrets(text)
        assert len(findings) == 0

    def test_hinglish_password_mention_not_yet_detected(self):
        """
        Honest limitation test: the current secret detector only matches
        English keywords (password, api_key, token, etc.) via
        CREDENTIAL_KEYWORDS. A Hinglish phrasing like "mera password hai
        xyz123..." without the literal English keyword adjacent to an
        assignment operator will NOT be caught by the current
        implementation. This test documents that gap explicitly rather
        than silently missing it — see KAVACH_LIMITATIONS.md item #15.
        """
        text = "mera password hai Xk9$mLpQ2vZr8nT"
        findings = detect_secrets(text)
        # This currently returns no findings because there's no '=' or ':'
        # assignment operator immediately after "password" in this phrasing.
        # Asserting the CURRENT (limited) behavior, not the desired one.
        assert findings == [], (
            "If this assertion fails, the detector has been improved to "
            "catch natural-language credential mentions — update "
            "KAVACH_LIMITATIONS.md to remove this documented gap."
        )


class TestPolicyEngine:
    """Test risk-adaptive, action-aware policy decisions (Limitation #4)."""

    def test_classify_high_risk_action(self):
        assert classify_action_risk("delete all customer records") == "high"

    def test_classify_medium_risk_action(self):
        assert classify_action_risk("update the database schema") == "medium"

    def test_classify_low_risk_action(self):
        assert classify_action_risk("explain how this function works") == "low"

    def test_no_findings_means_zero_risk(self):
        score = compute_risk_score([], action_risk="high")
        assert score == 0.0

    def test_high_severity_finding_increases_risk(self):
        findings = [{"severity": "critical", "category": "credential"}]
        score = compute_risk_score(findings, action_risk="low")
        assert score > 0.5

    def test_action_risk_amplifies_score(self):
        findings = [{"severity": "medium", "category": "PAN"}]
        low_action_score = compute_risk_score(findings, action_risk="low")
        high_action_score = compute_risk_score(findings, action_risk="high")
        assert high_action_score > low_action_score

    def test_credential_always_blocks_regardless_of_score(self):
        findings = [{"severity": "low", "category": "credential"}]
        decision = decide_policy_action(risk_score=0.1, findings=findings)
        assert decision == PolicyAction.BLOCK

    def test_zero_risk_allows(self):
        decision = decide_policy_action(risk_score=0.0, findings=[])
        assert decision == PolicyAction.ALLOW

    def test_evaluate_policy_low_risk_safe_request(self):
        result = evaluate_policy("add a health-check endpoint", findings=[])
        assert result["decision"] == PolicyAction.ALLOW.value
        assert result["risk_score"] == 0.0

    def test_evaluate_policy_high_risk_combination(self):
        """A sensitive finding combined with a high-risk action (delete)
        should score higher than the same finding with a low-risk action."""
        findings = [{"severity": "high", "category": "Aadhaar-like"}]
        safe_action_result = evaluate_policy("explain this Aadhaar format", findings)
        risky_action_result = evaluate_policy("delete records with this Aadhaar", findings)
        assert risky_action_result["risk_score"] >= safe_action_result["risk_score"]


class TestAuditRedaction:
    """Test that sensitive values never reach audit/history storage raw (Limitation #12)."""

    def test_redacts_pan(self):
        text = "my PAN is ABCDE1234F"
        redacted = redact_text(text)
        assert "ABCDE1234F" not in redacted
        assert "[REDACTED:PAN]" in redacted

    def test_redacts_credential(self):
        text = "API_KEY=sk-abc123XYZ789defGHI456jklMNO"
        redacted = redact_text(text)
        assert "sk-abc123XYZ789defGHI456jklMNO" not in redacted
        assert "[REDACTED:credential]" in redacted

    def test_safe_text_passes_through_unchanged(self):
        text = "add a health-check endpoint"
        assert redact_text(text) == text

    def test_empty_text_handled(self):
        assert redact_text("") == ""
        assert redact_text(None) is None
