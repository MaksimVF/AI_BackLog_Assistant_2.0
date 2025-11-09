

"""
Level 4 Graph Orchestrator

This module provides a LangGraph-based orchestrator for Level 4 agents
that integrates with the existing system architecture.
"""

import logging
from typing import Dict, Any
from src.agents.langgraph_agents.level4_graph_agent import Level4GraphAgent

# Configure logging
logger = logging.getLogger(__name__)

class Level4GraphOrchestrator:
    """Orchestrates Level 4 processing using LangGraph"""

    def __init__(self):
        """Initialize the Level 4 Graph Orchestrator"""
        logger.info("Initializing Level 4 Graph Orchestrator")
        self.graph_agent = Level4GraphAgent()

    def process_recommendations(self, level3_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Level 4 recommendations and visualizations through LangGraph

        Args:
            level3_data: Outputs from Level 3 agents

        Returns:
            Recommendations and visualizations
        """
        # Use the graph agent to process recommendations
        result = self.graph_agent.process_recommendations(level3_data)

        # Map the result to the expected format from the original orchestrator
        return {
            "aggregation": result["aggregation"],
            "visualization": result["visualization"],
            "summary": result["summary"],
            "enhanced_summary": result["enhanced_summary"]
        }

# Create a global instance for easy access
level4_graph_orchestrator = Level4GraphOrchestrator()

