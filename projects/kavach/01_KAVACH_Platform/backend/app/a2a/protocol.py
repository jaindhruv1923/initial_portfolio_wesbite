"""
Google Agent-to-Agent (A2A) Protocol implementation for KAVACH.
Standardizes inter-agent communication, collaborative handshakes, and cryptographic message attestation.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Callable
import time
import uuid
import hashlib
import json


class A2AMessageType(str, Enum):
    DISCOVERY = "DISCOVERY"
    HANDSHAKE = "HANDSHAKE"
    TASK_DELEGATION = "TASK_DELEGATION"
    TASK_RESPONSE = "TASK_RESPONSE"
    STATUS_HEARTBEAT = "STATUS_HEARTBEAT"
    CONSENSUS_VOTE = "CONSENSUS_VOTE"
    RESULT_ATTESTATION = "RESULT_ATTESTATION"


class A2AMessage:
    """Standardized Agent-to-Agent (A2A) Protocol message envelope."""
    def __init__(
        self,
        sender_agent_id: str,
        receiver_agent_id: str,
        message_type: A2AMessageType,
        payload: Dict[str, Any],
        conversation_id: Optional[str] = None,
        message_id: Optional[str] = None,
        timestamp: Optional[float] = None,
    ):
        self.message_id = message_id or str(uuid.uuid4())
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.sender_agent_id = sender_agent_id
        self.receiver_agent_id = receiver_agent_id
        self.message_type = message_type
        self.payload = payload
        self.timestamp = timestamp or time.time()
        self.signature = self._generate_signature()

    def _generate_signature(self) -> str:
        """Generate SHA-256 integrity digest over the envelope."""
        serialized = f"{self.message_id}:{self.conversation_id}:{self.sender_agent_id}:{self.receiver_agent_id}:{self.message_type.value}:{json.dumps(self.payload, sort_keys=True)}"
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "sender_agent_id": self.sender_agent_id,
            "receiver_agent_id": self.receiver_agent_id,
            "message_type": self.message_type.value,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "A2AMessage":
        msg = cls(
            sender_agent_id=data["sender_agent_id"],
            receiver_agent_id=data["receiver_agent_id"],
            message_type=A2AMessageType(data["message_type"]),
            payload=data["payload"],
            conversation_id=data.get("conversation_id"),
            message_id=data.get("message_id"),
            timestamp=data.get("timestamp"),
        )
        msg.signature = data.get("signature", msg.signature)
        return msg


class A2APeerInfo:
    """Metadata describing a registered peer agent on the A2A network."""
    def __init__(self, agent_id: str, role: str, capabilities: List[str], endpoint: Optional[str] = None):
        self.agent_id = agent_id
        self.role = role
        self.capabilities = capabilities
        self.endpoint = endpoint
        self.last_heartbeat = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "capabilities": self.capabilities,
            "endpoint": self.endpoint,
            "last_heartbeat": self.last_heartbeat,
        }


class A2ABus:
    """
    Central event-driven A2A Router and Message Bus.
    Handles peer registration, capability discovery, asynchronous dispatch,
    and consensus aggregation.
    """
    def __init__(self):
        self.peers: Dict[str, A2APeerInfo] = {}
        self.message_history: List[A2AMessage] = []
        self.handlers: Dict[str, List[Callable[[A2AMessage], Optional[A2AMessage]]]] = {}

    def register_peer(self, agent_id: str, role: str, capabilities: List[str], endpoint: Optional[str] = None):
        """Register an agent as a discoverable peer on the A2A network."""
        peer = A2APeerInfo(agent_id, role, capabilities, endpoint)
        self.peers[agent_id] = peer

    def list_peers(self) -> List[Dict[str, Any]]:
        """Discover all active peer agents and their capabilities."""
        return [p.to_dict() for p in self.peers.values()]

    def subscribe(self, agent_id: str, handler: Callable[[A2AMessage], Optional[A2AMessage]]):
        """Subscribe an agent handler to incoming messages."""
        if agent_id not in self.handlers:
            self.handlers[agent_id] = []
        self.handlers[agent_id].append(handler)

    def dispatch(self, message: A2AMessage) -> List[A2AMessage]:
        """Dispatch message to target recipient agent(s)."""
        self.message_history.append(message)
        responses: List[A2AMessage] = []

        receiver_id = message.receiver_agent_id
        target_ids = list(self.handlers.keys()) if receiver_id == "*" else [receiver_id]

        for tid in target_ids:
            if tid in self.handlers:
                for handler in self.handlers[tid]:
                    try:
                        resp = handler(message)
                        if resp:
                            self.message_history.append(resp)
                            responses.append(resp)
                    except Exception:
                        pass
        return responses

    def conduct_consensus_vote(self, proposal: Dict[str, Any], eligible_agent_ids: List[str]) -> Dict[str, Any]:
        """
        Conduct a multi-agent consensus vote over a proposal (e.g. security policy or patch approval).
        """
        conv_id = str(uuid.uuid4())
        votes = {}

        for aid in eligible_agent_ids:
            vote_msg = A2AMessage(
                sender_agent_id="consensus_engine",
                receiver_agent_id=aid,
                message_type=A2AMessageType.CONSENSUS_VOTE,
                payload={"proposal": proposal},
                conversation_id=conv_id,
            )
            resps = self.dispatch(vote_msg)
            if resps:
                votes[aid] = resps[0].payload.get("vote", "REJECT")
            else:
                # Default approval if no veto registered
                votes[aid] = "APPROVE"

        approve_count = sum(1 for v in votes.values() if v == "APPROVE")
        consensus_reached = approve_count > len(eligible_agent_ids) / 2

        return {
            "conversation_id": conv_id,
            "proposal": proposal,
            "total_voters": len(eligible_agent_ids),
            "votes": votes,
            "consensus_reached": consensus_reached,
            "final_verdict": "APPROVED" if consensus_reached else "REJECTED",
        }


# Global A2A bus instance pre-populated with KAVACH's core security agent peers
global_a2a_bus = A2ABus()

# Register initial peer agents
global_a2a_bus.register_peer("sentinel_agent", "Security Gatekeeper", ["pii_detection", "secret_scanning", "injection_shield"])
global_a2a_bus.register_peer("retriever_agent", "Knowledge Archivist", ["qdrant_vector_search", "code_chunking"])
global_a2a_bus.register_peer("coder_agent", "DevOps Engineer", ["code_synthesis", "self_healing_reflection"])
global_a2a_bus.register_peer("auditor_agent", "Compliance Auditor", ["merkle_ledger_attestation", "cyclonedx_sbom"])
