"""
Google ADK State, Sessions, and Memory Architecture.
Handles transient vs. persistent memory mechanisms and session management.
"""

from typing import Dict, Any, List, Optional
import time
import json


class TransientMemory:
    """Transient scratchpad memory cleared across discrete execution sessions."""
    def __init__(self):
        self.scratchpad: Dict[str, Any] = {}
        self.intermediate_thoughts: List[str] = []
        self.tool_outputs: List[Dict[str, Any]] = []

    def set(self, key: str, value: Any):
        self.scratchpad[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.scratchpad.get(key, default)

    def add_thought(self, thought: str):
        self.intermediate_thoughts.append(thought)

    def record_tool_output(self, tool_name: str, output: Any):
        self.tool_outputs.append({
            "tool": tool_name,
            "output": output,
            "timestamp": time.time(),
        })

    def clear(self):
        self.scratchpad.clear()
        self.intermediate_thoughts.clear()
        self.tool_outputs.clear()


class PersistentSessionMemory:
    """Persistent session memory retaining long-term interaction history and state."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Dict[str, Any]] = []
        self.context_store: Dict[str, Any] = {}

    def append_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        self.history.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": time.time(),
        })

    def store_context(self, key: str, value: Any):
        self.context_store[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        return self.context_store.get(key, default)

    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.history[-limit:]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "history_count": len(self.history),
            "context_keys": list(self.context_store.keys()),
        }


class AgentMemory:
    """Unified ADK Agent Memory combining transient scratchpad with persistent sessions."""
    def __init__(self, session_id: str = "default_session"):
        self.transient = TransientMemory()
        self.persistent = PersistentSessionMemory(session_id)

    def reset_transient(self):
        self.transient.clear()
