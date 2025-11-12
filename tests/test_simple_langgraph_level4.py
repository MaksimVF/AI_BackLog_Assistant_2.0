



"""
Simple Test for LangGraph Level 4 Integration

This test verifies the basic functionality of the LangGraph Level 4 integration.
"""

import logging
import json
from src.agents.langgraph_agents.level4_graph_orchestrator import level4_graph_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_simple_level4_integration():
    """Test the Level 4 Graph Orchestrator with simple data"""

    # Simple Level 3 data for testing
    simple_level3_data = {
        "risk": {
            "score": 6.5,
            "details": "Moderate risk"
        },
        "impact": {
            "score": 7.2,
            "details": "Good impact on performance"
        },
        "confidence_urgency": {
            "confidence": 0.75,
            "urgency": 5.8
        },
        "resources": {
            "estimated_hours": 15,
            "required_skills": ["Python"]
        }
    }

    print("Testing Level 4 Graph Orchestrator with simple data...")
    print("Input data:", json.dumps(simple_level3_data, indent=2))

    # Process recommendations
    result = level4_graph_orchestrator.process_recommendations(simple_level3_data)

    print("\nResults:")
    print("Aggregation:", json.dumps(result.get("aggregation", {}), indent=2))
    print("Summary:", json.dumps(result.get("summary", {}), indent=2))

    # Verify that all expected components are present
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

    print("\n✅ Simple test passed! Level 4 Graph Orchestrator integration is working correctly.")

if __name__ == "__main__":
    test_simple_level4_integration()



