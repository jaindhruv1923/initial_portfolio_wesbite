# Running Kavach - Complete Guide

This document provides step-by-step instructions for running the complete Kavach security-governed AI DevOps platform, including testing and demo.

## Table of Contents
1. [Setup](#setup)
2. [Running Tests](#running-tests)
3. [Starting the Backend](#starting-the-backend)
4. [Running the Demo](#running-the-demo)
5. [Troubleshooting](#troubleshooting)

---

## Setup

### Prerequisites
- Python 3.10+
- pip package manager
- Windows, macOS, or Linux

### Step 1: Install Dependencies

```powershell
cd "C:\Users\jaind\Videos\PRJ-IV Work\kavach"
python -m pip install -r backend/requirements.txt
```

This installs:
- fastapi, uvicorn - Web framework
- pydantic - Data validation
- qdrant-client, sentence-transformers - RAG system
- pytest, pytest-cov, httpx - Testing

### Step 2: Configure Environment & Gemini API Key (Automatic & Permanent)

The Gemini API key is permanently stored and automatically loaded from:
- `kavach/keys/gemini_key.txt`
- `kavach/backend/keys/gemini_key.txt`
- `kavach/backend/.env`

Kavach automatically discovers the key upon startup with zero manual input required! You can also click **"Set Gemini Key"** in the top navigation bar of the web dashboard anytime to view or update it dynamically.

---

## Running Tests

### Run All Tests

From the project root:

```powershell
python -m pytest tests -v
```

**Expected Output**:
```
...
tests/test_cyber_defense_tough.py::test_base64_obfuscated_injection_payload_decloaked PASSED
tests/test_cyber_defense_tough.py::test_merkle_tree_ledger_inclusion_proof_and_tamper_detection PASSED
tests/test_cyber_defense_tough.py::test_cyber_attack_simulator_full_matrix_interception PASSED
...
======================== 274 passed, exit code 0 ========================
```

### Run Tough Cyber Defense & Red-Teaming Tests

```bash
# Run the 54 tough adversarial tests
python -m pytest tests/test_cyber_defense_tough.py -v

# Run the complete automated project verification
python verify_project.py
```

### Run Specific Test Module

```bash
# Test Cyber Defense & Red-Team Suite (54 tests)
python -m pytest tests/test_cyber_defense_tough.py -v

# Test Phase 1 RAG only
python -m pytest tests/test_rag.py -v

# Test Phase 2 Agent only
python -m pytest tests/test_agent.py -v

# Test Phase 4 Security Core only
python -m pytest tests/test_security.py -v

# Test Phase 4 Security v2 & Policy Engine
python -m pytest tests/test_security_v2.py -v

# Test Phase 5 Impact Analysis only
python -m pytest tests/test_impact.py -v

# Test API endpoints only
python -m pytest tests/test_api_endpoints.py -v

# Test end-to-end workflows only
python -m pytest tests/test_integration.py -v
```

### Run Tests with Coverage

```bash
python -m pytest tests --cov=backend/app --cov-report=html
# View coverage report: htmlcov/index.html
```

### Run Quick Sanity Check

```bash
python -m pytest tests -q
# Shows just pass/fail count, faster execution
```

---

## Starting the Backend

### Start Uvicorn Server

```powershell
cd "C:\Users\jaind\Videos\PRJ-IV Work\kavach"
python -m uvicorn app.main:app --reload --reload-dir backend/app --app-dir backend --host 127.0.0.1 --port 8000
```

### Starting the Dashboard

**Option A (All-in-One - Recommended):**
Open your browser directly to:
**http://127.0.0.1:8000/**
FastAPI mounts the frontend static files automatically and serves everything on port 8000!

**Option B (Separate Live Server - Port 5500):**
In a second terminal:

```powershell
cd "C:\Users\jaind\Videos\PRJ-IV Work\kavach"
python -m http.server 5500 --directory frontend
```

Open `http://127.0.0.1:5500`. Use Chrome or Edge for microphone input.

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

### Verify Server is Running

In another terminal:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "service": "kavach-backend"}
```

### Access API Documentation

Open in browser: `http://localhost:8000/docs`

You'll see the Swagger UI with interactive documentation for all endpoints.

---

## Running the Demo

The demo showcases Kavach analyzing a sample authentication system codebase.

### Demo Scenario: Security Analysis of Authentication System

#### Step 1: Ingest Demo Repository

Using curl:
```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_path": "demo_repo"
  }'
```

Expected response:
```json
{
  "repo_path": "demo_repo",
  "files_chunks_found": 12,
  "chunks_indexed": 12
}
```

Or using Swagger UI:
1. Go to http://localhost:8000/docs
2. Find POST `/ingest`
3. Enter repo_path: `demo_repo`
4. Click "Execute"

#### Step 2: Search Repository

Search for authentication code:

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "password validation and hashing",
    "top_k": 3
  }'
```

Expected: Returns 3 most relevant code chunks about password handling.

#### Step 3: Detect Sensitive Data

Test security detection:

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "My PAN is ABCDE1234F"
  }'
```

Expected response:
```json
{
  "input": "My PAN is ABCDE1234F",
  "findings": [
    {
      "category": "PAN",
      "value": "ABCDE1234F",
      "action": "BLOCK",
      "severity": "high",
      "confidence": 0.95,
      "reason": "Matches PAN format (5 letters + 4 digits + 1 letter)"
    }
  ],
  "allowed": false
}
```

#### Step 4: Submit Development Request Through Full Workflow

Submit a realistic development request:

```bash
curl -X POST "http://localhost:8000/agent/request" \
  -H "Content-Type: application/json" \
  -d '{
    "request_text": "Add OAuth 2.0 authentication support to the login system"
  }'
```

Expected response (simplified):
```json
{
  "workflow_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "final_stage": "COMPLETE",
  "plan": [
    "Understand the request and identify its scope",
    "Identify authentication-related files",
    "Review existing auth logic",
    "Retrieve grounding evidence from the repository (RAG)",
    "Run security/policy checks on the request and any retrieved context"
  ],
  "retrieved_context": [
    {
      "score": 0.92,
      "file_path": "auth.py",
      "chunk_index": 0,
      "text": "def authenticate_user(username: str, password: str..."
    }
  ],
  "security_findings": [],
  "generation_result": {
    "llm_configured": false,
    "evidence_chunks_used": 1,
    "prompt": "You are a careful software engineer...",
    "generated_output": "[STUB RESPONSE — no GEMINI_API_KEY set...]"
  },
  "validation_result": {
    "valid_syntax": true,
    "error": null,
    "extracted_code": "def oauth_authenticate()..."
  },
  "impact_report": [
    {
      "file_path": "auth.py",
      "relevance_score": 0.95,
      "reason": "semantically related to the change description"
    },
    {
      "file_path": "api.py",
      "relevance_score": 0.82,
      "reason": "imports/references the most-related file"
    }
  ],
  "history": [
    "REQUEST_RECEIVED -> PLANNING (Starting planning phase)",
    "PLANNING -> CONTEXT_RETRIEVAL",
    "CONTEXT_RETRIEVAL -> SECURITY_CHECK",
    "SECURITY_CHECK -> IMPACT_ANALYSIS",
    "IMPACT_ANALYSIS -> GENERATION",
    "GENERATION -> COMPLETE (Phase 3 scope complete...)"
  ]
}
```

This shows the complete workflow:
- Planning → task decomposition
- RAG → code retrieval
- Security → PII detection
- Impact → file prediction
- Generation → code synthesis
- Validation → syntax checking

#### Step 5: Retrieve Workflow Run

Get the results of the workflow:

```bash
curl http://localhost:8000/agent/runs/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

#### Step 6: List All Workflow Runs

```bash
curl http://localhost:8000/agent/runs
```

Response:
```json
{
  "count": 1,
  "runs": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "stage": "COMPLETE",
      "request": "Add OAuth 2.0 authentication support to the login system"
    }
  ]
}
```

#### Step 7: Analyze Impact of Change

Predict which files would be affected:

```bash
curl -X POST "http://localhost:8000/impact/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "change_description": "Modify password validation logic"
  }'
```

#### Step 8: Evaluate Security Engine

Get performance metrics on security test corpus:

```bash
curl http://localhost:8000/evaluate
```

Response shows precision/recall across PII categories (PAN, Aadhaar/National ID, sensitive numbers, phone, bank account, email).

---

## Understanding the Architecture

### 5-Phase Pipeline

**Phase 1: Repository Ingestion & RAG**
- Walks repository, chunks files
- Embeds with sentence-transformers
- Stores in Qdrant vector DB

**Phase 2: Agent Orchestrator**
- Manages workflow state machine
- Coordinates between phases
- Maintains audit trail

**Phase 3: Evidence-Grounded Generation**
- Retrieves relevant code (RAG)
- Builds grounded prompt
- Calls LLM with evidence
- Validates generated syntax

**Phase 4: Security Engine**
- Detects PII, sensitive numbers, credentials, and secrets
- Context-aware and standalone identifier detection
- Severity-based action (BLOCK/REDACT)
- Explainability for every finding

**Phase 5: Change Impact Analysis**
- Combines semantic + dependency signals
- Predicts affected files
- Ranks by relevance

### Data Flow

```
User Request
    ↓
Input PII Check (Security)
    ↓
Task Planning
    ↓
Repository Search (RAG)
    ↓
Context PII Check (Security)
    ↓
Impact Analysis
    ↓
Code Generation
    ↓
Output PII Check (Security)
    ↓
Syntax Validation
    ↓
Response with Audit Trail
```

---

## Troubleshooting

### Tests Not Running

**Problem**: `python -m pytest tests` produces no output

**Solution**:
```bash
# Verify pytest is installed
python -c "import pytest; print(pytest.__version__)"

# Try from backend directory
cd backend
python -m pytest ../tests -v

# Check for import errors
python -c "from tests import conftest"
```

### Server Won't Start

**Problem**: Port 8000 already in use

**Solution**:
```bash
# Use different port
python -m uvicorn app.main:app --reload --app-dir backend --port 8001
```

### API Requests Timeout

**Problem**: Requests to `/agent/request` take very long or timeout

**Reason**: First request initializes sentence-transformers model (~200MB download)

**Solution**: Wait for initial model download, subsequent requests are fast.

### Qdrant Index Errors

**Problem**: "Collection not found" or similar

**Solution**:
```bash
# Index is rebuilt on each ingest call
# Try ingesting demo_repo again
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "demo_repo"}'
```

### LLM Generation Returns Stub

**Problem**: Generation results show "[STUB RESPONSE - no GEMINI_API_KEY set]"

**Solution**: 
```bash
# Optional: Set up real API key
cd backend
python setup_env.py  # Enter your free Gemini API key

# Restart server
# Now generation will use real LLM
```

---

## Performance Notes

### First-Time Setup
- Initial pytest run: ~60 seconds (model download + initialization)
- Subsequent runs: ~10 seconds
- API startup: ~30 seconds
- First `/agent/request`: ~10 seconds (model initialization)
- Subsequent requests: ~2-5 seconds

### Optimization Tips
- Keep server running between requests
- Qdrant index persists in `backend/qdrant_storage/`
- Model cached in `~/.cache/huggingface/`
- Use `top_k` parameter to limit RAG results

---

## Next Steps

1. **Explore the Code**:
   - Read `docs/ARCHITECTURE.md` for system design
   - Read `docs/AGENT_SPEC.md` for orchestrator details
   - Read `docs/SECURITY_SPEC.md` for security rules

2. **Run the Tests**:
   - Review test implementations
   - Add additional test cases
   - Measure coverage

3. **Customize the Demo**:
   - Add your own repository
   - Create custom security rules
   - Extend with additional phases

4. **Deploy to Production**:
   - Set up persistent Qdrant
   - Add PostgreSQL for audit logs
   - Configure CI/CD integration
   - Deploy to cloud platform

---

## Support & Questions

- **API Documentation**: http://localhost:8000/docs
- **Project Spec**: See `docs/PROJECT_SPEC.md`
- **Architecture Docs**: See `docs/ARCHITECTURE.md`
- **Test Suite**: See `tests/` directory
- **Demo**: See `demo_repo/DEMO.md`
