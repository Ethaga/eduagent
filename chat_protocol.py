"""
Chat Protocol implementation for ASI:One integration
Enables EduAgent to be discoverable and accessible through ASI:One interface
"""
from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime
import json

class ChatMessage(BaseModel):
    """Model for chat protocol messages"""
    sender: str = Field(..., description="Address of the sender")
    receiver: str = Field(..., description="Address of the receiver")
    message_id: str = Field(..., description="Unique message identifier")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    message_type: str = Field(default="text", description="Type of message")
    metadata: Optional[Dict] = Field(None, description="Additional metadata")

class ChatSession(BaseModel):
    """Model for managing chat sessions"""
    session_id: str
    user_address: str
    agent_address: str
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_activity: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    is_active: bool = True

class AgentProfile(BaseModel):
    """Agent profile for ASI:One discovery"""
    agent_address: str
    agent_name: str = "EduAgent"
    description: str = "An autonomous educational tutor agent"
    capabilities: List[str] = Field(default_factory=list)
    supported_protocols: List[str] = Field(default_factory=list)
    version: str = "1.0.0"
    author: str = "ASI Alliance"
    tags: List[str] = Field(default_factory=list)

class ChatProtocolHandler:
    """
    Handles Chat Protocol implementation for ASI:One compatibility
    """
    
    def __init__(self, agent_address: str, agent_name: str = "EduAgent"):
        self.agent_address = agent_address
        self.agent_name = agent_name
        self.sessions: Dict[str, ChatSession] = {}
        self.message_history: List[ChatMessage] = []
        
        # Initialize agent profile
        self.profile = self._create_agent_profile()
    
    def _create_agent_profile(self) -> AgentProfile:
        """Create agent profile for ASI:One discovery"""
        return AgentProfile(
            agent_address=self.agent_address,
            agent_name=self.agent_name,
            description="An autonomous educational tutor agent that helps students understand mathematical and programming concepts through natural language interaction.",
            capabilities=[
                "answer_questions",
                "explain_concepts",
                "provide_practice_problems",
                "track_student_progress",
                "suggest_learning_resources",
                "agent_collaboration"
            ],
            supported_protocols=[
                "chat_protocol",
                "uagent_communication",
                "asi_one_compatible"
            ],
            tags=[
                "education",
                "tutoring",
                "mathematics",
                "programming",
                "learning",
                "asi_compatible"
            ]
        )
    
    def create_session(self, user_address: str) -> ChatSession:
        """Create a new chat session"""
        import uuid
        session_id = str(uuid.uuid4())
        
        session = ChatSession(
            session_id=session_id,
            user_address=user_address,
            agent_address=self.agent_address
        )
        
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retrieve an existing session"""
        return self.sessions.get(session_id)
    
    def add_message_to_session(self, 
                              session_id: str,
                              sender: str,
                              content: str,
                              message_type: str = "text") -> Optional[ChatMessage]:
        """Add a message to a chat session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        import uuid
        message = ChatMessage(
            sender=sender,
            receiver=self.agent_address if sender != self.agent_address else session.user_address,
            message_id=str(uuid.uuid4()),
            content=content,
            message_type=message_type
        )
        
        session.messages.append(message)
        session.last_activity = datetime.utcnow().isoformat()
        self.message_history.append(message)
        
        return message
    
    def get_session_history(self, session_id: str) -> List[ChatMessage]:
        """Get message history for a session"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.messages
    
    def format_for_asi_one(self, message: ChatMessage) -> Dict:
        """Format message for ASI:One interface"""
        return {
            "id": message.message_id,
            "sender": message.sender,
            "receiver": message.receiver,
            "content": message.content,
            "timestamp": message.timestamp,
            "type": message.message_type,
            "metadata": message.metadata or {}
        }
    
    def get_agent_info_for_discovery(self) -> Dict:
        """Get agent information for ASI:One discovery"""
        return {
            "agent": self.profile.dict(),
            "endpoints": {
                "chat": f"agent://{self.agent_address}/chat",
                "query": f"agent://{self.agent_address}/query",
                "status": f"agent://{self.agent_address}/status"
            },
            "registration_status": "active",
            "last_heartbeat": datetime.utcnow().isoformat()
        }
    
    def close_session(self, session_id: str) -> bool:
        """Close a chat session"""
        session = self.get_session(session_id)
        if session:
            session.is_active = False
            return True
        return False
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        return sum(1 for session in self.sessions.values() if session.is_active)
    
    def get_session_summary(self, session_id: str) -> Optional[Dict]:
        """Get a summary of a chat session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session.session_id,
            "user_address": session.user_address,
            "agent_address": session.agent_address,
            "message_count": len(session.messages),
            "created_at": session.created_at,
            "last_activity": session.last_activity,
            "is_active": session.is_active,
            "duration_seconds": self._calculate_session_duration(session)
        }
    
    def _calculate_session_duration(self, session: ChatSession) -> float:
        """Calculate session duration in seconds"""
        from datetime import datetime
        created = datetime.fromisoformat(session.created_at)
        last_activity = datetime.fromisoformat(session.last_activity)
        duration = (last_activity - created).total_seconds()
        return duration
