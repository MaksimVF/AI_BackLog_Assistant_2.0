

"""
Test the Level 3 LangGraph implementation
"""

import logging
import time
from src.agents.langgraph_agents.level3_graph_orchestrator import level3_graph_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_level3_graph_orchestrator():
    """Test the Level 3 LangGraph orchestrator"""

    # Test data
    test_cases = [
        {
            "text": "Critical security vulnerability in user authentication system",
            "task_type": "bug",
            "expected_risk": "high"
        },
        {
            "text": "New feature idea: AI-powered code review assistant",
            "task_type": "idea",
            "expected_impact": "high"
        },
        {
            "text": "User feedback: Mobile app crashes on iOS 17",
            "task_type": "feedback",
            "expected_urgency": "high"
        }
    ]

    print("Testing Level 3 LangGraph Orchestrator...")
    start_time = time.time()

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['text']}")
        print(f"Task Type: {test_case['task_type']}")

        try:
            # Run the analysis
            result = level3_graph_orchestrator.analyze_task(
                test_case["text"],
                test_case["task_type"]
            )

            # Print results
            print("Analysis Results:")
            print(f"  - Risk: {result.get('risk', {}).get('risk_score', 'N/A')}")
            print(f"  - Impact: {result.get('impact', {}).get('impact_score', 'N/A')}")
            print(f"  - Urgency: {result.get('confidence_urgency', {}).get('urgency', 'N/A')}")
            print(f"  - Priority: {result.get('prioritization', {}).get('priority_score', 'N/A')}")
            print(f"  - Priority Level: {result.get('prioritization', {}).get('priority_level', 'N/A')}")
            print(f"  - Recommendation: {result.get('prioritization', {}).get('recommendation', 'N/A')}")

        except Exception as e:
            print(f"Error in test case {i}: {str(e)}")

    end_time = time.time()
    duration = end_time - start_time
    print(f"\nAll tests completed in {duration:.2f} seconds")

    return duration

if __name__ == "__main__":
    test_level3_graph_orchestrator()

