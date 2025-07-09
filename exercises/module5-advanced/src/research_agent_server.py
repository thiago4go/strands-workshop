#!/usr/bin/env python3
"""
Research Agent A2A Server

A specialized research agent that runs as an A2A server, providing
web research capabilities using the actual A2AServer implementation.
"""

import os
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

def create_research_agent():
    """Create and configure the research specialist agent"""
    
    # Use Bedrock Claude model for research tasks
    # AWS credentials should be configured via aws configure or environment variables
    model = BedrockModel(
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=0.3,
        region="us-west-2"  # Specify region explicitly
    )
    
    # Create the research specialist agent
    agent = Agent(
        name="ResearchSpecialist",
        description="A specialized research agent that performs comprehensive web research and analysis",
        model=model,
        system_prompt="""You are a Research Specialist agent with expertise in conducting thorough research and analysis.

Your capabilities:
- Analyze and research topics comprehensively
- Provide well-structured information with clear reasoning
- Focus on accuracy, relevance, and completeness
- Break down complex topics into understandable components

When conducting research:
1. Break down the topic into key components
2. Provide comprehensive analysis based on your knowledge
3. Organize information logically and clearly
4. Highlight key insights and important details
5. Provide actionable recommendations when appropriate

Always strive for thorough, well-reasoned research that provides valuable insights and practical value."""
    )
    
    return agent

def main():
    """Main entry point for the research agent server"""
    
    logger.info("Starting Research Agent A2A Server...")
    
    try:
        # Create the research agent
        research_agent = create_research_agent()
        logger.info("✅ Research agent created successfully")
        
        # Create A2A server using the actual available class
        a2a_server = A2AServer(
            agent=research_agent,
            host="localhost",
            port=9001
        )
        
        logger.info("✅ A2AServer created successfully")
        logger.info(f"Research Agent server starting on http://localhost:9001")
        logger.info("Agent Card will be available at http://localhost:9001/.well-known/agent.json")
        
        # Start serving (this blocks)
        a2a_server.serve()
        
    except KeyboardInterrupt:
        logger.info("Research Agent server shutting down...")
    except Exception as e:
        logger.error(f"Error starting Research Agent server: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
