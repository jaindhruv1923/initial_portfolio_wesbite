"""
Google ADK (Agent Development Kit) implementation for KAVACH.
Complies with CSE3101 Agentic AI Module 4:
- Agent (LlmAgent) class, lifecycle, and capabilities
- Tool context, built-in tools, and custom tool development
- State, sessions, and memory (transient vs persistent)
- Coordinator agents, sub-agents, task delegation
- Multi-agent workflows (graph, dynamic, collaborative, template)
- 8-Hook-Point Callbacks architecture (3 phases: Agent, Model, Tool)
- 8 Canonical Callback Design Patterns (Guardrails, State, Logging, Caching, Modification, Skipping, Tool Actions, Artifacts)
- Medical Triage Multi-Agent Pipeline reference implementation
"""

from .agent import LlmAgent, AgentLifecycleState
from .coordinator import CoordinatorAgent
from .callbacks import (
    AgentCallbacks,
    ToolCallback,
    ModelCallback,
    CallbackContext,
    ToolContext,
    LlmRequest,
    LlmResponse,
    CallbackActions,
)
from .memory import AgentMemory, TransientMemory, PersistentSessionMemory
from .workflow import AgentWorkflowGraph, WorkflowExecutionMode
from .medical_triage import MedicalTriagePipeline, get_canonical_quiz_scenarios

__all__ = [
    "LlmAgent",
    "AgentLifecycleState",
    "CoordinatorAgent",
    "AgentCallbacks",
    "ToolCallback",
    "ModelCallback",
    "CallbackContext",
    "ToolContext",
    "LlmRequest",
    "LlmResponse",
    "CallbackActions",
    "AgentMemory",
    "TransientMemory",
    "PersistentSessionMemory",
    "AgentWorkflowGraph",
    "WorkflowExecutionMode",
    "MedicalTriagePipeline",
    "get_canonical_quiz_scenarios",
]
