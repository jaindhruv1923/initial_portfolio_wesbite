"""
Structured Output Engine using Pydantic for KAVACH.
Complies with Point 3 of Professor Pranshu Tiwari's Minimum Requirements:
"3. Structured Output using Pydantic - final output must be generated in a structured form (Markdown, Table, or JSON)."
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import time
import json
from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    MARKDOWN = "markdown"
    TABLE = "table"
    JSON = "json"


class AgentStepOutput(BaseModel):
    step_number: int
    agent_name: str
    framework: str = "Google ADK"  # 'Google ADK' or 'CrewAI'
    action_type: str
    output_summary: str
    duration_ms: float
    state_delta_keys: List[str] = Field(default_factory=list)


class GuardrailVerdict(BaseModel):
    is_safe: bool = True
    threat_category: str = "NONE"
    risk_score: float = 0.0
    action_taken: str = "ALLOW"
    redacted_items_count: int = 0
    cryptographic_seal: str = ""


class ExecutionMetrics(BaseModel):
    total_duration_ms: float
    tokens_consumed: int
    estimated_cost_usd: float
    estimated_cost_inr: float
    merkle_leaf_hash: str


class AgentStructuredReport(BaseModel):
    """
    Standardized Pydantic Output Model for all KAVACH & Bharat Bank multi-agent runs.
    Guarantees structured serialization into Markdown, Table, or JSON.
    """
    report_id: str
    task_goal: str
    execution_status: str  # 'SUCCESS', 'BLOCKED', 'REQUIRES_HITL'
    summary: str
    primary_agent: str
    collaborating_agents: List[str] = Field(default_factory=list)
    steps: List[AgentStepOutput] = Field(default_factory=list)
    security: GuardrailVerdict = Field(default_factory=GuardrailVerdict)
    metrics: ExecutionMetrics
    timestamp: float = Field(default_factory=time.time)

    def to_markdown(self) -> str:
        """Render formal GitHub-flavored markdown report."""
        md = []
        md.append(f"# KAVACH Multi-Agent Governance Report: `{self.report_id}`")
        md.append(f"**Task Goal:** {self.task_goal}  ")
        md.append(f"**Execution Status:** `{self.execution_status}` | **Primary Agent:** `{self.primary_agent}`  ")
        md.append(f"**Summary:** {self.summary}\n")

        md.append("## Security & Guardrails Verdict")
        sec_status = "SAFE" if self.security.is_safe else "FLAGGED / BLOCKED"
        md.append(f"- **Verdict:** `{sec_status}` ({self.security.action_taken})")
        md.append(f"- **Threat Category:** `{self.security.threat_category}` (Risk Score: `{self.security.risk_score}`)")
        md.append(f"- **Cryptographic Proof:** `{self.security.cryptographic_seal}`\n")

        md.append("## Multi-Agent Execution Steps (ADK & CrewAI)")
        md.append("| Step | Agent | Framework | Action | Output Summary | Latency (ms) |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for s in self.steps:
            md.append(f"| {s.step_number} | **{s.agent_name}** | {s.framework} | `{s.action_type}` | {s.output_summary} | {s.duration_ms}ms |")

        md.append("\n## Provenance & Cost Metrics")
        md.append(f"- **Total Latency:** `{self.metrics.total_duration_ms} ms`")
        md.append(f"- **Tokens Consumed:** `{self.metrics.tokens_consumed}` tokens")
        md.append(f"- **Estimated Cost:** `${self.metrics.estimated_cost_usd:.5f} USD` (`₹{self.metrics.estimated_cost_inr:.3f} INR`)")
        md.append(f"- **Merkle Anchor:** `{self.metrics.merkle_leaf_hash}`")
        return "\n".join(md)

    def to_table(self) -> List[Dict[str, Any]]:
        """Render tabular representation of execution steps and metrics."""
        table_rows = []
        for s in self.steps:
            table_rows.append({
                "Step": s.step_number,
                "Agent": s.agent_name,
                "Framework": s.framework,
                "Action": s.action_type,
                "Summary": s.output_summary,
                "Latency_ms": s.duration_ms,
                "Security_Risk": self.security.risk_score,
                "Status": self.execution_status
            })
        return table_rows

    def to_json_dict(self) -> Dict[str, Any]:
        """Render standard JSON dictionary."""
        return self.model_dump()

    def render(self, format_type: OutputFormat = OutputFormat.JSON) -> Any:
        """Universal rendering dispatcher."""
        if format_type == OutputFormat.MARKDOWN:
            return self.to_markdown()
        elif format_type == OutputFormat.TABLE:
            return self.to_table()
        else:
            return self.to_json_dict()
