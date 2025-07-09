#!/usr/bin/env python3
"""
Quality Assurance Agent A2A Server

A specialized QA agent that runs as an A2A server, providing
quality assessment and validation capabilities.
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

def create_qa_agent():
    """Create and configure the quality assurance specialist agent"""
    
    # Use Bedrock Claude model for QA tasks
    model = BedrockModel(
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=0.2,  # Lower temperature for more consistent QA assessments
        region="us-west-2"
    )
    
    # Create the QA specialist agent (no external tools needed)
    agent = Agent(
        name="QualityAssuranceSpecialist",
        description="A specialized quality assurance agent that evaluates research quality and completeness",
        model=model,
        system_prompt="""You are a Quality Assurance Specialist agent with expertise in evaluating research quality.

Your capabilities:
- Assess research completeness and thoroughness
- Evaluate information quality and reliability
- Identify gaps or weaknesses in research
- Provide recommendations for improvement
- Ensure research meets high standards

When conducting quality assurance:
1. Evaluate the completeness of research coverage
2. Assess the quality and credibility of sources used
3. Check for logical consistency and coherence
4. Identify any gaps, biases, or weaknesses
5. Verify that conclusions are well-supported by evidence
6. Provide specific recommendations for improvement
7. Rate overall research quality with clear justification

Quality Assessment Criteria:
- Comprehensiveness: Does the research cover all relevant aspects?
- Source Quality: Are sources credible, recent, and authoritative?
- Accuracy: Is the information factually correct?
- Balance: Are multiple perspectives considered?
- Clarity: Is the information well-organized and clearly presented?
- Evidence: Are conclusions properly supported by evidence?

Always provide constructive feedback with specific, actionable recommendations.""",
        tools=[]  # QA agent doesn't need external tools
    )
    
    return agent

def main():
    """Main entry point for the QA agent server"""
    
    logger.info("Starting Quality Assurance Agent A2A Server...")
    
    try:
        # Create the QA agent
        qa_agent = create_qa_agent()
        logger.info("✅ QA agent created successfully")
        
        # Create A2A server using the actual available class
        a2a_server = A2AServer(
            agent=qa_agent,
            host="localhost",
            port=9004
        )
        
        logger.info("✅ A2AServer created successfully")
        logger.info(f"QA Agent server starting on http://localhost:9004")
        logger.info("Agent Card will be available at http://localhost:9004/.well-known/agent.json")
        
        # Start serving (this blocks)
        a2a_server.serve()
        
    except KeyboardInterrupt:
        logger.info("QA Agent server shutting down...")
    except Exception as e:
        logger.error(f"Error starting QA Agent server: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
