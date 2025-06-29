# Exercise 4: Multi-Provider Production Setup
# Module 4 - Production

"""
Learning Objectives:
1. Configure multiple LLM providers for production resilience
2. Implement provider fallback strategies
3. Understand cost optimization across providers
4. Practice production-ready error handling

This exercise demonstrates how to build resilient agents that can:
- Switch between multiple providers seamlessly
- Handle provider failures gracefully
- Optimize costs by using appropriate models for different tasks
- Maintain consistent performance across providers

Supported Providers:
1. AWS Bedrock (Claude 3.7 Sonnet) - Default, enterprise-grade
2. NVIDIA NIM (Llama 3) - GPU-accelerated, high performance
3. OpenRouter (Multiple models) - Cost-effective gateway
4. OpenAI (GPT-4, GPT-4 Turbo) - Industry standard, reliable
"""

import os
import logging
from typing import Optional, List, Dict, Any
from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, current_time, http_request

# Configure logging for production monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiProviderAgentFactory:
    """
    Production-ready agent factory with multiple provider support and fallback strategies.
    """
    
    def __init__(self):
        self.provider_configs = self._setup_provider_configurations()
        self.usage_stats = {
            "requests_by_provider": {},
            "failures_by_provider": {},
            "total_requests": 0
        }
    
    def _setup_provider_configurations(self) -> List[Dict[str, Any]]:
        """
        Configure all available providers with their specific settings.
        Providers are ordered by preference (primary to fallback).
        """
        return [
            {
                "name": "AWS Bedrock (Claude 3.7 Sonnet)",
                "provider_id": "bedrock",
                "model_id": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                "create_agent": self._create_bedrock_agent,
                "requirements": ["AWS credentials configured"],
                "cost_tier": "premium",
                "use_cases": ["complex reasoning", "production workloads"]
            },
            {
                "name": "OpenAI (GPT-4 Turbo)",
                "provider_id": "openai",
                "model_id": "gpt-4-turbo-preview",
                "create_agent": self._create_openai_agent,
                "requirements": ["OPENAI_API_KEY environment variable"],
                "cost_tier": "premium",
                "use_cases": ["general purpose", "reliable performance"]
            },
            {
                "name": "NVIDIA NIM (Llama 3)",
                "provider_id": "nvidia",
                "model_id": "nvidia/meta/llama3-8b-instruct",
                "create_agent": self._create_nvidia_agent,
                "requirements": ["NVIDIA_API_KEY environment variable"],
                "cost_tier": "free",
                "use_cases": ["development", "high throughput"]
            },
            {
                "name": "OpenRouter (Mistral Small)",
                "provider_id": "openrouter",
                "model_id": "openrouter/mistralai/mistral-small-latest:free",
                "create_agent": self._create_openrouter_agent,
                "requirements": ["OPENROUTER_API_KEY environment variable"],
                "cost_tier": "free",
                "use_cases": ["cost optimization", "experimentation"]
            }
        ]
    
    def _create_bedrock_agent(self, config: Dict[str, Any]) -> Optional[Agent]:
        """Create AWS Bedrock agent."""
        try:
            return Agent(
                model=BedrockModel(
                    model_id=config["model_id"],
                    region_name='us-east-1',
                    temperature=0.3
                ),
                tools=[calculator, current_time, http_request],
                system_prompt=f"You are a helpful assistant powered by {config['name']}. You provide accurate, concise responses."
            )
        except Exception as e:
            logger.warning(f"Failed to create Bedrock agent: {e}")
            return None
    
    def _create_openai_agent(self, config: Dict[str, Any]) -> Optional[Agent]:
        """Create OpenAI agent."""
        if not os.getenv("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY not found in environment variables")
            return None
        
        try:
            return Agent(
                model=config["model_id"],  # LiteLLM handles OpenAI format
                tools=[calculator, current_time, http_request],
                system_prompt=f"You are a helpful assistant powered by {config['name']}. You provide accurate, concise responses."
            )
        except Exception as e:
            logger.warning(f"Failed to create OpenAI agent: {e}")
            return None
    
    def _create_nvidia_agent(self, config: Dict[str, Any]) -> Optional[Agent]:
        """Create NVIDIA NIM agent."""
        if not os.getenv("NVIDIA_API_KEY"):
            logger.warning("NVIDIA_API_KEY not found in environment variables")
            return None
        
        try:
            return Agent(
                model=config["model_id"],  # LiteLLM handles NVIDIA format
                tools=[calculator, current_time, http_request],
                system_prompt=f"You are a helpful assistant powered by {config['name']}. You provide accurate, concise responses."
            )
        except Exception as e:
            logger.warning(f"Failed to create NVIDIA agent: {e}")
            return None
    
    def _create_openrouter_agent(self, config: Dict[str, Any]) -> Optional[Agent]:
        """Create OpenRouter agent."""
        if not os.getenv("OPENROUTER_API_KEY"):
            logger.warning("OPENROUTER_API_KEY not found in environment variables")
            return None
        
        try:
            return Agent(
                model=config["model_id"],  # LiteLLM handles OpenRouter format
                tools=[calculator, current_time, http_request],
                system_prompt=f"You are a helpful assistant powered by {config['name']}. You provide accurate, concise responses."
            )
        except Exception as e:
            logger.warning(f"Failed to create OpenRouter agent: {e}")
            return None
    
    def create_resilient_agent(self) -> Optional[Agent]:
        """
        Create an agent with automatic fallback across all available providers.
        Returns the first successfully created agent from the provider hierarchy.
        """
        logger.info("🔄 Attempting to create resilient multi-provider agent...")
        
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
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get current status of all providers."""
        status = {
            "available_providers": [],
            "unavailable_providers": [],
            "usage_statistics": self.usage_stats
        }
        
        for config in self.provider_configs:
            provider_info = {
                "name": config["name"],
                "provider_id": config["provider_id"],
                "cost_tier": config["cost_tier"],
                "use_cases": config["use_cases"]
            }
            
            missing_requirements = self._check_requirements(config)
            if missing_requirements:
                provider_info["missing_requirements"] = missing_requirements
                status["unavailable_providers"].append(provider_info)
            else:
                status["available_providers"].append(provider_info)
        
        return status

def demonstrate_multi_provider_setup():
    """
    Demonstrate the multi-provider setup with comprehensive testing.
    """
    print("🚀 Multi-Provider Production Agent Demo")
    print("=" * 60)
    
    # Create the factory
    factory = MultiProviderAgentFactory()
    
    # Show provider status
    print("\n📊 Provider Status Check")
    print("-" * 30)
    status = factory.get_provider_status()
    
    print("✅ Available Providers:")
    for provider in status["available_providers"]:
        print(f"  • {provider['name']} ({provider['cost_tier']} tier)")
        print(f"    Use cases: {', '.join(provider['use_cases'])}")
    
    print("\n❌ Unavailable Providers:")
    for provider in status["unavailable_providers"]:
        print(f"  • {provider['name']}")
        print(f"    Missing: {', '.join(provider['missing_requirements'])}")
    
    # Create resilient agent
    print("\n🔧 Creating Resilient Agent")
    print("-" * 30)
    agent = factory.create_resilient_agent()
    
    if not agent:
        print("❌ Failed to create any agent. Please check your API keys and credentials.")
        print("\n🔧 Setup Instructions:")
        print("1. AWS Bedrock: Configure AWS credentials with `aws configure`")
        print("2. OpenAI: Set OPENAI_API_KEY environment variable")
        print("3. NVIDIA NIM: Set NVIDIA_API_KEY environment variable")
        print("4. OpenRouter: Set OPENROUTER_API_KEY environment variable")
        return
    
    # Test the agent with various tasks
    test_queries = [
        {
            "query": "What is the current time and what's 15 * 23?",
            "description": "Tool usage test"
        },
        {
            "query": "Explain the benefits of using multiple LLM providers in production",
            "description": "Knowledge test"
        },
        {
            "query": "Search for information about AWS Strands SDK and summarize its key features",
            "description": "Web search test"
        }
    ]
    
    print("\n🧪 Testing Agent Capabilities")
    print("-" * 30)
    
    for i, test in enumerate(test_queries, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"Query: {test['query']}")
        print("Response:")
        
        try:
            response = agent(test['query'])
            print(f"✅ {response[:200]}..." if len(response) > 200 else f"✅ {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Show final statistics
    print(f"\n📈 Usage Statistics")
    print("-" * 30)
    stats = factory.usage_stats
    print(f"Total requests: {stats['total_requests']}")
    for provider_id, count in stats['requests_by_provider'].items():
        failures = stats['failures_by_provider'].get(provider_id, 0)
        success_rate = ((count - failures) / count * 100) if count > 0 else 0
        print(f"{provider_id}: {count} requests, {success_rate:.1f}% success rate")

def setup_instructions():
    """
    Display comprehensive setup instructions for all providers.
    """
    print("\n" + "=" * 60)
    print("🔧 SETUP INSTRUCTIONS FOR ALL PROVIDERS")
    print("=" * 60)
    
    providers_setup = [
        {
            "name": "AWS Bedrock (Recommended for Production)",
            "steps": [
                "1. Install AWS CLI: pip install awscli",
                "2. Configure credentials: aws configure",
                "3. Enable Claude 3.7 Sonnet in Bedrock console",
                "4. Verify: aws bedrock list-foundation-models"
            ]
        },
        {
            "name": "OpenAI (Industry Standard)",
            "steps": [
                "1. Create account at https://platform.openai.com/",
                "2. Generate API key in API Keys section",
                "3. Set environment variable: export OPENAI_API_KEY='sk-...'",
                "4. Verify: echo $OPENAI_API_KEY"
            ]
        },
        {
            "name": "NVIDIA NIM (Free for Development)",
            "steps": [
                "1. Join NVIDIA Developer Program (free)",
                "2. Visit https://build.nvidia.com/",
                "3. Select a model and get API key",
                "4. Set environment variable: export NVIDIA_API_KEY='nvapi-...'",
                "5. Verify: echo $NVIDIA_API_KEY"
            ]
        },
        {
            "name": "OpenRouter (Cost-Effective Gateway)",
            "steps": [
                "1. Create account at https://openrouter.ai/",
                "2. Go to Keys page and create new key",
                "3. Set environment variable: export OPENROUTER_API_KEY='sk-or-...'",
                "4. Verify: echo $OPENROUTER_API_KEY"
            ]
        }
    ]
    
    for provider in providers_setup:
        print(f"\n📋 {provider['name']}")
        print("-" * 40)
        for step in provider['steps']:
            print(f"  {step}")

if __name__ == "__main__":
    # Run the demonstration
    demonstrate_multi_provider_setup()
    
    # Show setup instructions
    setup_instructions()
    
    print("\n" + "=" * 60)
    print("🎓 LEARNING EXERCISES")
    print("=" * 60)
    print("""
1. **Provider Comparison**: Test the same query across different providers
   and compare response quality, speed, and cost.

2. **Fallback Testing**: Temporarily disable your primary provider (remove API key)
   and verify the fallback mechanism works correctly.

3. **Cost Optimization**: Implement logic to route simple queries to free providers
   and complex queries to premium providers.

4. **Monitoring**: Add custom metrics tracking for response times, token usage,
   and error rates across providers.

5. **Custom Provider**: Add support for a local model using Ollama or another
   provider supported by LiteLLM.

6. **Circuit Breaker**: Implement a circuit breaker pattern that temporarily
   disables failing providers to prevent cascading failures.
    """)
