#!/usr/bin/env python3
"""
Analysis Agent A2A Server

A specialized analysis agent that runs as an A2A server, providing
data analysis capabilities using sequential thinking via MCP.
"""

import logging
from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands.models import BedrockModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_analysis_agent():
    """Create and configure the analysis specialist agent"""
    
    # Use Bedrock Claude model for analysis tasks
    model = BedrockModel(
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=0.3,
        region="us-west-2"
    )
    
    # For now, create agent without MCP tools to ensure basic functionality
    # TODO: Add MCP tools once basic A2A communication is working
    tools = []
    
    # Create the analysis specialist agent
    agent = Agent(
        name="AnalysisSpecialist",
        description="A specialized analysis agent that performs deep data analysis and synthesis",
        model=model,
        system_prompt="""You are an Analysis Specialist agent with expertise in data analysis and synthesis.

Your capabilities:
- Analyze complex research data and information
- Use systematic thinking to break down complex problems
- Identify patterns, trends, and key insights
- Synthesize information from multiple sources
- Provide structured, logical analysis

When analyzing data:
1. Approach complex analysis systematically
2. Break down information into logical components
3. Identify relationships and patterns between data points
4. Draw meaningful conclusions based on evidence
5. Present analysis in a clear, structured format
6. Highlight key insights and actionable findings

Always provide thorough, evidence-based analysis with clear reasoning.""",
        tools=tools
    )
    
    return agent

def main():
    """Main entry point for the analysis agent server"""
    
    logger.info("Starting Analysis Agent A2A Server...")
    
    try:
        # Create the analysis agent
        analysis_agent = create_analysis_agent()
        logger.info("✅ Analysis agent created successfully")
        
        # Create A2A server using the actual available class
        a2a_server = A2AServer(
            agent=analysis_agent,
            host="localhost",
            port=9002
        )
        
        logger.info("✅ A2AServer created successfully")
        logger.info(f"Analysis Agent server starting on http://localhost:9002")
        logger.info("Agent Card will be available at http://localhost:9002/.well-known/agent.json")
        
        # Start serving (this blocks)
        a2a_server.serve()
        
    except KeyboardInterrupt:
        logger.info("Analysis Agent server shutting down...")
    except Exception as e:
        logger.error(f"Error starting Analysis Agent server: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
