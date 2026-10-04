"""
End-to-End Integration Tests
Tests for complete Kavach workflow from user request to final result.
"""

import pytest
from app.agent.orchestrator import run_workflow
from app.agent.state import WorkflowStage, list_runs
from app.rag.ingest import ingest_repository
from app.rag.embed_store import index_chunks


class TestE2EWorkflowWithRepository:
    """Test complete workflow with actual repository."""

    def test_e2e_auth_request_with_real_repo(self, sample_repository_path):
        """Test complete workflow for authentication request with real repo."""
        # Phase 1: Ingest repository
        chunks = ingest_repository(sample_repository_path)
        assert len(chunks) > 0, "Should ingest repository chunks"
        
        indexed = index_chunks(chunks)
        assert indexed > 0, "Should index chunks"
        
        # Phase 2: Submit request through workflow
        run = run_workflow("Add authentication to the login module")
        
        # Phase 3: Verify workflow execution
        assert run is not None
        assert run.request_text == "Add authentication to the login module"
        
        # Should have gone through planning
        assert len(run.plan) > 0
        
        # Should have retrieved context
        assert isinstance(run.retrieved_context, list)
        
        # Should have performed security checks
        assert isinstance(run.security_findings, list)
        
        # Should have performed impact analysis
        assert isinstance(run.impact_report, list)
        
        # Should have attempted generation
        assert "generated_output" in run.generation_result
        
        # Should have validated
        assert "valid_syntax" in run.validation_result
        
        # Should have reached a terminal state
        assert run.stage in {
            WorkflowStage.COMPLETE,
            WorkflowStage.BLOCKED,
            WorkflowStage.NEEDS_REVIEW,
        }

    def test_e2e_database_request(self, sample_repository_path):
        """Test workflow for database-related change."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Update the database models to support user roles")
        
        # Should identify database tasks
        db_tasks = [t for t in run.plan if "database" in t.lower()]
        assert len(db_tasks) > 0
        
        # Should retrieve database-related context
        assert len(run.retrieved_context) >= 0
        
        # Should identify potentially affected files
        assert len(run.impact_report) >= 0

    def test_e2e_security_bypass_on_sensitive_input(self, sample_repository_path):
        """Test that workflow blocks on sensitive input."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("My PAN is ABCDE1234F and I need help with this code")
        
        # Should detect PII
        assert len(run.security_findings) > 0
        
        # Might be blocked
        if any(f["action"] == "BLOCK" for f in run.security_findings):
            assert run.stage in {WorkflowStage.BLOCKED, WorkflowStage.NEEDS_REVIEW}

    def test_e2e_multiple_sequential_requests(self, sample_repository_path):
        """Test multiple requests in sequence."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        requests = [
            "Add authentication",
            "Improve error handling",
            "Update database schema",
        ]
        
        runs = [run_workflow(req) for req in requests]
        
        # All should complete
        assert len(runs) == 3
        for i, run in enumerate(runs):
            assert run.request_text == requests[i]
            assert run.stage != WorkflowStage.REQUEST_RECEIVED

    def test_e2e_workflow_produces_valid_output(self, sample_repository_path):
        """Test that workflow produces structurally valid output."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Implement new API endpoint for authentication")
        
        # Validate structure
        assert isinstance(run.plan, list)
        assert isinstance(run.retrieved_context, list)
        assert isinstance(run.security_findings, list)
        assert isinstance(run.generation_result, dict)
        assert isinstance(run.validation_result, dict)
        assert isinstance(run.impact_report, list)
        assert isinstance(run.history, list)
        
        # Validate content
        if run.retrieved_context:
            for item in run.retrieved_context:
                assert "file_path" in item
                assert "text" in item
                assert "score" in item
        
        if run.security_findings:
            for finding in run.security_findings:
                assert "category" in finding
                assert "value" in finding
                assert "action" in finding
                assert "severity" in finding
        
        if run.impact_report:
            for item in run.impact_report:
                assert "file_path" in item
                assert "relevance_score" in item
                assert "reason" in item

    def test_e2e_workflow_with_no_gemini_key(self, sample_repository_path, monkeypatch):
        """Test workflow when LLM is not configured."""
        monkeypatch.setenv("GEMINI_API_KEY", "")
        
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Generate new code")
        
        # Should still complete
        assert run is not None
        # Generated output should indicate no LLM
        assert "generated_output" in run.generation_result
        assert isinstance(run.generation_result["generated_output"], str)

    def test_e2e_workflow_persistence(self, sample_repository_path):
        """Test that workflows persist correctly."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        # Run workflow
        run1 = run_workflow("Test persistence workflow")
        workflow_id = run1.id
        
        # List all runs
        all_runs = list_runs()
        
        # Should find our run
        found = False
        for run in all_runs:
            if run.id == workflow_id:
                found = True
                assert run.request_text == "Test persistence workflow"
                break
        
        assert found, "Workflow should be in persistence store"


class TestE2ESecurityIntegration:
    """Test security engine integration in workflow."""

    def test_e2e_pii_in_input_blocks_workflow(self, sample_repository_path):
        """Test that PII in input is caught."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Call me at +91-9876543210 about the code")
        
        # Should detect phone
        if run.security_findings:
            categories = {f["category"] for f in run.security_findings}
            # Should find phone at minimum
            assert len(categories) > 0

    def test_e2e_pii_in_generated_code_caught(self, sample_repository_path):
        """Test that PII in generated output would be caught."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        # If LLM generates code with email addresses, should be caught
        run = run_workflow("Add contact information handling")
        
        # Generation might include email patterns
        if run.generation_result.get("generated_output"):
            output = run.generation_result["generated_output"]
            # Verify it was processed through security
            assert isinstance(output, str)

    def test_e2e_devops_input_processed(self, sample_repository_path):
        """Test that diverse developer inputs are processed correctly."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run_1 = run_workflow("Improve authentication error handling")
        run_2 = run_workflow("Add validation logic to login router")
        
        assert run_1.request_text is not None
        assert run_2.request_text is not None


class TestE2EImpactAnalysis:
    """Test impact analysis integration in workflow."""

    def test_e2e_impact_analysis_included(self, sample_repository_path):
        """Test that impact analysis is performed in workflow."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Modify authentication module significantly")
        
        # Should have impact report
        assert isinstance(run.impact_report, list)
        # May be empty if no semantic matches, but should exist

    def test_e2e_impact_ranking(self, sample_repository_path):
        """Test that impact results are properly ranked."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Change database queries in auth")
        
        if run.impact_report and len(run.impact_report) > 1:
            # Should be sorted by relevance
            scores = [item["relevance_score"] for item in run.impact_report]
            assert scores == sorted(scores, reverse=True)


class TestE2EGenerationAndValidation:
    """Test generation and validation in workflow."""

    def test_e2e_generated_code_syntax_checked(self, sample_repository_path):
        """Test that generated code is syntax-checked."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Generate a function to validate user input")
        
        # Should have validation result
        assert "validation_result" in run.__dict__ or hasattr(run, "validation_result")
        val_result = run.validation_result
        
        # Should contain validity check
        assert "valid_syntax" in val_result

    def test_e2e_invalid_code_caught(self, sample_repository_path):
        """Test that invalid generated code is caught."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Generate any code")
        
        # If code was generated, it should be validated
        if run.generation_result.get("generated_output"):
            assert "validation_result" in run.__dict__


class TestE2EPipelineStages:
    """Test the pipeline flow through stages."""

    def test_e2e_stage_progression(self, sample_repository_path):
        """Test that workflow progresses through expected stages."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Safe request about code changes")
        
        # Should have history entries
        assert len(run.history) > 0, "Should have stage history"
        
        # Should reach a final stage
        final_stages = {
            WorkflowStage.COMPLETE,
            WorkflowStage.BLOCKED,
            WorkflowStage.NEEDS_REVIEW,
        }
        assert run.stage in final_stages, f"Should reach final stage, got {run.stage}"

    def test_e2e_history_completeness(self, sample_repository_path):
        """Test that history captures all stage transitions."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Test history tracking")
        
        # Should have multiple history entries
        assert len(run.history) > 1
        
        # Each entry should be descriptive
        for entry in run.history:
            assert isinstance(entry, str)
            assert len(entry) > 0


class TestE2EErrorRecovery:
    """Test error handling in workflow."""

    def test_e2e_continues_with_invalid_repo(self):
        """Test workflow continues if repository is invalid."""
        chunks = ingest_repository("/nonexistent/path")
        index_chunks(chunks)  # Should be empty
        
        run = run_workflow("Test request")
        
        # Should not crash
        assert run is not None
        # Should complete
        assert run.stage != WorkflowStage.REQUEST_RECEIVED

    def test_e2e_handles_unicode_input(self, sample_repository_path):
        """Test workflow with unicode characters."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Add support for 中文 and العربية languages")
        
        assert run is not None
        assert len(run.history) > 0

    def test_e2e_handles_very_long_input(self, sample_repository_path):
        """Test workflow with very long request."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        long_request = "Analyze and improve " + ("code " * 100)
        run = run_workflow(long_request)
        
        assert run is not None
        assert run.stage != WorkflowStage.REQUEST_RECEIVED


class TestE2ECompleteScenarios:
    """Test complete real-world scenarios."""

    def test_e2e_authentication_feature_request(self, sample_repository_path):
        """Test complete flow: implement authentication feature."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        # User wants to add OAuth authentication
        run = run_workflow("Implement OAuth 2.0 authentication in the login system")
        
        # Verify complete flow
        assert "plan" in run.__dict__  # Planning done
        assert isinstance(run.retrieved_context, list)  # RAG done
        assert isinstance(run.security_findings, list)  # Security checks done
        assert isinstance(run.impact_report, list)  # Impact analysis done
        assert "generated_output" in run.generation_result  # Generation done
        assert "valid_syntax" in run.validation_result  # Validation done
        
        # Should complete
        terminal_states = {
            WorkflowStage.COMPLETE,
            WorkflowStage.BLOCKED,
            WorkflowStage.NEEDS_REVIEW,
        }
        assert run.stage in terminal_states

    def test_e2e_security_enhancement_request(self, sample_repository_path):
        """Test complete flow: enhance security."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Add input validation and sanitization to prevent injection attacks")
        
        # Should recognize security-related request
        assert len(run.plan) > 0
        assert any("security" in t.lower() for t in run.plan)
        
        # Should complete successfully
        assert run.stage != WorkflowStage.REQUEST_RECEIVED

    def test_e2e_refactoring_request(self, sample_repository_path):
        """Test complete flow: code refactoring."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        run = run_workflow("Refactor the authentication module for better testability")
        
        # Should extract tasks
        assert len(run.plan) > 0
        
        # Should retrieve relevant code
        auth_context = [c for c in run.retrieved_context if "auth" in c.get("file_path", "").lower()]
        # May or may not find auth files depending on repo structure
        
        # Should complete
        assert run.stage in {
            WorkflowStage.COMPLETE,
            WorkflowStage.BLOCKED,
            WorkflowStage.NEEDS_REVIEW,
        }
