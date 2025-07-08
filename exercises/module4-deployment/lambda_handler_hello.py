import json
from strands import Agent

# Create the agent outside the handler for warm starts
# This ensures the agent is loaded only once per Lambda instance
hello_agent = Agent()

def handler(event, context):
    # Extract the prompt from the Lambda event
    # Assuming the event payload is JSON with a 'prompt' key
    try:
        body = json.loads(event.get('body', '{}'))
        user_prompt = body.get('prompt', 'Hello!')
    except json.JSONDecodeError:
        user_prompt = event.get('prompt', 'Hello!') # Fallback for non-JSON or direct invocation

    # Invoke the Strands agent
    response = hello_agent(user_prompt)

    # Return the response in a format API Gateway can understand
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'response': str(response)
        })
    }
