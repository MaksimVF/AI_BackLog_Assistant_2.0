

"""
Test for LangGraph Level 4 Agents

This test verifies the functionality of the LangGraph-based Level 4 agents.
"""

import logging
import json
from src.agents.langgraph_agents.level4_graph_orchestrator import level4_graph_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_level4_graph_orchestrator():
    """Test the Level 4 Graph Orchestrator"""

    # Sample Level 3 data for testing
    sample_level3_data = {
        "risk": {
            "score": 7.5,
            "details": "High risk due to security implications"
        },
        "impact": {
            "score": 8.2,
            "details": "Significant impact on user experience"
        },
        "confidence_urgency": {
            "confidence": 0.85,
            "urgency": 6.8
        },
        "resources": {
            "estimated_hours": 20,
            "required_skills": ["Python", "Django"]
        }
    }

    print("Testing Level 4 Graph Orchestrator...")
    print("Input data:", json.dumps(sample_level3_data, indent=2))

    # Process recommendations
    result = level4_graph_orchestrator.process_recommendations(sample_level3_data)

    print("\nResults:")
    print("Aggregation:", json.dumps(result.get("aggregation", {}), indent=2))
    print("Summary:", json.dumps(result.get("summary", {}), indent=2))
    print("Enhanced Summary:", json.dumps(result.get("enhanced_summary", {}), indent=2))

    # Verify visualization exists
    visualization = result.get("visualization", {})
    print("Visualization types:", list(visualization.keys()))

    # Check that all expected components are present
    assert "aggregation" in result, "Missing aggregation result"
    assert "visualization" in result, "Missing visualization result"
    assert "summary" in result, "Missing summary result"
    assert "enhanced_summary" in result, "Missing enhanced summary result"

    # Check aggregation structure
    aggregation = result["aggregation"]
    assert "overall_score" in aggregation, "Missing overall_score in aggregation"
    assert "recommendation" in aggregation, "Missing recommendation in aggregation"

    # Check summary structure
    summary = result["summary"]
    assert "recommendation" in summary, "Missing recommendation in summary"
    assert "rationale" in summary, "Missing rationale in summary"

    print("\n✅ All tests passed! Level 4 Graph Orchestrator is working correctly.")

if __name__ == "__main__":
    test_level4_graph_orchestrator()

