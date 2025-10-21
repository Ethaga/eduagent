"""
Flask web server for EduAgent demonstration
Provides a simple interface to interact with the agent
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
import json
from typing import Optional
from models import QuestionRequest, ConceptType

app = Flask(__name__)
CORS(app)

# Global reference to agent (will be set when agent starts)
agent_instance = None
agent_address = None

def set_agent_instance(agent, address):
    """Set the agent instance for web server to use"""
    global agent_instance, agent_address
    agent_instance = agent
    agent_address = address

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/agent/info', methods=['GET'])
def get_agent_info():
    """Get information about the agent"""
    if not agent_instance:
        return jsonify({"error": "Agent not initialized"}), 500
    
    return jsonify({
        "name": agent_instance.name,
        "address": agent_address,
        "status": "active",
        "capabilities": [
            "answer_questions",
            "explain_concepts",
            "provide_practice_problems",
            "track_student_progress"
        ]
    })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Submit a question to the agent"""
    data = request.json
    
    if not data or 'question' not in data:
        return jsonify({"error": "Question is required"}), 400
    
    question = data.get('question')
    concept_type = data.get('concept_type', 'mathematics')
    difficulty_level = data.get('difficulty_level', 'intermediate')
    student_id = data.get('student_id')
    
    try:
        # Create question request
        question_req = QuestionRequest(
            question=question,
            concept_type=ConceptType(concept_type),
            difficulty_level=difficulty_level,
            student_id=student_id
        )
        
        return jsonify({
            "status": "success",
            "message": "Question submitted to agent",
            "question": question,
            "request_id": student_id or "anonymous"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/concepts', methods=['GET'])
def get_concepts():
    """Get available concept types"""
    return jsonify({
        "concepts": [
            {"value": "mathematics", "label": "Mathematics"},
            {"value": "programming", "label": "Programming"},
            {"value": "algorithm", "label": "Algorithm"},
            {"value": "data_structure", "label": "Data Structure"}
        ]
    })

@app.route('/api/difficulty-levels', methods=['GET'])
def get_difficulty_levels():
    """Get available difficulty levels"""
    return jsonify({
        "levels": [
            {"value": "beginner", "label": "Beginner"},
            {"value": "intermediate", "label": "Intermediate"},
            {"value": "advanced", "label": "Advanced"}
        ]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agent_running": agent_instance is not None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
