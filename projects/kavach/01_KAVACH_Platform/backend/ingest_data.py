import sys
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).resolve().parent))

from app.rag.ingest import ingest_repository
from app.rag.embed_store import index_chunks

def ingest():
    repo_path = "app"
    print(f"Ingesting {repo_path}...")
    chunks = ingest_repository(repo_path)
    count = index_chunks(chunks)
    print(f"Indexed {count} chunks.")

if __name__ == "__main__":
    ingest()
