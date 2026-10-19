"""
Dependency graph extraction (Phase 5 — see docs/IMPACT_ANALYSIS_SPEC.md).

Uses Python's built-in `ast` module to find import statements and top-level
function/class definitions in each file, so we have an explicit signal
(alongside semantic similarity in analyzer.py) for change-impact prediction.
No external dependency needed — `ast` ships with Python.
"""

import ast
import os


def _parse_file(file_path: str) -> dict:
    """
    Parse a single .py file and extract:
      - imports: modules/names this file imports
      - defines: top-level function/class names this file defines
    Returns an empty result (not a crash) for unparseable files, since a
    single bad file shouldn't break impact analysis for the whole repo.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
        tree = ast.parse(source)
    except (OSError, SyntaxError, UnicodeDecodeError):
        return {"imports": [], "defines": []}

    imports = []
    defines = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defines.append(node.name)

    return {"imports": imports, "defines": defines}


def build_dependency_graph(repo_root: str) -> dict[str, dict]:
    """
    Walk repo_root for .py files and build a graph:
      { relative_file_path: {"imports": [...], "defines": [...]} }
    """
    graph = {}
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", "venv", ".venv"}]
        for filename in filenames:
            if filename.endswith(".py"):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, repo_root)
                graph[rel_path] = _parse_file(full_path)
    return graph


def find_dependent_files(graph: dict[str, dict], target_module_hint: str) -> list[str]:
    """
    Given a module/function name hint (e.g. a function defined in the
    changed file), return the relative paths of files whose `imports` list
    references it. This is a simple string-containment match — good enough
    as an explicit-dependency signal, not a full import resolver.
    """
    dependents = []
    for file_path, info in graph.items():
        if any(target_module_hint in imp for imp in info["imports"]):
            dependents.append(file_path)
    return dependents
