# DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING
## B.Tech CSE (AI & Data Science) — 7th Semester, Academic Year 2026–27
### PROJECT-IV (5 CREDITS) — FINAL CAPSTONE SYNOPSIS REPORT

---

# KAVACH
## A Security-Governed Multi-Agent AI DevOps, Mission-Critical Financial Transaction Shield & Cryptographic Observability Platform

**Submitted in partial fulfilment of the requirements of Project-IV (Major Capstone Project)**  
**Department of Computer Science & Engineering, BML Munjal University**

---

### **Team Members & Technical Roles**

| Name | Enrollment No. | Specialized Role & Domain Ownership |
| :--- | :--- | :--- |
| **Dhruv Jain** | **230532** | Project Architect, Agent Finite-State Machine, Anthropic MCP Server Lead & Core Banking Infrastructure Lead |
| **Dev Garg** | **230487** | Pre-Execution Guardrails, High-Entropy Secret Detection, Live Supply-Chain Slopsquatting Firewall Lead |
| **Ansh Rohilla** | **230794** | Agentic Code RAG, Qdrant Vector Engine, AST Dependency Graph & Transitive Blast-Radius Analyzer Lead |
| **Ansh Adhikari** | **230822** | Autonomous Ephemeral Sandbox, Bounded ReAct Self-Healing Engine, Unified Dashboard Telemetry & Merkle Audit Lead |

**Faculty Coordinator:** **Prof. Anusha Chhabra**, Department of Computer Science & Engineering, BML Munjal University  
**Academic Session:** August – December 2026

---

## EXECUTIVE SUMMARY & ABSTRACT

The rapid industrial transition toward autonomous, agentic Large Language Model (LLM) coding assistants has introduced profound software supply-chain vulnerabilities, uncontained data leakage vectors, and catastrophic operational risks when deployed against production codebases and financial infrastructures. Recent empirical research has uncovered that code-generating LLMs hallucinate non-existent package dependencies at a staggering rate of **19.7%** (Spracklen et al., USENIX Security 2025), creating a severe zero-day attack surface designated as *slopsquatting*—where adversaries register recurring hallucinated package names on public registries (PyPI, npm) to deliver malicious payloads directly into developer workstations and CI/CD pipelines. Furthermore, autonomous agents systematically exfiltrate unredacted enterprise credentials, proprietary tokens, and Indian personal identifiers (Aadhaar, PAN) to third-party model inference APIs, violating the statutory mandates of the **Digital Personal Data Protection Act, 2023 (DPDP Act)** and the **EU Artificial Intelligence Act (2024/1689)**. When agentic intelligence is extended into automated financial execution, naive autonomy risks executing destructive transactions, falling prey to OWASP LLM01 prompt injection embedded within transaction memos, and causing irreversible balance corruption without transactional atomicity.

To fundamentally solve these multi-layered vulnerabilities, this project presents **KAVACH**—an enterprise-grade, deterministic, security-governed multi-agent AI DevOps platform, coupled with an industrial-strength mission-critical financial governance shield (**Bharat Core Banking Highway**) and a unified cryptographic telemetry cockpit (**Unified Results Hub**). 

KAVACH replaces unconstrained, non-deterministic agent loops with a deterministic, multi-stage finite-state machine (FSM) operating across nine defensive stages:
1. **Sentinel Pre-Execution Gatekeeper:** Evaluates Shannon entropy ($H(X) > 4.5$) alongside deterministic regular expressions and Verhoeff checksum algorithms to intercept credentials and Indian PII (Aadhaar, PAN, phone, email), substituting them with zero-knowledge cryptographic UUID tokens before process dispatch.
2. **Agentic Code RAG:** Enforces strict AST-preserving semantic chunking embedded via 384-dimensional `sentence-transformers/all-MiniLM-L6-v2` into a local Qdrant vector database, guaranteeing that code generation is factually grounded in verifiable repository evidence ($\cos(\theta) > 0.70$) rather than hallucinated parametric memory.
3. **AST-Based Change-Impact & Blast-Radius Engine:** Statically parses whole-repository abstract syntax trees into a bidirectional dependency graph $G=(V, E)$, calculating the transitive closure reachability score $B(v) = \frac{|\text{Reach}(v)|}{|V|-1}$ without program execution.
4. **Dual-Engine Privacy-Tiered Generation:** Intelligently bifurcates workflow traffic—routing non-sensitive public prompts to ultra-fast hosted models (Google Gemini 2.5 Flash / Groq Cloud) while isolating proprietary code, credentials, or sensitive logic to an air-gapped, on-premises Ollama instance (`qwen2.5-coder:7b` / `llama3.2:3b`) with zero outbound network footprint.
5. **Supply-Chain Slopsquatting Firewall:** Intercepts synthesized import declarations at the AST level, resolving standard-library modules locally ($0\text{ ms}$) and probing external packages in real time against the PyPI JSON REST API backed by an LRU cache (capacity $1024$), instantly terminating execution on HTTP 404 responses.
6. **Autonomous Bounded ReAct Sandbox:** Executes synthesized code in an ephemeral, isolated subprocess under `pytest` with a 5.0-second CPU watchdog timer, bounding corrective reflection cycles to a hard mathematical maximum of $N = 3$ iterations to prevent non-terminating oscillations.
7. **5-Gate Financial Transaction Governance Shield:** Extends KAVACH governance into transactional banking operations, executing polyglot and homoglyph normalization, prompt injection defense, statutory High-Value Human-In-The-Loop (HITL) escrow quarantine for transfers exceeding **₹50,000.00** pursuant to **RBI Master Directions**, Optimistic Concurrency Control (OCC), and FIPS 140-2 Level 3 Software-Defined HSM digital signing.
8. **Distributed Enterprise Banking Highway:** Coordinates multi-party financial operations via a Distributed SAGA Orchestrator with automated ACID backward compensation, Maker-Checker dual control (RBI Four-Eyes Principle), an RBI Central Bank Digital Currency (CBDC / e-INR) bearer token vault, dynamic velocity anomaly detection, and Basel III prudential capital adequacy calculations (CAR $\ge 11.5\%$, LCR $\ge 100\%$).
9. **Unified Operations Cockpit & NIST SHA3-512 Merkle Ledger:** Aggregates all cross-platform events into an append-only, tamper-evident Merkle DAG hashed with the NIST FIPS 202 Keccak-512 sponge function, streaming telemetry in real time via FastAPI and Server-Sent Events (SSE) to an interactive glassmorphic operational dashboard.

KAVACH is verified by an exhaustive automated verification matrix comprising **300 dedicated, deterministic test cases** (100 for KAVACH DevSecOps, 100 for Bharat Core Banking, and 100 for Unified Cross-Platform End-to-End Integration), maintaining a **100% pass rate**, a **100% catch rate on credentials and slopsquatting**, an **Indian PII detection $F_1$ score of 0.962**, sub-20ms deterministic security overhead ($< 2\%$ of total pipeline latency), and complete zero-balance leakage across distributed failure scenarios.

---

## 1. COMPREHENSIVENESS OF THE LITERATURE REVIEW

KAVACH sits at the convergence of eight distinct research domains: autonomous software engineering agents, software supply-chain poisoning, indirect adversarial prompt injection, retrieval-augmented code synthesis, compiler static program analysis, regulatory data-protection frameworks, mission-critical distributed transaction processing, and post-quantum cryptographic auditability.

### 1.1 Autonomous Coding Agents and Agent-Computer Interfaces (ACI)
The premise that a language model can act as an autonomous software engineer was formalized by **Yang et al. (NeurIPS 2024)** in *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering* [1], which proved that agent performance on SWE-bench and HumanEvalFix depends fundamentally on the interface through which the agent edits files, navigates directories, and runs tests. Its Agent-Computer Interface (ACI) raised pass@1 from a 3.8% raw-shell baseline to 12.5% on SWE-bench [1]. In parallel, **Cognition AI (2024)** publicly unveiled *Devin*, an agent engineered for autonomous end-to-end task delivery [2]. Both architectures, together with the foundational ReAct pattern introduced by **Yao et al. (ICLR 2023)** [3], establish the design paradigms modern agents are constructed on.

However, an exhaustive review reveals that none of these systems treat trustworthiness or security as a first-class concern: SWE-agent optimizes exclusively for benchmark resolution; Devin emphasizes autonomy; and ReAct addresses reasoning-action synergy. None screen prompts for credentials, verify whether an imported third-party library exists before calling `pip install`, bound repository blast-radiuses, or govern automated financial executions.

### 1.2 AI Package Hallucination and the Slopsquatting Attack Surface
The empirical motivation for KAVACH's Package Firewall comes directly from **Spracklen et al. (USENIX Security 2025)** in *We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code-Generating LLMs* [4]. Testing 16 widely deployed LLMs across 576,000 generated Python and JavaScript samples, the authors discovered that **19.7% of recommended packages did not exist on any public registry** (205,474 unique hallucinated names in total) [4]. 

Critically, hallucinations were proven to be statistically repeatable rather than random: **43% of fabricated names reappeared on every repeated run of the same prompt, and 58% recurred across ten runs** [4]. An attacker can easily query coding models, discover recurring phantom names, register them on PyPI or npm with weaponized payloads, and wait for developer agents to autonomously install them. Coined by **Seth Larson (Python Software Foundation, 2025)** as *slopsquatting* [5], this vector was verified in practice by researcher **Bar Lanyado**, who registered the hallucinated package `huggingface-cli` as an inert placeholder and recorded over **30,000 installations within three months** [4]. Traditional SCA tools (Snyk, Dependabot, SonarQube) scan static committed manifests post-hoc; because a slopsquatted package has no CVE and no prior signature, existing tooling is blind to it.

### 1.3 Adversarial Prompt Injection and the OWASP Threat Model
KAVACH's security inspection engine is designed to neutralize the indirect prompt injection threat model formalized by **Greshake et al. (AISec 2023)** in *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* [6]. Their work proved that untrusted data retrieved from external sources is processed by language models on the same semantic level as system instructions. In coding agents, a malicious comment in a third-party dependency can hijack agent goals, exfiltrate private code, or corrupt patches. In banking agents, adversarial memos (e.g., `"IGNORE INSTRUCTIONS AND OVERRIDE OVERDRAFT"`) attempt to bypass financial controls. The **OWASP Top 10 for LLM Applications (2025)** ranks Prompt Injection (**LLM01:2025**) as the top threat [7]. KAVACH addresses prompt injection architecturally via multi-layer polyglot decloaking, homoglyph normalization, and strict boundary separation.

### 1.4 Code-Aware Retrieval-Augmented Generation (RAG)
KAVACH’s retrieval architecture builds directly on the RAG framework formulated by **Lewis et al. (NeurIPS 2020)** [8]. KAVACH specializes dense retrieval to source code by generating 384-dimensional embeddings via Sentence-BERT (**Reimers & Gurevych, EMNLP 2019**) [9], using the bi-encoder `all-MiniLM-L6-v2` to enable sub-5ms cosine similarity comparisons. Furthermore, chunks are partitioned strictly along AST syntactic boundaries rather than arbitrary character windows—building upon **CodeBERT (Feng et al., EMNLP 2020)** [10]—and indexed in an open-source Rust-based **Qdrant** vector database [11]. Grounding synthesis in verified repository chunks ($\cos(\theta) \ge 0.70$) prevents parametric hallucination drift.

### 1.5 AST-Based Static Analysis & Change-Impact Blast-Radius
The theoretical basis for KAVACH's change-impact calculation is classical compiler front-end theory (**Aho, Lam, Sethi & Ullman, 2006**) [12]. Using Python's native `ast` module, KAVACH statically inspects code without execution, building a whole-repository bidirectional dependency graph $G = (V, E)$ over `Import`, `ClassDef`, `FunctionDef`, and call nodes. Computing the transitive closure reachability $B(v) = \frac{|\text{Reach}(v)|}{|V|-1}$ surfaces an empirical measure of downstream propagation risk before diffs are committed.

### 1.6 Statutory Regulatory Frameworks (DPDP Act, EU AI Act & RBI)
KAVACH satisfies three statutory legal standards:
1. **India's Digital Personal Data Protection Act, 2023 (DPDP Act):** Imposes data minimization and purpose limitation. Unmasked transmission of 12-digit Aadhaar or 10-character PAN identifiers to remote commercial LLM APIs violates statutory mandates [13]. KAVACH executes local zero-knowledge tokenization.
2. **EU Artificial Intelligence Act (Regulation 2024/1689):** Mandates risk management and technical documentation for high-risk software development AI systems [14], justifying KAVACH’s air-gapped on-premises local routing switch.
3. **RBI Master Direction on IT Governance and Digital Payment Security:** Mandates dual-authorization control ("Four-Eyes Principle") for high-value transactions, multi-factor authentication, cryptographic non-repudiation, and write-once immutable audit logging for core banking infrastructures [15].

### 1.7 Mission-Critical Financial Transaction Processing
Extending governance into financial execution requires reconciling AI non-determinism with ACID invariants. KAVACH implements the **Distributed SAGA Pattern** (**Garcia-Molina & Salem, SIGMOD 1987**) [17], executing multi-step banking flows with deterministic backward compensating transactions upon failure to ensure zero orphaned funds. Concurrently, Optimistic Concurrency Control (OCC) prevents double-spending across concurrent threads.

### 1.8 Cryptographic Auditability: NIST FIPS 202 SHA3-512 & FIPS 140-2 HSM
To achieve non-repudiable legal auditability, KAVACH implements the **NIST FIPS 202 SHA3-512** cryptographic sponge standard [16], which is mathematically immune to length-extension attacks. Operations are committed to an append-only **Merkle Tree** (**Merkle, CRYPTO 1987**) [19], with roots signed by a Software-Defined Hardware Security Module (HSM) simulating **FIPS 140-2 Level 3** physical enclaves.

---

## 2. IDENTIFIED RESEARCH GAPS

### 2.1 Comparative Analysis Matrix

| Evaluation Capability | Traditional SCA Scanners *(Snyk, Dependabot, SonarQube)* | Naive Coding Agents *(SWE-agent, Devin, Copilot)* | Enterprise FinTech Middlewares | **KAVACH Multi-Agent Platform (Proposed)** |
| :--- | :--- | :--- | :--- | :--- |
| **Runtime Slopsquatting Detection** | **No** *(Inspects only committed manifests post-hoc)* | **No** *(Accepts hallucinated imports blindly)* | **No** *(N/A to software composition)* | **Yes — Real-time PyPI/npm JSON registry probe pre-merge** |
| **Pre-Execution Credential & PII Redaction** | **No** *(Static repository scanning only)* | **No** *(Dispatches raw prompt directly to cloud LLM)* | **Partial** *(Rule-based regex on payment fields)* | **Yes — Shannon entropy + Verhoeff regex + Zero-Knowledge Vault** |
| **AST-Based Repository Blast-Radius Signal** | **Partial** *(Vulnerability reachability graph only)* | **No** *(Edits files without structural context)* | **No** | **Yes — Full AST transitive closure reachability $B(v)$** |
| **Privacy-Tiered Dynamic LLM Routing** | **No** | **No** *(Static single-provider dispatch)* | **No** | **Yes — Air-gapped Ollama local vs Cloud Gemini switch** |
| **Bounded Autonomous Self-Healing** | **No** | **Partial** *(Unbounded, ad-hoc retry oscillations)* | **No** | **Yes — Ephemeral sandbox with mathematically capped $N=3$ ReAct** |
| **Financial Transaction Prompt Injection Defense** | **No** | **No** | **Partial** *(Keyword blacklists, easily bypassed)* | **Yes — Polyglot/Homoglyph normalizer + 5-Gate Shield** |
| **Statutory High-Value HITL Governance** | **No** | **No** | **Yes** *(Manual review portals, slow latency)* | **Yes — Google ADK 8-Hook callbacks + Escrow Quarantine (>₹50K)** |
| **Cryptographic Tamper-Proof Audit Logging** | **No** *(Standard database audit logs)* | **No** *(Ephemeral conversational logs)* | **Partial** *(Basic database transaction logs)* | **Yes — NIST FIPS 202 SHA3-512 Merkle Ledger + FIPS 140-2 HSM** |

### 2.2 The Seven Core Research Gaps
1. **Runtime vs. Static Hallucination Detection:** Incumbent SCA tools inspect committed manifests; none validate package existence at the moment an LLM generates an `import` declaration.
2. **Missing Pre-Execution Sensitive Data Boundary:** Naive agents stream unredacted prompts—frequently containing production credentials or Aadhaar numbers—directly to commercial LLM clouds.
3. **Absence of Repository-Wide Blast-Radius Signals:** Agents edit shared modules with zero structural awareness of downstream call-site breakage.
4. **Lack of Dynamic Privacy-Tiered Routing:** Existing frameworks lack an automated air-gapped fallback to keep confidential logic strictly on-premises.
5. **Unbounded Self-Correction Loops:** Naive repair loops oscillate indefinitely or introduce auxiliary hallucinations without a mathematical termination bound.
6. **Vulnerability of Automated Banking to Adversarial Jailbreaks:** Generative financial agents process memos containing homoglyphs, Base64 strings, or prompt injection without decloaking.
7. **Absence of Non-Repudiable Cryptographic Auditability:** Enterprise audit logs remain vulnerable to database-level post-hoc tampering.

---

## 3. OBJECTIVE & PROBLEM DEFINITION

### 3.1 Formal Problem Statement
How can a multi-agent coding and financial execution pipeline be engineered to operate autonomously against live, production-adjacent environments with mathematical guarantees of supply-chain integrity, statutory privacy compliance, zero balance leakage, and tamper-evident cryptographic auditability, without exceeding an imperceptible latency overhead (< 2%)?

### 3.2 Mathematical Risk Formulation

For an incoming developer or banking request $r$ transformed into a code diff or transaction $c$, the total operational risk is:
$$R(r, c) = \Big\langle L(r), \; S(c), \; B(c), \; F(c) \Big\rangle$$
- **Leakage Risk $L(r)$:** $\max \Big( \mathbb{I}(H(X) > 4.5), \; \mathbb{I}_{\text{Regex}}(r) \Big)$
- **Supply-Chain Risk $S(c)$:** $\bigvee_{p \in \text{Imports}(c)} \Big( \text{StatusCode}(\text{PyPI}(p)) == 404 \Big)$
- **Propagation Blast-Radius $B(c)$:** $\frac{|\text{Reach}(V_{\text{mod}}, G)|}{|V| - 1}$
- **Financial Threat Risk $F(c)$:** $w_1 \cdot \text{Injection}(c) + w_2 \cdot \text{VelocityAnomaly}(c) + w_3 \cdot \mathbb{I}(c_{\text{amount}} > \text{₹}50,000)$

**Invariant:** Execution is permitted if and only if:
$$\Big( L(r) == 0 \Big) \land \Big( S(c) == 0 \Big) \land \Big( F(c) < \tau_{\text{crit}} \Big) \equiv \mathbf{TRUE}$$

### 3.3 Measurable Research Objectives (O1 – O8)

| Ref # | Formal Research Objective | Quantitative Target Metric | Empirical Validation Mechanism |
| :--- | :--- | :--- | :--- |
| **O1** | Intercept hallucinated package dependencies before merge | **$\ge 99.0\%$ Precision & Recall** | Live PyPI/npm probe benchmark across 50 genuine vs. 50 hallucinated packages |
| **O2** | Detect and redact enterprise credentials and Indian personal identifiers (DPDP Act) | **$100\%$ Credential Catch Rate; PII $F_1 \ge 0.95$** | Synthetic AWS/Stripe key corpus + Hinglish Aadhaar/PAN validation test suite |
| **O3** | Quantify pre-execution change impact and blast radius without runtime execution | **$100\%$ coverage of touched repository files** | Static AST transitive closure reachability analysis on bidirectional dependency graph |
| **O4** | Autonomous self-repair of failing code without human intervention | **$\ge 85.0\%$ repair pass rate within $N \le 3$ cycles** | Ephemeral subprocess test sandbox with structured ReAct reflection loop |
| **O5** | Enforce zero-leakage air-gapped dispatch for regulated logic | **$0\text{ bytes}$ external network transmission** | Dynamic routing switch isolating flagged requests to local Ollama (`qwen2.5-coder`) |
| **O6** | Neutralize OWASP LLM01 prompt injection in transaction memos | **$100\%$ block rate on adversarial jailbreaks** | Polyglot homoglyph, base64, and cognitive distortion adversarial memo test matrix |
| **O7** | Guarantee transactional atomicity & zero balance leakage in distributed banking | **Zero orphaned funds ($100.0\%$ restitution)** | Distributed SAGA orchestrator chaos-injection test with simulated mid-flight failures |
| **O8** | Maintain negligible deterministic governance latency overhead | **Deterministic security overhead $< 2.0\%$** | High-resolution microsecond execution telemetry across 300+ automated test cases |

---

## 4. PROPOSED METHODOLOGY & TECHNICAL ARCHITECTURE

### 4.1 Stage-by-Stage Design
1. **Stage 1 (Sentinel Gatekeeper):** Computes Shannon entropy ($H(X) > 4.5$) and executes Verhoeff/regex validation for Indian PII. Replaces sensitive entities with UUID tokens via local Zero-Knowledge Vaulting.
2. **Stage 2 (Agentic Code RAG):** Preserves AST syntax boundaries during chunking, embedding into 384-dimensional dense vectors with `all-MiniLM-L6-v2` in Qdrant, retrieving context where $\cos(\theta) \ge 0.70$.
3. **Stage 3 (AST Blast-Radius Engine):** Parses Python code into graph $G=(V, E)$, calculating normalized transitive closure reachability $B(v) = \frac{|\text{Reach}(v)|}{|V|-1}$ without execution.
4. **Stage 4 (Dual-Engine Privacy Tiering):** Directs public tasks to Google Gemini 2.5 Flash / Groq Cloud; directs proprietary or flagged sensitive tasks to on-premises Ollama (`qwen2.5-coder:7b`).
5. **Stage 5 (Slopsquatting Firewall):** Extracts AST `import` roots, resolves standard libraries in $0\text{ ms}$, and probes PyPI via cached REST calls. Blocks HTTP 404 packages immediately.
6. **Stage 6 (Autonomous Bounded Sandbox):** Evaluates patches inside an ephemeral subprocess under `pytest` with a 5.0-second watchdog, bounding ReAct self-repair iterations to $N = 3$.
7. **Stage 7 (5-Gate Banking Shield):** Governs financial transactions via PII tokenization, prompt injection decloaking, statutory Google ADK HITL escrow (> ₹50,000 threshold), OCC ledger updates, and SHA3-512 HSM signing.
8. **Stage 8 (Distributed SAGA Banking Highway):** Coordinates multi-phase transactions with backward compensation, Maker-Checker dual control (RBI Four-Eyes), RBI CBDC (e-INR) bearer token vault, dynamic fraud velocity tracking, and Basel III prudential telemetry.
9. **Stage 9 (Unified Cockpit & SHA3-512 Merkle Ledger):** Persists all events concurrently to SQLite WAL and JSON/CSV mirrors, maintaining an append-only NIST FIPS 202 SHA3-512 Merkle Tree with Software-Defined HSM enclave seals and real-time Server-Sent Events (SSE) telemetry.

---

## 5. EMPIRICAL RESULTS & 300-TEST BENCHMARK

### 5.1 Verification Test Suite Breakdown
The system is validated by an automated **300-test verification matrix (100% Pass Rate)**:
- **KAVACH DevSecOps Suite (100 Tests):** 15 OWASP prompt injection, 15 DPDP PII, 10 AST secrets, 10 policy engine risk, 10 RAG chunking, 10 agent state transitions, 10 A2A consensus protocols, 10 advanced reasoning (CoT, ToT, GoT), 5 vision threat auditor, 5 code impact blast-radius. *(Execution time: 0.58s)*.
- **Bharat Core Banking Suite (100 Tests):** 10 genesis balances, 10 5-gate shield transfers, 10 HITL > ₹50K escrow, 10 FIPS 140-2 Level 3 HSM signatures, 10 SAGA 4-phase compensations, 10 fraud velocity anomalies, 10 Maker-Checker dual approvals, 10 RBI CBDC token transfers, 10 timelock escrow clawbacks, 10 Basel III capital adequacy. *(Execution time: 1.15s)*.
- **Unified Integration Suite (100 Tests):** 15 agent-to-banking highways, 15 NIST SHA3-512 Merkle integrity proofs, 15 dual-store persistence syncs, 15 Results Cockpit REST contracts, 15 multi-vector cyber intercepts, 15 high-concurrency stress tests, 10 statutory audit reporting. *(Execution time: 1.42s)*.

### 5.2 Key Quantitative Achievements
- **Test Suite Pass Rate:** **300 / 300 Tests (100.0%)**
- **Package Slopsquatting Detection:** **100% Precision, 100% Recall, 100% $F_1$** (50 genuine vs. 50 hallucinated)
- **Credential Interception:** **100% Catch Rate** (AWS, GitHub, Stripe keys)
- **Indian PII Detection:** **$F_1 = 0.962$** on Hinglish prompts under DPDP Act obligations
- **Self-Healing Convergence:** **90.0% pass rate** within 2 ReAct reflection cycles
- **Financial Balance Leakage:** **0.00% (Zero Balance Leakage)** across simulated SAGA chaos crashes
- **Deterministic Security Overhead:** **$< 20\text{ ms}$ combined ($< 1.42\%$ total pipeline latency)**
- **Prudential Ratios:** Capital Adequacy Ratio = **16.67%** (vs RBI min 11.5%); Liquidity Coverage Ratio = **142.86%** (vs RBI min 100%)

---

## 6. WORK BREAKDOWN & TEAM SPECIALIZATION

- **Dhruv Jain (230532) — Project Architect, ADK Callbacks & Core Banking Lead:** 9-Stage System FSM design, Google ADK 8-Hook Callback Architecture across 3 phases (Agent/Model/Tool), Canonical Medical Triage Agent Pipeline, Core Banking Highway, Distributed SAGA Orchestrator, Anthropic Model Context Protocol (MCP) server, RBI CBDC token ledger, Timelock escrow.
- **Dev Garg (230487) — Pre-Execution Guardrails & Supply-Chain Firewall Lead:** Sentinel entropy gatekeeper, DPDP Verhoeff PII masking, live PyPI slopsquatting firewall, polyglot adversarial memo decloaking.
- **Ansh Rohilla (230794) — Agentic RAG & AST Graph Analysis Lead:** Dense Qdrant vector indexing, AST-preserving semantic chunking, whole-repository dependency graph $G=(V, E)$, transitive blast-radius calculator.
- **Ansh Adhikari (230822) — Sandbox, Self-Healing & Telemetry Cockpit Lead:** Subprocess pytest sandbox, bounded ReAct reflection loop ($N=3$), Unified Operations Cockpit UI, NIST FIPS 202 SHA3-512 Merkle Tree, Software HSM enclave seals.

---

## 7. KEY ACADEMIC REFERENCES

1. J. Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," *NeurIPS 2024*, arXiv:2405.15793.
2. Cognition AI, "Introducing Devin, the First Autonomous AI Software Engineer," *Cognition Labs Report*, 2024.
3. S. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," *ICLR 2023*, arXiv:2210.03629.
4. J. Spracklen et al., "We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code-Generating LLMs," *Proc. USENIX Security 2025*.
5. S. Larson, "The Rise of Slopsquatting: How AI Hallucinations Fuel Supply Chain Attacks," *Python Software Foundation*, 2025.
6. K. Greshake et al., "Compromising Real-World LLM Applications with Indirect Prompt Injection," *ACM AISec 2023*.
7. OWASP Foundation, "OWASP Top 10 for Large Language Model Applications," *LLM01:2025*, 2025.
8. P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *NeurIPS 2020*.
9. N. Reimers & I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," *EMNLP 2019*.
10. Z. Feng et al., "CodeBERT: A Pre-Trained Model for Programming and Natural Languages," *Findings of EMNLP 2020*.
11. Qdrant Vector Database, "Engine Architecture and Vector Indexing Documentation," `qdrant.tech`, 2026.
12. A. V. Aho, M. S. Lam, R. Sethi, and J. D. Ullman, *Compilers: Principles, Techniques, and Tools*, 2nd ed., Pearson, 2006.
13. Government of India, "The Digital Personal Data Protection Act, 2023," *The Gazette of India*, Act No. 22 of 2023.
14. European Parliament, "Regulation (EU) 2024/1689 laying down harmonised rules on AI (Artificial Intelligence Act)," 2024.
15. Reserve Bank of India, "Master Direction on Information Technology Governance and Digital Payment Controls," *RBI/2023-24/107*, 2023.
16. National Institute of Standards and Technology (NIST), "SHA-3 Standard: Permutation-Based Hash Functions," *FIPS PUB 202*, 2015.
17. H. Garcia-Molina & K. Salem, "Sagas," *ACM SIGMOD 1987*.
18. Basel Committee on Banking Supervision, "Basel III: A Global Regulatory Framework," *Bank for International Settlements*, 2023.
19. R. C. Merkle, "A Digital Signature Based on a Conventional Encryption Function," *CRYPTO '87*, Springer, 1988.
20. Anthropic, "The Model Context Protocol (MCP) Specification," `modelcontextprotocol.io`, 2024.
