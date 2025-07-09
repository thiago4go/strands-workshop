#!/usr/bin/env python3
"""
Module 5: A2A Research Team - Main Entry Point

This is the main entry point for the A2A (Agent-to-Agent) multi-agent research system.
It provides options to start agent servers, test individual agents, or run the orchestrator.
"""

import asyncio
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print the module banner"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Module 5: A2A Research Team                              ║
║                  Agent-to-Agent Multi-Agent Orchestration                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

This module demonstrates a decoupled multi-agent architecture using the A2A protocol.
Each agent runs as an independent A2A server and communicates via HTTP.

Available Agents:
• Research Specialist (Port 9001) - Comprehensive research and analysis
• Analysis Specialist (Port 9002) - Deep data analysis and insights  
• Fact-Check Specialist (Port 9003) - Information verification
• QA Specialist (Port 9004) - Quality assurance and validation

Architecture: HTTP-based A2A protocol with Strands Agents + Amazon Bedrock
""")

def print_menu():
    """Print the main menu"""
    print("""
Choose an option:

1. 🚀 Start All Agent Servers
   Launch all A2A agent servers in the background

2. 🧪 Test Individual Agents  
   Test each agent server individually to verify functionality

3. 🎯 Run Research Orchestrator
   Execute a comprehensive research task using all agents

4. 📖 View Documentation
   Show detailed information about the A2A implementation

5. ❌ Exit

""")

def show_documentation():
    """Show documentation about the A2A implementation"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           A2A Implementation Guide                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

🏗️  ARCHITECTURE:
   • Each agent runs as an independent A2AServer (HTTP server)
   • Agents expose Agent Cards at /.well-known/agent.json
   • Communication uses JSON-RPC 2.0 over HTTP
   • Orchestrator uses A2AClient to coordinate agents

🔧 COMPONENTS:
   • A2AServer: Wraps Strands agents for A2A protocol
   • StrandsA2AExecutor: Handles agent execution in A2A context
   • A2AClient: Client for communicating with A2A servers
   • A2ACardResolver: Service discovery via Agent Cards

📋 PREREQUISITES:
   • AWS credentials configured (aws configure)
   • Claude 3.7 Sonnet enabled in Bedrock
   • strands-agents and a2a-sdk packages installed

🚀 USAGE WORKFLOW:
   1. Start agent servers (Option 1)
   2. Test individual agents (Option 2) 
   3. Run orchestrator for full research (Option 3)

🔍 TROUBLESHOOTING:
   • Check AWS credentials: aws sts get-caller-identity
   • Verify Bedrock access: Check AWS Bedrock console
   • Check agent cards: curl http://localhost:9001/.well-known/agent.json
   • View logs: Check terminal output for error messages

📚 FILES:
   • src/research_agent_server.py - Research specialist A2A server
   • src/analysis_agent_server.py - Analysis specialist A2A server  
   • src/factcheck_agent_server.py - Fact-check specialist A2A server
   • src/qa_agent_server.py - QA specialist A2A server
   • src/orchestrator_client.py - Multi-agent orchestrator
   • start_all_agents.py - Server management script
   • test_individual_agents.py - Individual agent testing

Press Enter to continue...
""")
    input()

async def run_orchestrator():
    """Run the research orchestrator"""
    try:
        from src.orchestrator_client import main as orchestrator_main
        await orchestrator_main()
    except ImportError as e:
        logger.error(f"Failed to import orchestrator: {e}")
        print("❌ Error: Could not import orchestrator. Check that all dependencies are installed.")
    except Exception as e:
        logger.error(f"Error running orchestrator: {e}")
        print(f"❌ Error running orchestrator: {e}")

async def test_agents():
    """Test individual agents"""
    try:
        # Import and run the test
        import test_individual_agents
        await test_individual_agents.main()
    except ImportError as e:
        logger.error(f"Failed to import test script: {e}")
        print("❌ Error: Could not import test script. Check that all dependencies are installed.")
    except Exception as e:
        logger.error(f"Error testing agents: {e}")
        print(f"❌ Error testing agents: {e}")

def start_servers():
    """Start all agent servers"""
    try:
        import start_all_agents
        start_all_agents.main()
    except ImportError as e:
        logger.error(f"Failed to import server manager: {e}")
        print("❌ Error: Could not import server manager. Check that all dependencies are installed.")
    except Exception as e:
        logger.error(f"Error starting servers: {e}")
        print(f"❌ Error starting servers: {e}")

async def main():
    """Main function"""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting all agent servers...")
                print("Note: This will run until you press Ctrl+C")
                print("Servers will be available at:")
                print("  • Research: http://localhost:9001")
                print("  • Analysis: http://localhost:9002") 
                print("  • Fact-Check: http://localhost:9003")
                print("  • QA: http://localhost:9004")
                print("\nPress Enter to continue or Ctrl+C to cancel...")
                input()
                start_servers()
                
            elif choice == "2":
                print("\n🧪 Testing individual agents...")
                print("Note: Make sure agent servers are running first (Option 1)")
                print("Press Enter to continue or Ctrl+C to cancel...")
                input()
                await test_agents()
                
            elif choice == "3":
                print("\n🎯 Running research orchestrator...")
                print("Note: Make sure agent servers are running first (Option 1)")
                print("This will conduct a comprehensive research task using all agents.")
                print("Press Enter to continue or Ctrl+C to cancel...")
                input()
                await run_orchestrator()
                
            elif choice == "4":
                show_documentation()
                
            elif choice == "5":
                print("\n👋 Goodbye!")
                break
                
            else:
                print("\n❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error in main menu: {e}")
            print(f"\n❌ Error: {e}")
            print("Please try again or choose a different option.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
