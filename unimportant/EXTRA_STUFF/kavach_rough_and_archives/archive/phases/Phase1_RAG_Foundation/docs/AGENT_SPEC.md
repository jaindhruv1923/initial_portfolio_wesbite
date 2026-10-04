# AGENT_SPEC.md — Kavach

## Role of the Agent
The agent turns a natural-language developer request into a validated, repository-consistent
change, while Kavach governs every step it takes.

## Workflow State Machine (high level)
```
REQUEST_RECEIVED
  → PLANNING
  → CONTEXT_RETRIEVAL (RAG)
  → IMPACT_ANALYSIS
  → GENERATION
  → SECURITY_CHECK (Kavach)
  → TEST_GENERATION
  → BUILD_AND_TEST
  → CICD_GATE
  → [HUMAN_APPROVAL if high-risk]
  → REPORT / DEPLOY
```
Any stage can transition to `BLOCKED` (Kavach denies progress) or `NEEDS_REVIEW` (human
decision required) instead of proceeding.

## Tools the Agent Can Use
- Repository read (file listing, file content, search)
- RAG retrieval query
- Code write/edit (scoped to the working branch, never main directly)
- Test runner invocation
- Git operations (branch, commit, checkpoint) — no force-push, no history rewriting
- CI/CD trigger (or read CI status)

## Permission Principles
- The agent never has unrestricted destructive permissions.
- All code changes happen on a feature branch, never directly on main.
- Git checkpoints are created at stable milestones so any bad autonomous stretch can be rolled
  back.
- High-risk actions (e.g. touching auth/security-relevant files, deleting files, modifying CI
  config) require explicit human approval before proceeding.

## What "Bounded Milestone" Means Here
The agent should be given one clearly-scoped subsystem or task at a time (e.g. "implement
repository ingestion for RAG"), not "build the whole project." Each milestone has:
- A clear acceptance criterion
- Tests that must pass
- A Git checkpoint on completion

## Non-Goals for the Agent
- Do not let the agent choose the project's core architecture unsupervised — major
  architectural decisions require human sign-off (see PROJECT_SPEC.md non-negotiable rules).
- Do not let the agent fabricate evaluation results or claim untested features work.
