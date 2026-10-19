# RAG_SPEC.md — Kavach

## Purpose
Give the code-generation agent real, repository-grounded evidence instead of letting it invent
APIs, libraries, or file structures that don't exist in the project (hallucination risk from
Professor Idea #4).

## What Gets Indexed
- Source files (chunked at a sensible granularity — function/class level where possible)
- Project documentation (README, docs folder)
- Dependency manifests (requirements.txt / package.json etc.)
- API definitions / route files
- Coding conventions, if documented

## Pipeline
1. **Ingestion** — walk the repository, extract text from relevant file types.
2. **Chunking** — split into embeddable units (aim for semantically coherent chunks, not
   arbitrary line counts).
3. **Embedding** — generate vector embeddings for each chunk.
4. **Storage** — store in Qdrant (or comparable vector DB) with metadata (file path, chunk type,
   last-modified).
5. **Retrieval** — given a developer request or a planned sub-task, retrieve top-k relevant
   chunks.
6. **Grounding** — pass retrieved chunks to the generation agent as context before it writes any
   code.

## Evaluation (for Research Question 2)
Compare: **LLM without RAG** vs. **LLM + repository RAG**, measuring:
- Compilation success rate
- Functional test-pass rate
- Hallucinated API/library rate
- Number of incorrect implementations
- Retrieval accuracy / relevance
- Response latency
- Token/resource consumption

## Open Questions To Resolve During Phase 2
- Chunk size and overlap strategy.
- Embedding model choice (local vs. API-based — factor in laptop constraints).
- Top-k retrieval count and re-ranking strategy (if any).
