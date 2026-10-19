# PROJECT_SPEC.md — Kavach

## Project Identity
**Name:** Kavach
**Full title:** Multilingual Security-Governed Agentic AI DevOps Platform
**Course context:** 7th-semester, 5-credit course project (solo)

## Core Rule
Do not replace Kavach with a generic chatbot, generic code generator, or unrelated AI-DevOps
project. Preserve this scope unless explicitly changed by the project owner.

## Core Thesis
An AI coding agent should not have unrestricted access to a software repository and deployment
pipeline. Kavach is the security and governance layer that continuously checks the agent's
inputs, retrieved context, generated code, generated tests, and CI/CD artifacts before allowing
the workflow to proceed.

## Project Explained Simply
Imagine a very capable AI programmer. You tell it: "Add a password-reset feature." It can read
the project, decide which files matter, write code, create tests, and run checks.

But it can make mistakes — invent a library, modify the wrong files, break another feature,
leak an API key into code, expose personal information, or write code that looks correct but
doesn't actually work.

Kavach is the security guard and supervisor standing between that AI agent and the real
software system. It checks what the agent is doing, what it retrieved, what code it generated,
what the tests say, and what is about to enter CI/CD.

Workflow in one line: **UNDERSTAND → PLAN → READ → PREDICT → BUILD → PROTECT → TEST →
VALIDATE → APPROVE → DEPLOY**

If safe, continue. If dangerous, block or redact. If high-risk/uncertain, ask a human. Record
every important decision in an audit log.

## Professor's Five Project Directions (source: course-provided PDF)
| # | Idea | Core contribution |
|---|------|--------------------|
| 1 | Repository Evolution Intelligence | LLM/RAG predicts which files/functions/APIs/tests a code change may affect |
| 2 | Software History & Development Decisions | RAG over commits/issues/PRs to explain *why* something was implemented a certain way |
| 3 | Intelligent Technical Debt & Refactoring | Combines static analysis + repo context to prioritize and recommend refactors |
| 4 | Evidence-Grounded Code Generation | RAG retrieves real repo code/APIs/deps before generation; validates via compile/test |
| 5 | Developer Intent → Executable DevOps Workflow | NL requirement → plan → RAG → code → tests → CI/CD → report, with human approval checkpoints |

## What We Are Building (Selected Scope)
| Idea | Decision | Role in Kavach |
|------|----------|-----------------|
| #5 | **PRIMARY / BACKBONE** | The end-to-end agentic workflow: intent → plan → RAG → code → tests → CI/CD → report |
| #4 | **PRIMARY** | Repository-aware RAG + evidence-grounded code generation, validated by compile/test |
| #1 | **SELECTED COMPONENT (focused)** | Semantic change-impact analysis: predicts affected files/functions/APIs/tests |
| #2 | NOT CORE | Optional future extension only |
| #3 | NOT CORE | At most, reuse static-analysis checks as a CI quality gate; not a full product |

**Why not all five:** combining all five would create several separate research projects inside
one semester. This selection has one coherent story: an agent performs software-development
work, while Kavach governs and secures that work.

## Core Research Problem
Can a security-governed, multilingual agentic AI system reliably transform natural-language
software requirements into validated repository changes while reducing unsupported code
generation and preventing sensitive or unsafe artifacts from progressing through the
development pipeline?

## System Goal
Combine agentic software development, repository RAG, semantic change-impact analysis,
security governance, multilingual sensitive-information detection, and CI/CD validation into
one controlled workflow.

## Non-Negotiable Quality Rules
- No fake completion — files existing ≠ feature complete; acceptance tests must pass.
- No fake evaluation — metrics must come from real experiments, never fabricated.
- No fake multilingual support — only claim languages that are actually implemented and tested.
- No unrestricted destructive autonomy — use branches/checkpoints and scoped permissions.
- No real secrets or real personal data in tests — synthetic data only.
- No architecture drift — new tools/technologies need a clear justification.
- No giant untested changes — work in small, testable, reviewable milestones.
- Document failures — failure analysis is part of the research value, not a weakness to hide.

## Scope Boundaries — What We Are NOT Building
- Not all five professor projects as separate full products.
- Not a complete technical-debt/refactoring platform.
- Not a complete repository-history intelligence system (unless core is stable early and time remains).
- Not "all Indian languages perfectly supported" — only what is actually tested.
- Not a large multi-agent swarm just to use the phrase "multi-agent."
- Not unrestricted autonomous deployment — policy gates and human approval remain for
  appropriate risk levels.
- Not disproportionate time on frontend styling — functional clarity over visual polish.

## Definition of Done (project-level)
1. Developer can enter a natural-language request.
2. Agent produces a structured plan.
3. Repository RAG retrieves relevant evidence.
4. Change-impact analyzer predicts affected components.
5. Agent generates repository-consistent changes.
6. Generated code/tests are automatically tested.
7. Kavach detects defined sensitive data/secrets.
8. Kavach provides reason/severity and enforcement action for each finding.
9. Allow/redact/block/review paths all work.
10. Explicitly supported multilingual/code-mixed cases are tested and reported.
11. CI/CD executes required gates on repository changes.
12. Human approval can be required for high-risk actions.
13. Audit events are stored safely and are traceable.
14. Dashboard shows workflow/security status live.
15. Real baselines and evaluation metrics exist (not fabricated).
16. Failure cases are analyzed and documented.
17. End-to-end request-to-report demo works.
18. Setup is reproducible from documentation.
19. No major component is mocked while being presented as functional.
