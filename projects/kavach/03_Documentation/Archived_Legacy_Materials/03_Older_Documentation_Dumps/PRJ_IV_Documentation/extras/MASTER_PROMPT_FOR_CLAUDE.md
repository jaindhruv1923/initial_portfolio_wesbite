# MASTER PROMPT FOR CLAUDE: PRJ-IV MID-TERM PRESENTATION & SYNOPSIS REPORT
**Designed for:** Claude 3.5 Sonnet / Claude 3 Opus  
**Target Course:** Project-IV (7th Semester Major Capstone Project — 5 Credits)  
**Institution:** BML Munjal University (School of Engineering & Technology, Dept of CSE)  
**Evaluator / Coordinator:** Prof. Anusha Chhabra  
**Evaluation Date:** 29th September 2026 (12:00 PM – 2:00 PM)  

---

> ### 📋 HOW TO USE THIS PROMPT
> Copy the complete text inside the block below and paste it directly into Claude. It contains every architectural, mathematical, empirical, and administrative detail of Project KAVACH, structured to force Claude to produce a flawless, publication-grade Synopsis Report and 8–10 Slide Presentation Script matching Prof. Anusha Chhabra's exact 25-mark grading rubrics.

---

```markdown
You are an elite Computer Science Professor, Principal AI Security Researcher, and Capstone Project Defense Coach. 

I am presenting my 7th-Semester Major Capstone Project (Project-IV, 5 Credits) at BML Munjal University, Department of Computer Science & Engineering.
Our Mid-Term Presentation is scheduled on 29th September 2026 at 12:00 PM – 2:00 PM before Faculty Coordinator Prof. Anusha Chhabra.

You must generate:
1. An exhaustive, publication-grade Academic Synopsis Report.
2. A professional, slide-by-slide 8–10 Slide Presentation Deck Script (with visual layout, bullet points, speaking notes, and time allocations).

Both the Report and Presentation MUST strictly address the 4 official grading rubrics specified by Prof. Anusha Chhabra (Total 25 Marks):
- RUBRIC 1: Comprehensiveness of the Literature Review (10 Marks)
- RUBRIC 2: Research Gap Identified (5 Marks)
- RUBRIC 3: Objective / Problem Definition (5 Marks)
- RUBRIC 4: Proposed Methodology (Tools, Techniques, Methods, Datasets) (5 Marks)

--------------------------------------------------------------------------------
1. PROJECT METADATA & TEAM ROSTER
--------------------------------------------------------------------------------
• Project Title: KAVACH: A Security-Governed Multi-Agent AI DevOps & Observability Platform
• Platform Name: Kavach (Hindi for "Shield / Armor")
• Department: Department of Computer Science & Engineering, BML Munjal University
• Academic Year: 2026–27 | 7th Semester B.Tech CSE
• Team Members:
  1. Dhruv Jain (Enrollment No: 230532) — Architecture, Agent State Machine, MCP Server Lead
  2. Dev Garg (Enrollment No: 230487) — Pre-Execution Guardrails, Secret Scanning, Package Firewall Lead
  3. Ansh Rohilla (Enrollment No: 230794) — Agentic RAG, Qdrant Vector Store, AST Dependency Graph Lead
  4. Ansh Adhikari (Enrollment No: 230822) — Autonomous Sandbox, Self-Healing ReAct Loop, Dashboard Telemetry Lead

--------------------------------------------------------------------------------
2. DETAILED PROJECT TECHNICAL ANATOMY (WHAT, WHY, AND HOW IT HAPPENS)
--------------------------------------------------------------------------------

A. THE "WHY" — THE CRITICAL ENTERPRISE AI DILEMMA:
Autonomous software engineering agents (e.g., Devin, SWE-agent, AutoPR) promise end-to-end automation of software delivery: reading code, generating patches, and opening pull requests. However, deploying unconstrained LLM agents in enterprise environments introduces fatal vulnerabilities:
1. AI Package Hallucination & "Slopsquatting" (AI Dependency Confusion): LLMs are probabilistic token predictors that regularly hallucinate non-existent third-party library imports (e.g., `import fastapi_jwt_vault_security`). Attackers monitor common hallucinations, register those package names on PyPI/npm with malicious payloads, and wait for developer agents to `pip install` them. Traditional SCA tools (Snyk, Dependabot) only scan static `requirements.txt` files and are 100% blind to runtime agent-synthesized code.
2. Credential & PII Leakage: Developers accidentally paste production API keys (AWS, GitHub, Stripe) or regulated national identity data (Indian Aadhaar, PAN) into prompt context, leaking proprietary IP into third-party cloud LLM prompt logs.
3. Unbounded Blast Radius: Coding agents modify shared utilities without understanding transitive caller-callee dependency graphs, silently breaking downstream microservices.
4. Non-Terminating Oscillations: Stochastic generation leads to infinite debugging loops where fixing bug A breaks bug B.
5. Prompt Injection: Adversarial delimiter sequences embedded in code comments or issue descriptions hijack the agent's goal state.

B. THE "WHAT" — THE KAVACH GOVERNED PIPELINE:
Kavach is an enterprise-grade, security-governed agentic AI observability and self-healing platform. Rather than trusting raw LLMs, Kavach routes every developer request through a 6-stage deterministic finite state machine governed by 5 collaborative agent personas:
`Developer Prompt -> Sentinel Screening -> Qdrant RAG -> AST Blast Radius -> LLM Synthesis -> AST Package Firewall -> ReAct Sandbox -> Verified Patch`

C. THE "HOW" — MINUTE TECHNICAL, MATHEMATICAL & ARCHITECTURAL IMPLEMENTATION:
1. Stage 1: Sentinel Pre-Execution Gatekeeper (`SentinelAgent`):
   - Computes Shannon Entropy over input tokens: H = -sum(p_i * log2(p_i)). High-entropy strings (H > 4.5) with length > 20 characters trigger immediate blocking of AWS, GitHub, Stripe, and private RSA keys.
   - Executes deterministic regex matching with Verhoeff context validation for Indian national identifiers (Aadhaar cards, PAN cards, phone numbers, emails) complying with India's Digital Personal Data Protection (DPDP) Act 2023.
   - Zero-Knowledge Token Vaulting: Tokens are masked with UUID placeholders (`[REDACTED_AADHAAR_01]`) before external dispatch and rehydrated locally upon response return.
2. Stage 2: Agentic Code RAG (`RetrieverAgent`):
   - Chunks repository files using semantic AST line-windows that preserve complete class and function boundaries rather than arbitrary character slicing.
   - Embeds code into a 384-dimensional dense vector space using `sentence-transformers/all-MiniLM-L6-v2`.
   - Indexes chunks into a persistent/in-memory Qdrant vector database, performing cosine similarity search (threshold > 0.70) to inject only grounded repository evidence into the prompt.
3. Stage 3: Change Impact & Blast Radius Analysis (`BlastRadiusAnalyst`):
   - Uses Python's built-in `ast` module (`ast.parse`, `ast.NodeVisitor`) to statically parse all repository files without code execution.
   - Builds a bidirectional dependency graph mapping `Import`, `ImportFrom`, `ClassDef`, `FunctionDef`, and symbol call references.
   - Computes the transitive closure reachability matrix to calculate an empirical blast-radius score (0.0 to 1.0) and alert developers if critical upstream dependencies are touched.
4. Stage 4: Dual-Engine Privacy LLM Routing (`DevOpsCoderAgent`):
   - Air-gapped privacy switch: If prompt or code contains sensitive IP, cloud APIs are disabled.
   - Public/low-risk tasks route to Google Gemini 2.5 Flash / Groq Cloud.
   - Sensitive enterprise code routes to local Ollama running `qwen2.5-coder:7b` or `llama3.2:3b` on localhost:11434 with zero internet exposure.
5. Stage 5: Supply-Chain Slopsquatting Firewall (`PackageFirewall`):
   - Intercepts generated code before compilation.
   - AST parser traverses all `Import` and `ImportFrom` nodes to extract module root names.
   - Instant local filter: checks against Python standard library (`sys.stdlib_module_names`) and local repo modules (0ms latency).
   - Live PyPI Registry Probe: For external third-party imports, queries `https://pypi.org/pypi/<pkg>/json` backed by an in-memory LRU cache (`maxsize=1024`).
   - If PyPI returns HTTP 404, the package is flagged as an AI Hallucination and the pipeline aborts immediately with a security block, preventing slopsquatting.
6. Stage 6: Autonomous Self-Healing ReAct Sandbox (`SelfHealer`):
   - Executes synthesized code inside an isolated ephemeral subprocess directory running `pytest`.
   - Strict 5.0-second CPU timeout.
   - If tests fail, captures `stderr` and traceback, constructs a structured ReAct reflection prompt ("Identify root cause in 2 sentences and patch"), and repairs code iteratively.
   - Hard bounded at N = 3 iterations to mathematically prevent infinite token exhaustion loops.
7. Open Tool Interoperability via Model Context Protocol (MCP):
   - Implements an Anthropic Model Context Protocol (MCP) server over JSON-RPC 2.0 (`mcp_server.py`).
   - Exposes `kavach_scan_security`, `kavach_get_blast_radius`, and `kavach_search_repository` directly to external IDEs (Cursor IDE, Claude Desktop, Windsurf).
8. Real-Time Telemetry & Observability Dashboard:
   - FastAPI backend with Server-Sent Events (SSE) streaming live execution stages to a dark-mode frontend dashboard (`#08090D` surface, `#00D2FF` electric cyan accents).
   - Audio input powered by Groq Whisper (`whisper-large-v3-turbo`) with Web Speech API fallback.
   - Real-time Prometheus OpenMetrics exporter (`/metrics`) and live cost calculation.

D. EMPIRICAL BENCHMARKS & TEST EVIDENCE:
• 220 automated unit and integration tests passing with 100% success rate (`pytest kavach/tests`).
• 42 persistent evaluation runs logged in `backend/data/workflow_runs.json` across 4 distinct user personas (Junior Developer, DevOps SRE, Security Auditor, CI/CD Webhook).
• Package Slopsquatting Catch Rate: 100% Precision, 100% Recall, 100% F1 (50 real packages vs 50 hallucinations).
• Credential Catch Rate: 100% detection of AWS/GitHub/Stripe keys.
• Indian Identifier PII Detection: F1 = 0.962 on multilingual Hinglish developer prompts.
• Pipeline Latency: Average 1,370 ms; all deterministic security guardrails execute in < 20 ms combined (< 2% total latency overhead).
• Autonomous Self-Healing Pass Rate: 90.0% recovery within 2 ReAct reflection cycles.

--------------------------------------------------------------------------------
3. REQUIRED OUTPUT STRUCTURE
--------------------------------------------------------------------------------

Please generate the response organized into two complete sections:

PART 1: THE FORMAL SYNOPSIS REPORT
Structure into the exact 4 headings matching Anusha Chhabra's rubrics:
- Section 1: Comprehensiveness of the Literature Review (10 Marks) — Cite 12+ seminal papers covering autonomous coding agents (SWE-agent, Devin), AI package hallucination & slopsquatting (Bar-Zik, Lazaar, Ladisa), prompt injection (OWASP, Greshake), code RAG (Lewis, Feng, Guo), AST static analysis (Aho, Ren, Lehnert), and Indian DPDP Act 2023 / EU AI Act.
- Section 2: Identified Research Gaps (5 Marks) — Formulate a detailed comparison table contrasting existing SCA tools (Snyk, Dependabot, SonarQube) and naive agents against Kavach's 5 key technical novelties.
- Section 3: Objective / Problem Definition (5 Marks) — State the acute enterprise dilemma, formal risk model, and 5 measurable research objectives with quantitative targets.
- Section 4: Proposed Methodology, Tools, Techniques & Datasets (5 Marks) — Detailed 6-stage architecture, mathematical formulas (Shannon entropy, cosine similarity, AST graph closure, risk score), tools table, and descriptions of the 3 evaluation datasets.

PART 2: THE 10-SLIDE MID-TERM PRESENTATION SCRIPT
Structure as a 10-slide deck matching the 25-mark rubrics:
- Slide 1: Title, Team Members, Guide & Academic Context
- Slide 2: Problem Definition & Enterprise Industry Dilemma (5 Marks)
- Slide 3: Literature Review Part 1 — Autonomous Agents & Supply-Chain Attacks (10 Marks)
- Slide 4: Literature Review Part 2 — Code RAG, AST Static Analysis & Privacy (10 Marks)
- Slide 5: Identified Research Gaps in State-of-the-Art (5 Marks)
- Slide 6: Research Objectives & Quantitative Target Metrics (5 Marks)
- Slide 7: Proposed Methodology — 6-Stage Governed Pipeline (5 Marks)
- Slide 8: Technical Tools, Architectural Stack & Mathematical Formulations (5 Marks)
- Slide 9: Experimental Datasets & Empirical Evaluation Results (5 Marks)
- Slide 10: Current Implementation Status (220 Tests Passing), Deliverables & Roadmap

For EACH slide, provide:
- Slide Title & Category Badge
- Visual Card Layout (structured bullet points with bold keywords)
- Speaker Cue & Verbal Script (written in first-person plural: "Dhruv, Dev, Ansh, and I...") explaining the technical intuition to Prof. Anusha Chhabra.

Write with the highest academic caliber, mathematical precision, and persuasive defense logic.
```
