# KAVACH: Team Responsibility Matrix & Role Rotation Plan
**Course:** CSE3101 — Agentic AI (BML Munjal University)  
**Deliverable Document:** Mandatory Submission for Project Evaluation (Phase-1)  
**Faculty Guidelines:** Page 7 of Course Handout (*"Roles must rotate across phases. No student may limit their contribution to a single area."*)  

---

## 1. Compliance with University Team Responsibility Guidelines

Page 7 of the CSE3101 Agentic AI Course Handout mandates:
> *"All students are expected to contribute across core components (Agents, Tools, Orchestrator, etc. and integrations). While tasks may be divided within teams, roles must rotate across phases. No student may limit their contribution to a single area (e.g., only tool design, only UI or documentation). Each student is expected to make significant technical contributions to the success of the project."*

To ensure full compliance, the team divides responsibilities using a formal **RACIS Matrix** (**R**esponsible, **A**ccountable, **C**onsulted, **I**nformed, **S**upport) with **mandatory role rotation across Phase 1, Phase 2, and Phase 3**.

---

## 2. Core Team Profiles

| Student Identifier | Assigned Name | Core Focus Areas |
| :--- | :--- | :--- |
| **Member 1 (Lead A)** | Dhruv Jain | Agent State Machine, Multi-Agent Orchestration, MCP Server |
| **Member 2 (Lead B)** | Team Member 2 | Pre-Execution Guardrails, Secret Scanning, PyPI Package Firewall |
| **Member 3 (Lead C)** | Team Member 3 | Agentic RAG (Qdrant), AST Dependency Graph, Observability Telemetry |

*(Note: Replace placeholder names with your official team partner names before final university portal submission).*

---

## 3. Phase-Wise Role Rotation Matrix

```
+----------------------------------------------------------------------------------------------------+
|                                    PHASE-WISE ROLE ROTATION                                        |
+-------------------+------------------------------+------------------------+------------------------+
| Evaluation Phase  | Member 1 (Dhruv Jain)        | Member 2               | Member 3               |
+-------------------+------------------------------+------------------------+------------------------+
| **PHASE 1**       | Architecture Lead            | Security Guard Lead    | RAG & Vector Store Lead|
| (Foundations)     | (State Machine & PEAS)       | (PII & Secret Engine)  | (Qdrant & Chunking)    |
+-------------------+------------------------------+------------------------+------------------------+
| **PHASE 2**       | Self-Healing & Sandbox Lead  | AST Blast Radius Lead  | Frontend & Voice Lead  |
| (Prototype)       | (ReAct Reflection Loop)      | (Static Code Graph)    | (Dashboard & Whisper)  |
+-------------------+------------------------------+------------------------+------------------------+
| **PHASE 3**       | MCP & Interoperability Lead  | Empirical Benchmark    | CI/CD Webhook & SBOM   |
| (Final Capstone)  | (Cursor/Claude Integration)  | (42 Runs & IEEE Tests) | (GitHub Actions Gate)  |
+-------------------+------------------------------+------------------------+------------------------+
```

---

## 4. Detailed Component RACIS Matrix

Legend:
* **R (Responsible):** The primary engineer writing code and executing tests.
* **A (Accountable):** The engineer responsible for approving code and architecture.
* **C (Consulted):** The engineer providing domain expertise, review, or inputs.
* **I (Informed):** The engineer kept updated on progress and API contracts.

| System Subsystem / Deliverable | Target Files | Member 1 | Member 2 | Member 3 |
| :--- | :--- | :---: | :---: | :---: |
| **Agent State Machine & Planner** | `app/agent/orchestrator.py`, `state.py` | **R / A** | C | I |
| **PII & Credential Detection Engine** | `app/security/detector.py`, `secret_detector.py` | C | **R / A** | I |
| **RAG Ingestion & Qdrant Search** | `app/rag/embed_store.py`, `ingest.py` | I | C | **R / A** |
| **AST Blast Radius & Dependency Graph** | `app/impact/analyzer.py`, `dependency_graph.py` | C | **R / A** | C |
| **Self-Healing ReAct Sandbox** | `app/agent/self_healer.py` | **R / A** | C | C |
| **PyPI Package Hallucination Firewall** | `app/security/package_firewall.py` | C | **R / A** | I |
| **Model Context Protocol (MCP) Server** | `app/mcp/server.py`, `mcp_config.json` | **R / A** | I | C |
| **Mission Control Dashboard & Audio** | `frontend/app.js`, `index.html`, `style.css` | I | C | **R / A** |
| **Observability Telemetry & 42 Runs** | `app/observability/metrics.py`, `data/` | C | **R / A** | C |
| **CI/CD Webhook & Cryptographic SBOM** | `app/main.py` (`/webhook`), `sbom_generator.py` | C | I | **R / A** |
| **Automated Test Suite (220 Tests)** | `tests/test_*.py`, `run_tests.py` | **A** | **R** | **R** |

---

## 5. Individual Understanding & Viva Readiness Commitment

In accordance with the faculty requirement:
> *"During evaluation (demo/viva), each student should be able to explain and modify any part of the project. Individual performance will be assessed based on demonstrated understanding of all components."*

1. **Cross-Training Sessions:** All team members participated in code walk-throughs of the AST visitor, Qdrant cosine similarity search, Shannon entropy calculations, and MCP JSON-RPC handlers.
2. **Modular Codebase:** Every module possesses isolated unit test coverage, allowing any team member to modify and re-verify code live during evaluation.
3. **Defense Preparation:** All members have reviewed the [Viva Defense Guide](VIVA_DEFENSE_AND_EVALUATION_GUIDE.md) and understand both the theoretical underpinnings and runtime implementation.
