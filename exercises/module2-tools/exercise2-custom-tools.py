#!/usr/bin/env python3
"""
Module 2: Custom Tools - Extending Agent Capabilities
Based on official Strands SDK documentation
"""

from strands import Agent, tool
from strands_tools import calculator, current_time

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
    # Input validation
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0
    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")
    
    return word.lower().count(letter.lower())

@tool
def text_reverser(text: str) -> str:
    """
    Reverse the order of characters in text.
    
    Args:
        text (str): Text to reverse
        
    Returns:
        str: Reversed text
    """
    if not isinstance(text, str):
        return "Error: Input must be a string"
    
    return text[::-1]

@tool
def word_counter(text: str) -> int:
    """
    Count the number of words in text.
    
    Args:
        text (str): Text to count words in
        
    Returns:
        int: Number of words
    """
    if not isinstance(text, str):
        return 0
    
    words = text.strip().split()
    return len(words)

def main():
    """Demonstrate custom tools with Strands agent."""
    print("🛠️  Custom Tools Demo")
    print("="*50)
    
    # Create agent with both built-in and custom tools
    agent = Agent(tools=[
        calculator,           # Built-in tool
        current_time,        # Built-in tool
        letter_counter,      # Custom tool
        text_reverser,       # Custom tool
        word_counter         # Custom tool
    ])
    
    # Show available tools
    print("Available tools:")
    for tool_name in agent.tool_names:
        print(f"  • {tool_name}")
    
    # Test the agent with questions that require different tools
    test_requests = [
        "What time is it right now?",
        "Calculate 15 * 23 + 47",
        "How many letter 'r's are in the word 'strawberry'?",
        "Reverse the text 'Hello World'",
        "How many words are in this sentence: 'The quick brown fox jumps over the lazy dog'?"
    ]
    
    print(f"\n🧪 Testing {len(test_requests)} different tool scenarios:")
    print("="*50)
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. 📝 Request: {request}")
        try:
            response = agent(request)
            print(f"   🤖 Response: {response}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Interactive mode
    print(f"\n{'='*50}")
    print("🎮 Interactive Mode - Try your own questions!")
    print("Available capabilities:")
    print("  • Mathematical calculations")
    print("  • Current time")
    print("  • Letter counting in words")
    print("  • Text reversal")
    print("  • Word counting")
    print("\nType 'quit' to exit")
    print("="*50)
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
                
            response = agent(user_input)
            print(f"🤖 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
