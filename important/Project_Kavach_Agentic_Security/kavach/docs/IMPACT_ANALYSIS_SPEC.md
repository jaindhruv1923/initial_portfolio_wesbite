# IMPACT_ANALYSIS_SPEC.md — Kavach

## Purpose (Professor Idea #1, focused slice)
Given a proposed code change, predict which other files/functions/APIs/tests may be affected —
using semantic understanding (via RAG/embeddings), not just keyword/dependency search.

## Approach
1. Represent the proposed change (diff or planned modification) as a query.
2. Retrieve semantically related chunks from the indexed repository (reuses RAG_SPEC.md
   infrastructure).
3. Rank candidate affected files/functions by relevance.
4. Cross-reference with any explicit dependency graph available (imports, function calls) as a
   secondary signal.
5. Produce a ranked impact report: "This change may affect X, Y, Z. Consider re-running tests
   A, B."

## Evaluation (for Research Question 3)
Create a small set of test changes where the **actual affected files are known ahead of time**
(you construct these deliberately in a sample repo or in Kavach's own codebase). Compare:
**Actual affected files vs. Predicted affected files**, measuring:
- Precision
- Recall
- F1-score
- False positives
- False negatives
- Processing time
- Token/resource consumption

## Scope Discipline
This is a **focused component**, not a full standalone repository-intelligence product. Keep it
scoped to: given a change, predict affected components, and evaluate that prediction. Do not
expand into a general-purpose code-search product.
