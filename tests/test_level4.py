



"""
Tests for Level 4 components
"""

from src.agents.level4.aggregator_agent import aggregator_agent
from src.agents.level4.visualization_agent import visualization_agent
from src.agents.level4.summary_agent import summary_agent

def test_aggregator_agent():
    """Test the Aggregator Agent"""
    # Sample Level 3 data
    level3_data = {
        "risk": {
            "risk_score": 6.5,
            "interpretation": "Medium"
        },
        "resources": {
            "time_hours": 12,
            "team_size": 2,
            "skills": ["backend", "frontend"]
        },
        "impact": {
            "impact_score": 7.2,
            "interpretation": "High"
        },
        "confidence_urgency": {
            "confidence": 0.85,
            "urgency": 6.0,
            "rationale": "High urgency due to time-sensitive keywords"
        }
    }

    # Test aggregation
    result = aggregator_agent.generate_summary(level3_data)

    # Verify results
    assert "overall_score" in result
    assert "recommendation" in result
    assert result["overall_score"] > 0
    assert result["recommendation"] in ["High priority - Implement immediately", "Medium priority - Schedule for next sprint"]

def test_visualization_agent():
    """Test the Visualization Agent"""
    # Sample analysis data
    analysis_data = {
        "risk_score": 6.5,
        "impact_score": 7.2,
        "urgency": 6.0,
        "confidence": 0.85
    }

    # Test visualization
    result = visualization_agent.generate_visualization(analysis_data)

    # Verify results
    assert "radar_chart" in result
    assert "bar_chart" in result
    assert "scores" in result
    assert result["scores"]["Risk"] == 6.5
    assert result["scores"]["Impact"] == 7.2

def test_summary_agent():
    """Test the Summary Agent"""
    # Sample analysis data
    analysis_data = {
        "overall_score": 6.8,
        "risk_score": 6.5,
        "impact_score": 7.2,
        "urgency": 6.0,
        "confidence": 0.85,
        "recommendation": "Medium priority - Schedule for next sprint"
    }

    # Test summary
    result = summary_agent.generate_summary(analysis_data)

    # Verify results
    assert "recommendation" in result
    assert "rationale" in result
    assert "priority" in result
    assert "next_steps" in result
    assert result["recommendation"] == "Schedule for next sprint"
    assert result["priority"] in ["High", "Medium", "Low"]
    assert len(result["next_steps"]) > 0

def test_level4_integration():
    """Test Level 4 integration"""
    from src.orchestrator.level4_orchestrator import level4_orchestrator

    # Sample Level 3 data
    level3_data = {
        "risk": {
            "risk_score": 6.5,
            "interpretation": "Medium"
        },
        "resources": {
            "time_hours": 12,
            "team_size": 2,
            "skills": ["backend", "frontend"]
        },
        "impact": {
            "impact_score": 7.2,
            "interpretation": "High"
        },
        "confidence_urgency": {
            "confidence": 0.85,
            "urgency": 6.0,
            "rationale": "High urgency due to time-sensitive keywords"
        }
    }

    # Test Level 4 processing
    result = level4_orchestrator.process_recommendations(level3_data)

    # Verify results
    assert "aggregation" in result
    assert "visualization" in result
    assert "summary" in result

    # Verify aggregation
    assert "overall_score" in result["aggregation"]
    assert "recommendation" in result["aggregation"]

    # Verify visualization
    assert "radar_chart" in result["visualization"]
    assert "bar_chart" in result["visualization"]

    # Verify summary
    assert "recommendation" in result["summary"]
    assert "rationale" in result["summary"]
    assert "priority" in result["summary"]




