#!/usr/bin/env python3
"""
Fact-Check Agent A2A Server

A specialized fact-checking agent that runs as an A2A server, providing
fact verification capabilities using web search via MCP.
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

def create_factcheck_agent():
    """Create and configure the fact-checking specialist agent"""
    
    # Use Bedrock Claude model for fact-checking tasks
    model = BedrockModel(
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=0.2,  # Lower temperature for more consistent fact-checking
        region="us-west-2"
    )
    
    # For now, create agent without MCP tools to ensure basic functionality
    # TODO: Add MCP tools once basic A2A communication is working
    tools = []
    
    # Create the fact-checking specialist agent
    agent = Agent(
        name="FactCheckSpecialist",
        description="A specialized fact-checking agent that verifies claims and information accuracy",
        model=model,
        system_prompt="""You are a Fact-Check Specialist agent with expertise in verifying information accuracy.

Your capabilities:
- Verify factual claims using your knowledge base
- Cross-reference information for consistency
- Identify potential misinformation or inaccuracies
- Assess information credibility and reliability
- Provide evidence-based fact verification

When fact-checking:
1. Identify specific claims that need verification
2. Analyze claims against your knowledge base
3. Cross-reference information for consistency
4. Assess the credibility and logical consistency of claims
5. Clearly indicate which claims are verified, disputed, or uncertain
6. Provide reasoning for all verification assessments
7. Flag any potential misinformation or questionable claims

Always prioritize accuracy and provide clear reasoning for your assessments.""",
        tools=tools
    )
    
    return agent

def main():
    """Main entry point for the fact-check agent server"""
    
    logger.info("Starting Fact-Check Agent A2A Server...")
    
    try:
        # Create the fact-check agent
        factcheck_agent = create_factcheck_agent()
        logger.info("✅ Fact-check agent created successfully")
        
        # Create A2A server using the actual available class
        a2a_server = A2AServer(
            agent=factcheck_agent,
            host="localhost",
            port=9003
        )
        
        logger.info("✅ A2AServer created successfully")
        logger.info(f"Fact-Check Agent server starting on http://localhost:9003")
        logger.info("Agent Card will be available at http://localhost:9003/.well-known/agent.json")
        
        # Start serving (this blocks)
        a2a_server.serve()
        
    except KeyboardInterrupt:
        logger.info("Fact-Check Agent server shutting down...")
    except Exception as e:
        logger.error(f"Error starting Fact-Check Agent server: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
