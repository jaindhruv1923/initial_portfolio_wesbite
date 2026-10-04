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

import os
from app.rag.embed_store import index_chunks, search
from app.rag.ingest import ingest_repository
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
    if not semantic_hits:
        # Direct callers may not have ingested the repository yet. Only bootstrap
        # if the vector collection is genuinely empty.
        try:
            from app.rag.embed_store import get_client, COLLECTION_NAME
            client = get_client()
            info = client.get_collection(COLLECTION_NAME)
            is_empty = (info.points_count == 0)
        except Exception:
            is_empty = True

        if is_empty:
            index_chunks(ingest_repository(repo_root))
            semantic_hits = search(change_description, top_k=top_k * 2)

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

    # Fallback keyword matching over dependency graph if semantic search had no hits
    if not file_scores and graph:
        import re
        words = set(re.findall(r"[a-zA-Z]{3,}", change_description.lower()))
        for fpath in graph.keys():
            base = os.path.splitext(os.path.basename(fpath))[0].lower()
            if base in words or any(w in base or base in w for w in words):
                file_scores[fpath] = {"semantic_score": 0.30, "dependency_hit": False}

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
        semantic_component = round(SEMANTIC_WEIGHT * info["semantic_score"], 3)
        dep_component = round(DEPENDENCY_BONUS if info["dependency_hit"] else 0.0, 3)
        score = round(min(semantic_component + dep_component, 1.0), 3)

        reasons = []
        breakdown_items = []
        if info["dependency_hit"]:
            reasons.append("imports/references the most-related file")
            breakdown_items.append(
                "⚡ AST Dependency Link (+0.40): Directly imports or references the modified target module. Breaking changes to exported symbols or signatures will fail runtime imports."
            )
        if info["semantic_score"] > 0:
            reasons.append("semantically related to the change description")
            breakdown_items.append(
                f"🧠 Semantic Alignment (+{semantic_component:.3f}): Vector embedding similarity ({info['semantic_score']:.2f} cosine score) with requested change intent."
            )

        # Determine Significance and Impact Tier
        if score >= 0.35:
            tier = "CRITICAL"
            significance = "Highest Impact — Direct Blast Radius (High Risk of Cascading Failure)"
            action_hint = "Prioritize regression tests and inspect caller interfaces before applying changes."
        elif score >= 0.25:
            tier = "HIGH"
            significance = "High Impact — Direct Import Dependency or Strong Architectural Coupling"
            action_hint = "Verify exported signatures and run integration tests for this module."
        elif score >= 0.15:
            tier = "MODERATE"
            significance = "Moderate Impact — Shared Business Domain / Semantic Overlap"
            action_hint = "Review logic for consistency with shared domain assumptions."
        else:
            tier = "LOW"
            significance = "Low Impact — Peripheral / Advisory Context"
            action_hint = "Standard code review and lint checks are sufficient."

        # Clear human-readable justification explaining exactly WHY this score was assigned:
        if info["dependency_hit"] and info["semantic_score"] > 0:
            score_justification = (
                f"Score {score:.3f} was assigned because this file combines semantic alignment "
                f"(+{semantic_component:.3f}) with an explicit AST import link (+0.400 bonus) to the target module."
            )
        elif info["dependency_hit"]:
            score_justification = (
                f"Score {score:.3f} was assigned because this file has a direct AST import dependency "
                f"(+0.400 bonus) on the modified module, meaning parameter or signature changes will directly ripple here."
            )
        elif info["semantic_score"] > 0:
            score_justification = (
                f"Score {score:.3f} was assigned based on vector embedding semantic similarity "
                f"(+{semantic_component:.3f} from {info['semantic_score']:.2f} cosine distance) matching the requested feature."
            )
        else:
            score_justification = f"Score {score:.3f} reflects low or advisory coupling to the requested change."

        report.append({
            "file_path": file_path,
            "relevance_score": score,
            "score_percentage": int(round(score * 100)),
            "reason": "; ".join(reasons) if reasons else "weak signal",
            "impact_tier": tier,
            "significance": significance,
            "score_justification": score_justification,
            "breakdown": breakdown_items,
            "action_hint": action_hint,
            "semantic_score": round(info["semantic_score"], 3),
            "dependency_hit": info["dependency_hit"],
            "is_highest_impact": False,
        })

    report.sort(key=lambda r: r["relevance_score"], reverse=True)
    if report and report[0]["relevance_score"] > 0:
        report[0]["is_highest_impact"] = True
        if report[0]["impact_tier"] != "CRITICAL":
            report[0]["impact_tier"] = "CRITICAL"
            report[0]["significance"] = "Highest Impact — Primary Target Component"
    return report[:top_k]
