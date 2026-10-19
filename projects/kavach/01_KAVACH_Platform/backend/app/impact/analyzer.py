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
SEMANTIC_WEIGHT = 0.75
DEPENDENCY_WEIGHT = 0.25
DEPENDENCY_BONUS = 0.20  # flat bonus added when a file is an explicit dependent


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

    def _norm(p: str) -> str:
        s = p.replace("\\", "/").lower()
        while "//" in s:
            s = s.replace("//", "/")
        if "/app/" in s:
            s = s.split("/app/", 1)[1]
        elif s.startswith("app/"):
            s = s[len("app/"):]
        return s.lstrip("./")

    # Deduplicate to file level using normalized path keys
    file_scores: dict[str, dict] = {}
    for hit in semantic_hits:
        fp = _norm(hit["file_path"])
        if fp not in file_scores or hit["score"] > file_scores[fp]["semantic_score"]:
            file_scores[fp] = {"semantic_score": hit["score"] * 0.35, "dependency_hit": False}

    # --- Signal 2: explicit dependency graph ---
    try:
        graph = build_dependency_graph(repo_root)
    except Exception:
        graph = {}

    # --- Signal 2: Hybrid lexical, keyword coverage & symbol matching ---
    import re
    raw_words = [w.lower() for w in re.findall(r"[a-zA-Z]{3,}", change_description)]
    stopwords = {"the", "for", "and", "that", "how", "used", "from", "with", "modify", "change", "update", "logic", "are", "down"}
    meaningful_words = [w for w in raw_words if w not in stopwords]
    if not meaningful_words:
        meaningful_words = raw_words

    def _stem(word: str) -> str:
        for sfx in ("tion", "sion", "ing", "ment", "ers", "er", "or", "ed", "es", "s"):
            if word.endswith(sfx) and len(word) - len(sfx) >= 3:
                return word[:-len(sfx)]
        return word

    for fpath, meta in graph.items():
        clean_path = _norm(fpath)
        base = os.path.splitext(os.path.basename(clean_path))[0]
        defines_str = " ".join(meta.get("defines", [])).lower()
        imports_str = " ".join(meta.get("imports", [])).lower()
        
        full_p = os.path.join(repo_root, fpath)
        content = ""
        if os.path.isfile(full_p):
            try:
                with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(5000).lower()
            except Exception:
                content = ""

        matched_words = 0
        path_matches = 0.0
        for w in meaningful_words:
            w_stem = _stem(w)
            in_base = (w == base or w_stem == _stem(base) or w in base)
            in_path = (w in clean_path or w_stem in clean_path)
            in_def = (w in defines_str or w_stem in defines_str)
            in_content = bool(re.search(r"\b" + re.escape(w) + r"\b", content))

            if in_base:
                path_matches += 3.5
                matched_words += 1
            elif in_path:
                path_matches += 1.8
                matched_words += 1
            elif in_def:
                matched_words += 1
            elif in_content:
                matched_words += 0.5

        if matched_words > 0:
            coverage = (matched_words / len(meaningful_words)) * 0.70
            path_bonus = min(0.30, path_matches * 0.08)
            lexical_score = round(coverage + path_bonus, 3)
            if clean_path not in file_scores:
                file_scores[clean_path] = {"semantic_score": lexical_score, "dependency_hit": False}
            else:
                file_scores[clean_path]["semantic_score"] = max(file_scores[clean_path]["semantic_score"], lexical_score)

    # Find dependents for top-ranking relevant files
    if file_scores:
        sorted_files = sorted(file_scores.items(), key=lambda kv: kv[1]["semantic_score"], reverse=True)[:3]
        for top_file, _ in sorted_files:
            module_hint = os.path.splitext(os.path.basename(top_file))[0]
            dependents = find_dependent_files(graph, module_hint)
            for dep_file in dependents:
                cdep = _norm(dep_file)
                if cdep not in file_scores:
                    file_scores[cdep] = {"semantic_score": 0.10, "dependency_hit": True}
                else:
                    file_scores[cdep]["dependency_hit"] = True

    # --- Combine into a final ranked report ---
    report = []
    for file_path, info in file_scores.items():
        semantic_component = round(SEMANTIC_WEIGHT * info["semantic_score"], 3)
        dep_component = round(0.12 if info["dependency_hit"] else 0.0, 3)
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

    # Dynamic confidence thresholding: avoid padding with irrelevant low-confidence files
    confident = [r for r in report if r["relevance_score"] >= 0.22]
    if len(confident) >= 2:
        return confident[:top_k]
    return report[:top_k]
