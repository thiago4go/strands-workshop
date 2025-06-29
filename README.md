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
4. Implement multi-agent orchestration patterns
5. Deploy agents to production using AWS Lambda
6. Understand A2A protocol for agent interoperability

## 📋 Prerequisites

### Required Setup
- **Python 3.10+** installed
- **AWS Account** with Bedrock access
- **API Keys** (optional but recommended):
  - OpenAI API key
  - NVIDIA NIM API key  
  - OpenRouter API key

### Pre-Workshop Setup
1. Clone this repository
2. Set up virtual environment: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure AWS credentials: `aws configure`
5. Enable Claude 3.7 Sonnet in [AWS Bedrock Console](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)

## 🏗️ Workshop Structure: Three-Act Journey

### **Act I: The Single Agent (15 minutes)**
Master individual agent development

- **Module 1: Hello Agent** (5 min) - Your first working agent
- **Module 2: Custom Tools** (10 min) - Extend agent capabilities

### **Act II: Multi-Agent Orchestration (30 minutes)**  
Build collaborative agent systems

- **Module 3: Research Team** (15 min) - Agent collaboration patterns
- **Module 4: Multi-Provider** (15 min) - Production resilience with OpenAI integration

### **Act III: A2A Protocol & Deployment (30 minutes)**
Production deployment and interoperability

- **Module 5: A2A Preview** (15 min) - Agent-to-agent communication
- **Module 6: Lambda Deployment** (15 min) - Deploy to production

## 📁 Directory Structure

```
strands-workshop/
├── README.md                    # This file
├── WORKSHOP_PLAN.md            # Detailed instructor guide
├── requirements.txt            # Python dependencies
├── setup/                      # Setup verification scripts
│   ├── verify_setup.py
│   └── test_providers.py
└── exercises/                  # All workshop exercises
    ├── module1-basics/
    │   └── exercise1-hello-agent.py
    ├── module2-tools/
    │   └── exercise2-custom-tools.py
    ├── module3-multi-agent/
    │   └── exercise3-research-team.py
    ├── module4-production/
    │   ├── exercise4-multi-provider.py
    │   └── exercise4-multi-provider-CORRECTED.py
    ├── module5-advanced/
    │   └── exercise5-a2a-preview.py
    └── module6-deployment/
        └── exercise6-lambda-deployment.py
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

### Core Strands SDK
```bash
pip install strands-agents
```

### Provider-Specific Dependencies
```bash
# For OpenAI integration
pip install 'strands-agents[openai]'

# For NVIDIA NIM and OpenRouter
pip install 'strands-agents[litellm]'

# For tools
pip install strands-agents-tools
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

- **AWS Strands SDK**: Model-driven agent framework
- **Amazon Bedrock**: Enterprise LLM service (Claude 3.7 Sonnet)
- **OpenAI**: GPT-4 models for comparison
- **NVIDIA NIM**: GPU-accelerated inference
- **OpenRouter**: Cost-effective model gateway
- **AWS Lambda**: Serverless deployment

## 🎓 Workshop Flow

Each module builds on the previous one:
1. **Single Agent** → Learn core concepts
2. **Tools** → Extend capabilities  
3. **Multi-Agent** → Orchestration patterns
4. **Multi-Provider** → Production resilience
5. **A2A Protocol** → Interoperability
6. **Deployment** → Production ready

## 🆘 Troubleshooting

### Common Issues
- **ModuleNotFoundError**: Install missing dependencies
- **AWS Credentials**: Run `aws configure`
- **Bedrock Access**: Enable models in console
- **API Keys**: Check environment variables

### Getting Help
- Check `WORKSHOP_PLAN.md` for detailed instructions
- Use setup verification scripts
- Ask instructor during workshop

## 📖 Additional Resources

- [AWS Strands SDK Documentation](https://strandsagents.com/)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [A2A Protocol Documentation](https://github.com/a2aproject/A2A)

---

**Ready to build production AI agents? Let's get started! 🚀**

