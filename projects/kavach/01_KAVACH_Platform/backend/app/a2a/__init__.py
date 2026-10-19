"""
Google Agent2Agent (A2A) Protocol implementation for KAVACH.
Complies with CSE3101 Agentic AI Module 5 (6 Sessions):
- Agent-to-Agent (A2A) Protocol: Communication, collaboration, and coordination among AI agents.
- Inter-agent messaging, capability discovery, task delegation, and multi-agent consensus attestation.
"""

from .protocol import (
    A2AMessage,
    A2AMessageType,
    A2ABus,
    A2APeerInfo,
    global_a2a_bus,
)

__all__ = [
    "A2AMessage",
    "A2AMessageType",
    "A2ABus",
    "A2APeerInfo",
    "global_a2a_bus",
]
