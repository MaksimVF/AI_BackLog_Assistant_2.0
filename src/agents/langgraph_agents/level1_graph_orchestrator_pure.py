


"""
Level 1 Graph Orchestrator - Pure LangGraph Implementation

This module provides a high-level orchestrator for the Level 1 LangGraph implementation
without depending on old agents.
"""

import logging
from typing import Dict, Any

# Import the pure LangGraph implementation
from src.agents.langgraph_agents.level1_graph_agent_pure import level1_graph_agent_pure

# Configure logging
logger = logging.getLogger(__name__)

class Level1GraphOrchestratorPure:
    """Orchestrator for Level 1 LangGraph processing without old agents"""

    def __init__(self):
        """Initialize the Level 1 Graph Orchestrator"""
        logger.info("Initializing Level 1 Graph Orchestrator (Pure LangGraph)")

    def process_input(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process Level 1 input using pure LangGraph

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed input data
        """
        logger.info("Processing Level 1 input with pure LangGraph")

        # Use the pure LangGraph implementation
        result = level1_graph_agent_pure.process_input(input_data, metadata)

        # Log the result
        logger.info("Level 1 processing completed with pure LangGraph")

        return result

# Create a global instance for easy access
level1_graph_orchestrator_pure = Level1GraphOrchestratorPure()


