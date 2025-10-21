"""
Configuration module for EduAgent
Handles environment variables and agent settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Agent Configuration
AGENT_NAME = "EduAgent"
AGENT_SEED = os.getenv("AGENT_SEED", "edu_agent_seed_phrase_12345")
AGENT_PORT = int(os.getenv("AGENT_PORT", 8000))
AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT", "http://localhost:8000/submit")

# Agentverse Configuration
AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY", "")
AGENTVERSE_URL = "https://agentverse.ai"

# External APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
RAPID_API_KEY = os.getenv("RAPID_API_KEY", "")

# Blockchain Configuration (Optional)
WEB3_PROVIDER = os.getenv("WEB3_PROVIDER", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
