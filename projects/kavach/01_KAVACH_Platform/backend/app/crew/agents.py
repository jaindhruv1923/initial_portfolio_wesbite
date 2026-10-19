"""
CrewAI Agents Architecture for KAVACH.
Standardizes roles, goals, backstories, tools, and memory for multi-agent collaboration.
"""

from typing import Dict, Any, List, Optional, Callable
import time


class CrewAgent:
    """Standard CrewAI Agent representation."""
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: Optional[List[Callable]] = None,
        verbose: bool = True,
        allow_delegation: bool = True,
        memory: bool = True,
    ):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.verbose = verbose
        self.allow_delegation = allow_delegation
        self.memory = memory
        self.memory_buffer: List[Dict[str, Any]] = []

    def execute_task(self, task_description: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a task assigned to this agent persona."""
        start_time = time.time()
        tool_results = []

        # Execute registered tools
        for tool in self.tools:
            try:
                res = tool(task_description)
                tool_results.append({"tool": getattr(tool, "__name__", "tool"), "result": res})
            except Exception as e:
                tool_results.append({"tool": getattr(tool, "__name__", "tool"), "error": str(e)})

        thought_trace = f"[{self.role}] executed task: '{task_description[:60]}...' with {len(tool_results)} tool actions."
        duration_ms = round((time.time() - start_time) * 1000, 2)

        output = {
            "agent_role": self.role,
            "goal": self.goal,
            "task": task_description,
            "trace": thought_trace,
            "tool_results": tool_results,
            "duration_ms": duration_ms,
        }
        if self.memory:
            self.memory_buffer.append(output)
        return output

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "tools_count": len(self.tools),
            "allow_delegation": self.allow_delegation,
            "memory": self.memory,
            "memory_items": len(self.memory_buffer),
        }


def create_sentinel_agent() -> CrewAgent:
    from app.security.detector import detect_pii
    from app.security.secret_detector import detect_secrets
    from app.security.injection_shield import inspect_prompt_safety

    return CrewAgent(
        role="Principal Security Auditor",
        goal="Audit all developer prompts, code patches, and retrieved evidence for PII, API tokens, and prompt injection attacks.",
        backstory="Veteran cybersecurity auditor dedicated to zero-trust enforcement and DPDP Act 2023 compliance.",
        tools=[detect_pii, detect_secrets, inspect_prompt_safety],
        allow_delegation=False,
    )


def create_retriever_agent() -> CrewAgent:
    from app.rag.embed_store import search

    def _rag_tool(query: str):
        return search(query, top_k=3)

    return CrewAgent(
        role="Repository Knowledge Archivist",
        goal="Retrieve semantic context, symbol definitions, and relevant code chunks from Qdrant vector database.",
        backstory="Deep codebase indexing specialist ensuring all agent reasoning is grounded in factual repository context.",
        tools=[_rag_tool],
        allow_delegation=False,
    )


def create_blast_radius_agent() -> CrewAgent:
    from app.impact.analyzer import analyze_impact
    import os

    def _ast_tool(desc: str):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return analyze_impact(desc, repo_root, top_k=5)

    return CrewAgent(
        role="Software Architect & Dependency Analyst",
        goal="Traverse AST symbol trees to compute blast radius, reachability graphs, and downstream regression risks.",
        backstory="Systems architect safeguarding service boundaries and maintaining low regression blast radius.",
        tools=[_ast_tool],
        allow_delegation=False,
    )


def create_coder_agent() -> CrewAgent:
    from app.generation.generator import generate_code
    from app.agent.self_healer import autonomous_self_heal

    def _coder_tool(prompt: str):
        return generate_code(prompt, [])

    return CrewAgent(
        role="Principal Software Engineer",
        goal="Synthesize clean, idiomatic, syntactically verified Python patches and repair broken unit tests via closed-loop reflection.",
        backstory="Staff engineer with a passion for test-driven development, type safety, and self-healing resilience.",
        tools=[_coder_tool],
        allow_delegation=False,
    )


def create_supervisor_agent() -> CrewAgent:
    return CrewAgent(
        role="Engineering Lead & Release Gatekeeper",
        goal="Coordinate execution across Sentinel, Retriever, Blast-Radius, and Coder agents to ensure secure, high-confidence delivery.",
        backstory="Engineering director responsible for overall pipeline governance, approval gates, and deployment safety.",
        allow_delegation=True,
    )
