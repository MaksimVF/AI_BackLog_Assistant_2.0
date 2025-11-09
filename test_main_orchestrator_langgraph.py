


"""
Test for Main Orchestrator with LangGraph

This test verifies the functionality of the main orchestrator using LangGraph for Level 4 processing.
"""

import logging
import json
import asyncio
from src.orchestrator.main_orchestrator_langgraph import main_orchestrator_langgraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_main_orchestrator_langgraph():
    """Test the Main Orchestrator with LangGraph"""

    # Sample input data for testing
    sample_input = "Implement user authentication with OAuth2 and JWT for our web application. This should include login, logout, and token refresh functionality."

    print("Testing Main Orchestrator with LangGraph...")
    print("Input data:", sample_input)

    # Process the workflow
    result = await main_orchestrator_langgraph.process_workflow(sample_input)

    print("\nResults:")
    print("Level 1:", json.dumps(result.get("level1", {}), indent=2))
    print("Level 2:", json.dumps(result.get("level2", {}), indent=2))
    print("Level 3:", json.dumps(result.get("level3", {}), indent=2))
    print("Level 4:", json.dumps(result.get("level4", {}), indent=2))

    # Verify that all expected components are present
    assert "level1" in result, "Missing Level 1 result"
    assert "level2" in result, "Missing Level 2 result"
    assert "level3" in result, "Missing Level 3 result"
    assert "level4" in result, "Missing Level 4 result"
    assert result.get("langgraph_enabled", False), "LangGraph not enabled"

    # Check Level 4 structure
    level4 = result["level4"]
    assert "aggregation" in level4, "Missing aggregation in Level 4"
    assert "visualization" in level4, "Missing visualization in Level 4"
    assert "summary" in level4, "Missing summary in Level 4"
    assert "enhanced_summary" in level4, "Missing enhanced summary in Level 4"

    print("\n✅ All tests passed! Main Orchestrator with LangGraph is working correctly.")

if __name__ == "__main__":
    asyncio.run(test_main_orchestrator_langgraph())


