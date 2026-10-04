"""
Workflow state machine (Phase 2 — see docs/AGENT_SPEC.md).

Defines the stages a developer request moves through, and a simple in-memory
store for workflow runs. This will move to the real database (see
docs/DATABASE_SPEC.md) once Phase 1's DB layer is wired in — kept in-memory
for now so Phase 2 can be built and tested independently.
"""

import uuid
from dataclasses import dataclass, field
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
    history: list[str] = field(default_factory=list)  # human-readable stage log

    def advance(self, new_stage: WorkflowStage, note: str = ""):
        self.history.append(f"{self.stage} -> {new_stage}" + (f" ({note})" if note else ""))
        self.stage = new_stage


# In-memory store — fine for local dev/demo; replace with the real DB (audit_log,
# workflow_runs tables from DATABASE_SPEC.md) before this needs to survive a restart.
_workflow_runs: dict[str, WorkflowRun] = {}


def save_run(run: WorkflowRun):
    _workflow_runs[run.id] = run


def get_run(run_id: str) -> WorkflowRun | None:
    return _workflow_runs.get(run_id)


def list_runs() -> list[WorkflowRun]:
    return list(_workflow_runs.values())
