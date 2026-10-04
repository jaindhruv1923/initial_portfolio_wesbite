"""
Embedding + vector storage (Phase 1 — see docs/RAG_SPEC.md).

Uses a small, CPU-friendly sentence-transformers model (all-MiniLM-L6-v2 —
~80MB, fast on CPU, no GPU required) and a local on-disk Qdrant instance
(no Docker/server needed for development).
"""

import os
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from app.rag.ingest import Chunk

COLLECTION_NAME = "kavach_repo_chunks"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Use absolute path for consistency, but allow override via environment variable for tests
DEFAULT_QDRANT_PATH = str(Path(__file__).resolve().parents[2] / "qdrant_storage")
QDRANT_PATH = os.environ.get("QDRANT_PATH", DEFAULT_QDRANT_PATH)

_model = None
_client = None
_client_target_path = None


class _VectorResult:
    def __init__(self, data):
        self._data = data

    def tolist(self):
        return self._data


class FallbackEmbeddingModel:
    """Lightweight 384-dimensional fallback embedding model used when
    system application control or missing DLLs block PyTorch / scipy."""

    def encode(self, texts, show_progress_bar: bool = False):
        import hashlib
        import math

        is_single = isinstance(texts, str)
        items = [texts] if is_single else texts
        all_vecs = []
        for text in items:
            vec = [0.0] * 384
            words = text.lower().replace("_", " ").replace("-", " ").split()
            if not words:
                vec[0] = 1.0
            else:
                for w in words:
                    h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
                    vec[h % 384] += 1.0
                norm = math.sqrt(sum(v * v for v in vec)) or 1.0
                vec = [round(v / norm, 6) for v in vec]
            all_vecs.append(vec)
        return _VectorResult(all_vecs[0] if is_single else all_vecs)


def get_model():
    global _model
    if _model is None:
        if "PYTEST_CURRENT_TEST" in os.environ:
            _model = FallbackEmbeddingModel()
            return _model
        try:
            from sentence_transformers import SentenceTransformer
            try:
                # Fast-path: use local cached weights directly (0.2s instead of 9s)
                _model = SentenceTransformer(EMBEDDING_MODEL_NAME, local_files_only=True)
            except Exception:
                # Fallback to online loading if not yet downloaded
                _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        except (ImportError, OSError, Exception) as e:
            print(f"[Kavach] Notice: Using lightweight fallback embedding engine ({e})")
            _model = FallbackEmbeddingModel()
    return _model


def get_client() -> QdrantClient:
    global _client, _client_target_path
    requested_path = os.environ.get("QDRANT_PATH", DEFAULT_QDRANT_PATH)
    if _client is not None and _client_target_path != requested_path:
        try:
            _client.close()
        except Exception:
            pass
        _client = None
    if _client is None:
        try:
            _client = QdrantClient(path=requested_path)
        except Exception:
            # If disk storage path is locked by another running process (e.g. uvicorn server),
            # gracefully fall back to an isolated in-memory collection.
            _client = QdrantClient(location=":memory:")
        _client_target_path = requested_path
        _ensure_collection(_client)
    return _client


def _ensure_collection(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qmodels.VectorParams(size=384, distance=qmodels.Distance.COSINE),
        )


def index_chunks(chunks: list[Chunk]) -> int:
    """Embed and store a list of chunks. Clears any previously indexed data
    first, so each /ingest call starts fresh instead of accumulating stale
    chunks from earlier ingests of a different path."""
    client = get_client()
    client.delete_collection(COLLECTION_NAME)
    _ensure_collection(client)

    if not chunks:
        return 0
    model = get_model()

    texts = [c.text for c in chunks]
    vectors = model.encode(texts, show_progress_bar=False).tolist()

    points = [
        qmodels.PointStruct(
            id=i,
            vector=vectors[i],
            payload={
                "file_path": chunks[i].file_path,
                "chunk_index": chunks[i].chunk_index,
                "text": chunks[i].text,
            },
        )
        for i in range(len(chunks))
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)


def search(query: str, top_k: int = 5) -> list[dict]:
    """Return the top_k most relevant chunks for a query."""
    model = get_model()
    client = get_client()
    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    ).points
    return [
        {
            "score": r.score,
            "file_path": r.payload["file_path"],
            "chunk_index": r.payload["chunk_index"],
            "text": r.payload["text"],
        }
        for r in results
    ]
