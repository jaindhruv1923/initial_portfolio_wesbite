# 🏦 Bharat Commercial Core Banking & Unified Results Cockpit (`02_Banking_and_Results_Dashboard`)

Welcome to the **Commercial Core Banking System & Real-Time Telemetry Results Cockpit** module of the **KAVACH Platform**.

This directory brings together two mission-critical enterprise environments:
1. **Bharat Commercial Core Banking System (`implementation_banks/`)**: An enterprise-grade, RBI DPDP / FIPS-compliant core banking engine governed by the KAVACH 5-Gate Security Shield.
2. **Unified Results Cockpit (`results_dashboard/`)**: A high-concurrency, dual SQLite WAL + JSON telemetry hub providing live event streaming, Merkle ledger auditing, and executive dashboards.
3. **Cross-Platform Integration Test Suite (`tests_unified/`)**: Exactly 100 rigorous, deterministic integration test cases validating cross-platform contracts between KAVACH and Bharat Bank.

---

## 📂 Subdirectory Architecture

```
02_Banking_and_Results_Dashboard/
├── implementation_banks/              # Bharat Core Banking Platform & Security Shield
│   ├── core_banking.py                # Double-entry ledger, accounts, ACID persistence
│   ├── kavach_banking_shield.py       # 5-Gate defense highway (Prompt injection, DPDP PII, HITL)
│   ├── advanced_banking_engines.py    # SAGA orchestrator, Maker-Checker, CBDC e-INR, HSM
│   ├── server.py                      # FastAPI microservice (Port 8050)
│   ├── index.html, app.js, style.css  # Interactive Banking UI & customer simulation portal
│   ├── test_banking_100_suite.py      # Exactly 100 deterministic banking tests (100% pass)
│   ├── test_banking_kavach.py         # 11-stage enterprise security verification
│   └── data/                          # Persistent ledger JSON and write-ahead snapshots
├── results_dashboard/                 # Real-Time Telemetry & Results Cockpit
│   ├── results_hub.py                 # FastAPI telemetry engine (Port 8090)
│   ├── index.html, app.js, style.css  # Dynamic dashboard with real-time SSE streaming
│   └── data/                          # SQLite WAL database & JSON export snapshots
├── tests_unified/                     # Unified Cross-Platform Integration Suite
│   └── test_unified_100_suite.py      # Exactly 100 cross-platform stress & contract tests
├── run_banking.bat                    # Start Banking server on Port 8050
├── run_dashboard.bat                  # Start Results Cockpit on Port 8090
├── run_all.bat                        # Start both Banking and Results Cockpit simultaneously
├── run_tests.bat                      # Execute all 200 Banking + Unified tests
└── README.md                          # This documentation file
```

---

## ⚡ Quick Start & Run Commands

### 1. Launch All Services (Banking + Results)
```bash
# Windows Command Prompt
run_all.bat
```
* **Bharat Core Banking Portal**: [http://localhost:8050](http://localhost:8050)
* **Unified Results Cockpit**: [http://localhost:8090](http://localhost:8090)

### 2. Run Individual Services
```bash
# Launch Core Banking Server only (Port 8050)
run_banking.bat
# Or via CLI:
python -m uvicorn implementation_banks.server:app --host 127.0.0.1 --port 8050 --reload

# Launch Results Cockpit only (Port 8090)
run_dashboard.bat
# Or via CLI:
python -m uvicorn results_hub:app --app-dir results_dashboard --host 127.0.0.1 --port 8090 --reload
```

### 3. Run Test Suites (200 Tests)
```bash
# Execute both test suites (200 deterministic tests)
run_tests.bat

# Or run separately:
python -m pytest implementation_banks/test_banking_100_suite.py -q
python -m pytest tests_unified/test_unified_100_suite.py -q
```

---

## 🛡️ Key Features & Technical Specifications

| Feature | Technical Implementation | Regulatory / Security Standard |
| :--- | :--- | :--- |
| **5-Gate Security Highway** | Pre-flight injection sanitizer, PII vaulting, HITL review | OWASP LLM01, DPDP Act 2023 |
| **Maker-Checker Segregation** | Dual-control cryptographic approval for transactions > ₹50,000 | RBI Section 45ZA Guidelines |
| **Distributed SAGA Orchestrator** | 2-phase commit with automatic compensating reversals | ACID Ledger Integrity |
| **Software-Defined HSM** | FIPS 140-2 Level 3 RSA-PSS & HMAC digital signatures | NIST SP 800-57 |
| **RBI CBDC e-INR Vault** | Bearer-token offline/online double-spend protection | RBI Digital Rupee Spec |
| **Telemetry Sync Engine** | SQLite WAL mode with sub-millisecond SSE streaming | Real-Time Audit Telemetry |
| **Merkle Audit Ledger** | NIST FIPS 202 SHA3-512 cryptographic tamper detection | Immutability Proofs |

---

[← Back to Master Repository README](../README.md) &nbsp;|&nbsp; [🛡️ KAVACH Platform (`../01_KAVACH_Platform`)](../01_KAVACH_Platform/README.md) &nbsp;|&nbsp; [📚 Master Documentation (`../03_Documentation`)](../03_Documentation/README.md)
