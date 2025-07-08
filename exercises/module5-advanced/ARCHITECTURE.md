# Module 5: A2A Preview - Architecture

## Overview
This module demonstrates the A2A (Agent-to-Agent) protocol with a subprocess-based architecture where agents run as independent processes and communicate via the standard A2A SDK protocol.

## Architecture Diagram

```mermaid
graph TB
    User[👤 User Request] --> MainProcess[🚀 Main Process<br/>main.py]
    MainProcess --> |subprocess.Popen| ResearchProcess[🔬 Research Agent<br/>research_agent.py]
    MainProcess --> |subprocess.Popen| AnalysisProcess[📊 Analysis Agent<br/>analysis_agent.py]
    MainProcess --> |subprocess.Popen| FactCheckProcess[✅ Fact-Check Agent<br/>factcheck_agent.py]
    MainProcess --> |subprocess.Popen| QAProcess[⭐ QA Agent<br/>qa_agent.py]
    MainProcess --> |subprocess.Popen| OrchestratorProcess[🎯 Orchestrator Agent<br/>orchestrator.py]
    
    MainProcess --> |a2a.discover()| A2ADiscovery[🔍 A2A Agent Discovery]
    A2ADiscovery --> OrchestratorProxy[📞 Orchestrator Proxy<br/>Remote Method Calls]
    
    OrchestratorProxy --> |A2A Protocol| ResearchAgent[ResearchSpecialist]
    OrchestratorProxy --> |A2A Protocol| AnalysisAgent[AnalysisSpecialist]
    OrchestratorProxy --> |A2A Protocol| FactCheckAgent[FactCheckSpecialist]
    OrchestratorProxy --> |A2A Protocol| QAAgent[QualityAssuranceSpecialist]
    
    ResearchAgent --> MCPDocker1[🐳 DuckDuckGo MCP<br/>Docker Container]
    FactCheckAgent --> MCPDocker2[🐳 DuckDuckGo MCP<br/>Docker Container]
    
    ResearchAgent --> Bedrock1[☁️ AWS Bedrock<br/>Claude 3.7 Sonnet]
    AnalysisAgent --> Bedrock2[☁️ AWS Bedrock<br/>Claude 3.7 Sonnet]
    FactCheckAgent --> Bedrock3[☁️ AWS Bedrock<br/>Claude 3.7 Sonnet]
    QAAgent --> Bedrock4[☁️ AWS Bedrock<br/>Claude 3.7 Sonnet]
    OrchestratorProcess --> Bedrock5[☁️ AWS Bedrock<br/>Claude 3.7 Sonnet]
    
    OrchestratorProxy --> Results[📋 Aggregated Results]
    Results --> MainProcess
    MainProcess --> User
    
    subgraph "Independent Agent Processes"
        ResearchProcess
        AnalysisProcess
        FactCheckProcess
        QAProcess
        OrchestratorProcess
    end
    
    subgraph "A2A Communication Layer"
        A2ADiscovery
        OrchestratorProxy
        ResearchAgent
        AnalysisAgent
        FactCheckAgent
        QAAgent
    end
    
    subgraph "External Tools & Services"
        MCPDocker1
        MCPDocker2
        Bedrock1
        Bedrock2
        Bedrock3
        Bedrock4
        Bedrock5
    end
    
    style User fill:#e1f5fe
    style MainProcess fill:#f3e5f5
    style OrchestratorProcess fill:#e8f5e8
    style ResearchProcess fill:#fff3e0
    style AnalysisProcess fill:#fce4ec
    style FactCheckProcess fill:#e3f2fd
    style QAProcess fill:#f1f8e9
    style A2ADiscovery fill:#f9fbe7
    style OrchestratorProxy fill:#e8f5e8
```

## Key Components

### 1. Main Process Entry Point
```python
# main.py
import subprocess
import time
from strands.multiagent import a2a
import logging

def run_a2a_research_team(topic: str):
    """
    Starts all A2A agent processes, orchestrates a research task,
    and then terminates the agent processes.
    """
    processes = []
    try:
        logger.info("Starting A2A agent processes...")
        # Start each agent in a separate subprocess
        processes.append(subprocess.Popen(["python3", "research_agent.py"], cwd="./src"))
        processes.append(subprocess.Popen(["python3", "analysis_agent.py"], cwd="./src"))
        processes.append(subprocess.Popen(["python3", "factcheck_agent.py"], cwd="./src"))
        processes.append(subprocess.Popen(["python3", "qa_agent.py"], cwd="./src"))
        processes.append(subprocess.Popen(["python3", "orchestrator.py"], cwd="./src"))

        # Wait for agents to initialize
        time.sleep(15)

        # Discover the Orchestrator agent via A2A
        orchestrator = a2a.discover("ResearchOrchestrator")

        # Call the Orchestrator agent to conduct research
        result = orchestrator(topic)
        print(result)

    except Exception as e:
        logger.error(f"An error occurred during A2A research: {e}")
    finally:
        # Terminate all subprocesses
        for process in processes:
            if process.poll() is None:
                process.terminate()
                process.wait()
```

### 2. Orchestrator Agent
```python
# src/orchestrator.py
from strands import Agent
from strands.multiagent import a2a
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

orchestrator = Agent(
    name="ResearchOrchestrator",
    model=model,
    system_prompt="""You are a Research Orchestrator managing a team of specialist agents.
    You have access to these specialist agents:
    - ResearchSpecialist: Performs web research using DuckDuckGo search
    - AnalysisSpecialist: Analyzes research data using sequential thinking
    - FactCheckSpecialist: Fact-checks claims using DuckDuckGo search
    - QualityAssuranceSpecialist: Assesses research quality and completeness

    Your coordination strategy:
    1. For any research request, use ResearchSpecialist to gather information.
    2. Use AnalysisSpecialist to process and synthesize the research data.
    3. For complex topics, use FactCheckSpecialist to verify key claims.
    4. Use QualityAssuranceSpecialist to ensure research meets high standards.
    5. Coordinate intelligently based on the complexity and requirements.

    You will communicate with these agents using the A2A protocol.
    """
)

if __name__ == "__main__":
    # Start the A2A listener for the orchestrator agent
    a2a.listen(agent=orchestrator)
```

### 3. Research Agent
```python
# src/research_agent.py
from strands import Agent
from strands.multiagent import a2a
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

# Setup MCP client for DuckDuckGo search
duckduckgo_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="docker",
        args=["run", "-i", "--rm", "mcp/duckduckgo"]
    )
))

research_agent = Agent(
    name="ResearchSpecialist",
    model=model,
    system_prompt="""You are a specialized Research Agent.
    Your expertise is to perform web research using the DuckDuckGo search tool.
    You will be given a topic and you need to return a comprehensive research finding with source attribution.""",
    tools=duckduckgo_client.list_tools_sync()
)

if __name__ == "__main__":
    a2a.listen(agent=research_agent)
```

### 4. Analysis Agent
```python
# src/analysis_agent.py
from strands import Agent
from strands.multiagent import a2a
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

# Setup MCP client for sequential thinking
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="docker",
        args=["run", "-i", "--rm", "mcp/sequentialthinking"]
    )
))

analysis_agent = Agent(
    name="AnalysisSpecialist",
    model=model,
    system_prompt="""You are a specialized Analysis Agent.
    Your expertise is to analyze research data and extract key insights.
    You will use sequential thinking to provide structured analysis.""",
    tools=mcp_client.list_tools_sync()
)

if __name__ == "__main__":
    a2a.listen(agent=analysis_agent)
```

### 5. Fact-Check Agent
```python
# src/factcheck_agent.py
from strands import Agent
from strands.multiagent import a2a
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

# Setup MCP client for DuckDuckGo search
duckduckgo_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="docker",
        args=["run", "-i", "--rm", "mcp/duckduckgo"]
    )
))

factcheck_agent = Agent(
    name="FactCheckSpecialist",
    model=model,
    system_prompt="""You are a specialized Fact-Checking Agent.
    Your expertise is to verify claims using web search and provide accuracy assessments.""",
    tools=duckduckgo_client.list_tools_sync()
)

if __name__ == "__main__":
    a2a.listen(agent=factcheck_agent)
```

### 6. Quality Assurance Agent
```python
# src/qa_agent.py
from strands import Agent
from strands.multiagent import a2a
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3
)

qa_agent = Agent(
    name="QualityAssuranceSpecialist",
    model=model,
    system_prompt="""You are a specialized Quality Assurance Agent.
    Your expertise is to assess the quality and completeness of research work.
    You ensure high standards and identify areas for improvement."""
)

if __name__ == "__main__":
    a2a.listen(agent=qa_agent)
```

## A2A Protocol Implementation

### Agent Discovery Pattern
```python
# Main process discovers agents using A2A
orchestrator = a2a.discover("ResearchOrchestrator")

# Direct method invocation on remote agent
result = orchestrator(research_topic)
```

### Agent Registration Pattern
```python
# Each agent registers itself with A2A listener
if __name__ == "__main__":
    a2a.listen(agent=agent_instance)
```

### Communication Flow
1. **Process Launch**: Main process starts all agent subprocesses using `subprocess.Popen`
2. **Agent Registration**: Each agent calls `a2a.listen()` to register with A2A protocol
3. **Discovery**: Main process uses `a2a.discover()` to find the orchestrator
4. **Remote Invocation**: Main process calls orchestrator methods via A2A proxy
5. **Inter-Agent Communication**: Orchestrator coordinates with specialist agents via A2A
6. **Process Cleanup**: Main process terminates all subprocesses on completion

## Dependencies and Installation

### Required Packages
```bash
pip install strands-agents[a2a]  # Core SDK with A2A support
pip install a2a-sdk[sql]         # A2A SDK with database support
pip install mcp[cli]             # Model Context Protocol
```

### Docker Requirements
- Docker engine for MCP tool containers
- `mcp/duckduckgo` image for web search
- `mcp/sequentialthinking` image for structured analysis

### AWS Configuration
- AWS Bedrock access with Claude 3.7 Sonnet enabled
- Proper AWS credentials configured
- US region access for Bedrock

## Error Handling & Resilience

### Process Management
```python
try:
    # Start agent processes
    processes = []
    for agent_script in agent_scripts:
        process = subprocess.Popen(["python3", agent_script], cwd="./src")
        processes.append(process)
    
    # Agent discovery and execution
    orchestrator = a2a.discover("ResearchOrchestrator")
    result = orchestrator(topic)
    
except Exception as e:
    logger.error(f"A2A research failed: {e}")
finally:
    # Ensure all processes are terminated
    for process in processes:
        if process.poll() is None:
            process.terminate()
            process.wait()
```

### Timeout Handling
- 15-second initialization wait for agent startup
- Graceful process termination on completion or error
- Process health checking with `poll()`

## Performance Considerations

### Resource Optimization
- **Shared Model Instances**: Single Bedrock model per agent to reduce memory
- **Process Isolation**: Each agent runs in separate subprocess for stability
- **Docker Caching**: MCP containers benefit from Docker layer caching

### Scalability Patterns
- **Horizontal Scaling**: Multiple instances of specialist agents
- **Load Distribution**: Different topics can be processed in parallel
- **Resource Pooling**: Docker containers can be reused across requests

## Production Deployment

### Container Deployment
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY main.py .
COPY src/ ./src/

# Ensure Docker is available for MCP tools
RUN apt-get update && apt-get install -y docker.io

CMD ["python", "main.py"]
```

### Environment Variables
```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# Optional Provider Keys
OPENAI_API_KEY=...
NVIDIA_API_KEY=...
OPENROUTER_API_KEY=...
```

### Monitoring & Observability
- Process-level logging for each agent
- A2A protocol message tracing
- Bedrock API usage monitoring
- Docker container resource tracking

## Security Considerations

### Process Isolation
- Each agent runs in isolated subprocess
- No shared memory between processes
- Docker containers provide additional isolation for tools

### Credential Management
- AWS credentials via environment variables
- No hardcoded API keys in source code
- Secure credential rotation support

### Network Security
- A2A protocol uses localhost communication
- Docker containers run with minimal privileges
- No external network access except for required APIs

## Future Enhancements

### Distributed Deployment
- **Kubernetes**: Deploy agents as separate pods
- **Service Mesh**: Use Istio for service-to-service communication
- **Message Queues**: Replace subprocess with distributed messaging

### Advanced Features
- **Agent Health Monitoring**: Heartbeat and recovery mechanisms
- **Dynamic Scaling**: Auto-scale agents based on workload
- **Circuit Breakers**: Prevent cascading failures in multi-agent chains
- **Distributed Tracing**: Full request tracing across agent boundaries