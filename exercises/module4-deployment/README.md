# Module 4: Lambda Deployment

## 📁 Files in this directory

### 📖 Tutorial
- `exercise4-lambda-deployment-tutorial.md` - **START HERE** - Complete deployment guide

### 🏗️ Code Files (Ready to Use)
- `lambda_handler.py` - Lambda function handler (converts your agent for serverless)
- `deploy.py` - Automated deployment script
- `test_lambda.py` - Testing script for your deployed function
- `requirements.txt` - Python dependencies
- `bedrock-policy.json` - AWS permissions for Bedrock access

### 📝 Original Exercises
- `exercise1-hello-agent.py` - Basic agent from Module 1
- `exercise2-custom-tools.py` - Custom tools agent from Module 2

## 🚀 Quick Start

1. **Read the tutorial**: `exercise4-lambda-deployment-tutorial.md`
2. **Deploy your agent**: `python3 deploy.py`
3. **Test your agent**: `python3 test_lambda.py`

## 🎯 What You'll Deploy

Your `exercise2-custom-tools.py` agent with:
- Built-in tools (calculator, current_time)
- Custom tools (letter_counter, text_reverser, word_counter)
- Production-ready Lambda deployment
- Proper error handling and security

## 📋 Prerequisites

- AWS CLI configured (`aws configure`)
- Python 3.10+
- AWS Bedrock access enabled

---

**Ready to deploy? Start with the tutorial!** 🚀
