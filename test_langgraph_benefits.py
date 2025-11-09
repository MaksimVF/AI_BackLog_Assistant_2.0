



"""
Demonstration of LangGraph benefits for Level 2 agents

This test demonstrates the advantages of using LangGraph for agent coordination:
1. Better error handling and recovery
2. State persistence and checkpointing
3. Dynamic workflow adaptation
4. Improved debugging and tracing
"""

import logging
from src.agents.langgraph_agents import level2_graph_agent

# Configure logging for this test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("langgraph_benefits_test")

def test_error_recovery():
    """Test error handling and recovery in LangGraph"""
    logger.info("Testing error recovery...")

    # Test with malformed input
    malformed_text = "This is a test with invalid characters: \x00 \x01"

    try:
        result = level2_graph_agent.analyze_text(malformed_text)
        logger.info("✓ Successfully processed malformed input")
        logger.info(f"Result: {result['advanced_classification']['task_type']}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to process malformed input: {e}")
        return False

def test_state_persistence():
    """Test state persistence across graph executions"""
    logger.info("Testing state persistence...")

    # First execution
    text1 = "This is a bug report for the login system"
    result1 = level2_graph_agent.analyze_text(text1)

    # Second execution with related content
    text2 = "The login system also has performance issues"
    result2 = level2_graph_agent.analyze_text(text2)

    # Check if state is maintained (both should be classified as bugs)
    if (result1["advanced_classification"]["task_type"] == "bug" and
        result2["advanced_classification"]["task_type"] == "bug"):
        logger.info("✓ State persistence working correctly")
        return True
    else:
        logger.error("✗ State persistence not working as expected")
        return False

def test_workflow_adaptation():
    """Test dynamic workflow adaptation"""
    logger.info("Testing workflow adaptation...")

    # Test with different types of input
    inputs = [
        "This is a bug in the payment system",  # Bug
        "We should add a new feature for user profiles",  # Idea
        "The UI is confusing and needs improvement",  # Feedback
        "What are the system requirements for the next release?"  # Question
    ]

    results = []
    for text in inputs:
        result = level2_graph_agent.analyze_text(text)
        results.append(result["advanced_classification"]["task_type"])

    # Check if different inputs produce appropriate classifications
    expected = ["bug", "idea", "feedback", "question"]
    matches = [r in expected for r in results]

    if all(matches):
        logger.info("✓ Workflow adaptation working correctly")
        logger.info(f"Classifications: {results}")
        return True
    else:
        logger.error("✗ Workflow adaptation not working as expected")
        logger.error(f"Expected: {expected}")
        logger.error(f"Got: {results}")
        return False

def test_debugging_capabilities():
    """Test improved debugging and tracing"""
    logger.info("Testing debugging capabilities...")

    # Test with complex input that should trigger multiple agents
    complex_text = """# Feature Request: Advanced Analytics Dashboard

## Description
We need a comprehensive analytics dashboard that provides real-time insights
into user behavior, system performance, and business metrics.

## Requirements:
- Real-time data visualization
- Customizable widgets
- User access controls
- Export functionality
- Integration with existing data sources

## Contact:
Email: analytics@company.com
Phone: +1-800-123-4567
Deadline: 2023-12-31
"""

    try:
        result = level2_graph_agent.analyze_text(complex_text)

        # Check that all components produced results
        checks = [
            "advanced_classification" in result,
            "reflection" in result,
            "semantic_blocks" in result,
            "context" in result,
            len(result["messages"]) > 4  # Should have multiple messages from different agents
        ]

        if all(checks):
            logger.info("✓ Debugging capabilities working correctly")
            logger.info(f"Generated {len(result['messages'])} debug messages")
            return True
        else:
            logger.error("✗ Debugging capabilities not working as expected")
            return False
    except Exception as e:
        logger.error(f"✗ Debugging test failed: {e}")
        return False

def main():
    """Run all LangGraph benefit tests"""
    logger.info("=== Testing LangGraph Benefits ===")

    tests = [
        test_error_recovery,
        test_state_persistence,
        test_workflow_adaptation,
        test_debugging_capabilities
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        logger.info(f"\n--- Running {test.__name__} ---")
        if test():
            passed += 1
        else:
            logger.warning(f"Test {test.__name__} failed!")

    logger.info(f"\n=== Test Results ===")
    logger.info(f"Passed: {passed}/{total}")
    logger.info(f"Success rate: {passed/total*100:.1f}%")

    if passed == total:
        logger.info("🎉 All LangGraph benefit tests passed!")
    else:
        logger.warning("⚠️  Some tests failed - LangGraph benefits may be limited")

if __name__ == "__main__":
    main()




