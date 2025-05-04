# agent_protocol.py

from datetime import datetime
from typing import Dict, List, Literal
from pydantic.v1 import Field, UUID4
import uuid

from uagents import Protocol
from uagents_core.models import Model
from uagents_core.protocol import ProtocolSpecification

# --- Metadata Content
class MetadataContent(Model):
    type: Literal["metadata"] = "metadata"
    metadata: Dict[str, str]

# --- AgentMessage (only contains metadata content)
class AgentMessage(Model):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    msg_id: UUID4 = Field(default_factory=uuid.uuid4)
    content: List[MetadataContent]

# --- AgentAcknowledgement
class AgentAcknowledgement(Model):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    acknowledged_msg_id: UUID4
    metadata: Dict[str, str] | None = None

# --- Protocol Specification
agent_protocol_spec = ProtocolSpecification(
    name="AgentProtocol22",
    version="1.0.0",
    interactions={
        AgentMessage: {AgentAcknowledgement},
        AgentAcknowledgement: set()
    },
)

# --- Create the protocol
agent_proto = Protocol(spec=agent_protocol_spec)

# --- Helper to create metadata messages
def create_metadata_message(metadata: Dict[str, str]) -> AgentMessage:
    return AgentMessage(content=[MetadataContent(metadata=metadata)])
