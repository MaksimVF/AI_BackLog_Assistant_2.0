




"""
Level 3 Graph Orchestrator - Pure LangGraph Implementation

This module provides a high-level orchestrator for the Level 3 LangGraph implementation
without depending on old agents.
"""

import logging
from typing import Dict, Any

# Import the pure LangGraph implementation
from src.agents.langgraph_agents.level3_graph_agent_pure import level3_graph_agent_pure

# Configure logging
logger = logging.getLogger(__name__)

class Level3GraphOrchestratorPure:
    """Orchestrator for Level 3 LangGraph processing without old agents"""

    def __init__(self):
        """Initialize the Level 3 Graph Orchestrator"""
        logger.info("Initializing Level 3 Graph Orchestrator (Pure LangGraph)")

    def analyze_task(self, input_text: str, task_type: str = "general") -> Dict[str, Any]:
        """
        Analyze task using pure LangGraph

        Args:
            input_text: Text to analyze
            task_type: Type of task (from Level 2)

        Returns:
            Analysis results
        """
        logger.info("Analyzing task with pure LangGraph Level 3")

        # Use the pure LangGraph implementation
        result = level3_graph_agent_pure.analyze_task(input_text, task_type)

        # Log the result
        logger.info("Level 3 analysis completed with pure LangGraph")

        return result

# Create a global instance for easy access
level3_graph_orchestrator_pure = Level3GraphOrchestratorPure()




