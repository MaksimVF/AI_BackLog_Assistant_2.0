


"""
Level 4 Graph Orchestrator

This module provides a high-level orchestrator for the Level 4 LangGraph implementation.
"""

import logging
from typing import Dict, Any

# Import the LangGraph implementation
from src.agents.langgraph_agents.level4_graph_agent import level4_graph_agent

# Configure logging
logger = logging.getLogger(__name__)

class Level4GraphOrchestrator:
    """Orchestrator for Level 4 LangGraph processing"""

    def __init__(self):
        """Initialize the Level 4 Graph Orchestrator"""
        logger.info("Initializing Level 4 Graph Orchestrator")

    def process_recommendations(self, level3_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Level 4 recommendations using LangGraph

        Args:
            level3_data: Outputs from Level 3 agents

        Returns:
            Recommendations and visualizations
        """
        logger.info("Processing Level 4 recommendations with LangGraph")

        # Use the LangGraph implementation
        result = level4_graph_agent.process_recommendations(level3_data)

        # Log the result
        logger.info("Level 4 processing completed with LangGraph")

        return result

# Create a global instance for easy access
level4_graph_orchestrator = Level4GraphOrchestrator()


