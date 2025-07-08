# qa_agent.py

from strands import Agent
from strands.multiagent import a2a
from strands.models import BedrockModel
import logging

# Configure logging for production monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# It is recommended to use a single model instance for all agents
# to reduce memory usage and improve performance.
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

# Create the QA agent. This agent is responsible for assessing the
# quality and completeness of the research.
qa_agent = Agent(
    name="QualityAssuranceSpecialist",
    model=model,
    system_prompt="""You are a specialized Quality Assurance Agent.
    Your expertise is to assess research quality and completeness.
    You will be given a complete research summary and you need to return a quality assessment with scores and recommendations."""
)

if __name__ == "__main__":
    # Start the A2A listener for the QA agent.
    # This makes the agent available for other agents to communicate with.
    a2a.listen(agent=qa_agent)