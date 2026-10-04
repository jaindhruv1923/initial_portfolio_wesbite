"""
Pytest configuration and shared fixtures for Kavach test suite.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

# Add the backend app to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))


@pytest.fixture
def client():
    """FastAPI TestClient for testing endpoints."""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def mock_gemini_llm():
    """Mock LLM response for testing generation without API calls."""
    def mock_call(prompt: str) -> str:
        return """```python
def authenticate_user(username: str, password: str) -> bool:
    # Mock authentication implementation
    # In real code, this would use proper credential validation
    return username and password and len(password) >= 8
```"""
    return mock_call


@pytest.fixture
def sample_chunk():
    """Sample repository chunk for testing."""
    from app.rag.ingest import Chunk
    return Chunk(
        file_path="auth/login.py",
        chunk_index=0,
        text="""def authenticate_user(username: str, password: str) -> bool:
    # Validate credentials against database
    if not username or not password:
        return False
    return db.verify_credentials(username, password)""",
    )


@pytest.fixture
def sample_repository_path(tmp_path):
    """Create a temporary repository with sample Python files."""
    repo_root = tmp_path / "test_repo"
    repo_root.mkdir()
    
    # Create auth module
    auth_dir = repo_root / "auth"
    auth_dir.mkdir()
    (auth_dir / "login.py").write_text("""
def login_user(username: str, password: str):
    if not username or not password:
        raise ValueError("Missing credentials")
    return {"status": "logged_in", "username": username}
""")
    
    # Create database module
    db_dir = repo_root / "database"
    db_dir.mkdir()
    (db_dir / "models.py").write_text("""
from sqlalchemy import Column, String

class User:
    id = Column(String, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
""")
    
    # Create utils
    (repo_root / "utils.py").write_text("""
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
""")
    
    return str(repo_root)


@pytest.fixture
def sample_security_text():
    """Sample security test text with various sensitivities."""
    return {
        "pan": "My PAN card is ABCDE1234F",
        "phone": "Call me at +91-9876543210",
        "safe": "The meeting is tomorrow at 2 PM",
        "email": "user@example.com",
        "aadhaar": "My Aadhaar is 1234 5678 9012",
        "bare_number": "12454323454",
    }


@pytest.fixture
def workflow_run_with_results():
    """Sample workflow run with complete results."""
    from app.agent.state import WorkflowRun, WorkflowStage
    
    run = WorkflowRun(request_text="Add authentication to the login module")
    run.stage = WorkflowStage.COMPLETE
    run.plan = [
        "Identify authentication-related files",
        "Review existing auth logic",
        "Retrieve relevant repository context",
        "Run security checks",
    ]
    run.retrieved_context = [
        {
            "score": 0.92,
            "file_path": "auth/login.py",
            "chunk_index": 0,
            "text": "def login_user(username, password): pass",
        }
    ]
    run.security_findings = []
    run.impact_report = [
        {
            "file_path": "auth/login.py",
            "relevance_score": 0.95,
            "reason": "semantically related to the change description",
        },
        {
            "file_path": "database/models.py",
            "relevance_score": 0.75,
            "reason": "imports/references the most-related file",
        },
    ]
    run.generation_result = {
        "llm_configured": False,
        "evidence_chunks_used": 1,
        "prompt": "Test prompt",
        "generated_output": "def authenticate(): pass",
    }
    run.validation_result = {
        "valid_syntax": True,
        "error": None,
        "extracted_code": "def authenticate(): pass",
    }
    return run


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, tmp_path):
    """Setup test environment with isolated Qdrant storage."""
    # Point Qdrant to temp directory for tests
    test_qdrant_path = str(tmp_path / "qdrant_test")
    monkeypatch.setenv("QDRANT_PATH", test_qdrant_path)
    
    # Clear in-memory workflow runs before each test
    from app.agent import state as state_module
    state_module._workflow_runs.clear()
    
    yield
    
    # Cleanup
    state_module._workflow_runs.clear()
