#!/usr/bin/env python3
"""
Test script for the deployed Custom Tools Agent Lambda function
Supports profile selection and custom prompts
"""

import json
import subprocess
import sys
import argparse
from pathlib import Path

def test_lambda(prompt, function_name="custom-tools-agent", profile="default", region="us-east-1"):
    """Test the deployed Lambda function"""
    
    payload = json.dumps({"prompt": prompt})
    
    # Build AWS CLI command
    cmd = [
        "aws", "lambda", "invoke",
        "--function-name", function_name,
        "--cli-binary-format", "raw-in-base64-out",
        "--payload", payload,
        "--region", region,
        "lambda_test_output.json"
    ]
    
    # Add profile if not default
    if profile != "default":
        cmd.extend(["--profile", profile])
    
    print(f"🧪 Testing Lambda function: {function_name}")
    print(f"📝 Prompt: {prompt}")
    print(f"🔧 Profile: {profile}")
    print(f"🌍 Region: {region}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        with open("lambda_test_output.json", "r") as f:
            response = json.load(f)
        
        if response.get("statusCode") == 200:
            body = json.loads(response["body"])
            print("✅ Success!")
            print(f"🤖 Response: {body['message']}")
            if 'available_tools' in body:
                print(f"🛠️  Available Tools: {', '.join(body['available_tools'])}")
        else:
            print("❌ Error!")
            print(f"Status Code: {response.get('statusCode')}")
            if "body" in response:
                body = json.loads(response["body"])
                print(f"Error: {body.get('error', 'Unknown error')}")
        
        Path("lambda_test_output.json").unlink(missing_ok=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ AWS CLI Error: {e}")
        print(f"stderr: {e.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function with argument parsing"""
    
    parser = argparse.ArgumentParser(
        description="Test deployed Custom Tools Agent Lambda function",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with default profile and predefined test cases
  python3 test_lambda.py
  
  # Test with custom profile
  python3 test_lambda.py --profile personal
  
  # Test with custom prompt
  python3 test_lambda.py --prompt "Calculate 15 * 23 + 47"
  
  # Test with custom profile and prompt
  python3 test_lambda.py --profile personal --prompt "What time is it?"
  
  # Test different function name
  python3 test_lambda.py --function hello-agent-strands --profile personal
        """
    )
    
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        help="Custom prompt to send to the agent"
    )
    
    parser.add_argument(
        "--profile",
        type=str,
        default="default",
        help="AWS profile to use (default: default)"
    )
    
    parser.add_argument(
        "--region", "-r",
        type=str,
        default="us-east-1",
        help="AWS region (default: us-east-1)"
    )
    
    parser.add_argument(
        "--function", "-f",
        type=str,
        default="custom-tools-agent",
        help="Lambda function name (default: custom-tools-agent)"
    )
    
    args = parser.parse_args()
    
    if args.prompt:
        # Single test with custom prompt
        test_lambda(args.prompt, args.function, args.profile, args.region)
    else:
        # Run predefined test cases
        test_cases = [
            "What tools do you have available?",
            "Calculate 15 * 23 + 47",
            "What time is it right now?",
            "How many letter 'r's are in the word 'strawberry'?",
            "Reverse the text 'Hello World'",
            "How many words are in this sentence: 'The quick brown fox jumps'?"
        ]
        
        print("🚀 Running predefined test cases...")
        print(f"🔧 Profile: {args.profile}")
        print(f"🌍 Region: {args.region}")
        print(f"⚡ Function: {args.function}")
        print("=" * 60)
        
        for i, prompt in enumerate(test_cases, 1):
            print(f"\n{i}/{len(test_cases)}:")
            test_lambda(prompt, args.function, args.profile, args.region)
            if i < len(test_cases):
                print("\n" + "─" * 60)

if __name__ == "__main__":
    main()
