# EduAgent Setup Guide

## Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/yourusername/edu-agent.git
cd edu-agent
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Environment Variables
\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### 5. Run the Agent
\`\`\`bash
python edu_agent.py
\`\`\`

You should see output like:
\`\`\`
INFO: [EduAgent]: Registration on Almanac API successful
INFO: [EduAgent]: Agent Address: agent1q...
INFO: [EduAgent]: Ready to help students learn!
\`\`\`

## Testing the Agent

### Using Python Client
\`\`\`python
from uagents import Agent
from models import QuestionRequest, ConceptType

# Create a test agent
test_agent = Agent(name="test_student")

@test_agent.on_interval(period=2.0)
async def ask_question(ctx):
    question = QuestionRequest(
        question="What is the derivative of x^2?",
        concept_type=ConceptType.MATHEMATICS,
        difficulty_level="intermediate",
        student_id="student_001"
    )
    await ctx.send("agent1q...", question)  # Replace with EduAgent address

test_agent.run()
\`\`\`

## Next Steps
- Deploy to Agentverse
- Integrate Chat Protocol
- Add external API integrations
- Implement blockchain progress tracking
