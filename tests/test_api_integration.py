



"""
Test the API integration with new classification and prioritization
"""

import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api_integration():
    """Test the API with new classification and prioritization"""

    # Start the API server in a separate process
    # Note: In a real test, this would be done with a test client
    # For now, we'll simulate the API call

    # Sample task input
    task_text = "Critical security bug in the login system causing authentication failures"

    print("=== Testing API Integration ===")
    print(f"Input: {task_text}\n")

    # Simulate API call to /tasks endpoint
    # In a real test, this would be:
    # response = requests.post("http://localhost:8000/tasks", json={"input_data": task_text})

    # For now, we'll test the orchestrator directly
    from src.orchestrator.main_orchestrator import main_orchestrator

    result = main_orchestrator.process_workflow(task_text)

    print("API Response:")
    print(f"   - Task Type: {result['level2']['advanced_classification']['task_type']}")
    print(f"   - Sub-category: {result['level2']['advanced_classification']['sub_category']}")
    print(f"   - Confidence: {result['level2']['advanced_classification']['confidence']:.2f}")
    print(f"   - Domain: {result['level2']['advanced_classification']['metadata']['domain']}")
    print(f"   - Sentiment: {result['level2']['advanced_classification']['metadata']['sentiment']}")
    print(f"   - Priority Level: {result['level3']['prioritization']['priority_level']}")
    print(f"   - Priority Score: {result['level3']['prioritization']['priority_score']}")
    print(f"   - Recommendation: {result['level3']['prioritization']['recommendation']}\n")

    print("=== API Integration Test Complete ===")

    # Verify the API integration works
    assert "advanced_classification" in result["level2"]
    assert result["level2"]["advanced_classification"]["task_type"] == "bug"
    assert result["level2"]["advanced_classification"]["confidence"] > 0.7
    assert "prioritization" in result["level3"]
    assert result["level3"]["prioritization"]["priority_level"] in ["Low", "Medium", "High", "Critical"]
    assert result["level3"]["prioritization"]["priority_score"] > 0

if __name__ == "__main__":
    test_api_integration()
    print("API integration test completed successfully!")




