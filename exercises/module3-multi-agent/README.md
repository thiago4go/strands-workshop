# Multi-Agent Exercise - Fixed Version

## Overview
This exercise demonstrates a working multi-agent system using the Model Context Protocol (MCP) with Strands Agents.

## Fixes Applied

### 1. Environment Configuration
- Added proper loading of environment variables from `.env` file using `python-dotenv`
- Added validation to ensure `OPENAI_API_KEY` is available

### 2. Model Configuration
- Configured `LiteLLMModel` with OpenAI API key from environment variables
- Set model to `gpt-4o-mini` for cost-effective testing
- Added proper temperature setting (0.3)

### 3. MCP Client Fixes
- Removed call to non-existent `list_resources_sync()` method
- Fixed tool attribute access (MCPAgentTool objects don't have `.name` attribute)
- Improved error handling in the test integration function

### 4. Quiz Logic Improvements
- Enhanced `submit_answer` function to handle both direct answers and option numbers
- Added proper parsing for option selection (1-4)
- Improved feedback messages for correct/incorrect answers

### 5. Error Handling
- Added try-catch blocks around agent calls
- Added validation for environment variables
- Improved error messages and logging

## Usage

### Run the Demo (Default)
```bash
cd /home/thiago/agentic-era/on-agents/agents-workspace/strands-workshop
source .venv/bin/activate
python exercises/module3-multi-agent/exercise3-multi-agents.py
```

### Run in Interactive Mode
```bash
python exercises/module3-multi-agent/exercise3-multi-agents.py --interactive
```

### Run as MCP Server Only
```bash
python exercises/module3-multi-agent/exercise3-multi-agents.py --server
```

## Features

### Calculator Tools
- `add(a, b)`: Addition
- `multiply(a, b)`: Multiplication  
- `power(base, exponent)`: Exponentiation

### Quiz Tools
- `start_quiz(topic, user_id)`: Start a quiz on Python or Math topics
- `submit_answer(answer, user_id)`: Submit an answer (supports option numbers 1-4 or direct answers)

## Environment Requirements
- Python 3.8+
- Virtual environment with required packages installed
- `.env` file with `OPENAI_API_KEY` configured

## Test Results
The script now successfully:
- ✅ Loads environment variables
- ✅ Configures the model with API credentials
- ✅ Starts the MCP server
- ✅ Connects the agent client to the server
- ✅ Executes calculator operations
- ✅ Runs interactive quizzes
- ✅ Handles both interactive and automated modes
