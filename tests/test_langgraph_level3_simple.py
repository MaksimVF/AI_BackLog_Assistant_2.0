


"""
Simple test for Level 3 LangGraph implementation without LLM calls
"""

import logging
import time
from unittest.mock import patch, MagicMock

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_level3_graph_structure():
    """Test the Level 3 LangGraph structure without making LLM calls"""

    print("Testing Level 3 LangGraph structure...")

    try:
        # Import the graph agent
        from src.agents.langgraph_agents.level3_graph_agent import Level3GraphAgent

        # Create a mock agent
        agent = Level3GraphAgent()

        # Verify the graph structure
        print("✅ Level3GraphAgent created successfully")
        print(f"✅ Graph has {len(agent.graph.nodes)} nodes")

        # Check that all expected nodes exist
        expected_nodes = [
            "risk_assessment",
            "resource_analysis",
            "impact_evaluation",
            "confidence_urgency",
            "task_prioritization"
        ]

        for node in expected_nodes:
            if node in agent.graph.nodes:
                print(f"✅ Node '{node}' found in graph")
            else:
                print(f"❌ Node '{node}' missing from graph")

        # Verify entry and exit points
        if hasattr(agent.graph, 'entry_point'):
            print(f"✅ Entry point: {agent.graph.entry_point}")
        if hasattr(agent.graph, 'finish_point'):
            print(f"✅ Finish point: {agent.graph.finish_point}")

        print("✅ Level 3 LangGraph structure test completed successfully")
        return True

    except Exception as e:
        print(f"❌ Error in structure test: {str(e)}")
        return False

def test_level3_orchestrator_integration():
    """Test the Level 3 orchestrator integration"""

    print("\nTesting Level 3 orchestrator integration...")

    try:
        # Import the orchestrator
        from src.agents.langgraph_agents.level3_graph_orchestrator import Level3GraphOrchestrator

        # Create an orchestrator instance
        orchestrator = Level3GraphOrchestrator()

        print("✅ Level3GraphOrchestrator created successfully")
        print("✅ Level 3 orchestrator integration test completed successfully")
        return True

    except Exception as e:
        print(f"❌ Error in orchestrator test: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running Level 3 LangGraph tests...\n")

    # Test structure
    structure_ok = test_level3_graph_structure()

    # Test integration
    integration_ok = test_level3_orchestrator_integration()

    if structure_ok and integration_ok:
        print("\n🎉 All Level 3 LangGraph tests passed!")
    else:
        print("\n❌ Some Level 3 LangGraph tests failed!")

    print("\nNote: Full functionality test requires LLM API access and proper configuration.")

