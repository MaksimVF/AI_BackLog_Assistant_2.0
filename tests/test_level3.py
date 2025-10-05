


"""
Tests for Level 3 components
"""

from src.agents.level3.risk_assessment_agent import risk_assessment_agent
from src.agents.level3.resource_availability_agent import resource_availability_agent
from src.agents.level3.impact_potential_agent import impact_potential_agent
from src.agents.level3.confidence_urgency_agent import confidence_urgency_agent

def test_risk_assessment_agent():
    """Test the Risk Assessment Agent"""
    # Test with low risk text
    result = risk_assessment_agent.evaluate_risk("This is a simple task")
    assert result["risk_score"] > 0
    assert result["risk_score"] < 5
    assert result["interpretation"] == "Low"

    # Test with high risk text
    result = risk_assessment_agent.evaluate_risk("This is an urgent critical security vulnerability that needs immediate attention")
    assert result["risk_score"] > 5
    assert result["interpretation"] in ["Medium", "High"]

def test_resource_availability_agent():
    """Test the Resource Availability Agent"""
    # Test with simple task
    result = resource_availability_agent.assess_resources("Simple bug fix")
    assert result["time_hours"] > 0
    assert result["team_size"] >= 1
    assert "general" in result["skills"]

    # Test with complex task
    result = resource_availability_agent.assess_resources("Complex system overhaul requiring backend and frontend changes")
    assert result["time_hours"] > 10
    assert result["team_size"] > 1
    assert "backend" in result["skills"] or "frontend" in result["skills"]

def test_impact_potential_agent():
    """Test the Impact Potential Agent"""
    # Test with low impact text
    result = impact_potential_agent.assess_impact("Minor UI tweak")
    assert result["impact_score"] > 0
    assert result["impact_score"] < 5
    assert result["interpretation"] == "Low"

    # Test with high impact text
    result = impact_potential_agent.assess_impact("Major feature that will increase revenue and user engagement across all users")
    assert result["impact_score"] > 5
    assert result["interpretation"] in ["Medium", "High"]

def test_confidence_urgency_agent():
    """Test the Confidence & Urgency Agent"""
    # Test with standard task
    result = confidence_urgency_agent.score_task("Standard task with clear requirements")
    assert result["confidence"] > 0.5
    assert result["urgency"] > 0
    assert result["urgency"] < 5

    # Test with urgent task
    result = confidence_urgency_agent.score_task("Urgent critical task that needs immediate attention ASAP")
    assert result["urgency"] > 5
    assert "urgency" in result["rationale"].lower()

def test_level3_integration():
    """Test Level 3 integration"""
    from src.orchestrator.level3_orchestrator import level3_orchestrator

    # Test with a sample input
    text = "Urgent feature request: Add user profiles to increase engagement. This will impact all users and requires backend changes."

    result = level3_orchestrator.analyze_task(text)

    # Check that all components are present
    assert "risk" in result
    assert "resources" in result
    assert "impact" in result
    assert "confidence_urgency" in result

    # Verify risk result
    assert "risk_score" in result["risk"]
    assert result["risk"]["risk_score"] > 0

    # Verify resources
    assert "time_hours" in result["resources"]
    assert result["resources"]["time_hours"] > 0

    # Verify impact
    assert "impact_score" in result["impact"]
    assert result["impact"]["impact_score"] > 0

    # Verify confidence/urgency
    assert "confidence" in result["confidence_urgency"]
    assert "urgency" in result["confidence_urgency"]



