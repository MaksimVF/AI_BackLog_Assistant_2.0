
#!/usr/bin/env python3

"""
Test script to verify the Mistral API connection works correctly
"""

import os
from src.utils.llm_client import LLMClient

def test_mistral_connection():
    """Test the Mistral API connection"""
    print("Testing Mistral API connection...")

    # Create LLM client
    client = LLMClient()

    # Test with a simple prompt
    test_prompt = "Say 'Hello, World!'"

    print(f"Sending test prompt: {test_prompt}")
    response = client.generate_text(test_prompt)

    print(f"Response: {response}")

    # Check if we got a response
    if response:
        print("✅ Connection test successful!")
        return True
    else:
        print("❌ Connection test failed!")
        return False

if __name__ == "__main__":
    test_mistral_connection()
