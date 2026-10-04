# SECURITY_SPEC.md — Kavach

## Detection Categories
- PII/SPDI-like identifiers and sensitive personal information (e.g. PAN, Aadhaar-like numbers,
  phone numbers, bank account numbers).
- Secrets and credentials — API keys, tokens, passwords.
- Sensitive information appearing in: prompts, retrieved RAG context, generated code, generated
  tests/fixtures, and logs.
- Policy-defined risky content or workflow actions where reliable detection rules can be
  established.

## Where Checks Happen
1. Developer input (the natural-language request)
2. Retrieved RAG context
3. Generated code
4. Generated tests / fixtures
5. CI/CD artifacts
6. Audit/logging paths

## Enforcement Actions
| Action | Meaning |
|--------|---------|
| ALLOW | Safe content continues |
| REDACT | Sensitive value is masked before downstream use |
| BLOCK | Workflow stops |
| REVIEW | Human approval required |
| AUDIT | Event and rationale are persisted regardless of the above |

## Explainability Requirement
Every important security decision must answer:
- What was detected?
- Why was it detected (which rule/pattern/model signal fired)?
- What is its severity/confidence?
- What action was taken?
- Which workflow stage produced the event?

## Severity Tiers (draft — refine during Phase 4)
| Tier | Example | Default action |
|------|---------|------------------|
| Low | A name appearing in casual context | Log only |
| Medium | Phone number, email address | Redact |
| High | PAN, Aadhaar-like number | Block + review |
| Critical | Real API key / credential / password | Block + immediate review |

## Testing Data Rule
Never use real personal information or real credentials in test fixtures. All PII/secret test
cases must use synthetic, clearly-fake values (see `/data/multilingual_test_corpus.md`).

## Open Questions To Resolve During Phase 4
- Exact regex/pattern set per entity type (PAN format, Aadhaar-like format, phone number
  formats used in India).
- Confidence scoring approach (rule-based vs. small classifier vs. hybrid).
- False-positive tuning strategy per severity tier.
