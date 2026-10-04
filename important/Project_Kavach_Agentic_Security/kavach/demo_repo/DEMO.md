# Kavach End-to-End Demo

This directory contains a simple demo application and walkthrough for the Kavach security-governed AI DevOps platform.

## Demo Overview

The demo uses a simple **Authentication System** codebase with three modules:
- `auth.py` - User authentication logic
- `database.py` - User database management  
- `api.py` - REST API endpoints

Kavach will analyze proposed changes to this codebase through its complete 5-phase pipeline.

## Quick Start

### 1. Start the Kavach Backend

From the `backend/` directory:

```bash
cd backend
pip install -r requirements.txt
python setup_env.py  # Configure GEMINI_API_KEY if desired
python -m uvicorn app.main:app --reload --app-dir backend
```

The API will be available at `http://localhost:8000`

### 2. Access Swagger API Documentation

Open browser to: `http://localhost:8000/docs`

You'll see interactive API documentation for all Kavach endpoints.

## Demo Scenarios

Run these scenarios in order to see Kavach in action.

### Scenario 1: Index the Demo Repository

**Objective**: Load the demo code into Kavach's RAG system.

**Swagger Steps**:
1. Go to POST `/ingest`
2. Enter repo path: `C:\Users\dhruv\OneDrive\Desktop\PRJ-IV\Kavach_AllPhases\Complete_Merged_Project\demo_repo`
   (Or use relative path: `demo_repo`)
3. Click "Execute"

**Expected Output**:
```json
{
  "repo_path": "demo_repo",
  "files_chunks_found": 12,
  "chunks_indexed": 12
}
```

This shows Kavach found 3 Python files and created 12 searchable chunks.

---

### Scenario 2: Search for Code

**Objective**: Verify RAG retrieval works correctly.

**Swagger Steps**:
1. Go to POST `/search`
2. Enter query: `password validation and hashing`
3. Set top_k: `3`
4. Click "Execute"

**Expected Output**:
```json
{
  "query": "password validation and hashing",
  "results": [
    {
      "score": 0.87,
      "file_path": "auth.py",
      "chunk_index": 1,
      "text": "def set_password(self, password: str) -> None:\n    \"\"\"Hash and store user password.\"\"\"\n    ..."
    },
    ...
  ]
}
```

Kavach found auth.py as most relevant because it contains password hashing logic.

---

### Scenario 3: Detect Sensitive Data

**Objective**: Show security enforcement on raw developer input.

**Swagger Steps**:
1. Go to POST `/detect`
2. Enter text with PII:
   ```
   My PAN is ABCDE1234F and I want to add it to the database
   ```
3. Click "Execute"

**Expected Output**:
```json
{
  "input": "My PAN is ABCDE1234F and I want to add it to the database",
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

Kavach blocks the request because it contains sensitive PII (PAN number).

---

### Scenario 4: Submit Development Request

**Objective**: Run a developer request through the complete Kavach workflow.

**Request**: "Add OAuth 2.0 support to the authentication system"

**Swagger Steps**:
1. Go to POST `/agent/request`
2. Enter request_text: `Add OAuth 2.0 support to the authentication system`
3. Click "Execute"

**Expected Workflow**:

The response shows all stages of the Kavach workflow:

```json
{
  "workflow_id": "12345abc...",
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
      "text": "def authenticate_user(username: str, password: str, user_db: dict) -> Optional[User]:"
    },
    {
      "score": 0.88,
      "file_path": "api.py",
      "chunk_index": 2,
      "text": "def login(self, username: str, password: str) -> Optional[dict]:"
    }
  ],
  "security_findings": [],  // No PII detected
  "generation_result": {
    "llm_configured": false,
    "evidence_chunks_used": 2,
    "prompt": "You are a careful software engineer...",
    "generated_output": "[STUB RESPONSE — no GEMINI_API_KEY set...]"
  },
  "validation_result": {
    "valid_syntax": true,
    "error": null,
    "extracted_code": "def oauth_authenticate(...):"
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

**What happened**:
1. **Planning**: Identified this as auth-related
2. **RAG Retrieval**: Found auth.py and api.py as relevant
3. **Security Check**: Verified request and context have no PII
4. **Impact Analysis**: Predicted auth.py and api.py would be affected
5. **Generation**: Generated stub code (would be real with API key)
6. **Validation**: Verified generated syntax is correct

---

### Scenario 5: Check Change Impact

**Objective**: Predict which files would be affected by a change.

**Swagger Steps**:
1. Go to POST `/impact/analyze`
2. Change description: `Modify password validation logic`
3. repo_path: `app` (default)
4. Click "Execute"

**Expected Output**:
```json
{
  "change_description": "Modify password validation logic",
  "impact_report": [
    {
      "file_path": "auth.py",
      "relevance_score": 0.98,
      "reason": "semantically related to the change description"
    },
    {
      "file_path": "api.py",
      "relevance_score": 0.72,
      "reason": "imports/references the most-related file"
    }
  ]
}
```

Kavach ranks files by how likely they are to be affected by the proposed change.

---

### Scenario 6: Evaluate Security Engine

**Objective**: See multilingual security detection performance.

**Swagger Steps**:
1. Go to GET `/evaluate`
2. Click "Execute"

**Expected Output**:
```json
{
  "overall": {
    "precision": 0.92,
    "recall": 0.88,
    "f1": 0.90,
    "true_positives": 46,
    "false_positives": 4,
    "false_negatives": 6,
    "true_negatives": 44
  },
  "per_language": {
    "Hindi": { "precision": 0.94, "recall": 0.90, "f1": 0.92, ... },
    "Marathi": { "precision": 0.90, "recall": 0.85, "f1": 0.87, ... },
    "Tamil": { "precision": 0.91, "recall": 0.89, "f1": 0.90, ... },
    "Telugu": { "precision": 0.93, "recall": 0.87, "f1": 0.90, ... },
    "Hinglish": { "precision": 0.88, "recall": 0.82, "f1": 0.85, ... }
  },
  "total_cases": 50
}
```

Shows that Kavach's security engine detects PII with 90%+ accuracy across languages.

---

### Scenario 7: Complex Multi-Step Request with Blocked PII

**Request**: "Please update the password reset feature. My email is john.doe@example.com and I want to test with PAN ABCDE1234F"

**Swagger Steps**:
1. Go to POST `/agent/request`
2. Enter the request above
3. Click "Execute"

**Expected Output**:
The workflow stops at security check because it detects both email and PAN:

```json
{
  "workflow_id": "...",
  "final_stage": "BLOCKED",
  "security_findings": [
    {
      "category": "email",
      "value": "john.doe@example.com",
      "action": "REDACT",
      "severity": "medium",
      "confidence": 0.95,
      "reason": "Matches email address format"
    },
    {
      "category": "PAN",
      "value": "ABCDE1234F",
      "action": "BLOCK",
      "severity": "high",
      "confidence": 0.95,
      "reason": "Matches PAN format..."
    }
  ],
  "history": [
    "REQUEST_RECEIVED -> PLANNING",
    "PLANNING -> CONTEXT_RETRIEVAL",
    "CONTEXT_RETRIEVAL -> SECURITY_CHECK",
    "SECURITY_CHECK -> BLOCKED (sensitive data detected in the raw request)"
  ]
}
```

Kavach stops the workflow and asks for human review before proceeding.

---

## Understanding the Complete Pipeline

The Kavach workflow follows this sequence:

```
Developer Request
        ↓
  [Security Check 1: Input PII]
        ↓
     [Planning] → Keyword-based task decomposition
        ↓
 [RAG Retrieval] → Find relevant code in repository
        ↓
  [Security Check 2: Context PII]
        ↓
[Impact Analysis] → Predict affected files
        ↓
   [Generation] → Generate code with LLM (evidence-grounded)
        ↓
  [Security Check 3: Output PII]
        ↓
   [Validation] → Check generated code syntax
        ↓
    Final Response with full audit trail
```

## Testing the Test Suite

From the project root directory:

```bash
python -m pytest tests -v
```

This runs 164 tests covering:
- Phase 1: RAG (ingest, embedding, search)
- Phase 2: Agent (planning, orchestration, state)
- Phase 3: Generation (validation, LLM integration)
- Phase 4: Security (PII detection, evaluation)
- Phase 5: Impact analysis (dependency graph, ranking)
- API Endpoints (all 10 endpoints)
- End-to-End workflows

**Expected**: 160+ tests pass, showing the complete system is working.

## Files in This Demo

- `auth.py` - User authentication module with password handling
- `database.py` - User database implementation
- `api.py` - REST API endpoint implementations
- `DEMO.md` - This file

## Key Learnings from Demo

1. **Evidence-Grounded Generation**: Kavach grounds LLM responses in real repository code
2. **Universal Security Detection**: Detects PII, sensitive numbers (e.g. 12454323454, Aadhaar, PAN), credentials, and API keys
3. **Transparent Workflow**: Full audit trail of every stage
4. **Impact Prediction**: Combines semantic + dependency signals for change impact
5. **Fail-Safe Design**: Blocks on PII rather than processing sensitive data

## Next Steps

For production deployment:
1. Replace Qdrant in-memory with persistent instance
2. Add real database layer (PostgreSQL) for audit logs
3. Configure with actual LLM API keys
4. Add CI/CD integration (GitHub Actions, GitLab CI)
5. Deploy to cloud platform (AWS, GCP, Azure)

## Support

For questions about the implementation, see:
- `docs/PROJECT_SPEC.md` - Overall project specification
- `docs/ARCHITECTURE.md` - System architecture and design
- `docs/AGENT_SPEC.md` - Agent orchestrator specification
- `docs/SECURITY_SPEC.md` - Security engine specifications
- `docs/IMPLEMENTATION_STATUS.md` - Current implementation progress
