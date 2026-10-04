# COMPETITIVE_ANALYSIS.md — Kavach

> Purpose: an honest, defensible comparison against existing tools — for the report and for
> answering "why not just use X" questions during evaluation. Overclaiming novelty here will
> hurt credibility; the goal is an accurate positioning, not a "nobody does this" claim.

## Existing Tools in This Space

| Tool | What it does | Where it differs from Kavach |
|------|---------------|-------------------------------|
| **AgentOps.ai / LangSmith / Langfuse** | Trace and observe AI agent behavior; log prompts, tool calls, outputs for debugging | Primarily English-first; typically send traces to the vendor's own cloud for analysis, which conflicts with data-localization requirements for Indian regulated sectors |
| **Fiddler / Galileo / Arize** | Enterprise AI monitoring and governance, some with on-premise/VPC deployment and compliance certifications (SOC 2, HIPAA) | Not specifically built or evaluated for Hindi-English code-mixed / Indian-language inputs |
| **Lyzr (India-based)** | Enterprise agent platform with built-in compliance controls, audit logging, PII guarding, used in BFSI/healthcare | Closest existing comparison; a full commercial platform rather than a focused, open, student-built system with a published multilingual evaluation |

## What Genuinely Doesn't Exist (as far as could be found)
A **published, evaluated, open implementation** that specifically targets **PII/secret detection
in Hindi-English code-mixed conversational text**, combined with a **fully local/self-hosted**
deployment model aimed at Indian data-localization requirements (RBI-style rules).

## Honest Positioning Statement (for the report / viva)
> "Tools like Lyzr, Langfuse, and Fiddler already provide agent observability and compliance
> controls, some with on-premise deployment options. Kavach does not claim to replace these —
> it focuses on a narrower, specifically under-evaluated gap: sensitive-data detection in
> Hindi-English code-mixed text, combined with a fully local architecture built and evaluated
> as part of this project rather than adopted as a third-party SaaS product."

## Why Not Just Call an LLM API for Detection
- Sending message content to an external LLM API (including Claude/GPT) means the data has
  already left the local environment — which defeats the compliance premise Kavach is built
  around.
- A single prompt call can classify one message; it does not provide the real-time
  interception, audit-log format, low-latency local inference, or evaluated multilingual
  accuracy that a deployed system needs.

## Answering "Couldn't a bigger company just build this?"
Yes, theoretically — data availability is not the bottleneck, engineering effort and market
priority are. No published tool currently claims and evaluates Hindi-English code-mixed PII
detection specifically. Kavach's contribution is a working, evaluated implementation of that
gap, not a claim of permanent or exclusive novelty.
