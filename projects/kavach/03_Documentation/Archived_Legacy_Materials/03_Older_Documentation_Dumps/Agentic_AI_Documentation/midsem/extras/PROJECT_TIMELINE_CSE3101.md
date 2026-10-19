# KAVACH: 16-Week Project Timeline & Milestone Schedule
**Course Code:** CSE3101 — Agentic AI (Academic Year 2026–27)  
**Semester Duration:** 27th July 2026 to 20th November 2026 (16 Academic Weeks)  
**Deliverable Document:** Mandatory Submission for Project Evaluation (Phase-1)  

---

## 1. High-Level Phase Overview & Milestones

The project lifecycle is organized across the three formal evaluation phases mandated in the CSE3101 Course Handout:

```
[ WEEKS 1 - 4 ] ──> PHASE 1: Foundations, Charter & Pre-Execution Safety (10% Evaluation)
[ WEEKS 5 - 12 ] ──> PHASE 2: Multi-Agent Orchestration, RAG, Self-Healing & Working Prototype (30% Evaluation)
[ WEEKS 13 - 16 ] ──> PHASE 3: Hardening, MCP Interoperability, IEEE Benchmarks & End-Term Viva (40% Evaluation)
```

---

## 2. Detailed Week-by-Week Gantt Schedule

| Week | Dates | Focus Area & Syllabus Alignment | Concrete Deliverables & Work Items | Status |
| :---: | :--- | :--- | :--- | :---: |
| **Week 1** | Jul 27 – Jul 31 | Review of Prerequisites & LLM Foundations | • Problem definition & threat modeling for autonomous agents.<br>• Review of transformer attention, embeddings, and token limits. | ✅ Completed |
| **Week 2** | Aug 03 – Aug 07 | Introduction to Agentic AI (Chapter 1) | • Formulation of formal PEAS matrix for MAS.<br>• Definition of User Personas (Junior Dev, SRE, Auditor) and Agent Personas. | ✅ Completed |
| **Week 3** | Aug 10 – Aug 14 | Reasoning & Prompt Strategies (Chapter 2) | • Implementation of ReAct, CoT, and COTS prompt strategies.<br>• Comparative evaluation of zero-shot vs self-reflection. | ✅ Completed |
| **Week 4** | Aug 17 – Aug 21 | Agentic RAG Architecture (Chapter 2) | • AST code-aware chunking engine (`app/rag/ingest.py`).<br>• Local Qdrant vector database integration with MiniLM-L6-v2. | ✅ Completed |
| **Week 5** | Aug 24 – Aug 28 | **Phase-1 Milestone Preparation (September 3rd Week)** | • **One-Page Project Charter & Synopsis finalized.**<br>• **16-Week Timeline and Team Responsibility Matrix submitted.**<br>• **Phase-1 Evaluation (10% Weightage) Defense.** | ✅ **Current Phase** |
| **Week 6** | Aug 31 – Sep 04 | CrewAI & Multi-Agent Frameworks (Chapter 3) | • Construction of Supervisor-Worker finite state machine.<br>• Collaborative task handoffs between Sentinel and Coder agents. | ✅ Completed |
| **Week 7** | Sep 07 – Sep 11 | Tooling & Function Calling (Chapter 3/4) | • Shannon entropy calculation for API credentials.<br>• Context-aware Indian national identifier regex (Aadhaar/PAN). | ✅ Completed |
| **Week 8** | Sep 14 – Sep 18 | Change Impact & Blast Radius Analysis | • Python AST parser extracting imports and symbol call graphs.<br>• Transitive closure calculation of affected repository modules. | ✅ Completed |
| **Week 9** | Sep 21 – Sep 25 | Air-Gapped Privacy & Local LLMs | • Dual-engine routing: Google Gemini 2.5 Flash vs Local Ollama.<br>• Privacy toggle preventing proprietary code leaks to public clouds. | ✅ Completed |
| **Week 10** | Sep 28 – Oct 02 | Package Hallucination Defense | • AST import extraction & PyPI live registry verification.<br>• Slopsquatting supply-chain firewall with in-memory LRU cache. | ✅ Completed |
| **Week 11** | Oct 05 – Oct 09 | Self-Healing Reflection Loop | • Ephemeral sandbox subprocess runner (`pytest`).<br>• Automated reflection and iterative patch repair (max 3 cycles). | ✅ Completed |
| **Week 12** | Oct 12 – Oct 16 | **Phase-2 Milestone Preparation (October 3rd/4th Week)** | • **Working Prototype & Live Code Demonstration.**<br>• **Brief Progress Report (1-2 pages) & Demo-Based Evidence.**<br>• **Phase-2 Evaluation (30% Weightage) Defense.** | Scheduled |
| **Week 13** | Oct 19 – Oct 23 | Model Context Protocol (MCP) Integration | • Standalone MCP Server (`app/mcp/server.py`) using JSON-RPC 2.0.<br>• Integration with external developer tools (Cursor IDE / Claude Desktop). | ✅ Completed |
| **Week 14** | Oct 26 – Oct 30 | Mission Control Observability Dashboard | • Real-time dark-mode dashboard with SSE telemetry stream.<br>• Groq Whisper voice recognition and Prometheus metric exporter. | ✅ Completed |
| **Week 15** | Nov 02 – Nov 06 | Empirical Evaluation & 40+ Runs Verification | • Execution of 42 diverse benchmark runs logged in `workflow_runs.json`.<br>• LLM-as-a-Judge evaluation and agent latency profiling. | ✅ Completed |
| **Week 16** | Nov 09 – Nov 20 | **Final Capstone Defense & End-Term Exam (Phase-3)** | • **Full Functional Agentic Application deployed.**<br>• **Public GitHub Repository with 220 passing automated tests.**<br>• **Final Project Report (10%), Live Demo (20%), Viva (10%).** | Scheduled |

---

## 3. Evaluation Milestone Checkpoints

1. **Phase 1 Evaluation (10% Weightage — September 3rd Week):**
   * Charter, Timeline, Responsibility Matrix, and PEAS / Persona defense.
2. **Phase 2 Evaluation (30% Weightage — October 3rd/4th Week):**
   * Code demo of multi-agent flow, PII/secret gating, RAG retrieval, and working dashboard.
3. **Phase 3 End-Term Evaluation (40% Weightage — November 3rd Week):**
   * Final report submission, public repo inspection, MCP IDE demo, and individual viva.
