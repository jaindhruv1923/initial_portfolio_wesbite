# DASHBOARD_SPEC.md — Kavach

## Purpose
A human-readable control plane showing what the agent is doing and what Kavach has caught —
this is the primary demo surface.

## Screens / Sections

### 1. Live Findings Feed
- Timestamp, source stage, detected category, severity/confidence, action taken (allow/redact/
  block/review), one-line explanation.

### 2. Workflow Status
- Current stage of the active agent workflow (from AGENT_SPEC.md state machine).
- History of recent workflow runs and their outcomes.

### 3. Audit Log / Compliance View
- Full traceable history of every important decision, exportable as a report (ties to the
  compliance/audit angle in SECURITY_SPEC.md).

### 4. Metrics Panel
- Total detections, blocks, redactions.
- Latency per check.
- Workflow success rate, test pass rate.
- Per-language detection metrics (from MULTILINGUAL_SPEC.md evaluation).

## Agent/User Interface (separate, simpler screen)
- Text box to enter a natural-language development request.
- Shows the agent's plan, retrieved evidence summary, and final result/response.
- Can be used to demonstrate multilingual sensitive-data detection live by typing a Hinglish/
  regional-language message containing fake PII.

## Design Principle
Functional clarity over visual polish. This is a vehicle for demonstrating the engineering
underneath — do not spend disproportionate time on styling.
