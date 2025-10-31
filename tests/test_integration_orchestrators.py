


"""
Integration test for the updated orchestrators with new classification and prioritization
"""

from src.orchestrator.level2_orchestrator import level2_orchestrator
from src.orchestrator.level3_orchestrator import level3_orchestrator

def test_integrated_orchestrators():
    """Test the integrated orchestrators with new components"""

    # Sample task input
    task_text = "Critical security bug in the login system causing authentication failures"

    print("=== Testing Integrated Orchestrators ===")
    print(f"Input: {task_text}\n")

    # Test Level 2 Orchestrator
    print("1. Level 2 Orchestrator:")
    level2_result = level2_orchestrator.analyze_text(task_text)
    print(f"   - Advanced classification: {level2_result['advanced_classification']['task_type']}")
    print(f"   - Sub-category: {level2_result['advanced_classification']['sub_category']}")
    print(f"   - Confidence: {level2_result['advanced_classification']['confidence']:.2f}")
    print(f"   - Domain: {level2_result['advanced_classification']['metadata']['domain']}")
    print(f"   - Sentiment: {level2_result['advanced_classification']['metadata']['sentiment']}\n")

    # Test Level 3 Orchestrator (using the classified task type)
    task_type = level2_result['advanced_classification']['task_type']
    print("2. Level 3 Orchestrator:")
    level3_result = level3_orchestrator.analyze_task(task_text, task_type)
    print(f"   - Priority score: {level3_result['prioritization']['priority_score']}")
    print(f"   - Priority level: {level3_result['prioritization']['priority_level']}")
    print(f"   - Recommendation: {level3_result['prioritization']['recommendation']}")
    print(f"   - Risk score: {level3_result['prioritization']['risk_score']}")
    print(f"   - Impact score: {level3_result['prioritization']['impact_score']}")
    print(f"   - Urgency score: {level3_result['prioritization']['urgency_score']}\n")

    print("=== Integration Test Complete ===")

    # Verify the integration works
    assert "advanced_classification" in level2_result
    assert level2_result['advanced_classification']['task_type'] == "bug"
    assert level2_result['advanced_classification']['confidence'] > 0.7
    assert "prioritization" in level3_result
    assert level3_result['prioritization']['priority_score'] > 0
    assert level3_result['prioritization']['priority_level'] in ["Low", "Medium", "High", "Critical"]

if __name__ == "__main__":
    test_integrated_orchestrators()
    print("Integration test completed successfully!")



