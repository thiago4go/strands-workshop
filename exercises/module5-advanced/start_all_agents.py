#!/usr/bin/env python3
"""
Start All Agent Servers

Starts all A2A agent servers in separate processes for testing.
"""

import subprocess
import time
import logging
import signal
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class AgentServerManager:
    """Manages multiple agent server processes"""
    
    def __init__(self):
        self.processes = {}
        self.agents = [
            ("research", "src/research_agent_server.py", 9001),
            ("analysis", "src/analysis_agent_server.py", 9002),
            ("factcheck", "src/factcheck_agent_server.py", 9003),
            ("qa", "src/qa_agent_server.py", 9004)
        ]
    
    def start_agent(self, name: str, script_path: str, port: int):
        """Start a single agent server"""
        try:
            logger.info(f"Starting {name} agent server on port {port}...")
            
            # Start the process
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes[name] = {
                'process': process,
                'port': port,
                'script': script_path
            }
            
            logger.info(f"✅ {name} agent server started (PID: {process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start {name} agent server: {e}")
            return False
    
    def start_all_agents(self):
        """Start all agent servers"""
        logger.info("Starting all A2A agent servers...")
        
        success_count = 0
        for name, script_path, port in self.agents:
            if self.start_agent(name, script_path, port):
                success_count += 1
                time.sleep(2)  # Give each server time to start
        
        logger.info(f"Started {success_count}/{len(self.agents)} agent servers")
        
        if success_count > 0:
            logger.info("Waiting for servers to initialize...")
            time.sleep(5)  # Give servers time to fully initialize
            
            logger.info("Agent servers are ready!")
            logger.info("Available endpoints:")
            for name, _, port in self.agents:
                if name in self.processes:
                    logger.info(f"  {name}: http://localhost:{port}")
                    logger.info(f"  {name} agent card: http://localhost:{port}/.well-known/agent.json")
        
        return success_count
    
    def stop_all_agents(self):
        """Stop all agent servers"""
        logger.info("Stopping all agent servers...")
        
        for name, info in self.processes.items():
            try:
                process = info['process']
                logger.info(f"Stopping {name} agent server (PID: {process.pid})...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                    logger.info(f"✅ {name} agent server stopped gracefully")
                except subprocess.TimeoutExpired:
                    logger.warning(f"Force killing {name} agent server...")
                    process.kill()
                    process.wait()
                    logger.info(f"✅ {name} agent server force stopped")
                    
            except Exception as e:
                logger.error(f"Error stopping {name} agent server: {e}")
        
        self.processes.clear()
        logger.info("All agent servers stopped")
    
    def check_agent_status(self):
        """Check status of all agent servers"""
        logger.info("Checking agent server status...")
        
        for name, info in self.processes.items():
            process = info['process']
            port = info['port']
            
            if process.poll() is None:
                logger.info(f"✅ {name} agent server running on port {port} (PID: {process.pid})")
            else:
                logger.error(f"❌ {name} agent server stopped (exit code: {process.returncode})")
    
    def show_logs(self, name: str, lines: int = 10):
        """Show recent logs for a specific agent"""
        if name not in self.processes:
            logger.error(f"Agent {name} not found")
            return
        
        process = self.processes[name]['process']
        logger.info(f"Recent logs for {name} agent:")
        
        # This is a simplified version - in practice you'd want to capture logs properly
        logger.info(f"Process PID: {process.pid}, Status: {'Running' if process.poll() is None else 'Stopped'}")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("Received shutdown signal...")
    if 'manager' in globals():
        manager.stop_all_agents()
    sys.exit(0)

def main():
    """Main function"""
    global manager
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("A2A Agent Server Manager")
    logger.info("=" * 50)
    
    manager = AgentServerManager()
    
    try:
        # Start all agents
        success_count = manager.start_all_agents()
        
        if success_count == 0:
            logger.error("No agent servers started successfully. Exiting.")
            return
        
        logger.info(f"\n🚀 {success_count} agent servers are running!")
        logger.info("\nNext steps:")
        logger.info("1. Test individual agents: python3 test_individual_agents.py")
        logger.info("2. Run orchestrator: python3 src/orchestrator_client.py")
        logger.info("3. Press Ctrl+C to stop all servers")
        
        # Keep running until interrupted
        while True:
            time.sleep(10)
            manager.check_agent_status()
            
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        manager.stop_all_agents()

if __name__ == "__main__":
    main()
