

"""
Main Orchestrator with Pure LangGraph for Level 4

This module provides a main orchestrator that uses LangGraph for all levels,
with Level 4 using a pure LangGraph implementation without old agents.
"""

import logging
from typing import Dict, Any

# Import LangGraph orchestrators
from src.agents.langgraph_agents.level1_graph_orchestrator_pure import level1_graph_orchestrator_pure
from src.agents.langgraph_agents.level2_graph_orchestrator_pure import level2_graph_orchestrator_pure
from src.agents.langgraph_agents.level3_graph_orchestrator_pure import level3_graph_orchestrator_pure
from src.agents.langgraph_agents.level4_graph_orchestrator_pure import level4_graph_orchestrator_pure

# Configure logging
logger = logging.getLogger(__name__)

class MainOrchestratorLangGraphPure:
    """Main orchestrator that uses LangGraph for all levels, with pure implementation for Level 4"""

    def __init__(self):
        """Initialize the main orchestrator"""
        logger.info("Initializing Main Orchestrator with LangGraph (pure Level 4)")

    async def process_workflow(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process the complete workflow using LangGraph for all levels,
        with pure implementation for Level 4

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed results from all levels
        """
        logger.info("Processing workflow with LangGraph (pure Level 4)")

        # Process Level 1 with pure LangGraph
        level1_result = level1_graph_orchestrator_pure.process_input(input_data, metadata)
        logger.debug(f"Level 1 completed - Modality: {level1_result.get('modality', 'unknown')}")

        # Process Level 2 with pure LangGraph
        level2_result = level2_graph_orchestrator_pure.analyze_text(level1_result.get("content", ""))
        logger.debug(f"Level 2 completed - Task Type: {level2_result.get('advanced_classification', {}).get('task_type', 'unknown')}")

        # Process Level 3 with pure LangGraph
        task_type = level2_result.get("advanced_classification", {}).get("task_type", "general")
        level3_result = level3_graph_orchestrator_pure.analyze_task(level1_result.get("content", ""), task_type)
        logger.debug(f"Level 3 completed - Priority: {level3_result.get('prioritization', {}).get('priority_level', 'N/A')}")

        # Process Level 4 with pure LangGraph
        level4_result = level4_graph_orchestrator_pure.process_recommendations(level3_result)
        logger.debug(f"Level 4 completed - Recommendation: {level4_result.get('recommendation', 'N/A')}")

        # Combine all results
        result = {
            "level1": level1_result,
            "level2": level2_result,
            "level3": level3_result,
            "level4": level4_result
        }

        logger.info("Workflow processing completed with LangGraph (pure Level 4)")

        return result

# Create a global instance for easy access
main_orchestrator_langgraph_pure = MainOrchestratorLangGraphPure()

