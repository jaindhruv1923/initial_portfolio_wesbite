import os
from typing import List, Dict, Any

IGNORE_DIRS = {
    ".git", "__pycache__", "node_modules", "venv", ".venv", 
    "env", ".pytest_cache", ".idea", ".vscode", "dist", "build"
}

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", 
    ".json", ".sql", ".md", ".sh", ".yml", ".yaml", ".txt"
}

def ingest_repository(repo_path: str, chunk_lines: int = 50) -> Dict[str, Any]:
    """
    Ingests all source code files from a directory, creating searchable chunks.
    """
    repo_path = os.path.abspath(repo_path)
    if not os.path.exists(repo_path):
        raise ValueError(f"Repository path does not exist: {repo_path}")

    files_list = []
    chunks = []
    total_lines = 0

    for root, dirs, files in os.walk(repo_path):
        # Filter out ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ALLOWED_EXTENSIONS or file in {"Dockerfile", "Makefile"}:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, repo_path).replace("\\", "/")

                try:
                    with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                except Exception as e:
                    continue

                line_count = len(lines)
                total_lines += line_count
                files_list.append({
                    "path": rel_path,
                    "lines": line_count,
                    "ext": ext
                })

                # Chunking file
                for i in range(0, max(1, line_count), chunk_lines):
                    chunk_text = "".join(lines[i:i + chunk_lines])
                    if chunk_text.strip():
                        chunks.append({
                            "file": rel_path,
                            "start_line": i + 1,
                            "end_line": min(i + chunk_lines, line_count),
                            "content": chunk_text
                        })

    return {
        "repo_path": repo_path,
        "files_count": len(files_list),
        "total_lines": total_lines,
        "chunks_count": len(chunks),
        "files": files_list,
        "chunks": chunks
    }
