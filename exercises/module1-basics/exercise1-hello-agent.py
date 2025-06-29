from strands import Agent
from strands.models import BedrockModel

# Create a BedrockModel
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name='us-east-1',
    temperature=0.3,
    system_prompt="You are a helpful assistant that provides concise responses."

)

agent = Agent(model=bedrock_model)

# Send a message to the agent
response = agent("Hello! Tell me a joke.")
