"""
Workflow state machine (Phase 2 — see docs/AGENT_SPEC.md).

Defines the stages a developer request moves through, and a simple in-memory
store for workflow runs. This will move to the real database (see
docs/DATABASE_SPEC.md) once Phase 1's DB layer is wired in — kept in-memory
for now so Phase 2 can be built and tested independently.
"""

import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class WorkflowStage(str, Enum):
    REQUEST_RECEIVED = "REQUEST_RECEIVED"
    PLANNING = "PLANNING"
    CONTEXT_RETRIEVAL = "CONTEXT_RETRIEVAL"
    IMPACT_ANALYSIS = "IMPACT_ANALYSIS"       # Phase 5 — not implemented yet, passthrough for now
    GENERATION = "GENERATION"                  # Phase 3 — not implemented yet, passthrough for now
    SECURITY_CHECK = "SECURITY_CHECK"           # uses the Phase-0 /detect logic
    TEST_GENERATION = "TEST_GENERATION"         # Phase 3 — not implemented yet, passthrough for now
    BUILD_AND_TEST = "BUILD_AND_TEST"           # Phase 3/7 — not implemented yet, passthrough for now
    CICD_GATE = "CICD_GATE"                     # Phase 7 — not implemented yet, passthrough for now
    NEEDS_REVIEW = "NEEDS_REVIEW"
    BLOCKED = "BLOCKED"
    COMPLETE = "COMPLETE"


@dataclass
class WorkflowRun:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    request_text: str = ""
    stage: WorkflowStage = WorkflowStage.REQUEST_RECEIVED
    plan: list[str] = field(default_factory=list)
    retrieved_context: list[dict] = field(default_factory=list)
    security_findings: list[dict] = field(default_factory=list)
    generation_result: dict = field(default_factory=dict)
    validation_result: dict = field(default_factory=dict)
    impact_report: list[dict] = field(default_factory=list)
    policy_decision: dict = field(default_factory=dict)
    redacted_request_text: str = ""  # audit-safe version — see security/audit_redaction.py
    history: list[str] = field(default_factory=list)  # human-readable stage log
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
    duration_ms: float = 0.0
    run_type: str = "workflow"  # workflow, self_heal, review, pypi
    metadata: dict = field(default_factory=dict)

    def advance(self, new_stage: WorkflowStage, note: str = ""):
        self.history.append(f"{self.stage} -> {new_stage}" + (f" ({note})" if note else ""))
        self.stage = new_stage

    def to_dict(self) -> dict:
        stage_str = self.stage.value if hasattr(self.stage, "value") else str(self.stage)
        verdict = "BLOCKED" if "BLOCKED" in stage_str else ("NEEDS_REVIEW" if "NEEDS_REVIEW" in stage_str else "ALLOWED")
        return {
            "id": self.id,
            "workflow_id": self.id,
            "timestamp": self.timestamp,
            "request_text": self.request_text,
            "final_stage": stage_str,
            "stage": stage_str,
            "verdict": verdict,
            "plan": self.plan,
            "retrieved_context": self.retrieved_context,
            "security_findings": self.security_findings,
            "generation_result": self.generation_result,
            "validation_result": self.validation_result,
            "impact_report": self.impact_report,
            "policy_decision": self.policy_decision,
            "redacted_request_text": self.redacted_request_text,
            "history": self.history,
            "duration_ms": self.duration_ms,
            "run_type": self.run_type,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorkflowRun":
        raw_stage = data.get("stage", data.get("final_stage", "REQUEST_RECEIVED"))
        try:
            stage = WorkflowStage(raw_stage)
        except Exception:
            stage = WorkflowStage.REQUEST_RECEIVED

        run = cls(
            id=data.get("id", data.get("workflow_id", str(uuid.uuid4()))),
            request_text=data.get("request_text", ""),
            stage=stage,
            plan=data.get("plan", []),
            retrieved_context=data.get("retrieved_context", []),
            security_findings=data.get("security_findings", []),
            generation_result=data.get("generation_result", {}),
            validation_result=data.get("validation_result", {}),
            impact_report=data.get("impact_report", []),
            policy_decision=data.get("policy_decision", {}),
            redacted_request_text=data.get("redacted_request_text", ""),
            history=data.get("history", []),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")),
            duration_ms=data.get("duration_ms", 0.0),
            run_type=data.get("run_type", "workflow"),
            metadata=data.get("metadata", {}),
        )
        return run


# Persistent disk store — saves runs to backend/data/workflow_runs.json
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
RUNS_FILE = os.path.join(DATA_DIR, "workflow_runs.json")

_workflow_runs: dict[str, WorkflowRun] = {}


def _save_to_disk():
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        serialized = [run.to_dict() for run in _workflow_runs.values()]
        with open(RUNS_FILE, "w", encoding="utf-8") as f:
            json.dump(serialized, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to persist workflow runs to disk: {e}")


def _load_from_disk():
    if not os.path.exists(RUNS_FILE):
        return
    try:
        with open(RUNS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    run = WorkflowRun.from_dict(item)
                    _workflow_runs[run.id] = run
    except Exception as e:
        print(f"Warning: Failed to load workflow runs from disk: {e}")


# Initialize persistent state on module load
_load_from_disk()


def save_run(run: WorkflowRun):
    _workflow_runs[run.id] = run
    _save_to_disk()


def get_run(run_id: str) -> WorkflowRun | None:
    return _workflow_runs.get(run_id)


def list_runs() -> list[WorkflowRun]:
    return list(_workflow_runs.values())


def clear_runs():
    _workflow_runs.clear()
    _save_to_disk()

