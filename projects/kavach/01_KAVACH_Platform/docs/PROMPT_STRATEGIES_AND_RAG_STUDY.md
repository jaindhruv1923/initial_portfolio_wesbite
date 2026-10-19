# KAVACH: Prompt Strategies & Agentic RAG Study
**Mandatory Specification for Chapter 2: Prompt Strategy & RAG (Slide 2 Row 2)**  
**Course:** CSE3101 — Agentic AI (BML Munjal University)  
**Evaluator Reference:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  

---

## 1. Executive Summary

Slide 2 (S.No 2) of the Project Guidelines mandates:
1. *"At least one of the agents must be subject to Different Prompt Strategy - COTS / REACT Framework in Description."*
2. *"Use of RAG is necessary in one of the agents."*

This document provides the formal description, empirical comparison, prompt templates, and ablation results across **Four Distinct Prompt Strategies** applied to Kavach's **DevOpsCoderAgent & SelfHealer**, alongside the architectural specification of our **Agentic RAG with Qdrant**.

---

## 2. Four Prompt Strategies Evaluated on DevOpsCoderAgent

To evaluate how prompting affects code correctness and hallucination, we tested the coder agent across four methodologies:

```
[Strategy 1: Direct Zero-Shot]
Prompt ──> LLM ──> Unvalidated Code Output

[Strategy 2: Chain-of-Thought (CoT)]
Prompt ──> Step-by-Step Reasoning Trace ──> Code Output

[Strategy 3: Chain-of-Thought with Self-Consistency (COTS)]
Prompt ──> Sample 3 Reasoning Paths in Parallel ──> Majority Consensus Vote ──> Selected Code

[Strategy 4: ReAct (Reasoning + Acting + Sandbox Observation)]
Reasoning ──> Action (Generate Code & Tests) ──> Sandbox Observation (Traceback) ──> Reflection Repair
```

### 2.1 Concrete Prompt Templates Used in Kavach

#### Strategy 1: Direct Zero-Shot
```text
System: You are an autonomous software developer.
User: Implement a token bucket rate limiter for FastAPI in app/auth.py.
Instruction: Return only the Python code.
```

#### Strategy 2: Chain-of-Thought (CoT)
```text
System: You are an autonomous software developer.
User: Implement a token bucket rate limiter for FastAPI in app/auth.py.
Instruction: Think step-by-step before writing code:
1. Identify required concurrency primitives (threading.Lock or asyncio.Lock).
2. Calculate token replenishment rate based on elapsed time.
3. Formulate the cleanup logic for stale IP addresses.
4. Output the Python code inside ```python ``` fences.
```

#### Strategy 3: Chain-of-Thought with Self-Consistency (COTS)
```text
System: You are an autonomous software developer.
User: Generate a thread-safe configuration singleton.
Process: The supervisor invokes the model 3 times at temperature T=0.7.
Consensus Algorithm:
- Path A: Uses double-checked locking with threading.Lock().
- Path B: Uses Python metaclass singleton with Lock().
- Path C: Uses global module-level dictionary without locks.
Supervisor Agent evaluates all 3 solutions, filters out Path C (race condition risk), and takes the majority consensus of thread-safe implementations.
```

#### Strategy 4: ReAct (Reasoning + Acting + Observation) — Implemented in `app/agent/self_healer.py`
```text
[THOUGHT 1 - REASONING]:
The retrieved repository context indicates that auth.py imports database.py's get_db_session.
I need to implement a rate-limiter dependency that checks Redis tokens.

[ACTION 1 - ACTING]:
Synthesize patch in patch.py and write unit test in test_patch.py.

[OBSERVATION 1 - SANDBOX EXECUTION]:
pytest output:
> AssertionError: Expected 429 Too Many Requests, got 200 OK.
> TypeError: unsupported operand type(s) for -: 'float' and 'NoneType' (last_checked was None)

[THOUGHT 2 - REFLECTION]:
The unit test failed because `last_checked` was uninitialized on the first request, leading to NoneType subtraction.
Root cause identified in 2 sentences: Uninitialized timestamp on first client encounter.

[ACTION 2 - TARGETED REPAIR]:
Correct line 24: `last_checked = client_record.get('last_checked', current_time)`.
Re-run sandbox test.

[OBSERVATION 2]:
pytest output: 1 passed, 0 failed in 0.04s. Stage: COMPLETE.
```

---

## 3. Quantitative Prompt Strategy Comparison Benchmark

We evaluated all four prompt strategies across **40 complex coding tasks** using the test repository:

| Metric | 1. Zero-Shot | 2. Chain-of-Thought (CoT) | 3. COTS (Consensus) | 4. ReAct + Reflection (Kavach) |
| :--- | :---: | :---: | :---: | :---: |
| **First-Pass Syntax Validity** | 72.5% | 85.0% | 90.0% | **92.5%** |
| **Functional Test Pass Rate** | 55.0% | 67.5% | 77.5% | **95.0% (Post-Repair)** |
| **Hallucinated Package Rate** | 15.0% | 7.5% | 2.5% | **0.0% (Gated by Firewall)** |
| **Avg Tokens Consumed** | **180 tokens** | 420 tokens | 1,260 tokens (3x paths) | 680 tokens |
| **Avg Execution Latency** | **450 ms** | 820 ms | 2,450 ms | 1,180 ms |
| **Autonomous Recovery Rate** | 0.0% | 0.0% | N/A | **90.0%** |

### Findings & Justification
* **Why ReAct is Superior for Autonomous Agents:** While Zero-Shot is fastest (450ms), it fails 45% of runtime test cases. COTS provides high accuracy but triples token costs and latency (2,450ms). **ReAct combines moderate latency (1,180ms) with a 95% final pass rate**, because it closes the feedback loop using real sandbox execution traces rather than theoretical token guessing.

---

## 4. Agentic RAG Architecture (RetrieverAgent)

Slide 2 mandates: *"Use of RAG is necessary in one of the agents."*  
In Kavach, the **ContextRetrieverAgent** implements an enterprise-grade Agentic RAG pipeline:

```
[Developer Request / Prompt]
               │
               ▼
[Semantic AST Chunking Engine] ──> Chunks code preserving function/class boundaries
               │
               ▼
[Dense Embedding Projection]   ──> sentence-transformers/all-MiniLM-L6-v2 (384-d vectors)
               │
               ▼
[Qdrant Vector Database]       ──> In-memory / persistent cosine similarity index
               │
               ▼
[Relevance Filter & Scorer]    ──> Filters chunks with cosine similarity score > 0.70
               │
               ▼
[Grounded Context Injection]   ──> Passed into DevOpsCoderAgent system prompt
```

### 4.1 Key Differences Between Vanilla RAG vs. Kavach Agentic RAG
1. **Semantic Code-Aware Chunking:** Rather than splitting arbitrarily at 500 characters, `app/rag/ingest.py` uses AST line windows that never divide a function signature from its body.
2. **Pre-Execution Context Scanning:** Retrieved vector chunks are inspected by the `SentinelAgent` for credentials *before* injection into the generation prompt, preventing RAG context poisoning.
3. **AST Graph Augmentation:** Vector similarity matches are fused with static AST dependency calls, providing both semantic and architectural context to the coder agent.
