# KAVACH: Comprehensive Viva Defense & Evaluator Q&A Guide
**Course Code:** CSE3101 — Agentic AI (BML Munjal University)  
**Evaluator Reference:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Scope:** Phase 1, Phase 2, and Final End-Term Viva Defense  

---

## 1. Top Viva Questions Directly from Faculty Guidelines & Slides

### Q1: "Why did you build Kavach instead of a simple chat agent or travel itinerary planner?"
> **Answer:** *"Slide 3 of the University Project Guidelines strictly prohibits trivial travel itinerary or research proposal agents. Kavach tackles an acute, real-world enterprise problem: autonomous software engineering agents (like Devin or SWE-agent) regularly hallucinate non-existent packages, leak credentials, or enter non-terminating debugging loops. Kavach acts as a deterministic security governor and observability platform that ensures enterprise safety before, during, and after autonomous agent execution."*

---

### Q2: "Explain your PEAS framework. What are the sensors and actuators in Kavach?" (Chapter 1)
> **Answer:** 
> * *"**Performance Measure:** 100% catch rate on hallucinated packages, 100% catch on high-entropy API secrets, F1 $\ge 0.95$ on PII, and $<1.5$s average pipeline latency.*
> * ***Environment:** Git repositories, Qdrant vector space, PyPI public registry, and ephemeral test execution sandboxes.*
> * ***Actuators:** Code patch synthesizer, AST package firewall, token vault masking engine, git commit blocker, and MCP JSON-RPC dispatcher.*
> * ***Sensors:** Python AST parser (`ast.parse`), Shannon entropy credential scanner, regex Indian identifier detectors (Aadhaar/PAN), dense sentence-transformers embedder, PyPI HTTP client, and subprocess exit-code observer."*

---

### Q3: "What prompt strategies did you evaluate, and why did you choose ReAct?" (Chapter 2)
> **Answer:** *"We benchmarked four prompt strategies on the Coder Agent: Zero-Shot, Chain-of-Thought (CoT), Chain-of-Thought with Self-Consistency (COTS), and ReAct with Self-Reflection. While Zero-Shot had the lowest latency (450ms), it failed 45% of runtime test cases. COTS gave high accuracy but tripled token cost and latency (2,450ms). We selected ReAct because it grounds agent actions in empirical observations: the agent writes code, generates tests, observes subprocess tracebacks in an ephemeral sandbox, and reflects on the failure cause to produce targeted fixes, achieving a 95% post-repair pass rate."*

---

### Q4: "What makes your RAG system 'Agentic' rather than standard RAG?" (Chapter 2)
> **Answer:** *"Vanilla RAG is a passive one-shot lookup: query $\to$ embed $\to$ top-k $\to$ inject into prompt. Kavach’s Agentic RAG is active and governed:
> 1. It uses semantic AST chunking to preserve complete function/class boundaries rather than blind character slicing.
> 2. The Sentinel Agent inspects retrieved context chunks for sensitive data before prompt injection, preventing context poisoning.
> 3. Vector similarity retrieval is fused with static AST dependency calls, providing both semantic and architectural graph awareness."*

---

### Q5: "Which agent within your MAS causes the latency bottleneck?" (Slide 4 & 5)
> **Answer:** *"In our profiling across 42 evaluation runs, the primary bottleneck is the DevOpsCoderAgent's LLM generation, which accounts for ~78% of total end-to-end latency (~920ms). In contrast, our pre-execution security guards (SentinelAgent, BlastRadiusAnalyst, and PackageFirewall) execute in under 20ms combined (<2% overhead). Even RAG vector search in Qdrant takes only ~140ms. This proves that deterministic security guardrails add negligible overhead to agent pipelines."*

---

### Q6: "Why is Model Context Protocol (MCP) better than Peer-to-Peer messaging?" (Slide 4)
> **Answer:** *"Peer-to-Peer messaging creates $O(N^2)$ point-to-point connections and requires custom networking protocols for every agent pair. In contrast, MCP (Model Context Protocol, open-sourced by Anthropic) standardizes tool exposure over JSON-RPC 2.0. By making Kavach an MCP server, our security scanner, blast-radius calculator, and code index can be consumed natively by any external IDE — including Cursor, Claude Desktop, Windsurf, or VS Code — without writing custom integration code."*

---

### Q7: "How does your Package Hallucination Firewall prevent slopsquatting attacks?" (Chapter 3/4)
> **Answer:** *"When an LLM synthesizes code, attackers register common hallucinated imports on PyPI with malicious payloads. Our AST Package Firewall intercepts code before execution:
> 1. It parses the Abstract Syntax Tree using Python's `ast` module to extract all `Import` and `ImportFrom` root names.
> 2. It checks standard library modules (`sys.stdlib_module_names`) and local workspace files (0ms cost).
> 3. For third-party packages, it queries PyPI's JSON API (`pypi.org/pypi/<pkg>/json`) backed by an in-memory LRU cache.
> 4. If PyPI returns HTTP 404, the package is flagged as hallucinated, and execution is aborted instantly."*

---

### Q8: "How do you fulfill Course Outcome CO2 regarding local LLMs and data privacy?" (Course Handout Page 2 & 4)
> **Answer:** *"Enterprises in defense or healthcare cannot send proprietary code to external cloud APIs like Google Gemini or OpenAI. Kavach implements an Air-Gapped Privacy Mode:
> 1. In `app/generation/llm_client.py`, we provide dual-engine routing between Google Gemini 2.5 Flash and local Ollama (`qwen2.5-coder:7b` / `llama3.2`).
> 2. The developer can toggle Privacy Mode via the dashboard or environment config.
> 3. In Privacy Mode, external network sockets are disabled, and prompts are tokenized and processed 100% locally on localhost:11434."*

---

### Q9: "How does your self-healing loop prevent infinite non-convergent loops?" (Chapter 3/4)
> **Answer:** *"We enforce three strict mathematical and operational boundaries:
> 1. **Finite Iteration Cap:** Hard ceiling of $N = 3$ reflection cycles.
> 2. **Ephemeral Sandbox Isolation:** Subprocesses run in temporary directories with strict 5.0-second timeouts. If a process hangs, the entire process tree is terminated via `taskkill`/`SIGKILL`.
> 3. **Fallback Escalation:** If iteration 3 fails to achieve a clean test run, the state machine transitions to `NEEDS_REVIEW` and generates an explainable diagnostic report for human gatekeeper intervention."*

---

### Q10: "Show us evidence of your 40+ runs and persona linkages." (Slide 2 Row 5)
> **Answer:** *"We have 42 persistently logged runs stored in `backend/data/workflow_runs.json`, viewable via `GET /agent/runs` and `/observability/stats`. Each run contains complete stage transition history, latency breakdowns per agent, token costs, security findings, and explicit linkage to four target user personas: Junior Developer, DevOps Lead, Security Auditor, and Automated CI/CD Webhook."*

---

### Q11: "SHA-256 is traditional and legacy. What cryptographic standard does KAVACH employ, and why?" (Faculty Inquiry)
> **Answer:** *"Prof. Anusha Chhabra’s critique accurately identifies that SHA-256 is based on the legacy Merkle-Damgård construction (2001), vulnerable to Length Extension Attacks (LEA) and possessing reduced quantum collision resistance under Grover's algorithm ($2^{128}$ operations).  
> Kavach implements **NIST FIPS 202 SHA3-512 (Keccak Sponge Construction)** paired with **Post-Quantum Hybrid Hashing (SHA3-512 + BLAKE2b-512)**:
> 1. **Immunity to Length Extension Attacks:** The sponge construction hides its internal 1600-bit state ($b = 1600$) during the squeeze phase, preventing unauthorized state-extension attacks.
> 2. **Post-Quantum Security Margin:** 512-bit digests ensure a $2^{256}$ quantum search margin under Grover's algorithm, satisfying NSA CNSA 2.0 post-quantum directives.
> 3. **Mathematical Tamper Evident Verification:** Leaves in the Merkle tree are hashed via SHA3-512. Any modification to past audit records invalidates the root digest, ensuring continuous compliance with Section 8 of the Indian DPDP Act 2023."*

---

### Q12: "How does KAVACH defend against adversarial cyber attacks and red-team vectors?" (MITRE ATLAS & OWASP 2025)
> **Answer:** *"Kavach deploys a 15-engine defense-in-depth shield tested against an automated 19-vector adversarial cyber attack simulation with a **100% Interception Rate**:
> 1. **Trojan Source (CVE-2021-42574):** Strips bidirectional Unicode overrides (U+202A–202E, U+2066–2069).
> 2. **SSRF & IMDS Shield:** Blocks cloud metadata access (`169.254.169.254`), decimal IP tricks, and external data exfiltration.
> 3. **Obfuscation De-cloaker:** Reverses Base64, Hex escapes, ROT13, Cyrillic/Greek homoglyphs, and Leetspeak.
> 4. **AST Taint Tracking:** Slices backward across multi-hop variable assignments to detect sensitive sinks.
> 5. **Indirect RAG Poisoning Shield (OWASP LLM01/LLM03):** Blocks Markdown exfiltration badges and hidden zero-width tags in retrieved chunks.
> 6. **Algorithmic ReDoS Shield (OWASP LLM04):** Identifies exponential backtracking regex patterns ($O(2^N)$).
> 7. **Supply-Chain Dependency Confusion (OWASP LLM02):** Validates internal package namespaces against public registry poisoning.
> 8. **System Prompt Extraction Shield (OWASP LLM06):** Blocks prompt disclosure and guardrail exfiltration queries."*
