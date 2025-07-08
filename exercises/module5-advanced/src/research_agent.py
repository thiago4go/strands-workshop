# research_agent.py

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

# Setup the MCP client for the DuckDuckGo search tool.
# This allows the agent to use the search tool to perform web searches.
# The MCP client is initialized with a lambda function that starts the
# MCP server in a Docker container.
duckduckgo_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="docker",
        args=["run", "-i", "--rm", "mcp/duckduckgo"]
    )
))

# Create the research agent. This agent is responsible for performing
# web research on a given topic.
research_agent = Agent(
    name="ResearchSpecialist",
    model=model,
    system_prompt="""You are a specialized Research Agent.
    Your expertise is to perform web research using the DuckDuckGo search tool.
    You will be given a topic and you need to return a comprehensive research finding with source attribution.""",
    tools=duckduckgo_client.list_tools_sync()
)

if __name__ == "__main__":
    # Start the A2A listener for the research agent.
    # This makes the agent available for other agents to communicate with.
    a2a.listen(agent=research_agent)