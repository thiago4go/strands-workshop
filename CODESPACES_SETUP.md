# 🚀 GitHub Codespaces Quick Setup

**Get started with the AWS Strands Workshop in under 2 minutes!**

## Quick Start Steps

### 1. Fork the Repository
Click here to fork: [**Fork strands-workshop**](https://github.com/thiago4go/strands-workshop/fork)

### 2. Launch Codespace
After forking, click the green **"Code"** button → **"Create codespace on main"**

Or use this direct link (after forking): `https://codespaces.new/YOUR_USERNAME/strands-workshop`

### 3. Wait for Setup (2-3 minutes)
Codespaces will automatically install:
- ✅ Python 3.10+ and all dependencies
- ✅ AWS CLI and Docker
- ✅ Strands SDK and required packages
- ✅ MCP Docker images for advanced tools
- ✅ Q CLI for Amazon Q integration
- ✅ MCP Inspector UI for debugging

### 4. Configure AWS Credentials
Once setup is complete, run:
```bash
aws configure
```

Enter your AWS credentials:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region: `us-west-2` (recommended)
- Default output format: `json`

### 5. Enable Claude 3.7 Sonnet
Visit [AWS Bedrock Console](https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess) and enable Claude 3.7 Sonnet.

### 6. Verify Setup
```bash
python setup/verify_setup.py
```

### 7. Start Workshop
```bash
cd exercises/module1-basics
python exercise1-hello-agent.py
```

## What's Pre-Configured

Your Codespace includes:

### Core Dependencies
- **Python 3.10+** with virtual environment
- **AWS CLI** for Bedrock access
- **Docker** with MCP server images pre-pulled
- **Node.js** for MCP Inspector UI

### Strands SDK & Tools
- `strands-agents` - Core SDK
- `strands-agents[openai]` - OpenAI integration
- `strands-agents[litellm]` - NVIDIA NIM & OpenRouter
- `strands-agents-tools` - Built-in tools
- `strands-agents-builder` - Agent builder utilities

### Advanced Features
- **MCP CLI** for Model Context Protocol
- **A2A SDK** for agent-to-agent communication
- **Q CLI** for Amazon Q integration
- **MCP Inspector** at `http://localhost:3000`

### Pre-pulled Docker Images
- `mcp/duckduckgo` - Web search capabilities
- `mcp/sequentialthinking` - Advanced reasoning

## Optional: API Keys

Create a `.env` file for additional providers:
```bash
# Optional API Keys
OPENAI_API_KEY=sk-...
NVIDIA_API_KEY=nvapi-...
OPENROUTER_API_KEY=sk-or-...
```

## Troubleshooting

### Setup Taking Too Long?
- Codespace setup typically takes 2-3 minutes
- Check the terminal for progress updates
- If stuck, try refreshing the browser

### AWS Credentials Issues?
```bash
# Check current configuration
aws configure list

# Reconfigure if needed
aws configure
```

### Docker Not Working?
```bash
# Check Docker status
docker --version
docker info

# Restart if needed (rare in Codespaces)
sudo service docker restart
```

### Verification Failing?
```bash
# Run detailed verification
python setup/verify_setup.py

# Check specific providers
python setup/test_providers.py
```

## Why Codespaces?

- **🚀 Zero Setup**: No local installation required
- **☁️ Cloud-Powered**: 4-core CPU, 8GB RAM, fast SSD
- **🔧 Pre-Configured**: All dependencies and tools ready
- **🌐 Access Anywhere**: Works on any device with a browser
- **💰 Free Tier**: 120 core-hours/month for personal accounts

## Need Help?

- Check the [main setup guide](workshop-website/setup.html)
- Review [troubleshooting guide](setup/troubleshooting.md)
- Run verification: `python setup/verify_setup.py`

---

**Ready to build AI agents? Let's go! 🤖**
