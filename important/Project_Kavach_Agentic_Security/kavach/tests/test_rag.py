"""
Phase 1 - Repository Ingestion & RAG Tests
Tests for repository walking, chunking, embedding, and vector search.
"""

import pytest
import os
import tempfile
from app.rag.ingest import (
    ingest_repository,
    chunk_text,
    iter_repository_files,
    Chunk,
    CHUNK_SIZE,
)
from app.rag.embed_store import (
    index_chunks,
    search,
    get_client,
    get_model,
)


class TestIngestion:
    """Test repository ingestion (chunking and file iteration)."""

    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        text = "a" * (CHUNK_SIZE * 2)  # Two chunk-sizes of text
        chunks = chunk_text(text, "test.py")
        
        assert len(chunks) >= 2, "Should create multiple chunks for large text"
        assert chunks[0].file_path == "test.py"
        assert all(chunk.text.strip() for chunk in chunks), "All chunks should have non-empty text"
    
    def test_chunk_text_empty(self):
        """Test that empty text produces no chunks."""
        chunks = chunk_text("", "empty.py")
        assert len(chunks) == 0
    
    def test_chunk_text_small(self):
        """Test that small text produces single chunk."""
        text = "small content"
        chunks = chunk_text(text, "small.py")
        assert len(chunks) == 1
        assert chunks[0].text == text
    
    def test_chunk_text_overlap(self):
        """Test that chunks overlap as expected."""
        text = "x" * (CHUNK_SIZE + 100)
        chunks = chunk_text(text, "overlap.py")
        
        assert len(chunks) >= 2
        # Second chunk should start before first chunk ends (overlap)
        first_chunk_text = chunks[0].text
        second_chunk_text = chunks[1].text
        assert first_chunk_text[-100:] in (second_chunk_text[:200] or ""), "Should have overlap"

    def test_iter_repository_files(self, sample_repository_path):
        """Test that repository file iterator finds all eligible files."""
        files = list(iter_repository_files(sample_repository_path))
        
        assert len(files) > 0, "Should find files"
        # Check that .py files are included
        py_files = [f for f in files if f.endswith(".py")]
        assert len(py_files) >= 3, "Should find all Python files"
    
    def test_ingest_repository(self, sample_repository_path):
        """Test full repository ingestion."""
        chunks = ingest_repository(sample_repository_path)
        
        assert len(chunks) > 0, "Should ingest chunks"
        assert all(isinstance(c, Chunk) for c in chunks)
        assert all(c.file_path for c in chunks), "All chunks should have file paths"


class TestEmbedding:
    """Test embedding and vector storage."""

    def test_get_model(self):
        """Test that model is loaded correctly."""
        model = get_model()
        assert model is not None
        assert hasattr(model, "encode"), "Model should have encode method"
    
    def test_model_singleton(self):
        """Test that model is cached (singleton)."""
        model1 = get_model()
        model2 = get_model()
        assert model1 is model2, "Model should be cached"

    def test_get_client(self):
        """Test that Qdrant client initializes."""
        client = get_client()
        assert client is not None
        assert hasattr(client, "upsert"), "Client should have upsert method"
    
    def test_index_chunks(self, sample_chunk):
        """Test indexing chunks into Qdrant."""
        indexed_count = index_chunks([sample_chunk])
        
        assert indexed_count == 1, "Should index exactly 1 chunk"
    
    def test_index_multiple_chunks(self):
        """Test indexing multiple chunks."""
        chunks = [
            Chunk(file_path="a.py", chunk_index=0, text="Authentication logic"),
            Chunk(file_path="b.py", chunk_index=0, text="Database models"),
            Chunk(file_path="c.py", chunk_index=0, text="API endpoints"),
        ]
        indexed_count = index_chunks(chunks)
        assert indexed_count == 3
    
    def test_index_empty_chunks(self):
        """Test indexing empty chunk list."""
        indexed_count = index_chunks([])
        assert indexed_count == 0

    def test_search_basic(self, sample_chunk):
        """Test basic vector search."""
        index_chunks([sample_chunk])
        
        results = search("authentication", top_k=1)
        assert len(results) > 0, "Should find at least one result"
        assert results[0]["file_path"] == "auth/login.py"
        assert "score" in results[0]
        assert "text" in results[0]
    
    def test_search_empty_query(self):
        """Test search with empty query."""
        results = search("", top_k=5)
        # Should return results even with empty query (vector is all zeros)
        assert isinstance(results, list)
    
    def test_search_top_k(self):
        """Test that top_k parameter is respected."""
        chunks = [
            Chunk(file_path="f1.py", chunk_index=0, text="Authentication"),
            Chunk(file_path="f2.py", chunk_index=0, text="Authorization"),
            Chunk(file_path="f3.py", chunk_index=0, text="API authentication"),
        ]
        index_chunks(chunks)
        
        results = search("authentication", top_k=2)
        assert len(results) <= 2, f"Should return at most 2 results, got {len(results)}"
    
    def test_search_results_have_required_fields(self, sample_chunk):
        """Test that search results have all required fields."""
        index_chunks([sample_chunk])
        results = search("auth", top_k=1)
        
        if results:
            result = results[0]
            assert "score" in result
            assert "file_path" in result
            assert "chunk_index" in result
            assert "text" in result


class TestRAGIntegration:
    """Integration tests for full RAG pipeline."""

    def test_ingest_and_search_workflow(self, sample_repository_path):
        """Test complete ingest -> search workflow."""
        # Ingest
        chunks = ingest_repository(sample_repository_path)
        indexed = index_chunks(chunks)
        
        assert indexed > 0, "Should have indexed chunks"
        
        # Search
        results = search("authentication", top_k=3)
        assert len(results) > 0, "Should find auth-related content"
        
        # Results should be sorted by score (descending)
        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True), "Results should be sorted by score"
    
    def test_rag_with_semantic_query(self, sample_repository_path):
        """Test RAG with conceptual English queries."""
        chunks = ingest_repository(sample_repository_path)
        index_chunks(chunks)
        
        # Test semantic search query
        results = search("user identity verification and credentials", top_k=3)
        assert isinstance(results, list)
        assert len(results) > 0
