#!/usr/bin/env python3
"""
Lambda Handler for Hello Agent
Converts the hello agent to work with AWS Lambda
"""

import json
from strands import Agent

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    
    Args:
        event: Lambda event object containing the input
        context: Lambda context object
    
    Returns:
        dict: Response object with statusCode and body
    """
    try:
        # Extract prompt from event
        # Support both direct prompt and JSON body
        if isinstance(event, dict):
            if 'prompt' in event:
                prompt = event['prompt']
            elif 'body' in event:
                # Handle API Gateway integration
                body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
                prompt = body.get('prompt', 'Tell me about agentic AI in exactly 50 words')
            else:
                prompt = 'Tell me about agentic AI in exactly 50 words'
        else:
            prompt = str(event)
        
        # Create an agent with default settings (uses Bedrock + Claude 3.7 Sonnet)
        agent = Agent()
        
        # Get response from agent
        response = agent(prompt)
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': str(response),
                'prompt': prompt
            })
        }
        
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }

# For local testing
if __name__ == "__main__":
    # Test the handler locally
    test_event = {
        'prompt': 'Tell me about agentic AI in exactly 50 words'
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
