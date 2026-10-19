"""
FastAPI Server connecting KAVACH Security Shield with Commercial Core Banking Engine.
Exposes full retail & corporate banking modules, Autonomous Highway telemetry,
and real-time cryptographic audit proofs.
"""

import os
import sys
from typing import Optional, Dict, Any, List
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
WORKSPACE_ROOT = os.path.abspath(os.path.join(DASHBOARD_DIR, ".."))

_candidate_kavach_backends = [
    os.path.join(WORKSPACE_ROOT, "01_KAVACH_Platform", "backend"),
    os.path.join(WORKSPACE_ROOT, "important", "kavach", "backend"),
    os.path.join(CURRENT_DIR, "..", "important", "kavach", "backend"),
]
PROJECT_ROOT = next((p for p in _candidate_kavach_backends if os.path.exists(p)), _candidate_kavach_backends[0])

for p in [WORKSPACE_ROOT, DASHBOARD_DIR, CURRENT_DIR, PROJECT_ROOT]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from implementation_banks.core_banking import global_core_bank
from implementation_banks.kavach_banking_shield import global_banking_shield
from implementation_banks.advanced_banking_engines import (
    DistributedSagaOrchestrator,
    MakerCheckerWorkflow,
    OpenTelemetryTracer,
    DynamicVelocityAnomalyDetector,
    RbiCbdcDigitalRupeeLedger,
    ChaosStressWorkbench,
    TimeLockSmartEscrow,
    BaselThreePrudentialTelemetry,
    RegulatoryComplianceDossierGenerator,
)

# Advanced Enterprise Engines
global_saga_orchestrator = DistributedSagaOrchestrator(global_core_bank, global_banking_shield)
global_maker_checker = MakerCheckerWorkflow(global_core_bank, global_banking_shield)
global_otel_tracer = OpenTelemetryTracer()
global_anomaly_detector = DynamicVelocityAnomalyDetector()
global_cbdc_ledger = RbiCbdcDigitalRupeeLedger(global_core_bank)
global_chaos_workbench = ChaosStressWorkbench(global_core_bank, global_banking_shield)
global_timelock_escrow = TimeLockSmartEscrow(global_core_bank, global_banking_shield)
global_basel3_telemetry = BaselThreePrudentialTelemetry(global_core_bank)
global_compliance_dossier = RegulatoryComplianceDossierGenerator(global_core_bank, global_banking_shield, global_maker_checker)

# Unified Results Hub Persistence Hook
try:
    RESULTS_HUB_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "results"))
    if RESULTS_HUB_PATH not in sys.path:
        sys.path.insert(0, RESULTS_HUB_PATH)
    from results_hub import record_unified_event
except Exception:
    def record_unified_event(*args, **kwargs):
        pass

app = FastAPI(
    title="Bharat Core Bank × KAVACH AI Governance Platform",
    description="Tier-1 Commercial Banking Engine with Autonomous Highway Simulation & Post-Quantum Cryptographic Proofs",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request Models ---

class TransferRequest(BaseModel):
    sender_acc: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    receiver_acc: str = Field(..., json_schema_extra={"example": "ICIC00045678901"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 5000.0})
    memo: str = Field("", json_schema_extra={"example": "Vendor monthly invoice payment"})
    transfer_type: str = Field("UPI", json_schema_extra={"example": "UPI"})
    expected_sender_version: Optional[int] = Field(None, json_schema_extra={"example": 1})


class ScanMemoRequest(BaseModel):
    memo: str = Field(..., json_schema_extra={"example": "Payment for services"})


class HitlActionRequest(BaseModel):
    pending_id: str = Field(...)
    officer_id: Optional[str] = Field("OFFICER-RAJESH-99")
    officer_notes: Optional[str] = Field("Approved after verifying KYC & AML risk score")


class CreateDepositRequest(BaseModel):
    account_number: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    principal: float = Field(..., gt=0, json_schema_extra={"example": 50000.0})
    tenure_months: int = Field(12, ge=1, le=120)
    is_senior_citizen: bool = Field(False)


class LiquidateDepositRequest(BaseModel):
    fd_id: str = Field(...)
    is_premature: bool = Field(True)


class FreezeCardRequest(BaseModel):
    card_id: str = Field(...)


class UpdateCardLimitsRequest(BaseModel):
    card_id: str = Field(...)
    pos_daily_limit: Optional[float] = None
    online_daily_limit: Optional[float] = None
    international_allowed: Optional[bool] = None


class AddBeneficiaryRequest(BaseModel):
    owner_account: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    beneficiary_account: str = Field(..., json_schema_extra={"example": "ICIC00045678901"})
    name: str = Field(..., json_schema_extra={"example": "Ananya Sharma"})
    ifsc_code: str = Field(..., json_schema_extra={"example": "ICIC0000042"})
    nickname: Optional[str] = Field("")


class CreateMandateRequest(BaseModel):
    account_number: str = Field(...)
    beneficiary_account: str = Field(...)
    amount: float = Field(...)
    frequency: str = Field("MONTHLY")
    category: str = Field("SIP_MUTUAL_FUND")
    description: Optional[str] = Field("")


class ApplyOverdraftRequest(BaseModel):
    account_number: str = Field(...)
    requested_limit: float = Field(...)


class KillswitchToggleRequest(BaseModel):
    active: bool = Field(...)
    reason: Optional[str] = Field("")
    officer_id: Optional[str] = Field("CISO-SUPERADMIN-01")


class SagaTransferRequest(BaseModel):
    sender_acc: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    receiver_acc: str = Field(..., json_schema_extra={"example": "ICIC00045678901"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 50000.0})
    memo: str = Field("", json_schema_extra={"example": "Protected Saga distributed vendor payment"})
    transfer_type: str = Field("UPI", json_schema_extra={"example": "UPI"})
    simulate_failure_at_step: Optional[str] = Field(None, json_schema_extra={"example": "STEP_2"})


class MakerRequestModel(BaseModel):
    maker_id: str = Field("MAKER-OFFICER-PRIYA", json_schema_extra={"example": "MAKER-OFFICER-PRIYA"})
    action_type: str = Field("HIGH_VALUE_TRANSFER", json_schema_extra={"example": "HIGH_VALUE_TRANSFER"})
    payload: Dict[str, Any] = Field(...)
    business_justification: str = Field("Corporate quarterly dividend disbursement", json_schema_extra={"example": "Corporate quarterly dividend disbursement"})


class CheckerApproveModel(BaseModel):
    request_id: str = Field(...)
    checker_id: str = Field("CHECKER-OFFICER-ARUN", json_schema_extra={"example": "CHECKER-OFFICER-ARUN"})
    checker_notes: str = Field("Dual-control authorized after AML check", json_schema_extra={"example": "Dual-control authorized after AML check"})


class CheckerRejectModel(BaseModel):
    request_id: str = Field(...)
    checker_id: str = Field("CHECKER-OFFICER-ARUN", json_schema_extra={"example": "CHECKER-OFFICER-ARUN"})
    rejection_reason: str = Field("Adverse media sanction alert flagged", json_schema_extra={"example": "Adverse media sanction alert flagged"})


class AnomalyEvalRequest(BaseModel):
    account_number: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 45000.0})
    origin_city: str = Field("MUMBAI", json_schema_extra={"example": "MUMBAI"})
    origin_ip: str = Field("103.21.244.0", json_schema_extra={"example": "103.21.244.0"})


class CbdcMintRequest(BaseModel):
    account_number: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    target_wallet: str = Field("WALLET-DHRUV-CBDC", json_schema_extra={"example": "WALLET-DHRUV-CBDC"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 2500.0})


class CbdcTransferRequest(BaseModel):
    sender_wallet: str = Field(..., json_schema_extra={"example": "WALLET-DHRUV-CBDC"})
    receiver_wallet: str = Field(..., json_schema_extra={"example": "WALLET-MERCHANT-CBDC"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 500.0})


class CbdcRedeemRequest(BaseModel):
    wallet_id: str = Field(..., json_schema_extra={"example": "WALLET-DHRUV-CBDC"})
    account_number: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 500.0})


class ChaosOccRaceRequest(BaseModel):
    account_number: str = Field("SBIN00012345678", json_schema_extra={"example": "SBIN00012345678"})
    workers: int = Field(15, ge=2, le=30, json_schema_extra={"example": 15})
    transfer_amount: float = Field(100.0, gt=0, json_schema_extra={"example": 100.0})


class EscrowCreateRequest(BaseModel):
    sender_acc: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    receiver_acc: str = Field(..., json_schema_extra={"example": "ICIC00045678901"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 10000.0})
    duration_seconds: int = Field(60, ge=10, le=600, json_schema_extra={"example": 60})
    memo: str = Field("Protected Time-Lock Escrow Transfer", json_schema_extra={"example": "Protected Time-Lock Escrow Transfer"})


class EscrowClawbackRequest(BaseModel):
    escrow_id: str = Field(...)
    sender_acc: str = Field(..., json_schema_extra={"example": "SBIN00012345678"})
    reason: str = Field("Emergency fraud clawback", json_schema_extra={"example": "Emergency fraud clawback"})


# =============================================================================
# 1. ACCOUNTS & BALANCE LEDGER ROUTES
# =============================================================================

@app.get("/api/accounts")
def get_accounts():
    """List all accounts with statutory PII masking."""
    return {"accounts": global_banking_shield.bank.list_all_accounts(mask_sensitive=True)}


@app.get("/api/accounts/unmasked")
def get_unmasked_accounts():
    """Unmasked account view for authorized banking officers."""
    return {"accounts": global_banking_shield.bank.list_all_accounts(mask_sensitive=False)}


@app.get("/api/accounts/{account_number}")
def get_single_account(account_number: str):
    """Retrieve details for a specific bank account."""
    acc = global_banking_shield.bank.get_account(account_number)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found.")
    return {"account": acc.to_dict(mask_sensitive=False)}


# =============================================================================
# 2. FUND TRANSFERS & 5-GATE SHIELD PIPELINE
# =============================================================================

@app.post("/api/scan-memo")
def scan_memo_preflight(req: ScanMemoRequest):
    """Pre-flight memo screening with Zero-Knowledge PII Masking and Polyglot Normalization."""
    masked_memo, vault_id, vault_meta = global_banking_shield.scan_and_mask_pii(req.memo)
    injection_res = global_banking_shield.inspect_transaction_memo(req.memo)

    return {
        "raw_memo": req.memo,
        "masked_memo": masked_memo,
        "pii_detected": vault_meta.get("tokenized", False),
        "pii_tokens_count": vault_meta.get("tokens_created", 0),
        "is_safe": injection_res["is_safe"],
        "threat_detected": injection_res["threat_detected"],
        "risk_level": injection_res["risk_level"],
        "threat_category": injection_res["threat_category"],
        "explanation": injection_res["explanation"],
        "polyglot_transformations": injection_res.get("polyglot_transformations", []),
    }


@app.post("/api/transfer")
def transfer_funds(req: TransferRequest):
    """Execute transfer through KAVACH 5-Gate pipeline with thread-safety and HSM seal."""
    # 1. Start OpenTelemetry distributed trace with W3C traceparent
    trace = global_otel_tracer.start_trace("TRANSFER_FUNDS", {
        "sender": req.sender_acc,
        "receiver": req.receiver_acc,
        "amount": req.amount,
        "type": req.transfer_type
    })

    t0 = time.time()
    # 2. Dynamic Velocity & Anomaly Risk Scan
    anomaly_eval = global_anomaly_detector.evaluate_risk(req.sender_acc, req.amount)
    global_otel_tracer.add_span(trace["trace_id"], "anomaly_risk_scan", int((time.time() - t0) * 1000000), "OK", attributes=anomaly_eval)

    # 3. Governed Core Pipeline
    t1 = time.time()
    result = global_banking_shield.process_governed_transfer(
        sender_acc=req.sender_acc,
        receiver_acc=req.receiver_acc,
        amount=req.amount,
        memo=req.memo,
        transfer_type=req.transfer_type,
        expected_sender_version=req.expected_sender_version,
    )
    span_status = "OK" if result.get("status") in ["SUCCESS", "REQUIRES_HITL_APPROVAL"] else "ERROR"
    global_otel_tracer.add_span(trace["trace_id"], "kavach_core_pipeline", int((time.time() - t1) * 1000000), span_status, attributes={"status": result.get("status")})

    # Finalize OpenTelemetry trace
    fin_trace = global_otel_tracer.finalize_trace(trace["trace_id"])

    result["w3c_traceparent"] = trace["w3c_traceparent"]
    result["trace_id"] = trace["trace_id"]
    result["anomaly_evaluation"] = anomaly_eval
    result["spans"] = fin_trace.get("spans", []) if fin_trace else []

    # Auto-persist to Unified Results Dashboard
    try:
        status_val = result.get("status", "SUCCESS")
        risk_score = 0.0
        risk_level = "LOW"
        category = "TRANSFER"
        if status_val == "BLOCKED_BY_KAVACH":
            status_clean = "BLOCKED"
            risk_score = 0.95
            risk_level = "CRITICAL"
            category = "INJECTION_SHIELD"
            action_title = f"Transfer Blocked: {result.get('threat_category', 'Prompt Injection')}"
            summary = result.get("explanation", f"KAVACH Shield blocked transfer of INR {req.amount:,.2f}")
        elif status_val == "REQUIRES_HITL_APPROVAL":
            status_clean = "REQUIRES_HITL_APPROVAL"
            risk_score = 0.60
            risk_level = "MEDIUM"
            category = "HITL"
            action_title = f"High-Value HITL Quarantined: INR {req.amount:,.2f}"
            summary = result.get("message", f"Transfer of INR {req.amount:,.2f} quarantined for human sign-off")
        else:
            status_clean = "SUCCESS"
            risk_score = 0.02
            risk_level = "SAFE"
            category = "TRANSFER"
            action_title = f"{req.transfer_type} Transfer Cleared: INR {req.amount:,.2f}"
            summary = f"Transferred INR {req.amount:,.2f} via {req.transfer_type}. Memo: '{req.memo}'"

        import uuid
        record_unified_event(
            platform="BANKING",
            category=category,
            action_title=action_title,
            actor=req.sender_acc,
            target=req.receiver_acc,
            status=status_clean,
            risk_score=risk_score,
            risk_level=risk_level,
            amount=req.amount,
            summary=summary,
            details=result,
            event_id=f"BANK-TXN-{result.get('transaction_id', result.get('request_id', uuid.uuid4().hex[:8].upper()))}"
        )
    except Exception:
        pass

    return result


# =============================================================================
# 3. TRANSACTION HISTORY & CRYPTOGRAPHIC E-RECEIPTS
# =============================================================================

@app.get("/api/transactions")
def get_transactions(
    account_number: Optional[str] = None,
    transfer_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    search: Optional[str] = None,
):
    """Search and filter complete transaction history."""
    records = global_banking_shield.bank.get_transaction_history(
        account_number=account_number,
        transfer_type=transfer_type,
        status=status,
        limit=limit,
        search_query=search,
    )
    return {"total": len(records), "transactions": records}


@app.get("/api/receipt/{transaction_id}")
def get_receipt(transaction_id: str):
    """Generate statutory e-Receipt with cryptographic verification hashes."""
    receipt = global_banking_shield.bank.generate_transaction_receipt(transaction_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Transaction record not found.")

    # Attach Merkle and HSM info
    receipt["hsm_key_id"] = global_banking_shield.hsm.key_id
    receipt["merkle_root"] = global_banking_shield.merkle_ledger.get_root_hash()
    return receipt


# =============================================================================
# 4. FIXED DEPOSITS & TERM INVESTMENTS
# =============================================================================

@app.get("/api/deposits")
def get_deposits(account_number: Optional[str] = None):
    """List active and matured Fixed Deposits."""
    return {"deposits": global_banking_shield.bank.list_fixed_deposits(account_number=account_number)}


@app.post("/api/deposits/create")
def create_deposit(req: CreateDepositRequest):
    """Book a new Fixed Deposit with compound quarterly interest."""
    res = global_banking_shield.bank.create_fixed_deposit(
        account_number=req.account_number,
        principal=req.principal,
        tenure_months=req.tenure_months,
        is_senior_citizen=req.is_senior_citizen,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.post("/api/deposits/liquidate")
def liquidate_deposit(req: LiquidateDepositRequest):
    """Liquidate a Fixed Deposit with penalty calculation."""
    res = global_banking_shield.bank.liquidate_fixed_deposit(
        fd_id=req.fd_id,
        is_premature=req.is_premature,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


# =============================================================================
# 5. VIRTUAL DEBIT CARDS & CARD CONTROLS
# =============================================================================

@app.get("/api/cards")
def get_cards(account_number: Optional[str] = None):
    """List virtual debit cards linked to account."""
    return {"cards": global_banking_shield.bank.list_virtual_cards(account_number=account_number)}


@app.post("/api/cards/freeze")
def freeze_card(req: FreezeCardRequest):
    """Instantly toggle freeze on a virtual debit card."""
    res = global_banking_shield.bank.toggle_card_freeze(req.card_id)
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.post("/api/cards/limits")
def update_card_limits(req: UpdateCardLimitsRequest):
    """Update POS, online, and international card spending limits."""
    res = global_banking_shield.bank.update_card_limits(
        card_id=req.card_id,
        pos_daily_limit=req.pos_daily_limit,
        online_daily_limit=req.online_daily_limit,
        international_allowed=req.international_allowed,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


# =============================================================================
# 6. BENEFICIARY REGISTRY & COOLING-OFF GUARDRAILS
# =============================================================================

@app.get("/api/beneficiaries")
def get_beneficiaries(owner_account: Optional[str] = None):
    """List registered beneficiaries with cooling-off status."""
    return {"beneficiaries": global_banking_shield.bank.list_beneficiaries(owner_account=owner_account)}


@app.post("/api/beneficiaries/add")
def add_beneficiary(req: AddBeneficiaryRequest):
    """Add a new beneficiary with mandatory 4-hour cooling limit."""
    res = global_banking_shield.bank.add_beneficiary(
        owner_account=req.owner_account,
        beneficiary_account=req.beneficiary_account,
        name=req.name,
        ifsc_code=req.ifsc_code,
        nickname=req.nickname or "",
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


# =============================================================================
# 7. STANDING INSTRUCTIONS & AUTO-DEBIT RECURRING MANDATES
# =============================================================================

@app.get("/api/standing-instructions")
def get_standing_instructions(account_number: Optional[str] = None):
    """List active recurring auto-debit mandates."""
    return {"mandates": global_banking_shield.bank.list_standing_instructions(account_number=account_number)}


@app.post("/api/standing-instructions/create")
def create_standing_instruction(req: CreateMandateRequest):
    """Set up an automated monthly/weekly SIP or utility mandate."""
    res = global_banking_shield.bank.create_standing_instruction(
        account_number=req.account_number,
        beneficiary_account=req.beneficiary_account,
        amount=req.amount,
        frequency=req.frequency,
        category=req.category,
        description=req.description or "",
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


# =============================================================================
# 8. OVERDRAFT & CIBIL BUREAU CREDIT FACILITY
# =============================================================================

@app.post("/api/overdraft/apply")
def apply_overdraft(req: ApplyOverdraftRequest):
    """Assess and activate instant overdraft line based on balance & CIBIL score."""
    res = global_banking_shield.bank.apply_overdraft_facility(
        account_number=req.account_number,
        requested_limit=req.requested_limit,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


# =============================================================================
# 9. MULTI-CURRENCY FOREX & REMITTANCE
# =============================================================================

@app.get("/api/forex/rates")
def get_forex_rates():
    """Live foreign exchange rates with LRS 20% TCS calculation."""
    return global_banking_shield.bank.get_forex_rates()


# =============================================================================
# 10. AML SURVEILLANCE & CISO GLOBAL KILLSWITCH
# =============================================================================

@app.get("/api/aml/sar-reports")
def get_sar_reports():
    """Retrieve FinCEN / RBI Suspicious Activity Reports (SAR)."""
    return {"sar_reports": global_banking_shield.bank.sar_reports}


@app.get("/api/killswitch/status")
def get_killswitch_status():
    """Check emergency platform killswitch status."""
    return {
        "global_killswitch_active": global_banking_shield.bank.global_killswitch_active,
        "reason": global_banking_shield.bank.killswitch_reason,
    }


@app.post("/api/killswitch/toggle")
def toggle_killswitch(req: KillswitchToggleRequest):
    """Emergency halt of all outbound automated banking transfers."""
    res = global_banking_shield.bank.toggle_global_killswitch(
        active=req.active,
        reason=req.reason or "",
        officer_id=req.officer_id or "CISO-SUPERADMIN-01",
    )
    return res


# =============================================================================
# 11. HITL COMPLIANCE DESK & MERKLE AUDIT
# =============================================================================

@app.get("/api/hitl/pending")
def list_pending_hitl():
    """List high-value transfers awaiting Senior Compliance Officer sign-off."""
    return {"pending_transactions": global_banking_shield.get_pending_hitl_transfers()}


@app.post("/api/hitl/approve")
def approve_hitl_transfer(req: HitlActionRequest):
    """Compliance Officer authorizes a queued high-value transfer."""
    res = global_banking_shield.approve_hitl_transfer(
        pending_id=req.pending_id,
        approver_officer_id=req.officer_id or "OFFICER-RAJESH-SENIOR",
        officer_notes=req.officer_notes or "Statutory high-value authorization approved"
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    try:
        record_unified_event(
            platform="BANKING",
            category="HITL",
            action_title=f"HITL Approved: {req.pending_id}",
            actor=req.officer_id or "OFFICER-RAJESH-SENIOR",
            target="Settlement Ledger",
            status="SUCCESS",
            risk_score=0.1,
            risk_level="LOW",
            amount=float(res.get("amount", 0.0) or 0.0),
            summary=f"Senior Officer approved quarantined high-value transfer {req.pending_id}. Notes: {req.officer_notes}",
            details=res,
            event_id=f"BANK-HITL-APP-{req.pending_id}"
        )
    except Exception:
        pass
    return res


@app.post("/api/hitl/reject")
def reject_hitl_transfer(req: HitlActionRequest):
    """Compliance Officer declines a queued high-value transfer."""
    res = global_banking_shield.reject_hitl_transfer(
        pending_id=req.pending_id,
        rejector_officer_id=req.officer_id or "OFFICER-RAJESH-SENIOR",
        reason=req.officer_notes or "Compliance verification failed."
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    try:
        record_unified_event(
            platform="BANKING",
            category="HITL",
            action_title=f"HITL Declined: {req.pending_id}",
            actor=req.officer_id or "OFFICER-RAJESH-SENIOR",
            target="Quarantine Queue",
            status="BLOCKED",
            risk_score=0.75,
            risk_level="HIGH",
            summary=f"Senior Officer declined high-value transfer {req.pending_id}. Reason: {req.officer_notes}",
            details=res,
            event_id=f"BANK-HITL-REJ-{req.pending_id}"
        )
    except Exception:
        pass
    return res


@app.get("/api/merkle/ledger")
def get_merkle_ledger(limit: int = Query(20, ge=1, le=100)):
    """Retrieve immutable Merkle Tree root and recent entries."""
    entries = global_banking_shield.merkle_ledger.entries[-limit:]
    return {
        "crypto_suite": global_banking_shield.merkle_ledger.crypto_suite,
        "merkle_root": global_banking_shield.merkle_ledger.get_merkle_root(),
        "total_records": len(global_banking_shield.merkle_ledger.entries),
        "recent_entries": entries,
    }


@app.get("/api/merkle/proof/{index}")
def get_merkle_proof(index: int):
    """Generate cryptographic inclusion proof with HSM Digital Signature for RBI auditor."""
    try:
        proof = global_banking_shield.get_merkle_inclusion_proof(index)
        is_valid = global_banking_shield.merkle_ledger.verify_inclusion(
            leaf_hash=proof["leaf_hash"],
            proof=proof["proof_path"],
            expected_root=proof["merkle_root"],
            crypto_suite=proof["crypto_suite"],
        )
        proof["is_cryptographically_verified"] = is_valid
        return proof
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/merkle/verify")
def verify_ledger():
    """Verify entire ledger integrity with HSM signature validation."""
    return global_banking_shield.verify_ledger_integrity()


@app.get("/api/hsm/status")
def get_hsm_status():
    """Software-Defined HSM Enclave status."""
    return {
        "status": "ACTIVE",
        "enclave_standard": "FIPS_140_2_LEVEL_3_SIMULATED",
        "key_id": global_banking_shield.hsm.key_id,
        "epoch": global_banking_shield.hsm.epoch,
        "signatures_issued": global_banking_shield.hsm.signatures_generated,
        "algorithm": "HMAC_SHA3_512_ENCLAVE_MASTER",
    }


@app.get("/api/persistence/status")
def get_persistence_status():
    """Check atomic write-ahead disk journal status."""
    return {
        "status": "PERSISTED",
        "engine": "ATOMIC_WRITE_AHEAD_JOURNAL",
        "path": global_banking_shield.bank.persistence_path,
        "file_exists": os.path.exists(global_banking_shield.bank.persistence_path),
        "concurrency_control": "OPTIMISTIC_VERSIONING_OCC",
        "thread_lock": "REENTRANT_RLOCK",
    }


@app.get("/api/stats")
def get_system_stats():
    """System health & CISO security telemetry."""
    return global_banking_shield.get_system_status()


@app.post("/api/reset-demo")
def reset_demo():
    """Reset balances and states for fresh presentation demo."""
    global_banking_shield.bank.reset_to_genesis()
    global_banking_shield.pending_hitl_transactions.clear()
    return {"status": "SUCCESS", "message": "Bank demo state successfully re-initialized."}


# =============================================================================
# 12. DISTRIBUTED SAGA ORCHESTRATOR ROUTES (ACID COMPENSATING 2PC)
# =============================================================================

@app.post("/api/saga/transfer")
def execute_saga_transfer(req: SagaTransferRequest):
    """Execute distributed multi-phase Saga transfer with automatic compensating reversal."""
    res = global_saga_orchestrator.execute_saga_transfer(
        sender_acc=req.sender_acc,
        receiver_acc=req.receiver_acc,
        amount=req.amount,
        memo=req.memo,
        transfer_type=req.transfer_type,
        simulate_failure_at_step=req.simulate_failure_at_step,
    )
    try:
        is_succ = res.get("status") == "SUCCESS"
        record_unified_event(
            platform="BANKING",
            category="SAGA",
            action_title=f"Distributed Saga Transfer: INR {req.amount:,.2f}",
            actor=req.sender_acc,
            target=req.receiver_acc,
            status="SUCCESS" if is_succ else "BLOCKED",
            risk_score=0.04 if is_succ else 0.45,
            risk_level="SAFE" if is_succ else "MEDIUM",
            amount=req.amount,
            summary=f"Saga execution across steps. Result: {res.get('status')}. Failed step: {res.get('failed_step', 'None')}",
            details=res,
            event_id=f"BANK-SAGA-{res.get('saga_id', uuid.uuid4().hex[:8].upper())}"
        )
    except Exception:
        pass
    return res


@app.get("/api/saga/list")
def list_saga_transactions(limit: int = Query(30, ge=1, le=100)):
    """Retrieve history of distributed Saga executions and compensating rollbacks."""
    return {"sagas": global_saga_orchestrator.list_sagas(limit=limit)}


# =============================================================================
# 13. MAKER-CHECKER DUAL-CONTROL WORKFLOW (RBI FOUR-EYES STATUTORY PROTOCOL)
# =============================================================================

@app.get("/api/maker-checker/requests")
def list_maker_checker_requests():
    """List pending and executed dual-authorization requests."""
    return {"requests": global_maker_checker.list_requests()}


@app.post("/api/maker-checker/create")
def create_maker_request(req: MakerRequestModel):
    """Maker (Initiating Officer) logs dual-control proposal."""
    return global_maker_checker.create_maker_request(
        maker_id=req.maker_id,
        action_type=req.action_type,
        payload=req.payload,
        business_justification=req.business_justification,
    )


@app.post("/api/maker-checker/approve")
def approve_checker_request(req: CheckerApproveModel):
    """Checker (Supervisory Officer) authorizes request with distinct cryptographic seal."""
    res = global_maker_checker.approve_checker_request(
        request_id=req.request_id,
        checker_id=req.checker_id,
        checker_notes=req.checker_notes,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.post("/api/maker-checker/reject")
def reject_checker_request(req: CheckerRejectModel):
    """Checker declines request."""
    res = global_maker_checker.reject_checker_request(
        request_id=req.request_id,
        checker_id=req.checker_id,
        rejection_reason=req.rejection_reason,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


# =============================================================================
# 14. OPENTELEMETRY DISTRIBUTED TRACING & W3C TRACEPARENT PIPELINE
# =============================================================================

@app.get("/api/opentelemetry/traces")
def get_opentelemetry_traces(limit: int = Query(15, ge=1, le=50)):
    """Retrieve microsecond-level distributed trace spans for visual waterfall."""
    return {"traces": global_otel_tracer.get_recent_traces(limit=limit)}


# =============================================================================
# 15. DYNAMIC VELOCITY & IMPOSSIBLE TRAVEL ANOMALY RADAR
# ==============================================================================

@app.post("/api/anomaly/evaluate")
def evaluate_anomaly_risk(req: AnomalyEvalRequest):
    """Compute real-time multi-dimensional behavioral risk score (0-100)."""
    return global_anomaly_detector.evaluate_risk(
        account_number=req.account_number,
        amount=req.amount,
        origin_city=req.origin_city,
        origin_ip=req.origin_ip,
    )


# =============================================================================
# 16. RBI CBDC (DIGITAL RUPEE / e-INR) TOKENIZED BEARER VAULT
# =============================================================================

@app.get("/api/cbdc/wallet")
def get_cbdc_wallet(wallet_id: str = Query("WALLET-DHRUV-CBDC")):
    """Get e-INR token wallet balance and discrete bearer notes."""
    return global_cbdc_ledger.get_wallet_summary(wallet_id)


@app.post("/api/cbdc/mint")
def mint_cbdc_tokens(req: CbdcMintRequest):
    """Debit commercial bank account and mint official RBI e-INR token notes."""
    res = global_cbdc_ledger.mint_tokens_from_bank_account(
        account_number=req.account_number,
        target_wallet=req.target_wallet,
        amount=req.amount,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.post("/api/cbdc/transfer")
def transfer_cbdc_tokens(req: CbdcTransferRequest):
    """Peer-to-peer CBDC bearer token transfer with double-spend validation."""
    res = global_cbdc_ledger.transfer_tokens(
        sender_wallet=req.sender_wallet,
        receiver_wallet=req.receiver_wallet,
        amount=req.amount,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.post("/api/cbdc/redeem")
def redeem_cbdc_tokens(req: CbdcRedeemRequest):
    """Burn e-INR tokens and credit back to commercial bank account."""
    res = global_cbdc_ledger.redeem_tokens_to_bank_account(
        wallet_id=req.wallet_id,
        account_number=req.account_number,
        amount=req.amount,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


# =============================================================================
# 17. CHAOS ENGINEERING & OCC CONCURRENCY STRESS WORKBENCH
# =============================================================================

@app.post("/api/chaos/occ-race")
def run_chaos_occ_stress_test(req: ChaosOccRaceRequest):
    """Simulate 15-20 concurrent threads racing to drain the same account version."""
    return global_chaos_workbench.run_occ_concurrency_race(
        account_number=req.account_number,
        workers=req.workers,
        transfer_amount=req.transfer_amount,
    )


# =============================================================================
# 18. TIME-LOCK SMART ESCROW WITH EMERGENCY CLAWBACK
# =============================================================================

@app.post("/api/escrow/create")
def create_timelock_escrow(req: EscrowCreateRequest):
    """Lock funds into revocable escrow with countdown window."""
    res = global_timelock_escrow.create_timelock_escrow(
        sender_acc=req.sender_acc,
        receiver_acc=req.receiver_acc,
        amount=req.amount,
        duration_seconds=req.duration_seconds,
        memo=req.memo,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.post("/api/escrow/clawback")
def emergency_escrow_clawback(req: EscrowClawbackRequest):
    """Sender immediately halts and refunds escrowed funds before expiration."""
    res = global_timelock_escrow.emergency_clawback(
        escrow_id=req.escrow_id,
        sender_acc=req.sender_acc,
        reason=req.reason,
    )
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@app.get("/api/escrow/list")
def list_escrows():
    """List active, matured, and clawed-back escrows."""
    return {"escrows": global_timelock_escrow.list_escrows()}


# =============================================================================
# 19. BASEL III CAPITAL ADEQUACY & PRUDENTIAL LIQUIDITY (LCR) TELEMETRY
# =============================================================================

@app.get("/api/basel3/telemetry")
def get_basel3_telemetry():
    """Prudential solvency metrics: LCR, CRAR, SLR, and CRR reserves."""
    return global_basel3_telemetry.get_prudential_metrics()


# =============================================================================
# 20. STATUTORY RBI REGULATORY COMPLIANCE DOSSIER & CERTIFICATE
# =============================================================================

@app.get("/api/compliance/dossier")
def get_regulatory_compliance_dossier():
    """Formal RBI institutional audit dossier with NIST SHA3 Merkle root & HSM seal."""
    return global_compliance_dossier.generate_dossier()


# Mount Static Files for frontend
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(CURRENT_DIR, "index.html"))

@app.get("/style.css")
def serve_css():
    return FileResponse(os.path.join(CURRENT_DIR, "style.css"))

@app.get("/app.js")
def serve_js():
    return FileResponse(os.path.join(CURRENT_DIR, "app.js"))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8050)
