"""
Repository ingestion + chunking (Phase 1 — see docs/RAG_SPEC.md).

Walks a repository, reads text-like source files, and splits them into
chunks suitable for embedding. Kept deliberately simple for a first pass —
refine chunk boundaries (e.g. per-function splitting) later if evaluation
shows plain line-based chunking isn't good enough.
"""

import os
from dataclasses import dataclass

# File extensions we'll actually try to read as text/code.
INCLUDED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".md", ".txt",
    ".json", ".yaml", ".yml", ".sql", ".html", ".css",
}

# Folders we never want to walk into.
EXCLUDED_DIRS = {
    ".git", "__pycache__", "node_modules", "venv", ".venv",
    "dist", "build", ".idea", ".vscode",
}

# Roughly how many characters per chunk (character-based for now —
# simple and language-agnostic; token-based chunking can replace this later).
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


@dataclass
class Chunk:
    file_path: str
    chunk_index: int
    text: str


def iter_repository_files(repo_root: str):
    """Yield absolute paths of every text-like file under repo_root."""
    for dirpath, dirnames, filenames in os.walk(repo_root):
        # prune excluded directories in-place so os.walk skips them
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in INCLUDED_EXTENSIONS:
                yield os.path.join(dirpath, filename)


def chunk_text(text: str, file_path: str) -> list[Chunk]:
    """Split a single file's text into overlapping chunks."""
    chunks = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk_str = text[start:end]
        if chunk_str.strip():
            chunks.append(Chunk(file_path=file_path, chunk_index=index, text=chunk_str))
            index += 1
        if end == len(text):
            break
        start = end - CHUNK_OVERLAP
    return chunks


def ingest_repository(repo_root: str) -> list[Chunk]:
    """Read every eligible file under repo_root and return all chunks."""
    all_chunks: list[Chunk] = []
    for file_path in iter_repository_files(repo_root):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError):
            continue  # skip unreadable files rather than crash the whole ingest
        rel_path = os.path.relpath(file_path, repo_root)
        all_chunks.extend(chunk_text(text, rel_path))
    return all_chunks
