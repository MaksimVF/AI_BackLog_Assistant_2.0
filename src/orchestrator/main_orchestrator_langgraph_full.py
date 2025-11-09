






"""
Main Orchestrator with LangGraph for All Levels

This module provides a main orchestrator that uses LangGraph for all levels of processing.
"""

import logging
from typing import Dict, Any

# Import LangGraph orchestrators
from src.agents.langgraph_agents.level1_graph_orchestrator import level1_graph_orchestrator
from src.agents.langgraph_agents.level2_graph_orchestrator import level2_graph_orchestrator
from src.agents.langgraph_agents.level3_graph_orchestrator import level3_graph_orchestrator
from src.agents.langgraph_agents.level4_graph_orchestrator import level4_graph_orchestrator

# Configure logging
logger = logging.getLogger(__name__)

class MainOrchestratorLangGraphFull:
    """Main orchestrator that uses LangGraph for all levels of processing"""

    def __init__(self):
        """Initialize the main orchestrator"""
        logger.info("Initializing Main Orchestrator with LangGraph for all levels")

    async def process_workflow(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process the complete workflow using LangGraph for all levels

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed results from all levels
        """
        logger.info("Processing workflow with LangGraph for all levels")

        # Process Level 1 with LangGraph
        level1_result = level1_graph_orchestrator.process_input(input_data, metadata)
        logger.debug(f"Level 1 completed - Modality: {level1_result.get('modality', 'unknown')}")

        # Process Level 2 with LangGraph
        level2_result = level2_graph_orchestrator.analyze_text(level1_result["content"])
        logger.debug(f"Level 2 completed - Task Type: {level2_result.get('advanced_classification', {}).get('task_type', 'unknown')}")

        # Process Level 3 with LangGraph
        task_type = level2_result.get("advanced_classification", {}).get("task_type", "general")
        level3_result = level3_graph_orchestrator.analyze_task(level1_result["content"], task_type)
        logger.debug(f"Level 3 completed - Priority: {level3_result.get('prioritization', {}).get('priority_level', 'N/A')}")

        # Process Level 4 with LangGraph
        level4_result = level4_graph_orchestrator.process_recommendations(level3_result)
        logger.debug(f"Level 4 completed - Recommendation: {level4_result.get('recommendation', 'N/A')}")

        # Combine all results
        result = {
            "level1": level1_result,
            "level2": level2_result,
            "level3": level3_result,
            "level4": level4_result
        }

        logger.info("Workflow processing completed with LangGraph for all levels")

        return result

# Create a global instance for easy access
main_orchestrator_langgraph_full = MainOrchestratorLangGraphFull()





