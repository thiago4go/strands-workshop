# Module 2 Extra: MCP Integration - Real External MCP Servers

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
- Node.js installed (for MCP servers)
- Understanding of client-server architecture

## What the Workshop Exercise Actually Does

The `optional-module2-mcp-integration.py` file is a **student exercise** that demonstrates real MCP integration with external servers. Here's what it actually provides:

### 🎯 Three Complete Exercises

#### **Exercise 1: File Operations with MCP Filesystem Server**
- **MCP Server Used**: `@modelcontextprotocol/server-filesystem`
- **Installation**: `npm install -g @modelcontextprotocol/server-filesystem`
- **Capabilities**:
  - List files in directories
  - Create new files with content
  - Read file contents
  - Search for files by pattern
  - Write to existing files

**What it does:**
1. Lists all `.py` files in current directory
2. Creates a `student_notes.txt` file with MCP learning notes
3. Reads back the content of the created file

#### **Exercise 2: Memory Operations with MCP Memory Server**
- **MCP Server Used**: `@modelcontextprotocol/server-memory`
- **Installation**: `npm install -g @modelcontextprotocol/server-memory`
- **Capabilities**:
  - Create entities in knowledge graph
  - Create relationships between entities
  - Read entire knowledge graph
  - Search nodes by content
  - Persistent memory across sessions

**What it does:**
1. Stores information about the student's learning progress
2. Records completion of filesystem exercise
3. Retrieves stored information about learning progress
4. Searches memory for MCP-related information

#### **Exercise 3: Custom Workflow Implementation**
- **Purpose**: Student implements their own MCP workflow
- **Example Provided**: Learning Progress Tracker
- **Requirements**:
  - Use at least one MCP server
  - Create agent inside context manager
  - Perform multiple related tasks
  - Handle errors gracefully

### 🛠️ Setup and Installation

The exercise includes complete setup instructions and verification:

```bash
# 1. Install required MCP servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-memory

# 2. Verify installation
python optional-module2-mcp-integration.py --check

# 3. See setup instructions
python optional-module2-mcp-integration.py --setup

# 4. Run specific exercises
python optional-module2-mcp-integration.py --exercise 1  # File operations
python optional-module2-mcp-integration.py --exercise 2  # Memory operations
python optional-module2-mcp-integration.py --exercise 3  # Custom workflow
```

### 🔧 Key Technical Implementation

#### **Critical MCP Pattern - Context Manager Usage**

The exercise teaches the **most important MCP concept**:

❌ **WRONG WAY** (causes MCPClientInitializationError):
```python
client = MCPClient(...)
tools = client.list_tools_sync()  # Outside context manager
agent = Agent(tools=tools)        # Outside context manager
with client:
    response = agent("task")       # Agent created outside, used inside
```

✅ **CORRECT WAY** (works properly):
```python
client = MCPClient(...)
with client:                      # Context manager first
    tools = client.list_tools_sync()  # Inside context manager
    agent = Agent(tools=tools)        # Inside context manager
    response = agent("task")           # Everything inside
```

#### **MCP Client Configuration**

**Filesystem Server:**
```python
client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", current_dir]
    )
))
```

**Memory Server:**
```python
client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-memory"]
    )
))
```

### 🎓 Learning Outcomes

By completing this exercise, students learn:

✅ **Real MCP Integration** - Connect to actual external MCP servers  
✅ **Context Manager Lifecycle** - Proper MCP client session management  
✅ **Tool Auto-Discovery** - How agents automatically discover MCP tools  
✅ **Error Handling** - Graceful handling of MCP connection issues  
✅ **Stateful Operations** - Memory server maintains state across calls  
✅ **Production Patterns** - Best practices for MCP integration  

### 🚀 Actual Exercise Output

When you run the exercises, you'll see real interactions like:

```
📁 Exercise 1: File Operations
==================================================
Secure MCP Filesystem Server running on stdio
Allowed directories: ['/home/user/workshop/exercises/module2-tools']

📝 Task 1: List all .py files in the current directory
✅ Result: Here are all the Python (.py) files found:
1. `/path/to/exercise2-custom-tools.py`
2. `/path/to/module2-exercise-real-mcp-fixed.py`

📝 Task 2: Create a new file called 'student_notes.txt'
✅ Result: I've created 'student_notes.txt' with comprehensive MCP learning notes...

🧠 Exercise 2: Memory Operations (FIXED)
==================================================
Knowledge Graph MCP Server running on stdio

💭 Task 1: Remember that I am a student learning about MCP integration
✅ Result: I've stored that you're a student learning about MCP integration in Module 2...
```

### 🔍 Setup Verification

The exercise includes robust setup checking:

```bash
$ python optional-module2-mcp-integration.py --check
🔍 Checking Student Setup...
✅ Node.js: v23.7.0
✅ MCP filesystem server available
✅ MCP memory server available
✅ Setup complete! Ready for exercises.
```

## Architecture Overview

```
┌─────────────────┐    stdio/JSON-RPC    ┌─────────────────┐
│  Strands Agent  │ ◄─────────────────► │   MCP Server    │
│   (MCP Client)  │                    │  (Node.js/npm)  │
└─────────────────┘                    └─────────────────┘
        │                                       │
        │                                       │
    ┌───▼────┐                              ┌───▼────┐
    │ Claude │                              │ Tools: │
    │ 3.7    │                              │ • Files│
    │ Sonnet │                              │ • Memory│
    └────────┘                              └────────┘
```

## Common Issues & Solutions

### Issue: "MCP filesystem server not working"
**Solution:** The exercise includes a fixed setup checker that properly tests MCP servers:
```python
# Fixed server check uses proper arguments
result = subprocess.run(
    ["npx", "-y", "@modelcontextprotocol/server-filesystem", "."],
    capture_output=True, timeout=3
)
```

### Issue: "MCPClientInitializationError"
**Solution:** The exercise teaches proper context manager usage - all MCP operations must be inside the `with client:` block.

### Issue: "Node.js not found"
**Solution:** Install Node.js first, then install MCP servers with npm.

## Production Considerations

### Security
- MCP filesystem server restricts access to specified directories only
- Input validation in all tool interactions
- Proper error handling and logging

### Performance
- Stdio transport is efficient for local development
- Memory server maintains persistent state
- Connection lifecycle managed by context managers

### Deployment
- MCP servers can run as separate processes
- HTTP transport available for remote servers
- Docker containerization supported

## Key Differences from Documentation

**This exercise IS:**
- ✅ Real integration with external MCP servers
- ✅ Using official npm-published MCP servers
- ✅ Teaching proper MCP client lifecycle management
- ✅ Demonstrating stateful interactions
- ✅ Production-ready patterns and error handling

## Next Steps

1. **Complete the exercises**: Follow the TODOs in the code
2. **Extend functionality**: Add your own custom workflows
3. **Explore other MCP servers**: Try database, API, or web servers
4. **Build production applications**: Use HTTP transport for remote services

## Resources

- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Strands MCP Integration Guide](https://strandsagents.com/latest/user-guide/concepts/tools/mcp-tools/)

**Time to Complete:** 15 minutes  
**Difficulty:** Intermediate  
**Status:** ✅ **FULLY WORKING** - Real MCP integration with external servers!

---

**Start the exercises now:** `python optional-module2-mcp-integration.py --setup` 🚀
