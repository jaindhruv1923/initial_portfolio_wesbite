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
> 
> * **Visual Proof:** [Autonomous ReAct Reflection Loop Repair (`ss10.png`)](../kavach/artifacts/screenshots/ss10.png)

---

### Q10: "Show us evidence of your 40+ runs and persona linkages." (Slide 2 Row 5)
> **Answer:** *"We have 42 persistently logged runs stored in `backend/data/workflow_runs.json`, viewable via `GET /agent/runs` and `/observability/stats`. Each run contains complete stage transition history, latency breakdowns per agent, token costs, security findings, and explicit linkage to four target user personas: Junior Developer, DevOps Lead, Security Auditor, and Automated CI/CD Webhook."*
> 
> * **Visual Proof:** [Recorded Runs History & Telemetry (`ss7.png`)](../kavach/artifacts/screenshots/ss7.png) & [Canonical Verification Trace (`ss24.png`)](../kavach/artifacts/screenshots/ss24.png)

---

## 2. Empirical Cyber Defense & Examiner Proof Gallery

When examiners request empirical proof during the defense, cite the high-resolution evidence captured in [`important/kavach/artifacts/screenshots/`](../kavach/artifacts/screenshots/):

| Examination Defense Topic | Empirical Evidence | Visual Screenshot Link |
| :--- | :--- | :---: |
| **Full Automated Pytest Suite** | Official clean execution passing all 278 unit, integration, and security tests in 58s. | [`ss23.png`](../kavach/artifacts/screenshots/ss23.png) |
| **All 10 E2E Verifications** | Canonical `verify_project.py` verifying all 10 cyber defense engines with 100% success. | [`ss24.png`](../kavach/artifacts/screenshots/ss24.png) |
| **15-Vector Red-Team Simulator** | 19 attacks tested, 19 intercepted (100.0% interception rate) mapped to MITRE ATLAS. | [`ss15.png`](../kavach/artifacts/screenshots/ss15.png) |
| **Cryptographic Merkle Ledger** | Append-only SHA-256 Merkle root verification under India DPDP Act 2023. | [`ss16.png`](../kavach/artifacts/screenshots/ss16.png) |
| **PyPI Slopsquatting Defense** | Real-time AST import interception of phantom package `completely_fake_ai_auth_lib_9999`. | [`ss11.png`](../kavach/artifacts/screenshots/ss11.png) |
| **Autonomous ReAct Reflection** | Automatic traceback capture and candidate repair verified passing on iteration 2. | [`ss10.png`](../kavach/artifacts/screenshots/ss10.png) |
| **State-Sponsored Hacker Defense** | Interception of APT-29 / CozyBear Base64 + Unicode RLO prompt obfuscation. | [`ss19.png`](../kavach/artifacts/screenshots/ss19.png) |
| **Active Honeytoken Tripwires** | Intrusion interception and session quarantine on decoy canary AWS / JWT keys. | [`ss20.png`](../kavach/artifacts/screenshots/ss20.png) |
| **150-Vector Adversarial Matrix** | 99.3% overall interception rate across obfuscation, slopsquatting, and kernel RCE. | [`ss21.png`](../kavach/artifacts/screenshots/ss21.png) |
| **MITRE ATLAS Threat Matrix** | Standardized mapping of adversarial techniques against Kavach mathematical defenses. | [`ss22.png`](../kavach/artifacts/screenshots/ss22.png) |

