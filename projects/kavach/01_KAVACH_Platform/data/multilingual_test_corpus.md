# Security Test Corpus — Kavach

> Purpose: evaluation data for the security engine's PII, sensitive number, and credential detection.
> All PAN/Aadhaar/phone/account/email values below are FAKE, for testing only. Never use real
> data. This corpus is balanced between sensitive and non-sensitive examples so
> precision, recall, and F1 can be measured meaningfully — measuring both detection recall
> and protection against false positives on safe developer text.

## Format
| ID | Text | Sensitive? | Entity type |
|----|------|------------|-------------|

---

## English DevOps & Sensitive Data Corpus (50 examples)

| ID | Text | Sensitive? | Entity Type |
|----|------|------------|-------------|
| ENG-01 | My PAN card number is ABCDE1234F | Yes | PAN |
| ENG-02 | Add a health check endpoint to the backend returning JSON status | No | — |
| ENG-03 | 12454323454 | Yes | Sensitive Number |
| ENG-04 | 123456789012 | Yes | Aadhaar-like |
| ENG-05 | My Aadhaar number is 1234 5678 9012 | Yes | Aadhaar-like |
| ENG-06 | Please call me at 9876543210 regarding the deployment | Yes | Phone number |
| ENG-07 | Set server timeout to 30 seconds and maximum pool size to 10 | No | — |
| ENG-08 | Transfer payment to bank account number 112233445566 | Yes | Bank account |
| ENG-09 | Refactor authentication middleware to use JWT tokens | No | — |
| ENG-10 | Contact lead engineer at alex.dev@example.com | Yes | Email |
| ENG-11 | My permanent account number PAN is ABCDE1234F for verification | Yes | PAN |
| ENG-12 | Optimize Docker build with multi-stage caching | No | — |
| ENG-13 | National identification number: 9876 5432 1098 | Yes | Aadhaar-like |
| ENG-14 | Update customer mobile to +91 9876543210 | Yes | Phone number |
| ENG-15 | Fix SQL query performance on users table by adding an index | No | — |
| ENG-16 | Wire funds to a/c 998877665544 immediately | Yes | Bank account |
| ENG-17 | When is the next release scheduled for staging? | No | — |
| ENG-18 | Audit report sent to security-team@corp.example.com | Yes | Email |
| ENG-19 | Configure CORS middleware to accept local origins | No | — |
| ENG-20 | My PAN is ABCDE1234F and email is user@example.com | Yes | PAN |
| ENG-21 | Identity document number: 1234-5678-9012 | Yes | Aadhaar-like |
| ENG-22 | Create database migration script for user preferences table | No | — |
| ENG-23 | Verify customer account number 123456789012 before processing | Yes | Bank account |
| ENG-24 | Emergency hotline number is 9876543210 | Yes | Phone number |
| ENG-25 | What is the recommended retry count for external API calls? | No | — |
| ENG-26 | Customer sensitive ID code 12454323454 | Yes | Sensitive Number |
| ENG-27 | Enable gzip compression on all static asset responses | No | — |
| ENG-28 | Send credentials to admin.security@example.com | Yes | Email |
| ENG-29 | Setup Prometheus metrics exporter on port 9090 | No | — |
| ENG-30 | Government ID: 1234 5678 9012 for onboarding check | Yes | Aadhaar-like |
| ENG-31 | Register PAN ABCDE1234F with tax compliance service | Yes | PAN |
| ENG-32 | Implement rate limiting using Redis sliding window | No | — |
| ENG-33 | Billing department phone number is 9123456789 | Yes | Phone number |
| ENG-34 | How do we run integration tests in headless mode? | No | — |
| ENG-35 | Customer bank account 556677889900 details updated | Yes | Bank account |
| ENG-36 | Bare identification number sequence 987654321012 | Yes | Aadhaar-like |
| ENG-37 | Add OpenAPI schema tags for reporting endpoints | No | — |
| ENG-38 | Direct notification to test.alert@example.com | Yes | Email |
| ENG-39 | Upgrade pytest and httpx packages to latest version | No | — |
| ENG-40 | My Aadhaar card is 123456789012 | Yes | Aadhaar-like |
| ENG-41 | Verify PAN card ABCDE1234F against national registry | Yes | PAN |
| ENG-42 | Format log output as structured JSON with correlation ID | No | — |
| ENG-43 | Primary mobile contact: +919876543210 | Yes | Phone number |
| ENG-44 | What is the expected latency threshold for RAG search? | No | — |
| ENG-45 | Deposit payout into account number 445566778899 | Yes | Bank account |
| ENG-46 | Input value: 12454323454 | Yes | Sensitive Number |
| ENG-47 | Generate automated changelog based on git commit history | No | — |
| ENG-48 | Support contact email is devops-team@internal.example.org | Yes | Email |
| ENG-49 | Check health status of Qdrant vector database service | No | — |
| ENG-50 | National ID: 1234 5678 9012 verification passed | Yes | Aadhaar-like |

## Entity Types Covered
- PAN (Permanent Account Number): 5 letters + 4 digits + 1 letter
- Aadhaar-like number: 12 digits formatted or plain (e.g. `1234 5678 9012`, `123456789012`)
- Sensitive numeric identifiers: bare numbers (e.g. 11-digit `12454323454`)
- Indian phone number: 10 digits starting with 6-9
- Bank account number: 9-18 digits with financial context
- Email address: standard RFC-compliant patterns
