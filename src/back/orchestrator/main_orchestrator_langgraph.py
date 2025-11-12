



"""
Main Orchestrator with LangGraph

This module provides a main orchestrator that uses LangGraph for Level 4 processing.
"""

import logging
import asyncio
from typing import Dict, Any

# Import existing orchestrators
from src.orchestrator.level1_orchestrator import level1_orchestrator
from src.orchestrator.level2_orchestrator import level2_orchestrator
from src.orchestrator.level3_orchestrator import level3_orchestrator

# Import LangGraph Level 4 orchestrator
from src.agents.langgraph_agents.level4_graph_orchestrator import level4_graph_orchestrator

# Configure logging
logger = logging.getLogger(__name__)

class MainOrchestratorLangGraph:
    """Main orchestrator that uses LangGraph for Level 4 processing"""

    def __init__(self):
        """Initialize the main orchestrator"""
        logger.info("Initializing Main Orchestrator with LangGraph")

    async def process_workflow(self, input_data: Dict[str, Any], task_type: str = "standard") -> Dict[str, Any]:
        """
        Process the complete workflow using LangGraph for Level 4

        Args:
            input_data: Input data for processing
            task_type: Type of task (standard, urgent, etc.)

        Returns:
            Processed results from all levels
        """
        logger.info("Processing workflow with LangGraph for Level 4")

        # Process Level 1
        level1_result = level1_orchestrator.process_input(input_data)

        # Process Level 2
        level2_result = level2_orchestrator.process_analysis(level1_result)

        # Process Level 3
        level3_result = level3_orchestrator.analyze_task(level2_result["content"], task_type)

        # Process Level 4 with LangGraph
        level4_result = level4_graph_orchestrator.process_recommendations(level3_result)

        # Combine all results
        result = {
            "level1": level1_result,
            "level2": level2_result,
            "level3": level3_result,
            "level4": level4_result
        }

        logger.info("Workflow processing completed with LangGraph")

        return result

# Create a global instance for easy access
main_orchestrator_langgraph = MainOrchestratorLangGraph()



