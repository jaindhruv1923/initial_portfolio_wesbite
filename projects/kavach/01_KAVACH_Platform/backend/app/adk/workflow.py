"""
Google ADK Multi-Agent Workflow Graphs & Topologies.
Supports:
- Graph workflows (DAG execution)
- Dynamic workflows (conditional branching)
- Collaborative workflows (shared blackboard/state)
- Template-based workflows
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Callable
import time
from .agent import LlmAgent


class WorkflowExecutionMode(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    GRAPH_DAG = "GRAPH_DAG"
    COLLABORATIVE = "COLLABORATIVE"
    DYNAMIC = "DYNAMIC"


class WorkflowNode:
    """Node in an ADK Multi-Agent Workflow Graph."""
    def __init__(self, node_id: str, agent: LlmAgent, task_template: str):
        self.node_id = node_id
        self.agent = agent
        self.task_template = task_template
        self.dependencies: List[str] = []
        self.condition: Optional[Callable[[Dict[str, Any]], bool]] = None


class AgentWorkflowGraph:
    """
    DAG and Dynamic Multi-Agent Workflow Graph Engine.
    Executes agents respecting topological dependency order and conditional branch guards.
    """
    def __init__(self, name: str = "ADK_Master_Workflow"):
        self.name = name
        self.nodes: Dict[str, WorkflowNode] = {}
        self.execution_mode = WorkflowExecutionMode.GRAPH_DAG

    def add_node(
        self,
        node_id: str,
        agent: LlmAgent,
        task_template: str,
        dependencies: Optional[List[str]] = None,
        condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ):
        node = WorkflowNode(node_id, agent, task_template)
        if dependencies:
            node.dependencies = dependencies
        node.condition = condition
        self.nodes[node_id] = node

    def run(self, initial_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the workflow graph topologically."""
        start_time = time.time()
        shared_state = dict(initial_payload)
        executed_nodes = []
        node_outputs = {}

        # Simple topological level resolution
        pending = set(self.nodes.keys())
        while pending:
            progress = False
            for node_id in list(pending):
                node = self.nodes[node_id]
                # Check dependencies
                deps_met = all(dep in node_outputs for dep in node.dependencies)
                if deps_met:
                    # Check condition if dynamic
                    if node.condition is None or node.condition(shared_state):
                        task_text = node.task_template.format(**shared_state) if "{" in node.task_template else node.task_template
                        out = node.agent.execute(task_text, shared_state)
                        node_outputs[node_id] = out
                        shared_state[f"{node_id}_output"] = out
                        executed_nodes.append(node_id)
                    else:
                        node_outputs[node_id] = {"skipped": True, "reason": "Condition returned False"}
                        executed_nodes.append(f"{node_id} (SKIPPED)")
                    pending.remove(node_id)
                    progress = True
            if not progress and pending:
                # Break circular or unresolvable dependencies
                for node_id in list(pending):
                    node_outputs[node_id] = {"error": "Dependency resolution deadlock"}
                    pending.remove(node_id)

        duration_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "workflow_name": self.name,
            "execution_mode": self.execution_mode.value,
            "executed_sequence": executed_nodes,
            "node_outputs": node_outputs,
            "duration_ms": duration_ms,
        }
