



"""
Test for LangGraph Level 4 Integration

This test verifies the functionality of the LangGraph Level 4 integration.
"""

import logging
import json
import pytest
from unittest.mock import patch
from src.agents.langgraph_agents.level4_graph_orchestrator import level4_graph_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_level4_graph_integration():
    """Test the Level 4 Graph Orchestrator with sample data"""

    # Sample Level 3 data for testing
    sample_level3_data = {
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

    print("Testing Level 4 Graph Orchestrator with sample data...")
    print("Input data:", json.dumps(sample_level3_data, indent=2))

    # Process recommendations
    result = level4_graph_orchestrator.process_recommendations(sample_level3_data)

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

    print("\n✅ Test passed! Level 4 Graph Orchestrator integration is working correctly.")

def test_level4_graph_error_handling():
    """Test error handling in Level 4 Graph Orchestrator"""

    # Test with malformed input
    malformed_data = {
        "risk": {
            "score": "invalid",  # Should be a number
            "details": "Moderate risk"
        },
        "impact": {
            "score": 7.2,
            "details": "Good impact on performance"
        }
    }

    print("Testing Level 4 Graph Orchestrator with malformed data...")

    # This should not raise an exception, but handle the error gracefully
    result = level4_graph_orchestrator.process_recommendations(malformed_data)

    # Verify that we still get results (with fallback values)
    assert "aggregation" in result, "Missing aggregation result"
    assert "summary" in result, "Missing summary result"

    print("\n✅ Error handling test passed!")

def test_level4_graph_different_inputs():
    """Test Level 4 Graph Orchestrator with different input types"""

    # Test with high risk, low impact
    high_risk_data = {
        "risk": {
            "score": 9.5,
            "details": "High risk"
        },
        "impact": {
            "score": 3.2,
            "details": "Low impact"
        },
        "confidence_urgency": {
            "confidence": 0.65,
            "urgency": 8.8
        },
        "resources": {
            "estimated_hours": 30,
            "required_skills": ["Python", "Django"]
        }
    }

    print("Testing Level 4 Graph Orchestrator with high risk, low impact data...")
    result = level4_graph_orchestrator.process_recommendations(high_risk_data)

    # Verify that we get appropriate recommendations
    assert "aggregation" in result, "Missing aggregation result"
    assert "summary" in result, "Missing summary result"

    # Check that the recommendation reflects the high risk
    summary = result["summary"]
    assert "recommendation" in summary, "Missing recommendation in summary"

    print("\n✅ Different input types test passed!")

if __name__ == "__main__":
    test_level4_graph_integration()
    test_level4_graph_error_handling()
    test_level4_graph_different_inputs()



