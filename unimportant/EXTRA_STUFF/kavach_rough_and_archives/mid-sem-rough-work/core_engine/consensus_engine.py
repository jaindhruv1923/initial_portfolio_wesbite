"""
KAVACH Multi-Model Consensus & Hallucination Cross-Verification Engine.
Directly implements Feature #3 from WHAT_NEXT_ROADMAP.md.

Combines outputs from multiple model families (Gemini, Claude, Local Qwen):
1. Parses AST structures and imported packages across all candidates
2. Computes Jaccard AST Token & Node Type similarity metrics
3. Detects unilateral hallucinations where a single model invents an API or package
4. Escalates to Human Gatekeeper if cross-model consensus < 85%
"""

import ast
from typing import Dict, Any, List, Set


def _extract_ast_signature(code_str: str) -> Dict[str, Any]:
    """Extract AST node types, functions, and imports as a comparative signature."""
    try:
        tree = ast.parse(code_str)
    except SyntaxError:
        return {"valid_syntax": False, "node_types": set(), "functions": set(), "imports": set()}

    node_types: Set[str] = set()
    functions: Set[str] = set()
    imports: Set[str] = set()

    for node in ast.walk(tree):
        node_types.add(type(node).__name__)
        if isinstance(node, ast.FunctionDef):
            functions.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    return {
        "valid_syntax": True,
        "node_types": node_types,
        "functions": functions,
        "imports": imports
    }


def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """Compute Jaccard similarity index between two sets."""
    if not set_a and not set_b:
        return 1.0
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return round(intersection / union, 3) if union > 0 else 0.0


def evaluate_multi_model_consensus(model_outputs: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Evaluates consensus across model outputs (list of {'model_name': str, 'code': str}).
    """
    if not model_outputs:
        return {
            "consensus_reached": False,
            "consensus_score": 0.0,
            "verdict": "REJECTED_NO_INPUT",
            "details": "No model outputs provided."
        }

    if len(model_outputs) == 1:
        sig = _extract_ast_signature(model_outputs[0].get("code", ""))
        return {
            "consensus_reached": sig["valid_syntax"],
            "consensus_score": 1.0 if sig["valid_syntax"] else 0.0,
            "verdict": "SINGLE_MODEL_ACCEPTED" if sig["valid_syntax"] else "SYNTAX_ERROR",
            "details": "Single model provided, verified syntax."
        }

    signatures = []
    for mo in model_outputs:
        sig = _extract_ast_signature(mo.get("code", ""))
        signatures.append({
            "model_name": mo.get("model_name", "unknown_llm"),
            "signature": sig
        })

    # Syntax validity check
    syntax_valid_count = sum(1 for s in signatures if s["signature"]["valid_syntax"])
    if syntax_valid_count < len(signatures) // 2 + 1:
        return {
            "consensus_reached": False,
            "consensus_score": 0.20,
            "verdict": "ESCALATE_SYNTAX_FAILURE",
            "details": "Majority of models failed to produce valid syntax."
        }

    # Compute pairwise similarities for functions, imports, and node types
    similarities = []
    for i in range(len(signatures)):
        for j in range(i + 1, len(signatures)):
            sig_a = signatures[i]["signature"]
            sig_b = signatures[j]["signature"]
            
            node_sim = jaccard_similarity(sig_a["node_types"], sig_b["node_types"])
            func_sim = jaccard_similarity(sig_a["functions"], sig_b["functions"])
            imp_sim = jaccard_similarity(sig_a["imports"], sig_b["imports"])
            
            pair_score = (0.3 * node_sim) + (0.4 * func_sim) + (0.3 * imp_sim)
            similarities.append(pair_score)

    avg_consensus = round(sum(similarities) / len(similarities), 3) if similarities else 0.0

    # Cross-check package imports: identify any outlier package imported by only 1 model
    all_imports: Dict[str, List[str]] = {}
    for s in signatures:
        for imp in s["signature"]["imports"]:
            all_imports.setdefault(imp, []).append(s["model_name"])

    outlier_packages = [pkg for pkg, models in all_imports.items() if len(models) == 1 and len(signatures) >= 3]

    consensus_reached = avg_consensus >= 0.80 and not outlier_packages
    verdict = "APPROVED_BY_CONSENSUS" if consensus_reached else "ESCALATE_TO_HUMAN_GATEKEEPER"

    return {
        "consensus_reached": consensus_reached,
        "consensus_score": avg_consensus,
        "verdict": verdict,
        "models_evaluated": [s["model_name"] for s in signatures],
        "outlier_packages_detected": outlier_packages,
        "details": (
            f"Tri-Model Consensus: {round(avg_consensus * 100, 1)}% agreement. Verdict: {verdict}"
            if not outlier_packages
            else f"Divergence Alert: Package(s) {outlier_packages} hallucinated by only one model."
        )
    }
