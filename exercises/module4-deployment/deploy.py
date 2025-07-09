#!/usr/bin/env python3
"""
Deploy Hello Agent to AWS Lambda
Simple deployment script using AWS CLI and Python
Supports command-line arguments for profile, region, and function name
"""

import os
import sys
import json
import zipfile
import tempfile
import subprocess
import argparse
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def create_deployment_package():
    """Create the Lambda deployment package"""
    print("Creating Lambda deployment package...")
    
    # Create temporary directory for packaging
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Install dependencies with correct architecture for Lambda
        print("Installing dependencies...")
        install_cmd = f"""pip3 install -r requirements.txt \
            --target {temp_path} \
            --platform manylinux2014_x86_64 \
            --python-version 3.12 \
            --only-binary=:all: \
            --upgrade"""
        
        try:
            run_command(install_cmd)
        except:
            print("⚠️  Platform-specific install failed, trying regular install...")
            run_command(f"pip3 install -r requirements.txt -t {temp_path}")
        
        # Copy lambda handler
        handler_source = Path("lambda_handler.py")
        handler_dest = temp_path / "lambda_handler.py"
        handler_dest.write_text(handler_source.read_text())
        
        # Create ZIP file
        zip_path = Path("hello-agent-lambda.zip")
        if zip_path.exists():
            zip_path.unlink()
            
        print("Creating ZIP package...")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_path)
                    zipf.write(file_path, arcname)
        
        size_mb = zip_path.stat().st_size / 1024 / 1024
        print(f"Created deployment package: {zip_path} ({size_mb:.1f} MB)")
        return zip_path

def deploy_to_lambda(profile_name="default", region="us-east-1", function_name="hello-agent-strands", role_name="hello-agent-lambda-role"):
    """Deploy the agent to AWS Lambda"""
    
    print(f"🚀 Deploying to AWS Lambda...")
    print(f"   Function: {function_name}")
    print(f"   Region: {region}")
    print(f"   Profile: {profile_name}")
    print(f"   Role: {role_name}")
    print("-" * 50)
    
    # Create deployment package
    zip_path = create_deployment_package()
    
    # Check if role exists, create if not
    print("Checking IAM role...")
    check_role_cmd = f"aws iam get-role --role-name {role_name} --profile {profile_name}"
    result = run_command(check_role_cmd, check=False)
    
    if result.returncode != 0:
        print("Creating IAM role...")
        
        # Create trust policy
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        with open("trust-policy.json", "w") as f:
            json.dump(trust_policy, f)
        
        # Create role
        create_role_cmd = f"aws iam create-role --role-name {role_name} --assume-role-policy-document file://trust-policy.json --profile {profile_name}"
        run_command(create_role_cmd)
        
        # Attach basic Lambda execution policy
        attach_basic_cmd = f"aws iam attach-role-policy --role-name {role_name} --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole --profile {profile_name}"
        run_command(attach_basic_cmd)
        
        # Create and attach Bedrock policy
        bedrock_policy_cmd = f"aws iam put-role-policy --role-name {role_name} --policy-name BedrockAccess --policy-document file://bedrock-policy.json --profile {profile_name}"
        run_command(bedrock_policy_cmd)
        
        print("Waiting for role to be ready...")
        import time
        time.sleep(10)
    
    # Get role ARN
    get_role_cmd = f"aws iam get-role --role-name {role_name} --profile {profile_name} --query 'Role.Arn' --output text"
    role_arn = run_command(get_role_cmd).stdout.strip()
    print(f"Using role ARN: {role_arn}")
    
    # Check if function exists
    check_function_cmd = f"aws lambda get-function --function-name {function_name} --profile {profile_name} --region {region}"
    function_exists = run_command(check_function_cmd, check=False).returncode == 0
    
    if function_exists:
        print("Updating existing Lambda function...")
        update_cmd = f"aws lambda update-function-code --function-name {function_name} --zip-file fileb://{zip_path} --profile {profile_name} --region {region}"
        run_command(update_cmd)
    else:
        print("Creating new Lambda function...")
        create_cmd = f"""aws lambda create-function \
            --function-name {function_name} \
            --runtime python3.12 \
            --role {role_arn} \
            --handler lambda_handler.lambda_handler \
            --zip-file fileb://{zip_path} \
            --timeout 60 \
            --memory-size 512 \
            --profile {profile_name} \
            --region {region}"""
        run_command(create_cmd)
    
    print(f"✅ Successfully deployed {function_name} to AWS Lambda!")
    
    # Test the function
    print("Testing the deployed function...")
    test_payload = json.dumps({"prompt": "Tell me about agentic AI in exactly 50 words"})
    
    test_cmd = f"""aws lambda invoke \
        --function-name {function_name} \
        --payload '{test_payload}' \
        --profile {profile_name} \
        --region {region} \
        response.json"""
    
    run_command(test_cmd)
    
    # Show response
    if Path("response.json").exists():
        with open("response.json", "r") as f:
            response = json.load(f)
        print("\n📋 Test Response:")
        print(json.dumps(response, indent=2))
    
    # Cleanup temporary files
    for temp_file in ["trust-policy.json", "response.json"]:
        if Path(temp_file).exists():
            Path(temp_file).unlink()
    
    print(f"\n🎉 Deployment complete! Function name: {function_name}")
    print(f"Region: {region}")
    print(f"You can test it with:")
    print(f"aws lambda invoke --function-name {function_name} --cli-binary-format raw-in-base64-out --payload '{{\"prompt\": \"Your question here\"}}' --profile {profile_name} --region {region} output.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy Custom Tools Agent to AWS Lambda",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy with default profile
  python3 deploy.py
  
  # Deploy with custom profile
  python3 deploy.py --profile personal
  
  # Deploy with custom function name
  python3 deploy.py --function my-custom-agent
  
  # Deploy with custom region
  python3 deploy.py --region us-west-2 --profile personal
  
  # Full customization
  python3 deploy.py --profile personal --region us-east-1 --function custom-tools-agent
        """
    )
    
    parser.add_argument(
        "--profile", "-p",
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
        default="hello-agent-strands",
        help="Lambda function name (default: hello-agent-strands)"
    )
    
    parser.add_argument(
        "--role",
        type=str,
        default="hello-agent-lambda-role",
        help="IAM role name (default: hello-agent-lambda-role)"
    )
    
    args = parser.parse_args()
    
    print(f"🚀 Deployment Configuration:")
    print(f"   Profile: {args.profile}")
    print(f"   Region: {args.region}")
    print(f"   Function: {args.function}")
    print(f"   Role: {args.role}")
    print("=" * 50)
    
    deploy_to_lambda(
        profile_name=args.profile,
        region=args.region,
        function_name=args.function,
        role_name=args.role
    )
