"""
Agent-to-Agent Communication module
Enables EduAgent to collaborate with other agents in the ASI ecosystem
"""
from typing import Optional, Dict, List, Callable
from pydantic import BaseModel, Field
from datetime import datetime
import json
from enum import Enum

class MessageType(str, Enum):
    """Types of agent-to-agent messages"""
    QUERY = "query"
    RESPONSE = "response"
    COLLABORATION = "collaboration"
    KNOWLEDGE_SHARE = "knowledge_share"
    RESOURCE_REQUEST = "resource_request"
    RESOURCE_PROVIDE = "resource_provide"
    STATUS = "status"

class AgentRequest(BaseModel):
    """Request from one agent to another"""
    request_id: str
    sender_agent: str
    receiver_agent: str
    message_type: MessageType
    content: Dict = Field(..., description="Request content")
    priority: str = Field(default="normal", description="Priority: low, normal, high")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    requires_response: bool = True

class AgentResponse(BaseModel):
    """Response from one agent to another"""
    response_id: str
    request_id: str
    sender_agent: str
    receiver_agent: str
    status: str = Field(..., description="Status: success, error, pending")
    content: Dict = Field(..., description="Response content")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class CollaborationRequest(BaseModel):
    """Request for collaboration between agents"""
    collaboration_id: str
    initiator_agent: str
    target_agents: List[str]
    task_description: str
    required_capabilities: List[str]
    deadline: Optional[str] = None
    metadata: Optional[Dict] = None

class KnowledgeShare(BaseModel):
    """Knowledge sharing between agents"""
    share_id: str
    source_agent: str
    target_agents: List[str]
    knowledge_type: str
    content: Dict
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class AgentCommunicationManager:
    """
    Manages communication between EduAgent and other agents
    """
    
    def __init__(self, agent_address: str):
        self.agent_address = agent_address
        self.pending_requests: Dict[str, AgentRequest] = {}
        self.completed_requests: List[Dict] = []
        self.active_collaborations: Dict[str, CollaborationRequest] = {}
        self.knowledge_base: List[KnowledgeShare] = []
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.connected_agents: Dict[str, Dict] = {}
    
    def register_message_handler(self, message_type: MessageType, handler: Callable):
        """Register a handler for a specific message type"""
        self.message_handlers[message_type] = handler
    
    def create_request(self,
                      receiver_agent: str,
                      message_type: MessageType,
                      content: Dict,
                      priority: str = "normal",
                      requires_response: bool = True) -> AgentRequest:
        """Create an agent-to-agent request"""
        import uuid
        request_id = str(uuid.uuid4())
        
        request = AgentRequest(
            request_id=request_id,
            sender_agent=self.agent_address,
            receiver_agent=receiver_agent,
            message_type=message_type,
            content=content,
            priority=priority,
            requires_response=requires_response
        )
        
        self.pending_requests[request_id] = request
        return request
    
    def create_response(self,
                       request: AgentRequest,
                       status: str,
                       content: Dict) -> AgentResponse:
        """Create a response to an agent request"""
        import uuid
        response_id = str(uuid.uuid4())
        
        response = AgentResponse(
            response_id=response_id,
            request_id=request.request_id,
            sender_agent=self.agent_address,
            receiver_agent=request.sender_agent,
            status=status,
            content=content
        )
        
        # Mark request as completed
        if request.request_id in self.pending_requests:
            del self.pending_requests[request.request_id]
            self.completed_requests.append({
                "request": request.dict(),
                "response": response.dict()
            })
        
        return response
    
    def initiate_collaboration(self,
                             target_agents: List[str],
                             task_description: str,
                             required_capabilities: List[str],
                             deadline: Optional[str] = None) -> CollaborationRequest:
        """Initiate a collaboration with other agents"""
        import uuid
        collaboration_id = str(uuid.uuid4())
        
        collaboration = CollaborationRequest(
            collaboration_id=collaboration_id,
            initiator_agent=self.agent_address,
            target_agents=target_agents,
            task_description=task_description,
            required_capabilities=required_capabilities,
            deadline=deadline
        )
        
        self.active_collaborations[collaboration_id] = collaboration
        return collaboration
    
    def share_knowledge(self,
                       target_agents: List[str],
                       knowledge_type: str,
                       content: Dict) -> KnowledgeShare:
        """Share knowledge with other agents"""
        import uuid
        share_id = str(uuid.uuid4())
        
        knowledge = KnowledgeShare(
            share_id=share_id,
            source_agent=self.agent_address,
            target_agents=target_agents,
            knowledge_type=knowledge_type,
            content=content
        )
        
        self.knowledge_base.append(knowledge)
        return knowledge
    
    def register_agent(self, agent_address: str, agent_info: Dict):
        """Register a connected agent"""
        self.connected_agents[agent_address] = {
            "address": agent_address,
            "info": agent_info,
            "registered_at": datetime.utcnow().isoformat(),
            "last_seen": datetime.utcnow().isoformat()
        }
    
    def get_connected_agents(self) -> List[Dict]:
        """Get list of connected agents"""
        return list(self.connected_agents.values())
    
    def find_agents_by_capability(self, capability: str) -> List[str]:
        """Find agents that have a specific capability"""
        matching_agents = []
        
        for agent_address, agent_data in self.connected_agents.items():
            capabilities = agent_data.get("info", {}).get("capabilities", [])
            if capability in capabilities:
                matching_agents.append(agent_address)
        
        return matching_agents
    
    def handle_incoming_request(self, request: AgentRequest) -> Optional[AgentResponse]:
        """Handle an incoming request from another agent"""
        handler = self.message_handlers.get(request.message_type)
        
        if handler:
            try:
                response_content = handler(request.content)
                return self.create_response(request, "success", response_content)
            except Exception as e:
                return self.create_response(
                    request,
                    "error",
                    {"error": str(e)}
                )
        else:
            return self.create_response(
                request,
                "error",
                {"error": f"No handler for message type: {request.message_type}"}
            )
    
    def get_collaboration_status(self, collaboration_id: str) -> Optional[Dict]:
        """Get status of an active collaboration"""
        collaboration = self.active_collaborations.get(collaboration_id)
        
        if not collaboration:
            return None
        
        return {
            "collaboration_id": collaboration.collaboration_id,
            "initiator": collaboration.initiator_agent,
            "target_agents": collaboration.target_agents,
            "task": collaboration.task_description,
            "status": "active",
            "created_at": collaboration.deadline
        }
    
    def get_communication_stats(self) -> Dict:
        """Get communication statistics"""
        return {
            "pending_requests": len(self.pending_requests),
            "completed_requests": len(self.completed_requests),
            "active_collaborations": len(self.active_collaborations),
            "connected_agents": len(self.connected_agents),
            "knowledge_shares": len(self.knowledge_base)
        }

class AgentDiscoveryService:
    """
    Service for discovering and registering agents in the ASI ecosystem
    """
    
    def __init__(self):
        self.registered_agents: Dict[str, Dict] = {}
        self.agent_registry: List[Dict] = []
    
    def register_agent(self, agent_address: str, agent_profile: Dict):
        """Register an agent in the discovery service"""
        self.registered_agents[agent_address] = {
            "address": agent_address,
            "profile": agent_profile,
            "registered_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
        self.agent_registry.append(self.registered_agents[agent_address])
    
    def discover_agents(self, 
                       capability: Optional[str] = None,
                       tag: Optional[str] = None) -> List[Dict]:
        """Discover agents by capability or tag"""
        results = []
        
        for agent_data in self.agent_registry:
            profile = agent_data.get("profile", {})
            
            if capability:
                if capability in profile.get("capabilities", []):
                    results.append(agent_data)
            
            elif tag:
                if tag in profile.get("tags", []):
                    results.append(agent_data)
            
            else:
                results.append(agent_data)
        
        return results
    
    def get_agent_profile(self, agent_address: str) -> Optional[Dict]:
        """Get profile of a specific agent"""
        agent_data = self.registered_agents.get(agent_address)
        return agent_data.get("profile") if agent_data else None
    
    def update_agent_status(self, agent_address: str, status: str):
        """Update agent status"""
        if agent_address in self.registered_agents:
            self.registered_agents[agent_address]["status"] = status
            self.registered_agents[agent_address]["last_updated"] = datetime.utcnow().isoformat()
