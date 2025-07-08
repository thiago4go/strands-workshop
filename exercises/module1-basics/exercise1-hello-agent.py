#!/usr/bin/env python3
"""
Module 1: Hello Agent - Your First Strands Agent
Based on official Strands SDK documentation
"""

from strands import Agent

def main():
   
    # Create an agent with default settings (uses Bedrock + Claude 3.7 Sonnet)
    agent = Agent()

    agent("Tell me about agentic AI in exactly 50 words")
    
if __name__ == "__main__":
    main()
