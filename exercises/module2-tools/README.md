# Module 2: Custom Tools - Extending Agent Capabilities

## Learning Objectives
- Understand how tools transform agents from conversational to functional
- Use built-in tools from strands-agents-tools package
- Create custom tools using the @tool decorator
- Implement input validation and error handling
- Build a practical agent with multiple tools
- **BONUS**: Connect to external services using MCP (Model Context Protocol)

## Prerequisites
- Completed Module 1 (Hello Agent)
- Understanding of Python functions and decorators
- strands-agents-tools package installed

## What Are Tools?

Tools are functions that agents can use to perform actions beyond generating text:
- **Access external data** (files, APIs, databases)
- **Perform calculations** and specialized processing
- **Create and modify content**
- **Connect to any external service**

The Strands SDK automatically determines when to use tools based on conversation context.

## Step-by-Step Instructions

### Step 1: Using Built-in Tools

Create and run `exercise2-custom-tools.py`:

```bash
python exercise2-custom-tools.py
```

This demonstrates:
- Built-in tools: `calculator`, `current_time`
- Custom tools: `letter_counter`, `text_reverser`, `word_counter`
- Automatic tool selection based on user queries
- Interactive mode for testing

**Expected Output:**
```
🛠️  Custom Tools Test
Available tools:
  • calculator
  • current_time
  • letter_counter
  • text_reverser
  • word_counter

🧪 Testing 5 different tool scenarios:
1. 📝 Request: What time is it right now?
   🤖 Response: The current time is 2025-06-29T10:38:50...

2. 📝 Request: Calculate 15 * 23 + 47
   🤖 Response: The result of 15 * 23 + 47 is 392...
```

### Step 2: Understanding Custom Tool Creation

Key patterns from the working example:

```python
from strands import Agent, tool
from strands_tools import calculator, current_time

@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.
    
    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count
        
    Returns:
        int: The number of occurrences of the letter in the word
    """
    # Input validation
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0
    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")
    
    return word.lower().count(letter.lower())

# Create agent with both built-in and custom tools
agent = Agent(tools=[calculator, current_time, letter_counter])
```

**Tool Design Principles:**
- **Clear docstring** - Used for tool specification
- **Type hints** - Enable automatic validation
- **Input validation** - Prevent errors and security issues
- **Descriptive function name** - Helps agent understand purpose

### Step 3: Testing Your Understanding

Try these exercises with the working example:

1. **Run the interactive mode**: Test different tool combinations
2. **Modify existing tools**: Add new functionality
3. **Create your own tool**: Build a simple calculator extension
4. **Test error handling**: See how validation works

## 🌟 BONUS: MCP Integration - External Services

**Model Context Protocol (MCP)** allows agents to connect to external services through a standardized interface. This enables connection to databases, APIs, and specialized tools.

### Quick MCP Demo

Run the working MCP integration:

```bash
python exercise2-mcp-integration.py
```

**What You'll See:**
```
🎯 Testing 7 scenarios:
============================================================

1. 💬 User: Calculate 15 + 23
   🤖 Agent: The sum of 15 + 23 is 38.

4. 💬 User: Start a Python quiz for me
   🤖 Agent: Great! I've started a Python quiz for you.
   
   Question: What is the output of print(2 ** 3)?
   Options: 1. 6  2. 8  3. 9  4. 16

5. 💬 User: My answer is 8
   🤖 Agent: ✅ Correct! The answer is 8. Great job!

🎉 SUCCESS: MCP Integration Fully Working!
```

### MCP Features Demonstrated:
- **5 MCP Tools**: `add`, `multiply`, `power`, `start_quiz`, `submit_answer`
- **Stateful Interactions**: Quiz system maintains progress
- **Real-time Communication**: Immediate tool discovery
- **External Service Pattern**: Shows how to connect to any external system

**📚 For complete MCP tutorial, see:** [`MCP_INTEGRATION.md`](./MCP_INTEGRATION.md)

## Understanding Tool Integration

### Automatic Tool Selection
The agent automatically:
1. **Analyzes the user's request**
2. **Identifies which tools are needed**
3. **Calls tools in the correct order**
4. **Integrates results into a natural response**

### Tool Specification Generation
The `@tool` decorator automatically creates tool specifications from:
- **Function name** - Becomes tool identifier
- **Docstring** - Provides description and usage
- **Type hints** - Define input/output types
- **Parameters** - Become tool arguments

### Error Handling Best Practices
```python
@tool
def safe_division(a: float, b: float) -> str:
    """Safely divide two numbers with error handling."""
    try:
        if b == 0:
            return "Error: Cannot divide by zero"
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

## Common Issues & Solutions

### Issue: Tool Not Being Called
**Problem:** Agent doesn't use your custom tool
**Solution:** 
- Ensure clear, descriptive docstring
- Use specific function names
- Add type hints
- Test with explicit requests

### Issue: Tool Validation Errors
**Problem:** `ValidationError: Invalid input type`
**Solution:**
```python
@tool
def validated_tool(text: str, count: int = 1) -> str:
    """Tool with proper validation."""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(count, int) or count < 1:
        raise ValueError("count must be a positive integer")
    return text * count
```

### Issue: Tool Import Errors
**Problem:** `ModuleNotFoundError` for strands_tools
**Solution:**
```bash
pip install strands-agents-tools
```

## Testing Your Understanding

Try these exercises:

1. **Create a unit converter tool** that converts between different units
2. **Build a password generator tool** with customizable length and complexity
3. **Make a text formatter tool** that can uppercase, lowercase, or title case text
4. **Design a simple math tool** that handles multiple operations

## Advanced Concepts

### Tool Chaining
Tools can work together through the agent:

```python
@tool
def complex_analysis(data: str) -> str:
    """Perform complex analysis that might need multiple tools."""
    # The agent will automatically use other tools as needed
    return f"Analyzing: {data}"
```

### Tool Configuration
```python
# Inspect available tools
print("Available tools:", agent.tool_names)

# Get tool specifications
for tool_name in agent.tool_names:
    spec = agent.get_tool_spec(tool_name)
    print(f"{tool_name}: {spec['description']}")
```

## Key Takeaways

✅ **Tools extend agent capabilities** beyond conversation  
✅ **@tool decorator** makes function creation simple  
✅ **Automatic tool selection** based on context  
✅ **Input validation** prevents errors  
✅ **Error handling** ensures robust operation  
✅ **MCP integration** connects to external services  

**Time to Complete:** 40 minutes (+ 30 minutes for MCP bonus)  
**Difficulty:** Intermediate  
**Status:** ✅ **FULLY WORKING** - All examples tested and verified  

## Next Steps

- **Module 3**: Multi-Agent Systems (orchestration patterns)
- **Advanced MCP**: Build your own MCP servers
- **Production Tools**: Deploy tools to cloud services

## Resources

- [Official Tools Documentation](https://strandsagents.com/latest/user-guide/concepts/tools/)
- [Built-in Tools Reference](https://strandsagents.com/latest/api-reference/tools/)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Community Examples](https://github.com/strands-agents/samples)
