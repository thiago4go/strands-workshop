# main.py

import subprocess
import time
from strands.multiagent import a2a
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_a2a_research_team(topic: str):
    """
    Starts all A2A agent processes, orchestrates a research task,
    and then terminates the agent processes.
    """
    processes = []
    try:
        logger.info("Starting A2A agent processes...")
        # Start each agent in a separate subprocess.
        # The `cwd` (current working directory) is set to './src'
        # so that each agent script can find its dependencies and
        # run correctly.
        processes.append(subprocess.Popen(["python3", "research_agent.py"], cwd="./src"))
        processes.append(subprocess.Popen(["python3", "analysis_agent.py"], cwd="./src"))
        processes.append(subprocess.Popen(["python3", "factcheck_agent.py"], cwd="./src"))
        processes.append(subprocess.Popen(["python3", "qa_agent.py"], cwd="./src"))
        processes.append(subprocess.Popen(["python3", "orchestrator.py"], cwd="./src"))

        # Give agents some time to initialize and start their A2A listeners.
        # In a real-world scenario, you might want a more robust readiness check.
        logger.info("Waiting for agents to start...")
        time.sleep(15) # Increased sleep time for potentially slower Docker/MCP startups

        logger.info("Discovering Orchestrator agent...")
        # Discover the Orchestrator agent via A2A.
        # This returns a proxy object that allows us to call methods on the remote agent.
        orchestrator = a2a.discover("ResearchOrchestrator")

        logger.info(f"Conducting research on: {topic}")
        # Call the Orchestrator agent to conduct the research.
        # The Orchestrator will then communicate with other specialist agents
        # using their A2A interfaces.
        result = orchestrator(topic)

        logger.info("Research completed. Result:")
        print(result)

    except Exception as e:
        logger.error(f"An error occurred during A2A research: {e}")
    finally:
        logger.info("Terminating agent processes...")
        # Ensure all subprocesses are terminated, even if an error occurs.
        for process in processes:
            if process.poll() is None: # Check if process is still running
                process.terminate()
                process.wait() # Wait for process to actually terminate
        logger.info("All agent processes terminated.")

if __name__ == "__main__":
    # Example usage: run a research task
    research_topic = "How do multi-agent systems work with A2A communication?"
    run_a2a_research_team(research_topic)