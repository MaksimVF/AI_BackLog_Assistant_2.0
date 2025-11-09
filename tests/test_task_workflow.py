







"""
Task Workflow Test

This module provides a simple test to verify the complete task workflow
using LangGraph orchestrators.
"""

import asyncio
from src.orchestrator.main_orchestrator_langgraph_full import main_orchestrator_langgraph_full

def test_task_workflow():
    """Test a complete task workflow"""

    print("🚀 Starting Task Workflow Test")

    # Test cases
    test_cases = [
        {
            "name": "Feature Request",
            "input": "Add user authentication with OAuth and social login options",
            "expected_type": "feature"
        },
        {
            "name": "Bug Report",
            "input": "Critical security bug in payment processing",
            "expected_type": "bug"
        },
        {
            "name": "User Feedback",
            "input": "The mobile app is very slow and crashes frequently",
            "expected_type": "feedback"
        },
        {
            "name": "Idea",
            "input": "Implement AI-powered chatbot for customer support",
            "expected_type": "idea"
        }
    ]

    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"   Input: {test_case['input']}")

        try:
            # Process the task
            result = asyncio.run(main_orchestrator_langgraph_full.process_workflow(test_case["input"]))

            # Extract key information
            task_type = result["level2"]["advanced_classification"]["task_type"]
            priority = result["level3"]["prioritization"]["priority_level"]
            recommendation = result["level4"]["aggregation"]["recommendation"]

            print(f"   ✅ Task Type: {task_type}")
            print(f"   ✅ Priority: {priority}")
            print(f"   ✅ Recommendation: {recommendation[:50]}...")

            # Verify expected classification
            if task_type == test_case["expected_type"]:
                print(f"   ✅ Classification correct")
            else:
                print(f"   ❌ Classification incorrect (expected {test_case['expected_type']})")

        except Exception as e:
            print(f"   ❌ Error processing task: {e}")
            import traceback
            traceback.print_exc()

    print("\n✅ Task Workflow Test Completed")

if __name__ == "__main__":
    test_task_workflow()





