

"""
Test script for Level 1 LangGraph implementation
"""

import logging
import asyncio
from src.agents.langgraph_agents.level1_graph_agent import Level1GraphAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_level1_graph_agent():
    """Test the Level 1 Graph Agent"""

    # Create the agent
    agent = Level1GraphAgent()

    # Test cases
    test_cases = [
        {
            "name": "Text input",
            "input": "This is a simple text message",
            "expected_modality": "text"
        },
        {
            "name": "PDF file path",
            "input": "document.pdf",
            "expected_modality": "pdf"
        },
        {
            "name": "Audio file path",
            "input": "recording.mp3",
            "expected_modality": "audio"
        },
        {
            "name": "Image file path",
            "input": "screenshot.png",
            "expected_modality": "image"
        }
    ]

    for test_case in test_cases:
        print(f"\n--- Testing {test_case['name']} ---")
        print(f"Input: {test_case['input']}")

        # Process the input
        result = agent.process_input(test_case['input'])

        detected_modality = result["modality_detection"].get("modality", "unknown")
        print(f"Detected modality: {detected_modality}")
        print(f"Expected modality: {test_case['expected_modality']}")
        print(f"Content: {result['input_processing'].get('content', '')[:100]}...")  # Show first 100 chars

        # Verify the result
        if detected_modality == test_case['expected_modality']:
            print("✅ Test passed")
        else:
            print("❌ Test failed")

        # Show metadata
        print(f"Metadata keys: {list(result.keys())}")

if __name__ == "__main__":
    test_level1_graph_agent()

