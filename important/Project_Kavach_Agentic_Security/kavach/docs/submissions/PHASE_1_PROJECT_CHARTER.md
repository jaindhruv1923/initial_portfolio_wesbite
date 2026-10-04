# ONE-PAGE PROJECT CHARTER & SYNOPSIS
**Academic Year:** 2026–27 | **Semester:** 7th Semester (B.Tech CSE)  
**Course Code & Name:** CSE3101 — Agentic AI  
**Course Faculty:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Institution:** School of Engineering & Technology, BML Munjal University  

---

### Project Title
**KAVACH: A Security-Governed Multi-Agent AI DevOps & Observability Platform**

### 1. Problem Definition (Rubric C1)
Modern autonomous software engineering agents (e.g., Devin, SWE-agent) automate code generation, dependency imports, and pull requests. However, deploying unconstrained agents in enterprise environments introduces critical vulnerabilities:
1. **Supply-Chain Slopsquatting:** Autonomous agents hallucinate non-existent package names (e.g., `import fastapi_jwt_vault`), creating attack vectors for malicious takeover on PyPI/npm.
2. **Credential & PII Leaks:** Agents inadvertently leak proprietary API keys or national identifiers (Aadhaar/PAN) into public Git commits or external LLM prompt logs.
3. **Unbounded Blast Radius:** Agents modify shared dependencies without structural awareness, causing downstream regressions.
4. **Infinite Debugging Loops:** Stochastic generation leads to non-convergent debugging oscillations and token exhaustion.

### 2. Objectives and Measurable Outcomes (Rubric C2 — Aligned with CO1, CO2, CO3)
* **Objective 1 (CO1 - Multi-Agent Orchestration):** Construct a collaborative multi-agent architecture (Supervisor, Sentinel, Retriever, BlastRadius, and Coder) coordinating via deterministic state machines.
* **Objective 2 (CO2 - Privacy & Data Security):** Implement an air-gapped local LLM switch (Ollama / Qwen2.5-Coder) and zero-knowledge token vaulting to protect proprietary source code.
* **Objective 3 (CO3 - Multi-Modal & Interoperable Tools):** Expose security tools over Anthropic’s Model Context Protocol (MCP) for Cursor/Claude IDE integration, with Groq Whisper multimodal voice input.
* **Quantitative Target Metrics:** 100% catch rate on hallucinated packages, 100% detection of high-entropy secrets, F1 $\ge 0.95$ on PII, and $<1.5$s average end-to-end governed latency.

### 3. Proposed Methodology & Architecture (Rubric C3)
Kavach implements a 6-stage governed execution pipeline:
$$\text{Prompt} \longrightarrow \text{Sentinel Screening} \longrightarrow \text{Qdrant RAG} \longrightarrow \text{AST Blast Radius} \longrightarrow \text{LLM Synthesis} \longrightarrow \text{AST Firewall} \longrightarrow \text{ReAct Sandbox}$$
* **Sentinel Pre-Execution Guard:** Deterministic Shannon entropy calculation ($H > 4.5$) and regex filters for PII and credentials before invoking any LLM.
* **Agentic RAG Knowledge Base:** `sentence-transformers/all-MiniLM-L6-v2` dense embeddings with Qdrant vector storage.
* **AST Package Firewall:** Static Python Abstract Syntax Tree analysis verifying all external imports against PyPI registry APIs.
* **Self-Healing ReAct Sandbox:** Ephemeral test execution capturing failure tracebacks with reflective repair (max 3 cycles).

### 4. Feasibility, Resource Planning & Tech Stack (Rubric C4)
* **Backend:** Python 3.11+, FastAPI (Async REST + SSE Streams), Qdrant Vector Client, Pydantic V2.
* **Models:** Google Gemini 2.5 Flash / Groq Cloud (`whisper-large-v3-turbo`) with zero-cost local fallback (Ollama `qwen2.5-coder:7b`).
* **Interoperability:** Model Context Protocol (MCP SDK), GitHub DevOps Webhooks.
* **Frontend:** Modern dark-mode Mission Control Dashboard (`Inter` + `JetBrains Mono` fonts, Vanilla JS/CSS).
* **Cost & Feasibility:** Entire platform runs locally on standard student hardware without mandatory paid subscriptions.

### 5. Individual Understanding & Team Responsibility (Rubric C5)
* **Team Structure:** 3 Core Engineering Members with mandatory role rotation across phases (Agent Workflows, Security Engine, RAG & Tooling).
* **Public Repository:** All source code, test suites (220 passing tests), and benchmarks maintained under a public GitHub repository adhering to university academic integrity standards.
