



"""
Level 2 Graph Orchestrator - Pure LangGraph Implementation

This module provides a high-level orchestrator for the Level 2 LangGraph implementation
without depending on old agents.
"""

import logging
from typing import Dict, Any

# Import the pure LangGraph implementation
from src.agents.langgraph_agents.level2_graph_agent_pure import level2_graph_agent_pure

# Configure logging
logger = logging.getLogger(__name__)

class Level2GraphOrchestratorPure:
    """Orchestrator for Level 2 LangGraph processing without old agents"""

    def __init__(self):
        """Initialize the Level 2 Graph Orchestrator"""
        logger.info("Initializing Level 2 Graph Orchestrator (Pure LangGraph)")

    def analyze_text(self, input_text: str) -> Dict[str, Any]:
        """
        Analyze text using pure LangGraph

        Args:
            input_text: Text to analyze

        Returns:
            Analysis results
        """
        logger.info("Analyzing text with pure LangGraph Level 2")

        # Use the pure LangGraph implementation
        result = level2_graph_agent_pure.analyze_text(input_text)

        # Log the result
        logger.info("Level 2 analysis completed with pure LangGraph")

        return result

# Create a global instance for easy access
level2_graph_orchestrator_pure = Level2GraphOrchestratorPure()



