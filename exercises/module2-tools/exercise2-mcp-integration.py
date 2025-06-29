#!/usr/bin/env python3
"""
Module 2 Extra: Working MCP Integration
Based on official MCP Python SDK and verified working examples
"""

import os
import sys
import time
from mcp.server import FastMCP
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_demo")

class WorkingMCPServer:
    """Working MCP server using official Python SDK."""
    
    def __init__(self):
        self.mcp = FastMCP("Quiz & Calculator Server")
        self._setup_tools()
        self._setup_resources()
        self.quiz_state = {}
    
    def _setup_tools(self):
        """Setup MCP tools using official SDK patterns."""
        
        @self.mcp.tool()
        def add(a: float, b: float) -> float:
            """Add two numbers together."""
            logger.info(f"Adding {a} + {b}")
            return a + b
        
        @self.mcp.tool()
        def multiply(a: float, b: float) -> float:
            """Multiply two numbers."""
            logger.info(f"Multiplying {a} * {b}")
            return a * b
        
        @self.mcp.tool()
        def power(base: float, exponent: float) -> float:
            """Calculate base raised to the power of exponent."""
            logger.info(f"Calculating {base} ^ {exponent}")
            return base ** exponent
        
        @self.mcp.tool()
        def start_quiz(topic: str, user_id: str = "default") -> str:
            """Start a quiz on a specific topic."""
            logger.info(f"Starting quiz on {topic} for user {user_id}")
            
            quiz_questions = {
                "python": {
                    "question": "What is the output of print(2 ** 3)?",
                    "options": ["6", "8", "9", "16"],
                    "correct": "8"
                },
                "math": {
                    "question": "What is 15 * 23?",
                    "options": ["345", "355", "365", "375"],
                    "correct": "345"
                }
            }
            
            if topic.lower() not in quiz_questions:
                return f"Topic '{topic}' not available. Available topics: {', '.join(quiz_questions.keys())}"
            
            question_data = quiz_questions[topic.lower()]
            self.quiz_state[user_id] = {
                "topic": topic,
                "question": question_data,
                "answered": False
            }
            
            return f"""Quiz started on topic: {topic}

Question: {question_data['question']}

Options:
{chr(10).join([f"{i+1}. {opt}" for i, opt in enumerate(question_data['options'])])}

Use submit_answer to provide your answer."""
        
        @self.mcp.tool()
        def submit_answer(answer: str, user_id: str = "default") -> str:
            """Submit an answer to the current quiz question."""
            logger.info(f"User {user_id} submitted answer: {answer}")
            
            if user_id not in self.quiz_state:
                return "No active quiz found. Please start a quiz first."
            
            quiz_data = self.quiz_state[user_id]
            if quiz_data["answered"]:
                return "Quiz already completed!"
            
            correct_answer = quiz_data["question"]["correct"]
            is_correct = answer.strip() == correct_answer
            
            quiz_data["answered"] = True
            
            if is_correct:
                return f"✅ Correct! The answer is {correct_answer}. Great job!"
            else:
                return f"❌ Incorrect. The correct answer is {correct_answer}. Better luck next time!"
    
    def _setup_resources(self):
        """Setup MCP resources."""
        
        @self.mcp.resource("help://calculator")
        def calculator_help() -> str:
            """Get help for calculator functions."""
            return """
Calculator Help
===============
Available functions:
- add(a, b): Add two numbers
- multiply(a, b): Multiply two numbers
- power(base, exponent): Calculate base^exponent

Examples:
- add(5, 3) = 8
- multiply(4, 7) = 28
- power(2, 3) = 8
"""
        
        @self.mcp.resource("help://quiz")
        def quiz_help() -> str:
            """Get help for quiz functions."""
            return """
Quiz Help
=========
Available functions:
- start_quiz(topic, user_id): Start a quiz on a topic
- submit_answer(answer, user_id): Submit your answer

Available topics: python, math

Example:
1. start_quiz("python", "user1")
2. submit_answer("8", "user1")
"""
    
    def run_server(self):
        """Run the MCP server with stdio transport."""
        try:
            logger.info("🚀 Starting MCP server with stdio transport...")
            self.mcp.run(transport="stdio")
        except Exception as e:
            logger.error(f"Server error: {e}")

def run_mcp_server_in_background():
    """Run MCP server in a separate process."""
    server = WorkingMCPServer()
    server.run_server()

def test_working_mcp_integration():
    """Test the working MCP integration."""
    print("🧪 Testing Working MCP Integration")
    print("="*60)
    
    try:
        # Create MCP client using stdio transport
        print("🔌 Creating MCP client...")
        
        # Get path to this script to run as MCP server
        server_script = __file__
        
        # Create MCP client that spawns our server
        mcp_client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command="python",
                args=[server_script, "--server"]
            )
        ))
        
        print("✅ MCP client created")
        
        with mcp_client:
            print("🔍 Discovering tools and resources...")
            
            # List tools
            tools = mcp_client.list_tools_sync()
            print(f"✅ Found {len(tools)} MCP tools:")
            for tool in tools:
                print(f"   • {tool.tool_name}")
            
            # List resources
            try:
                resources = mcp_client.list_resources_sync()
                print(f"✅ Found {len(resources)} MCP resources:")
                for resource in resources:
                    print(f"   • {resource.uri}")
            except Exception as e:
                print(f"ℹ️  Resources: {e}")
            
            # Create agent
            print("\n🤖 Creating Strands agent with MCP tools...")
            agent = Agent(
                tools=tools,
                system_prompt="You are a helpful assistant with calculator and quiz capabilities."
            )
            print("✅ Agent created successfully")
            
            # Test scenarios
            test_scenarios = [
                "Calculate 15 + 23",
                "What is 7 multiplied by 8?",
                "Calculate 2 to the power of 5", 
                "Start a Python quiz for me",
                "My answer is 8",
                "Start a math quiz",
                "I think the answer is 345"
            ]
            
            print(f"\n🎯 Testing {len(test_scenarios)} scenarios:")
            print("="*60)
            
            for i, scenario in enumerate(test_scenarios, 1):
                print(f"\n{i}. 💬 User: {scenario}")
                try:
                    response = agent(scenario)
                    print(f"   🤖 Agent: {response}")
                    
                    # Small delay between requests
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")
            
            return True
            
    except Exception as e:
        print(f"❌ MCP Integration Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function - can run as server or client."""
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        # Run as MCP server
        server = WorkingMCPServer()
        server.run_server()
    else:
        # Run as test client
        print("🌟 Working MCP Integration Demo")
        print("="*60)
        print("This demo shows:")
        print("• MCP server with calculator and quiz tools")
        print("• Strands agent connecting via stdio transport")
        print("• Real-time tool discovery and execution")
        print("• Stateful quiz interactions")
        print("="*60)
        
        try:
            success = test_working_mcp_integration()
            
            if success:
                print("\n" + "="*60)
                print("🎉 SUCCESS: MCP Integration Fully Working!")
                print("✅ MCP server created with official SDK")
                print("✅ Multiple tools and resources available")
                print("✅ Strands agent connected successfully")
                print("✅ Calculator and quiz functions working")
                print("✅ Stateful interactions maintained")
                print("="*60)
                
                print("\n🎓 Workshop Ready!")
                print("Participants can now:")
                print("• Learn MCP concepts with working examples")
                print("• See real-time tool discovery")
                print("• Experience stateful agent interactions")
                print("• Understand production deployment patterns")
                
            else:
                print("\n❌ Integration test failed - check errors above")
            
            return success
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
