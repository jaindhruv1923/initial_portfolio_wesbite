"""
CrewAI Tasks Architecture for KAVACH.
Encapsulates task descriptions, expected outputs, assigned agents, and execution state.
"""

from typing import Dict, Any, List, Optional
from .agents import CrewAgent


class CrewTask:
    """Standard CrewAI Task representation."""
    def __init__(
        self,
        description: str,
        expected_output: str,
        agent: CrewAgent,
        context: Optional[List["CrewTask"]] = None,
    ):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.context = context or []
        self.output: Optional[Dict[str, Any]] = None

    def execute(self, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute task using the assigned agent."""
        desc = self.description
        if inputs:
            for k, v in inputs.items():
                desc = desc.replace(f"{{{k}}}", str(v))

        # Collect context outputs from preceding tasks
        ctx_data = {}
        for c in self.context:
            if c.output:
                ctx_data[c.agent.role] = c.output

        self.output = self.agent.execute_task(desc, ctx_data)
        return self.output

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "expected_output": self.expected_output,
            "assigned_agent": self.agent.role,
            "has_output": self.output is not None,
        }
