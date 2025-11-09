








"""
Simple Integration Test

This module provides a simple test to verify the integration of LangGraph agents
without requiring external API calls.
"""

import logging
from src.agents.langgraph_agents.level1_graph_orchestrator import level1_graph_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_level1_integration():
    """Test Level 1 LangGraph integration"""

    print("🚀 Testing Level 1 LangGraph Integration")

    # Test cases
    test_cases = [
        {
            "name": "Text Input",
            "input": "This is a simple text message for testing",
            "expected_modality": "text"
        },
        {
            "name": "PDF File",
            "input": "document.pdf",
            "expected_modality": "pdf"
        },
        {
            "name": "Audio File",
            "input": "recording.mp3",
            "expected_modality": "audio"
        },
        {
            "name": "Image File",
            "input": "screenshot.png",
            "expected_modality": "image"
        }
    ]

    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"   Input: {test_case['input']}")

        try:
            # Process the input
            result = level1_graph_orchestrator.process_input(test_case["input"])

            # Verify results
            detected_modality = result.get("modality", "unknown")
            content = result.get("content", "")

            print(f"   ✅ Detected Modality: {detected_modality}")
            print(f"   ✅ Expected Modality: {test_case['expected_modality']}")
            print(f"   ✅ Content: {content[:50]}...")

            # Verify the result
            if detected_modality == test_case["expected_modality"] and content:
                print(f"   ✅ Test passed")
            else:
                print(f"   ❌ Test failed")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n✅ Level 1 Integration Test Completed")

if __name__ == "__main__":
    test_level1_integration()






