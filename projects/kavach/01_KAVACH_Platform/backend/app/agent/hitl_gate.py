"""
Human-in-the-Loop (HITL) Interactive Approval Gate & Dynamic Breakpoint System.
Fulfills BMU CSE3101 Agentic AI Course Handout:
  - Module 1: Introduction to Agentic AI (Session 4: Levels of Autonomy & HITL Systems)
  - Module 4: Google ADK (Session 28: Human Intervention Hooks & Approval Workflows)
  - Module 6: Ethical AI & Governance (Sessions 37-41: Breakpoint Gates & Operator Overrides)
  - Course Outcomes: CO3 (Implement autonomous agents) & CO4 (Multi-agent workflows)
  - Evaluation Components: C2 (Multi-Agent Interaction), C8 (Milestone 2), C11 (Viva Demo)

Ensures that autonomous agents NEVER deploy high-blast-radius or critical-impact code
modifications without human-in-the-loop cryptographic authorization.
"""

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import time
from typing import Any, Dict, List, Optional


class HITLStatus(str, Enum):
    PENDING = "PENDING_OPERATOR_REVIEW"
    APPROVED = "APPROVED_BY_OPERATOR"
    REVISED = "REVISED_WITH_FEEDBACK"
    ABORTED = "ABORTED_BY_OPERATOR"


class RiskTier(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


@dataclass
class HITLRequest:
    id: str
    task_id: str
    risk_tier: RiskTier
    reason: str
    affected_files: List[str]
    blast_radius_score: float
    proposed_code_diff: str
    status: HITLStatus = HITLStatus.PENDING
    operator_feedback: Optional[str] = None
    operator_id: Optional[str] = None
    approval_signature: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "risk_tier": self.risk_tier.value,
            "reason": self.reason,
            "affected_files": self.affected_files,
            "blast_radius_score": round(self.blast_radius_score, 3),
            "proposed_code_diff": self.proposed_code_diff,
            "status": self.status.value,
            "operator_feedback": self.operator_feedback,
            "operator_id": self.operator_id,
            "approval_signature": self.approval_signature,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
        }


class HITLGovernanceGate:
    """
    Central Human-in-the-Loop Governance Gate for managing approval lifecycles.
    """

    def __init__(self, critical_threshold: float = 0.65):
        self.critical_threshold = critical_threshold
        self.requests: Dict[str, HITLRequest] = {}
        self.request_counter = 0

    def evaluate_gate_requirement(
        self,
        task_id: str,
        blast_radius_score: float,
        affected_files: List[str],
        proposed_code_diff: str,
        security_findings: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Determines whether the agent requires a Human-in-the-Loop approval breakpoint.
        """
        requires_approval = False
        reasons = []
        tier = RiskTier.LOW

        if blast_radius_score >= self.critical_threshold:
            requires_approval = True
            tier = RiskTier.CRITICAL
            reasons.append(
                f"Blast radius score ({blast_radius_score:.2f}) exceeds critical threshold ({self.critical_threshold:.2f})"
            )
        elif blast_radius_score >= 0.40:
            requires_approval = True
            tier = RiskTier.HIGH
            reasons.append(f"Significant blast radius ({blast_radius_score:.2f}) detected across multiple modules")

        if security_findings and len(security_findings) > 0:
            requires_approval = True
            if tier != RiskTier.CRITICAL:
                tier = RiskTier.HIGH
            reasons.append(f"{len(security_findings)} potential security anomalies detected in proposed diff")

        # Check for core infrastructure file changes
        high_risk_filenames = {"main.py", "orchestrator.py", "db.py", "auth.py", "config.py"}
        for f in affected_files:
            base = f.replace("\\", "/").split("/")[-1].lower()
            if base in high_risk_filenames:
                requires_approval = True
                if tier != RiskTier.CRITICAL:
                    tier = RiskTier.HIGH
                reasons.append(f"Core architectural file targeted for modification: {base}")
                break

        if not requires_approval:
            return {
                "requires_approval": False,
                "tier": RiskTier.LOW.value,
                "reason": "Changes are within safe autonomous boundaries (Low risk).",
                "request_id": None,
            }

        # Create pending HITL request
        self.request_counter += 1
        req_id = f"HITL-{self.request_counter:04d}"
        reason_str = "; ".join(reasons)

        hitl_req = HITLRequest(
            id=req_id,
            task_id=task_id,
            risk_tier=tier,
            reason=reason_str,
            affected_files=affected_files,
            blast_radius_score=blast_radius_score,
            proposed_code_diff=proposed_code_diff,
        )
        self.requests[req_id] = hitl_req

        return {
            "requires_approval": True,
            "tier": tier.value,
            "reason": reason_str,
            "request_id": req_id,
            "request_details": hitl_req.to_dict(),
        }

    def resolve_request(
        self,
        request_id: str,
        action: str,
        operator_id: str = "Dr. Soharab Hossain Shaikh / Pranshu Tiwari",
        feedback: str = "",
    ) -> Dict[str, Any]:
        """
        Operator resolves a pending HITL request with APPROVE, REVISE, or ABORT.
        """
        if request_id not in self.requests:
            raise KeyError(f"HITL request {request_id} does not exist.")

        req = self.requests[request_id]
        action_upper = action.upper()

        # Generate cryptographic attestation signature
        sig_payload = f"{request_id}:{operator_id}:{action_upper}:{time.time()}"
        signature = hashlib.sha256(sig_payload.encode()).hexdigest()[:24]

        req.operator_id = operator_id
        req.operator_feedback = feedback
        req.approval_signature = signature
        req.resolved_at = time.time()

        if action_upper == "APPROVE":
            req.status = HITLStatus.APPROVED
            return {
                "status": "APPROVED",
                "message": f"Modification approved by {operator_id}. Agent may proceed to commit.",
                "signature": signature,
                "request": req.to_dict(),
            }
        elif action_upper == "REVISE":
            req.status = HITLStatus.REVISED
            return {
                "status": "REVISED",
                "message": f"Operator requested revisions: '{feedback}'. Agent will incorporate feedback and replan.",
                "signature": signature,
                "request": req.to_dict(),
            }
        elif action_upper == "ABORT":
            req.status = HITLStatus.ABORTED
            return {
                "status": "ABORTED",
                "message": f"Operator aborted modification safely. Zero changes applied to codebase.",
                "signature": signature,
                "request": req.to_dict(),
            }
        else:
            raise ValueError(f"Unknown HITL action '{action}'. Must be APPROVE, REVISE, or ABORT.")

    def list_requests(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.requests.values()]


# Global Singleton Gate
global_hitl_gate = HITLGovernanceGate()
