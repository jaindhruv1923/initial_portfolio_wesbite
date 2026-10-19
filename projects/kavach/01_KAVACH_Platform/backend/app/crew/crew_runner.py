"""
Crew Runner Architecture for KAVACH.
Supports Sequential and Hierarchical Crew orchestration processes.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
import time
from .agents import CrewAgent
from .tasks import CrewTask


class ProcessType(str, Enum):
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"


class Crew:
    """Standard CrewAI Crew execution coordinator."""
    def __init__(
        self,
        agents: List[CrewAgent],
        tasks: List[CrewTask],
        process: ProcessType = ProcessType.SEQUENTIAL,
        manager_agent: Optional[CrewAgent] = None,
        verbose: bool = True,
    ):
        self.agents = agents
        self.tasks = tasks
        self.process = process
        self.manager_agent = manager_agent
        self.verbose = verbose
        self.history: List[Dict[str, Any]] = []

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute all tasks in the Crew according to the defined process."""
        start_time = time.time()
        task_outputs = []

        for task in self.tasks:
            out = task.execute(inputs)
            task_outputs.append(out)

        duration_ms = round((time.time() - start_time) * 1000, 2)
        summary = {
            "crew_process": self.process.value,
            "agent_count": len(self.agents),
            "task_count": len(self.tasks),
            "task_outputs": task_outputs,
            "duration_ms": duration_ms,
        }
        self.history.append(summary)
        return summary
