#!/usr/bin/env python3
"""
Research Team Orchestrator Client

A client that orchestrates multiple A2A agents to perform comprehensive research tasks.
Uses the official A2A SDK for agent communication.
"""

import asyncio
import logging
import httpx
from uuid import uuid4
from typing import Dict, List, Optional

from a2a.client import A2AClient, A2ACardResolver
from a2a.types import MessageSendParams, SendMessageRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ResearchTeamOrchestrator:
    """Orchestrates multiple A2A agents for comprehensive research tasks"""
    
    def __init__(self):
        self.agents = {
            "research": "http://localhost:9001",
            "analysis": "http://localhost:9002", 
            "factcheck": "http://localhost:9003",
            "qa": "http://localhost:9004"
        }
        self.clients: Dict[str, A2AClient] = {}
        self.agent_cards = {}
        
    async def initialize(self):
        """Initialize connections to all A2A agents"""
        logger.info("Initializing connections to A2A agents...")
        
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            for agent_name, base_url in self.agents.items():
                try:
                    # Resolve agent card
                    resolver = A2ACardResolver(http_client, base_url=base_url)
                    agent_card = await resolver.get_agent_card()
                    self.agent_cards[agent_name] = agent_card
                    
                    # Create client
                    client = A2AClient(http_client, agent_card)
                    self.clients[agent_name] = client
                    
                    logger.info(f"✅ Connected to {agent_name} agent: {agent_card.name}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to connect to {agent_name} agent at {base_url}: {e}")
                    
        logger.info(f"Successfully connected to {len(self.clients)} agents")
        
    async def send_message_to_agent(self, agent_name: str, message: str) -> Optional[str]:
        """Send a message to a specific agent and get the response"""
        if agent_name not in self.clients:
            logger.error(f"Agent {agent_name} not available")
            return None
            
        try:
            client = self.clients[agent_name]
            
            # Create message request
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(
                    message={
                        "role": "user",
                        "parts": [{"kind": "text", "text": message}],
                        "messageId": uuid4().hex,
                    }
                ),
            )
            
            logger.info(f"Sending message to {agent_name} agent...")
            response = await client.send_message(request)
            
            # Extract response text
            if response.result and response.result.message and response.result.message.parts:
                response_text = ""
                for part in response.result.message.parts:
                    if part.kind == "text":
                        response_text += part.text
                return response_text
            else:
                logger.warning(f"No response content from {agent_name} agent")
                return None
                
        except Exception as e:
            logger.error(f"Error communicating with {agent_name} agent: {e}")
            return None
    
    async def conduct_research(self, topic: str) -> Dict[str, str]:
        """Conduct comprehensive research using all available agents"""
        logger.info(f"Starting comprehensive research on: {topic}")
        
        results = {}
        
        # Step 1: Initial Research
        if "research" in self.clients:
            research_prompt = f"""Please conduct comprehensive research on the following topic: {topic}

Provide a thorough analysis covering:
1. Key concepts and definitions
2. Current state and recent developments
3. Important facts and statistics
4. Major players or stakeholders involved
5. Challenges and opportunities
6. Future outlook and trends

Please be comprehensive and well-structured in your response."""

            research_result = await self.send_message_to_agent("research", research_prompt)
            if research_result:
                results["research"] = research_result
                logger.info("✅ Research phase completed")
            else:
                logger.error("❌ Research phase failed")
        
        # Step 2: Analysis (if research was successful)
        if "analysis" in self.clients and "research" in results:
            analysis_prompt = f"""Please analyze the following research data about {topic}:

{results["research"]}

Provide a detailed analysis including:
1. Key insights and patterns
2. Critical success factors
3. Risk assessment
4. Strategic implications
5. Recommendations for action
6. Areas requiring further investigation

Focus on actionable insights and strategic implications."""

            analysis_result = await self.send_message_to_agent("analysis", analysis_prompt)
            if analysis_result:
                results["analysis"] = analysis_result
                logger.info("✅ Analysis phase completed")
            else:
                logger.error("❌ Analysis phase failed")
        
        # Step 3: Fact-checking (if research was successful)
        if "factcheck" in self.clients and "research" in results:
            factcheck_prompt = f"""Please fact-check the following research about {topic}:

{results["research"]}

Verify:
1. Factual accuracy of key claims
2. Consistency of information
3. Logical coherence
4. Potential misinformation or errors
5. Source credibility assessment
6. Areas needing verification

Provide a detailed fact-check report with specific findings."""

            factcheck_result = await self.send_message_to_agent("factcheck", factcheck_prompt)
            if factcheck_result:
                results["factcheck"] = factcheck_result
                logger.info("✅ Fact-check phase completed")
            else:
                logger.error("❌ Fact-check phase failed")
        
        # Step 4: Quality Assurance (if we have research and at least one other result)
        if "qa" in self.clients and len(results) >= 2:
            qa_prompt = f"""Please conduct quality assurance on this research project about {topic}.

Research Results:
{results.get("research", "Not available")}

Analysis Results:
{results.get("analysis", "Not available")}

Fact-check Results:
{results.get("factcheck", "Not available")}

Evaluate:
1. Overall research quality and completeness
2. Consistency across different phases
3. Gaps or weaknesses identified
4. Reliability and credibility assessment
5. Recommendations for improvement
6. Final quality rating and justification

Provide a comprehensive quality assessment report."""

            qa_result = await self.send_message_to_agent("qa", qa_prompt)
            if qa_result:
                results["qa"] = qa_result
                logger.info("✅ Quality assurance phase completed")
            else:
                logger.error("❌ Quality assurance phase failed")
        
        logger.info(f"Research orchestration completed. Generated {len(results)} reports.")
        return results
    
    def format_final_report(self, topic: str, results: Dict[str, str]) -> str:
        """Format the final comprehensive research report"""
        report = f"""
# Comprehensive Research Report: {topic}

Generated by Multi-Agent Research Team using A2A Protocol
Agents involved: {', '.join(results.keys())}

"""
        
        if "research" in results:
            report += f"""
## 📊 Research Findings
{results["research"]}

"""
        
        if "analysis" in results:
            report += f"""
## 🔍 Strategic Analysis
{results["analysis"]}

"""
        
        if "factcheck" in results:
            report += f"""
## ✅ Fact-Check Report
{results["factcheck"]}

"""
        
        if "qa" in results:
            report += f"""
## 🎯 Quality Assurance Assessment
{results["qa"]}

"""
        
        report += f"""
---
*Report generated using A2A (Agent-to-Agent) protocol with Strands Agents*
*Agents: Research Specialist, Analysis Specialist, Fact-Check Specialist, QA Specialist*
"""
        
        return report

async def main():
    """Main orchestrator function"""
    logger.info("Starting Research Team Orchestrator...")
    
    # Initialize orchestrator
    orchestrator = ResearchTeamOrchestrator()
    
    try:
        # Initialize connections
        await orchestrator.initialize()
        
        if not orchestrator.clients:
            logger.error("No agents available. Please start the agent servers first.")
            return
        
        # Example research topic
        topic = "The impact of artificial intelligence on modern software development practices"
        
        # Conduct research
        results = await orchestrator.conduct_research(topic)
        
        # Generate final report
        final_report = orchestrator.format_final_report(topic, results)
        
        # Save report
        with open("research_report.md", "w") as f:
            f.write(final_report)
        
        logger.info("✅ Research completed successfully!")
        logger.info("📄 Final report saved to: research_report.md")
        
        # Print summary
        print("\n" + "="*80)
        print("RESEARCH ORCHESTRATION SUMMARY")
        print("="*80)
        print(f"Topic: {topic}")
        print(f"Agents Used: {len(results)}")
        print(f"Reports Generated: {', '.join(results.keys())}")
        print(f"Final Report: research_report.md")
        print("="*80)
        
    except Exception as e:
        logger.error(f"Error in orchestration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
