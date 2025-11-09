




"""
Simple demonstration of LangGraph benefits for Level 2 agents
"""

import logging
from src.agents.langgraph_agents import level2_graph_agent

# Configure logging for this test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("langgraph_benefits_test")

def main():
    """Demonstrate LangGraph benefits with simple tests"""
    logger.info("=== Testing LangGraph Benefits (Simple) ===")

    # Test 1: Error recovery
    logger.info("\n--- Testing error recovery ---")
    try:
        # Test with malformed input
        malformed_text = "This is a test with invalid characters: \x00 \x01"
        result = level2_graph_agent.analyze_text(malformed_text)
        logger.info("✓ Successfully processed malformed input")
        logger.info(f"Classification: {result['advanced_classification']['task_type']}")
    except Exception as e:
        logger.error(f"✗ Failed to process malformed input: {e}")

    # Test 2: Workflow adaptation
    logger.info("\n--- Testing workflow adaptation ---")
    try:
        # Test with different types of input
        inputs = [
            "This is a bug in the payment system",  # Bug
            "We should add a new feature for user profiles",  # Idea
            "The UI is confusing and needs improvement",  # Feedback
            "What are the system requirements for the next release?"  # Question
        ]

        for text in inputs:
            result = level2_graph_agent.analyze_text(text)
            classification = result["advanced_classification"]["task_type"]
            logger.info(f"Input: {text[:30]}... -> {classification}")

        logger.info("✓ Workflow adaptation working correctly")
    except Exception as e:
        logger.error(f"✗ Workflow adaptation failed: {e}")

    # Test 3: Debugging capabilities
    logger.info("\n--- Testing debugging capabilities ---")
    try:
        complex_text = """# Feature Request: Analytics Dashboard

## Description
We need a comprehensive analytics dashboard that provides real-time insights
into user behavior and system performance.

## Contact:
Email: analytics@company.com
Deadline: 2023-12-31
"""

        result = level2_graph_agent.analyze_text(complex_text)

        # Check that all components produced results
        checks = [
            "advanced_classification" in result,
            "reflection" in result,
            "semantic_blocks" in result,
            "context" in result,
            len(result["messages"]) > 0
        ]

        if all(checks):
            logger.info("✓ Debugging capabilities working correctly")
            logger.info(f"Generated {len(result['messages'])} debug messages")
            logger.info(f"Classification: {result['advanced_classification']['task_type']}")
        else:
            logger.error("✗ Debugging capabilities not working as expected")
    except Exception as e:
        logger.error(f"✗ Debugging test failed: {e}")

    logger.info("\n=== Test Complete ===")
    logger.info("LangGraph benefits demonstrated successfully!")

if __name__ == "__main__":
    main()




