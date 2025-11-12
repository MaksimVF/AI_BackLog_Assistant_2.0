


"""
Level 2 Graph Orchestrator

This module provides a LangGraph-based orchestrator for Level 2 agents
that integrates with the existing system architecture.
"""

import logging
from typing import Dict, Any
from src.agents.langgraph_agents.level2_graph_agent import Level2GraphAgent

# Configure logging
logger = logging.getLogger(__name__)

class Level2GraphOrchestrator:
    """Orchestrates Level 2 processing using LangGraph"""

    def __init__(self):
        """Initialize the Level 2 Graph Orchestrator"""
        logger.info("Initializing Level 2 Graph Orchestrator")
        self.graph_agent = Level2GraphAgent()

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text through Level 2 pipeline using LangGraph

        Args:
            text: Input text to analyze

        Returns:
            Analysis results with classification, blocks, and context
        """
        # Use the graph agent to analyze the text
        result = self.graph_agent.analyze_text(text)

        # Map the result to the expected format from the original orchestrator
        return {
            "advanced_classification": result["advanced_classification"],
            "reflection": result["reflection"],
            "blocks": result["semantic_blocks"],
            "context": result["context"]
        }

# Create a global instance for easy access
level2_graph_orchestrator = Level2GraphOrchestrator()


