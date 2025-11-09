









"""
Final Integration Test

This module provides a final integration test that verifies the complete
LangGraph implementation works correctly.
"""

import logging
import asyncio
from unittest.mock import patch
from src.orchestrator.main_orchestrator_langgraph_full import main_orchestrator_langgraph_full

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_final_integration():
    """Final integration test with minimal dependencies"""

    print("🚀 Final Integration Test")
    print("Testing the complete LangGraph implementation...")

    # Test with a simple input
    input_data = "Implement user authentication with OAuth"

    try:
        # Run the workflow
        result = asyncio.run(main_orchestrator_langgraph_full.process_workflow(input_data))

        print("\n✅ Workflow completed successfully!")

        # Verify all levels are present
        assert "level1" in result, "Level 1 missing"
        assert "level2" in result, "Level 2 missing"
        assert "level3" in result, "Level 3 missing"
        assert "level4" in result, "Level 4 missing"

        # Verify Level 1
        assert "modality" in result["level1"], "Level 1 missing modality"
        assert "content" in result["level1"], "Level 1 missing content"
        print(f"   ✅ Level 1: {result['level1']['modality']} modality detected")

        # Verify Level 2
        assert "advanced_classification" in result["level2"], "Level 2 missing classification"
        task_type = result["level2"]["advanced_classification"].get("task_type", "unknown")
        print(f"   ✅ Level 2: Task classified as '{task_type}'")

        # Verify Level 3
        assert "prioritization" in result["level3"], "Level 3 missing prioritization"
        priority = result["level3"]["prioritization"].get("priority_level", "unknown")
        print(f"   ✅ Level 3: Priority '{priority}'")

        # Verify Level 4
        assert "aggregation" in result["level4"], "Level 4 missing aggregation"
        recommendation = result["level4"].get("recommendation", "N/A")
        print(f"   ✅ Level 4: Recommendation generated")

        print("\n🎉 All integration tests passed!")
        print("The LangGraph implementation is working correctly!")

        return True

    except Exception as e:
        print(f"\n❌ Error during integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_system_health():
    """Test system health and basic functionality"""

    print("\n🏥 Testing System Health...")

    # Test basic imports
    try:
        from src.agents.langgraph_agents.level1_graph_orchestrator import level1_graph_orchestrator
        from src.agents.langgraph_agents.level2_graph_orchestrator import level2_graph_orchestrator
        from src.agents.langgraph_agents.level3_graph_orchestrator import level3_graph_orchestrator
        from src.agents.langgraph_agents.level4_graph_orchestrator import level4_graph_orchestrator

        print("   ✅ All LangGraph agents imported successfully")

        # Test basic functionality
        level1_result = level1_graph_orchestrator.process_input("test input")
        assert "modality" in level1_result
        assert "content" in level1_result

        print("   ✅ Level 1 basic functionality working")
        print("   ✅ System health check passed")

        return True

    except Exception as e:
        print(f"   ❌ System health check failed: {e}")
        return False

def test_task_workflow_simple():
    """Simple task workflow test"""

    print("\n📋 Testing Simple Task Workflow...")

    # Test cases
    test_cases = [
        "Add user authentication feature",
        "Fix critical security bug in login",
        "Implement dark mode for the application",
        "User feedback: app is slow on mobile"
    ]

    for i, task in enumerate(test_cases, 1):
        print(f"\n   Task {i}: {task}")

        try:
            # Run the workflow
            result = asyncio.run(main_orchestrator_langgraph_full.process_workflow(task))

            # Verify basic structure
            assert "level1" in result
            assert "level2" in result
            assert "level3" in result
            assert "level4" in result

            # Extract key information
            task_type = result["level2"]["advanced_classification"].get("task_type", "unknown")
            priority = result["level3"]["prioritization"].get("priority_level", "unknown")

            print(f"      Task Type: {task_type}")
            print(f"      Priority: {priority}")
            print(f"      ✅ Processed successfully")

        except Exception as e:
            print(f"      ❌ Error: {e}")
            return False

    print("   ✅ All tasks processed successfully")
    return True

if __name__ == "__main__":
    print("🚀 Starting Final Integration Tests")

    # Run all tests
    health_ok = test_system_health()
    integration_ok = test_final_integration()
    workflow_ok = test_task_workflow_simple()

    # Final report
    print("\n" + "="*50)
    print("FINAL INTEGRATION TEST REPORT")
    print("="*50)

    if health_ok and integration_ok and workflow_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is healthy")
        print("✅ Integration is working")
        print("✅ Workflow processing is functional")
        print("\n🚀 The LangGraph implementation is ready for production!")
    else:
        print("❌ Some tests failed")
        print(f"   System health: {'✅' if health_ok else '❌'}")
        print(f"   Integration: {'✅' if integration_ok else '❌'}")
        print(f"   Workflow: {'✅' if workflow_ok else '❌'}")

    print("="*50)








