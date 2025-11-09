



"""
Test script for Main Orchestrator with LangGraph
"""

import logging
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator.main_orchestrator_langgraph import main_orchestrator_langgraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_main_orchestrator_langgraph():
    """Test the Main Orchestrator with LangGraph"""

    # Test cases
    test_cases = [
        {
            "name": "Simple text task",
            "input": "Create a new feature for user authentication",
            "expected_modality": "text"
        },
        {
            "name": "PDF document",
            "input": "requirements.pdf",
            "expected_modality": "pdf"
        }
    ]

    for test_case in test_cases:
        print(f"\n--- Testing {test_case['name']} ---")
        print(f"Input: {test_case['input']}")

        # Process the input through the entire workflow
        result = main_orchestrator_langgraph.process_workflow(test_case['input'])

        # Verify Level 1 results
        level1 = result.get("level1", {})
        detected_modality = level1.get("modality", "unknown")
        print(f"Detected modality: {detected_modality}")
        print(f"Expected modality: {test_case['expected_modality']}")

        # Verify Level 2 results
        level2 = result.get("level2", {})
        task_type = level2.get("advanced_classification", {}).get("task_type", "unknown")
        print(f"Task type: {task_type}")

        # Verify Level 3 results
        level3 = result.get("level3", {})
        priority = level3.get("prioritization", {}).get("priority_level", "N/A")
        print(f"Priority: {priority}")

        # Verify Level 4 results
        level4 = result.get("level4", {})
        recommendation = level4.get("recommendation", "N/A")
        print(f"Recommendation: {recommendation}")

        # Verify the result
        if detected_modality == test_case['expected_modality']:
            print("✅ Test passed")
        else:
            print("❌ Test failed")

if __name__ == "__main__":
    test_main_orchestrator_langgraph()



