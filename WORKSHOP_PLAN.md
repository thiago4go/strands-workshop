# AWS Strands Workshop: Complete Organization Plan

## Workshop Overview
**Title**: Building Production AI Agents with AWS Strands SDK  
**Duration**: 3 hours (180 minutes)  
**Format**: Hands-on workshop with live coding  
**Target Audience**: Developers, AI Engineers, Solution Architects

## Learning Objectives
By the end of this workshop, participants will be able to:
1. Build AI agents using the model-driven AWS Strands SDK approach
2. Integrate multiple LLM providers (Bedrock, OpenAI, NVIDIA NIM, OpenRouter)
3. Create custom tools and extend agent capabilities
4. Implement multi-agent orchestration patterns
5. Deploy agents to production using AWS Lambda
6. Understand A2A protocol for agent interoperability

## Workshop Structure (3-Act Journey)

### **Act I: The Single Agent (60 minutes)**
**Goal**: Master individual agent development

#### Module 1: Hello Agent (20 minutes)
- **Learning Outcome**: Create your first working agent
- **Key Concepts**: Model-driven approach, agentic loop
- **Exercise**: `exercise1-hello-agent.py`
- **Status**: ✅ **IMPLEMENTED**

**Instructor Notes**:
- Start with simple Bedrock model
- Explain model-driven vs. workflow-driven approaches
- Show the basic Agent class instantiation
- Demonstrate simple conversation

#### Module 2: Custom Tools (40 minutes)  
- **Learning Outcome**: Extend agent capabilities with tools
- **Key Concepts**: @tool decorator, tool integration patterns
- **Exercise**: `exercise2-custom-tools.py`
- **Status**: ❌ **NEEDS IMPLEMENTATION**

**Instructor Notes**:
- Introduce strands_tools package
- Show calculator, current_time, http_request tools
- Demonstrate custom tool creation
- Explain tool calling patterns

### **Act II: Multi-Agent Orchestration (60 minutes)**
**Goal**: Build collaborative agent systems

#### Module 3: Research Team (30 minutes)
- **Learning Outcome**: Implement agent collaboration
- **Key Concepts**: Orchestrator-worker pattern, task delegation
- **Exercise**: `exercise3-research-team.py`
- **Status**: ❌ **NEEDS IMPLEMENTATION**

**Instructor Notes**:
- Show multi-agent coordination patterns
- Demonstrate task delegation
- Explain agent communication
- Show orchestrator design patterns

#### Module 4: Multi-Provider Production (30 minutes)
- **Learning Outcome**: Production-ready resilient systems
- **Key Concepts**: Provider fallbacks, error handling, OpenAI integration
- **Exercise**: `exercise4-multi-provider-CORRECTED.py`
- **Status**: ✅ **IMPLEMENTED AND TESTED**

**Instructor Notes**:
- Demonstrate all 4 providers: Bedrock, OpenAI, NVIDIA NIM, OpenRouter
- Show fallback patterns and error handling
- Explain production resilience strategies
- Test with real API keys

### **Act III: A2A Protocol & Deployment (60 minutes)**
**Goal**: Production deployment and interoperability

#### Module 5: A2A Preview (30 minutes)
- **Learning Outcome**: Understand agent-to-agent communication
- **Key Concepts**: Agent Cards, A2A protocol, discovery
- **Exercise**: `exercise5-a2a-preview.py`
- **Status**: ❌ **NEEDS IMPLEMENTATION**

**Instructor Notes**:
- Introduce A2A protocol concepts
- Show agent discovery mechanisms
- Demonstrate inter-agent communication
- Explain agent cards and capabilities

#### Module 6: Lambda Deployment (30 minutes)
- **Learning Outcome**: Deploy agents to production
- **Key Concepts**: Serverless deployment, packaging, monitoring
- **Exercise**: `exercise6-lambda-deployment.py`
- **Status**: ❌ **NEEDS IMPLEMENTATION**

**Instructor Notes**:
- Show AWS Lambda packaging
- Demonstrate deployment process
- Explain monitoring and observability
- Show production best practices

## Current Implementation Status

### ✅ Completed Modules
- **Module 1**: Basic hello agent implementation
- **Module 4**: Complete multi-provider implementation with OpenAI integration (tested)

### ❌ Modules Needing Implementation
- **Module 2**: Custom tools integration
- **Module 3**: Multi-agent research team
- **Module 5**: A2A protocol preview
- **Module 6**: Lambda deployment

### 📋 Supporting Materials Status
- ✅ **README.md**: Complete workshop overview and setup
- ✅ **requirements.txt**: All dependencies listed
- ✅ **setup/verify_setup.py**: Complete setup verification
- ✅ **setup/test_providers.py**: Provider testing script
- ✅ **WORKSHOP_PLAN.md**: This instructor guide
- ❌ **Individual module READMEs**: Need creation
- ❌ **Troubleshooting guide**: Need creation

## Pre-Workshop Setup Instructions

### For Participants
1. **Python Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or .venv\Scripts\activate  # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **AWS Configuration**:
   ```bash
   aws configure
   ```

4. **Enable Bedrock Models**:
   - Visit [Bedrock Console](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess)
   - Enable Claude 3.7 Sonnet

5. **Optional API Keys** (create `.env` file):
   ```bash
   OPENAI_API_KEY=sk-...
   NVIDIA_API_KEY=nvapi-...
   OPENROUTER_API_KEY=sk-or-...
   ```

6. **Verify Setup**:
   ```bash
   python setup/verify_setup.py
   python setup/test_providers.py
   ```

### For Instructors
- Test all exercises in clean environment
- Prepare backup API keys for demo
- Have troubleshooting scenarios ready
- Test deployment examples beforehand

## Workshop Timing Guide

### Opening (10 minutes)
- Welcome and introductions
- Workshop overview and objectives
- Quick setup verification

### Act I: Single Agent (60 minutes)
- **0:10-0:30**: Module 1 - Hello Agent (20 min)
- **0:30-1:10**: Module 2 - Custom Tools (40 min)

### Break (10 minutes)
- **1:10-1:20**: Networking and Q&A

### Act II: Multi-Agent (60 minutes)  
- **1:20-1:50**: Module 3 - Research Team (30 min)
- **1:50-2:20**: Module 4 - Multi-Provider (30 min)

### Break (10 minutes)
- **2:20-2:30**: Quick break

### Act III: A2A & Deployment (60 minutes)
- **2:30-3:00**: Module 5 - A2A Preview (30 min)
- **3:00-3:30**: Module 6 - Lambda Deployment (30 min)

### Closing (10 minutes)
- **3:30-3:40**: Wrap-up, next steps, resources

## Troubleshooting Guide

### Common Issues
1. **ModuleNotFoundError**: 
   - Solution: `pip install -r requirements.txt`
   
2. **AWS Credentials Error**:
   - Solution: `aws configure` or check IAM permissions
   
3. **Bedrock Access Denied**:
   - Solution: Enable models in Bedrock console
   
4. **API Key Issues**:
   - Solution: Check .env file format and key validity

### Backup Plans
- If Bedrock fails: Use OpenAI as primary
- If all cloud providers fail: Use local Ollama
- If tools fail: Show manual implementations
- If deployment fails: Show local containerization

## Next Steps for Workshop Completion

### Immediate Priorities (Week 1)
1. Implement Module 2: Custom Tools
2. Implement Module 3: Multi-Agent Research Team
3. Test all existing modules end-to-end

### Medium Term (Week 2)
1. Implement Module 5: A2A Preview
2. Implement Module 6: Lambda Deployment
3. Create individual module documentation

### Final Polish (Week 3)
1. End-to-end workshop testing
2. Instructor training materials
3. Participant feedback collection system
4. Advanced exercises for fast learners

## Success Metrics

### Workshop Completion Criteria
- [ ] All 6 modules implemented and tested
- [ ] Setup verification scripts working
- [ ] End-to-end workshop flow tested
- [ ] Instructor materials complete
- [ ] Troubleshooting documentation ready

### Participant Success Indicators
- Can create basic agents independently
- Can integrate multiple providers
- Can deploy to production
- Understand A2A protocol concepts
- Can troubleshoot common issues

---

**Workshop Status**: 2/6 modules complete, setup infrastructure ready
**Next Action**: Implement Module 2 (Custom Tools)
**Goal**: Master individual agent development

#### Module 1: Basics - Hello Agent (20 minutes)
- **Learning Outcome**: Create first working agent
- **Key Concepts**: Model-driven approach, Agentic loop
- **Exercise**: `exercise1-hello-agent.py`
- **Tools**: Basic agent with Claude 3.7 Sonnet

#### Module 2: Tools - Custom Tools (40 minutes)
- **Learning Outcome**: Extend agent capabilities with tools
- **Key Concepts**: @tool decorator, tool integration patterns
- **Exercise**: `exercise2-custom-tools.py`
- **Tools**: Calculator, current_time, python_repl, custom letter_counter

### **Act II: Multi-Agent Orchestration (60 minutes)**
**Goal**: Build collaborative agent systems

#### Module 3: Multi-Agent - Research Team (30 minutes)
- **Learning Outcome**: Implement agent collaboration
- **Key Concepts**: Orchestrator-worker pattern, task delegation
- **Exercise**: `exercise3-research-team.py`
- **Tools**: Specialized agents working together

#### Module 4: Production - Multi-Provider (30 minutes)
- **Learning Outcome**: Production-ready resilient systems
- **Key Concepts**: Provider fallbacks, error handling
- **Exercise**: `exercise4-multi-provider.py`
- **Tools**: NVIDIA NIM, OpenRouter integration

### **Act III: A2A Protocol & Deployment (60 minutes)**
**Goal**: Production deployment and interoperability

#### Module 5: Advanced - A2A Preview (30 minutes)
- **Learning Outcome**: Understand agent-to-agent communication
- **Key Concepts**: Agent Cards, A2A protocol, discovery
- **Exercise**: `exercise5-a2a-preview.py`
- **Tools**: A2A client/server implementation

#### Module 6: Deployment - Lambda Deployment (30 minutes)
- **Learning Outcome**: Deploy to production
- **Key Concepts**: Serverless deployment, packaging, monitoring
- **Exercise**: `exercise6-lambda-deployment.py`
- **Tools**: AWS Lambda, CloudWatch

## Pre-Workshop Setup Requirements

### Environment Setup
```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install strands-agents strands-agents-tools boto3

# 3. Configure AWS credentials
aws configure
# OR set environment variables

# 4. Get API keys for alternative providers
# - NVIDIA NIM: https://build.nvidia.com/
# - OpenRouter: https://openrouter.ai/
```

### Required AWS Services
- Amazon Bedrock (Claude 3.7 Sonnet enabled)
- AWS Lambda
- CloudWatch (for monitoring)

## Workshop Materials Structure

```
strands-workshop/
├── README.md                    # Workshop overview and setup
├── setup/
│   ├── verify_setup.py         # Environment verification
│   └── troubleshooting.md      # Common issues and solutions
├── exercises/
│   ├── module1-basics/
│   │   ├── exercise1-hello-agent.py
│   │   └── solutions/
│   ├── module2-tools/
│   │   ├── exercise2-custom-tools.py
│   │   └── solutions/
│   ├── module3-multi-agent/
│   │   ├── exercise3-research-team.py
│   │   └── solutions/
│   ├── module4-production/
│   │   ├── exercise4-multi-provider.py
│   │   └── solutions/
│   ├── module5-advanced/
│   │   ├── exercise5-a2a-preview.py
│   │   └── solutions/
│   └── module6-deployment/
│       ├── exercise6-lambda-deployment.py
│       └── solutions/
├── docs/
│   ├── instructor-guide.md     # Detailed teaching notes
│   ├── participant-guide.md    # Participant reference
│   └── troubleshooting.md      # Common issues
└── resources/
    ├── slides/                 # Presentation materials
    ├── templates/              # Code templates
    └── examples/               # Additional examples
```

## Instructor Preparation Checklist

### 2 Weeks Before
- [ ] Test all exercises in clean environment
- [ ] Verify AWS account setup and permissions
- [ ] Prepare backup environments for common issues
- [ ] Create presentation slides
- [ ] Set up demo environments

### 1 Week Before
- [ ] Send pre-workshop setup instructions to participants
- [ ] Prepare troubleshooting guide
- [ ] Test alternative provider integrations
- [ ] Prepare solution files
- [ ] Set up monitoring for workshop environment

### Day of Workshop
- [ ] Verify all demo environments work
- [ ] Have backup API keys ready
- [ ] Prepare troubleshooting support
- [ ] Set up screen sharing and recording
- [ ] Have contact information for technical support

## Success Metrics

### Immediate (End of Workshop)
- [ ] 90%+ participants complete Module 1-2 successfully
- [ ] 80%+ participants complete Module 3-4 successfully  
- [ ] 70%+ participants complete Module 5-6 successfully
- [ ] Positive feedback on hands-on approach
- [ ] Clear understanding of production deployment

### Follow-up (1 Week Later)
- [ ] Participants can reproduce exercises independently
- [ ] Questions answered in community forum
- [ ] Participants share their own agent implementations
- [ ] Interest in advanced workshops

## Next Steps for Development

### Priority 1: Core Content
1. Complete all exercise files with working code
2. Create comprehensive solution files
3. Develop instructor guide with timing and tips
4. Create troubleshooting documentation

### Priority 2: Supporting Materials
1. Presentation slides for each module
2. Participant reference guide
3. Setup verification scripts
4. Common issues documentation

### Priority 3: Advanced Features
1. Additional example implementations
2. Integration with other AWS services
3. Advanced A2A protocol examples
4. Performance optimization guides

## Community and Follow-up

### Resources for Continued Learning
- Strands Documentation: https://strandsagents.com
- GitHub Repository: https://github.com/strands-agents
- Community Discord/Forum
- Monthly follow-up sessions

### Advanced Workshop Ideas
- Multi-modal agents with vision/audio
- Enterprise integration patterns
- Custom model provider development
- Advanced A2A protocol implementations
