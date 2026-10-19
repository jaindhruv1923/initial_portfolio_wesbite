---
title: KAVACH Zero-Trust Agentic AI DevOps & Multi-Agent Governance
emoji: 🛡️
colorFrom: green
colorTo: emerald
sdk: docker
app_port: 8000
pinned: false
license: apache-2.0
---

# KAVACH · Security-Governed AI DevOps & Autonomous Multi-Agent Swarm
### Instructors: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
**BML Munjal University — CSE3101 Agentic AI Standardization Capstone (11/11 Verified)**

KAVACH is an enterprise-grade autonomous zero-trust multi-agent system combining **Google ADK** and **CrewAI** via signed **A2A (Agent-to-Agent)** protocol envelopes, Model Context Protocol (MCP) JSON-RPC 2.0 tools, and a central reactive **Hover Blackboard** architecture.

---

## 1. Quick Deploy to Hugging Face Spaces (30 Seconds)

1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/new-space).
2. Set Space Name: `kavach-platform`
3. License: `Apache 2.0`
4. SDK: Select **Docker** (Blank).
5. Clone and push this directory:
```bash
git remote add hf https://huggingface.co/spaces/<your-username>/kavach-platform
git push hf main
```
The container builds automatically and launches live at `https://huggingface.co/spaces/<your-username>/kavach-platform`.

---

## 2. Standardized Architecture Features

- **Hover Blackboard Architecture**: 5 reactive partitions (`domain_context`, `intermediate_outputs`, `security_guardrails`, `execution_artifacts`, `audit_provenance`) with SHA-256 state sealing.
- **Model Context Protocol (MCP)**: 4 standardized JSON-RPC 2.0 external tools (Web Search, DB Lookup, AST File Parser, Calculator).
- **A2A Interoperability Bridge**: Google ADK `LlmAgent` and CrewAI `CrewAgent` exchanging HMAC-SHA256 authenticated envelopes.
- **Pydantic Structured Outputs**: Rendering execution verdicts into Markdown, Table, and JSON formats.
- **6-Way Prompt Variance Engine**: ReAct vs Few-Shot across Junior Dev, DevOps SRE, and SecOps personas.
- **NIST FIPS 202 SHA3-512**: Cryptographic provenance hashing for immutable audit trails.
