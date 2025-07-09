#!/usr/bin/env python3
"""
Test Individual Agents

Test each agent server individually to ensure they work before testing A2A communication.
"""

import asyncio
import logging
import httpx
from uuid import uuid4

from a2a.client import A2AClient, A2ACardResolver
from a2a.types import MessageSendParams, SendMessageRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def test_agent(agent_name: str, base_url: str, test_message: str):
    """Test a single agent"""
    logger.info(f"Testing {agent_name} agent at {base_url}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as http_client:
            # Test agent card endpoint
            logger.info(f"Checking agent card for {agent_name}...")
            resolver = A2ACardResolver(http_client, base_url=base_url)
            agent_card = await resolver.get_agent_card()
            logger.info(f"✅ Agent card retrieved: {agent_card.name} - {agent_card.description}")
            
            # Create client and test message
            logger.info(f"Testing message communication with {agent_name}...")
            client = A2AClient(http_client, agent_card)
            
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(
                    message={
                        "role": "user",
                        "parts": [{"kind": "text", "text": test_message}],
                        "messageId": uuid4().hex,
                    }
                ),
            )
            
            response = await client.send_message(request)
            
            if response.result and response.result.message and response.result.message.parts:
                response_text = ""
                for part in response.result.message.parts:
                    if part.kind == "text":
                        response_text += part.text
                
                logger.info(f"✅ {agent_name} agent responded successfully")
                logger.info(f"Response preview: {response_text[:200]}...")
                return True
            else:
                logger.error(f"❌ {agent_name} agent returned empty response")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error testing {agent_name} agent: {e}")
        return False

async def main():
    """Test all agents individually"""
    logger.info("Starting individual agent tests...")
    
    agents_to_test = [
        ("Research", "http://localhost:9001", "What are the key benefits of cloud computing?"),
        ("Analysis", "http://localhost:9002", "Analyze the following data: Cloud adoption has increased 300% in the last 5 years. What does this mean?"),
        ("Fact-Check", "http://localhost:9003", "Please fact-check this claim: Python is the most popular programming language in 2024."),
        ("QA", "http://localhost:9004", "Evaluate the quality of this research: 'AI will replace all jobs by 2030.' Is this well-researched?")
    ]
    
    results = {}
    
    for agent_name, base_url, test_message in agents_to_test:
        logger.info(f"\n{'='*60}")
        logger.info(f"TESTING {agent_name.upper()} AGENT")
        logger.info(f"{'='*60}")
        
        success = await test_agent(agent_name, base_url, test_message)
        results[agent_name] = success
        
        if success:
            logger.info(f"✅ {agent_name} agent test PASSED")
        else:
            logger.error(f"❌ {agent_name} agent test FAILED")
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for agent_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{agent_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} agents working")
    
    if passed == total:
        logger.info("🎉 All agents are working! You can now test the orchestrator.")
    else:
        logger.warning("⚠️  Some agents are not working. Check the server logs and fix issues before testing orchestrator.")

if __name__ == "__main__":
    asyncio.run(main())
