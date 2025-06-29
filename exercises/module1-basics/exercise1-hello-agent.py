#!/usr/bin/env python3
"""
Module 1: Hello Agent - Your First Strands Agent
Based on official Strands SDK documentation
"""

from strands import Agent

def main():
    """Create and test your first Strands agent."""
    print("🤖 Creating your first Strands agent...")
    
    # Create an agent with default settings (uses Bedrock + Claude 3.7 Sonnet)
    agent = Agent()
    
    # Ask the agent a question
    print("\n📝 Asking: 'Tell me about agentic AI in exactly 50 words'")
    response = agent("Tell me about agentic AI in exactly 50 words")
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    # Test with a few more questions
    test_questions = [
        "What is the capital of France?",
        "Explain machine learning in one sentence.",
        "What's 15 * 23?"
    ]
    
    print("\n" + "="*50)
    print("Testing with additional questions:")
    print("="*50)
    
    for question in test_questions:
        print(f"\n❓ Q: {question}")
        response = agent(question)
        print(f"🤖 A: {response}")

if __name__ == "__main__":
    main()
