

"""
Simple test to verify the integration is working
"""

from src.orchestrator.main_orchestrator import main_orchestrator

def test_simple_integration():
    """Test the integration with a simple example"""

    # Test with different types of inputs
    test_cases = [
        ("Critical security vulnerability affecting all users. Urgent fix needed ASAP.", "bug"),
        ("New feature to increase user engagement by 30% with detailed implementation plan.", "idea"),
        ("The UI could be improved with better color contrast.", "feedback")
    ]

    for text, expected_classification in test_cases:
        print(f"\n=== Testing: {text[:50]}...")
        result = main_orchestrator.process_workflow(text)

        # Verify basic structure
        assert "level1" in result
        assert "level2" in result
        assert "level3" in result
        assert "level4" in result

        # Verify classification
        classification = result["level2"].get("reflection", {}).get("task_type")
        print(f"Classification: {classification} (expected: {expected_classification})")

        # Verify prioritization exists
        assert "prioritization" in result["level3"]
        prioritization = result["level3"]["prioritization"]

        print(f"Priority Level: {prioritization['priority_level']}")
        print(f"Priority Score: {prioritization['priority_score']}")
        print(f"Recommendation: {prioritization['recommendation']}")

        # Verify prioritization has expected structure
        assert "priority_score" in prioritization
        assert "priority_level" in prioritization
        assert "recommendation" in prioritization

        print("✓ Test passed")

    print("\nAll integration tests passed!")

if __name__ == "__main__":
    test_simple_integration()

