# TESTING_SPEC.md — Kavach

## Test Categories

### 1. Unit tests
Individual functions — detection regex/rules, chunking logic, severity mapping, etc.

### 2. Integration tests
Multi-component flows — e.g. "RAG retrieval feeds correctly into generation," "security engine
correctly blocks a workflow run."

### 3. End-to-end tests
Full pipeline: developer request in → final report out, including at least one case that gets
BLOCKED and one that gets ALLOWED.

### 4. Security / detection tests
Run the multilingual test corpus (`/data/multilingual_test_corpus.md`) through the security
engine and compute precision/recall/F1 per language and entity type.

### 5. Regression tests
Every stress-test case that Kavach has successfully caught becomes a permanent regression
test — re-run automatically whenever the detection model/rules are updated, so a fix in one
place doesn't silently break a previous catch.

## Rule
Never use real personal data or real credentials anywhere in the test suite — synthetic values
only (see SECURITY_SPEC.md).

## CI Integration
All test categories above should be runnable via a single command locally and wired into the
CI/CD pipeline (see CICD_SPEC.md) so every PR is validated automatically.
