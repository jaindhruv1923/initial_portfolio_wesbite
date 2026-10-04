"""
Phase 3 - Evidence-Grounded Generation Tests
Tests for code generation, validation, and LLM integration.
"""

import pytest
from unittest.mock import patch, MagicMock
from app.generation.generator import build_grounded_prompt, generate_code
from app.generation.validator import (
    extract_python_code_block,
    check_python_syntax,
    validate_generated_output,
)
from app.generation.llm_client import is_llm_configured, call_llm


class TestPromptBuilding:
    """Test grounded prompt construction."""

    def test_build_prompt_with_evidence(self):
        """Test prompt building with repository evidence."""
        request = "Add authentication to the login module"
        context = [
            {
                "file_path": "auth/login.py",
                "text": "def login_user(username, password): pass",
            }
        ]
        
        prompt = build_grounded_prompt(request, context)
        
        assert "REPOSITORY EVIDENCE" in prompt
        assert "auth/login.py" in prompt
        assert "login_user" in prompt
        assert "DEVELOPER REQUEST" in prompt
        assert request in prompt

    def test_build_prompt_without_evidence(self):
        """Test prompt building without evidence."""
        request = "Add logging to the system"
        prompt = build_grounded_prompt(request, [])
        
        assert "No repository evidence" in prompt
        assert request in prompt

    def test_build_prompt_multiple_chunks(self):
        """Test prompt with multiple evidence chunks."""
        request = "Improve performance"
        context = [
            {"file_path": "db.py", "text": "Database code"},
            {"file_path": "cache.py", "text": "Caching code"},
            {"file_path": "api.py", "text": "API endpoints"},
        ]
        
        prompt = build_grounded_prompt(request, context)
        
        assert "db.py" in prompt
        assert "cache.py" in prompt
        assert "api.py" in prompt
        assert prompt.count("---") >= 3  # At least 3 file markers

    def test_prompt_instructs_careful_generation(self):
        """Test that prompt instructs careful, evidence-based generation."""
        prompt = build_grounded_prompt("test", [])
        
        assert "careful" in prompt.lower()
        assert "evidence" in prompt.lower() or "repository" in prompt.lower()
        assert "do not invent" in prompt.lower() or "not invented" in prompt.lower()


class TestCodeExtraction:
    """Test Python code extraction from LLM responses."""

    def test_extract_fenced_code_block(self):
        """Test extraction of ```python fenced code."""
        response = '''Here's the code:
```python
def hello():
    return "Hello"
```
This is it.'''
        
        code = extract_python_code_block(response)
        
        assert code is not None
        assert 'def hello():' in code
        assert '"Hello"' in code

    def test_extract_code_without_language_tag(self):
        """Test extraction of ``` code block without python tag."""
        response = '''Here's the code:
```
def greet(name):
    return f"Hello {name}"
```
Done.'''
        
        code = extract_python_code_block(response)
        assert code is not None
        assert 'def greet' in code

    def test_extract_plain_code_fallback(self):
        """Test fallback to plain text when no fencing found."""
        response = "def simple(): pass"
        
        code = extract_python_code_block(response)
        
        assert code is not None
        assert 'def simple()' in code

    def test_extract_from_empty_text(self):
        """Test extraction from empty text."""
        code = extract_python_code_block("")
        assert code is None

    def test_extract_first_block_only(self):
        """Test that only first code block is extracted."""
        response = '''
```python
def first():
    pass
```

```python
def second():
    pass
```
'''
        
        code = extract_python_code_block(response)
        assert 'def first' in code
        # Should only get first block
        lines = code.strip().split('\n')
        assert any('first' in line for line in lines)


class TestSyntaxValidation:
    """Test Python syntax validation."""

    def test_valid_syntax(self):
        """Test validation of syntactically correct code."""
        code = """
def authenticate(user, password):
    if not user or not password:
        return False
    return verify_credentials(user, password)
"""
        
        result = check_python_syntax(code)
        
        assert result["valid_syntax"] is True
        assert result["error"] is None

    def test_invalid_syntax(self):
        """Test validation of syntactically incorrect code."""
        code = """def broken(
    return None
"""
        
        result = check_python_syntax(code)
        
        assert result["valid_syntax"] is False
        assert result["error"] is not None

    def test_missing_colon(self):
        """Test detection of missing colon."""
        code = "def func(x)\n    pass"
        result = check_python_syntax(code)
        assert result["valid_syntax"] is False

    def test_indentation_error(self):
        """Test detection of indentation errors."""
        code = """
def func():
pass
"""
        result = check_python_syntax(code)
        assert result["valid_syntax"] is False

    def test_empty_code(self):
        """Test validation of empty code."""
        result = check_python_syntax("")
        assert result["valid_syntax"] is False
        assert "No code" in result["error"] or "empty" in result["error"].lower()


class TestOutputValidation:
    """Test full output validation pipeline."""

    def test_validate_complete_output(self):
        """Test validation of complete LLM output."""
        output = '''```python
def new_feature():
    """Implement new feature."""
    return True
```'''
        
        result = validate_generated_output(output)
        
        assert result["valid_syntax"] is True
        assert result["extracted_code"] is not None
        assert "def new_feature" in result["extracted_code"]

    def test_validate_invalid_output(self):
        """Test validation of invalid code output."""
        output = '''```python
def broken(
```'''
        
        result = validate_generated_output(output)
        
        assert result["valid_syntax"] is False
        assert result["error"] is not None

    def test_validate_no_code_found(self):
        """Test validation when no code block found."""
        output = "This response has no code at all."
        
        result = validate_generated_output(output)
        
        assert result["valid_syntax"] is False
        assert result["extracted_code"] is not None  # Falls back to plain text extraction

    def test_validate_multiple_functions(self):
        """Test validation of output with multiple functions."""
        output = '''```python
def authenticate(user, password):
    return user and password

def verify_token(token):
    return token and len(token) > 0
```'''
        
        result = validate_generated_output(output)
        
        assert result["valid_syntax"] is True
        assert result["extracted_code"] is not None
        assert "def authenticate" in result["extracted_code"]
        assert "def verify_token" in result["extracted_code"]


class TestLLMClient:
    """Test LLM client configuration and calling."""

    def test_is_llm_configured_detection(self):
        """Test LLM configuration detection."""
        # This will be True if GEMINI_API_KEY is set in env
        configured = is_llm_configured()
        assert isinstance(configured, bool)

    def test_call_llm_stub_when_unconfigured(self):
        """Test that stub response is returned when LLM not configured."""
        with patch.dict('os.environ', {'GEMINI_API_KEY': ''}):
            # Reimport to get fresh is_llm_configured check
            from app.generation import llm_client
            with patch.object(llm_client, 'GEMINI_API_KEY', ''):
                response = llm_client.call_llm("test prompt")
                
                assert isinstance(response, str)
                assert len(response) > 0
                # Stub response should be identifiable
                assert "STUB" in response or "placeholder" in response.lower()

    def test_call_llm_returns_string(self):
        """Test that call_llm always returns a string."""
        response = call_llm("What is authentication?")
        assert isinstance(response, str)
        assert len(response) > 0


class TestGenerationIntegration:
    """Integration tests for code generation pipeline."""

    def test_generate_code_with_evidence(self):
        """Test code generation with repository evidence."""
        request = "Add user authentication"
        context = [
            {
                "file_path": "auth.py",
                "text": "def login(): pass",
            }
        ]
        
        result = generate_code(request, context)
        
        assert "generated_output" in result
        assert "prompt" in result
        assert "evidence_chunks_used" in result
        assert result["evidence_chunks_used"] == 1
        assert isinstance(result["generated_output"], str)

    def test_generate_code_without_context(self):
        """Test code generation without evidence."""
        request = "Create a hello world function"
        
        result = generate_code(request, [])
        
        assert "generated_output" in result
        assert result["evidence_chunks_used"] == 0
        assert isinstance(result["generated_output"], str)

    def test_generation_result_structure(self):
        """Test that generation result has all required fields."""
        result = generate_code("test", [])
        
        required_fields = ["llm_configured", "evidence_chunks_used", "prompt", "generated_output"]
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
