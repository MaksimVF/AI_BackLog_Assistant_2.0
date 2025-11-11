

"""
Main Orchestrator with Pure LangGraph for All Levels

This module provides a main orchestrator that uses pure LangGraph implementations
for all levels without depending on old agents.
"""

import logging
from typing import Dict, Any

# Import LangGraph orchestrators (pure versions for all levels)
from src.agents.langgraph_agents.level1_graph_orchestrator_pure import level1_graph_orchestrator_pure as level1_graph_orchestrator
from src.agents.langgraph_agents.level2_graph_orchestrator_pure import level2_graph_orchestrator_pure as level2_graph_orchestrator
from src.agents.langgraph_agents.level3_graph_orchestrator_pure import level3_graph_orchestrator_pure as level3_graph_orchestrator
from src.agents.langgraph_agents.level4_graph_orchestrator_pure import level4_graph_orchestrator_pure

# Configure logging
logger = logging.getLogger(__name__)

class MainOrchestratorLangGraphPure:
    """Main orchestrator that uses pure LangGraph implementations for all levels"""

    def __init__(self):
        """Initialize the main orchestrator"""
        logger.info("Initializing Main Orchestrator with pure LangGraph for all levels")

    async def process_workflow(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process the complete workflow using pure LangGraph implementations for all levels

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed results from all levels
        """
        logger.info("Processing workflow with pure LangGraph for all levels")

        # Process Level 1 with LangGraph
        logger.info(f"Processing Level 1 with input: '{input_data}'")
        level1_result = level1_graph_orchestrator.process_input(input_data, metadata)
        logger.debug(f"Level 1 completed - Modality: {level1_result.get('modality', 'unknown')}")
        logger.debug(f"Level 1 result: {level1_result}")

        # Process Level 2 with LangGraph (now with duplicate detection)
        user_id = metadata.get("user_id", "default") if metadata else "default"
        content = level1_result.get("input", {}).get("content", "")
        logger.debug(f"Processing Level 2 with content: '{content}'")
        level2_result = await level2_graph_orchestrator.analyze_text(content, user_id)
        logger.debug(f"Level 2 completed - Task Type: {level2_result.get('advanced_classification', {}).get('task_type', 'unknown')}")

        # Process Level 3 with LangGraph
        task_type = level2_result.get("advanced_classification", {}).get("task_type", "general")
        level3_result = level3_graph_orchestrator.analyze_task(content, task_type)
        logger.debug(f"Level 3 completed - Priority: {level3_result.get('prioritization', {}).get('priority_level', 'N/A')}")

        # Process Level 4 with pure LangGraph (no old agents)
        level4_result = level4_graph_orchestrator_pure.process_recommendations(level3_result)
        logger.debug(f"Level 4 completed - Recommendation: {level4_result.get('recommendation', 'N/A')}")

        # Combine all results
        result = {
            "level1": level1_result,
            "level2": level2_result,
            "level3": level3_result,
            "level4": level4_result
        }

        logger.info("Workflow processing completed with pure LangGraph for all levels")

        return result

# Create a global instance for easy access
main_orchestrator_langgraph_pure = MainOrchestratorLangGraphPure()

