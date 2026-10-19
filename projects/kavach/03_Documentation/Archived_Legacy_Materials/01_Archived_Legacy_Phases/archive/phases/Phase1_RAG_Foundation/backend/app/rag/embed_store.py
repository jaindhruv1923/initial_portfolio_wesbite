"""
Embedding + vector storage (Phase 1 — see docs/RAG_SPEC.md).

Uses a small, CPU-friendly sentence-transformers model (all-MiniLM-L6-v2 —
~80MB, fast on CPU, no GPU required) and a local on-disk Qdrant instance
(no Docker/server needed for development).
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

from app.rag.ingest import Chunk

COLLECTION_NAME = "kavach_repo_chunks"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # 384-dim, small, CPU-friendly
QDRANT_PATH = "./qdrant_storage"  # local on-disk storage, gitignored

_model = None
_client = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(path=QDRANT_PATH)
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
