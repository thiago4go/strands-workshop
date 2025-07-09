# AWS Strands AI Agents Workshop

## 🚀 Workshop Overview

**Building Production AI Agents with AWS Strands SDK**  
**Duration**: 1 hour and 20 minutes (80 minutes)  
**Format**: Hands-on workshop with live coding  
**Target Audience**: Developers, AI Engineers, Solution Architects

## 🎯 Learning Objectives

By the end of this workshop, you will be able to:
1. Build AI agents using the model-driven AWS Strands SDK approach
2. Integrate multiple LLM providers (Bedrock, OpenAI, NVIDIA NIM, OpenRouter)
3. Create custom tools and extend agent capabilities
4. Implement multi-agent orchestration patterns using agents-as-tools
5. Deploy agents to production using AWS Lambda
6. Understand A2A protocol for agent interoperability
7. Integrate MCP (Model Context Protocol) for enhanced tool capabilities

## 🚀 Quick Start with GitHub Codespaces (Recommended)

**Get started in under 2 minutes with zero local setup!**

1. **Fork this repository**: [Fork strands-workshop](https://github.com/thiago4go/strands-workshop/fork)
2. **Launch Codespace**: Click "Code" → "Create codespace on main"
3. **Wait for setup** (2-3 minutes): All dependencies install automatically
4. **Configure AWS**: Run `aws configure` and enable Claude 3.7 Sonnet in [Bedrock Console](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)
5. **Verify & Start**: `python setup/verify_setup.py` then begin Module 1

[📖 **Detailed Codespaces Setup Guide**](CODESPACES_SETUP.md)

## 📋 Prerequisites (Local Setup Only)

*Skip this section if using Codespaces above*

### Required Setup
- **Python 3.10+** installed
- **AWS Account** with Bedrock access
- **Docker** (for MCP server integration)
- **API Keys** (optional but recommended):
  - OpenAI API key
  - NVIDIA NIM API key  
  - OpenRouter API key

### Pre-Workshop Setup
1. Fork and clone this repository
2. Create virtual environment: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure AWS credentials: `aws configure`
5. Enable Claude 3.7 Sonnet in [AWS Bedrock Console](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)
6. Verify setup: `python setup/verify_setup.py`

## 🏗️ Workshop Structure: Three-Act Journey

### **Act I: The Single Agent (20 minutes)**
Master individual agent development

- **Module 1: Hello Agent** (10 min) - Your first working agent with basic model integration
- **Module 2: Custom Tools** (10 min) - Extend agent capabilities with @tool decorator and MCP integration

### **Act II: Multi-Agent Orchestration (35 minutes)**  
Build collaborative agent systems

- **Module 3: Research Team** (20 min) - Real multi-agent coordination using agents-as-tools pattern with MCP
- **Module 4: Lambda Deployment** (20 min) - Production deployment patterns and serverless architecture

### **Act III: Advanced Patterns & Interoperability (25 minutes)**
Production deployment and interoperability

- **Module 5: A2A Preview** (20 min) - Agent-to-agent communication with decoupled architecture

## 📁 Directory Structure

```
strands-workshop/
├── README.md                          # This file
├── setup/                             # Setup verification scripts
│   ├── verify_setup.py               # Complete setup verification
│   ├── test_providers.py             # Test provider access
│   └── troubleshooting.md            # Common issue resolution
└── exercises/                         # Progressive workshop modules
    ├── module1-basics/
    │   ├── README.md                  # Module 1 documentation
    │   ├── exercise1-hello-agent.py   # Basic agent creation
    │   └── exercise1-simple-multi-provider.py  # Multi-provider example
    ├── module2-tools/
    │   ├── README.md                  # Module 2 documentation
    │   ├── MCP_INTEGRATION.md         # MCP integration guide
    │   ├── exercise2-custom-tools.py  # Custom tool development
    │   └── optional-module2-mcp-integration.py  # Optional MCP exercise
    ├── module3-multi-agent/
    │   ├── README.md                  # Module 3 documentation
    │   └── exercise3-research-team.py # Multi-agent orchestration
    ├── module4-deployment/
    │   └── exercise4-lambda-deployment-tutorial.md  # Deployment guide
    └── module5-advanced/
        ├── README.md                  # Module 5 documentation
        ├── exercise5-a2a-preview.py   # A2A protocol overview
        ├── main.py                    # A2A system entry point
        └── src/                       # Decoupled agent implementation
            ├── orchestrator.py        # Main orchestration logic
            ├── research_agent.py      # Research specialist
            ├── analysis_agent.py      # Analysis specialist
            ├── factcheck_agent.py     # Fact-checking specialist
            └── qa_agent.py            # Quality assurance specialist
```

## 🔧 Quick Start

1. **Verify Setup**:
   ```bash
   python setup/verify_setup.py
   ```

2. **Test Provider Access**:
   ```bash
   python setup/test_providers.py
   ```

3. **Start with Module 1**:
   ```bash
   cd exercises/module1-basics
   python exercise1-hello-agent.py
   ```

## 🛠️ Installation Commands

### Core Dependencies
```bash
# Virtual environment setup
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Individual Component Installation
```bash
# Core Strands SDK
pip install strands-agents

# Provider-specific dependencies
pip install 'strands-agents[openai]'      # OpenAI integration
pip install 'strands-agents[litellm]'     # NVIDIA NIM and OpenRouter
pip install 'strands-agents-tools'        # Built-in tools

# AWS integration
pip install boto3                                 # AWS SDK for Bedrock
```

## 🔑 Environment Variables

Create a `.env` file in the workshop root:
```bash
# AWS (configured via aws configure)
AWS_REGION=us-east-1

# Optional API Keys
OPENAI_API_KEY=sk-...
NVIDIA_API_KEY=nvapi-...
OPENROUTER_API_KEY=sk-or-...
```

## 📚 Key Technologies

- **AWS Strands SDK**: Model-driven agent framework with intelligent routing
- **Amazon Bedrock**: Enterprise LLM service (Claude 3.7 Sonnet)
- **OpenAI**: GPT-4 models for comparison and fallback
- **NVIDIA NIM**: GPU-accelerated inference
- **OpenRouter**: Cost-effective model gateway
- **MCP (Model Context Protocol)**: Tool integration and external service access
- **AWS Lambda**: Serverless deployment and production scaling
- **A2A Protocol**: Agent-to-agent communication standard

## 🎓 Workshop Learning Path

Each module builds progressive complexity:
1. **Module 1: Hello Agent** → Master core SDK concepts and basic agent creation
2. **Module 2: Custom Tools** → Extend capabilities with @tool decorator and MCP integration
3. **Module 3: Multi-Agent** → Real orchestration using agents-as-tools pattern
4. **Module 4: Lambda Deployment** → Production deployment patterns and serverless architecture
5. **Module 5: A2A Preview** → Advanced interoperability and decoupled agent systems

## 🏗️ Architecture Patterns

### Module 1: Basic Agent Architecture
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │───▶│    Agent    │───▶│   Bedrock   │
│   Input     │    │   (Strands) │    │   Claude    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Module 2: Agent + Custom Tools
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │───▶│    Agent    │───▶│   Bedrock   │
│   Input     │    │   +Tools    │    │   Claude    │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │ Custom Tools│
                   │ MCP Server  │
                   └─────────────┘
```

### Module 3: Multi-Agent Orchestration
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │───▶│Orchestrator │───▶│   Bedrock   │
│   Input     │    │   Agent     │    │   Claude    │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │ Specialist  │
                   │   Agents    │
                   │ (@tool)     │
                   └─────────────┘
```

### Module 4: Lambda Deployment
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Lambda    │───▶│   Bedrock   │
│  Request    │    │   Handler   │    │   Claude    │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │ Agent Logic │
                   │   +Tools    │
                   └─────────────┘
```

### Module 5: A2A Decoupled Architecture
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │───▶│Orchestrator │───▶│ Research    │
│   Input     │    │   Process   │    │   Agent     │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ├─────────▶ ┌─────────────┐
                           │           │ Analysis    │
                           │           │   Agent     │
                           │           └─────────────┘
                           │
                           └─────────▶ ┌─────────────┐
                                       │ Fact-Check  │
                                       │   Agent     │
                                       └─────────────┘
```

## 🆘 Troubleshooting

### Common Issues
- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **AWS Credentials**: Run `aws configure` and ensure Bedrock access
- **Bedrock Access**: Enable Claude 3.7 Sonnet in [AWS Bedrock Console](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)
- **API Keys**: Check environment variables in `.env` file
- **Docker Issues**: Required for MCP server integration (DuckDuckGo, Sequential Thinking)
- **MCP Connection**: Ensure Docker is running for MCP server-based tools

### Getting Help
- Check `setup/troubleshooting.md` for detailed issue resolution
- Use setup verification scripts: `python setup/verify_setup.py`
- Review individual module READMEs for specific guidance

## 📖 Additional Resources

- [AWS Strands SDK Documentation](https://strandsagents.com/)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [Model Context Protocol (MCP) Documentation](https://modelcontextprotocol.io/)
- [A2A Protocol Documentation](https://github.com/a2aproject/A2A)


---

**Ready to build production AI agents? Let's get started! 🚀**

