#!/usr/bin/env python3
"""
Module 1: Simple Multi-Provider Agent - Choose Your Model

This is a REALLY SIMPLE exercise to let students use whatever AI provider they have available.
No complex fallback logic, no production patterns - just pick one and go!

Learning Objectives:
- Create your first Strands agent with ANY available provider
- Understand that Strands works with multiple AI providers
- Get started quickly regardless of which API keys you have

Choose ONE provider that you have access to:
1. AWS Bedrock (if you have AWS credentials)
2. OpenAI (if you have OpenAI API key)
3. NVIDIA NIM (free tier available)
4. OpenRouter (free tier available)
"""

import os
from strands import Agent

def create_bedrock_agent():
    """Option 1: AWS Bedrock (if you have AWS credentials configured)"""
    from strands.models import BedrockModel
    
    print("🔧 Creating AWS Bedrock agent...")
    model = BedrockModel(
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=0.3
    )
    
    return Agent(
        model=model,
        system_prompt="You are a helpful assistant powered by AWS Bedrock Claude."
    )

def create_openai_agent():
    """Option 2: OpenAI (requires OPENAI_API_KEY environment variable)"""
    from strands.models.openai import OpenAIModel
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY environment variable")
    
    print("🔧 Creating OpenAI agent...")
    model = OpenAIModel(
        client_args={"api_key": api_key},
        model_id="gpt-4o-mini",  # Cheaper option
        params={"temperature": 0.3}
    )
    
    return Agent(
        model=model,
        system_prompt="You are a helpful assistant powered by OpenAI GPT."
    )

def create_nvidia_agent():
    """Option 3: NVIDIA NIM (requires NVIDIA_API_KEY, free tier available)"""
    from strands.models.litellm import LiteLLMModel
    
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("Please set NVIDIA_API_KEY environment variable")
    
    print("🔧 Creating NVIDIA NIM agent...")
    model = LiteLLMModel(
        client_args={"api_key": api_key},
        model_id="nvidia_nim/meta/llama3-8b-instruct",
        params={"temperature": 0.3}
    )
    
    return Agent(
        model=model,
        system_prompt="You are a helpful assistant powered by NVIDIA NIM Llama."
    )

def create_openrouter_agent():
    """Option 4: OpenRouter (requires OPENROUTER_API_KEY, free tier available)"""
    from strands.models.litellm import LiteLLMModel
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENROUTER_API_KEY environment variable")
    
    print("🔧 Creating OpenRouter agent...")
    model = LiteLLMModel(
        client_args={"api_key": api_key},
        model_id="openrouter/mistralai/mistral-7b-instruct:free",
        params={"temperature": 0.3}
    )
    
    return Agent(
        model=model,
        system_prompt="You are a helpful assistant powered by OpenRouter Mistral."
    )

def show_setup_instructions():
    """Show setup instructions for each provider"""
    print("""
🛠️  SETUP INSTRUCTIONS - Choose ONE that you have access to:
================================================================

1️⃣  AWS BEDROCK (Recommended if you have AWS account)
   Setup: Configure AWS credentials
   Command: aws configure
   Cost: Pay per use
   
2️⃣  OPENAI (Popular choice)
   Setup: Get API key from https://platform.openai.com/api-keys
   Command: export OPENAI_API_KEY="sk-..."
   Install: pip install 'strands-agents[openai]'
   Cost: Pay per use
   
3️⃣  NVIDIA NIM (FREE tier available!)
   Setup: Get free API key from https://build.nvidia.com/
   Command: export NVIDIA_API_KEY="nvapi-..."
   Install: pip install 'strands-agents[litellm]'
   Cost: FREE tier available
   
4️⃣  OPENROUTER (FREE tier available!)
   Setup: Get free API key from https://openrouter.ai/keys
   Command: export OPENROUTER_API_KEY="sk-or-..."
   Install: pip install 'strands-agents[litellm]'
   Cost: FREE tier available

💡 TIP: If you don't have any API keys, try NVIDIA NIM or OpenRouter - they have free tiers!
""")

def main():
    print("🚀 Module 1: Simple Multi-Provider Agent")
    print("=" * 50)
    print("Choose the AI provider you have access to!")
    print()
    
    # Check what's available
    available_providers = []
    
    # Check AWS Bedrock
    try:
        if os.getenv("AWS_ACCESS_KEY_ID") or os.path.exists(os.path.expanduser("~/.aws/credentials")):
            available_providers.append("1. AWS Bedrock ✅")
        else:
            available_providers.append("1. AWS Bedrock ❌ (no AWS credentials)")
    except:
        available_providers.append("1. AWS Bedrock ❌ (no AWS credentials)")
    
    # Check OpenAI
    if os.getenv("OPENAI_API_KEY"):
        available_providers.append("2. OpenAI ✅")
    else:
        available_providers.append("2. OpenAI ❌ (no OPENAI_API_KEY)")
    
    # Check NVIDIA
    if os.getenv("NVIDIA_API_KEY"):
        available_providers.append("3. NVIDIA NIM ✅")
    else:
        available_providers.append("3. NVIDIA NIM ❌ (no NVIDIA_API_KEY)")
    
    # Check OpenRouter
    if os.getenv("OPENROUTER_API_KEY"):
        available_providers.append("4. OpenRouter ✅")
    else:
        available_providers.append("4. OpenRouter ❌ (no OPENROUTER_API_KEY)")
    
    print("📋 Available Providers:")
    for provider in available_providers:
        print(f"   {provider}")
    
    print("\n" + "=" * 50)
    
    # If no providers available, show setup
    if not any("✅" in p for p in available_providers):
        print("❌ No providers configured!")
        show_setup_instructions()
        return
    
    # Let user choose
    print("Choose a provider (1-4) or 'setup' for instructions:")
    
    try:
        choice = input("Your choice: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        # Handle non-interactive mode - auto-select first available
        available_choices = []
        if "AWS Bedrock ✅" in str(available_providers):
            available_choices.append('1')
        if "OpenAI ✅" in str(available_providers):
            available_choices.append('2')
        if "NVIDIA NIM ✅" in str(available_providers):
            available_choices.append('3')
        if "OpenRouter ✅" in str(available_providers):
            available_choices.append('4')
        
        if available_choices:
            choice = available_choices[0]
            print(f"Auto-selecting provider {choice} (non-interactive mode)")
        else:
            print("❌ No providers available in non-interactive mode")
            show_setup_instructions()
            return
    
    if choice == 'setup':
        show_setup_instructions()
        return
    
    # Create agent based on choice
    agent = None
    try:
        if choice == '1':
            agent = create_bedrock_agent()
        elif choice == '2':
            agent = create_openai_agent()
        elif choice == '3':
            agent = create_nvidia_agent()
        elif choice == '4':
            agent = create_openrouter_agent()
        else:
            print("❌ Invalid choice. Please choose 1, 2, 3, 4, or 'setup'")
            return
            
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        print("\n💡 Run again and type 'setup' for configuration help")
        return
    
    if not agent:
        print("❌ Failed to create agent")
        return
    
    print("✅ Agent created successfully!")
    print("\n🧪 Testing your agent...")
    print("-" * 30)
    
    # Simple test
    test_question = "Hello! Please introduce yourself in exactly 25 words."
    print(f"Question: {test_question}")
    
    try:
        response = agent(test_question)
        print(f"Response: {response}")
        
        print("\n🎉 SUCCESS! Your Strands agent is working!")
        print("\n💡 Try asking it other questions:")
        print("   - What is 15 + 23?")
        print("   - Explain AI in simple terms")
        print("   - Write a haiku about coding")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    main()
