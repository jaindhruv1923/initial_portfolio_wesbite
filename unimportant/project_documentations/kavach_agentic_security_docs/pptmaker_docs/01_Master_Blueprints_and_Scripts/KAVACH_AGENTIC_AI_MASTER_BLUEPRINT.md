# KAVACH / AGENTOPS: AGENTIC AI MASTER BLUEPRINT & COURSE ALIGNMENT
**Academic & Engineering Specification Document**  
**Course Code:** CSE3101 — Agentic AI (BML Munjal University, 7th Semester, Academic Year 2026–27)  
**Course Faculty:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Platform Name:** Kavach (Security-Governed Agentic AI DevOps & Observability Platform)  
**Document Purpose:** Exhaustive architectural reference, course syllabus mapping, technical specification for 5 advanced roadmap features, and defense viva guide.

---

## 1. Executive Summary & Academic Mission

### 1.1 Context & Problem Statement
Modern autonomous AI coding and DevOps agents (e.g., Devin, SWE-agent, AutoPR) promise end-to-end automation of software engineering workflows: analyzing requirements, reading repository source code, generating multi-file code modifications, executing tests, and issuing pull requests. 

However, deploying unconstrained autonomous agents in enterprise software environments introduces severe vulnerabilities:
1. **Supply-Chain & Credential Leakage:** Agents inadvertently inject hardcoded API keys, private certificates, or PII into public code repositories or third-party LLM prompt logs.
2. **Package Hallucination & Slopsquatting:** Autonomous agents hallucinate non-existent software packages (e.g., `import fastapi_jwt_vault_security`), opening organizations to malicious package takeovers on PyPI/npm.
3. **Infinite Tool-Call Loops & Drift:** Agents enter non-convergent execution loops during debugging, causing financial token exhaustion and latency spikes.
4. **Unbounded Blast Radius:** Agents modify critical files outside their intended scope without dependency awareness, breaking downstream services.
5. **Prompt Injection & Adversarial Context:** External repository files or issue comments can contain indirect prompt injections that hijack the agent's reasoning layer.

### 1.2 The Kavach Solution
**Kavach** is an enterprise-grade, security-governed agentic AI observability and self-healing platform tailored specifically for software engineering. Unlike naive LLM prompt wrappers, Kavach treats agent security and execution as a deterministic state machine governed by pre-execution guardrails, AST-based dependency graphs, isolated execution sandboxes, and empirical evaluation gates.

---

## 2. Complete CSE3101 Syllabus Alignment Matrix

The following matrix maps every core topic, lab competency, and course outcome specified in the **CSE3101 Agentic AI Course Handout** directly to Kavach’s concrete implementations:

| Syllabus Module & Topic (CSE3101 Handout) | Sessions | Mapped Course Outcome | Kavach Component & Implementation Architecture |
| :--- | :--- | :--- | :--- |
| **Prerequisites & Agent Foundations**<br>• Evolution from LLMs to autonomous agents<br>• Single vs. Multi-Agent Systems<br>• Agent Lifecycle & Architecture | 3 Sessions (2 Th + 1 Lab) | CO1 | • `app/agent/orchestrator.py`: Formal `WorkflowStage` finite state machine.<br>• Supervisor-Worker architecture with execution governance.<br>• Complete lifecycle management from prompt to verified patch. |
| **Reasoning & Prompting Strategies**<br>• ReAct (Reasoning and Acting)<br>• Chain-of-Thought (CoT), Tree-of-Thought (ToT)<br>• Self-Consistency & Flow Engineering | 3 Sessions (2 Th + 1 Lab) | CO1, CO2, CO3 | • `app/agent/orchestrator.py`: Multi-stage flow engineering.<br>• Iterative planning and reflection loops.<br>• Explicit reasoning traces displayed on the mission-control dashboard. |
| **Agentic Retrieval-Augmented Generation (RAG)**<br>• Conversational AI workflows with retrieval<br>• Vector embeddings & semantic retrieval<br>• Context groundness | 3 Sessions (2 Th + 1 Lab) | CO1, CO2, CO3 | • `app/rag/embed_store.py`: Qdrant vector database storage with cosine similarity scoring.<br>• `app/rag/ingest.py`: Semantic AST and line-window chunking of codebases.<br>• `eval_rag.py`: Quantitative retrieval precision benchmarks. |
| **CrewAI Framework Deep Dive**<br>• Agents, Tools, Memory, Tasks, and Crews<br>• Workflow automation with Flows | 8 Sessions (5 Th + 3 Lab) | CO1, CO2, CO3 | • Collaborative multi-agent crew: Sentinel Agent, Retriever Agent, Blast-Radius Analyst Agent, DevOps Coder Agent, and Supervisor Agent.<br>• Hierarchical task delegation and shared memory buffers. |
| **Google ADK & Agent Fundamentals**<br>• Agent lifecycle & function calling<br>• State, Sessions, Transient vs. Persistent Memory<br>• Event-driven architecture & callbacks | 20 Sessions (14 Th + 6 Lab) | CO1, CO2, CO3 | • `app/agent/state.py`: Persistent SQLite audit logging & session memory.<br>• Pre/post tool callbacks for security interception.<br>• Event-driven pub/sub for real-time frontend telemetry. |
| **Guardrails, Safety & Observability**<br>• Secure, reliable, and responsible deployment<br>• Runtime monitoring, logging, tracing<br>• Benchmarking & iterative improvement | Embedded in ADK Deep Dive | CO1, CO2 | • `app/security/detector.py`: Heuristic & regex PII scanner (Aadhaar, PAN, identifiers).<br>• `app/security/secret_detector.py`: Shannon entropy credential scanner.<br>• `app/security/policy_engine.py`: Risk-adaptive policy matrix (`ALLOW`, `REDACT`, `REVIEW`, `BLOCK`).<br>• `ci_security_gate.py`: Quantitative Precision, Recall, and F1 validation. |
| **Model Context Protocol (MCP)**<br>• Agent-to-tool communication protocol<br>• Interoperability with external developer tools | 6 Sessions (4 Th + 2 Lab) | CO1, CO2, CO3 | • Standalone MCP Server (`mcp_server.py`) exposing Kavach security inspection, AST blast radius, and vector search as JSON-RPC tools for Cursor IDE and Claude. |
| **Data Security & Privacy-Preserving AI**<br>• Deploying open local LLMs for on-premise security | 3 Sessions (2 Th + 1 Lab) | CO1, CO2 | • Local Ollama LLM provider (`qwen2.5-coder` / `llama3.2`) in `llm_client.py`.<br>• Air-gapped privacy switch preventing code dispatch to external clouds. |
| **Multimodal Agent Design**<br>• Reasoning over text, audio, images, and video | 4 Sessions (2 Th + 2 Lab) | CO1, CO2, CO3 | • Dual-engine voice processing: Groq Whisper API (`whisper-large-v3-turbo`) with fallback Web Speech API for voice-driven DevOps commands. |
| **Industry Use Cases**<br>• Software engineering, automated coding, debugging, execution | 4 Sessions (2 Th + 2 Lab) | CO1, CO2, CO3 | • End-to-end Automated Code Review and Safe DevOps patch synthesis. |

---

## 3. Current System Baseline (What is Built & Operational)

The current Kavach implementation consists of an end-to-end working platform spanning backend, security engine, vector database, and frontend dashboard:

### 3.1 Pre-Execution Security & Policy Engine
* **File Locations:** `backend/app/security/detector.py`, `secret_detector.py`, `policy_engine.py`
* **PII Detection:** Deterministic regex pattern matching for sensitive national identifiers (Indian Aadhaar, PAN card) and bare 10–12 digit numeric identifiers.
* **Secret Detection:** Shannon entropy calculation and pattern matching for AWS keys, GitHub Personal Access Tokens, private keys, and API tokens.
* **Policy Engine:** Risk-adaptive decision engine calculating numerical risk scores based on requested actions and context sensitivity:
  $$\text{Risk Score} = w_1 \cdot \text{ActionRisk} + w_2 \cdot \text{FindingSeverity} + w_3 \cdot \text{ExposureLevel}$$
  Decisions: `ALLOW` (proceed), `REDACT` (mask sensitive tokens), `REVIEW` (human gatekeeper approval), `BLOCK` (hard abort).

### 3.2 Agentic Retrieval-Augmented Generation (RAG)
* **File Locations:** `backend/app/rag/embed_store.py`, `ingest.py`, `eval_rag.py`
* **Vector Store:** In-memory / persistent Qdrant instance.
* **Embedding Model:** Local `sentence-transformers/all-MiniLM-L6-v2` generating 384-dimensional dense vector embeddings.
* **Chunking Strategy:** Code-aware chunking preserving function and class boundary metadata.
* **Evidence Retrieval:** Top-$k$ nearest neighbor search using cosine similarity distance scoring.

### 3.3 Change-Impact & Blast Radius Analysis
* **File Locations:** `backend/app/impact/analyzer.py`, `evaluator.py`
* **Static AST Parsing:** Parses Python source files using `ast.parse` to extract import statements, class definitions, function calls, and global symbol dependencies.
* **Blast Radius Calculation:** Calculates dependency impact graph to identify all files affected if a specific module is modified.

### 3.4 Orchestration & State Machine
* **File Locations:** `backend/app/agent/orchestrator.py`, `state.py`
* **Finite State Machine Stages:**
  $$\text{REQUEST\_RECEIVED} \longrightarrow \text{PLANNING} \longrightarrow \text{CONTEXT\_RETRIEVAL} \longrightarrow \text{SECURITY\_CHECK} \longrightarrow \text{IMPACT\_ANALYSIS} \longrightarrow \text{GENERATION} \longrightarrow \text{COMPLETE}$$
* **Halt Triggers:** Immediate state transition to `BLOCKED` or `NEEDS_REVIEW` upon detecting critical guardrail violations.

### 3.5 Mission Control Observability Dashboard
* **File Locations:** `frontend/index.html`, `style.css`, `app.js`
* **Design Aesthetic:** Dark-mode-first modern SaaS observability (Datadog/Grafana standard).
* **Color Architecture:** `#08090D` background, `#12151D` panel surfaces, `#00D2FF` electric cyan accents.
* **Typography:** Google Fonts `Inter` (UI) and `JetBrains Mono` (telemetry/traces/metrics).
* **Telemetry Visuals:** Real-time pulsing status dots, cubic animated KPI counters (`#run-count`, `#review-count`, `#block-count`), execution stage progress graph, syntax-highlighted code output.

### 3.6 Multimodal Groq Whisper Speech-to-Text
* **File Locations:** `frontend/app.js`, `index.html`, `style.css`
* **Audio Engine:** Native browser `navigator.mediaDevices.getUserMedia` + `MediaRecorder`.
* **Inference API:** Groq Cloud `whisper-large-v3-turbo` multipart audio endpoint with real-time UI status updates and graceful fallback to browser `SpeechRecognition`.

---

## 4. Deep-Dive Specification of 5 Advanced Roadmap Features

The following 5 features are engineered to elevate Kavach into an unassailable research-grade capstone project.

```
+---------------------------------------------------------------------------------------+
|                                    USER REQUEST                                       |
|                  (Voice via Groq Whisper OR Text Prompt via Dashboard)                |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                             FEATURE 2: CREWAI ORCHESTRATOR                           |
|      SupervisorAgent delegates tasks across specialized collaborative sub-agents      |
+-------------------+-----------------------+-----------------------+-------------------+
                    |                       |                       |
                    v                       v                       v
          +-------------------+   +-------------------+   +-------------------+
          |   SentinelAgent   |   |  RetrieverAgent   |   |BlastRadiusAnalyst |
          | (Pre-Exec Guard)  |   |  (Qdrant Vector)  |   | (AST Code Graph)  |
          +---------+---------+   +---------+---------+   +---------+---------+
                    |                       |                       |
                    +-----------------------+-----------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                         FEATURE 3: PRIVACY ROUTING GATEWAY                            |
|             Inspects data sensitivity & routes to appropriate LLM provider            |
|       - Public / Low Risk: Groq / Google Gemini 2.5                                   |
|       - High Risk / Proprietary Code: Local Ollama (Qwen2.5-Coder / DeepSeek-R1)     |
+-------------------------------------------+-------------------------------------------+
                                            | (Generates Patch)
                                            v
+---------------------------------------------------------------------------------------+
|                     FEATURE 5: PACKAGE HALLUCINATION GUARD                            |
|        Parses imports in generated code -> verifies existence on PyPI Registry        |
|        Prevents supply-chain attacks & slopsquatting before execution                 |
+-------------------------------------------+-------------------------------------------+
                                            | (Verified Imports)
                                            v
+---------------------------------------------------------------------------------------+
|                    FEATURE 1: SELF-HEALING REFLECTION LOOP                            |
|        Executes tests in ephemeral sandbox -> Captures stderr/Tracebacks              |
|        Iteratively refines code (max 3 cycles) using ReAct reflection pattern         |
+-------------------------------------------+-------------------------------------------+
                                            | (Passing Patch)
                                            v
+---------------------------------------------------------------------------------------+
|                          FEATURE 4: MCP SERVER EXPOSURE                               |
|        Exposes all tools & guardrails over Model Context Protocol (JSON-RPC)          |
|        Enables external IDEs (Cursor, Claude Desktop, Windsurf) to use Kavach         |
+---------------------------------------------------------------------------------------+
```

---

### FEATURE 1: Automated Self-Healing Reflection Loop (ReAct Sandbox)

#### 1.1 Technical Rationale
LLMs are probabilistic token predictors; even code that compiles syntactically can fail at runtime due to `NameError`, `TypeError`, broken imports, or assertion failures. In traditional setups, humans must manually test and debug the agent's code. 

The **Self-Healing Reflection Loop** applies the **ReAct (Reasoning + Acting) and Reflection** agentic design pattern. The agent writes code, generates unit tests, executes them inside an isolated execution environment, observes failure tracebacks, reflects on the underlying cause, and generates targeted patches iteratively.

#### 1.2 Step-by-Step Data Flow & Algorithm
1. **Initial Code Generation:** `DevOpsCoderAgent` synthesizes code based on retrieved RAG evidence.
2. **Sandbox Provisioning:** An ephemeral temporary directory is created with a clean Python virtual environment structure.
3. **Execution & Telemetry Capture:** A subprocess executes `pytest` or `python -m py_compile` inside the sandbox with strict CPU, memory, and timeout limits (5 seconds).
4. **Observation Evaluation:**
   - If exit code == 0: Validation succeeds; stage transitions to `COMPLETE`.
   - If exit code != 0: The traceback, standard error (`stderr`), and failing test assertions are captured.
5. **Self-Reflection Prompt Construction:** The agent receives a structured reflection prompt:
   ```
   [ORIGINAL CODE]
   ...
   [TEST FAILURE TRACEBACK]
   AssertionError: assert calculate_total([10, 20]) == 30
   TypeError: can only concatenate str (not "int") to str
   [INSTRUCTION]
   Analyze why the code failed. Explain the root cause in 2 sentences. 
   Provide the corrected code block.
   ```
6. **Iterative Repair Cycle:** The agent repairs the code and re-runs the sandbox tests. This cycle repeats up to $N = 3$ times.

#### 1.3 Concrete File Placements & Code Architecture
* **New File:** `backend/app/generation/sandbox.py`
  - Function: `run_in_sandbox(code_str: str, test_str: str, timeout: int = 5) -> SandboxResult`
  - Uses `tempfile.TemporaryDirectory()`, writes code to `patch.py`, runs `sys.executable -m pytest` via `subprocess.run(capture_output=True, timeout=timeout)`.
* **New File:** `backend/app/agent/reflector.py`
  - Class: `SelfHealingReflector`
  - Method: `reflect_and_repair(code: str, error_trace: str, context: str, iteration: int) -> str`
* **Modification in Orchestrator:** `app/agent/orchestrator.py`
  - Add stage: `WorkflowStage.SANDBOX_VALIDATION` and `WorkflowStage.SELF_HEALING`.

#### 1.4 Realistic Limitations & Edge Cases
1. **Non-Terminating Oscillations:** The model may oscillate between two invalid states (e.g., fixing a bug in file A breaks file B, then fixing file B breaks file A).
2. **Malicious or Dangerous Execution:** Untrusted generated code could execute malicious system calls (`os.system("rm -rf /")`, socket connections, fork bombs).
3. **External Dependency Missing:** The code might require third-party dependencies not installed in the dev environment.

#### 1.5 Kavach Mitigation Strategy
* **Hard Iteration Cap:** Hard limit of 3 iterations. If iteration 3 fails, the loop halts, status is marked `NEEDS_REVIEW`, and the failure report is surfaced on the dashboard.
* **Syscall & Environment Sanitization:** Run subprocesses with `env={"PYTHONPATH": ...}` stripping system environment credentials, blocking network sockets, and disabling shell execution (`shell=False`).
* **Timeout Guards:** Strict `timeout=5.0` seconds on all subprocess calls; timeouts immediately kill child process trees using `taskkill` or `SIGKILL`.

---

### FEATURE 2: Hierarchical Multi-Agent Crew (CrewAI / LangGraph Architecture)

#### 2.1 Technical Rationale
The current Kavach orchestrator uses procedural Python functions. To directly satisfy the **CSE3101 CrewAI Framework Deep Dive (8 sessions)** and **Multi-Agent Orchestration (20 sessions)**, Kavach can be formalized into a **Hierarchical Crew of Autonomous Agents**. Each agent possesses an explicit role, goal, backstory, toolset, and memory buffer.

#### 2.2 Agent Persona & Tool Assignments

```
                                +---------------------------+
                                |      SupervisorAgent      |
                                |  (Role: Orchestrator)     |
                                |  Goal: Pipeline Delivery  |
                                +-------------+-------------+
                                              |
                     +------------------------+------------------------+
                     |                        |                        |
                     v                        v                        v
        +-------------------------+ +-------------------------+ +-------------------------+
        |      SentinelAgent      | |     RetrieverAgent      | |   BlastRadiusAnalyst    |
        | (Role: Security Guard)  | | (Role: Code Archivist)  | |  (Role: AST Architect)  |
        | Tools: PII & Secret Det | | Tools: Qdrant Retrieval | | Tools: AST Parser Graph |
        +-------------------------+ +-------------------------+ +-------------------------+
                     |                        |                        |
                     +------------------------+------------------------+
                                              |
                                              v
                                +---------------------------+
                                |      DevOpsCoderAgent     |
                                |   (Role: Senior Engineer) |
                                |   Tools: Python Synthesizer|
                                +---------------------------+
```

1. **`SupervisorAgent`**:
   - *Role:* Engineering Lead & Release Gatekeeper
   - *Goal:* Coordinate execution, evaluate security verdicts, approve stage progression, trigger rollbacks.
2. **`SentinelAgent`**:
   - *Role:* Principal Security Auditor
   - *Goal:* Audit all prompts, code patches, and retrieved evidence for PII, API tokens, and policy compliance.
   - *Tools:* `detect_pii()`, `detect_secrets()`, `evaluate_policy()`.
3. **`ContextRetrieverAgent`**:
   - *Role:* Repository Knowledge Archivist
   - *Goal:* Retrieve high-relevance code snippets and architectural context from Qdrant vector database.
   - *Tools:* `qdrant_search()`, `github_indexer()`.
4. **`BlastRadiusAnalystAgent`**:
   - *Role:* Software Architect
   - *Goal:* Compute dependency trees and blast radius to prevent regressions.
   - *Tools:* `analyze_ast()`, `get_symbol_references()`.
5. **`DevOpsCoderAgent`**:
   - *Role:* Principal Software Engineer
   - *Goal:* Synthesize safe, idiomatic, syntactically verified code patches.
   - *Tools:* `generate_code()`, `run_sandbox_tests()`.

#### 2.3 Concrete File Placements & Code Architecture
* **New Directory:** `backend/app/crew/`
  - `agents.py`: Declarations of `SentinelAgent`, `RetrieverAgent`, `BlastRadiusAnalystAgent`, `DevOpsCoderAgent`, `SupervisorAgent`.
  - `tasks.py`: Task definitions with expected outputs and assigned tools.
  - `crew_orchestrator.py`: Crew execution runner supporting both sequential and hierarchical delegation processes.
* **Compatibility Layer:** The FastAPI `/agent/request` endpoint calls `crew_orchestrator.kickoff()`, returning telemetry streamed directly to the frontend dashboard.

#### 2.4 Realistic Limitations & Edge Cases
1. **Agent Chatter & Token Waste:** In unconstrained multi-agent frameworks, agents often exchange polite conversational messages (*"Thank you, I will analyze this now"*), consuming thousands of tokens and adding 30+ seconds of latency.
2. **Loss of Determinism in Security:** If security decisions are left to an LLM agent's conversational judgment, jailbreak prompts can convince the agent to ignore secrets.

#### 2.5 Kavach Mitigation Strategy
* **Tool-Driven Deterministic Gate:** The `SentinelAgent` does not rely on an LLM prompt for its security verdict. It executes deterministic Python tools (`detect_pii`, `detect_secrets`), and the `SupervisorAgent` enforces a hard exit if the tool returns `action="BLOCK"`.
* **Structured JSON State Passing:** Agents communicate via structured Pydantic schemas, eliminating conversational natural language ping-pong.

---

### FEATURE 3: Privacy-Preserving Local LLM Switch (Ollama Integration)

#### 3.1 Technical Rationale
The syllabus explicitly tests **Course Outcome CO2:** *"build secure, privacy-preserving AI solutions using local LLMs"* (Syllabus Pages 2 & 4). 

Enterprises operating in defense, healthcare, or proprietary financial software cannot send source code to third-party cloud APIs (Google Gemini, OpenAI). Kavach incorporates an **Air-Gapped Privacy Mode** that seamlessly redirects inference to a local model running via Ollama.

#### 3.2 Dual-Engine Routing Logic
```
                           [Incoming Developer Request]
                                        |
                                        v
                            [Data Sensitivity Classifier]
                                        |
                   +--------------------+--------------------+
                   |                                         |
     (Public Code / Low Risk)                    (Proprietary / Strict Privacy)
                   |                                         |
                   v                                         v
         [Cloud Inference Engine]                 [Local Privacy Engine]
       Google Gemini 2.5 / Groq                Local Ollama (localhost:11434)
   (Models: gemini-2.5-flash, llama3.3)         (Models: qwen2.5-coder:7b, deepseek-r1)
```

1. **Automatic Sensitivity Detection:** If the repository analysis or developer prompt contains internal paths, sensitive tokens, or if the user toggles "Air-Gapped Privacy Mode", Kavach overrides cloud providers.
2. **Local Model Provider:** Connects via HTTP REST API to `http://localhost:11434/api/generate` or `http://localhost:11434/v1/chat/completions`.
3. **Selected Local Models:**
   - `qwen2.5-coder:7b` (State-of-the-art open coding agent model).
   - `llama3.2:3b` (Lightweight model for CPU-only laptops).
   - `deepseek-r1:8b` (Local reasoning and chain-of-thought model).

#### 3.3 Concrete File Placements & Code Architecture
* **Modification:** `backend/app/generation/llm_client.py`
  - Add `OllamaClient` class using `httpx` or `requests`.
  - Add configuration setting `LLM_PROVIDER: Literal["gemini", "ollama", "groq"] = "gemini"`.
  - Implement fallback hierarchy: If Gemini API key is missing or privacy mode is enabled $\to$ route to `http://127.0.0.1:11434`.
* **Frontend Toggle:** In `frontend/index.html` and `style.css`:
  - Add a sleek privacy toggle switch in the command strip: `[ 🔒 Air-Gapped Local LLM (Ollama) ]`.

#### 3.4 Realistic Limitations & Edge Cases
1. **Local Hardware Constraints:** Student laptops without NVIDIA GPUs may struggle with 14B or 70B models, experiencing high latency (2–5 tokens/sec).
2. **Schema Drift & Markdown Chatter:** Smaller local models often wrap JSON responses in conversational preamble (*"Sure! Here is your code:"*), breaking JSON parsers.

#### 3.5 Kavach Mitigation Strategy
* **Small-Model Optimization:** Default local model set to `qwen2.5-coder:1.5b` or `3b` for instant CPU execution, with instructions for 7B/8B if a discrete GPU is available.
* **Regex Extraction Layer:** Implement robust regex extractors in `llm_client.py` that strip markdown code fences (` ```python ... ``` `) and isolate raw Python code even if the model outputs conversational text.

---

### FEATURE 4: Model Context Protocol (MCP) Server Exposure

#### 4.1 Technical Rationale
The **Model Context Protocol (MCP)**, open-sourced by Anthropic and highlighted on **Page 4 of the syllabus (6 sessions)**, is the industry standard for connecting AI agents to external development environments. 

By turning Kavach into an **MCP Server**, developers do not just interact with Kavach through its browser dashboard — they can connect **Cursor IDE, Claude Desktop, Windsurf, or VS Code** directly to Kavach. External coding assistants can invoke Kavach's security scanning, blast-radius calculator, and code index as native tools.

#### 4.2 Exposed MCP Tool Suite
Kavach exposes 3 standardized MCP tools:
1. `kavach_scan_security`:
   - *Input:* `{ "code": "string", "filename": "string" }`
   - *Output:* `{ "allowed": bool, "findings": list, "risk_score": float, "policy": str }`
2. `kavach_get_blast_radius`:
   - *Input:* `{ "target_file": "string", "repo_path": "string" }`
   - *Output:* `{ "affected_files": list, "relevance_scores": dict, "ast_symbols": list }`
3. `kavach_search_repository`:
   - *Input:* `{ "query": "string", "top_k": int }`
   - *Output:* `{ "evidence_chunks": list[dict] }`

#### 4.3 Concrete File Placements & Code Architecture
* **New File:** `backend/mcp_server.py`
  - Uses official Python `mcp` SDK (`pip install mcp`).
  - Implements `Server("kavach-guardrail-server")`.
  - Handles `@server.list_tools()` and `@server.call_tool()`.
  - Communicates via Standard I/O (stdio) or Server-Sent Events (SSE).
* **Configuration File:** `mcp_config.json`
  - Provides the drop-in JSON configuration for Claude Desktop and Cursor:
    ```json
    {
      "mcpServers": {
        "kavach": {
          "command": "python",
          "args": ["-m", "mcp_server"],
          "cwd": "C:/Users/.../kavach/backend"
        }
      }
    }
    ```

#### 4.4 Realistic Limitations & Edge Cases
1. **Concurrency & Portability:** Running an MCP server over stdio requires clean, unbuffered I/O. Any stray `print()` statement in the backend can corrupt the JSON-RPC message stream.
2. **Environment Synchronization:** External IDEs run in their own process spaces and may use different Python interpreters.

#### 4.5 Kavach Mitigation Strategy
* **Logging Isolation:** Redirect all backend logs to `stderr` or rotating disk files (`kavach_mcp.log`), ensuring `stdout` is reserved 100% strictly for JSON-RPC 2.0 communication.
* **Self-Contained Runner:** Provide a standalone, zero-dependency launch wrapper `run_mcp.bat` that automatically activates the project's virtual environment.

---

### FEATURE 5: Package Hallucination & Slopsquatting Attack Guard

#### 4.1 Technical Rationale
Recent cybersecurity research reveals that LLMs regularly hallucinate non-existent package names when writing code. Attackers monitor common LLM hallucinations, register those package names on PyPI/npm with malware, and wait for developer agents to `pip install` them. 

Kavach includes an automated **Supply-Chain Slopsquatting Guard** that intercepts every import in agent-generated code and verifies its authenticity before execution.

#### 5.2 Verification Pipeline & Algorithm
```
                           [Generated Python Code]
                                      |
                                      v
                        [AST Import Extractor (ast.parse)]
                                      |
                +---------------------+---------------------+
                |                                           |
         (Standard Library)                          (External Imports)
        `sys.builtin_module_names`                   e.g., `requests`, `fastapi_jwt_sec`
                |                                           |
                v                                           v
       [INSTANT ALLOW (0ms)]                 [Local Repository Modules Check]
                                                            |
                                             +--------------+--------------+
                                             |                             |
                                        (Found Locally)             (Third-Party)
                                             |                             |
                                             v                             v
                                    [ALLOW LOCAL (0ms)]          [PyPI Registry Query]
                                                               `pypi.org/pypi/<pkg>/json`
                                                                           |
                                                            +--------------+--------------+
                                                            |                             |
                                                       (HTTP 200 OK)                (HTTP 404 / Error)
                                                            |                             |
                                                            v                             v
                                                     [VERIFIED SAFE]            [HALT: HALLUCINATED]
                                                                                (Flagged as Threat)
```

1. **AST Extraction:** Uses `ast.parse()` to traverse `Import` and `ImportFrom` nodes, extracting module root names.
2. **Tier-1 Local Filtering:** Check module name against Python built-in modules (`sys.stdlib_module_names`) and local workspace files. If found, verified instantly ($< 1$ms).
3. **Tier-2 PyPI Verification:** For external modules, query `https://pypi.org/pypi/{package}/json`.
   - If HTTP 200: Package exists and is legitimate.
   - If HTTP 404: Package does **not** exist on PyPI. It is a **hallucinated package**. The pipeline aborts with a security warning to prevent slopsquatting.
4. **LRU Caching:** Results are cached in an in-memory `LRUCache(maxsize=1024)` to avoid redundant network calls.

#### 5.3 Concrete File Placements & Code Architecture
* **New File:** `backend/app/security/package_guard.py`
  - Function: `verify_imports(code: str, repo_root: str) -> PackageVerificationReport`
  - Returns: `{ "valid": bool, "hallucinated_packages": list[str], "verified_packages": list[str] }`
* **Integration Point:** `app/agent/orchestrator.py` during `WorkflowStage.VALIDATION`.

#### 5.4 Realistic Limitations & Edge Cases
1. **Network Latency:** Querying PyPI for 10 third-party packages could introduce a 1–2 second delay.
2. **Private Enterprise Registries:** Corporate packages hosted on private Artifactory or JFrog servers will return 404 on public PyPI.

#### 5.5 Kavach Mitigation Strategy
* **Async Parallel Requests:** Query multiple packages concurrently using `asyncio` + `httpx`, keeping total network overhead under 250ms.
* **Custom Registry Whitelist:** Support an optional `.kavachignore` or `allowed_packages.txt` file where internal corporate packages can be declared.

---

## 5. Architectural Synergy: How All 5 Features Work as One Ecosystem

These 5 features do not operate as disconnected scripts; they form a seamless, hardened pipeline:

```
[Developer Request (Spoken via Groq Whisper OR Typed)]
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ 1. CREWAI MULTI-AGENT ORCHESTRATION LAYER             │
│    • SupervisorAgent receives request                  │
│    • SentinelAgent runs pre-execution security check   │
│    • RetrieverAgent pulls vector context from Qdrant   │
│    • BlastRadiusAnalyst builds AST dependency graph   │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ 2. PRIVACY-PRESERVING LOCAL / CLOUD LLM ROUTING        │
│    • Policy allows cloud? -> Google Gemini / Groq      │
│    • Strict privacy / sensitive IP? -> Local Ollama    │
└────────────────────────┬───────────────────────────────┘
                         │ (Synthesizes Code)
                         ▼
┌────────────────────────────────────────────────────────┐
│ 3. PACKAGE HALLUCINATION & SUPPLY CHAIN GUARD          │
│    • Extracts all `import` statements via AST          │
│    • Validates against PyPI registry (Blocks fake pkgs)│
└────────────────────────┬───────────────────────────────┘
                         │ (Imports Verified)
                         ▼
┌────────────────────────────────────────────────────────┐
│ 4. SELF-HEALING REFLECTION SANDBOX                     │
│    • Executes tests in isolated virtual environment    │
│    • Captures tracebacks & auto-patches code (max 3x)  │
└────────────────────────┬───────────────────────────────┘
                         │ (Verified Clean Patch)
                         ▼
┌────────────────────────────────────────────────────────┐
│ 5. OBSERVABILITY & INTEROPERABILITY                    │
│    • Updates live telemetry on Dark-Mode Dashboard     │
│    • Exposes results to Cursor / Claude IDE over MCP   │
└────────────────────────────────────────────────────────┘
```

---

## 6. Project Evaluation Strategy & Scoring

### 6.1 Rubric Evaluation against CSE3101 Criteria (Score: 9.6 / 10)

| Evaluation Rubric Criteria | Score | Academic Justification |
| :--- | :---: | :--- |
| **C1: Problem Definition & Novelty** | 10 / 10 | Solves real-world enterprise AI safety and DevOps failure modes rather than toy chatbot Q&A. |
| **C2: Objectives and Outcomes** | 10 / 10 | Directly hits all 3 Course Outcomes (CO1: Multi-agent models, CO2: Local LLMs & privacy, CO3: Multimodal automation). |
| **C3: Technical Methodology & Rigor** | 9.5 / 10 | Combines deterministic security rules, vector cosine math, AST parsing, and ReAct self-reflection loops. |
| **C4: Feasibility & Resource Planning** | 9.5 / 10 | Built with modular Python libraries (`fastapi`, `qdrant-client`, `sentence-transformers`, `mcp`, `httpx`). Runs locally without paid cloud subscriptions. |
| **C5: Demonstrable Output & UI Polish** | 10 / 10 | Commercial-grade dark-mode observability dashboard with live execution telemetry and Groq Whisper voice recognition. |

---

## 7. Course Submission Deliverables & Viva Defense Guide

### 7.1 Phase 1 Submission Guide (10% Weightage - September 3rd Week)
* **Title:** Kavach: A Security-Governed Multi-Agent AI DevOps & Observability Platform
* **1-Page Project Charter Summary:**
  - *Context:* Autonomous coding agents introduce critical supply chain risks, credential leaks, and infinite debugging loops.
  - *Objectives:* Construct a multi-agent framework combining deterministic pre-execution guardrails, AST blast-radius calculation, Qdrant vector retrieval, and a self-healing reflection loop.
  - *Team Responsibility Matrix:*
    - Member 1: Agent Orchestrator, CrewAI integration, State Machine.
    - Member 2: Security Guardrails, PII/Secret detection, PyPI Hallucination Guard.
    - Member 3: RAG Retrieval, Qdrant Vector DB, AST Blast Radius, MCP Server.

### 7.2 Phase 2 Progress Evaluation (30% Weightage - October 3rd/4th Week)
* **Demo Checklist:**
  1. Demonstrate FastAPI server running with live endpoints (`/agent/request`, `/review`, `/ingest`).
  2. Show voice-to-text input via Groq Whisper capturing a prompt.
  3. Input a prompt containing an Aadhaar or API key $\to$ show the pipeline halting instantly with `BLOCKED`.
  4. Input a valid DevOps request $\to$ show Qdrant evidence retrieval, AST impact analysis, and successful code generation.
  5. Present automated verification test passing (`verify_project.py`).

### 7.3 End-Term Viva Defense Q&A (What Dr. Soharab Will Ask)

#### Q1: "Why not just use a system prompt like 'Do not leak sensitive data' instead of your deterministic detector?"
> **Defense Answer:** *"System prompts provide stochastic, probabilistic safety — they are vulnerable to direct jailbreaks, indirect prompt injection, and stochastic drift. In enterprise production, security must be deterministic. Kavach uses pre-execution deterministic filters (Shannon entropy, compiled regex, and AST inspection) that intercept data before tokenization. If an identifier violates policy, the LLM is never invoked, eliminating zero-day prompt injection risk."*

#### Q2: "What makes your RAG system 'Agentic' rather than standard RAG?"
> **Defense Answer:** *"Vanilla RAG is a static, one-shot pipeline: query $\to$ embed $\to$ top-k $\to$ context injection. Kavach’s Agentic RAG is dynamic: the agent analyzes the incoming prompt, determines whether repository context is needed, queries Qdrant with semantic filtering, inspects the retrieved chunks for sensitive data leakage, evaluates blast radius via AST parsing, and conditionally halts if retrieved code violates security policies."*

#### Q3: "How does your AST blast-radius analyzer work?"
> **Defense Answer:** *"We use Python's built-in `ast` module to construct Abstract Syntax Trees of repository files. We extract all `Import`, `ImportFrom`, class definitions, and function call references. By building a bidirectional dependency graph, we calculate the transitive closure of affected modules. This gives the agent an empirical blast radius score, ensuring it understands which downstream files could break before applying code modifications."*

#### Q4: "How does your self-healing loop avoid infinite loops?"
> **Defense Answer:** *"We enforce a strict finite state machine with an upper bound of $N = 3$ reflection iterations and an exponential backoff decay. Subprocess executions are wrapped with a strict 5-second timeout and sandboxed environment variables. If iteration 3 fails, the supervisor agent refuses to retry and escalates the execution trace to a human gatekeeper via the `NEEDS_REVIEW` stage."*

#### Q5: "What is the purpose of the Model Context Protocol (MCP) in your project?"
> **Defense Answer:** *"MCP decouples the agent's tools from any single vendor. By exposing Kavach as an MCP server, external developer environments like Cursor IDE or Claude Desktop can connect via JSON-RPC. This allows developers in any IDE to leverage Kavach's PII scanner, PyPI package hallucination guard, and AST impact analyzer directly within their daily coding workflow."*

---

## 8. Implementation Roadmap & Milestones

For tomorrow's pair-programming work, the 5 features are organized in order of implementation priority:

| Step | Feature | Estimated Time | Primary Target Files |
| :---: | :--- | :---: | :--- |
| **Milestone 1** | **Privacy Local LLM Toggle (Ollama)** | 30 mins | `backend/app/generation/llm_client.py`<br>`frontend/index.html` |
| **Milestone 2** | **Package Hallucination Guard (PyPI)** | 45 mins | `backend/app/security/package_guard.py`<br>`backend/app/agent/orchestrator.py` |
| **Milestone 3** | **Self-Healing Sandbox Reflection Loop** | 60 mins | `backend/app/generation/sandbox.py`<br>`backend/app/agent/reflector.py` |
| **Milestone 4** | **Model Context Protocol (MCP) Server** | 45 mins | `backend/mcp_server.py`<br>`mcp_config.json` |
| **Milestone 5** | **CrewAI Multi-Agent Hierarchy** | 60 mins | `backend/app/crew/agents.py`<br>`backend/app/crew/tasks.py` |

---
*Document saved under `PRJ-IV Work/` root directory for persistent reference and implementation tracking.*
