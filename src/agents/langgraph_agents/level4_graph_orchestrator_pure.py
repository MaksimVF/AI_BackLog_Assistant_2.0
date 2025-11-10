

"""
Level 4 Graph Orchestrator - Pure LangGraph Implementation

This module provides a high-level orchestrator for the Level 4 LangGraph implementation
without depending on old agents.
"""

import logging
from typing import Dict, Any

# Import the pure LangGraph implementation
from src.agents.langgraph_agents.level4_graph_agent_pure import level4_graph_agent_pure

# Configure logging
logger = logging.getLogger(__name__)

class Level4GraphOrchestratorPure:
    """Orchestrator for Level 4 LangGraph processing without old agents"""

    def __init__(self):
        """Initialize the Level 4 Graph Orchestrator"""
        logger.info("Initializing Level 4 Graph Orchestrator (Pure LangGraph)")

    def process_recommendations(self, level3_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Level 4 recommendations using pure LangGraph

        Args:
            level3_data: Outputs from Level 3 agents

        Returns:
            Recommendations and visualizations
        """
        logger.info("Processing Level 4 recommendations with pure LangGraph")

        # Use the pure LangGraph implementation
        result = level4_graph_agent_pure.process_recommendations(level3_data)

        # Log the result
        logger.info("Level 4 processing completed with pure LangGraph")

        return result

# Create a global instance for easy access
level4_graph_orchestrator_pure = Level4GraphOrchestratorPure()

