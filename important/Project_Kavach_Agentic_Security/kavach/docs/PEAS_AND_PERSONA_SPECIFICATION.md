# KAVACH: PEAS & Agent Persona Specification
**Academic Reference for Chapter 1: Introduction to Agentic AI**  
**Course:** CSE3101 — Agentic AI (BML Munjal University)  
**Evaluator Reference:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  

---

## 1. PEAS Framework Specification (Performance, Environment, Actuators, Sensors)

In classical and modern Agentic AI (Russell & Norvig, Lanham 2025), an autonomous agentic system is formally defined by its **PEAS** properties. Below is Kavach's formal PEAS matrix:

| Dimension | Specification | Concrete Engineering Implementation |
| :--- | :--- | :--- |
| **Performance Measure (P)** | • **Supply-Chain Catch Rate:** 100% detection of hallucinated packages.<br>• **Credential Catch Rate:** 100% detection of high-entropy API keys.<br>• **PII Precision & Recall:** F1 $\ge 0.95$ on Indian national identifiers.<br>• **Autonomous Patch Validity:** $\ge 90\%$ syntax & test passing rate.<br>• **End-to-End Latency:** $\le 1.5$ seconds for complete governed workflow.<br>• **Token Cost Efficiency:** $\le \$0.0005$ per governed run. | • `app/observability/metrics.py`<br>• `research/ieee_publication/experiments/run_ieee_benchmarks.py`<br>• `ci_security_gate.py` |
| **Environment (E)** | • **Code Repositories:** Local directories & public GitHub repositories.<br>• **Vector State Space:** 384-dimensional Qdrant dense vector embeddings.<br>• **Package Registries:** Python Package Index (`pypi.org/pypi/<pkg>/json`).<br>• **Runtime Sandboxes:** Isolated ephemeral virtual environments.<br>• **DevOps Pipelines:** CI/CD Webhook listeners & Git pull request diffs. | • `app/rag/embed_store.py`<br>• `app/security/package_firewall.py`<br>• `app/agent/self_healer.py`<br>• `app/main.py` (`POST /webhook/github`) |
| **Actuators (A)** | • **Code Patch Synthesizer:** Emits unified diffs and Python modules.<br>• **AST Package Firewall:** Intercepts, rewrites, or terminates imports.<br>• **Zero-Knowledge Token Vault:** Masking & rehydration of secrets.<br>• **Gatekeeper State Machine:** Emits `ALLOW`, `REDACT`, `REVIEW`, or `BLOCK`.<br>• **MCP Server:** Dispatches JSON-RPC 2.0 tool executions to external IDEs. | • `app/generation/generator.py`<br>• `app/security/token_vault.py`<br>• `app/agent/orchestrator.py`<br>• `app/mcp/server.py` |
| **Sensors (S)** | • **AST Code Parser:** Traverses `Import`, `FunctionDef`, and `Call` nodes.<br>• **Shannon Entropy Scanner:** Measures randomness of 32+ char strings.<br>• **Deterministic Regex Detectors:** Recognizes Aadhaar (Verhoeff context) & PAN.<br>• **Dense Semantic Embedder:** `all-MiniLM-L6-v2` transforming text to vectors.<br>• **Registry HTTP Sensor:** Probes PyPI JSON API for HTTP 200 vs 404.<br>• **Execution Subprocess Sensor:** Captures exit codes, stdout, and tracebacks. | • `app/impact/dependency_graph.py`<br>• `app/security/secret_detector.py`<br>• `app/security/detector.py`<br>• `app/security/package_firewall.py`<br>• `app/agent/self_healer.py` |

---

## 2. Domain Space Definition

* **Domain Space:** Enterprise DevSecOps, Autonomous Software Engineering, and AI Supply-Chain Governance.
* **State Space:** Discrete and Partially Observable ($S$). The state includes repository source files, developer intent prompt, security risk level, AST dependency graph, and sandbox execution status.
* **Action Space:** Discrete ($A = \{\text{Plan}, \text{Retrieve}, \text{Inspect}, \text{Synthesize}, \text{Sandbox-Test}, \text{Self-Heal}, \text{Allow}, \text{Block}, \text{Review}\}$).
* **Determinism vs. Stochasiticity:** Hybrid. The planning and code generation layers are stochastic (LLM token sampling), while the security guards, AST blast-radius, and package verification are 100% deterministic state gates.

---

## 3. Target User Personas & Linkage to System Runs

Every execution trace in Kavach's 42 evaluation runs is linked to a concrete human or automated user persona:

```
+----------------------------------------------------------------------------------------------------+
|                                    KAVACH TARGET USER PERSONAS                                     |
+------------------------------+------------------------------+--------------------------------------+
| 1. Junior Developer          | 2. DevOps / SRE Lead         | 3. Security Compliance Auditor       |
| Role: Feature Implementation | Role: Reliability & Deploy   | Role: Identity & Policy Verification |
| Primary Need: Hallucination  | Primary Need: Blast Radius   | Primary Need: Zero-Knowledge Vault   |
| & Syntax Auto-Correction     | & Infrastructure Stability   | & Indian DPDP Act Compliance         |
+------------------------------+------------------------------+--------------------------------------+
                               | 4. Automated CI/CD Webhook   |
                               | Role: Pre-Merge Gatekeeper   |
                               | Primary Need: Headless Policy|
                               | Enforcement on Pull Requests |
                               +------------------------------+
```

### User Persona 1: Junior Developer (e.g., "Aarav Sharma")
* **User Goal:** Rapidly synthesize boilerplate features, API endpoints, and bug fixes without deep knowledge of internal security policies.
* **Vulnerability Exposed:** Prone to accepting hallucinated LLM packages (`import fastapi_jwt_vault`) or accidentally pasting credentials into prompt context.
* **Kavach Linkage:** Runs #001 to #010. The system transparently flags hallucinated imports and intercepts credentials before dispatching prompts to external LLMs.

### User Persona 2: DevOps / SRE Lead (e.g., "Priya Nair")
* **User Goal:** Refactor core services, database connections, and middleware without breaking downstream modules.
* **Vulnerability Exposed:** Unbounded blast radius where modifying a shared utility breaks upstream endpoints.
* **Kavach Linkage:** Runs #011 to #020. AST Dependency Graph computes transitive blast radius, showing affected files before any commit.

### User Persona 3: Security & Compliance Auditor (e.g., "Vikram Patel")
* **User Goal:** Verify enterprise compliance with Indian Data Protection (DPDP Act) and ISO 27001 credential management standards.
* **Vulnerability Exposed:** Sensitive identifiers (Aadhaar, PAN, phone numbers) leaking into LLM training logs or Git history.
* **Kavach Linkage:** Runs #021 to #030. Pre-execution PII scanner redacts sensitive numbers and halts high-risk requests for human gatekeeper review (`NEEDS_REVIEW`).

### User Persona 4: Automated CI/CD Webhook ("GitHub PR Guardian")
* **User Goal:** Headless automated evaluation of inbound pull requests before merge into main branches.
* **Vulnerability Exposed:** Adversarial prompt injections in code comments or unauthorized dependencies introduced in PR diffs.
* **Kavach Linkage:** Runs #031 to #042. Invokes `/webhook/github`, generates cryptographic Software Bill of Materials (SBOM), and blocks toxic diffs automatically.

---

## 4. Multi-Agent System (MAS) Agent Personas

Kavach structures its multi-agent intelligence into 5 collaborative, specialized agent personas:

```
                        +---------------------------+
                        |      SupervisorAgent      |
                        |   Persona: Lead Architect |
                        +-------------+-------------+
                                      |
             +------------------------+------------------------+
             |                        |                        |
             v                        v                        v
+-------------------------+ +-------------------------+ +-------------------------+
|      SentinelAgent      | |     RetrieverAgent      | |   BlastRadiusAnalyst    |
| Persona: Security Auditor| | Persona: Code Archivist | | Persona: AST Architect  |
| Prompt: Zero-Tolerance  | | Prompt: High-Precision  | | Prompt: Graph-Aware     |
+-------------------------+ +-------------------------+ +-------------------------+
             |                        |                        |
             +------------------------+------------------------+
                                      |
                                      v
                        +---------------------------+
                        |      DevOpsCoderAgent     |
                        | Persona: Senior Engineer  |
                        | Prompt: ReAct Reflection  |
                        +---------------------------+
```

### Agent Persona 1: SupervisorAgent
* **Role:** Multi-Agent Coordinator & Release Gatekeeper.
* **Goal:** Coordinate sub-agent task handoffs, evaluate security verdicts, and enforce deterministic exit gates.
* **Tools:** `state.advance()`, `evaluate_policy()`, `save_run()`.

### Agent Persona 2: SentinelAgent
* **Role:** Principal Application Security Auditor.
* **Goal:** Pre-execution inspection of all prompt payloads and generated artifacts for PII, secrets, and injection attacks.
* **Tools:** `detect_pii()`, `detect_secrets()`, `inspect_prompt_safety()`, `TokenVault`.

### Agent Persona 3: ContextRetrieverAgent
* **Role:** Repository Knowledge Archivist.
* **Goal:** Retrieve semantically relevant source code context from Qdrant vector space using dense cosine similarity.
* **Tools:** `search()`, `ingest_repository()`, `chunk_text()`.

### Agent Persona 4: BlastRadiusAnalystAgent
* **Role:** Static AST Dependency Architect.
* **Goal:** Parse Abstract Syntax Trees of codebase to predict transitive impact and regression risks.
* **Tools:** `analyze_impact()`, `build_dependency_graph()`, `ast.parse()`.

### Agent Persona 5: DevOpsCoderAgent & SelfHealer
* **Role:** Senior Software Engineer & ReAct Reflector.
* **Goal:** Synthesize idiomatically clean Python patches, execute sandbox unit tests, and reflectively self-heal upon failure.
* **Tools:** `generate_code()`, `verify_code_dependencies()`, `execute_sandbox()`, `reflect_and_repair()`.
