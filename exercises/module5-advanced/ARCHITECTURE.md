# A2A Research Team Architecture - Production Implementation

This document describes the **production-ready** architecture of the A2A (Agent-to-Agent) multi-agent research system using the Strands Agents SDK, incorporating current best practices and acknowledging the experimental nature of A2A support.

## ⚠️ **IMPORTANT: Experimental Feature Warning**

**From Official Strands Documentation:**

> **"A2A support in Strands is currently EXPERIMENTAL. APIs may change, and additional functionality will be added in future releases. If you encounter bugs or have feature requests, please report them on GitHub."**

### Implications for This Implementation:
- **API Stability**: The A2A interfaces may undergo breaking changes in future SDK releases
- **Production Readiness**: While functional, this implementation should be considered experimental
- **Evolution**: The Strands project is continuously evolving, and A2A patterns may change significantly
- **Feedback Loop**: Users are encouraged to report issues and contribute to the development process

## ✅ Current Implementation Status

**WORKING WITH EXPERIMENTAL COMPONENTS**: All components are functional but subject to change:

| Component | Status | Stability Level | Notes |
|-----------|--------|-----------------|-------|
| `A2AServer` | ✅ **Working** | Experimental | HTTP servers exposing Strands agents via A2A protocol |
| `StrandsA2AExecutor` | ✅ **Working** | Experimental | Handles agent execution in A2A context |
| `A2AClient` | ✅ **Working** | Stable | Official client from a2a-sdk package |
| `A2ACardResolver` | ✅ **Working** | Stable | Service discovery via Agent Cards |
| Security | ✅ **Secure** | Production | No hardcoded credentials, uses AWS configuration |
| Testing | ✅ **Complete** | Production | Individual and integration testing available |

## System Architecture Overview

The system implements a distributed multi-agent architecture following **current A2A best practices** while acknowledging experimental limitations:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    A2A Research Team System (Experimental)                  │
│                        Built with Strands SDK 0.2.1                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    HTTP/JSON-RPC 2.0    ┌─────────────────┐
│   Orchestrator  │◄─────────────────────────│ Research Agent  │
│     Client      │      (A2A Protocol)      │ A2AServer:9001  │
│  (A2AClient)    │                          │ + Bedrock       │
└─────────────────┘                          └─────────────────┘
         │                                            │
         │ Service Discovery                          │ StrandsA2AExecutor
         │ /.well-known/agent.json                    ▼
         │                                   ┌─────────────────┐
         │                                   │ Claude 3.7      │
         │                                   │ Sonnet Model    │
         │                                   └─────────────────┘
         │
         ├─────────────────────────────────► ┌─────────────────┐
         │        Parallel A2A Calls         │ Analysis Agent  │
         │                                   │ A2AServer:9002  │
         │                                   │ + Bedrock       │
         │                                   └─────────────────┘
         │
         ├─────────────────────────────────► ┌─────────────────┐
         │                                   │ Fact-Check      │
         │                                   │ A2AServer:9003  │
         │                                   │ + Bedrock       │
         │                                   └─────────────────┘
         │
         └─────────────────────────────────► ┌─────────────────┐
                                             │ QA Agent        │
                                             │ A2AServer:9004  │
                                             │ + Bedrock       │
                                             └─────────────────┘
```

## A2A Protocol Implementation - Current Best Practices

### 1. A2AServer Implementation (Experimental Component)

**Current Implementation Pattern:**
```python
from strands.multiagent.a2a import A2AServer

# Best Practice: Defensive initialization with error handling
try:
    a2a_server = A2AServer(
        agent=strands_agent,           # Required: Strands Agent instance
        host="localhost",              # Explicit host specification
        port=9001,                     # Unique port per agent
        version="0.0.1"                # Version for compatibility tracking
    )
    
    # Verify server creation before starting
    agent_card = a2a_server.public_agent_card
    logger.info(f"Agent card generated: {agent_card.name}")
    
    # Start server with proper error handling
    a2a_server.serve()
    
except Exception as e:
    logger.error(f"A2AServer initialization failed: {e}")
    # Implement fallback or graceful degradation
```

**Available Methods (Subject to Change):**
- `serve()` - Start the HTTP server (blocking)
- `public_agent_card` - Get the agent card metadata
- `to_fastapi_app()` - Convert to FastAPI app (experimental)
- `to_starlette_app()` - Convert to Starlette app (experimental)

### 2. Agent Card Standards (Stable Component)

Each A2AServer exposes standardized metadata at `/.well-known/agent.json`:

```json
{
  "name": "ResearchSpecialist",
  "description": "A specialized research agent that performs comprehensive web research and analysis",
  "version": "0.0.1",
  "protocolVersion": "0.2.5",
  "url": "http://localhost:9001/",
  "capabilities": {},
  "skills": [],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"]
}
```

**Best Practice**: Always include comprehensive descriptions and version information for forward compatibility.

### 3. A2A Client Communication (Stable Component)

**Recommended Implementation Pattern:**
```python
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import MessageSendParams, SendMessageRequest
import httpx
from uuid import uuid4

async def communicate_with_agent(base_url: str, message: str) -> str:
    """
    Best practice A2A client implementation with proper error handling
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as http_client:
            # Service discovery
            resolver = A2ACardResolver(http_client, base_url=base_url)
            agent_card = await resolver.get_agent_card()
            
            # Verify compatibility
            if not agent_card.name:
                raise ValueError("Invalid agent card received")
            
            # Create client
            client = A2AClient(http_client, agent_card)
            
            # Send message with proper structure
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(
                    message={
                        "role": "user",
                        "parts": [{"kind": "text", "text": message}],
                        "messageId": uuid4().hex,
                    }
                ),
            )
            
            response = await client.send_message(request)
            
            # Extract response safely
            if response.result and response.result.message and response.result.message.parts:
                response_text = ""
                for part in response.result.message.parts:
                    if part.kind == "text":
                        response_text += part.text
                return response_text
            else:
                raise ValueError("Empty response from agent")
                
    except Exception as e:
        logger.error(f"A2A communication failed: {e}")
        # Implement retry logic or fallback
        raise
```

## Current Agent Implementations

### Research Specialist (Port 9001)
- **Purpose**: Comprehensive research and analysis
- **Model**: Claude 3.7 Sonnet (temperature: 0.3, region: us-west-2)
- **Capabilities**: Topic analysis, information synthesis, structured reporting
- **A2A Status**: Experimental wrapper around stable Strands agent

### Analysis Specialist (Port 9002)  
- **Purpose**: Deep data analysis and insights
- **Model**: Claude 3.7 Sonnet (temperature: 0.3, region: us-west-2)
- **Capabilities**: Pattern identification, strategic analysis, recommendations
- **A2A Status**: Experimental wrapper around stable Strands agent

### Fact-Check Specialist (Port 9003)
- **Purpose**: Information verification and accuracy assessment
- **Model**: Claude 3.7 Sonnet (temperature: 0.2, region: us-west-2)
- **Capabilities**: Claim verification, source assessment, accuracy reporting
- **A2A Status**: Experimental wrapper around stable Strands agent

### QA Specialist (Port 9004)
- **Purpose**: Quality assurance and validation
- **Model**: Claude 3.7 Sonnet (temperature: 0.2, region: us-west-2)
- **Capabilities**: Quality assessment, gap identification, improvement recommendations
- **A2A Status**: Experimental wrapper around stable Strands agent

## Best Practices for Experimental A2A Implementation

### 1. **Defensive Programming**
```python
# Always wrap A2A operations in try-catch blocks
try:
    server = A2AServer(agent=agent, host="localhost", port=port)
    logger.info("✅ A2AServer created successfully")
except Exception as e:
    logger.error(f"❌ A2AServer creation failed: {e}")
    # Implement fallback or graceful degradation
```

### 2. **Version Pinning**
```bash
# Pin specific versions to avoid breaking changes
pip install strands-agents==0.2.1 a2a-sdk==0.2.11
```

### 3. **Comprehensive Logging**
```python
# Log all A2A interactions for debugging
logger.info(f"Sending A2A message to {agent_name}: {message[:100]}...")
response = await client.send_message(request)
logger.info(f"Received A2A response from {agent_name}: {len(response_text)} chars")
```

### 4. **Graceful Degradation**
```python
# Implement fallbacks for A2A failures
try:
    result = await a2a_communication(agent_url, message)
except Exception as e:
    logger.warning(f"A2A failed, using local fallback: {e}")
    result = local_agent_fallback(message)
```

### 5. **Testing Strategy**
- **Unit Tests**: Test individual agent creation and A2AServer initialization
- **Integration Tests**: Test A2A communication between agents
- **Regression Tests**: Verify compatibility after SDK updates
- **Fallback Tests**: Ensure graceful degradation when A2A fails

## Evolution Considerations

### Expected Changes in Future Releases:
1. **API Modifications**: Method signatures and class interfaces may change
2. **Protocol Updates**: Message formats and communication patterns may evolve
3. **Security Enhancements**: Authentication and encryption may become mandatory
4. **Performance Improvements**: Connection pooling and streaming may be added

### Migration Strategy:
1. **Monitor Releases**: Track Strands SDK release notes for A2A changes
2. **Maintain Compatibility Layers**: Abstract A2A interactions behind interfaces
3. **Implement Feature Flags**: Allow switching between A2A and fallback modes
4. **Contribute Feedback**: Report issues and feature requests to help shape development

## File Structure (Current Implementation)

```
src/
├── research_agent_server.py       # Research specialist A2A server (experimental)
├── analysis_agent_server.py       # Analysis specialist A2A server (experimental)
├── factcheck_agent_server.py      # Fact-check specialist A2A server (experimental)
├── qa_agent_server.py             # QA specialist A2A server (experimental)
└── orchestrator_client.py         # Multi-agent orchestrator (stable client)

Root Files:
├── main.py                        # Interactive entry point
├── start_all_agents.py           # Server management
├── test_individual_agents.py     # Testing infrastructure
├── README.md                     # Usage documentation
└── ARCHITECTURE.md               # This file
```

## Security Considerations (Production-Ready)

- ✅ **No Hardcoded Credentials**: Uses AWS configuration (`aws configure`)
- ✅ **Secure Communication**: HTTP-based with proper error handling
- ✅ **Input Validation**: Proper message format validation
- ✅ **Resource Management**: Proper connection and resource cleanup
- ⚠️ **A2A Security**: Limited by experimental status of A2A components

## Performance Characteristics

- **Startup Time**: ~5-10 seconds per agent server
- **Response Time**: Varies by task complexity (typically 10-60 seconds)
- **Concurrency**: Each agent can handle multiple concurrent requests
- **Scalability**: Agents can be deployed on separate machines/containers
- **Reliability**: Subject to experimental A2A component stability

## Technology Stack

- **Strands Agents SDK 0.2.1**: Core agent framework with experimental A2A support
- **A2A SDK 0.2.11**: Official Agent-to-Agent protocol implementation (stable)
- **Amazon Bedrock**: Claude 3.7 Sonnet for LLM capabilities (production)
- **HTTP/JSON-RPC 2.0**: Transport protocol for agent communication (standard)
- **Python AsyncIO**: Asynchronous orchestration and communication (stable)
- **HTTPX**: HTTP client library for A2A communication (stable)

## Key Architectural Benefits and Limitations

### Benefits:
1. **Standards Compliance**: Follows official A2A protocol specification
2. **Service Discovery**: Automatic agent discovery via Agent Cards
3. **Interoperability**: Compatible with other A2A-compliant systems
4. **Modular Design**: Each agent runs independently

### Limitations (Due to Experimental Status):
1. **API Instability**: Interfaces may change without notice
2. **Limited Support**: Experimental features have limited documentation
3. **Breaking Changes**: Updates may require code modifications
4. **Production Risk**: Not recommended for critical production systems

## Recommendations for Users

### For Development:
- ✅ Use for prototyping and experimentation
- ✅ Implement comprehensive error handling
- ✅ Pin dependency versions
- ✅ Maintain fallback mechanisms

### For Production:
- ⚠️ Use with caution and extensive testing
- ✅ Implement monitoring and alerting
- ✅ Have rollback plans ready
- ✅ Consider alternative patterns for critical systems

---

**Architecture Status**: ⚠️ **Experimental but Functional** - Complete A2A implementation using experimental Strands components with production-ready patterns and defensive programming practices.

**Evolution Note**: This implementation will evolve alongside the Strands Agents SDK. Users should expect periodic updates and potential breaking changes as the A2A support matures from experimental to stable status.
