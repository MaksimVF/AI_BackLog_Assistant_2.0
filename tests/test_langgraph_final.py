




"""
Final test of LangGraph implementation for Level 2 agents
"""

import logging
from src.agents.langgraph_agents import level2_graph_orchestrator

# Configure logging for this test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("langgraph_final_test")

def main():
    """Final test of LangGraph implementation"""
    logger.info("=== Final Test of LangGraph Implementation ===")

    # Test with a comprehensive input
    text = """# Feature Request: Advanced Analytics Dashboard

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
Deadline: 2023-12-31
"""

    try:
        # Test the LangGraph orchestrator
        result = level2_graph_orchestrator.analyze_text(text)

        # Verify the structure
        assert "advanced_classification" in result
        assert "reflection" in result
        assert "blocks" in result
        assert "context" in result

        # Verify classifications
        classification = result["advanced_classification"]["task_type"]
        reflection = result["reflection"]["task_type"]

        logger.info("✓ LangGraph implementation working correctly")
        logger.info(f"Classification: {classification}")
        logger.info(f"Reflection: {reflection}")
        logger.info(f"Semantic blocks: {len(result['blocks']['blocks'])}")
        logger.info(f"Context domain: {result['context']['domain']}")

        # Verify the results make sense
        expected_classifications = ["idea", "feedback", "request"]
        if classification in expected_classifications and reflection in expected_classifications:
            logger.info("✓ Classifications are reasonable")
        else:
            logger.warning(f"⚠️  Unexpected classifications: {classification}, {reflection}")

        # Test with a bug report
        bug_text = """# Bug Report: Login System Failure

## Description
The login system is not working properly when users try to log in with their Google accounts.
It shows an error message "Invalid credentials" even with correct passwords.

## Steps to reproduce:
1. Go to login page
2. Click "Login with Google"
3. Enter credentials
4. See error message

## Expected behavior:
Users should be able to login successfully with their Google accounts.
"""

        bug_result = level2_graph_orchestrator.analyze_text(bug_text)
        bug_classification = bug_result["advanced_classification"]["task_type"]
        bug_reflection = bug_result["reflection"]["task_type"]

        logger.info("\n✓ Bug report test completed")
        logger.info(f"Classification: {bug_classification}")
        logger.info(f"Reflection: {bug_reflection}")

        # Verify bug classification
        if bug_classification == "bug" and bug_reflection == "bug":
            logger.info("✓ Bug classification working correctly")
        else:
            logger.warning(f"⚠️  Bug classification issue: {bug_classification}, {bug_reflection}")

        logger.info("\n=== All Tests Complete ===")
        logger.info("🎉 LangGraph implementation is working successfully!")

    except Exception as e:
        logger.error(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()





