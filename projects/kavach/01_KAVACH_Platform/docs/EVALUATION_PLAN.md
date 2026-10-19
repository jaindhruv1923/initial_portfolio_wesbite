# EVALUATION_PLAN.md — Kavach

## Principle
A working demo alone is not sufficient. Every major claim of "improvement" needs a baseline
comparison and a real, reproducible metric — not an assertion.

## Experiments

| Experiment | Baseline | Kavach / advanced system | Metrics |
|------------|----------|----------------------------|---------|
| Security detection | Baseline detector / unprotected agent | Kavach multilingual security engine | Precision, Recall, F1, FP, FN, latency |
| RAG / code generation | LLM without repository RAG | LLM + repository evidence | Compilation success, test-pass rate, hallucinated API/library rate, retrieval accuracy |
| Change impact | Keyword/textual or conventional dependency approach | Semantic repository impact analyzer | Precision, Recall, F1, FP, FN, time/resources |
| Agentic DevOps workflow | Developer + conventional tools | Developer + agentic Kavach workflow | Task completion, successful changes, test-pass rate, human interventions |
| Multilingual security | Single-language / baseline detector | Multilingual + code-mixed Kavach | Per-language Precision/Recall/F1, FP/FN, latency |

## Research Questions
1. Can Kavach reliably detect sensitive information in multilingual and code-mixed AI
   interactions?
2. Does repository-grounded retrieval reduce unsupported/hallucinated code generation compared
   with an LLM without RAG?
3. Can semantic repository analysis accurately identify components affected by an AI-generated
   change?
4. Can an LLM-driven workflow transform natural-language requirements into validated software
   changes with reduced human intervention?
5. Can a security-governance layer enforce meaningful controls across the agentic development
   lifecycle without making the workflow impractically slow?

## Rule
These experiments must be designed **before** implementation is considered "finished." Datasets,
baseline outputs, Kavach outputs, and metric calculations must all be reproducible — never
fabricated or estimated after the fact.
