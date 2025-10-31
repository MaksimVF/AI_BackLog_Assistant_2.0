
"""
Integration test for the full workflow including task prioritization
"""

import pytest
from src.orchestrator.main_orchestrator import main_orchestrator

def test_full_workflow_with_prioritization():
    """Test the complete workflow including task prioritization"""

    # Test with a critical bug
    critical_bug = "Critical security vulnerability affecting all users. Urgent fix needed ASAP."

    print("=== Testing Full Workflow with Prioritization ===")
    print(f"Input: {critical_bug}\n")

    result = main_orchestrator.process_workflow(critical_bug)

    # Verify the workflow completed successfully
    assert "level1" in result
    assert "level2" in result
    assert "level3" in result
    assert "level4" in result

    # Verify level 2 provides classification
    classification = result["level2"].get("reflection", {}).get("task_type")
    assert classification in ["bug", "idea", "feedback"]

    # Verify level 3 includes prioritization
    assert "prioritization" in result["level3"]
    prioritization = result["level3"]["prioritization"]

    # Verify prioritization details
    assert "priority_score" in prioritization
    assert "priority_level" in prioritization
    assert "recommendation" in prioritization

    # For a critical bug, priority should be high
    assert prioritization["priority_score"] > 50
    assert prioritization["priority_level"] in ["High", "Critical"]

    print(f"Classification: {classification}")
    print(f"Priority Level: {prioritization['priority_level']}")
    print(f"Priority Score: {prioritization['priority_score']}")
    print(f"Recommendation: {prioritization['recommendation']}")

    print("Full workflow test completed successfully!")

if __name__ == "__main__":
    test_full_workflow_with_prioritization()
