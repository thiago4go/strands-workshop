# Deploying Strands SDK Agents on AWS Lambda: A Beginner's Guide

This tutorial will guide you through deploying Strands SDK agents to AWS Lambda. We'll cover deploying a simple "Hello Agent" and an agent with custom tools, focusing on a beginner-friendly approach.

## Why AWS Lambda for Strands Agents?

AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. This is ideal for Strands agents because:

*   **Scalability:** Lambda automatically scales your agent to handle varying loads.
*   **Cost-effectiveness:** You only pay for the compute time your agent consumes.
*   **Ease of Integration:** Lambda integrates seamlessly with other AWS services like API Gateway, which can expose your agent as a web API.

## Prerequisites

Before you begin, ensure you have the following:

1.  **An AWS Account:** If you don't have one, you can sign up for a free tier account.
2.  **AWS CLI Configured:** Ensure your AWS Command Line Interface (CLI) is installed and configured with appropriate credentials and a default region.
3.  **Python 3.8+:** Lambda supports various Python runtimes.
4.  **Basic Understanding of Python:** This tutorial assumes familiarity with Python.
5.  **Basic Understanding of AWS Lambda:** Familiarity with Lambda concepts will be helpful but is not strictly required.

## Understanding the Agent Code

We will be deploying two types of agents:

*   **Simple Agent:** From `/home/thiago/agentic-era/on-agents/agents-workspace/strands-workshop/exercises/module1-basics/exercise1-hello-agent.py`
*   **Agent with Custom Tools:** From `/home/thiago/agentic-era/on-agents/agents-workspace/strands-workshop/exercises/module2-tools/exercise2-custom-tools.py`

Since AWS Lambda is not ideal for hosting MCP servers (which are long-running processes), we will focus on agents that either use built-in Strands tools or custom tools that do not require a separate MCP server.

---

## Step 1: Deploying a Simple "Hello Agent"

First, let's deploy a basic Strands agent that simply responds to a greeting.

### 1.1. Prepare the Agent Code

We'll use the `exercise1-hello-agent.py` as our base. We need to adapt it slightly to be a Lambda handler.

**Original `exercise1-hello-agent.py` (simplified for context):**

```python
from strands import Agent
from strands.models import BedrockModel # Assuming Bedrock is configured

# Initialize the Bedrock model
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

# Create a simple agent
hello_agent = Agent(
    name="HelloAgent",
    model=model,
    system_prompt="You are a friendly AI assistant that greets users."
)

if __name__ == "__main__":
    response = hello_agent("Hello there!")
    print(response)
```

**Create `lambda_handler_hello.py`:**

We'll create a new file that acts as the Lambda function's entry point. This file will contain the `handler` function that Lambda invokes.

```python
import json
from strands import Agent
from strands.models import BedrockModel # Assuming Bedrock is configured

# Initialize the Bedrock model outside the handler for warm starts
# This ensures the model is loaded only once per Lambda instance
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
    region="us-east-1"  # Adjust region as needed
)

# Create the agent outside the handler for warm starts
hello_agent = Agent(
    name="HelloAgent",
    model=model,
    system_prompt="You are a friendly AI assistant that greets users."
)

def handler(event, context):
    # Extract the prompt from the Lambda event
    # Assuming the event payload is JSON with a 'prompt' key
    try:
        body = json.loads(event.get('body', '{}'))
        user_prompt = body.get('prompt', 'Hello!')
    except json.JSONDecodeError:
        user_prompt = event.get('prompt', 'Hello!') # Fallback for non-JSON or direct invocation

    # Invoke the Strands agent
    response = hello_agent(user_prompt)

    # Return the response in a format API Gateway can understand
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'response': str(response)
        })
    }
```

Save this content to a new file: `/home/thiago/agentic-era/on-agents/agents-workspace/strands-workshop/exercises/module4-deployment/lambda_handler_hello.py`

### 1.2. Package the Lambda Function

AWS Lambda requires your code and its dependencies to be packaged into a `.zip` file.

**a. Create `requirements.txt`:**

First, create a `requirements.txt` file in the same directory as your `lambda_handler_hello.py` file. This file lists all the Python packages your Lambda function depends on.

```
strands
boto3 # AWS SDK for Python, often useful in Lambda
```

**b. Install Dependencies and Create Deployment Package:**

You'll need to install these dependencies into a directory and then zip everything together.

```bash
# Create a directory for your deployment package
mkdir package

# Install dependencies into the 'package' directory
# Use --platform manylinux2014_x86_64 if your Lambda architecture is x86_64
# Use --platform manylinux2014_aarch64 if your Lambda architecture is arm64 (Graviton)
# For simplicity, we'll assume x86_64 for now.
pip install -r requirements.txt --target package/

# Copy your Lambda handler file into the package directory
cp lambda_handler_hello.py package/

# Navigate into the package directory
cd package/

# Zip all contents of the package directory
zip -r ../hello_agent_lambda.zip .

# Navigate back to the parent directory
cd ..
```

After these steps, you should have a `hello_agent_lambda.zip` file in your `module4-deployment` directory. This is your deployment package.

---

### 1.3. Create the Lambda Function in AWS

Now, let's create the Lambda function using the AWS CLI.

**a. Create an IAM Role for Lambda:**

Your Lambda function needs permissions to execute and to interact with other AWS services (like Bedrock for the Strands agent).

```bash
# Create a trust policy for Lambda
cat << EOF > lambda-trust-policy.json
{
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
EOF

# Create the IAM role
aws iam create-role --role-name StrandsHelloAgentLambdaRole --assume-role-policy-document file://lambda-trust-policy.json

# Attach the AWSLambdaBasicExecutionRole policy (for CloudWatch Logs)
aws iam attach-role-policy --role-name StrandsHelloAgentLambdaRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Attach a policy for Bedrock access (if using BedrockModel)
# You might need to create a custom policy with bedrock:InvokeModel permissions
aws iam attach-role-policy --role-name StrandsHelloAgentLambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess # Use a more restrictive policy in production!

# Get the ARN of the created role (you'll need this for the next step)
LAMBDA_ROLE_ARN=$(aws iam get-role --role-name StrandsHelloAgentLambdaRole --query 'Role.Arn' --output text)
echo "Lambda Role ARN: $LAMBDA_ROLE_ARN"
```

**b. Create the Lambda Function:**

```bash
aws lambda create-function \
    --function-name StrandsHelloAgent \
    --runtime python3.10 \
    --role "$LAMBDA_ROLE_ARN" \
    --handler lambda_handler_hello.handler \
    --zip-file fileb://hello_agent_lambda.zip \
    --memory 1024 \
    --timeout 30 \
    --environment Variables="{MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0,TEMPERATURE=0.3}" # Example for Bedrock
```

*   `--function-name`: A unique name for your Lambda function.
*   `--runtime`: The Python runtime version.
*   `--role`: The ARN of the IAM role you created.
*   `--handler`: The file and function name (e.g., `your_file_name.your_function_name`).
*   `--zip-file`: The path to your deployment package.
*   `--memory`: Memory allocated to the function (1024 MB is a good starting point for LLM agents).
*   `--timeout`: Maximum execution time (30 seconds is common for API Gateway, adjust as needed).
*   `--environment`: Environment variables for your agent (e.g., Bedrock model ID, temperature).

---

### 1.4. Test the Deployed Agent

Once the Lambda function is created, you can test it directly using the AWS CLI.

```bash
aws lambda invoke \
    --function-name StrandsHelloAgent \
    --payload '{"body": "{\"prompt\": \"Hello Lambda Agent!\"}"}' \
    output.json

# View the output
cat output.json
```

You should see a `output.json` file created with the response from your Lambda function. Check the contents of `output.json` to verify the agent's response.

---

## Step 2: Deploying an Agent with Custom Tools

Now, let's deploy a Strands agent that utilizes a custom tool. We'll use the `exercise2-custom-tools.py` as our base, which demonstrates a simple custom tool.

### 2.1. Prepare the Agent Code with Custom Tools

We need to adapt `exercise2-custom-tools.py` to be a Lambda handler, similar to what we did for the "Hello Agent".

**Original `exercise2-custom-tools.py` (simplified for context):**

```python
from strands import Agent, tool
from strands.models import BedrockModel

# Define a simple custom tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers and returns the result."""
    return a * b

# Initialize the Bedrock model
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

# Create an agent with the custom tool
math_agent = Agent(
    name="MathAgent",
    model=model,
    system_prompt="You are a helpful math assistant. Use the 'multiply' tool for multiplication.",
    tools=[multiply]
)

if __name__ == "__main__":
    response = math_agent("What is 5 multiplied by 7?")
    print(response)
```

**Create `lambda_handler_custom_tool.py`:**

This file will contain the `handler` function for our custom tool agent.

```python
import json
from strands import Agent, tool
from strands.models import BedrockModel

# Define the custom tool within the Lambda handler file
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers and returns the result."""
    return a * b

# Initialize the Bedrock model outside the handler for warm starts
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

# Create the agent with the custom tool outside the handler for warm starts
math_agent = Agent(
    name="MathAgent",
    model=model,
    system_prompt="You are a helpful math assistant. Use the 'multiply' tool for multiplication.",
    tools=[multiply]
)

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        user_prompt = body.get('prompt', 'What is 2 multiplied by 3?')
    except json.JSONDecodeError:
        user_prompt = event.get('prompt', 'What is 2 multiplied by 3?')

    response = math_agent(user_prompt)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'response': str(response)
        })
    }
```

Save this content to a new file: `/home/thiago/agentic-era/on-agents/agents-workspace/strands-workshop/exercises/module4-deployment/lambda_handler_custom_tool.py`

### 2.2. Package the Lambda Function with Custom Tools

The packaging process is very similar to the "Hello Agent", but we'll use the new handler file.

**a. Create `requirements.txt`:**

The `requirements.txt` will be the same as before, as the core dependencies (`strands`, `boto3`) are sufficient.

```
strands
boto3
```

**b. Install Dependencies and Create Deployment Package:**

```bash
# Create a new directory for your custom tool agent deployment package
mkdir package_custom_tool

# Install dependencies into the 'package_custom_tool' directory
pip install -r requirements.txt --target package_custom_tool/

# Copy your Lambda handler file into the package directory
cp lambda_handler_custom_tool.py package_custom_tool/

# Navigate into the package directory
cd package_custom_tool/

# Zip all contents of the package directory
zip -r ../custom_tool_agent_lambda.zip .

# Navigate back to the parent directory
cd ..
```

After these steps, you should have a `custom_tool_agent_lambda.zip` file in your `module4-deployment` directory. This is your deployment package.

---

### 2.3. Create the Lambda Function in AWS

Now, let's create the Lambda function for the custom tool agent using the AWS CLI. You can reuse the `StrandsHelloAgentLambdaRole` IAM role created earlier, as it already has the necessary permissions for Bedrock access.

```bash
# Get the ARN of the existing role
LAMBDA_ROLE_ARN=$(aws iam get-role --role-name StrandsHelloAgentLambdaRole --query 'Role.Arn' --output text)
echo "Lambda Role ARN: $LAMBDA_ROLE_ARN"

# Create the Lambda function
aws lambda create-function \
    --function-name StrandsCustomToolAgent \
    --runtime python3.10 \
    --role "$LAMBDA_ROLE_ARN" \
    --handler lambda_handler_custom_tool.handler \
    --zip-file fileb://custom_tool_agent_lambda.zip \
    --memory 1024 \
    --timeout 30 \
    --environment Variables="{MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0,TEMPERATURE=0.3}" # Example for Bedrock
```

---

### 2.4. Test the Deployed Agent with Custom Tools

Once the Lambda function is created, test it directly using the AWS CLI.

```bash
aws lambda invoke \
    --function-name StrandsCustomToolAgent \
    --payload '{"body": "{\"prompt\": \"What is 12 multiplied by 9?\"}"}' \
    output_custom_tool.json

# View the output
cat output_custom_tool.json
```

You should see a `output_custom_tool.json` file created with the response from your Lambda function. Verify that the agent correctly used the `multiply` tool to answer the question.

---

## Step 3: Cleanup

To avoid incurring unnecessary AWS charges, it's important to clean up the resources you've created.

### 3.1. Delete the Lambda Functions

```bash
aws lambda delete-function --function-name StrandsHelloAgent
aws lambda delete-function --function-name StrandsCustomToolAgent
```

### 3.2. Detach Policies and Delete the IAM Role

```bash
# Detach policies
aws iam detach-role-policy --role-name StrandsHelloAgentLambdaRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam detach-role-policy --role-name StrandsHelloAgentLambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# Delete the role
aws iam delete-role --role-name StrandsHelloAgentLambdaRole
```

### 3.3. Remove Local Files

```bash
rm -rf package/
rm -rf package_custom_tool/
rm hello_agent_lambda.zip
rm custom_tool_agent_lambda.zip
rm lambda_handler_hello.py
rm lambda_handler_custom_tool.py
rm requirements.txt
rm lambda-trust-policy.json
rm output.json
rm output_custom_tool.json
```

---

## Conclusion

Congratulations! You have successfully learned how to deploy Strands SDK agents to AWS Lambda. You've deployed both a simple "Hello Agent" and an agent with a custom tool, understanding the key steps involved in preparing your code, packaging dependencies, creating IAM roles, and deploying Lambda functions using the AWS CLI.

This tutorial focused on agents that do not require a separate MCP server, as Lambda's ephemeral nature makes long-running MCP servers challenging. For more complex scenarios involving persistent MCP servers or advanced multi-agent communication (like A2A), you might consider other AWS compute options like AWS Fargate or Amazon ECS, which are better suited for long-running processes.

### Next Steps

*   **Explore API Gateway Integration:** Learn how to integrate your Lambda function with Amazon API Gateway to expose your agent as a public REST API.
*   **Implement More Complex Tools:** Experiment with creating more sophisticated custom tools for your agents.
*   **State Management:** For conversational agents, explore how to manage session state using services like Amazon DynamoDB or external memory solutions.
*   **Monitoring and Logging:** Dive deeper into AWS CloudWatch for monitoring your Lambda function's performance and debugging.
*   **Infrastructure as Code (IaC):** For production deployments, consider using AWS Cloud Development Kit (CDK) or AWS Serverless Application Model (SAM) to define and deploy your infrastructure programmatically.

Happy building with Strands SDK and AWS Lambda!