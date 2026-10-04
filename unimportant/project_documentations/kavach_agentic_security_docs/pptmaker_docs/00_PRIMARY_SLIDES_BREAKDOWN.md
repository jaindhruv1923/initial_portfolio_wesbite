# 🎯 KAVACH Mid-Term Presentation Slide Breakdown & Speaker Script

**Course:** PRJ-IV (Capstone Project, B.Tech 7th Semester, Academic Year 2026–27)  
**Evaluator / Coordinator:** Prof. Anusha Chhabra  
**Date & Time:** 29/09/2026 | 12:00 PM – 2:00 PM  
**Total Target Marks:** 25 Marks  
**Slide Deck:** `KAVACH_MidTerm_Presentation.pptx` (10 Slides)

---

## ⏱️ Recommended 10-Minute Presentation Timing Breakdown

| Slide # | Slide Title | Rubric Mapped | Marks | Target Time | Presenter |
|:---:|:---|:---|:---:|:---:|:---:|
| **1** | Title & Academic Team Information | Overview | — | 0:45 min | Dhruv Jain |
| **2** | The Security Dilemma of Autonomous AI Agents | Objective / Problem Definition | 5 M | 1:15 min | Dhruv Jain |
| **3** | Literature Review: Agents & Supply Chains (Part 1) | Comprehensiveness of Lit. Review | 5 M | 1:15 min | Dev Garg |
| **4** | Literature Review: Code RAG, AST & DPDP (Part 2) | Comprehensiveness of Lit. Review | 5 M | 1:15 min | Dev Garg |
| **5** | Critical Research Gaps in State-of-the-Art | Research Gap | 5 M | 1:30 min | Ansh Rohilla |
| **6** | Research Objectives & Measurable Target Metrics | Objective / Problem Definition | 5 M | 1:00 min | Ansh Rohilla |
| **7** | Proposed Methodology: 6-Stage Governed Pipeline | Proposed Methodology | 5 M | 1:30 min | Ansh Adhikari |
| **8** | Technological Implementation & Math Formulations | Tools, Techniques & Methods | 5 M | 1:00 min | Ansh Adhikari |
| **9** | Experimental Datasets & Empirical Results | Dataset & Evaluation | 5 M | 1:00 min | Dhruv Jain |
| **10**| Implementation Status, Evidence & Phase 2 Roadmap | Deliverables & Status | — | 0:30 min | All |

---

## 🎙️ Slide-by-Slide Content & Speaker Script

### Slide 1: Title Slide — KAVACH
- **Visuals:** Deep Navy background, electric cyan headers, gold team card.
- **Presenter:** Dhruv Jain
- **Speaker Transcript:**
  > *"Good afternoon, respected Professor Anusha Chhabra and evaluators. We are presenting our 7th-semester Capstone Project for PRJ-IV titled **KAVACH: A Security-Governed Multi-Agent AI DevOps & Observability Platform**. Our team consists of Dhruv Jain, Dev Garg, Ansh Rohilla, and Ansh Adhikari. Today, we will address each of the four designated evaluation rubrics: Literature Review, Research Gap, Problem Definition, and Proposed Methodology."*

---

### Slide 2: Problem Definition & Industry Motivation (5 Marks)
- **Rubric:** Objective / Problem Definition (5 Marks)
- **Key Concepts:**
  - Unconstrained autonomous agents (Devin, SWE-agent)
  - AI Package Hallucination & Slopsquatting
  - Credential & PII exfiltration to cloud LLMs
  - Post-facto SCA blindness (Snyk/Dependabot only check static files)
- **Presenter:** Dhruv Jain
- **Speaker Transcript:**
  > *"While autonomous coding agents like Devin and SWE-agent promise 10x engineering velocity, deploying them in enterprise environments introduces catastrophic risks. Because LLMs are probabilistic token predictors, they frequently invent non-existent package names. Attackers weaponize this through 'slopsquatting'—registering these hallucinated names on PyPI with malicious payloads. Furthermore, developers inadvertently paste production AWS keys or Indian Aadhaar/PAN numbers into prompts, leaking them to third-party cloud LLM logs. Existing tools like Snyk and Dependabot only inspect static requirements.txt files post-commit. They are completely blind to dynamically synthesized imports in agent memory. KAVACH solves this with a deterministic, pre-execution governance layer."*

---

### Slide 3: Literature Review — Part 1 (10 Marks)
- **Rubric:** Comprehensiveness of Literature Review (10 Marks)
- **Citations Covered:**
  - *SWE-agent* (Yang et al., 2024), *Devin* (Cognition, 2024), *ReAct* (Yao et al., 2023)
  - *AI Package Hallucination* (Bar-Zik, 2024; Lazaar et al., 2024; Ladisa et al., 2023)
  - *LLM Security & Prompt Injection* (OWASP Top 10 for LLMs 2025; Greshake et al., 2023)
- **Presenter:** Dev Garg
- **Speaker Transcript:**
  > *"To build our theoretical foundation, we conducted a comprehensive review of over 12 landmark publications across six domains. First, analyzing autonomous coding agents: Yang et al. (2024) introduced SWE-agent's terminal-based ReAct loop, but their architecture lacks safety gates, permitting arbitrary destructive shell commands. Second, in software supply chain security, Bar-Zik (2024) and Lazaar et al. (2024) proved that LLMs regularly hallucinate dependencies, while Ladisa et al. (2023) confirmed traditional SCA tools cannot inspect runtime code. Third, OWASP 2025 and Greshake et al. (2023) established that prompt injection via code comments can hijack agent execution. Therefore, security cannot rely on prompt instructions; it must be deterministically enforced outside the LLM context."*

---

### Slide 4: Literature Review — Part 2 (10 Marks)
- **Rubric:** Comprehensiveness of Literature Review (10 Marks)
- **Citations Covered:**
  - *Code RAG* (Lewis et al., 2020; Feng et al., 2020; Guo et al., 2022)
  - *AST & Change Impact* (Aho et al., 2006; Ren et al., 2004; Lehnert, 2011)
  - *Regulatory Compliance* (Indian DPDP Act 2023; EU AI Act 2024; Jain et al., 2023)
- **Presenter:** Dev Garg
- **Speaker Transcript:**
  > *"Continuing our review, in Code RAG, Lewis et al. (2020) and Feng et al. (2020) introduced dense vector retrieval, yet standard chunking shatters AST syntactic boundaries and risks re-indexing sensitive credentials. In static analysis, Aho et al. (2006) and Ren et al. (2004) demonstrated that calculating transitive closures over Abstract Syntax Tree call graphs provides ground-truth blast-radius quantification. Finally, under the Indian DPDP Act 2023, organizations face statutory penalties for data leaks. As shown by Jain et al. (2023), Western English-only PII models fail on code-mixed Hinglish developer text and Indian identity cards. This synthesis directly drives our architectural requirements."*

---

### Slide 5: Identified Research Gaps (5 Marks)
- **Rubric:** Research Gap (5 Marks)
- **5 Critical Gaps Table:**
  1. *Absence of Pre-Execution Deterministic Guardrails* (Prompts are stochastic -> Shannon entropy + regex halting pre-tokenization).
  2. *Package Slopsquatting Blindspot* (SCA only checks lockfiles -> AST Package Firewall with live PyPI registry caching).
  3. *Missing AST Blast-Radius Grounding* (Blind modifications -> Transitive closure over function call-graph).
  4. *Lack of Closed-Loop Self-Healing Sandboxing* (Syntax pass but runtime assertion fails -> ReAct sandbox with traceback reflection).
  5. *Disconnection from Open Tool Standards* (Proprietary silos -> Native Anthropic Model Context Protocol [MCP] JSON-RPC 2.0).
- **Presenter:** Ansh Rohilla
- **Speaker Transcript:**
  > *"Through this literature review, we pinpointed five explicit research gaps in existing state-of-the-art tooling. Slide 5 presents our comparative gap matrix. Gap 1: Existing agents use system prompts for security, which fail against jailbreaks. KAVACH enforces Shannon entropy and deterministic regex filters that halt execution before the LLM is even called. Gap 2: Zero existing tools verify dynamically generated imports; KAVACH builds an AST Package Firewall querying PyPI in under 5 milliseconds. Gap 3: Agents modify code without blast-radius awareness; KAVACH computes transitive caller-callee graphs. Gap 4: Code often fails at runtime; KAVACH adds a ReAct self-healing sandbox. Gap 5: Instead of closed vendor lock-in, KAVACH exposes all capabilities over the open Model Context Protocol for seamless Cursor and Claude IDE integration."*

---

### Slide 6: Research Objectives & Measurable Target Outcomes (5 Marks)
- **Rubric:** Objective / Problem Definition (5 Marks)
- **Concrete Metrics:**
  - 100% precision and recall on hallucinated packages.
  - 100% detection of production AWS/GitHub/Stripe keys.
  - F1 Score >= 0.95 on Indian PII (Aadhaar/PAN).
  - Pipeline latency <= 1.5 seconds (<20ms security overhead).
  - >90% autonomous recovery rate in ReAct reflection loop.
  - 220+ automated unit & integration tests.
- **Presenter:** Ansh Rohilla
- **Speaker Transcript:**
  > *"To rigorously evaluate our framework, we defined five concrete research objectives paired with measurable quantitative targets. We require a 100% catch rate on hallucinated packages with zero false negatives, 100% interception of production credentials, and an F1 score above 0.95 on Indian national identifiers. Crucially, our deterministic security guards must execute in under 20 milliseconds—representing less than 2% of total pipeline latency—to ensure zero developer friction."*

---

### Slide 7: Proposed Methodology & 6-Stage Pipeline (5 Marks)
- **Rubric:** Proposed Methodology (Tools / Techniques / Methods) (5 Marks)
- **The 6 Stages:**
  1. *Sentinel Screening*: Shannon entropy + regex checks before LLM invocation.
  2. *Qdrant RAG Context*: Cosine similarity over 384-d AST-aware chunks.
  3. *AST Blast Radius*: Caller-callee graph construction to predict regressions.
  4. *Dual-Engine LLM*: Gemini 2.5 Flash API + Local Ollama (Qwen2.5-Coder:7b) routing.
  5. *AST Package Firewall*: Intercepts external imports, queries PyPI index.
  6. *ReAct Sandbox*: Ephemeral subprocess execution with stderr reflection (max 3x).
- **Presenter:** Ansh Adhikari
- **Speaker Transcript:**
  > *"Our proposed methodology organizes agent execution into a 6-stage governed pipeline. When a developer submits a prompt, Stage 1 executes Sentinel Screening. If high-entropy secrets or destructive commands like 'DROP TABLE' are detected, the request is halted immediately. In Stage 2, AST-aware code chunks are retrieved from Qdrant vector storage. In Stage 3, the AST module computes the downstream blast radius. In Stage 4, our dual-engine router dispatches public requests to Gemini 2.5 Flash and proprietary tasks to local Ollama. In Stage 5, the AST Package Firewall inspects all synthesized imports against PyPI. Finally, Stage 6 executes tests inside an ephemeral sandbox, reflecting on tracebacks if assertions fail."*

---

### Slide 8: Tools, Techniques & Algorithms (5 Marks)
- **Rubric:** Tools, Techniques & Algorithms (5 Marks)
- **Mathematical Formulations:**
  - Shannon Entropy: $H(X) = -\sum_{i=1}^{n} p(x_i) \log_2 p(x_i)$ (Threshold $H > 4.5$).
  - Risk Policy Formula: $Risk = w_1 \cdot \text{ActionRisk} + w_2 \cdot \text{FindingSeverity} + w_3 \cdot \text{ExposureLevel} \rightarrow \{\text{ALLOW, REDACT, REVIEW, BLOCK}\}$.
  - Dense Cosine Similarity: $\cos(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$.
  - Transitive Graph Reachability: Matrix multiplication $R = (I \lor A)^k$.
  - ReAct Reflection Loop: $Prompt_{k+1} = Prompt_k + Traceback_k \quad (k \le 3)$.
- **Presenter:** Ansh Adhikari
- **Speaker Transcript:**
  > *"The mathematical rigor of KAVACH is anchored in deterministic information theory and graph algorithms. For secret detection, we calculate Shannon Entropy $H(X)$ over character frequency distributions; values above 4.5 indicate cryptographically high-entropy tokens like API keys. Our risk scoring engine calculates a weighted risk metric determining whether to ALLOW, REDACT, REVIEW, or BLOCK actions. Semantic context retrieval uses cosine similarity over 384-dimensional dense vectors. Blast radius estimation computes reachability over the AST call-graph adjacency matrix, while ReAct reflection iteratively feeds captured tracebacks back to the repair engine with an upper bound of 3 iterations."*

---

### Slide 9: Experimental Datasets & Empirical Results (5 Marks)
- **Rubric:** Dataset & Empirical Evaluation (5 Marks)
- **4 Datasets & Results:**
  1. *Package Hallucination Corpus (100 pkgs)*: 100.0% Precision, 100.0% Recall (0 false negatives).
  2. *Multilingual PII Corpus (100 prompts)*: 0.990 F1 score on Hinglish PII.
  3. *Operational 42-Run Benchmark Dataset*: Average latency 1,370 ms; security overhead < 20 ms.
  4. *AST Blast-Radius Test Suite*: 100% accuracy on caller-callee regression boundaries.
- **Presenter:** Dhruv Jain
- **Speaker Transcript:**
  > *"To empirically validate our methodology, we tested KAVACH across four specialized benchmark datasets. In our 100-package Hallucination Corpus, KAVACH achieved a 100% catch rate against hallucinated and slopsquatted packages with zero false negatives. On our 100-prompt Multilingual PII Corpus containing English and Hinglish developer chats, KAVACH scored 0.990 F1, outperforming baseline regex by 139%. In our operational dataset of 42 full-lifecycle workflow runs, average pipeline latency was 1,370 milliseconds, with security overhead consuming under 20 milliseconds (<2%). Furthermore, our ReAct sandbox achieved a 90% autonomous self-repair rate within 2 iterations."*

---

### Slide 10: Implementation Status & Phase 2 Roadmap
- **Key Deliverables:**
  - 220 automated unit and integration tests passing.
  - 18 FastAPI endpoints operational.
  - Native MCP tool server for Cursor / Claude IDEs.
  - Interactive Dark-Mode Mission Control Dashboard.
  - Phase 2 roadmap: Enterprise PostgreSQL, GitHub App Webhooks, and SLSA Level 3 SBOM provenance.
- **Presenter:** All Members
- **Speaker Transcript:**
  > *"In conclusion, KAVACH successfully bridges the critical gap between autonomous developer velocity and enterprise security governance. All 220 automated unit and integration tests are passing with 100% success. We have operationalized 18 REST endpoints, an MCP server, and an interactive mission control dashboard. In Phase 2, we will expand to multi-repository dependency analysis and automated SLSA Level 3 SBOM generation. Thank you, Professor Chhabra and evaluators. We are now eager to take your questions and demonstrate our working system."*
