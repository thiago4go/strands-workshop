# Exercise 5: A2A Research Team - Decoupled Multi-Agent Orchestration

This directory contains a complete implementation of a multi-agent research team using the A2A (Agent-to-Agent) protocol with Strands Agents SDK. Each agent runs as an independent A2A server and communicates via HTTP using the standardized A2A protocol.

## ✅ Implementation Status

**WORKING**: This implementation uses the correct Strands A2A components:

- ✅ **A2AServer**: Available and working for creating A2A-compatible servers
- ✅ **StrandsA2AExecutor**: Available for executing agent logic in A2A context  
- ✅ **Security**: No hardcoded credentials - uses proper AWS configuration
- ✅ **All Agent Servers**: Updated to use A2AServer (correct implementation)
- ✅ **Orchestrator Client**: Working A2A client using official a2a-sdk
- ✅ **Testing Infrastructure**: Complete testing and management tools

## Architecture

The implementation follows the official A2A protocol specification:

```
┌─────────────────┐    HTTP/A2A     ┌─────────────────┐
│   Orchestrator  │◄──────────────► │ A2AServer       │
│     Client      │                 │ (Research)      │
│  (A2AClient)    │                 │ Port 9001       │
└─────────────────┘                 └─────────────────┘
         │                                   │
         │ HTTP/A2A                         │ StrandsA2AExecutor
         ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│ A2AServer       │                 │ Strands Agent   │
│ (Analysis)      │                 │ + Bedrock Model │
│ Port 9002       │                 └─────────────────┘
└─────────────────┘                          
         │                          
         │ HTTP/A2A                 
         ▼                          
┌─────────────────┐    HTTP/A2A     ┌─────────────────┐
│ A2AServer       │◄──────────────► │ A2AServer       │
│ (Fact-check)    │                 │ (QA)            │
│ Port 9003       │                 │ Port 9004       │
└─────────────────┘                 └─────────────────┘
```

## File Structure

```
module5-advanced/
├── README.md                          # This documentation
├── ARCHITECTURE.md                    # Detailed architecture guide
├── main.py                           # Interactive main entry point
├── start_all_agents.py               # Server management script
├── test_individual_agents.py         # Individual agent testing
└── src/                              # Agent implementations
    ├── research_agent_server.py       # Research specialist A2A server
    ├── analysis_agent_server.py       # Analysis specialist A2A server
    ├── factcheck_agent_server.py      # Fact-check specialist A2A server
    ├── qa_agent_server.py             # QA specialist A2A server
    └── orchestrator_client.py         # Multi-agent orchestrator
```

## Prerequisites

1. **AWS Configuration**:
   ```bash
   aws configure
   # Ensure Claude 3.7 Sonnet is enabled in Bedrock console
   ```

2. **Dependencies**:
   ```bash
   pip install 'strands-agents[a2a]' 'a2a-sdk[sqlite]' strands-agents-tools
   ```

3. **Verification**:
   ```bash
   aws sts get-caller-identity  # Check AWS access
   ```

## Quick Start

### Option 1: Interactive Menu (Recommended)
```bash
python3 main.py
```
Choose from the menu:
1. 🚀 Start All Agent Servers
2. 🧪 Test Individual Agents  
3. 🎯 Run Research Orchestrator
4. 📖 View Documentation

### Option 2: Manual Steps

1. **Start Agent Servers**:
   ```bash
   python3 start_all_agents.py
   ```

2. **Test Individual Agents** (in another terminal):
   ```bash
   python3 test_individual_agents.py
   ```

3. **Run Full Orchestration** (in another terminal):
   ```bash
   python3 src/orchestrator_client.py
   ```

## Available Agents

| Agent | Port | Description | Endpoint |
|-------|------|-------------|----------|
| Research Specialist | 9001 | Comprehensive research and analysis | http://localhost:9001 |
| Analysis Specialist | 9002 | Deep data analysis and insights | http://localhost:9002 |
| Fact-Check Specialist | 9003 | Information verification | http://localhost:9003 |
| QA Specialist | 9004 | Quality assurance and validation | http://localhost:9004 |

Each agent exposes an Agent Card at `/.well-known/agent.json` for service discovery.

## A2A Protocol Implementation

### Core Components Used:
- **A2AServer**: Creates HTTP servers that expose Strands agents via A2A protocol
- **StrandsA2AExecutor**: Handles execution of agent logic within A2A context
- **A2AClient**: Official client for communicating with A2A servers
- **A2ACardResolver**: Service discovery via Agent Cards

### Communication Flow:
1. **Service Discovery**: Orchestrator discovers agents via Agent Cards
2. **Message Sending**: JSON-RPC 2.0 messages sent over HTTP
3. **Task Execution**: Agents process tasks using Strands + Bedrock
4. **Response Handling**: Results returned via A2A protocol

## Example Usage

The orchestrator will conduct comprehensive research on a topic using all agents:

1. **Research Phase**: Initial comprehensive research
2. **Analysis Phase**: Deep analysis of research findings  
3. **Fact-Check Phase**: Verification of claims and information
4. **QA Phase**: Quality assessment of the entire research

Final report is saved as `research_report.md`.

## Troubleshooting

### Common Issues:
- **Connection Errors**: Ensure agent servers are running first
- **AWS Errors**: Check `aws configure` and Bedrock model access
- **Import Errors**: Verify all dependencies are installed
- **Port Conflicts**: Check if ports 9001-9004 are available

### Debug Commands:
```bash
# Check agent cards
curl http://localhost:9001/.well-known/agent.json

# Test AWS access
aws sts get-caller-identity

# Check dependencies
pip list | grep -E "(strands|a2a)"
```

## Key Features

- ✅ **True A2A Protocol**: Standards-compliant implementation
- ✅ **Decoupled Architecture**: Each agent runs independently
- ✅ **Service Discovery**: Automatic agent discovery via Agent Cards
- ✅ **Production Ready**: Proper error handling and logging
- ✅ **Secure**: No hardcoded credentials, uses AWS configuration
- ✅ **Comprehensive Testing**: Individual and integration testing
- ✅ **User Friendly**: Interactive menu system

## Technology Stack

- **Strands Agents SDK**: Core agent framework with A2A support
- **Amazon Bedrock**: Claude 3.7 Sonnet for LLM capabilities
- **A2A SDK**: Official Agent-to-Agent protocol implementation
- **HTTP/JSON-RPC 2.0**: Transport protocol for agent communication
- **Python AsyncIO**: Asynchronous orchestration and communication

---

**Status**: ✅ **Production Ready** - Complete A2A implementation with working multi-agent orchestration
