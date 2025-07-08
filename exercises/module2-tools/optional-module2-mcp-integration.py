#!/usr/bin/env python3
"""
Module 2 Exercise: Build Your Own MCP-Enabled Agent (FIXED VERSION)

STUDENT EXERCISE: Complete the TODOs to build a working MCP-enabled agent.

KEY FIX: Proper MCP client context manager usage - the agent must be created
and used WITHIN the client context manager.

Learning Goals:
1. Connect to real MCP servers
2. Create agents with MCP tools INSIDE context managers
3. Handle MCP client lifecycle properly
4. Build practical applications

Instructions:
1. Install required MCP servers (see setup section)
2. Complete the TODO sections
3. Test your implementation
4. Extend with additional functionality
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel


class StudentMCPAgent:
    """Student exercise: Build an MCP-enabled agent - FIXED VERSION."""
    
    def __init__(self):
        # TODO 1: Initialize the Bedrock model
        # Hint: Use BedrockModel with Claude 3.7 Sonnet
        self.model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            temperature=0.3
        )  # SOLUTION PROVIDED - Replace with your implementation
    
    def exercise_1_file_operations(self):
        """Exercise 1: Basic file operations with MCP - FIXED VERSION."""
        print("\n📁 Exercise 1: File Operations (FIXED)")
        print("="*50)
        
        current_dir = str(Path.cwd())
        
        # TODO 2: Create MCPClient for filesystem server
        # Hint: Use stdio_client with StdioServerParameters
        client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", current_dir]
            )
        ))  # SOLUTION PROVIDED - Replace with your implementation
        
        # CRITICAL FIX: Use agent WITHIN the client context manager
        with client:
            # TODO 3: Get tools and create agent INSIDE the context manager
            tools = client.list_tools_sync()  # SOLUTION PROVIDED
            
            agent = Agent(
                model=self.model,
                tools=tools,
                system_prompt="You are a filesystem assistant with file operation capabilities."
            )  # SOLUTION PROVIDED - Replace with your implementation
            
            tasks = [
                "List all .py files in the current directory",
                "Create a new file called 'student_notes.txt' with your learning notes about MCP",
                "Read the content of the file you just created"
            ]
            
            for i, task in enumerate(tasks, 1):
                print(f"\n📝 Task {i}: {task}")
                # TODO 4: Safely interact with the agent
                try:
                    response = agent(task)  # SOLUTION PROVIDED
                    print(f"✅ Result: {response}")
                except Exception as e:
                    print(f"❌ Error: {e}")
    
    def exercise_2_memory_operations(self):
        """Exercise 2: Memory operations with MCP - FIXED VERSION."""
        print("\n🧠 Exercise 2: Memory Operations (FIXED)")
        print("="*50)
        
        # TODO 5: Create MCPClient for memory server
        client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-memory"]
            )
        ))  # SOLUTION PROVIDED - Replace with your implementation
        
        # CRITICAL FIX: Use agent WITHIN the client context manager
        with client:
            # TODO 6: Get tools and create agent INSIDE the context manager
            tools = client.list_tools_sync()  # SOLUTION PROVIDED
            
            agent = Agent(
                model=self.model,
                tools=tools,
                system_prompt="You are a memory-enhanced assistant with persistent storage capabilities."
            )  # SOLUTION PROVIDED - Replace with your implementation
            
            tasks = [
                "Remember that I am a student learning about MCP integration in Module 2",
                "Store the fact that I completed the filesystem exercise successfully",
                "What do you remember about me and my learning progress?",
                "Search your memory for information about MCP exercises"
            ]
            
            for i, task in enumerate(tasks, 1):
                print(f"\n💭 Task {i}: {task}")
                # TODO 7: Safely interact with the agent
                try:
                    response = agent(task)  # SOLUTION PROVIDED
                    print(f"✅ Result: {response}")
                except Exception as e:
                    print(f"❌ Error: {e}")
    
    def exercise_3_custom_workflow(self):
        """
        Exercise 3: Create your own workflow - STUDENT IMPLEMENTATION.
        
        TODO 8: Design and implement a custom workflow that uses MCP tools.
        
        Requirements:
        1. Use at least one MCP server (filesystem or memory)
        2. Create agent INSIDE the context manager
        3. Perform multiple related tasks
        4. Handle errors gracefully
        
        Ideas:
        - Create a learning progress tracker
        - Build a project documentation generator
        - Make a file organizer
        - Create a research assistant
        """
        print("\n🚀 Exercise 3: Custom Workflow - YOUR IMPLEMENTATION")
        print("="*50)
        
        # TODO 8: Implement your custom workflow here
        print("📝 STUDENT TODO: Implement your custom workflow")
        print("\nExample structure:")
        print("1. Create MCPClient")
        print("2. Use 'with client:' context manager")
        print("3. Create agent inside the context manager")
        print("4. Execute your workflow tasks")
        print("5. Handle errors appropriately")
        
        # EXAMPLE IMPLEMENTATION (you can replace this):
        current_dir = str(Path.cwd())
        
        # Example: Learning Progress Tracker
        print("\n📚 Example: Learning Progress Tracker")
        
        # Use filesystem to create progress file
        fs_client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", current_dir]
            )
        ))
        
        with fs_client:
            fs_tools = fs_client.list_tools_sync()
            fs_agent = Agent(
                model=self.model,
                tools=fs_tools,
                system_prompt="You are a learning progress tracker assistant."
            )
            
            try:
                # Create a progress tracking file
                progress_task = "Create a file called 'learning_progress.md' that tracks my Module 2 MCP learning milestones"
                response = fs_agent(progress_task)
                print(f"Progress tracking: {response}")
            except Exception as e:
                print(f"❌ Workflow error: {e}")
        
        print("\n💡 Now implement your own custom workflow above this example!")
    
    def run_all_exercises(self):
        """Run all exercises."""
        print("🎓 Starting Module 2 MCP Exercises (FIXED VERSION)")
        print("🔧 KEY FIX: Proper context manager usage")
        
        self.exercise_1_file_operations()
        self.exercise_2_memory_operations()
        self.exercise_3_custom_workflow()
        
        print("\n🎯 Exercises Complete!")
        print("\n📚 What you learned:")
        print("✅ How to create MCP clients properly")
        print("✅ The importance of context manager lifecycle")
        print("✅ Creating agents INSIDE the context manager")
        print("✅ Handling MCP tool errors gracefully")
        print("✅ Building practical MCP applications")
        
        print("\n🚀 Next steps:")
        print("- Review your implementations")
        print("- Try extending the functionality")
        print("- Experiment with other MCP servers")
        print("- Build your own MCP-enabled applications")


def setup_instructions():
    """Show setup instructions for students."""
    print("""
🛠️  SETUP INSTRUCTIONS (UPDATED)
================================

Before starting the exercises, install the required MCP servers:

1. Install Node.js (if not already installed)
2. Install MCP servers:
   npm install -g @modelcontextprotocol/server-filesystem
   npm install -g @modelcontextprotocol/server-memory

3. Verify installation:
   python module2-exercise-real-mcp-fixed.py --check

4. Start exercises:
   python module2-exercise-real-mcp-fixed.py

🔧 CRITICAL FIX EXPLAINED
========================

The key issue was MCP client context manager usage:

❌ WRONG WAY:
```python
client = MCPClient(...)
tools = client.list_tools_sync()  # Outside context manager
agent = Agent(tools=tools)        # Outside context manager
with client:
    response = agent("task")       # Agent created outside, used inside
```

✅ CORRECT WAY:
```python
client = MCPClient(...)
with client:                      # Context manager first
    tools = client.list_tools_sync()  # Inside context manager
    agent = Agent(tools=tools)        # Inside context manager
    response = agent("task")           # Everything inside
```

📚 WHY THIS MATTERS
==================

- MCP tools need an active client session to work
- The context manager manages the client session lifecycle
- Creating agents outside the context manager breaks the connection
- This is a common mistake that causes MCPClientInitializationError

🎯 EXERCISE GOALS (UPDATED)
==========================

By completing these exercises, you will:
✅ Understand real MCP integration
✅ Master MCP client context manager usage
✅ Create MCP-enabled Strands agents correctly
✅ Handle MCP client lifecycle properly
✅ Build practical applications
✅ Follow MCP best practices
""")


def check_student_setup():
    """Check if student environment is ready."""
    import subprocess
    
    print("🔍 Checking Student Setup...")
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not installed")
        return False
    
    # Check MCP servers with proper arguments
    try:
        # Test filesystem server with current directory
        result = subprocess.run(
            ["npx", "-y", "@modelcontextprotocol/server-filesystem", "."],
            capture_output=True, timeout=3, text=True
        )
        # Server should start (timeout is expected)
        print("✅ MCP filesystem server available")
    except subprocess.TimeoutExpired:
        print("✅ MCP filesystem server available")
    except Exception as e:
        print(f"❌ MCP filesystem server not working: {e}")
        return False
    
    try:
        # Test memory server
        result = subprocess.run(
            ["npx", "-y", "@modelcontextprotocol/server-memory"],
            capture_output=True, timeout=3, text=True
        )
        # Server should start (timeout is expected)
        print("✅ MCP memory server available")
    except subprocess.TimeoutExpired:
        print("✅ MCP memory server available")
    except Exception as e:
        print(f"❌ MCP memory server not working: {e}")
        return False
    
    print("✅ Setup complete! Ready for exercises.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Module 2: MCP Exercise for Students (FIXED)")
    parser.add_argument('--setup', action='store_true', help='Show setup instructions')
    parser.add_argument('--check', action='store_true', help='Check setup')
    parser.add_argument('--exercise', type=int, choices=[1, 2, 3], help='Run specific exercise')
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    if args.setup:
        setup_instructions()
        return 0
    
    if args.check:
        return 0 if check_student_setup() else 1
    
    # Check setup before running exercises
    if not check_student_setup():
        print("\n💡 Run with --setup to see installation instructions")
        return 1
    
    student = StudentMCPAgent()
    
    try:
        if args.exercise == 1:
            student.exercise_1_file_operations()
        elif args.exercise == 2:
            student.exercise_2_memory_operations()
        elif args.exercise == 3:
            student.exercise_3_custom_workflow()
        else:
            ## show options to the student and aske to start yhe program with one of these args, or setup and check
            print("💡 You can run the following exercises:")
            print("   --exercise 1: File Operations")
            print("   --exercise 2: Memory Operations")
            print("   --exercise 3: Custom Workflow")
            print("\n🔧 Or you can run the setup and check commands:")
            print("   --setup: Show setup instructions")
            print("   --check: Check setup")

        return 0
        
    except Exception as e:
        print(f"❌ Exercise failed: {e}")
        print("💡 Check the context manager usage and try again")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
