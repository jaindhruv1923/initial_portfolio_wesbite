# MULTILINGUAL_SPEC.md — Kavach

## Principle
Multilingual and code-mixed security detection is a differentiator for Kavach, but the project
must never claim "all Indian languages are perfectly supported" without actually implementing
and evaluating them. **Only claim what is tested.**

## Target Languages (initial scope — adjust as time allows)
1. Hindi
2. Marathi
3. Tamil
4. Telugu
5. Hinglish / Hindi-English code-mixed

The architecture must make it easy to plug in additional languages later without redesigning
the security engine (i.e. detection logic should not be hardcoded to one language's grammar).

## Example Target Behavior
- Hindi: "मेरा PAN नंबर ABCDE1234F है" → detect PAN
- Marathi: "माझा PAN नंबर ABCDE1234F आहे" → detect PAN
- Tamil: "என் PAN number ABCDE1234F" → detect PAN
- Telugu: "నా PAN number ABCDE1234F" → detect PAN
- Hinglish: "bro mera PAN ABCDE1234F hai" → detect PAN
- Mixed-script / mixed-language inputs where the sensitive entity is surrounded by another
  language must also be handled.

## Evaluation Plan
Build a controlled multilingual test corpus (see `/data/multilingual_test_corpus.md`) and report,
**per language and per entity type**:
- Precision
- Recall
- F1
- False positives
- False negatives
- Latency

## Non-Goals
- Do not attempt all 22 official Indian languages this semester.
- Do not claim voice-input handling.
- Do not claim robustness against deliberate adversarial evasion unless specifically tested.
