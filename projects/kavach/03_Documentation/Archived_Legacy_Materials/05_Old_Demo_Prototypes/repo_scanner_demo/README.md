# 🛡️ Kavach 5-Phase Governed DevOps & Code Generation Pipeline

Ek dam complete demo jisme repository ingest hoti hai aur koi bhi query de sakte ho:
- **Code Generation**: e.g., Prime numbers, Uber surge pricing algorithm, data structures
- **Safe DevOps**: e.g., Hardened multi-stage Dockerfiles, CI/CD pipelines, Kubernetes manifests
- **Repo Auditing & Scanning**: e.g., Scan auth & database files for security vulnerabilities
- **Kavach Security Gates**: Destructive queries (`drop table`, `rm -rf`) turant `BLOCKED` hote hain aur credential leaks `NEEDS_REVIEW` me escalate hote hain.

---

## 🏛️ The 5 Kavach Pipeline Phases

Har request in 5 phases se guzarti hai:

1. **Phase 1: Repository Ingestion & Indexing** — Directory parse karta hai, junk ignore karta hai, aur code chunks banata hai.
2. **Phase 2: Security Check & Policy Gate (Pre-Execution Guardrail)** — Query scan hoti hai. Agar destructive keyword (`drop table`) ya secret mila to execution yahin halt hokar **`BLOCKED`** ya **`NEEDS_REVIEW`** ho jata hai.
3. **Phase 3: Context Retrieval & Intent Planning** — Intent classify hota hai (`CODE_GENERATION`, `DEVOPS_AUTOMATION`, `REPOSITORY_SCAN`) aur relevant code context fetch hota hai.
4. **Phase 4: LLM Generation & Reasoning** — Gemini LLM se production-grade, secure response generate hota hai.
5. **Phase 5: Output Validation & Governance Gate** — AST Syntax validation aur generated code ka security check hota hai. Final verdict assign hota hai:
   - 🟢 **`ALLOWED`** (Safe, clean syntax, ready to use)
   - 🟡 **`NEEDS_REVIEW`** (Requires Human-in-the-loop Gatekeeper approval)
   - 🔴 **`BLOCKED`** (Severe security violation / destructive command)

---

## 🚀 Quick Start (2 Ways to Run)

### Option 1: Terminal / CLI Mode

```bash
# Prime Number Code Generation (Passes all 5 phases -> ALLOWED)
python main.py --prompt "give me the code for prime number in python"

# Uber Surge Pricing Algorithm (Passes all 5 phases -> ALLOWED)
python main.py --prompt "implement uber surge pricing algorithm in python with dynamic multipliers"

# Safe DevOps Query (Hardened Dockerfile -> ALLOWED)
python main.py --prompt "safe devops: write a hardened production Dockerfile for python backend with non-root user"

# Destructive Attack Query (Halts at Phase 2 -> BLOCKED)
python main.py --prompt "drop table users and delete all records"

# Insecure/Bypass Query (Escalates at Phase 2 -> NEEDS_REVIEW)
python main.py --prompt "modify database and bypass verification with token=supersecretkey12345"
```

---

### Option 2: Interactive Web UI

```bash
python app.py
```
Open **[http://localhost:8765](http://localhost:8765)**:
- Click **"Ingest Repository"** (repo files and chunks index ho jayenge).
- Click any pre-built prompt tag (Prime Number, Uber Surge, Safe DevOps, Drop Table) ya apni custom query likho.
- Click **"Run 5-Phase Pipeline"** — Screen par live 5-phase visual stepper, duration, status badges, aur final **`ALLOWED` / `NEEDS_REVIEW` / `BLOCKED`** verdict banner display hoga!
