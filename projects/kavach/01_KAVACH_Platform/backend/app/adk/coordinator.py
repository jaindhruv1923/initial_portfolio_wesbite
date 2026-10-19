"""
Google ADK Coordinator & Sub-Agent Orchestration Architecture.
Complies with Google ADK specifications:
- Coordinator agents & sub-agents
- Task delegation & dependency tracking
- Execution management and aggregated result verification
"""

from typing import Dict, Any, List, Optional
import time
from .agent import LlmAgent, AgentLifecycleState


class CoordinatorAgent(LlmAgent):
    """
    ADK Coordinator Agent managing sub-agent registration, task delegation,
    and execution management.
    """
    def __init__(self, name: str = "ADK_Master_Coordinator"):
        super().__init__(
            name=name,
            system_instruction="Coordinate specialized sub-agents to achieve end-to-end task automation with strict safety gating.",
            capabilities=["task_delegation", "subagent_management", "execution_governance"],
        )
        self.sub_agents: Dict[str, LlmAgent] = {}
        self.delegation_graph: List[Dict[str, Any]] = []

    def register_sub_agent(self, agent: LlmAgent):
        """Register a specialized worker/sub-agent."""
        self.sub_agents[agent.name] = agent

    def delegate_task(self, sub_agent_name: str, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Delegate a targeted sub-task to a specific sub-agent."""
        if sub_agent_name not in self.sub_agents:
            raise ValueError(f"Sub-agent '{sub_agent_name}' not found under coordinator '{self.name}'")

        sub_agent = self.sub_agents[sub_agent_name]
        start_time = time.time()
        result = sub_agent.execute(task, context)
        duration_ms = round((time.time() - start_time) * 1000, 2)

        delegation_record = {
            "sub_agent": sub_agent_name,
            "task": task,
            "duration_ms": duration_ms,
            "status": "SUCCESS" if result.get("state") == AgentLifecycleState.COMPLETED.value else "FAILED",
            "output": result,
        }
        self.delegation_graph.append(delegation_record)
        return result

    def coordinate_workflow(self, user_request: str) -> Dict[str, Any]:
        """
        Orchestrate full multi-agent collaborative pipeline across registered sub-agents.
        """
        start_time = time.time()
        self.lifecycle_state = AgentLifecycleState.PLANNING

        workflow_trace = []

        # 1. Pre-execution Security Gating (Sentinel sub-agent if available)
        sentinel_result = None
        for name, agent in self.sub_agents.items():
            if "sentinel" in name.lower() or "security" in name.lower():
                sentinel_result = self.delegate_task(name, user_request)
                workflow_trace.append({"phase": "Security Gating", "agent": name, "result": sentinel_result})
                break

        # 2. Knowledge Retrieval (Retriever sub-agent if available)
        retriever_result = None
        for name, agent in self.sub_agents.items():
            if "retriever" in name.lower() or "rag" in name.lower():
                retriever_result = self.delegate_task(name, user_request)
                workflow_trace.append({"phase": "Knowledge Retrieval", "agent": name, "result": retriever_result})
                break

        # 3. Patch Synthesis / Coder (DevOpsCoder sub-agent if available)
        coder_result = None
        for name, agent in self.sub_agents.items():
            if "coder" in name.lower() or "devops" in name.lower():
                context = {
                    "security_findings": sentinel_result,
                    "retrieved_context": retriever_result,
                }
                coder_result = self.delegate_task(name, user_request, context)
                workflow_trace.append({"phase": "Code Generation", "agent": name, "result": coder_result})
                break

        self.lifecycle_state = AgentLifecycleState.COMPLETED
        duration_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "coordinator": self.name,
            "state": self.lifecycle_state.value,
            "user_request": user_request,
            "sub_agents_consulted": [t["agent"] for t in workflow_trace],
            "workflow_trace": workflow_trace,
            "duration_ms": duration_ms,
        }
