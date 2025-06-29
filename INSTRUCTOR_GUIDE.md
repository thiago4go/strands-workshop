# Strands Workshop: Instructor Guide

## Workshop Delivery Framework

### Pre-Workshop Preparation (Critical Success Factors)

#### Technical Setup Validation
- **2 weeks before**: Test all exercises in clean environments
- **1 week before**: Send detailed setup instructions to participants
- **Day before**: Verify all demo environments and backup systems
- **30 minutes before**: Final connectivity and API key validation

#### Cognitive Load Management
- Present **one concept at a time** before adding complexity
- Use **scaffolding** to build from simple to complex
- Provide **just-in-time** information rather than overwhelming upfront
- Include **regular checkpoints** to ensure no one falls behind

### Module-by-Module Instructor Notes

## **Act I: The Single Agent (60 minutes)**

### Module 1: Basics - Hello Agent (20 minutes)

#### **Opening Hook (3 minutes)**
Start with this powerful demonstration:

```python
# Show this first - the "wow" moment
from strands import Agent

# This single line creates a fully functional AI agent!
agent = Agent()
response = agent("Explain quantum computing in simple terms")
print(response)
```

**Key Teaching Points:**
- "This is the entire agent architecture - just 3 components"
- "No complex workflows or state machines needed"
- "The model does the planning and reasoning for us"

#### **Core Concepts (7 minutes)**
Explain the **Model-Driven Revolution**:

1. **Traditional Approach** (show complexity):
   - Hand-crafted workflows
   - Rigid state machines
   - Months of development
   
2. **Strands Approach** (show simplicity):
   - Model + Tools + Prompt
   - LLM handles planning
   - Days to production

#### **Hands-on Exercise (10 minutes)**
Guide participants through `exercise1-hello-agent.py`:

```python
from strands import Agent
from strands.models import BedrockModel

# Create agent with explicit configuration
agent = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        region_name='us-east-1',
        temperature=0.3,
        system_prompt="You are a helpful assistant that provides concise responses."
    )
)

# Test the agent
response = agent("Hello! Tell me a joke.")
print(response)
```

**Common Issues & Solutions:**
- **AWS Credentials Error**: Guide through `aws configure` or environment variables
- **Model Access Denied**: Check Bedrock model access in AWS Console
- **Import Errors**: Verify virtual environment and package installation

**Success Indicator**: All participants see a joke response from their agent

### Module 2: Tools - Custom Tools (40 minutes)

#### **Opening Demonstration (5 minutes)**
Show the power of tools with this live demo:

```python
from strands import Agent, tool
from strands_tools import calculator, current_time

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city (simulated)."""
    return f"The weather in {city} is sunny, 72°F"

agent = Agent(tools=[calculator, current_time, get_weather])
response = agent("What time is it, what's 15 * 23, and what's the weather in Seattle?")
```

**Key Teaching Point**: "The agent automatically decides which tools to use and when"

#### **Tool Development Deep Dive (15 minutes)**

**Best Practices for Tool Creation:**
1. **Clear docstrings** - LLM uses these to understand purpose
2. **Type hints** - Improve reliability  
3. **Error handling** - Tools should be resilient
4. **Single responsibility** - One tool, one job

**Live Coding Session**: Build the letter_counter tool together:

```python
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
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0
    
    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")
    
    return word.lower().count(letter.lower())
```

#### **Hands-on Exercise (20 minutes)**
Guide through `exercise2-custom-tools.py`:

**Teaching Sequence:**
1. Import tools and create agent
2. Test with complex multi-tool query
3. Observe agent's reasoning process
4. Discuss tool selection strategy

**Advanced Discussion Points:**
- Tool composition and chaining
- Error handling in tools
- Performance considerations
- Security implications

**Troubleshooting Tips:**
- Tool not being called: Check docstring clarity
- Type errors: Verify type hints and validation
- Performance issues: Consider tool complexity

## **Act II: Multi-Agent Orchestration (60 minutes)**

### Module 3: Multi-Agent - Research Team (30 minutes)

#### **Conceptual Foundation (5 minutes)**
**The Collaboration Paradigm:**
- Single agents have limits
- Specialized agents work better together
- Like microservices for AI

**Show the Power of Collaboration:**
```python
# Individual specialists
researcher = Agent(system_prompt="You excel at finding accurate information")
analyst = Agent(system_prompt="You identify patterns and insights")
writer = Agent(system_prompt="You create clear, engaging content")

# Working together
topic = "Impact of AI on software development"
research = researcher(f"Research: {topic}")
analysis = analyst(f"Analyze: {research}")
article = writer(f"Write article: {analysis}")
```

#### **Orchestration Patterns (10 minutes)**

**Pattern 1: Sequential (Pipeline)**
```python
# Task flows through agents in sequence
result1 = agent1(input)
result2 = agent2(result1)
final = agent3(result2)
```

**Pattern 2: Parallel (Concurrent)**
```python
# Multiple agents work simultaneously
results = await asyncio.gather(
    agent1(task1),
    agent2(task2),
    agent3(task3)
)
```

**Pattern 3: Hierarchical (Orchestrator-Worker)**
```python
# Supervisor delegates to specialists
orchestrator = Agent(system_prompt="You coordinate team work")
specialists = [agent1, agent2, agent3]
```

#### **Hands-on Exercise (15 minutes)**
Build the research team from `exercise3-research-team.py`:

**Key Implementation Points:**
- Clear role definition for each agent
- Proper task decomposition
- Result aggregation strategies
- Error handling across agents

### Module 4: Production - Multi-Provider (30 minutes)

#### **Production Readiness Concepts (10 minutes)**

**The Production Reality:**
- APIs fail
- Rate limits hit
- Costs vary by provider
- Performance requirements differ

**Multi-Provider Strategy:**
```python
providers = [
    {"name": "Primary", "model": "bedrock/claude-3-7"},
    {"name": "Fallback", "model": "openrouter/mistral"},
    {"name": "Cost-Effective", "model": "nvidia/llama3"}
]
```

#### **Resilience Patterns (10 minutes)**

**Circuit Breaker Pattern:**
```python
class ResilientAgent:
    def __init__(self):
        self.providers = self._setup_providers()
        self.current_provider = 0
    
    def _try_providers(self, prompt):
        for provider in self.providers:
            try:
                return provider.invoke(prompt)
            except Exception as e:
                logger.warning(f"Provider {provider.name} failed: {e}")
                continue
        raise Exception("All providers failed")
```

#### **Hands-on Exercise (10 minutes)**
Implement `exercise4-multi-provider.py`:

**Focus Areas:**
- Provider configuration
- Fallback logic
- Cost optimization
- Performance monitoring

## **Act III: A2A Protocol & Deployment (60 minutes)**

### Module 5: Advanced - A2A Preview (30 minutes)

#### **A2A Protocol Introduction (10 minutes)**

**The Interoperability Vision:**
- Agents from different frameworks communicating
- Standardized discovery and negotiation
- Agent marketplace ecosystem

**Critical Caveat**: "A2A support in Strands is EXPERIMENTAL - APIs may change"

#### **Agent Cards Concept (10 minutes)**

**Agent Card Structure:**
```json
{
  "name": "Research Specialist",
  "description": "Expert at gathering information",
  "capabilities": {
    "streaming": true,
    "multiModal": false
  },
  "skills": [
    {
      "name": "web-research",
      "description": "Search and analyze web content"
    }
  ]
}
```

#### **Hands-on Exercise (10 minutes)**
Implement basic A2A communication from `exercise5-a2a-preview.py`:

**Teaching Focus:**
- Agent discovery process
- Task negotiation
- Communication protocols
- Future possibilities

### Module 6: Deployment - Lambda Deployment (30 minutes)

#### **The "Last Mile" Challenge (5 minutes)**

**Common Deployment Issues:**
- Dependency packaging
- Environment compatibility
- Cold start performance
- Monitoring and debugging

#### **Lambda Deployment Recipe (15 minutes)**

**Step-by-Step Process:**
```bash
# 1. Create project structure
mkdir lambda-agent && cd lambda-agent

# 2. Install dependencies with target
pip install strands-agents --target ./package

# 3. Package dependencies
cd package && zip -r ../deployment.zip . && cd ..

# 4. Add handler code
zip -g deployment.zip lambda_function.py

# 5. Deploy to Lambda
# (AWS Console demonstration)
```

#### **Production Considerations (10 minutes)**

**Key Topics:**
- Environment variables for API keys
- Timeout configuration
- Memory optimization
- Cost monitoring
- Error handling and logging

## Workshop Delivery Best Practices

### Timing Management
- **Buffer Time**: Add 10% buffer to each module
- **Checkpoint Strategy**: Regular "everyone caught up?" moments
- **Flexible Pacing**: Adjust based on participant progress

### Engagement Techniques
- **Live Coding**: Code together, not just watch
- **Pair Programming**: Encourage collaboration
- **Problem-Solving**: Let participants discover solutions
- **Real Examples**: Use practical, relevant scenarios

### Troubleshooting Strategy
- **Common Issues List**: Prepare solutions for frequent problems
- **Backup Plans**: Have working environments ready
- **Helper Ratio**: 1 instructor per 10 participants maximum
- **Solution Checkpoints**: Provide working code at key points

### Assessment and Validation
- **Progressive Validation**: Ensure each module works before proceeding
- **Hands-on Verification**: Participants must run code successfully
- **Concept Checking**: Quick verbal confirmations of understanding
- **Final Integration**: Complete end-to-end working system

## Post-Workshop Follow-up

### Immediate Actions
- Share all code repositories
- Provide additional resources list
- Set up community forum access
- Schedule follow-up Q&A session

### Continued Learning Path
- Advanced workshops roadmap
- Community project suggestions
- Production deployment guides
- Integration pattern examples

## Success Metrics

### During Workshop
- 90%+ completion rate for Modules 1-2
- 80%+ completion rate for Modules 3-4
- 70%+ completion rate for Modules 5-6
- Active participation and questions

### Post Workshop
- Participants can reproduce exercises independently
- Community engagement and questions
- Shared implementations and variations
- Positive feedback and recommendations
