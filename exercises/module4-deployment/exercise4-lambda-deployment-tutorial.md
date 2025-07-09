# Module 4: Deploying Strands Agents to AWS Lambda

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- Deploy a Strands agent with custom tools to AWS Lambda
- Configure proper IAM permissions for Bedrock access
- Test your deployed Lambda function
- Understand serverless deployment patterns for AI agents

## 📋 Prerequisites

- AWS CLI configured with your credentials (`aws configure`)
- Python 3.10+ installed
- Completed Module 2 (Custom Tools)
- AWS account with Bedrock access enabled

## 🏗️ What We're Deploying

We'll deploy your `exercise2-custom-tools.py` agent to AWS Lambda. This agent includes:
- **Built-in tools**: calculator, current_time
- **Custom tools**: letter_counter, text_reverser, word_counter
- **Bedrock integration**: Uses Claude 3.7 Sonnet

## 📁 Step 1: Create Lambda Handler

First, we need to convert your agent to work with AWS Lambda's event-driven model.

Create a new file called `lambda_handler.py` (see the code file in this directory)

**Key changes from your original agent:**
- Added `lambda_handler(event, context)` function - this is what Lambda calls
- Extract the prompt from the Lambda event object
- Return a proper HTTP response with status code and JSON body
- Added error handling for production use

## 📦 Step 2: Create Requirements File

Create `requirements.txt` (see the file in this directory)

This tells Lambda what Python packages to install.

## 🔐 Step 3: Create IAM Policy for Bedrock

The `bedrock-policy.json` file (already in this directory) defines what AWS services your Lambda can access.

**Key permissions:**
- `bedrock:InvokeModel` - Call Bedrock models
- `bedrock:InvokeModelWithResponseStream` - Stream responses
- Covers all Claude model variants

## 🚀 Step 4: Deploy Your Agent

Use the `deploy.py` script (see the file in this directory) to automate deployment.

**What the deployment script does:**
1. **Package Dependencies** - Downloads all Python packages for Lambda
2. **Create IAM Role** - Sets up permissions for your function
3. **Deploy Function** - Uploads your code to Lambda
4. **Test Function** - Runs a quick test to verify it works

### Run Deployment
```bash
python3 deploy.py
```

The script will:
- ✅ Create a deployment package with all dependencies
- ✅ Create IAM role with proper permissions
- ✅ Deploy your agent to Lambda
- ✅ Run a test to verify everything works

## 🧪 Step 5: Test Your Deployed Agent

Use the `test_lambda.py` script (see the file in this directory) for easy testing.

### Run Tests
```bash
# Run all predefined test cases
python3 test_lambda.py

# Test with custom prompt
python3 test_lambda.py "Calculate the square root of 144 and reverse the word 'lambda'"
```

### Manual Testing
```bash
aws lambda invoke \
  --function-name custom-tools-agent \
  --cli-binary-format raw-in-base64-out \
  --payload '{"prompt": "What tools do you have?"}' \
  --region us-east-1 \
  output.json && cat output.json
```

## 🔧 Troubleshooting

### Common Issues and Solutions

**1. "ModuleNotFoundError" in Lambda**
- Re-run the deployment script to ensure all dependencies are included

**2. "AccessDeniedException" for Bedrock**
- Check that Claude 3.7 Sonnet is enabled in your AWS Bedrock console
- Verify the IAM role has the correct permissions

**3. "Function not found" error**
- Check the function name and region in your test commands

**4. Timeout errors**
- The function timeout is set to 60 seconds, which should be sufficient

### Verification Commands
```bash
# Check if function exists
aws lambda get-function --function-name custom-tools-agent --region us-east-1

# Manual test
aws lambda invoke \
  --function-name custom-tools-agent \
  --cli-binary-format raw-in-base64-out \
  --payload '{"prompt": "What tools do you have?"}' \
  --region us-east-1 \
  output.json && cat output.json
```

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Lambda function is created without errors
- ✅ Test cases run successfully
- ✅ Agent responds with tool usage (calculations, time, text operations)
- ✅ All custom tools are available and working

## 🚀 Next Steps

Once deployed, you can:
1. **Add API Gateway** to create HTTP endpoints
2. **Monitor with CloudWatch** for performance metrics
3. **Scale to multi-agent systems** (Module 3)
4. **Implement streaming responses** for real-time interaction

## 📚 Key Concepts Learned

- **Serverless Architecture**: No server management required
- **Event-Driven Processing**: Lambda responds to events/requests
- **IAM Security**: Proper permissions for AWS services
- **Dependency Management**: Packaging Python dependencies for Lambda
- **Tool Integration**: Custom tools work seamlessly in serverless environment

---

**🎯 Congratulations!** You've successfully deployed a production-ready AI agent with custom tools to AWS Lambda! Your agent is now scalable, cost-effective, and ready for real-world use.
