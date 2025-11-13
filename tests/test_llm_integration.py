


import pytest
from unittest.mock import patch, MagicMock
from src.utils.llm_client import llm_client
from src.back.agents.level2.reflection_agent import reflection_agent
from src.back.agents.level2.contextualiza_agent import contextualiza_agent
from src.back.agents.level3.risk_assessment_agent import risk_assessment_agent
from src.back.agents.level3.resource_availability_agent import resource_availability_agent
from src.back.agents.level3.impact_potential_agent import impact_potential_agent
from src.back.agents.level3.confidence_urgency_agent import confidence_urgency_agent
from src.back.agents.level4.summary_agent import summary_agent

# Test data
TEST_INPUT = "We need to fix the critical security vulnerability in the payment system"

# Mock LLM responses
MOCK_REFLECTION_RESPONSE = "bug"
MOCK_CONTEXT_RESPONSE = '{"entities": [{"type": "security", "text": "vulnerability", "confidence": 0.9}], "domain": "IT"}'
MOCK_RISK_RESPONSE = "8.5"
MOCK_RESOURCE_RESPONSE = '{"time_hours": 20, "team_size": 2, "skills": ["security", "backend"]}'
MOCK_IMPACT_RESPONSE = "9.0"
MOCK_CONFIDENCE_RESPONSE = '{"confidence": 0.9, "urgency": 8.5, "rationale": "Critical security issue"}'
MOCK_SUMMARY_RESPONSE = '{"recommendation": "Implement immediately", "reason": "Critical security vulnerability"}'

@pytest.fixture
def mock_llm_client():
    """Mock the LLM client for testing"""
    with patch.object(llm_client, 'generate_text') as mock_text, \
         patch.object(llm_client, 'generate_json') as mock_json:

        # Configure mock responses
        mock_text.side_effect = [
            MOCK_REFLECTION_RESPONSE,
            MOCK_RISK_RESPONSE,
            MOCK_IMPACT_RESPONSE
        ]

        mock_json.side_effect = [
            {"entities": [{"type": "security", "text": "vulnerability", "confidence": 0.9}], "domain": "IT"},
            {"time_hours": 20, "team_size": 2, "skills": ["security", "backend"]},
            {"confidence": 0.9, "urgency": 8.5, "rationale": "Critical security issue"},
            {"recommendation": "Implement immediately", "reason": "Critical security vulnerability"}
        ]

        yield mock_text, mock_json

def test_reflection_agent_llm_integration(mock_llm_client):
    """Test that reflection agent uses LLM when available"""
    mock_text, mock_json = mock_llm_client

    result = reflection_agent.classify_task(TEST_INPUT)

    # Verify LLM was called
    mock_text.assert_called_once()

    # Verify result
    assert result.task_type == "bug"
    assert result.confidence > 0.8
    assert result.metadata["classification_method"] == "llm"

def test_contextualiza_agent_llm_integration(mock_llm_client):
    """Test that contextualiza agent uses LLM when available"""
    mock_text, mock_json = mock_llm_client

    result = contextualiza_agent.analyze_context(TEST_INPUT)

    # Verify LLM was called
    assert mock_json.called

    # Verify result
    assert result.domain == "IT"
    assert len(result.entities) > 0
    assert result.entities[0].entity_type == "security"
    assert result.metadata["analysis_method"] == "llm"

def test_risk_assessment_agent_llm_integration(mock_llm_client):
    """Test that risk assessment agent uses LLM when available"""
    mock_text, mock_json = mock_llm_client

    result = risk_assessment_agent.assess_risk(TEST_INPUT)

    # Verify LLM was called
    assert mock_text.called

    # Verify result
    assert result.score > 7.0
    assert result.method == "llm"

def test_resource_availability_agent_llm_integration(mock_llm_client):
    """Test that resource availability agent uses LLM when available"""
    mock_text, mock_json = mock_llm_client

    # Reset the mock to ensure it's fresh
    mock_json.reset_mock()
    mock_json.side_effect = [{"time_hours": 20, "team_size": 2, "skills": ["security", "backend"]}]

    result = resource_availability_agent.assess_resources(TEST_INPUT)

    # Verify LLM was called
    assert mock_json.called

    # Verify result
    assert result["time_hours"] == 20
    assert result["team_size"] == 2
    assert "security" in result["skills"]
    assert result["method"] == "llm"

def test_impact_potential_agent_llm_integration(mock_llm_client):
    """Test that impact potential agent uses LLM when available"""
    mock_text, mock_json = mock_llm_client

    # Reset the mock to ensure it's fresh
    mock_text.reset_mock()
    mock_text.side_effect = [MOCK_IMPACT_RESPONSE]

    result = impact_potential_agent.assess_impact(TEST_INPUT)

    # Verify LLM was called
    assert mock_text.called

    # Verify result
    assert result["impact_score"] > 8.0
    assert result["method"] == "llm"

def test_confidence_urgency_agent_llm_integration(mock_llm_client):
    """Test that confidence urgency agent uses LLM when available"""
    mock_text, mock_json = mock_llm_client

    # Reset the mock to ensure it's fresh
    mock_json.reset_mock()
    mock_json.side_effect = [{"confidence": 0.9, "urgency": 8.5, "rationale": "Critical security issue"}]

    result = confidence_urgency_agent.score_task(TEST_INPUT)

    # Verify LLM was called
    assert mock_json.called

    # Verify result
    assert result["confidence"] > 0.8
    assert result["urgency"] > 8.0
    assert result["method"] == "llm"

def test_summary_agent_llm_integration(mock_llm_client):
    """Test that summary agent uses LLM when available"""
    mock_text, mock_json = mock_llm_client

    # Reset the mock to ensure it's fresh
    mock_json.reset_mock()
    mock_json.side_effect = [{"recommendation": "Implement immediately", "reason": "Critical security vulnerability"}]

    # Create a mock analysis
    mock_analysis = {
        "risk_score": 8.5,
        "impact_score": 9.0,
        "confidence": 0.9,
        "urgency": 8.5
    }

    result = summary_agent.generate_summary(mock_analysis)

    # Verify LLM was called
    assert mock_json.called

    # Verify result
    assert result["recommendation"] == "Implement immediately"
    assert result["method"] == "llm"

def test_fallback_to_heuristic():
    """Test that agents fall back to heuristic when LLM fails"""
    with patch.object(llm_client, 'generate_text', side_effect=Exception("LLM failed")):
        with patch.object(llm_client, 'generate_json', side_effect=Exception("LLM failed")):

            # Test reflection agent
            result = reflection_agent.classify_task(TEST_INPUT)
            assert result.metadata["classification_method"] == "keyword_based"

            # Test risk assessment
            result = risk_assessment_agent.assess_risk(TEST_INPUT)
            assert result.method == "heuristic_fallback"

            # Test impact assessment
            result = impact_potential_agent.assess_impact(TEST_INPUT)
            assert result["method"] == "heuristic_fallback"

            # Test summary agent
            result = summary_agent.generate_summary({"risk_score": 5})
            assert result["method"] == "heuristic_fallback"

