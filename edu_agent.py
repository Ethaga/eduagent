"""
Main EduAgent implementation
Autonomous educational tutor agent using uAgents framework
"""
import asyncio
import os
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from typing import Optional
from config import AGENT_NAME, AGENT_SEED, AGENT_PORT, AGENT_ENDPOINT
from models import QuestionRequest, ExplanationResponse, ConceptType, StudentProgress
from reasoning_engine import ReasoningEngine
from api_integrations import EducationalResourceAggregator
from chat_protocol import ChatProtocolHandler, ChatMessage
from agent_communication import (
    AgentCommunicationManager,
    AgentDiscoveryService,
    MessageType,
    AgentRequest,
    AgentResponse
)
from blockchain_integration import (
    BlockchainProgressTracker,
    ProgressRecord,
    AchievementSystem
)

load_dotenv()
AGENT_ADDRESS = os.getenv("AGENT_ADDRESS", "agent1qvuswp05mg6ahxjsn0r3lghmpkmsdj4l3kx90xm0d9lr2jpztaxtuy93h0s")

# Initialize the agent
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
    endpoint=[AGENT_ENDPOINT]
)

# Initialize all components
reasoning_engine = ReasoningEngine()
resource_aggregator = EducationalResourceAggregator()
chat_handler = None
comm_manager = None
discovery_service = AgentDiscoveryService()
blockchain_tracker = BlockchainProgressTracker()
achievement_system = AchievementSystem()

# Storage for student progress
student_progress = {}

@agent.on_event("startup")
async def startup(ctx: Context):
    """Agent startup handler"""
    global chat_handler, comm_manager
    
    chat_handler = ChatProtocolHandler(agent.address, AGENT_NAME)
    comm_manager = AgentCommunicationManager(agent.address)
    
    # Register message handlers for agent communication
    comm_manager.register_message_handler(
        MessageType.QUERY,
        handle_agent_query
    )
    comm_manager.register_message_handler(
        MessageType.RESOURCE_REQUEST,
        handle_resource_request
    )
    comm_manager.register_message_handler(
        MessageType.KNOWLEDGE_SHARE,
        handle_knowledge_share
    )
    
    # Register this agent in discovery service
    discovery_service.register_agent(
        agent.address,
        chat_handler.profile.dict()
    )
    
    ctx.logger.info(f"EduAgent initialized successfully!")
    ctx.logger.info(f"Agent Address: {agent.address}")
    ctx.logger.info(f"Chat Protocol enabled for ASI:One")
    ctx.logger.info(f"Agent-to-Agent Communication enabled")
    ctx.logger.info(f"Blockchain Progress Tracking enabled")
    ctx.logger.info(f"Ready to help students learn and collaborate with other agents!")

@agent.on_message(model=QuestionRequest)
async def handle_question(ctx: Context, sender: str, msg: QuestionRequest):
    """Handle incoming questions from students"""
    ctx.logger.info(f"Received question from {sender}: {msg.question}")
    
    if chat_handler:
        session = chat_handler.create_session(sender)
        chat_handler.add_message_to_session(
            session.session_id,
            sender,
            msg.question,
            "question"
        )
    
    try:
        explanation = reasoning_engine.generate_explanation(
            question=msg.question,
            concept_type=msg.concept_type,
            difficulty_level=msg.difficulty_level
        )
        
        try:
            resources = await resource_aggregator.get_comprehensive_learning_resources(
                concept=msg.question[:50],
                difficulty=msg.difficulty_level
            )
            
            if resources.get("wikipedia_summary"):
                explanation.explanation += f"\n\nAdditional Context:\n{resources['wikipedia_summary']}"
            
            if resources.get("practice_problems"):
                explanation.practice_problems = [
                    p.get("question", "") for p in resources["practice_problems"][:3]
                ]
            
            ctx.logger.info(f"Enhanced explanation with external resources")
        
        except Exception as e:
            ctx.logger.warning(f"Could not fetch external resources: {str(e)}")
        
        if msg.student_id:
            if msg.student_id not in student_progress:
                student_progress[msg.student_id] = {
                    "questions_asked": 0,
                    "concepts_learned": []
                }
            
            student_progress[msg.student_id]["questions_asked"] += 1
            if msg.concept_type.value not in student_progress[msg.student_id]["concepts_learned"]:
                student_progress[msg.student_id]["concepts_learned"].append(msg.concept_type.value)
            
            # Record progress on blockchain
            progress_record = ProgressRecord(
                student_id=msg.student_id,
                concepts_learned=student_progress[msg.student_id]["concepts_learned"],
                questions_answered=student_progress[msg.student_id]["questions_asked"],
                difficulty_level=msg.difficulty_level,
                score=min(100.0, student_progress[msg.student_id]["questions_asked"] * 10)
            )
            
            blockchain_result = blockchain_tracker.record_progress(progress_record)
            
            # Check for achievements
            unlocked_achievements = achievement_system.check_achievements(
                msg.student_id,
                student_progress[msg.student_id]
            )
            
            if unlocked_achievements:
                ctx.logger.info(f"Unlocked achievements for {msg.student_id}: {unlocked_achievements}")
                explanation.explanation += f"\n\n🎉 Achievements Unlocked: {', '.join(unlocked_achievements)}"
            
            ctx.logger.info(f"Updated progress for student {msg.student_id}")
            ctx.logger.info(f"Blockchain record: {blockchain_result}")
        
        await ctx.send(sender, explanation)
        
        if chat_handler:
            chat_handler.add_message_to_session(
                session.session_id,
                agent.address,
                explanation.explanation,
                "response"
            )
        
        ctx.logger.info(f"Sent explanation to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error processing question: {str(e)}")
        error_response = ExplanationResponse(
            question=msg.question,
            explanation=f"I encountered an error processing your question: {str(e)}",
            key_points=["Please try rephrasing your question"],
            examples=[],
            difficulty_level=msg.difficulty_level,
            concept_type=msg.concept_type.value
        )
        await ctx.send(sender, error_response)

@agent.on_message(model=AgentRequest)
async def handle_agent_communication(ctx: Context, sender: str, msg: AgentRequest):
    """Handle agent-to-agent communication"""
    ctx.logger.info(f"Received agent request from {sender}: {msg.message_type}")
    
    if comm_manager:
        response = comm_manager.handle_incoming_request(msg)
        if response:
            await ctx.send(sender, response)
            ctx.logger.info(f"Sent response to {sender}")

def handle_agent_query(content: dict) -> dict:
    """Handle query requests from other agents"""
    query = content.get("query", "")
    concept_type = content.get("concept_type", "mathematics")
    
    explanation = reasoning_engine.generate_explanation(
        question=query,
        concept_type=ConceptType(concept_type),
        difficulty_level="intermediate"
    )
    
    return {
        "status": "success",
        "explanation": explanation.explanation,
        "key_points": explanation.key_points,
        "examples": explanation.examples
    }

def handle_resource_request(content: dict) -> dict:
    """Handle resource requests from other agents"""
    resource_type = content.get("resource_type", "practice_problems")
    topic = content.get("topic", "")
    
    return {
        "status": "success",
        "resource_type": resource_type,
        "topic": topic,
        "resources": [
            "Resource 1: Practice Problem Set",
            "Resource 2: Concept Explanation",
            "Resource 3: Code Examples"
        ]
    }

def handle_knowledge_share(content: dict) -> dict:
    """Handle knowledge sharing from other agents"""
    knowledge_type = content.get("knowledge_type", "")
    knowledge_content = content.get("content", {})
    
    return {
        "status": "success",
        "message": f"Knowledge of type '{knowledge_type}' received and integrated"
    }

@agent.on_interval(period=60.0)
async def periodic_check(ctx: Context):
    """Periodic health check"""
    active_sessions = chat_handler.get_active_sessions_count() if chat_handler else 0
    comm_stats = comm_manager.get_communication_stats() if comm_manager else {}
    
    ctx.logger.info(f"EduAgent Status - Students: {len(student_progress)}, Sessions: {active_sessions}, Comm Stats: {comm_stats}")

if __name__ == "__main__":
    agent.run()
