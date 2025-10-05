
"""
Tests for Main Orchestrator
"""

import pytest
import pytest
import pytest
from src.orchestrator.main_orchestrator import main_orchestrator

def test_main_orchestrator():
    """Test the Main Orchestrator"""
    # Test with a simple text input
    input_data = "This is a test idea for a new feature. We should add user profiles."

    result = main_orchestrator.process_workflow(input_data)

    # Check that both levels are present
    assert "level1" in result
    assert "level2" in result

    # Verify Level 1 results
    assert "modality" in result["level1"]
    assert "content" in result["level1"]
    assert result["level1"]["modality"] == "text"

    # Verify Level 2 results
    assert "reflection" in result["level2"]
    assert "blocks" in result["level2"]
    assert "context" in result["level2"]

    # Check reflection result
    assert "task_type" in result["level2"]["reflection"]
    assert result["level2"]["reflection"]["task_type"] in ["idea", "bug", "feedback"]

    # Check blocks
    assert "blocks" in result["level2"]["blocks"]
    assert len(result["level2"]["blocks"]["blocks"]) > 0

    # Check context
    assert "domain" in result["level2"]["context"]
    assert "entities" in result["level2"]["context"]

def test_main_orchestrator_with_file():
    """Test the Main Orchestrator with a file input"""
    # Test with a file path (simulated)
    input_data = "/path/to/document.pdf"

    result = main_orchestrator.process_workflow(input_data)

    # Check that both levels are present
    assert "level1" in result
    assert "level2" in result

    # Verify Level 1 results
    assert "modality" in result["level1"]
    assert "content" in result["level1"]
    assert result["level1"]["modality"] in ["pdf", "audio", "image", "text"]

    # Verify Level 2 results
    assert "reflection" in result["level2"]
    assert "blocks" in result["level2"]
    assert "context" in result["level2"]
