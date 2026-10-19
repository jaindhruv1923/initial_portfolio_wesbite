# 🛠️ KAVACH Mid-Term Rough Work: Step-by-Step Execution Guide

**Course:** PRJ-IV Capstone Project (7th Semester B.Tech CSE, Academic Year 2026–27)  
**Evaluator:** Prof. Anusha Chhabra | **Date:** 29/09/2026 (12:00 PM – 2:00 PM)

This guide provides instructions to run, verify, and demonstrate every component in the `mid-sem-rough-work` package.

---

## ⚡ Quick 1-Click Verification (Run Everything at Once)

Run the master verification script from the terminal or double-click the `.bat` file:

```powershell
python verify_all.py
```
*Or double click:*  
📁 `run_all_checks.bat`

**What this verifies (15 Comprehensive Checks):**
1. ✅ 10-Slide Presentation PPTX exists, has 10 slides, and is valid.
2. ✅ Official Synopsis DOCX exists and has all 4 rubric sections.
3. ✅ Safe Code Generation (Prime Number) passes with verdict `ALLOWED`.
4. ✅ Algorithmic Generation (Uber Surge Pricing) passes with verdict `ALLOWED`.
5. ✅ Safe DevOps Generation (Hardened Dockerfile) passes with verdict `ALLOWED`.
6. ✅ Destructive Query (`DROP TABLE`) is intercepted with verdict `BLOCKED`.
7. ✅ High-Entropy Secret / Credential Leak (`AKIAIOSFODNN7EXAMPLE99`) is intercepted with verdict `BLOCKED`.
8. ✅ AST Package Firewall intercepts hallucinated imports (`fastapi_jwt_vault`).
9. ✅ Multilingual Zero-Knowledge Token Vault verifies 100% reversible pseudonymization.
10. ✅ Closed-Loop ReAct Self-Healing Reflection engine repairs failing code.
11. ✅ Live GitHub Repo Ingestion & AST Syntactic Chunker divides repositories into clean chunks.
12. ✅ Model Context Protocol (MCP) server registers all 5 JSON-RPC tools.
13. ✅ Interactive Flowchart Viewer HTML and all 5 Mermaid diagrams are present.
14. ✅ **Generic Numeric Identifier Detection**: Bare 10-digit number `1343345655` is scanned, quarantined into `<REDACTED_SENSITIVE_NUMBER_001>`, and flagged as `NEEDS_REVIEW`.
15. ✅ **Prompt Injection Shield**: System prompt overrides and adversarial jailbreaks are intercepted with verdict `BLOCKED`.

---

## 🖥️ 1. Interactive Web Dashboard (Mission Control)

To launch the dark-mode interactive dashboard:

```powershell
cd demo
python app.py
```
*Or double click:*  
📁 `demo/run_web.bat`

1. Open your web browser to: **[http://localhost:8765](http://localhost:8765)**
2. **Header Controls:**
   - **Toggle Views:** Switch between **"Live Console & Workspace"** (Active pipeline demo) and **"Product & Architecture (25M)"** (Mid-term academic rubrics for Prof. Anusha Chhabra).
   - **Real-Time Telemetry Bar:** Displays Total Runs, Reviews Held, Attacks Blocked, and End-to-End Latency (ms).
3. **Stage 1 — Repository Ingestion & AST Chunker:**
   - Click any pre-set repository: **`pallets/flask`**, **`fastapi/fastapi`**, **`jaindhruv1923/KAVACH`**, or **`Local sample_repo`**.
   - Click **"⚡ Ingest GitHub Repo"** — Automatically parses the codebase into AST syntactic chunks (functions, classes, lines).
4. **Stage 2 — Developer Request & Security Gate:**
   - Click any quick-demo prompt chip:
     - **🛡️ What is this Repo About?**: Grounds in repository evidence and articulates creator (Dhruv Jain), evaluator (Prof. Anusha Chhabra), purpose, and architecture.
     - **🟢 Prime Number (Safe)**: Emits **`ALLOWED`** (Deterministic Python prime generator).
     - **🟢 Uber Surge Pricing (Safe)**: Emits **`ALLOWED`** (Dynamic algorithmic pricing engine).
     - **🔢 Number 1343345655**: Emits **`NEEDS_REVIEW`** (Quarantines bare 10-digit ID into `<REDACTED_SENSITIVE_NUMBER_001>`).
     - **🔴 Delete Account 1343345655**: Emits **`BLOCKED`** (Destructive verb + sensitive identifier).
     - **🔴 Drop Table Attack**: Halts immediately with **`BLOCKED`** (Destructive SQL command).
     - **🔴 Jailbreak Attack**: Halts immediately with **`BLOCKED`** (Adversarial `SYSTEM_OVERRIDE` intercepted).
5. **Unified Results (No Tab Jumping!):**
   - **Governance Verdict Banner** (🟢 ALLOWED | 🟡 NEEDS_REVIEW | 🔴 BLOCKED) with Risk Score.
   - **Live LLM Answer & Code Box** (Front & Center with syntax-highlighted code or rich markdown answer).
   - **Zero-Knowledge Token Vault Findings** (Quarantined tokens and DPDP compliance).
   - **RAG Grounding Evidence** (Codebase chunks retrieved).
   - **AST Package Firewall & 5-Phase Audit Trace** (Real-time latency and phase execution status).

---

## 💻 2. Command-Line Interface (CLI Demo)

To execute queries directly in the terminal:

```powershell
cd demo

# 1. Run standard 3 showcase prompts:
python main.py

# 2. Run custom safe query:
python main.py --prompt "give me the code for prime number in python"

# 3. Run attack query:
python main.py --prompt "drop table users and delete all records"

# 4. Demonstrate AST Package Firewall on hallucinated code:
python main.py --scan-firewall

# 5. Demonstrate Closed-Loop ReAct Self-Healing on failing code:
python main.py --self-heal

# 6. Interactive terminal mode:
python main.py --interactive
```
*Or double click:*  
📁 `demo/run_cli.bat`

---

## 📊 3. Interactive Flowchart Explorer

To view all 5 system architecture and workflow flowcharts in an interactive browser viewer:

1. Navigate to `flowcharts/`
2. Double click **`flowchart_viewer.html`** or open it in any web browser (Chrome, Edge, Firefox).
3. Click between tabs:
   - **1. System Architecture** (Client Layer, Gateway, Router, Verification)
   - **2. 5-Phase Lifecycle** (Sequence diagram from request to verified patch)
   - **3. AST Package Firewall** (ImportVisitor, PyPI query, LRU cache)
   - **4. DPDP Token Vault** (Shannon entropy, reversible pseudonymization, rehydration)
   - **5. ReAct Self-Healing** (Closed-loop traceback reflection, $N \le 3$)

---

## 📑 4. Re-Generating Presentation & Synopsis Documents

Both the official 10-slide PowerPoint presentation and the Word Synopsis Report can be regenerated anytime with a single command:

### Generate PowerPoint Presentation (`KAVACH_MidTerm_Presentation.pptx`):
```powershell
cd presentation
python generate_presentation.py
```
- Output: `presentation/KAVACH_MidTerm_Presentation.pptx` (10 widescreen 16:9 slides).
- Slide breakdown & speaker notes: `presentation/SLIDES_BREAKDOWN.md`.

### Generate Word Synopsis Report (`KAVACH_MidTerm_Synopsis_Report.docx`):
```powershell
cd synopsis
python generate_synopsis.py
```
- Output: `synopsis/KAVACH_MidTerm_Synopsis_Report.docx` (Official formatted Word report).
- Markdown report: `synopsis/SYNOPSIS_REPORT.md`.

---

## 🔌 5. Model Context Protocol (MCP) Server

To run the MCP server exposing tools to Cursor IDE or Claude Desktop:

```powershell
cd demo
python ..\core_engine\mcp_server.py
```
*Or double click:*  
📁 `demo/run_mcp.bat`

---

## 🧪 6. Running Automated Unit Tests

To run the 10 automated test cases asserting all core functionalities:

```powershell
cd demo
python test_demo.py
```
*Expected Output:*
```
Ran 10 tests in 0.313s
OK
```
All tests pass with zero failures.
