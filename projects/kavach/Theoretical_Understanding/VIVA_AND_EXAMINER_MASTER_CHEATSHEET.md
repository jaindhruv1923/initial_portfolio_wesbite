# 🎓 KAVACH: Viva Voce & Examiner Defense Master Cheatsheet
## *High-Yield Q&A, Formula Derivations & Examiner Traps for B.Tech Capstone Defense*

---

## 📌 Top 15 Quick Formulas to Write on Whiteboard

| # | Topic | Mathematical Formula / Theorem | When to Use |
| :-: | :--- | :--- | :--- |
| **1** | **Shannon Entropy** | $$H(S) = -\sum_{i=1}^{k} P(c_i) \log_2 P(c_i)$$ | Explaining how KAVACH detects arbitrary secret keys ($H \ge 4.0$) vs code ($H \approx 2.5$). |
| **2** | **Verhoeff Equation** | $$c = \left( \sum_{i=1}^{12} d\left( c_{i-1}, F(i, a_i) \right) \right) \equiv 0$$ | Explaining 100% detection of adjacent transpositions in Indian 12-digit Aadhaar numbers using $D_5$. |
| **3** | **Precision & Recall** | $$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}$$ | Explaining KAVACH's 1.00 PII score across 42 benchmark runs. |
| **4** | **Harmonic F1 Score** | $$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = 1.00$$ | Proving zero false positives and zero false negatives. |
| **5** | **Blast Radius Score** | $$\text{BlastRadius}(f^*) = \frac{|\{u \in V \mid u \rightsquigarrow f^*\}|}{|V|} \times 100\%$$ | Explaining how AST DAG caller-callee reachability calculates regression risk. |
| **6** | **Merkle Tree Inclusion** | $$\text{Complexity} = O(\log_2 N)$$ | Proving regulators can audit 1 record out of 1,000,000 with only $\approx 20$ hashes. |
| **7** | **Grover Quantum Margin** | $$\text{Quantum Operations} = 2^{n / 2} = 2^{512 / 2} = 2^{256}$$ | Explaining why SHA3-512 is post-quantum resilient compared to SHA-256 ($2^{128}$). |
| **8** | **ReDoS Complexity** | $$\text{Complexity} = O(2^N)$$ | Explaining catastrophic backtracking in nested regex quantifiers `(a+)+$`. |
| **9** | **OCC Version Invariant** | $$\text{UPDATE accounts SET bal = bal - \Delta, ver = ver + 1 WHERE ver = v_{\text{old}}}$$ | Demonstrating race-condition elimination without database table locking. |
| **10** | **Transformer Attention** | $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$ | Proving why system prompt guardrails fail against adversarial prompt injection. |

---

## 🎯 Top 12 Anticipated Examiner Questions & Model Answers

### Q1: "Why did you build KAVACH when commercial tools like Snyk, SonarQube, and Dependabot already exist?"
> **Examiner Trap:** Testing whether you know the difference between traditional static code scanners and agentic runtime security.  
> **Model Answer:**  
> *"Existing Software Composition Analysis (SCA) tools like Snyk and Dependabot are **post-facto lockfile scanners** (Ladisa et al., 2023). They only inspect static `requirements.txt` or `package.json` files after code has already been written or committed. When an autonomous AI agent synthesizes code dynamically in memory, it introduces arbitrary import statements (e.g., `import fastapi_jwt_vault`) that never appear in lockfiles. Traditional SCA tools are completely blind to runtime agent hallucinations. KAVACH, in contrast, enforces **pre-execution and runtime AST import firewalling**, intercepting and validating imports against official PyPI registry APIs before any code touches the filesystem or sandbox."*

---

### Q2: "Why not just put 'Never leak Aadhaar or secret keys' inside the LLM system prompt?"
> **Examiner Trap:** Testing whether you understand the fundamental limits of probabilistic AI.  
> **Model Answer:**  
> *"Relying on system prompts is known as **probabilistic or stochastic guardrailing**, which OWASP 2025 and Greshake et al. (2023) proved is fundamentally vulnerable to prompt injection and jailbreaks. Because a Transformer treats all tokens in the context window symmetrically via self-attention, adversarial embeddings can easily dominate attention weights over the initial system prompt. Furthermore, an LLM's weights are static and frozen at training time, so it cannot verify real-world package registries or mathematical checksums. KAVACH enforces **deterministic guardrails outside the LLM context window** using Shannon entropy, AST parsers, and Verhoeff algorithms, which cannot be subverted by prompt injection."*

---

### Q3: "Explain why Luhn's algorithm is inadequate for Aadhaar, and how Verhoeff solves it mathematically."
> **Examiner Trap:** Testing your knowledge of discrete mathematics and abstract algebra.  
> **Model Answer:**  
> *"Luhn operates under modulo 10 arithmetic. While Luhn catches all single-digit substitutions, it completely fails to catch adjacent transposition errors where $|a - b| = 5$ (such as $16 \leftrightarrow 61$ or $27 \leftrightarrow 72$), as well as 10% of twin errors ($aa \leftrightarrow bb$). For national identifiers like India's 12-digit Aadhaar, transpositions in banking and KYC databases cause severe identity mismatches.  
> Verhoeff solves this by utilizing the non-abelian **Dihedral Group of order 10 ($D_5$)**, representing the symmetries of a regular pentagon. Because $D_5$ is non-commutative ($a \circ b \neq b \circ a$), swapping any two adjacent digits produces a different group element. Verhoeff guarantees **100% detection of single-digit substitutions, 100% of adjacent transpositions, and 100% of twin errors**."*

---

### Q4: "SHA-256 is an industry standard. Why did you upgrade KAVACH to NIST FIPS 202 SHA3-512?"
> **Examiner Trap:** Deep-dive into modern applied cryptography.  
> **Model Answer:**  
> *"SHA-256 is built on the **Merkle-Damgård construction** (standardized in 2001), which has two well-documented cryptographic limitations in zero-trust zero-knowledge environments:  
> 1. **Length Extension Attacks (LEA):** Because intermediate compression states are directly outputted as the hash digest, an adversary knowing $H(m)$ and $|m|$ can append malicious data $m'$ to calculate a valid hash $H(m \mathbin{\Vert} \text{pad} \mathbin{\Vert} m')$ without knowing secret $m$.  
> 2. **Quantum Security Margin:** Under Grover's quantum search algorithm, SHA-256's pre-image resistance is halved to $2^{128}$ operations, which is vulnerable over long-term 15-year statutory audit horizons.  
>  
> KAVACH upgraded to **NIST FIPS 202 SHA3-512 (Keccak Sponge Construction)**. Keccak uses a 1600-bit internal permutation state where 1024 capacity bits remain completely hidden during the squeezing phase. This provides **mathematical immunity to Length Extension Attacks by design** and guarantees a post-quantum resistance of $2^{256}$ operations under Grover’s algorithm, satisfying NSA CNSA 2.0 standards."*

---

### Q5: "How does KAVACH provide tamper-evident compliance under the Indian DPDP Act 2023?"
> **Examiner Trap:** Bridging computer science implementation with statutory law.  
> **Model Answer:**  
> *"Under Section 8 of the Indian Digital Personal Data Protection (DPDP) Act 2023, data fiduciaries face statutory penalties of up to ₹250 Crore for unauthorized data breaches or failure to maintain technical safeguards. KAVACH ensures compliance through two mechanisms:  
> 1. **Zero-Knowledge Token Vault:** Redacts 12-digit Aadhaar and 10-character PAN identifiers into surrogate tokens (`<REDACTED_AADHAAR_001>`) before prompts leave the local infrastructure, ensuring raw citizen data never touches third-party cloud LLM clusters.  
> 2. **Cryptographic Merkle DPDP Ledger:** Anchors every prompt, patch, and financial event into a binary SHA3-512 Merkle tree. If any actor modifies even a single character in the audit database, the root hash immediately fails re-verification (`tamper_detected: true`). Furthermore, external auditors can verify any transaction in $O(\log N)$ time using an inclusion proof without exposing private intellectual property or source code."*

---

### Q6: "Why did you use Optimistic Concurrency Control (OCC) instead of database locks (`SELECT ... FOR UPDATE`) in Bharat Banking?"
> **Examiner Trap:** Distributed systems scalability and concurrency bottlenecks.  
> **Model Answer:**  
> *"Pessimistic locking (`FOR UPDATE`) holds physical database locks on rows. In a high-throughput banking system with concurrent payment bursts (e.g., festival sales or corporate payroll disbursement where hundreds of workers hit the same account simultaneously), pessimistic locking causes extreme thread contention, connection pool exhaustion, and circular deadlocks.  
> KAVACH uses **Optimistic Concurrency Control (OCC)** with account versioning. Transactions read the balance and version without locking. When committing, the update executes an atomic Compare-And-Swap (CAS):  
> `UPDATE accounts SET balance = balance - amount, version = version + 1 WHERE id = ? AND version = expected_version`  
> If another worker committed first, affected rows equals 0, triggering an immediate clean abort. Our test suite verified 15 simultaneous worker threads executing rapid transfers with zero balance discrepancies."*

---

### Q7: "What is Trojan Source (CVE-2021-42574) and how does KAVACH stop it?"
> **Examiner Trap:** Demonstrating knowledge of real-world CVEs and compiler vulnerabilities.  
> **Model Answer:**  
> *"Trojan Source exploits the Unicode Bidirectional (Bidi) Algorithm. By injecting explicit directional override codepoints like Right-To-Left Override (`U+202E`) and Left-To-Right Isolate (`U+2066`), an attacker can cause source code to render in a human reviewer's IDE as a harmless comment, while the compiler or Python interpreter executes it as active logic (e.g., executing an admin privilege check inside a string). KAVACH enforces a dedicated Steganography Shield that scans all inbound code and strips bidirectional override codepoints before parsing or execution."*

---

### Q8: "What is the Google ADK 8-Hook Callback architecture?"
> **Examiner Trap:** Verifying your understanding of production-grade agentic frameworks.  
> **Model Answer:**  
> *"The Google Agent Development Kit (ADK) specification establishes an 8-hook lifecycle model across 3 distinct phases:  
> - **Pre-Execution:** `before_run` (session setup), `before_agent` (agent persona dispatch), `before_model` (context sanitization).  
> - **Execution & Tools:** `after_model` (model output inspection), `before_tool` (sandbox parameter and SSRF validation), `after_tool` (tool output sanitization).  
> - **Post-Execution:** `after_agent` (evaluating task completeness), `after_run` (telemetry and Merkle tree audit logging).  
> KAVACH implements this exact spec to place deterministic guardrails at every state transition boundary."*

---

### Q9: "Explain ReDoS and why regular expressions can freeze a server."
> **Examiner Trap:** Automata theory and algorithm complexity analysis.  
> **Model Answer:**  
> *"ReDoS occurs when a regular expression has nested quantifiers with overlapping states, such as `(a+)+$`. In formal language theory, these compile to Non-Deterministic Finite Automata (NFAs). When input consists of many repetitions of `'a'` followed by an invalid character (e.g., `aaaa...a!`), the regex engine must exhaustively backtrack through all possible groupings of states. This yields **$O(2^N)$ exponential time complexity**. An input of just 40 characters can lock a CPU core for hours. KAVACH’s ReDoS shield parses AST regex compile statements to detect overlapping states before deployment."*

---

### Q10: "How does your system handle medical emergencies in the Autonomous Medical Triage pipeline?"
> **Examiner Trap:** Safety-critical ethical AI guardrails.  
> **Model Answer:**  
> *"Our Medical Triage pipeline enforces a hard deterministic gate:  
> - If user symptoms indicate high urgency (e.g., crushing chest pain, breathlessness, signs of myocardial infarction), the pipeline dispatches the Emergency Agent. It is **programmatically prohibited** from suggesting medications or diagnosing, and immediately outputs emergency escalation protocols directing the user to **Call 112 / 108**.  
> - If symptoms are normal (e.g., mild tension headache after screen time), the pipeline routes to the Medicine Agent, recommending standard OTC remedies like Paracetamol with dosage disclaimers."*

---

### Q11: "What are the latency benchmarks of KAVACH's deterministic security layer?"
> **Examiner Trap:** Ensuring your platform is usable in real-world production.  
> **Model Answer:**  
> *"Our deterministic security layer—including Shannon entropy evaluation, regex tokenization, Verhoeff checksum validation, and in-memory LRU PyPI registry lookup—executes in **under 10 milliseconds**. This adds less than 1% latency overhead to total end-to-end LLM inference pipelines, satisfying enterprise SLAs."*

---

### Q12: "What is the difference between Token-Based and Account-Based CBDC (Digital Rupee)?"
> **Examiner Trap:** Modern fintech and central banking digital architectures.  
> **Model Answer:**  
> *"In an **Account-Based CBDC**, balances are recorded in a central or commercial bank ledger, and transactions require identity verification against the account. In a **Token-Based CBDC** (modeled after physical currency banknotes), each digital rupee unit has a distinct cryptographic serial number and denomination; possession of the private key signifies ownership, facilitating offline and peer-to-peer wallet transfers. KAVACH implements both: account deposits can be converted into cryptographic digital rupee wallet tokens via `mint_cbdc`, transferred P2P via `transfer_cbdc`, and redeemed back into statutory bank deposits via `redeem_cbdc`."*

---

## 📋 5 Examiner Trap Scenarios & How to Handle Them

| Trap Scenario | What the Examiner is Testing | Your Counter-Strategy |
| :--- | :--- | :--- |
| **"Your project claims 100% security. That is scientifically impossible."** | Testing your intellectual honesty and domain maturity. | Agree immediately: *"You are correct, Professor. No software system can guarantee 100% security against all unknown zero-days. When we state 1.00 Precision/Recall, we refer strictly to our evaluated 42-run benchmark corpus and 19 defined attack vectors (Aadhaar Verhoeff, PAN regex, and Trojan Bidi). We have documented our architectural limitations in `KAVACH_LIMITATIONS.md`."* |
| **"AST parsing only works for Python. What if the code is in Java or Go?"** | Testing polyglot microservice scalability. | *"Our static AST engine currently specializes in Python. For polyglot enterprise repositories (Go, Rust, TypeScript), our Phase 2 architecture integrates tree-sitter grammars and Language Server Protocol (LSP) indexing."* |
| **"Doesn't redacting tokens in prompts degrade the LLM's reasoning ability?"** | Testing context preservation in Zero-Knowledge Vaults. | *"We preserve syntactic semantic roles using typed surrogate tokens like `<CUSTOMER_ACC_01>` instead of random noise. The LLM understands that it is manipulating an account identifier and writes valid SQL/Python, which our local vault safely rehydrates."* |
| **"Why not use Blockchain instead of a Merkle Tree?"** | Testing distributed consensus knowledge. | *"Blockchains require distributed proof-of-work or proof-of-stake consensus across decentralized nodes, introducing high latency (seconds to minutes) and unnecessary overhead. In an enterprise bank, the institution is a known Data Fiduciary; a cryptographic Merkle tree provides the exact same mathematical non-repudiation and tamper-evidence in sub-millisecond execution time without consensus bloat."* |
| **"Can an attacker bypass your SSRF filter using decimal IP format?"** | Testing network socket engineering depth. | *"No, because KAVACH does not rely on naive string matching. We resolve hostnames to canonical 32-bit IPv4 integers using socket DNS resolution, evaluating binary IP representations directly against forbidden CIDR bitmasks."* |

---

*Authored by Dhruv Jain · B.Tech CSE (AI & Data Science) · PRJ-IV Capstone Project · KAVACH Defense Cheatsheet*
