# Module 1: Hello Agent - Architecture

## Overview
This module demonstrates the foundational architecture of the AWS Strands SDK with basic agent creation and multi-provider support. It includes two exercises: a simple "Hello Agent" introduction and an interactive multi-provider setup guide.

## Architecture Diagram

```mermaid
graph TB
    User[👤 User Input] --> Exercise1[📝 Exercise 1<br/>Hello Agent]
    User --> Exercise2[📝 Exercise 2<br/>Multi-Provider]
    
    Exercise1 --> DefaultAgent[🤖 Agent()<br/>Default Configuration]
    DefaultAgent --> BedrockDefault[☁️ AWS Bedrock<br/>Claude 3.7 Sonnet]
    
    Exercise2 --> ProviderSelection[🔧 Provider Selection<br/>Interactive Menu]
    ProviderSelection --> CredentialCheck[🔍 Credential Detection<br/>Auto-Discovery]
    
    CredentialCheck --> BedrockAgent[🤖 Bedrock Agent<br/>Claude 3.7 Sonnet]
    CredentialCheck --> OpenAIAgent[🤖 OpenAI Agent<br/>GPT-4o-mini]
    CredentialCheck --> NVIDIAAgent[🤖 NVIDIA NIM Agent<br/>Llama3-8B]
    CredentialCheck --> OpenRouterAgent[🤖 OpenRouter Agent<br/>Mistral-7B]
    
    BedrockAgent --> AWSBedrock[☁️ AWS Bedrock<br/>us.anthropic.claude-3-7-sonnet-20250219-v1:0]
    OpenAIAgent --> OpenAIAPI[☁️ OpenAI API<br/>gpt-4o-mini]
    NVIDIAAgent --> NVIDIAAPI[☁️ NVIDIA NIM<br/>meta/llama3-8b-instruct]
    OpenRouterAgent --> OpenRouterAPI[☁️ OpenRouter<br/>mistralai/mistral-7b-instruct:free]
    
    AWSBedrock --> Response1[📄 Response]
    OpenAIAPI --> Response2[📄 Response]
    NVIDIAAPI --> Response3[📄 Response]
    OpenRouterAPI --> Response4[📄 Response]
    
    BedrockDefault --> SimpleResponse[📄 Simple Response]
    
    subgraph "Workshop Exercises"
        Exercise1
        Exercise2
    end
    
    subgraph "Agent Configurations"
        DefaultAgent
        BedrockAgent
        OpenAIAgent
        NVIDIAAgent
        OpenRouterAgent
    end
    
    subgraph "Provider Infrastructure"
        AWSBedrock
        OpenAIAPI
        NVIDIAAPI
        OpenRouterAPI
        BedrockDefault
    end
    
    style User fill:#e1f5fe
    style Exercise1 fill:#f3e5f5
    style Exercise2 fill:#e8f5e8
    style ProviderSelection fill:#fff3e0
    style CredentialCheck fill:#fce4ec
```

## Workshop Exercises

### Exercise 1: Hello Agent (exercise1-hello-agent.py)
```python
#!/usr/bin/env python3
"""
Module 1: Hello Agent - Your First Strands Agent
Based on official Strands SDK documentation
"""

from strands import Agent

def main():
    # Create an agent with default settings (uses Bedrock + Claude 3.7 Sonnet)
    agent = Agent()
    
    agent("Tell me about agentic AI in exactly 50 words")
    
if __name__ == "__main__":
    main()
```

**Key Features:**
- **Minimal Setup**: Single line agent creation
- **Default Configuration**: Uses AWS Bedrock with Claude 3.7 Sonnet
- **Zero Configuration**: No explicit model or parameters needed
- **Educational Focus**: Simple introduction to Strands SDK

### Exercise 2: Multi-Provider Agent (exercise1-simple-multi-provider.py)
```python
#!/usr/bin/env python3
"""
Module 1: Simple Multi-Provider Agent - Choose Your Model

Learning Objectives:
- Create your first Strands agent with ANY available provider
- Understand that Strands works with multiple AI providers
- Get started quickly regardless of which API keys you have
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
```

## Interactive Provider Selection

### Credential Auto-Detection
```python
def main():
    print("🚀 Module 1: Simple Multi-Provider Agent")
    print("Choose the AI provider you have access to!")
    
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
    
    # Similar checks for NVIDIA and OpenRouter...
    
    print("📋 Available Providers:")
    for provider in available_providers:
        print(f"   {provider}")
```

### Setup Instructions System
```python
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
```

## Provider Configurations

### 1. AWS Bedrock (Default)
```python
# Default agent (Exercise 1)
agent = Agent()

# Explicit Bedrock configuration (Exercise 2)
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)
agent = Agent(model=model)
```

**Features:**
- **Model**: Claude 3.7 Sonnet (latest version)
- **Authentication**: AWS credentials via `aws configure`
- **Cost**: Pay-per-token
- **Setup**: Requires AWS account and Bedrock access

### 2. OpenAI Integration
```python
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    client_args={"api_key": api_key},
    model_id="gpt-4o-mini",  # Cost-optimized choice
    params={"temperature": 0.3}
)
```

**Features:**
- **Model**: GPT-4o-mini (cost-effective)
- **Authentication**: API key via environment variable
- **Cost**: Pay-per-token
- **Setup**: OpenAI account required

### 3. NVIDIA NIM Integration
```python
from strands.models.litellm import LiteLLMModel

model = LiteLLMModel(
    client_args={"api_key": api_key},
    model_id="nvidia_nim/meta/llama3-8b-instruct",
    params={"temperature": 0.3}
)
```

**Features:**
- **Model**: Llama3-8B-Instruct
- **Authentication**: NVIDIA API key
- **Cost**: FREE tier available
- **Setup**: NVIDIA Developer account

### 4. OpenRouter Integration
```python
from strands.models.litellm import LiteLLMModel

model = LiteLLMModel(
    client_args={"api_key": api_key},
    model_id="openrouter/mistralai/mistral-7b-instruct:free",
    params={"temperature": 0.3}
)
```

**Features:**
- **Model**: Mistral-7B-Instruct (free tier)
- **Authentication**: OpenRouter API key
- **Cost**: FREE tier available
- **Setup**: OpenRouter account

## Educational Features

### Interactive Learning Flow
1. **Provider Discovery**: Automatic credential detection
2. **Guided Setup**: Detailed instructions for each provider
3. **Interactive Selection**: User chooses preferred provider
4. **Validation**: Test agent with sample question
5. **Success Feedback**: Encouragement and next steps

### Non-Interactive Mode Support
```python
try:
    choice = input("Your choice: ").strip().lower()
except (EOFError, KeyboardInterrupt):
    # Handle non-interactive mode - auto-select first available
    available_choices = []
    if "AWS Bedrock ✅" in str(available_providers):
        available_choices.append('1')
    # ... check other providers
    
    if available_choices:
        choice = available_choices[0]
        print(f"Auto-selecting provider {choice} (non-interactive mode)")
```

### Error Handling & User Guidance
```python
try:
    if choice == '1':
        agent = create_bedrock_agent()
    elif choice == '2':
        agent = create_openai_agent()
    # ... other providers
        
except Exception as e:
    print(f"❌ Failed to create agent: {e}")
    print("\n💡 Run again and type 'setup' for configuration help")
    return
```

## Data Flow Patterns

### Exercise 1 Flow
1. **Import** → `from strands import Agent`
2. **Create** → `agent = Agent()` (uses default Bedrock)
3. **Invoke** → `agent("query")` (direct method call)
4. **Response** → Immediate output

### Exercise 2 Flow
1. **Detection** → Check available credentials
2. **Selection** → User chooses provider
3. **Configuration** → Create provider-specific model
4. **Creation** → Agent with custom model and system prompt
5. **Testing** → Validate with sample question
6. **Feedback** → Success confirmation and suggestions

## Installation Requirements

### Core SDK
```bash
pip install strands-agents
```

### Provider-Specific Extensions
```bash
# For OpenAI support
pip install 'strands-agents[openai]'

# For NVIDIA NIM and OpenRouter support
pip install 'strands-agents[litellm]'

# For all providers
pip install 'strands-agents[openai,litellm]'
```

### Environment Configuration
```bash
# AWS Bedrock (Option 1)
aws configure

# OpenAI (Option 2)
export OPENAI_API_KEY="sk-..."

# NVIDIA NIM (Option 3)
export NVIDIA_API_KEY="nvapi-..."

# OpenRouter (Option 4)
export OPENROUTER_API_KEY="sk-or-..."
```

## Performance Characteristics

### Latency Comparison
- **AWS Bedrock**: ~2-4 seconds (enterprise-grade)
- **OpenAI**: ~1-3 seconds (optimized infrastructure)
- **NVIDIA NIM**: ~1-2 seconds (GPU-accelerated)
- **OpenRouter**: ~2-5 seconds (varies by model)

### Cost Considerations
- **AWS Bedrock**: Enterprise pricing, pay-per-token
- **OpenAI**: Standard API pricing
- **NVIDIA NIM**: FREE tier available + paid tiers
- **OpenRouter**: FREE models available + premium options

## Error Handling Strategies

### Common Issues & Solutions
```python
# AWS Credentials not configured
if not (os.getenv("AWS_ACCESS_KEY_ID") or os.path.exists("~/.aws/credentials")):
    print("❌ AWS credentials not found")
    print("💡 Run: aws configure")

# Missing API keys
if not os.getenv("OPENAI_API_KEY"):
    print("❌ OpenAI API key not found")
    print("💡 Set: export OPENAI_API_KEY='sk-...'")

# Model access issues
try:
    response = agent(query)
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Check your API key and model access")
```

### Graceful Degradation
- Auto-detection of available providers
- Clear error messages with actionable guidance
- Setup instructions always accessible
- Non-interactive mode fallback

## Security Considerations

### Credential Management
- **Environment Variables**: Preferred method for API keys
- **AWS Credentials**: Standard AWS credential chain
- **No Hardcoding**: All examples use environment variables
- **Scope Limitation**: Minimal required permissions

### Best Practices
```python
# ✅ Good: Use environment variables
api_key = os.getenv("OPENAI_API_KEY")

# ❌ Bad: Hardcode credentials
api_key = "sk-hardcoded-key"  # Never do this

# ✅ Good: Check before using
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY")
```

## Future Extensions

### Potential Enhancements
- **Custom Model IDs**: Allow users to specify different models
- **Advanced Parameters**: Temperature, max_tokens, etc. customization
- **Provider Benchmarking**: Side-by-side comparison mode
- **Configuration Persistence**: Save preferred provider choice
- **Batch Testing**: Test multiple providers simultaneously

### Workshop Progression
Module 1 sets the foundation for:
- **Module 2**: Adding tools and capabilities
- **Module 3**: Multi-agent orchestration
- **Module 4**: Production resilience patterns
- **Module 5**: A2A protocol integration