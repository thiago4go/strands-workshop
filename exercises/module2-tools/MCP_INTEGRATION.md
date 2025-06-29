# Module 2 Extra: MCP Integration - Connecting to External Services

## What is Model Context Protocol (MCP)?

The Model Context Protocol (MCP) is an open standard that enables AI agents to connect to external tools and services through a unified interface. Think of it as "USB-C for AI agents" - one protocol that works with any compatible service.

### Why Use MCP?

**Before MCP**: Custom integration for each service
```python
# Different APIs, different patterns, lots of code
weather_api = WeatherAPI(api_key="...")
database = DatabaseConnector(host="...")
file_system = FileManager(path="...")
```

**With MCP**: One standard interface for everything
```python
# Single pattern, minimal code
mcp_client = MCPClient(lambda: stdio_client(...))
with mcp_client:
    tools = mcp_client.list_tools_sync()  # Auto-discover all capabilities
    agent = Agent(tools=tools)  # Ready to use!
```

## Prerequisites

- Completed Module 2 (Custom Tools)
- Additional packages: `pip install "mcp[cli]"`
- Understanding of client-server architecture

## Step-by-Step Tutorial

### Step 1: Understanding MCP Architecture

```
┌─────────────────┐    MCP Protocol    ┌─────────────────┐
│  Strands Agent  │ ◄─────────────────► │   MCP Server    │
│   (MCP Client)  │                    │  (External Tool)│
└─────────────────┘                    └─────────────────┘
```

- **MCP Server**: Exposes tools (calculator, database, API, etc.)
- **MCP Client**: Connects to servers and uses their tools
- **Protocol**: Standardized communication (JSON-RPC over various transports)

### Step 2: Run the Working MCP Demo

The workshop includes a complete, working MCP integration example:

```bash
python exercise2-mcp-integration.py
```

**What You'll See:**
```
🌟 Working MCP Integration Demo
============================================================
This demo shows:
• MCP server with calculator and quiz tools
• Strands agent connecting via stdio transport
• Real-time tool discovery and execution
• Stateful quiz interactions
============================================================

🎯 Testing 7 scenarios:
============================================================

1. 💬 User: Calculate 15 + 23
   🤖 Agent: The sum of 15 + 23 is 38.

2. 💬 User: What is 7 multiplied by 8?
   🤖 Agent: The result of 7 multiplied by 8 is 56.

4. 💬 User: Start a Python quiz for me
   🤖 Agent: Great! I've started a Python quiz for you.
   
   Question: What is the output of print(2 ** 3)?
   Options: 1. 6  2. 8  3. 9  4. 16

5. 💬 User: My answer is 8
   🤖 Agent: ✅ Correct! The answer is 8. Great job!

🎉 SUCCESS: MCP Integration Fully Working!
```

### Step 3: Understanding the Implementation

The working example demonstrates several key MCP concepts:

#### MCP Server (Official SDK)
```python
from mcp.server import FastMCP

# Create MCP server using official SDK
mcp = FastMCP("Quiz & Calculator Server")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def start_quiz(topic: str, user_id: str = "default") -> str:
    """Start a quiz on a specific topic."""
    # Implementation handles stateful quiz logic
    return quiz_response

# Run with stdio transport
mcp.run(transport="stdio")
```

#### Strands Agent Integration
```python
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

# Create MCP client that spawns the server
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="python",
        args=[__file__, "--server"]  # Run this script as server
    )
))

# Use within context manager
with mcp_client:
    tools = mcp_client.list_tools_sync()  # Discovers 5 tools
    agent = Agent(tools=tools)
    response = agent("Calculate 15 + 23")  # Uses MCP tools
```

### Step 4: Key Features Demonstrated

**✅ 5 Working MCP Tools:**
- `add` - Mathematical addition
- `multiply` - Mathematical multiplication  
- `power` - Exponentiation
- `start_quiz` - Begin interactive quiz
- `submit_answer` - Submit quiz answers

**✅ Stateful Interactions:**
- Quiz system maintains user progress
- Answers are validated and scored
- State persists across multiple interactions

**✅ Real-time Communication:**
- Tools are discovered automatically
- Agent calls tools as needed
- Results integrated seamlessly

**✅ Production Patterns:**
- Official MCP Python SDK
- Proper error handling
- Logging and debugging
- Clean separation of concerns

## Installation & Setup

### Required Dependencies
```bash
# Install official MCP SDK (already in requirements.txt)
pip install "mcp[cli]"

# Verify installation
python -c "from mcp.server import FastMCP; print('MCP SDK installed!')"
```

### Environment Setup
The workshop environment is already configured with all necessary dependencies.

## Understanding the Code Structure

### Dual-Mode Script Pattern
The working example uses a clever pattern where the same script can run as either:

1. **Client Mode** (default): Tests the MCP integration
2. **Server Mode** (`--server` flag): Runs as MCP server

```python
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        # Run as MCP server
        server = WorkingMCPServer()
        server.run_server()
    else:
        # Run as test client
        success = test_working_mcp_integration()
```

### MCP Server Implementation
```python
class WorkingMCPServer:
    def __init__(self):
        self.mcp = FastMCP("Quiz & Calculator Server")
        self._setup_tools()
        self.quiz_state = {}  # Maintains state
    
    def _setup_tools(self):
        @self.mcp.tool()
        def add(a: float, b: float) -> float:
            """Add two numbers together."""
            return a + b
        
        @self.mcp.tool()
        def start_quiz(topic: str, user_id: str = "default") -> str:
            """Start a quiz on a specific topic."""
            # Stateful quiz logic here
            return quiz_response
```

### Client Integration
```python
def test_working_mcp_integration():
    # Create client that spawns server as subprocess
    mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="python",
            args=[__file__, "--server"]
        )
    ))
    
    with mcp_client:
        tools = mcp_client.list_tools_sync()
        agent = Agent(tools=tools)
        # Test various scenarios...
```

## Common Issues & Solutions

### Issue: "MCPAgentTool has no attribute 'name'"
**Solution:** Use correct attribute name:
```python
# ❌ Wrong
print(f"{tool.name}: {tool.description}")

# ✅ Correct  
print(f"{tool.tool_name}")
```

### Issue: "Client initialization failed"
**Solution:** The working example handles this automatically by using stdio transport and proper server spawning.

### Issue: "Module not found"
**Solution:** All dependencies are included in `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Advanced Features

### Stateful Tool Interactions
The quiz system demonstrates how MCP tools can maintain state:

```python
def __init__(self):
    self.quiz_state = {}  # Maintains user state

@self.mcp.tool()
def start_quiz(topic: str, user_id: str = "default") -> str:
    # Store quiz state for this user
    self.quiz_state[user_id] = {
        "topic": topic,
        "current_question": question_data,
        "answered": False
    }
    return formatted_question

@self.mcp.tool()
def submit_answer(answer: str, user_id: str = "default") -> str:
    # Retrieve and update user state
    if user_id in self.quiz_state:
        # Process answer and update state
        return result
```

### Resource Endpoints
MCP also supports resource endpoints (read-only data):

```python
@self.mcp.resource("help://calculator")
def calculator_help() -> str:
    """Get help for calculator functions."""
    return help_text
```

## Production Considerations

### Security
- Input validation in all tools
- Proper error handling
- Logging for audit trails

### Performance
- Efficient state management
- Connection pooling for multiple clients
- Proper resource cleanup

### Deployment
- Docker containerization
- Health check endpoints
- Monitoring and metrics

## Key Takeaways

✅ **MCP standardizes external integrations** - One protocol for all services  
✅ **Official SDK is production-ready** - Robust, well-documented, actively maintained  
✅ **Stdio transport is perfect for development** - Easy testing and debugging  
✅ **Auto-discovery works seamlessly** - Tools appear natively to agents  
✅ **Stateful interactions supported** - Complex workflows possible  
✅ **Working example provided** - Real, tested implementation ready to run  

## Next Steps

1. **Modify the working example**: Add your own tools and quiz questions
2. **Explore HTTP transports**: For production web services
3. **Build domain-specific servers**: Create MCP servers for your use cases
4. **Deploy to production**: Use Docker, AWS ECS, or serverless platforms

## Resources

- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Strands MCP Integration Guide](https://strandsagents.com/latest/user-guide/concepts/tools/mcp-tools/)
- [Working Examples Repository](https://github.com/modelcontextprotocol/servers)

**Time to Complete:** 30 minutes  
**Difficulty:** Intermediate  
**Status:** ✅ **FULLY WORKING** - Ready for workshop!

---

**Try the working demo now:** `python exercise2-mcp-integration.py` 🚀
