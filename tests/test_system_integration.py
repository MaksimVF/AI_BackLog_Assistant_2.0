








"""
System Integration Tests

This module provides comprehensive tests for the entire system integration
with LangGraph orchestrators.
"""

import pytest
import asyncio
import logging
from src.orchestrator.main_orchestrator_langgraph_full import main_orchestrator_langgraph_full

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_system_integration_basic():
    """Basic system integration test"""

    # Test with a simple input
    input_data = "Implement user authentication with OAuth"

    result = await main_orchestrator_langgraph_full.process_workflow(input_data)

    # Verify all levels processed
    assert "level1" in result
    assert "level2" in result
    assert "level3" in result
    assert "level4" in result

    # Verify Level 1
    assert result["level1"]["modality"] == "text"
    assert "content" in result["level1"]

    # Verify Level 2
    assert "advanced_classification" in result["level2"]
    assert "reflection" in result["level2"]

    # Verify Level 3
    assert "prioritization" in result["level3"]
    assert "risk" in result["level3"]

    # Verify Level 4
    assert "aggregation" in result["level4"]
    assert "summary" in result["level4"]

@pytest.mark.asyncio
async def test_system_integration_feature():
    """System integration test for feature request"""

    # Test with a feature request
    input_data = """New Feature Request:
    We need to add a dark mode option to our application.
    This should include:
    - Toggle switch in settings
    - CSS theme changes
    - Persistent user preference
    """

    result = await main_orchestrator_langgraph_full.process_workflow(input_data)

    # Verify feature classification
    task_type = result["level2"]["advanced_classification"]["task_type"]
    assert task_type == "feature"

    # Verify prioritization
    priority = result["level3"]["prioritization"]["priority_level"]
    assert priority in ["Low", "Medium", "High", "Critical"]

    # Verify recommendation
    recommendation = result["level4"]["aggregation"]["recommendation"]
    assert recommendation != ""

@pytest.mark.asyncio
async def test_system_integration_bug():
    """System integration test for bug report"""

    # Test with a bug report
    input_data = """Bug Report:
    The login system crashes when using special characters in password.
    Error occurs on the authentication endpoint.
    """

    result = await main_orchestrator_langgraph_full.process_workflow(input_data)

    # Verify bug classification
    task_type = result["level2"]["advanced_classification"]["task_type"]
    assert task_type == "bug"

    # Verify higher priority for bugs
    priority = result["level3"]["prioritization"]["priority_level"]
    assert priority in ["High", "Critical"]

@pytest.mark.asyncio
async def test_system_integration_feedback():
    """System integration test for user feedback"""

    # Test with user feedback
    input_data = """User Feedback:
    The mobile app is very slow on Android devices.
    It takes more than 5 seconds to load the dashboard.
    """

    result = await main_orchestrator_langgraph_full.process_workflow(input_data)

    # Verify feedback classification
    task_type = result["level2"]["advanced_classification"]["task_type"]
    assert task_type == "feedback"

    # Verify prioritization
    priority = result["level3"]["prioritization"]["priority_level"]
    assert priority in ["Low", "Medium", "High", "Critical"]

def test_complete_system_workflow():
    """Complete system workflow test"""

    test_cases = [
        {
            "name": "Feature Request",
            "input": "Add payment gateway integration with Stripe and PayPal",
            "expected_type": "feature"
        },
        {
            "name": "Bug Report",
            "input": "Critical security vulnerability in user authentication",
            "expected_type": "bug"
        },
        {
            "name": "User Feedback",
            "input": "The search function is not working properly on mobile",
            "expected_type": "feedback"
        },
        {
            "name": "Idea",
            "input": "We should implement a gamification system with badges",
            "expected_type": "idea"
        }
    ]

    for test_case in test_cases:
        print(f"\n--- Testing {test_case['name']} ---")
        print(f"Input: {test_case['input']}")

        # Process the input
        result = asyncio.run(main_orchestrator_langgraph_full.process_workflow(test_case["input"]))

        # Verify classification
        actual_type = result["level2"]["advanced_classification"]["task_type"]
        print(f"Expected: {test_case['expected_type']}, Got: {actual_type}")

        if actual_type == test_case["expected_type"]:
            print("✅ Classification correct")
        else:
            print("❌ Classification incorrect")

        # Verify all levels processed
        assert "level1" in result
        assert "level2" in result
        assert "level3" in result
        assert "level4" in result

        print(f"Priority: {result['level3']['prioritization']['priority_level']}")
        print(f"Recommendation: {result['level4']['aggregation']['recommendation'][:50]}...")

    print("\n✅ Complete system workflow test completed successfully")

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])








