"""
Data models for EduAgent using Pydantic
Defines request/response structures for agent communication
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class ConceptType(str, Enum):
    """Types of educational concepts"""
    MATHEMATICS = "mathematics"
    PROGRAMMING = "programming"
    ALGORITHM = "algorithm"
    DATA_STRUCTURE = "data_structure"

class QuestionRequest(BaseModel):
    """Model for incoming question requests"""
    question: str = Field(..., description="The student's question")
    concept_type: ConceptType = Field(default=ConceptType.MATHEMATICS, description="Type of concept")
    difficulty_level: str = Field(default="intermediate", description="Difficulty: beginner, intermediate, advanced")
    student_id: Optional[str] = Field(None, description="Optional student identifier for progress tracking")
    context: Optional[str] = Field(None, description="Additional context about the question")

class ExplanationResponse(BaseModel):
    """Model for agent's explanation response"""
    question: str
    explanation: str = Field(..., description="Clear explanation of the concept")
    key_points: List[str] = Field(..., description="Key takeaways")
    examples: List[str] = Field(..., description="Practical examples")
    practice_problems: Optional[List[str]] = Field(None, description="Suggested practice problems")
    difficulty_level: str
    concept_type: str

class StudentProgress(BaseModel):
    """Model for tracking student progress"""
    student_id: str
    concepts_learned: List[str] = Field(default_factory=list)
    questions_asked: int = Field(default=0)
    last_interaction: Optional[str] = None
    blockchain_hash: Optional[str] = Field(None, description="Hash of progress record on blockchain")

class AgentMessage(BaseModel):
    """Model for agent-to-agent communication"""
    sender_agent: str
    receiver_agent: str
    message_type: str
    content: dict
    timestamp: Optional[str] = None

class ChatProtocolMessage(BaseModel):
    """Model for Chat Protocol messages"""
    session_id: str
    sender: str
    receiver: str
    content: str
    message_type: str = "text"
    timestamp: Optional[str] = None

class ChatSessionInfo(BaseModel):
    """Model for chat session information"""
    session_id: str
    user_address: str
    agent_address: str
    message_count: int
    is_active: bool
    created_at: str
    last_activity: str
