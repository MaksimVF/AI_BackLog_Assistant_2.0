







"""
Comprehensive tests for Main Orchestrator with LangGraph for all levels
"""

import pytest
import asyncio
from src.orchestrator.main_orchestrator_langgraph_full import main_orchestrator_langgraph_full

@pytest.mark.asyncio
async def test_main_orchestrator_langgraph_full_text():
    """Test the Main Orchestrator with LangGraph for all levels using text input"""

    # Test with a simple text input
    input_data = "This is a test idea for a new feature. We should add user profiles."

    result = await main_orchestrator_langgraph_full.process_workflow(input_data)

    # Check that all levels are present
    assert "level1" in result
    assert "level2" in result
    assert "level3" in result
    assert "level4" in result

    # Verify Level 1 results from LangGraph
    assert "modality" in result["level1"]
    assert "content" in result["level1"]
    assert result["level1"]["modality"] == "text"

    # Verify Level 2 results from LangGraph
    assert "advanced_classification" in result["level2"]
    assert "reflection" in result["level2"]
    assert "blocks" in result["level2"]
    assert "context" in result["level2"]

    # Verify Level 3 results from LangGraph
    assert "prioritization" in result["level3"]
    assert "risk" in result["level3"]
    assert "resources" in result["level3"]
    assert "impact" in result["level3"]

    # Verify Level 4 results from LangGraph
    assert "aggregation" in result["level4"]
    assert "visualization" in result["level4"]
    assert "summary" in result["level4"]

@pytest.mark.asyncio
async def test_main_orchestrator_langgraph_full_pdf():
    """Test the Main Orchestrator with LangGraph for all levels using PDF input"""

    # Test with a PDF file path (simulated)
    input_data = "document.pdf"

    result = await main_orchestrator_langgraph_full.process_workflow(input_data)

    # Check that all levels are present
    assert "level1" in result
    assert "level2" in result
    assert "level3" in result
    assert "level4" in result

    # Verify Level 1 results from LangGraph
    assert "modality" in result["level1"]
    assert "content" in result["level1"]
    assert result["level1"]["modality"] == "pdf"

    # Verify Level 2 results from LangGraph
    assert "advanced_classification" in result["level2"]
    assert "reflection" in result["level2"]
    assert "blocks" in result["level2"]
    assert "context" in result["level2"]

    # Verify Level 3 results from LangGraph
    assert "prioritization" in result["level3"]
    assert "risk" in result["level3"]
    assert "resources" in result["level3"]
    assert "impact" in result["level3"]

    # Verify Level 4 results from LangGraph
    assert "aggregation" in result["level4"]
    assert "visualization" in result["level4"]
    assert "summary" in result["level4"]

@pytest.mark.asyncio
async def test_main_orchestrator_langgraph_full_audio():
    """Test the Main Orchestrator with LangGraph for all levels using audio input"""

    # Test with an audio file path (simulated)
    input_data = "recording.mp3"

    result = await main_orchestrator_langgraph_full.process_workflow(input_data)

    # Check that all levels are present
    assert "level1" in result
    assert "level2" in result
    assert "level3" in result
    assert "level4" in result

    # Verify Level 1 results from LangGraph
    assert "modality" in result["level1"]
    assert "content" in result["level1"]
    assert result["level1"]["modality"] == "audio"

    # Verify Level 2 results from LangGraph
    assert "advanced_classification" in result["level2"]
    assert "reflection" in result["level2"]
    assert "blocks" in result["level2"]
    assert "context" in result["level2"]

    # Verify Level 3 results from LangGraph
    assert "prioritization" in result["level3"]
    assert "risk" in result["level3"]
    assert "resources" in result["level3"]
    assert "impact" in result["level3"]

    # Verify Level 4 results from LangGraph
    assert "aggregation" in result["level4"]
    assert "visualization" in result["level4"]
    assert "summary" in result["level4"]

def test_task_workflow():
    """Test a complete task workflow with LangGraph"""

    # Simple task test
    task_text = "Add user authentication feature with OAuth support"

    # Process the task
    result = asyncio.run(main_orchestrator_langgraph_full.process_workflow(task_text))

    # Verify the workflow completed successfully
    assert "level1" in result
    assert "level2" in result
    assert "level3" in result
    assert "level4" in result

    # Verify task classification
    task_type = result["level2"].get("advanced_classification", {}).get("task_type", "unknown")
    assert task_type in ["feature", "bug", "idea", "feedback", "question"]

    # Verify prioritization
    priority = result["level3"].get("prioritization", {}).get("priority_level", "unknown")
    assert priority in ["Low", "Medium", "High", "Critical"]

    # Verify recommendation
    recommendation = result["level4"].get("aggregation", {}).get("recommendation", "")
    assert recommendation != ""

    print("✅ Task workflow test completed successfully")
    print(f"   - Task Type: {task_type}")
    print(f"   - Priority: {priority}")
    print(f"   - Recommendation: {recommendation[:50]}...")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])





