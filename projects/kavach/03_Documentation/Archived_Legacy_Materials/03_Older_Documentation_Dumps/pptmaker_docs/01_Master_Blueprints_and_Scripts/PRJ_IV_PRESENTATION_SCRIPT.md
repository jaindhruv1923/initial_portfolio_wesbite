# PRJ-IV MID-TERM PRESENTATION ORAL DEFENSE SCRIPT
**Event:** Project-IV Mid-Term Presentation (7th Semester Major Project)  
**Scheduled Date:** 29th September 2026 at 12:00 PM – 2:00 PM  
**Evaluator / Coordinator:** Prof. Anusha Chhabra  
**Team Members:** Dhruv Jain (230532), Dev Garg (230487), Ansh Rohilla (230794), Ansh Adhikari (230822)  
**Slide Deck:** [PRJ_IV_Midterm_Presentation_8_10_Slides.pptx](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/PRJ_IV_Documentation/PRJ_IV_Midterm_Presentation_8_10_Slides.pptx)  

---

## Slide-by-Slide Speaker Notes & Rehearsal Guide

### Slide 1: Title & Introduction
* **Slide Visual:** Title, Project Name "KAVACH", Subtitle, Team Names & Enrollments.
* **Speaker Script (Dhruv Jain):**
  > *"Good afternoon, Professor Anusha and faculty members. Today, my team members — Dev, Ansh Rohilla, Ansh Adhikari, and myself, Dhruv Jain — are proud to present our 7th-semester Major Capstone Project: **Kavach — A Security-Governed Multi-Agent AI DevOps & Observability Platform**.
  > As autonomous coding agents enter modern engineering workflows, they introduce unprecedented security and supply-chain vulnerabilities. Kavach is designed as an enterprise governance platform that enforces deterministic security guardrails before, during, and after autonomous agent execution."*

---

### Slide 2: Problem Definition & Industry Motivation (5 Marks)
* **Slide Visual:** Two panels showing the Industry Context and the Core Research Dilemma.
* **Speaker Script (Dhruv Jain):**
  > *"To understand why Kavach is needed, consider the current industry dilemma. Modern organizations want the speed of autonomous coding agents like Devin or SWE-agent. However, LLMs are probabilistic token predictors — they hallucinate non-existent package imports, leak credentials, and modify code without architectural dependency awareness.
  > Traditional tools like Snyk or Dependabot only scan static lockfiles after code is already committed. Meanwhile, system prompts like 'Please do not leak keys' are easily bypassed via prompt injections. Our research problem is: **How can organizations harvest autonomous agent productivity while deterministically guaranteeing zero credential leaks, zero package hallucinations, and zero unbounded regressions?**"*

---

### Slide 3: Literature Review — Part 1: Autonomous Agents & Supply-Chain Risks (10 Marks)
* **Slide Visual:** 3-column cards covering Autonomous Agents (SWE-agent/Devin), AI Package Hallucination (Bar-Zik/Lazaar), and Prompt Injection (OWASP/Greshake).
* **Speaker Script (Dev Garg):**
  > *"Turning to our literature review, we analyzed foundational research across six domains.
  > First, Yang et al. (2024) introduced SWE-agent, showing how ReAct loops solve real GitHub issues. However, they observed that unconstrained terminal tool-use regularly causes destructive edits and command injection.
  > Second, Bar-Zik (2024) and Lazaar et al. (2024) proved that LLMs frequently hallucinate third-party package names. Attackers exploit this via **'Slopsquatting'** — registering these hallucinated package names on PyPI with malicious payloads. When an agent runs `pip install`, it introduces arbitrary code execution into the enterprise build pipeline. Ladisa et al. confirmed that existing SCA tools are completely blind to runtime agent-synthesized import statements.
  > Third, the OWASP Top 10 for LLMs and Greshake et al. (2023) established that indirect prompt injection inside source code comments can hijack the agent's internal goal state."*

---

### Slide 4: Literature Review — Part 2: Static Analysis, Code RAG & Privacy (10 Marks)
* **Slide Visual:** 3-column cards covering Code RAG (Lewis/Feng/Guo), AST Analysis (Aho/Ren/Lehnert), and DPDP Act Compliance (Jain et al.).
* **Speaker Script (Dev Garg):**
  > *"Fourth, in Code RAG, Lewis et al. (2020) and Feng et al. (2020) demonstrated dense vector retrieval for source code. However, standard RAG uses blind character slicing that shatters AST function boundaries and fails to screen retrieved chunks for hardcoded credentials.
  > Fifth, static Abstract Syntax Tree analysis (Aho et al., 2006; Lehnert, 2011) provides mathematical ground truth regarding program structure. Computing the transitive closure over AST dependency graphs is essential to predict the regression blast radius before committing code.
  > Finally, under India's Digital Personal Data Protection (DPDP) Act 2023, enterprises face strict statutory liability for leaking national identifiers. Jain et al. (2023) proved that western regex scanners fail on Indian Aadhaar and PAN cards embedded in code-mixed Hinglish text."*

---

### Slide 5: Identified Research Gaps (5 Marks)
* **Slide Visual:** 5 horizontal structured cards highlighting Gaps 1 to 5 with existing flaws and Kavach solutions.
* **Speaker Script (Ansh Rohilla):**
  > *"Based on this literature, we identified five critical research gaps:
  > 1. **Absence of Pre-Execution Deterministic Guardrails:** Existing systems rely on stochastic prompt rules. Kavach introduces pre-execution Shannon entropy and compiled regex that halt requests before LLM tokenization.
  > 2. **Complete Blind Spot on Package Slopsquatting:** No existing tool intercepts agent-generated imports. Kavach builds an AST Package Firewall querying live PyPI registry APIs.
  > 3. **Missing AST Blast-Radius Grounding:** Agents modify files blindly. Kavach calculates transitive dependency graphs to quantify regression risk.
  > 4. **Lack of Closed-Loop Self-Healing Sandboxing:** Syntactically valid code fails runtime assertions. Kavach provides an ephemeral sandbox with ReAct reflection loops.
  > 5. **Closed Vendor Silos:** Existing security tools cannot connect to modern developer IDEs. Kavach natively implements Anthropic’s Model Context Protocol (MCP) as an open JSON-RPC server."*

---

### Slide 6: Research Objectives & Scope (5 Marks)
* **Slide Visual:** Primary Objectives card and Quantitative Evaluation Targets card.
* **Speaker Script (Ansh Rohilla):**
  > *"To address these gaps, we formulated five concrete objectives:
  > First, eliminate 100% of package hallucination attacks. Second, enforce a zero-knowledge pre-execution gate blocking high-entropy secrets ($H > 4.5$) and Indian identifiers. Third, formulate an AST dependency scoring algorithm. Fourth, implement a ReAct self-healing loop achieving $>90\%$ autonomous recovery. Fifth, expose all tools over Model Context Protocol.
  > Our quantitative benchmarks target 100% precision on credentials, F1 $\ge 0.95$ on PII, and an average pipeline latency under 1.5 seconds."*

---

### Slide 7: Proposed Methodology & 6-Stage Governance Pipeline (5 Marks)
* **Slide Visual:** 6-card grid illustrating the sequential execution pipeline from prompt to verified patch.
* **Speaker Script (Ansh Adhikari):**
  > *"Our proposed methodology structures agent execution into a 6-stage governed pipeline:
  > 1. **Sentinel Screening:** Computes Shannon entropy on input text and runs regex filters. If an API key or Aadhaar is detected, execution is immediately blocked or redacted.
  > 2. **Context Retrieval:** Uses Qdrant vector database with AST-aware code chunking.
  > 3. **AST Blast Radius Analysis:** Traverses Python ASTs to map affected modules.
  > 4. **Dual-Engine LLM Router:** Routes public tasks to Gemini 2.5 Flash and sensitive tasks to local air-gapped Ollama (`qwen2.5-coder:7b`).
  > 5. **AST Package Firewall:** Intercepts external imports and verifies existence on PyPI index.
  > 6. **ReAct Sandbox:** Executes unit tests in ephemeral environments, capturing stderr tracebacks to trigger automated repair cycles."*

---

### Slide 8: Tools, Techniques & Mathematical Foundations (5 Marks)
* **Slide Visual:** Tech Stack panel and Mathematical Formulations panel.
* **Speaker Script (Ansh Adhikari):**
  > *"Technologically, the platform is built on FastAPI with Server-Sent Events, Qdrant vector database, Python's built-in `ast` module, and Anthropic's MCP SDK.
  > Mathematically, we use:
  > - **Shannon Entropy:** $H = -\sum p_i \log_2 p_i$ to distinguish human text ($H \approx 2.5$) from base64/hex production credentials ($H > 4.5$).
  > - **Cosine Similarity:** To retrieve dense 384-dimensional code embeddings from Qdrant.
  > - **Transitive Graph Closure:** Reachability matrices to calculate affected downstream modules.
  > - **Risk-Adaptive Policy Scoring:** Weighting action risk, finding severity, and exposure level to emit Allow, Review, Redact, or Block decisions."*

---

### Slide 9: Experimental Datasets & Empirical Evaluation (5 Marks)
* **Slide Visual:** 4 Evaluation Datasets and Empirical Findings cards.
* **Speaker Script (Dhruv Jain):**
  > *"We evaluated Kavach across three comprehensive benchmark datasets:
  > 1. A **100-package Hallucination Corpus** (50 real packages and 50 documented LLM hallucinations), where our firewall achieved **100% Precision, 100% Recall, and 100% F1 Score** with $<5$ms latency.
  > 2. A **100-prompt Multilingual PII & Credential Corpus**, achieving F1 = 0.962 on Indian national identifiers and 100% catch rate on AWS/GitHub secrets.
  > 3. An operational dataset of **42 persistent runs** in `workflow_runs.json` across 4 user personas (Junior Developer, SRE, Auditor, CI/CD Webhook), demonstrating an average pipeline latency of **1,370 ms**, where security guardrails contribute less than 20 ms (<2% overhead)."*

---

### Slide 10: Current Status, Test Evidence & Conclusion
* **Slide Visual:** Deliverables Completed and Phase 2 Roadmap cards.
* **Speaker Script (Dhruv Jain):**
  > *"In summary, Kavach has been fully implemented with **220 automated unit and integration tests passing with 100% success rate**. We have operational REST endpoints, a standalone MCP server for Cursor and Claude IDEs, and a real-time dark-mode Mission Control dashboard.
  > In Phase 2, we will integrate enterprise PostgreSQL persistence, GitHub App OAuth authentication, and continuous pull request pre-merge gating.
  > Thank you, Professor Anusha. We are now ready for your questions."*
