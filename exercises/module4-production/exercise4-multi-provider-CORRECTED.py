# Exercise 4: Multi-Provider Production Setup (CORRECTED VERSION)
# Module 4 - Production

"""
Learning Objectives:
1. Configure multiple LLM providers using correct Strands SDK patterns
2. Implement provider fallback strategies with proper error handling
3. Understand cost optimization across different providers
4. Practice production-ready deployment patterns

This exercise demonstrates the CORRECT way to integrate multiple providers:
- AWS Bedrock (using BedrockModel)
- OpenAI (using OpenAIModel from strands.models.openai)
- NVIDIA NIM (using LiteLLMModel)
- OpenRouter (using LiteLLMModel)

Based on official Strands documentation: https://strandsagents.com/
"""

import os
import logging
from typing import Optional, List, Dict, Any
from strands import Agent
from strands.models import BedrockModel
from strands.models.openai import OpenAIModel
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator, current_time, http_request

# Configure logging for production monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CorrectedMultiProviderFactory:
    """
    Production-ready multi-provider factory using correct Strands SDK patterns.
    Based on official documentation from strandsagents.com
    """
    
    def __init__(self):
        self.provider_configs = self._setup_correct_configurations()
        self.usage_stats = {
            "requests_by_provider": {},
            "failures_by_provider": {},
            "total_requests": 0
        }
    
    def _setup_correct_configurations(self) -> List[Dict[str, Any]]:
        """
        Configure providers using the CORRECT Strands SDK patterns.
        """
        return [
            {
                "name": "AWS Bedrock (Claude 3.7 Sonnet)",
                "provider_id": "bedrock",
                "create_agent": self._create_bedrock_agent,
                "requirements": ["AWS credentials configured"],
                "cost_tier": "premium",
                "installation": "pip install strands-agents  # Bedrock included by default"
            },
            {
                "name": "OpenAI (GPT-4)",
                "provider_id": "openai", 
                "create_agent": self._create_openai_agent,
                "requirements": ["OPENAI_API_KEY environment variable"],
                "cost_tier": "premium",
                "installation": "pip install 'strands-agents[openai]'"
            },
            {
                "name": "NVIDIA NIM (Llama 3)",
                "provider_id": "nvidia",
                "create_agent": self._create_nvidia_agent,
                "requirements": ["NVIDIA_API_KEY environment variable"],
                "cost_tier": "free",
                "installation": "pip install 'strands-agents[litellm]'"
            },
            {
                "name": "OpenRouter (Mistral)",
                "provider_id": "openrouter",
                "create_agent": self._create_openrouter_agent,
                "requirements": ["OPENROUTER_API_KEY environment variable"],
                "cost_tier": "free",
                "installation": "pip install 'strands-agents[litellm]'"
            }
        ]
    
    def _create_bedrock_agent(self, config: Dict[str, Any]) -> Optional[Agent]:
        """Create AWS Bedrock agent using BedrockModel."""
        try:
            model = BedrockModel(
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                region_name='us-east-1',
                temperature=0.3,
                max_tokens=2000
            )
            
            return Agent(
                model=model,
                tools=[calculator, current_time, http_request],
                system_prompt="You are a helpful assistant powered by AWS Bedrock Claude 3.7 Sonnet."
            )
        except Exception as e:
            logger.warning(f"Failed to create Bedrock agent: {e}")
            return None
    
    def _create_openai_agent(self, config: Dict[str, Any]) -> Optional[Agent]:
        """Create OpenAI agent using the CORRECT OpenAIModel class."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
            return None
        
        try:
            # CORRECT: Use OpenAIModel from strands.models.openai
            model = OpenAIModel(
                client_args={
                    "api_key": api_key,
                },
                model_id="gpt-4o",  # Default model from documentation
                params={
                    "max_tokens": 2000,
                    "temperature": 0.3,
                }
            )
            
            return Agent(
                model=model,
                tools=[calculator, current_time, http_request],
                system_prompt="You are a helpful assistant powered by OpenAI GPT-4."
            )
        except Exception as e:
            logger.warning(f"Failed to create OpenAI agent: {e}")
            return None
    
    def _create_nvidia_agent(self, config: Dict[str, Any]) -> Optional[Agent]:
        """Create NVIDIA NIM agent using LiteLLMModel."""
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            logger.warning("NVIDIA_API_KEY not found in environment variables")
            return None
        
        try:
            # CORRECT: Use LiteLLMModel for NVIDIA NIM
            model = LiteLLMModel(
                client_args={
                    "api_key": api_key,
                },
                model_id="nvidia/meta/llama3-8b-instruct",
                params={
                    "max_tokens": 2000,
                    "temperature": 0.3,
                }
            )
            
            return Agent(
                model=model,
                tools=[calculator, current_time, http_request],
                system_prompt="You are a helpful assistant powered by NVIDIA NIM Llama 3."
            )
        except Exception as e:
            logger.warning(f"Failed to create NVIDIA agent: {e}")
            return None
    
    def _create_openrouter_agent(self, config: Dict[str, Any]) -> Optional[Agent]:
        """Create OpenRouter agent using LiteLLMModel."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            logger.warning("OPENROUTER_API_KEY not found in environment variables")
            return None
        
        try:
            # CORRECT: Use LiteLLMModel for OpenRouter
            model = LiteLLMModel(
                client_args={
                    "api_key": api_key,
                },
                model_id="openrouter/mistralai/mistral-small-latest:free",
                params={
                    "max_tokens": 2000,
                    "temperature": 0.3,
                }
            )
            
            return Agent(
                model=model,
                tools=[calculator, current_time, http_request],
                system_prompt="You are a helpful assistant powered by OpenRouter Mistral."
            )
        except Exception as e:
            logger.warning(f"Failed to create OpenRouter agent: {e}")
            return None
    
    def create_resilient_agent(self) -> Optional[Agent]:
        """
        Create an agent with automatic fallback across all available providers.
        Uses the first successfully created agent from the provider hierarchy.
        """
        logger.info("🔄 Creating resilient multi-provider agent...")
        
        for config in self.provider_configs:
            provider_name = config["name"]
            logger.info(f"Trying provider: {provider_name}")
            
            # Check requirements
            missing_requirements = self._check_requirements(config)
            if missing_requirements:
                logger.warning(f"❌ {provider_name}: Missing requirements: {missing_requirements}")
                continue
            
            # Attempt to create agent
            try:
                agent = config["create_agent"](config)
                if agent:
                    logger.info(f"✅ Successfully created agent with {provider_name}")
                    self._update_usage_stats(config["provider_id"], success=True)
                    return agent
                else:
                    logger.warning(f"❌ {provider_name}: Agent creation returned None")
                    
            except Exception as e:
                logger.error(f"❌ {provider_name}: Exception during creation: {e}")
                self._update_usage_stats(config["provider_id"], success=False)
                continue
        
        logger.error("🚨 All providers failed! No agent could be created.")
        return None
    
    def _check_requirements(self, config: Dict[str, Any]) -> List[str]:
        """Check if provider requirements are met."""
        missing = []
        
        for requirement in config["requirements"]:
            if "environment variable" in requirement:
                env_var = requirement.split()[0]
                if not os.getenv(env_var):
                    missing.append(requirement)
            elif "AWS credentials" in requirement:
                # Basic check for AWS credentials
                if not (os.getenv("AWS_ACCESS_KEY_ID") or os.path.exists(os.path.expanduser("~/.aws/credentials"))):
                    missing.append(requirement)
        
        return missing
    
    def _update_usage_stats(self, provider_id: str, success: bool):
        """Update usage statistics for monitoring."""
        self.usage_stats["total_requests"] += 1
        
        if provider_id not in self.usage_stats["requests_by_provider"]:
            self.usage_stats["requests_by_provider"][provider_id] = 0
            self.usage_stats["failures_by_provider"][provider_id] = 0
        
        self.usage_stats["requests_by_provider"][provider_id] += 1
        if not success:
            self.usage_stats["failures_by_provider"][provider_id] += 1
    
    def get_installation_guide(self) -> str:
        """Get installation instructions for all providers."""
        guide = "🔧 INSTALLATION GUIDE FOR ALL PROVIDERS\n"
        guide += "=" * 50 + "\n\n"
        
        for config in self.provider_configs:
            guide += f"📦 {config['name']}\n"
            guide += f"   Installation: {config['installation']}\n"
            guide += f"   Requirements: {', '.join(config['requirements'])}\n"
            guide += f"   Cost Tier: {config['cost_tier']}\n\n"
        
        return guide

def demonstrate_corrected_implementation():
    """
    Demonstrate the CORRECTED multi-provider implementation.
    """
    print("🚀 CORRECTED Multi-Provider Strands Agent Demo")
    print("=" * 60)
    print("Based on official Strands SDK documentation")
    print("https://strandsagents.com/")
    print("=" * 60)
    
    # Create the factory
    factory = CorrectedMultiProviderFactory()
    
    # Show installation guide
    print(factory.get_installation_guide())
    
    # Create resilient agent
    print("🔧 Creating Resilient Agent with Correct Patterns")
    print("-" * 50)
    agent = factory.create_resilient_agent()
    
    if not agent:
        print("❌ Failed to create any agent. Please check setup:")
        print("\n1. AWS Bedrock: Configure AWS credentials")
        print("   aws configure")
        print("\n2. OpenAI: Install and set API key")
        print("   pip install 'strands-agents[openai]'")
        print("   export OPENAI_API_KEY='sk-...'")
        print("\n3. NVIDIA NIM: Install and set API key")
        print("   pip install 'strands-agents[litellm]'")
        print("   export NVIDIA_API_KEY='nvapi-...'")
        print("\n4. OpenRouter: Install and set API key")
        print("   pip install 'strands-agents[litellm]'")
        print("   export OPENROUTER_API_KEY='sk-or-...'")
        return
    
    # Test the agent
    test_queries = [
        "What is 15 * 23?",
        "What time is it right now?",
        "Explain the key benefits of using multiple AI model providers"
    ]
    
    print("\n🧪 Testing Agent with Correct Implementation")
    print("-" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        try:
            response = agent(query)
            print(f"✅ Response: {response[:150]}..." if len(response) > 150 else f"✅ Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Show statistics
    print(f"\n📈 Usage Statistics")
    print("-" * 30)
    stats = factory.usage_stats
    print(f"Total requests: {stats['total_requests']}")
    for provider_id, count in stats['requests_by_provider'].items():
        failures = stats['failures_by_provider'].get(provider_id, 0)
        success_rate = ((count - failures) / count * 100) if count > 0 else 0
        print(f"{provider_id}: {count} requests, {success_rate:.1f}% success rate")

if __name__ == "__main__":
    demonstrate_corrected_implementation()
    
    print("\n" + "=" * 60)
    print("🎓 KEY CORRECTIONS MADE")
    print("=" * 60)
    print("""
1. ✅ CORRECT OpenAI Integration:
   - Use: from strands.models.openai import OpenAIModel
   - Install: pip install 'strands-agents[openai]'
   - Configure: OpenAIModel(client_args={"api_key": "..."}, model_id="gpt-4o")

2. ✅ CORRECT LiteLLM Integration:
   - Use: from strands.models.litellm import LiteLLMModel
   - Install: pip install 'strands-agents[litellm]'
   - For: NVIDIA NIM and OpenRouter providers

3. ✅ CORRECT Bedrock Integration:
   - Use: from strands.models import BedrockModel
   - Included by default in strands-agents
   - Configure: BedrockModel(model_id="...", region_name="...")

4. ✅ CORRECT Installation Commands:
   - Base: pip install strands-agents
   - OpenAI: pip install 'strands-agents[openai]'
   - LiteLLM: pip install 'strands-agents[litellm]'

5. ✅ CORRECT Model IDs:
   - OpenAI: "gpt-4o" (default from docs)
   - NVIDIA: "nvidia/meta/llama3-8b-instruct"
   - OpenRouter: "openrouter/mistralai/mistral-small-latest:free"
   - Bedrock: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    """)
