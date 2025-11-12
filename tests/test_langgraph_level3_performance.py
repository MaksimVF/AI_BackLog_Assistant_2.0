


"""
Performance comparison between original Level 3 and LangGraph Level 3 implementations
"""

import logging
import time
from unittest.mock import patch, MagicMock
from src.orchestrator.level3_orchestrator import level3_orchestrator
from src.agents.langgraph_agents.level3_graph_orchestrator import level3_graph_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def mock_llm_calls():
    """Mock LLM calls to avoid actual API requests"""
    # Create mock responses for each agent
    mock_risk_response = {
        "risk_score": 7.5,
        "risk_level": "high",
        "risk_factors": ["security", "data loss"]
    }

    mock_resource_response = {
        "time_estimate": "2 weeks",
        "team_estimate": "2 developers",
        "resource_level": "medium"
    }

    mock_impact_response = {
        "impact_score": 8.2,
        "impact_level": "high",
        "impact_areas": ["user experience", "revenue"]
    }

    mock_confidence_response = {
        "confidence": 0.85,
        "urgency": 8.0,
        "urgency_level": "high"
    }

    mock_prioritization_response = {
        "priority_score": 88.5,
        "priority_level": "Critical",
        "risk_score": 7.5,
        "impact_score": 8.2,
        "urgency_score": 8.0,
        "confidence_score": 0.85,
        "resource_estimate": {"time_estimate": "2 weeks", "team_estimate": "2 developers"},
        "classification": "bug",
        "recommendation": "Critical bug - address immediately",
        "details": {
            "risk": mock_risk_response,
            "impact": mock_impact_response,
            "confidence_urgency": mock_confidence_response,
            "resources": mock_resource_response
        }
    }

    return {
        "risk_assessment_agent": mock_risk_response,
        "resource_availability_agent": mock_resource_response,
        "impact_potential_agent": mock_impact_response,
        "confidence_urgency_agent": mock_confidence_response,
        "task_prioritization_agent": mock_prioritization_response
    }

def test_performance_comparison():
    """Compare performance between original and LangGraph implementations"""

    print("Testing Level 3 performance comparison...")
    print("Note: This test uses mocked LLM responses for consistent timing\n")

    # Mock the LLM calls to avoid actual API requests
    mock_responses = mock_llm_calls()

    # Test data
    test_cases = [
        {
            "text": "Critical security vulnerability in user authentication system",
            "task_type": "bug"
        },
        {
            "text": "New feature idea: AI-powered code review assistant",
            "task_type": "idea"
        },
        {
            "text": "User feedback: Mobile app crashes on iOS 17",
            "task_type": "feedback"
        }
    ]

    # Test original implementation
    print("Testing original Level 3 implementation...")
    original_times = []

    with patch('src.agents.level3.risk_assessment_agent.risk_assessment_agent.evaluate_risk',
               return_value=mock_responses["risk_assessment_agent"]):
        with patch('src.agents.level3.resource_availability_agent.resource_availability_agent.assess_resources',
                   return_value=mock_responses["resource_availability_agent"]):
            with patch('src.agents.level3.impact_potential_agent.impact_potential_agent.assess_impact',
                       return_value=mock_responses["impact_potential_agent"]):
                with patch('src.agents.level3.confidence_urgency_agent.confidence_urgency_agent.score_task',
                           return_value=mock_responses["confidence_urgency_agent"]):
                    with patch('src.agents.level3.task_prioritization_agent.task_prioritization_agent.prioritize_task',
                               return_value=mock_responses["task_prioritization_agent"]):

                        for i, test_case in enumerate(test_cases, 1):
                            print(f"  Test case {i}: {test_case['text']}")

                            start_time = time.time()
                            result = level3_orchestrator.analyze_task(
                                test_case["text"],
                                test_case["task_type"]
                            )
                            end_time = time.time()

                            duration = end_time - start_time
                            original_times.append(duration)
                            print(f"    Completed in {duration:.3f} seconds")

    avg_original = sum(original_times) / len(original_times)
    print(f"\nOriginal Level 3 average time: {avg_original:.3f} seconds")

    # Test LangGraph implementation
    print("\nTesting LangGraph Level 3 implementation...")
    langgraph_times = []

    with patch('src.agents.level3.risk_assessment_agent.risk_assessment_agent.evaluate_risk',
               return_value=mock_responses["risk_assessment_agent"]):
        with patch('src.agents.level3.resource_availability_agent.resource_availability_agent.assess_resources',
                   return_value=mock_responses["resource_availability_agent"]):
            with patch('src.agents.level3.impact_potential_agent.impact_potential_agent.assess_impact',
                       return_value=mock_responses["impact_potential_agent"]):
                with patch('src.agents.level3.confidence_urgency_agent.confidence_urgency_agent.score_task',
                           return_value=mock_responses["confidence_urgency_agent"]):
                    with patch('src.agents.level3.task_prioritization_agent.task_prioritization_agent.prioritize_task',
                               return_value=mock_responses["task_prioritization_agent"]):

                        for i, test_case in enumerate(test_cases, 1):
                            print(f"  Test case {i}: {test_case['text']}")

                            start_time = time.time()
                            result = level3_graph_orchestrator.analyze_task(
                                test_case["text"],
                                test_case["task_type"]
                            )
                            end_time = time.time()

                            duration = end_time - start_time
                            langgraph_times.append(duration)
                            print(f"    Completed in {duration:.3f} seconds")

    avg_langgraph = sum(langgraph_times) / len(langgraph_times)
    print(f"\nLangGraph Level 3 average time: {avg_langgraph:.3f} seconds")

    # Compare results
    print(f"\nPerformance Comparison:")
    print(f"  Original Level 3: {avg_original:.3f} seconds")
    print(f"  LangGraph Level 3: {avg_langgraph:.3f} seconds")
    print(f"  Difference: {avg_langgraph - avg_original:.3f} seconds")

    if avg_langgraph < avg_original:
        print(f"  🎉 LangGraph is {((avg_original - avg_langgraph) / avg_original * 100):.1f}% faster!")
    else:
        print(f"  ⚠️  LangGraph is {((avg_langgraph - avg_original) / avg_original * 100):.1f}% slower")

    return {
        "original_times": original_times,
        "langgraph_times": langgraph_times,
        "avg_original": avg_original,
        "avg_langgraph": avg_langgraph
    }

if __name__ == "__main__":
    print("Running Level 3 performance comparison...\n")

    try:
        results = test_performance_comparison()
        print("\n✅ Performance comparison completed successfully!")

    except Exception as e:
        print(f"\n❌ Performance comparison failed: {str(e)}")

    print("\nNote: This test uses mocked responses. Real-world performance may vary based on LLM response times.")


