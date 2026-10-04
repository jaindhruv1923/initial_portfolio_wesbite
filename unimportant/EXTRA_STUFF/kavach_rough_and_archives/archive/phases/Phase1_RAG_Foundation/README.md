# Phase 1 — Repository Foundation / RAG

## What was built
- All 15 specification documents (`docs/`) — the full project plan.
- Project folder structure (`backend`, `frontend`, `docs`, `tests`, `data`).
- `backend/app/rag/ingest.py` — walks a repo, reads files, splits into chunks.
- `backend/app/rag/embed_store.py` — embeds chunks (sentence-transformers,
  all-MiniLM-L6-v2) and stores/searches them in a local Qdrant index.
- Multilingual test corpus starter (`data/multilingual_test_corpus.md`) —
  50 sentences across Hindi/Marathi/Tamil/Telugu/Hinglish.
- `backend/requirements.txt`, `backend/schema.sql` — dependency list and DB schema draft.

## Status
Tested and confirmed working: ingested the docs folder, ran semantic search
queries, got genuinely relevant chunks back (not just keyword matches).

## Note
`main.py` is not duplicated here — see Complete_Merged_Project for the full,
current version, since it was extended in every later phase.
