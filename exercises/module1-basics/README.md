# Module 1: Hello Agent - Your First Strands Agent

## Learning Objectives
- Create your first working Strands agent
- Understand the model-driven approach
- Configure AWS Bedrock with Claude 3.7 Sonnet
- Run and test a basic agent

## Prerequisites
- Python 3.10+ installed
- AWS credentials configured
- Virtual environment activated
- Strands SDK installed

## Step-by-Step Instructions

### Step 1: Verify Environment Setup

First, ensure your environment is properly configured:

```bash
# Check Python version (must be 3.10+)
python --version

# Verify virtual environment is activated
which python  # Should show path to .venv

# Check Strands installation
python -c "from strands import Agent; print('Strands SDK installed successfully')"
```

### Step 2: Configure AWS Credentials

Ensure AWS credentials are configured with Bedrock permissions:

```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify region (default of strands is us-west-2)
aws configure get region
```

**Required IAM Permissions:**
- `bedrock:InvokeModel`
- `bedrock:ListFoundationModels`

### Step 3: Create Your First Agent

Create `exercise1-hello-agent.py`:

```python
from strands import Agent

# Create an agent with default settings (uses Bedrock + Claude 3.7 Sonnet)
agent = Agent()

# Ask the agent a question
response = agent("Tell me about agentic AI in exactly 50 words")
```

**Key Points:**
- Default model: Claude 3.7 Sonnet in us-west-2 region
- No explicit model configuration needed for basic usage
- Agent automatically handles conversation context

### Step 4: Run Your Agent

Execute the agent:

```bash
python -u exercise1-hello-agent.py
```

**Expected Output:**
```
Agentic AI refers to artificial intelligence systems that can act autonomously, make decisions, and take actions to achieve goals. Unlike traditional AI that simply responds to prompts, agentic AI can plan, reason, use tools, and interact with environments to complete complex tasks independently and adaptively.
```

### Step 5: Enhanced Agent with Explicit Configuration

Create `exercise1-enhanced.py` with explicit Bedrock configuration:

```python
from strands import Agent
from strands.models import BedrockModel

# Create a BedrockModel with explicit configuration
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name='us-east-1',
    temperature=0.3,
    max_tokens=200
)

# Create agent with the configured model
agent = Agent(model=bedrock_model)

# Test with multiple questions
questions = [
    "What is the capital of France?",
    "Explain machine learning in one sentence.",
    "What's 15 * 23?"
]

for question in questions:
    print(f"Q: {question}")
    response = agent(question)
    print(f"A: {response}\n")
```

### Step 6: Add Debug Logging

Create `exercise1-debug.py` to see what's happening under the hood:

```python
import logging
from strands import Agent

# Enable Strands debug logging
logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

# Create agent
agent = Agent()

# Check model configuration
print("Model Configuration:")
print(agent.model.config)

# Ask a question with debug output
print("\nAsking question with debug logging:")
response = agent("Hello! How are you today?")
print(f"\nFinal Response: {response}")
```

## Understanding the Code

### Agent Class
- `Agent()` - Creates agent with default Bedrock configuration
- `Agent(model=model)` - Creates agent with specific model
- `agent(message)` - Sends message and returns response

### BedrockModel Parameters
- `model_id` - Specific Claude model version
- `region_name` - AWS region (us-east-1, us-west-2)
- `temperature` - Response randomness (0.0-1.0)
- `max_tokens` - Maximum response length

### Model-Driven Approach
Unlike workflow-based frameworks, Strands uses the model's native reasoning:
- No rigid conversation flows
- Model decides how to respond
- Natural conversation handling

## Common Issues & Solutions

### Issue: ModuleNotFoundError
```bash
ModuleNotFoundError: No module named 'strands'
```
**Solution:** Install in activated virtual environment:
```bash
source .venv/bin/activate
pip install strands-agents
```

### Issue: AWS Credentials Error
```bash
NoCredentialsError: Unable to locate credentials
```
**Solution:** Configure AWS credentials:
```bash
aws configure
# OR set environment variables:
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### Issue: Bedrock Access Denied
```bash
AccessDeniedException: User is not authorized to perform: bedrock:InvokeModel
```
**Solution:** 
1. Enable Claude 3.7 Sonnet in [Bedrock Console](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)
2. Add IAM permissions for `bedrock:InvokeModel`

### Issue: Region Mismatch
```bash
ValidationException: The model ID is not supported in this region
```
**Solution:** Use correct region:
- Claude 3.7 Sonnet: us-east-1, us-west-2
- Update `region_name` in BedrockModel

## Testing Your Understanding

Try these exercises:

1. **Temperature Experiment**: Create agents with different temperatures (0.1, 0.5, 0.9) and ask the same question
2. **Token Limits**: Set `max_tokens=50` and see how responses change
3. **Model Comparison**: Try different Claude models if available

## Next Steps

In Module 2, you'll learn to:
- Add tools to your agent
- Create custom functions
- Handle file operations
- Build more complex interactions

## Key Takeaways

✅ **Strands agents are simple to create** - Just `Agent()` works  
✅ **Model-driven approach** - No complex workflows needed  
✅ **AWS Bedrock integration** - Enterprise-grade models  
✅ **Flexible configuration** - Customize as needed  

**Time to Complete:** 10 minutes  
**Difficulty:** Beginner  
**Prerequisites Met:** ✅ Ready for Module 2
