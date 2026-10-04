# ARCHITECTURE.md — Kavach

## One-line analogy
The AI agent is the worker, the repository is the workshop, CI/CD is the factory
quality-control line, and Kavach is the security guard plus quality gate.

## End-to-End Pipeline

| Stage | What happens | Kavach's role |
|-------|---------------|----------------|
| 1. Developer intent | Natural-language request, e.g. "Add password reset." | Inspect input; policy/security checks; open audit record |
| 2. Agent planning | LLM decomposes the request into a structured plan | Govern the plan; detect unsafe/suspicious instructions |
| 3. Repository RAG | Retrieve relevant source, docs, APIs, dependencies, constraints | Inspect retrieved context for secrets/sensitive data |
| 4. Change-impact analysis | Predict affected files/functions/APIs/tests | Highlight security-sensitive components; produce impact report |
| 5. Evidence-grounded generation | Generate code using retrieved project evidence | Scan generated code for secrets, PII/SPDI, policy violations |
| 6. Test generation | Generate/update tests | Scan test fixtures/synthetic data; enforce policy (no real secrets) |
| 7. Build & tests | Compile/build and execute tests | Collect results; prevent progression on failed gates |
| 8. CI/CD security gate | Automated validation (GitHub Actions or equivalent) | Kavach policy gate decides pass / fail / review |
| 9. Human approval | Human reviews high-risk changes | Provide explanation, evidence, and audit trail |
| 10. Deployment/report | Deploy only when required gates pass; produce final report | Record complete decision history and metrics |

## Major System Components

| Component | Purpose | Output |
|-----------|---------|--------|
| Agent Orchestrator | Coordinates planning, retrieval, generation, testing, approvals | Structured workflow state |
| Repository Ingestion / RAG | Indexes source, docs, APIs, dependencies, constraints | Relevant evidence/context |
| Change-Impact Analyzer | Finds semantically related files/functions/likely-affected tests/APIs | Impact report + ranked components |
| Code Generation Agent | Produces repository-consistent modifications from retrieved evidence | Patch / code changes |
| Kavach Security Engine | Detects PII/SPDI, secrets, and policy/security violations | Allow / block / redact / review + reason |
| Multilingual NLP Layer | Processes Indian-language and code-mixed inputs | Normalized entities + detection results |
| Policy Engine | Maps detections to severity and enforcement rules | Policy decision |
| CI/CD Integration | Runs build, tests, security checks, validation | Pass/fail evidence |
| Audit Store | Persists events, decisions, findings, workflow metrics | Traceable audit log |
| Monitoring Dashboard | Shows live findings, severity, explanations, workflow state, metrics | Human-readable control plane |

## Interfaces

### A. Agent/User Interface
- Simple chatbot-like interface for entering natural-language dev requests.
- Shows agent workflow state and final response.
- Demonstrates multilingual sensitive-data detection in real time.

### B. Kavach Monitoring Dashboard
- Live feed of flagged events.
- Severity and confidence.
- Detected category and explanation.
- Original vs. redacted/blocked representation (where safe to display).
- Workflow/CI status.
- Audit log and compliance-style event view.
- Metrics: detections, blocks, latency, workflow success, test status, policy failures.

**Design principle:** the dashboard should be clean and functional but must not consume the
semester. Engineering, evaluation, and reliability of the underlying system matter far more than
visual complexity.

## Proposed Technical Stack

| Layer | Direction | Reason |
|-------|-----------|--------|
| Backend/API | Python + FastAPI | Simple service architecture, good fit for AI tooling |
| Agent orchestration | Python-based orchestrator, modular tool/agent design | Explicit, testable workflow |
| LLM | Local (Ollama, small/medium quantized) for routine tasks; cloud model for hard reasoning | Balances cost/privacy with reasoning quality |
| RAG / vector store | Qdrant or comparable | Repository/document retrieval |
| Repository analysis | Git parsing + AST/static-analysis tooling | Grounded code understanding, impact analysis |
| Database | SQLite initially; PostgreSQL if needed | Workflow events, findings, evaluation records |
| Frontend | React or lightweight HTML/JS | Separate agent UI and monitoring dashboard |
| CI/CD | GitHub Actions | Natural fit for repository-triggered workflows/gates |
| Containers | Docker | Reproducible local/CI deployment |
| Observability | Structured logs + metrics feeding the dashboard | Latency, decisions, workflow monitoring |

These are implementation recommendations, not hard requirements from the course.

---

## Communication Protocols & Architectural Decision Record (ADR)

### 1. Executive Summary & Design Rationale
Autonomous agentic AI platforms operate in an asynchronous, multi-tiered environment where latency, connection overhead, serialization efficiency, and enterprise firewall compatibility dictate system reliability. Rather than adopting a one-size-fits-all communication mechanism, Kavach implements a **polyglot protocol topology** optimized for specific directional dataflows:

```
[ Developer IDE / Cursor ]           [ GitHub / GitLab CI/CD ]
         │ (JSON-RPC / stdio or SSE)             │ (Webhooks)
         ▼                                       ▼
 ┌────────────────────────────────────────────────────────┐
 │           KAVACH SECURITY GATEWAY (FastAPI)            │
 ├───────────────────────────┬────────────────────────────┤
 │ REST API (Stateless CRUD) │ SSE (Unidirectional Stream)│
 └─────────────┬─────────────┴─────────────┬──────────────┘
               │                           │
               ▼                           ▼
      [ Mission Control UI ]     [ Real-Time Agent Stream ]
```

### 2. Comprehensive Protocol Evaluation & Decision Matrix

| Protocol | Mechanism & Characteristics | Directionality | Transport & Payload | Status in Kavach | Evaluated Role & Architectural Trade-off |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REST** (Representational State Transfer) | Stateless resource-oriented interface using standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`). | Request - Response (Half-duplex) | HTTP/1.1 or HTTP/2, JSON | **Selected & Implemented** | **Core Control Plane:** Powers `/review`, `/detect`, `/agent/request`, `/github/ingest`, and `/config/status`. Provides predictable caching, uniform error contracts (`RFC 7807`), and automatic OpenAPI/Swagger client generation. |
| **SSE** (Server-Sent Events) | Persistent, unidirectional HTTP stream sending event streams (`text/event-stream`) from server to client. | Server to Client (Unidirectional) | HTTP/1.1 or HTTP/2, UTF-8 text | **Selected & Implemented** | **Agent Telemetry & Token Streaming:** Powers `/agent/events/{run_id}` and MCP transports. Bypasses WebSocket complexity; provides native browser auto-reconnection and zero custom framing overhead for streaming LLM tokens and execution stage updates. |
| **Webhooks** | Asynchronous HTTP callbacks triggered by external events. | Producer to Consumer (Push) | HTTP/1.1 or HTTP/2, JSON | **Selected & Implemented** | **DevOps Event Ingestion:** Powers `/webhook/github`. Enables asynchronous pre-commit/pre-merge security scanning whenever pull requests or branch pushes occur, without requiring polling. |
| **gRPC** | High-performance RPC framework using HTTP/2 framing and Protocol Buffers. | Bidirectional, Unary, or Streaming | HTTP/2, Binary Protobuf | **Adopted for Scaled Microservices** | **High-Throughput Inter-Agent RPC:** Selected for decoupled worker services (e.g., offloading AST blast-radius DAG calculations to dedicated C++/Rust workers). Sub-millisecond serialization minimizes inter-agent latency. |
| **WebSockets** | Full-duplex, persistent TCP connection over a single socket handshake (`ws://`, `wss://`). | Bidirectional (Full-duplex) | TCP frame-based, text or binary | **Evaluated — Alternative / Optional** | **Interactive Agent Steering:** Evaluated for human-in-the-loop agent interrupts. Avoided for standard telemetry due to stateful connection persistence, proxy/firewall traversal friction, and complex ping-pong heartbeats where SSE suffices. |
| **GraphQL** | Declarative query language and runtime for fetching precise client-specified data trees. | Client-driven query over HTTP | HTTP, JSON | **Evaluated — Formally Rejected** | **Architectural Mismatch:** Kavach’s data domain consists of deterministic state-machine runs (`WorkflowRun`, `SecurityFinding`, `SBOM`) rather than polymorphic, sparse relational graphs. GraphQL introduces unnecessary query parsing overhead and breaks HTTP-level caching. |
| **MQTT** (Message Queuing Telemetry Transport) | Extremely lightweight publish-subscribe messaging protocol over TCP. | Pub/Sub via central broker | TCP, minimal binary header (2 bytes) | **Evaluated — Formally Rejected** | **Domain Mismatch:** Engineered for constrained IoT edge devices, telemetry sensors, and low-bandwidth/unreliable networks. Not appropriate for enterprise cloud-native DevOps repositories or high-payload LLM context transfers. |

### 3. Multi-Tiered Communication Topology

1. **Northbound Interface (Frontend Dashboard & Operator Plane):**
   - **Protocol:** REST (`FastAPI`) + Server-Sent Events (`text/event-stream`).
   - **Rationale:** Standard browser `fetch` and `EventSource` APIs require zero third-party client libraries, support seamless zero-config CORS, and run through standard corporate web proxies without port negotiation.

2. **Inbound DevOps Triggers (CI/CD Quality Gates):**
   - **Protocol:** HTTP Webhooks (`POST /webhook/github`).
   - **Rationale:** Standard GitHub/GitLab automation hooks push payload snapshots directly into the Sentinel pipeline, triggering asynchronous evaluation with deterministic delivery signatures (`X-Hub-Signature-256`).

3. **Tool & Extension Protocol (IDE Ecosystem):**
   - **Protocol:** Model Context Protocol (MCP) over JSON-RPC 2.0 (`stdio` / SSE).
   - **Rationale:** Adheres to Anthropic's open standard for AI agent tool calling, enabling Cursor IDE, VS Code, and Claude Desktop to leverage Kavach's security and RAG tools as native extensions.

---

### 4. Defense Viva Guide: Protocol Justification

- **Q: Why choose Server-Sent Events (SSE) instead of WebSockets for Kavach’s agent dashboard?**
  - **A:** WebSockets establish a stateful, bidirectional TCP connection that requires explicit heartbeat management, connection pooling, and complex load-balancing across reverse proxies. In Kavach, agent telemetry and LLM token delivery are fundamentally **unidirectional** (server to client). SSE operates over standard HTTP, natively supports automatic client reconnection with `Last-Event-ID`, traverses enterprise firewalls transparently, and aligns with the transport standard of modern LLM streaming (OpenAI, Anthropic, Gemini).

- **Q: Why is GraphQL not suitable for Kavach?**
  - **A:** GraphQL excels when frontend clients need to query arbitrary slices of deeply nested, polymorphic social graphs. In Kavach, state machine transitions (`WorkflowStage`), vulnerability audits, and blast-radius reports follow strictly typed, deterministic schemas defined in Pydantic. Adding a GraphQL resolver layer would introduce runtime query parsing overhead, complicate response caching, and add unnecessary abstraction without tangible benefit.

- **Q: Why is MQTT rejected?**
  - **A:** MQTT is optimized for telemetry from low-power, intermittent IoT hardware with tiny 2-byte headers and battery constraints. Kavach is a cloud-native, compute-intensive AI security platform processing multi-megabyte source code ASTs, vector embeddings, and CycloneDX SBOMs. Employing an MQTT broker would add operational baggage with zero architectural fit.

