# CICD_SPEC.md — Kavach

## Purpose
Automate build, test, and security validation for every change the agent proposes, using
GitHub Actions.

## Trigger
A pull request (opened by the agent on a feature branch, or manually) triggers the pipeline.

## Pipeline Stages (draft)
1. **Checkout** the PR branch.
2. **Install dependencies** (backend + frontend as applicable).
3. **Lint / static checks.**
4. **Run unit tests.**
5. **Run integration tests** (agent workflow smoke test, if feasible in CI).
6. **Kavach security gate** — run the security engine against the diff's generated
   code/tests/context; fail the pipeline on BLOCK-severity findings.
7. **Report generation** — summarize results as a PR comment or artifact (files changed,
   impact-analysis summary, test results, security findings).
8. **Gate decision** — pass / fail / needs-review, recorded in the audit store.

## What Counts as a Passing Gate
- All required tests pass.
- No unresolved BLOCK-severity Kavach findings.
- REVIEW-severity findings have an explicit human decision recorded.

## Non-Goals
- Do not build a full production deployment pipeline — a working CI validation gate with the
  security check integrated is sufficient for this project's scope.
