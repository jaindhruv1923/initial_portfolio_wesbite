"""
Change-impact analyzer (Phase 5 — Professor Idea #1 focused slice, see
docs/IMPACT_ANALYSIS_SPEC.md).

Combines two signals to predict which files a proposed change might affect:
  1. Semantic similarity — reuses Phase 1's RAG search() over the already
     -indexed repository chunks.
  2. Explicit dependency signal — reuses Phase 5's dependency_graph.py to
     check whether other files import/reference the changed area.

This is a focused component, not a full repository-intelligence product —
see docs/IMPACT_ANALYSIS_SPEC.md's scope discipline note.
"""

from app.rag.embed_store import search
from app.impact.dependency_graph import build_dependency_graph, find_dependent_files

# Weights for combining the two signals into one relevance score.
SEMANTIC_WEIGHT = 0.6
DEPENDENCY_WEIGHT = 0.4
DEPENDENCY_BONUS = 0.4  # flat bonus added when a file is an explicit dependent


def analyze_impact(change_description: str, repo_root: str, top_k: int = 5) -> list[dict]:
    """
    Given a natural-language description of a proposed change, return a
    ranked list of files likely to be affected, combining semantic search
    with explicit import-graph dependents.

    Returns: list of {"file_path": str, "relevance_score": float, "reason": str}
    """
    # --- Signal 1: semantic similarity via existing RAG index ---
    semantic_hits = search(change_description, top_k=top_k * 2)  # over-fetch, then merge/rank

    # Deduplicate to file level — a file may have multiple matching chunks;
    # keep its best (highest) semantic score.
    file_scores: dict[str, dict] = {}
    for hit in semantic_hits:
        fp = hit["file_path"]
        if fp not in file_scores or hit["score"] > file_scores[fp]["semantic_score"]:
            file_scores[fp] = {"semantic_score": hit["score"], "dependency_hit": False}

    # --- Signal 2: explicit dependency graph ---
    try:
        graph = build_dependency_graph(repo_root)
    except Exception:
        graph = {}

    # Use the top semantic hit's file (most likely to be the "changed" file)
    # as the hint for finding its dependents, if any semantic hits exist.
    if file_scores:
        top_file = max(file_scores.items(), key=lambda kv: kv[1]["semantic_score"])[0]
        # Use the file's own name (without extension) as a naive import hint.
        module_hint = top_file.replace("\\", "/").split("/")[-1].replace(".py", "")
        dependents = find_dependent_files(graph, module_hint)
        for dep_file in dependents:
            if dep_file not in file_scores:
                file_scores[dep_file] = {"semantic_score": 0.0, "dependency_hit": True}
            else:
                file_scores[dep_file]["dependency_hit"] = True

    # --- Combine into a final ranked report ---
    report = []
    for file_path, info in file_scores.items():
        score = SEMANTIC_WEIGHT * info["semantic_score"]
        if info["dependency_hit"]:
            score += DEPENDENCY_BONUS
        reasons = []
        if info["semantic_score"] > 0:
            reasons.append("semantically related to the change description")
        if info["dependency_hit"]:
            reasons.append("imports/references the most-related file")
        report.append({
            "file_path": file_path,
            "relevance_score": round(min(score, 1.0), 3),
            "reason": "; ".join(reasons) if reasons else "weak signal",
        })

    report.sort(key=lambda r: r["relevance_score"], reverse=True)
    return report[:top_k]
