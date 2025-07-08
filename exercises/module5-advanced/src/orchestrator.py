# orchestrator.py

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

# Create the Orchestrator Agent. This agent is responsible for coordinating
# the other specialist agents to conduct comprehensive research.
orchestrator = Agent(
    name="ResearchOrchestrator",
    model=model,
    system_prompt="""You are a Research Orchestrator managing a team of specialist agents.
    You have access to these specialist agents:
    - ResearchSpecialist: Performs web research using DuckDuckGo search
    - AnalysisSpecialist: Analyzes research data using sequential thinking
    - FactCheckSpecialist: Fact-checks claims using DuckDuckGo search
    - QualityAssuranceSpecialist: Assesses research quality and completeness

    Your coordination strategy:
    1. For any research request, use ResearchSpecialist to gather information.
    2. Use AnalysisSpecialist to process and synthesize the research data.
    3. For complex topics, use FactCheckSpecialist to verify key claims.
    4. Use QualityAssuranceSpecialist to ensure research meets high standards.
    5. Coordinate intelligently based on the complexity and requirements.

    You will communicate with these agents using the A2A protocol. When you need a specialist agent to perform a task, you will call its `run` method with the appropriate input.
    """
)

if __name__ == "__main__":
    # Start the A2A listener for the orchestrator agent.
    # This makes the agent available for other agents to communicate with.
    a2a.listen(agent=orchestrator)