#!/usr/bin/env python3
"""
Setup Verification Script for AWS Strands Workshop
Verifies all dependencies and configurations are correct.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version is 3.10+"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.10+")
        return False

def check_strands_installation():
    """Check if Strands SDK is installed correctly"""
    print("\n📦 Checking Strands SDK installation...")
    try:
        import strands
        from strands import Agent
        from strands.models import BedrockModel
        print("✅ Core strands-agents - OK")
        
        # Check OpenAI integration
        try:
            from strands.models.openai import OpenAIModel
            print("✅ strands-agents[openai] - OK")
        except ImportError:
            print("⚠️  strands-agents[openai] - Not installed (optional)")
        
        # Check LiteLLM integration
        try:
            from strands.models.litellm import LiteLLMModel
            print("✅ strands-agents[litellm] - OK")
        except ImportError:
            print("⚠️  strands-agents[litellm] - Not installed (optional)")
        
        # Check tools
        try:
            import strands_tools
            from strands_tools import calculator, current_time
            print("✅ strands-agents-tools - OK")
        except ImportError:
            print("❌ strands-agents-tools - Missing")
            return False
            
        return True
    except ImportError as e:
        print(f"❌ Strands SDK not installed: {e}")
        return False

def check_aws_credentials():
    """Check AWS credentials are configured"""
    print("\n🔑 Checking AWS credentials...")
    try:
        import boto3
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            print("✅ AWS credentials - OK")
            
            # Check region
            region = session.region_name or os.getenv('AWS_REGION', 'us-east-1')
            print(f"✅ AWS region: {region}")
            return True
        else:
            print("❌ AWS credentials not found")
            print("   Run: aws configure")
            return False
    except Exception as e:
        print(f"❌ AWS setup error: {e}")
        return False

def check_bedrock_access():
    """Check Bedrock model access"""
    print("\n🤖 Checking Bedrock access...")
    try:
        import boto3
        client = boto3.client('bedrock', region_name='us-east-1')
        
        # Try to list foundation models
        response = client.list_foundation_models()
        claude_models = [m for m in response['modelSummaries'] 
                        if 'claude-3' in m['modelId'].lower()]
        
        if claude_models:
            print("✅ Bedrock access - OK")
            print(f"✅ Found {len(claude_models)} Claude 3 models")
            return True
        else:
            print("⚠️  Bedrock access OK but no Claude 3 models found")
            print("   Enable models at: https://console.aws.amazon.com/bedrock/home#/modelaccess")
            return False
            
    except Exception as e:
        print(f"❌ Bedrock access error: {e}")
        print("   Check AWS permissions and region")
        return False

def check_environment_variables():
    """Check optional environment variables"""
    print("\n🌍 Checking environment variables...")
    
    env_vars = {
        'OPENAI_API_KEY': 'OpenAI integration',
        'NVIDIA_API_KEY': 'NVIDIA NIM integration', 
        'OPENROUTER_API_KEY': 'OpenRouter integration'
    }
    
    found_any = False
    for var, description in env_vars.items():
        if os.getenv(var):
            print(f"✅ {var} - OK ({description})")
            found_any = True
        else:
            print(f"⚠️  {var} - Not set ({description})")
    
    if not found_any:
        print("ℹ️  No optional API keys found - workshop will use Bedrock only")
    
    return True

def check_workshop_structure():
    """Check workshop directory structure"""
    print("\n📁 Checking workshop structure...")
    
    required_dirs = [
        'exercises/module1-basics',
        'exercises/module2-tools', 
        'exercises/module3-multi-agent',
        'exercises/module4-production',
        'exercises/module5-advanced',
        'exercises/module6-deployment'
    ]
    
    all_good = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path} - OK")
        else:
            print(f"❌ {dir_path} - Missing")
            all_good = False
    
    return all_good

def main():
    """Run all verification checks"""
    print("🔍 AWS Strands Workshop Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_strands_installation,
        check_aws_credentials,
        check_bedrock_access,
        check_environment_variables,
        check_workshop_structure
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED! You're ready for the workshop!")
    elif passed >= total - 2:
        print("⚠️  MOSTLY READY - Some optional features missing")
        print("   Workshop will work with reduced functionality")
    else:
        print("❌ SETUP INCOMPLETE - Please fix the issues above")
        print("   Workshop may not work properly")
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed < total:
        print("\n🛠️  NEXT STEPS:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Configure AWS: aws configure")
        print("3. Enable Bedrock models: https://console.aws.amazon.com/bedrock/home#/modelaccess")
        print("4. Set optional API keys in .env file")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
