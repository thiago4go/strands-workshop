# analysis_agent.py

from strands import Agent
from strands.multiagent import a2a
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
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

# Setup the MCP client for the Sequential Thinking tool.
# This allows the agent to use the tool to perform sequential thinking.
# The MCP client is initialized with a lambda function that starts the
# MCP server in a Docker container.
sequential_thinking_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="docker",
        args=["run", "-i", "--rm", "mcp/sequentialthinking"]
    )
))

# Create the analysis agent. This agent is responsible for analyzing
# research data and providing insights.
analysis_agent = Agent(
    name="AnalysisSpecialist",
    model=model,
    system_prompt="""You are a specialized Analysis Agent.
    Your expertise is to analyze research data using a sequential thinking approach.
    You will be given research findings and you need to return a detailed analysis with insights and patterns.""",
    tools=sequential_thinking_client.list_tools_sync()
)

if __name__ == "__main__":
    # Start the A2A listener for the analysis agent.
    # This makes the agent available for other agents to communicate with.
    a2a.listen(agent=analysis_agent)