import os

app_js_path = r"c:\Users\jaind\Videos\PRJ-IV Work\kavach\frontend\app.js"

with open(app_js_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find where PLAYBOOK_DATA starts
pbook_start = -1
for i, line in enumerate(lines):
    if "// ENTERPRISE INDUSTRY PLAYBOOK & PROCESS ROADMAP ENGINE" in line:
        pbook_start = i
        break

print(f"Playbook start line: {pbook_start + 1}")

# Find where switchToUseCases starts
switch_uc_idx = -1
for i, line in enumerate(lines):
    if "function switchToUseCases()" in line:
        switch_uc_idx = i
        break

print(f"switchToUseCases line: {switch_uc_idx + 1}")

if pbook_start == -1 or switch_uc_idx == -1:
    print("Error: Could not find markers!")
    exit(1)

# Extract playbook lines (from pbook_start to end of file)
playbook_block = "".join(lines[pbook_start:])
# The rest of lines before playbook_start
main_lines = lines[:pbook_start]

print("Playbook block lines:", len(playbook_block.splitlines()))
print("Main lines:", len(main_lines))

# Construct enhanced Playbook JS code
enhanced_playbook_code = '''
// ==========================================================================
// ENTERPRISE INDUSTRY PLAYBOOK & PROCESS ROADMAP ENGINE
// ==========================================================================

function safePlaybookEscape(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

window.PLAYBOOK_DATA = {
  currentIndustry: "bank",
  currentStep: 1,
  currentMode: "protected", // "protected" | "unprotected"
  autoPlayTimer: null,

  industries: {
    bank: {
      name: "Tier-1 Digital Bank (Fintech & Core Payments)",
      compliance: "RBI Cyber Framework • DPDP Act 2023 • PCI-DSS Level 1",
      repo: "enterprise-banking/upi-reconciliation-service",
      steps: {
        1: {
          title: "Initial Setup & Baseline Security Configuration",
          subtitle: "What happened before the request was made",
          userAction: "Security architect links GitHub repo and sets up Zero-Trust banking policy.",
          kavachAction: "Ingests repository AST, pre-warms local Qdrant vector index, and enables RBI/DPDP entity patterns (Aadhaar, PAN, Cards, AWS/DB secrets).",
          protectedSnippet: `[SETUP] Linked repo: enterprise-banking/upi-reconciliation-service
[POLICY] Active Profile: HIGH_SECURITY_FINTECH
[ENTITIES] Pre-warmed vault: Aadhaar (12-digit), PAN, Credit Cards, JWT/API Secrets
[AST RAG] Indexed 48 Python microservices in 82ms • Baseline clean`,
          unprotectedSnippet: `// UNPROTECTED PIPELINE
No governance control plane installed.
Autonomous AI agent granted direct write-access to master branch.
No pre-flight token vault or AST package check enabled.`,
          verdict: "ENVIRONMENT READY",
          verdictType: "allow",
          metrics: "48 Repositories Indexed • Latency 82ms • Zero Leaks"
        },
        2: {
          title: "Developer / AI Coding Prompt & Token Interception",
          subtitle: "If user prompts AI with sensitive database credentials & customer PII",
          userAction: `Developer queries Cursor/Devin:
"Refactor failed UPI reconciliation callback and log KYC verification for Aadhaar 4532 8765 1092 with AWS_KEY=AKIAIOSFODNN7EXAMPLE99"`,
          kavachAction: "Token Vault intercepts prompt in 3.1ms. Scans regex + Shannon entropy, encrypts sensitive data into synthetic tokens, and sends clean prompt to LLM.",
          protectedSnippet: `[KAVACH TOKEN VAULT] Intercepted raw outgoing prompt in 3.1ms
[VAULTED] 12-digit Aadhaar -> <VAULT_TOKEN_AADHAAR_92>
[VAULTED] AWS Secret Key -> <REDACTED_AWS_KEY_01>
[EGRESS] Sanitized prompt dispatched to Claude 3.5 Sonnet
[STATUS] Zero customer PII or cloud credentials leaked!`,
          unprotectedSnippet: `💥 DISASTER IN UNPROTECTED ENVIRONMENT:
Plaintext Aadhaar and production AWS secret sent to external cloud LLM API!
Stored in public model training transcripts & external cache.
Violation: DPDP Act 2023 Section 8 (Fine: ₹250 Crores / $30 Million).`,
          verdict: "PROTECTED & SANITIZED",
          verdictType: "allow",
          metrics: "2 Sensitive Entities Vaulted • Zero Cloud Egress • 3.1ms Latency"
        },
        3: {
          title: "AI Code Generation & Supply-Chain Slopsquatting Defense",
          subtitle: "If AI invents / hallucinates a non-existent package in the patch",
          userAction: `AI coding model writes the payment patch, but includes:
import py_upi_fast_crypto  # Hallucinated non-existent package!`,
          kavachAction: "AST Package Firewall parses Python AST Import node, queries PyPI live index in 12ms. Package does NOT exist on PyPI -> Flags potential Slopsquatting attack!",
          protectedSnippet: `[AST PACKAGE FIREWALL] Inspecting generated diff nodes...
[CHECK] Validated import 'fastapi' (Official PyPI: Verified)
[ALERT] Package 'py_upi_fast_crypto' NOT FOUND ON REGISTRY!
[THREAT] Hallucinated Dependency / Slopsquatting Attack Vector
[ACTION] BLOCKED! Agent forced to substitute verified 'cryptography>=41.0.0'`,
          unprotectedSnippet: `💥 DISASTER IN UNPROTECTED ENVIRONMENT:
Developer runs 'pip install py_upi_fast_crypto' blindly.
Attacker registered that exact package name 2 hours prior containing reverse shell.
Attacker gains root container access to bank payment database!`,
          verdict: "SLOPSQUATTING ATTACK BLOCKED",
          verdictType: "block",
          metrics: "AST Analyzed in 12ms • Malicious Import Quarantined"
        },
        4: {
          title: "Change-Impact Radar & Blast-Radius Evaluation",
          subtitle: "If AI modifies a shared database schema affecting downstream services",
          userAction: `AI modifies user account balance query in auth_service.py to add timeout parameter.`,
          kavachAction: "Change-Impact Engine builds whole-repo call-graph: Discovers 4 critical downstream services (atm_switch, upi_settlement, fraud_alert, loan_ledger) will break! Risk Score: 0.94 -> Multi-LLM Consensus demands Human Review.",
          protectedSnippet: `[CHANGE-IMPACT RADAR] Analyzing caller-callee reachability graph...
[BLAST RADIUS] Modifying 'validate_balance()' affects 4 microservices:
 - atm_switch.py (Direct crash on invalid timeout arg)
 - upi_settlement.py (Reconciliation halt)
 - fraud_alert.py (Silent exception)
 - loan_ledger.py (Downstream drift)
[POLICY DECISION] Risk 0.94 -> HALT AT HUMAN GATEKEEPER`,
          unprotectedSnippet: `💥 DISASTER IN UNPROTECTED ENVIRONMENT:
PR merged directly.
4 core banking microservices crash in production at 10:00 AM.
30,000 ATM and UPI transactions fail across the nation.`,
          verdict: "HUMAN GATEKEEPER HALT",
          verdictType: "review",
          metrics: "4 Microservices Saved • Blast Radius 0.94 • Outage Prevented"
        },
        5: {
          title: "Cryptographic Merkle Attestation & Production Merge",
          subtitle: "The final secure, audited deployment to CI/CD",
          userAction: "Staff Security Engineer reviews remediation diff and clicks 1-Click Approve in KAVACH Security Command Center.",
          kavachAction: "Cryptographically signs SHA-256 Merkle root, logs to immutable statutory ledger, updates CycloneDX SBOM, and merges PR into production pipeline.",
          protectedSnippet: `[KAVACH AUDIT ATTESTATION] Signed by Lead SecDev Engineer
[MERKLE ROOT] c8f49b1a0d7e2f5b902e41a6b7c893fa1e920d4371
[INCLUSION PROOF] Cryptographic verification: VALID
[COMPLIANCE] PCI-DSS 4.0 Section 6.5.1 & RBI Cyber Security: PASS
[CI/CD] GitHub Actions webhook triggered • Deployed to Production safely!`,
          unprotectedSnippet: `💥 UNPROTECTED ENVIRONMENT:
Audit logs are scattered across ephemeral containers.
No cryptographic proof of who modified what.
External compliance auditors fail SOC2 certification.`,
          verdict: "PRODUCTION DEPLOYED SAFELY",
          verdictType: "allow",
          metrics: "100% Cryptographically Audited • Zero Regressions • SOC2 Ready"
        }
      }
    },
    health: {
      name: "Healthcare & Telemedicine (HIPAA & EHR Patient Records)",
      compliance: "HIPAA Security Rule • HITECH Act • HL7 FHIR Standards",
      repo: "med-telehealth/patient-portal-api",
      steps: {
        1: {
          title: "Hospital EHR Setup & Patient Vault Configuration",
          subtitle: "What happened before the request was made",
          userAction: "Healthcare IT connects Hospital Electronic Health Record (EHR) microservice.",
          kavachAction: "Configures HIPAA Title II Privacy Vault rules, masking Medical Record Numbers (MRN), ICD-10 disease codes, and patient names.",
          protectedSnippet: `[SETUP] Target: med-telehealth/patient-portal-api
[COMPLIANCE] Mode: HIPAA_STRICT_SAFEGUARD
[PATIENT VAULT] Pre-loaded HIPAA 18 Safe Harbor identifiers`,
          unprotectedSnippet: `No HIPAA guardrails. Direct OpenAI API integration without patient data redaction.`,
          verdict: "HIPAA VAULT ACTIVE",
          verdictType: "allow",
          metrics: "HIPAA 18 Identifiers Guarded • Zero PII Leakage"
        },
        2: {
          title: "Doctor Prompt & Anonymization",
          subtitle: "If doctor or assistant queries diagnostic summaries",
          userAction: `Assistant queries: "Summarize blood lab report for patient John Doe, MRN-89412 with Diabetes Type 2"`,
          kavachAction: "Vault redacts name to <PATIENT_ID_481> and MRN to <REDACTED_MRN_12> before prompt leaves internal hospital VPC.",
          protectedSnippet: `[KAVACH HEALTH SHIELD] Patient Name & MRN detected
[REDACTED] John Doe -> <PATIENT_HASH_8471>
[REDACTED] MRN-89412 -> <VAULT_MRN_992>
[STATUS] Fully HIPAA Compliant Anonymized Egress`,
          unprotectedSnippet: `💥 Medical records exposed to third-party model! $50,000 fine per record under HIPAA.`,
          verdict: "PATIENT PII VAULTED",
          verdictType: "allow",
          metrics: "Zero Patient Data Leaked • HIPAA Compliant"
        },
        3: {
          title: "SSRF & Cloud Metadata Exfiltration Defense",
          subtitle: "If AI introduces an unverified telemetry beacon",
          userAction: `AI code snippet tries to fetch external telemetry via requests.get("http://169.254.169.254/latest/meta-data/")`,
          kavachAction: "KAVACH SSRF Shield intercepts AWS IMDSv1 metadata probe -> Drops connection and flags critical security alert.",
          protectedSnippet: `[SSRF SHIELD] Detected AWS IMDSv1 link-local address: 169.254.169.254
[VERDICT] BLOCKED • Cloud instance IAM credential harvesting prevented!`,
          unprotectedSnippet: `💥 Attacker exfiltrates hospital AWS root IAM role and dumps 500,000 patient records!`,
          verdict: "SSRF EXFILTRATION BLOCKED",
          verdictType: "block",
          metrics: "Cloud IAM Saved • MITRE T1552 Blocked"
        },
        4: {
          title: "Prescription Logic Impact Analysis",
          subtitle: "If AI alters medication dosage math",
          userAction: `AI modifies drug dosage calculation in pharmacy_dispense.py.`,
          kavachAction: "Change-Impact Radar flags discrepancy with clinical trial dosage unit. Demands Multi-LLM consensus verification.",
          protectedSnippet: `[IMPACT RADAR] dosage calculation altered in 3 ICU ward routes
[CONSENSUS] Multi-LLM Check: Gemini (REJECT) + Groq (REJECT)
[STATUS] Medical dosage drift caught before code execution`,
          unprotectedSnippet: `💥 Dosing math error deployed to automated pharmacy infusion pumps!`,
          verdict: "DOSAGE DRIFT CAUGHT",
          verdictType: "review",
          metrics: "ICU Ward Safety Verified • Multi-LLM Consensus"
        },
        5: {
          title: "Signed Medical SBOM & Audit Attestation",
          subtitle: "Final audited deployment for hospital inspection",
          userAction: "Chief Medical Information Officer signs off on verified change.",
          kavachAction: "Attests tamper-proof SHA-256 Merkle proof for FDA & HIPAA annual audits.",
          protectedSnippet: `[MERKLE AUDIT] Verified Leaf: 9b1a0d7e2f5b902e41a6b7c893fa1e92
[RESULT] FDA Digital Health Software & HIPAA Ready`,
          unprotectedSnippet: `No audit log. Hospital fails Joint Commission accreditation inspection.`,
          verdict: "FDA & HIPAA ATTESTED",
          verdictType: "allow",
          metrics: "100% Audit Readiness • Zero Patient Risk"
        }
      }
    },
    ecommerce: {
      name: "Global E-Commerce (Black Friday High-Concurrency Retail)",
      compliance: "PCI-DSS 4.0 • SOC 2 Type II • 99.999% High Availability",
      repo: "retail-cloud/cart-checkout-service",
      steps: {
        1: {
          title: "Cart & Checkout Engine Baseline Setup",
          subtitle: "What happened before the request was made",
          userAction: "DevOps engineer links Redis session and Stripe checkout repository.",
          kavachAction: "Loads PCI-DSS tokenization vault, pre-warms payment gateway AST, and connects live Redis pool monitoring.",
          protectedSnippet: `[SETUP] Target: retail-cloud/cart-checkout-service
[SLA] Target Availability: 99.999% High-Concurrency
[PCI-DSS] Live credit card & CVV interception enabled`,
          unprotectedSnippet: `Unmonitored dev environment. No concurrency or secret safeguards.`,
          verdict: "ECOMMERCE SHIELD ACTIVE",
          verdictType: "allow",
          metrics: "100,000 req/sec Capable • PCI-DSS Ready"
        },
        2: {
          title: "Stripe Key Interception & Customer Shield",
          subtitle: "If developer queries AI with live checkout tokens",
          userAction: `Developer queries: "Debug cart failure for customer test card 4242 4242 4242 4242 with stripe key sk_live_51M..."`,
          kavachAction: "Token Vault intercepts live Stripe secret key and credit card. Replaces with mock testing tokens in 1.9ms.",
          protectedSnippet: `[TOKEN VAULT] Live Stripe Secret Key detected!
[REDACTED] sk_live_51M... -> <MOCK_STRIPE_SANDBOX_KEY>
[REDACTED] Card 4242... -> <SYNTHETIC_CARD_TOKEN_01>
[STATUS] Zero production payment credentials exposed!`,
          unprotectedSnippet: `💥 Live Stripe secret key exposed in public LLM transcript! Attacker drains merchant wallet.`,
          verdict: "PAYMENT KEYS SHIELDED",
          verdictType: "allow",
          metrics: "Stripe Secret Vaulted in 1.9ms • 0 Leaks"
        },
        3: {
          title: "Concurrency Lock & Deadlock Detection",
          subtitle: "If AI introduces a synchronous database lock",
          userAction: `AI code suggests: with db.session.lock():  # Synchronous lock inside checkout loop!`,
          kavachAction: "Change-Impact Engine calculates latency impact: Throughput would drop from 45,000 req/s to 420 req/s -> ReAct Self-Healer automatically rewrites with async Redis distributed lock!",
          protectedSnippet: `[CHANGE-IMPACT RADAR] Detected synchronous database lock
[ANALYSIS] Checkout throughput degradation: -89.4%
[REACT SELF-HEALER] Auto-synthesizing non-blocking async Redis lock
[VERDICT] Auto-healed in 1 iteration • High-concurrency preserved!`,
          unprotectedSnippet: `💥 Black Friday checkout crashes! Website displays 504 Gateway Timeout for 45 minutes ($3.8M lost).`,
          verdict: "DEADLOCK AUTO-HEALED",
          verdictType: "allow",
          metrics: "45,000 req/s Preserved • Zero Downtime"
        },
        4: {
          title: "Polyglot Dependency & License Check",
          subtitle: "If AI imports an unauthorized GPL-licensed dependency",
          userAction: `AI proposes importing unverified package 'node-fast-crypto-gpl'.`,
          kavachAction: "Polyglot Firewall identifies GPL-v3 license contamination -> Flags legal IP risk for proprietary codebase.",
          protectedSnippet: `[POLYGLOT FIREWALL] License check on 'node-fast-crypto-gpl'
[LICENSE] GPL-3.0 (Copyleft Contamination Risk)
[VERDICT] BLOCKED • Enforced MIT/Apache-2.0 approved alternative`,
          unprotectedSnippet: `💥 Proprietary codebase legally contaminated with copyleft open-source license.`,
          verdict: "IP CONTAMINATION BLOCKED",
          verdictType: "block",
          metrics: "Commercial IP Protected • License Safe"
        },
        5: {
          title: "Zero-Downtime Deployment & Merkle Proof",
          subtitle: "Final audited deployment before Black Friday rush",
          userAction: "DevOps Lead approves verified non-blocking patch.",
          kavachAction: "Attests tamper-proof SHA-256 Merkle Ledger and triggers blue-green canary deployment.",
          protectedSnippet: `[MERKLE ATTESTATION] SHA-256 Root Hash: f49b1a0d7e2f5b902e41a6b7c893fa1e
[DEPLOYMENT] Canary Deploy: 100% Success • Zero cart dropouts!`,
          unprotectedSnippet: `Unverified deployment causes production database rollback and loss of cart state.`,
          verdict: "BLACK FRIDAY READY",
          verdictType: "allow",
          metrics: "99.999% SLA Maintained • Zero Outages"
        }
      }
    }
  }
};

var PLAYBOOK_DATA = window.PLAYBOOK_DATA;

function selectPlaybookIndustry(indKey) {
  if (!window.PLAYBOOK_DATA.industries[indKey]) return;
  window.PLAYBOOK_DATA.currentIndustry = indKey;
  window.PLAYBOOK_DATA.currentStep = 1;
  renderPlaybookStep();
}

function selectPlaybookStep(stepNum) {
  window.PLAYBOOK_DATA.currentStep = Math.max(1, Math.min(5, Number(stepNum)));
  renderPlaybookStep();
}

function togglePlaybookBranchMode(mode) {
  window.PLAYBOOK_DATA.currentMode = mode;
  renderPlaybookStep();
}

function togglePlaybookAutoPlay() {
  if (window.PLAYBOOK_DATA.autoPlayTimer) {
    clearInterval(window.PLAYBOOK_DATA.autoPlayTimer);
    window.PLAYBOOK_DATA.autoPlayTimer = null;
    renderPlaybookStep();
  } else {
    window.PLAYBOOK_DATA.autoPlayTimer = setInterval(() => {
      let next = window.PLAYBOOK_DATA.currentStep + 1;
      if (next > 5) next = 1;
      window.PLAYBOOK_DATA.currentStep = next;
      renderPlaybookStep();
    }, 3200);
    renderPlaybookStep();
  }
}

function renderPlaybookStep() {
  const container = document.getElementById("playbook-main-card");
  if (!container) return;

  const data = window.PLAYBOOK_DATA;
  const ind = data.industries[data.currentIndustry] || data.industries.bank;
  const step = ind.steps[data.currentStep] || ind.steps[1];
  const isProtected = data.currentMode === "protected";

  // 1. Sync industry selector tabs in DOM
  const tabs = ["bank", "health", "ecommerce"];
  tabs.forEach(t => {
    const btn = document.getElementById(`pbook-tab-${t}`);
    if (btn) btn.classList.toggle("active", t === data.currentIndustry);
  });

  // 2. Sync stepper buttons in DOM
  for (let i = 1; i <= 5; i++) {
    const btn = document.getElementById(`pstep-btn-${i}`);
    if (btn) btn.classList.toggle("active", i === data.currentStep);
  }

  // 3. Set outer card styling
  container.className = `playbook-main-card ${isProtected ? "mode-safe" : "mode-danger"}`;

  // 4. Render interactive inner card
  container.innerHTML = `
    <div class="scan-laser-line"></div>

    <!-- Top Header -->
    <div class="playbook-header-row">
      <div>
        <div class="playbook-step-pill">PHASE 0${data.currentStep}: ${safePlaybookEscape(step.title.toUpperCase())}</div>
        <div style="font-size:0.84rem;color:var(--text-secondary);margin-top:4px;">
          ${safePlaybookEscape(step.subtitle)} &bull; <span style="font-family:var(--font-mono);font-size:0.78rem;color:var(--text-dim);">${safePlaybookEscape(ind.compliance)}</span>
        </div>
      </div>

      <!-- What-If Branching Toggle -->
      <div class="playbook-branch-toggle-group" title="Toggle between What-If Unprotected Disaster vs With KAVACH Protection">
        <button type="button" class="playbook-toggle-btn safe-mode ${isProtected ? 'active' : ''}" onclick="togglePlaybookBranchMode('protected')">
          🛡️ With KAVACH (Protected)
        </button>
        <button type="button" class="playbook-toggle-btn danger-mode ${!isProtected ? 'active' : ''}" onclick="togglePlaybookBranchMode('unprotected')">
          ⚠️ Without KAVACH (Disaster)
        </button>
      </div>
    </div>

    <!-- Two-Column Process Inspection -->
    <div class="playbook-two-column playbook-animate-fade">
      
      <!-- Left: Developer / User Action -->
      <div class="playbook-event-box">
        <div class="event-box-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Step Action: What The User / AI Does
        </div>
        <p class="event-box-desc">${safePlaybookEscape(step.userAction)}</p>
        <pre class="event-code-snippet ${isProtected ? '' : 'danger'}"><code>${isProtected ? safePlaybookEscape(step.protectedSnippet.split('\\n')[0]) : safePlaybookEscape(step.unprotectedSnippet.split('\\n')[0])}</code></pre>
      </div>

      <!-- Right: KAVACH Real-Time Control Plane Response -->
      <div class="playbook-event-box">
        <div class="event-box-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          System Reaction: ${isProtected ? 'KAVACH Zero-Trust Control Plane' : 'Unprotected Ungoverned Failure'}
        </div>
        <p class="event-box-desc">${isProtected ? safePlaybookEscape(step.kavachAction) : 'No controls present. Raw execution without verification.'}</p>
        <pre class="event-code-snippet ${isProtected ? 'safe' : 'danger'}"><code>${isProtected ? safePlaybookEscape(step.protectedSnippet) : safePlaybookEscape(step.unprotectedSnippet)}</code></pre>
      </div>

    </div>

    <!-- Outcome / Verdict Banner -->
    <div class="playbook-verdict-banner playbook-animate-fade">
      <div class="playbook-verdict-left">
        <span class="playbook-verdict-pill ${isProtected ? step.verdictType : 'block'}">
          ${isProtected ? safePlaybookEscape(step.verdict) : '💥 PRODUCTION BREACH / OUTAGE'}
        </span>
        <span style="font-size:0.84rem;color:var(--text-secondary);font-weight:600;">
          ${isProtected ? safePlaybookEscape(step.metrics) : 'Regulatory Penalty • Production Outage • Stolen Credentials'}
        </span>
      </div>
      <div style="font-size:0.78rem;color:var(--text-dim);font-family:var(--font-mono);">
        Target Repo: ${safePlaybookEscape(ind.repo)}
      </div>
    </div>

    <!-- Controls Row -->
    <div class="playbook-controls-row">
      <div class="playbook-nav-btns">
        <button type="button" class="btn-playbook-step" id="btn-pstep-prev" onclick="selectPlaybookStep(${data.currentStep - 1})" ${data.currentStep === 1 ? 'disabled style="opacity:0.4;cursor:not-allowed;"' : ''}>
          &larr; Previous Process
        </button>
        <button type="button" class="btn-playbook-step" id="btn-pstep-next" onclick="selectPlaybookStep(${data.currentStep + 1})" ${data.currentStep === 5 ? 'disabled style="opacity:0.4;cursor:not-allowed;"' : ''}>
          Next Process &rarr;
        </button>
      </div>

      <button type="button" class="btn-playbook-auto ${data.autoPlayTimer ? 'running' : ''}" id="btn-playbook-auto" onclick="togglePlaybookAutoPlay()">
        ${data.autoPlayTimer ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> ⏸ Pause Walkthrough (Phase 0' + data.currentStep + '/05)' : '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg> ▶ Run Live Animated Walkthrough'}
      </button>
    </div>
  `;

  // Retrigger laser sweep animation
  const laser = container.querySelector('.scan-laser-line');
  if (laser) {
    laser.style.animation = 'none';
    void laser.offsetHeight;
    laser.style.animation = 'playbookScan 2s ease-in-out infinite';
  }
}

// Bind directly to window scope
window.selectPlaybookIndustry = selectPlaybookIndustry;
window.selectPlaybookStep = selectPlaybookStep;
window.togglePlaybookBranchMode = togglePlaybookBranchMode;
window.togglePlaybookAutoPlay = togglePlaybookAutoPlay;
window.renderPlaybookStep = renderPlaybookStep;
window.safePlaybookEscape = safePlaybookEscape;

'''

# Assemble new app.js:
# 1. Main lines before switchToUseCases
# 2. Enhanced playbook code
# 3. Main lines from switchToUseCases up to pbook_start
new_lines = (
    lines[:switch_uc_idx] +
    [enhanced_playbook_code + "\n\n"] +
    lines[switch_uc_idx:pbook_start]
)

new_content = "".join(new_lines)

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"app.js updated successfully! New total lines: {len(new_content.splitlines())}")
