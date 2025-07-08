
# Exercise 5: A2A Research Team - Decoupled Multi-Agent Orchestration

This directory contains a refactored version of the multi-agent research team that uses a decoupled, A2A (Agent-to-Agent) architecture. Each agent runs in its own process and communicates with the orchestrator via the A2A protocol.

## Architecture

The new architecture is composed of the following files, located in the `src` directory:

- `research_agent.py`: The specialized research agent.
- `analysis_agent.py`: The specialized analysis agent.
- `factcheck_agent.py`: The specialized fact-checking agent.
- `qa_agent.py`: The specialized quality assurance agent.
- `orchestrator.py`: The main orchestrator that will manage the other agents.
- `main.py`: The entry point to run the A2A research team.

## Running the A2A Research Team

To run the new A2A research team, you would typically execute the `main.py` script in this directory:

```bash
python3 main.py
```

However, there is a known issue with installing the `strands` library, which is a core dependency for this project. The installation fails due to a build error related to missing system-level dependencies. Until this issue is resolved, the code in this directory is intended for illustrative purposes only.

## A2A Pattern

The code in this directory demonstrates the A2A pattern, where each agent is a standalone process that communicates with other agents over the network. This is a more robust and scalable approach to building multi-agent systems than the "agents-as-tools" pattern.

The key concepts of the A2A pattern are:

- **`a2a.listen`**: This function is used to start an agent and make it available for other agents to communicate with.
- **`a2a.discover`**: This function is used to find and get a proxy for an agent that is listening on the network.

By using these two functions, you can build complex multi-agent systems where agents can be added, removed, and updated independently of each other.
