#!/usr/bin/env python3
"""
Provider Testing Script for AWS Strands Workshop
Tests all available LLM providers to verify they work correctly.
"""

import os
import sys
from typing import Optional

def test_bedrock():
    """Test AWS Bedrock provider"""
    print("🔵 Testing AWS Bedrock...")
    try:
        from strands import Agent
        from strands.models import BedrockModel
        
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name='us-east-1',
            temperature=0.3
        )
        
        agent = Agent(model=model)
        response = agent("Say 'Bedrock working' if you can hear me.")
        
        if response and "working" in response.lower():
            print("✅ AWS Bedrock - WORKING")
            return True
        else:
            print(f"⚠️  AWS Bedrock - Response unclear: {response[:50]}...")
            return False
            
    except Exception as e:
        print(f"❌ AWS Bedrock - ERROR: {e}")
        return False

def test_openai():
    """Test OpenAI provider"""
    print("\n🟢 Testing OpenAI...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OpenAI - SKIPPED (no API key)")
        return None
    
    try:
        from strands import Agent
        from strands.models.openai import OpenAIModel
        
        model = OpenAIModel(
            client_args={"api_key": api_key},
            model_id="gpt-4o",
            params={"max_tokens": 50, "temperature": 0.3}
        )
        
        agent = Agent(model=model)
        response = agent("Say 'OpenAI working' if you can hear me.")
        
        if response and "working" in response.lower():
            print("✅ OpenAI - WORKING")
            return True
        else:
            print(f"⚠️  OpenAI - Response unclear: {response[:50]}...")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI - ERROR: {e}")
        return False

def test_nvidia():
    """Test NVIDIA NIM provider"""
    print("\n🟡 Testing NVIDIA NIM...")
    
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("⚠️  NVIDIA NIM - SKIPPED (no API key)")
        return None
    
    try:
        from strands import Agent
        from strands.models.litellm import LiteLLMModel
        
        model = LiteLLMModel(
            client_args={"api_key": api_key},
            model_id="nvidia/meta/llama3-8b-instruct",
            params={"max_tokens": 50, "temperature": 0.3}
        )
        
        agent = Agent(model=model)
        response = agent("Say 'NVIDIA working' if you can hear me.")
        
        if response and "working" in response.lower():
            print("✅ NVIDIA NIM - WORKING")
            return True
        else:
            print(f"⚠️  NVIDIA NIM - Response unclear: {response[:50]}...")
            return False
            
    except Exception as e:
        print(f"❌ NVIDIA NIM - ERROR: {e}")
        return False

def test_openrouter():
    """Test OpenRouter provider"""
    print("\n🟣 Testing OpenRouter...")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("⚠️  OpenRouter - SKIPPED (no API key)")
        return None
    
    try:
        from strands import Agent
        from strands.models.litellm import LiteLLMModel
        
        model = LiteLLMModel(
            client_args={"api_key": api_key},
            model_id="openrouter/mistralai/mistral-small-latest:free",
            params={"max_tokens": 50, "temperature": 0.3}
        )
        
        agent = Agent(model=model)
        response = agent("Say 'OpenRouter working' if you can hear me.")
        
        if response and "working" in response.lower():
            print("✅ OpenRouter - WORKING")
            return True
        else:
            print(f"⚠️  OpenRouter - Response unclear: {response[:50]}...")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter - ERROR: {e}")
        return False

def test_tools():
    """Test Strands tools integration"""
    print("\n🛠️  Testing Tools...")
    try:
        from strands import Agent
        from strands.models import BedrockModel
        from strands_tools import calculator
        
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name='us-east-1',
            temperature=0.3
        )
        
        agent = Agent(model=model, tools=[calculator])
        response = agent("What is 15 * 23? Use the calculator tool.")
        
        if "345" in str(response):
            print("✅ Tools Integration - WORKING")
            return True
        else:
            print(f"⚠️  Tools Integration - Unexpected result: {response[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ Tools Integration - ERROR: {e}")
        return False

def main():
    """Run all provider tests"""
    print("🧪 AWS Strands Workshop Provider Testing")
    print("=" * 50)
    print("Testing all available LLM providers...")
    
    # Load environment variables from .env if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("📄 Loaded .env file")
    except ImportError:
        print("ℹ️  python-dotenv not installed - using system environment")
    except:
        print("ℹ️  No .env file found - using system environment")
    
    # Run all tests
    tests = [
        ("AWS Bedrock", test_bedrock),
        ("OpenAI", test_openai), 
        ("NVIDIA NIM", test_nvidia),
        ("OpenRouter", test_openrouter),
        ("Tools", test_tools)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            result = test_func()
            results[name] = result
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PROVIDER TEST SUMMARY")
    print("=" * 50)
    
    working = [name for name, result in results.items() if result is True]
    skipped = [name for name, result in results.items() if result is None]
    failed = [name for name, result in results.items() if result is False]
    
    print(f"✅ Working: {len(working)} providers")
    for name in working:
        print(f"   • {name}")
    
    if skipped:
        print(f"\n⚠️  Skipped: {len(skipped)} providers (no API keys)")
        for name in skipped:
            print(f"   • {name}")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)} providers")
        for name in failed:
            print(f"   • {name}")
    
    # Recommendations
    print(f"\n🎯 WORKSHOP READINESS:")
    if len(working) >= 2:  # Bedrock + at least one other
        print("🎉 EXCELLENT! Multiple providers working - full workshop experience available")
    elif "AWS Bedrock" in working:
        print("✅ GOOD! Bedrock working - core workshop will work fine")
        print("   Optional: Add API keys for multi-provider exercises")
    else:
        print("❌ CRITICAL! Bedrock not working - workshop will fail")
        print("   Fix AWS credentials and Bedrock access before workshop")
    
    return len(working) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
