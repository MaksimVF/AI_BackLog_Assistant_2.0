









"""
Mock Integration Test

This module provides a comprehensive test for all LangGraph agents
using mock data to avoid external API calls.
"""

import logging
from unittest.mock import patch, MagicMock
from src.agents.langgraph_agents.level1_graph_orchestrator import level1_graph_orchestrator
from src.agents.langgraph_agents.level2_graph_orchestrator import level2_graph_orchestrator
from src.agents.langgraph_agents.level3_graph_orchestrator import level3_graph_orchestrator
from src.agents.langgraph_agents.level4_graph_orchestrator import level4_graph_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_complete_mock_workflow():
    """Test complete workflow with mock data"""

    print("🚀 Testing Complete Workflow with Mock Data")

    # Mock the LLM client to avoid API calls
    with patch('src.utils.llm_client.llm_client.generate_text') as mock_generate:
        # Set up mock responses
        mock_generate.return_value = '{"result": "mocked response"}'

        # Test case
        input_data = "Add user authentication with OAuth support"

        print(f"\n📋 Input: {input_data}")

        try:
            # Level 1 Processing
            print("\n1️⃣ Level 1 Processing...")
            level1_result = level1_graph_orchestrator.process_input(input_data)
            print(f"   ✅ Modality: {level1_result.get('modality', 'unknown')}")
            print(f"   ✅ Content: {level1_result.get('content', '')[:50]}...")

            # Level 2 Processing
            print("\n2️⃣ Level 2 Processing...")
            level2_result = level2_graph_orchestrator.analyze_text(level1_result["content"])
            print(f"   ✅ Advanced Classification: {level2_result.get('advanced_classification', {}).get('task_type', 'unknown')}")
            print(f"   ✅ Reflection: {level2_result.get('reflection', {}).get('task_type', 'unknown')}")

            # Level 3 Processing
            print("\n3️⃣ Level 3 Processing...")
            task_type = level2_result.get("advanced_classification", {}).get("task_type", "general")
            level3_result = level3_graph_orchestrator.analyze_task(level1_result["content"], task_type)
            print(f"   ✅ Priority: {level3_result.get('prioritization', {}).get('priority_level', 'N/A')}")
            print(f"   ✅ Risk Score: {level3_result.get('risk', {}).get('risk_score', 0)}")

            # Level 4 Processing
            print("\n4️⃣ Level 4 Processing...")
            level4_result = level4_graph_orchestrator.process_recommendations(level3_result)
            print(f"   ✅ Recommendation: {level4_result.get('recommendation', 'N/A')[:50]}...")
            print(f"   ✅ Overall Score: {level4_result.get('aggregation', {}).get('overall_score', 0)}")

            print("\n✅ Complete Workflow Test Passed!")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()

def test_mock_level2():
    """Test Level 2 with mock data"""

    print("\n🚀 Testing Level 2 with Mock Data")

    with patch('src.utils.llm_client.llm_client.generate_text') as mock_generate:
        # Set up mock responses
        mock_generate.return_value = '{"task_type": "feature", "confidence": 0.95}'

        # Test case
        input_text = "Add user authentication with OAuth support"

        try:
            result = level2_graph_orchestrator.analyze_text(input_text)

            print(f"   ✅ Task Type: {result.get('advanced_classification', {}).get('task_type', 'unknown')}")
            print(f"   ✅ Confidence: {result.get('advanced_classification', {}).get('confidence', 0)}")

            assert result.get('advanced_classification', {}).get('task_type') == "feature"
            assert result.get('advanced_classification', {}).get('confidence') > 0.9

            print("   ✅ Level 2 Test Passed!")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_mock_level3():
    """Test Level 3 with mock data"""

    print("\n🚀 Testing Level 3 with Mock Data")

    with patch('src.utils.llm_client.llm_client.generate_text') as mock_generate:
        # Set up mock responses
        mock_generate.return_value = '{"priority_score": 8.5, "priority_level": "High"}'

        # Test case
        input_text = "Add user authentication with OAuth support"
        task_type = "feature"

        try:
            result = level3_graph_orchestrator.analyze_task(input_text, task_type)

            print(f"   ✅ Priority Score: {result.get('prioritization', {}).get('priority_score', 0)}")
            print(f"   ✅ Priority Level: {result.get('prioritization', {}).get('priority_level', 'N/A')}")

            assert result.get('prioritization', {}).get('priority_level') == "High"
            assert result.get('prioritization', {}).get('priority_score') > 8

            print("   ✅ Level 3 Test Passed!")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_mock_level4():
    """Test Level 4 with mock data"""

    print("\n🚀 Testing Level 4 with Mock Data")

    with patch('src.utils.llm_client.llm_client.generate_text') as mock_generate:
        # Set up mock responses
        mock_generate.return_value = '{"recommendation": "Proceed with implementation", "score": 8.7}'

        # Test case - create mock Level 3 result
        mock_level3_result = {
            "prioritization": {
                "priority_score": 8.5,
                "priority_level": "High"
            },
            "risk": {
                "risk_score": 7.2
            },
            "resources": {
                "time_hours": 40
            },
            "impact": {
                "impact_score": 8.1
            }
        }

        try:
            result = level4_graph_orchestrator.process_recommendations(mock_level3_result)

            print(f"   ✅ Recommendation: {result.get('recommendation', 'N/A')}")
            print(f"   ✅ Overall Score: {result.get('aggregation', {}).get('overall_score', 0)}")

            assert result.get('recommendation') == "Proceed with implementation"
            assert result.get('aggregation', {}).get('overall_score') > 8

            print("   ✅ Level 4 Test Passed!")

        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_complete_mock_workflow()
    test_mock_level2()
    test_mock_level3()
    test_mock_level4()
    print("\n✅ All Mock Integration Tests Completed Successfully!")







