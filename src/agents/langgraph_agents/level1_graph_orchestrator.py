

"""
Level 1 Graph Orchestrator

This module provides a LangGraph-based orchestrator for Level 1 agents
that integrates with the existing system architecture.
"""

import logging
from typing import Dict, Any
from src.agents.langgraph_agents.level1_graph_agent import Level1GraphAgent

# Configure logging
logger = logging.getLogger(__name__)

class Level1GraphOrchestrator:
    """Orchestrates Level 1 processing using LangGraph"""

    def __init__(self):
        """Initialize the Level 1 Graph Orchestrator"""
        logger.info("Initializing Level 1 Graph Orchestrator")
        self.graph_agent = Level1GraphAgent()

    def process_input(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process input through Level 1 pipeline using LangGraph

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed data with modality, content, and metadata
        """
        # Use the graph agent to process the input
        result = self.graph_agent.process_input(input_data, metadata)

        # Map the result to the expected format from the original orchestrator
        return {
            "modality": result["modality_detection"].get("modality", "unknown"),
            "content": result["preprocessing"].get("processed_text", ""),
            "metadata": {
                "modality_detection": result["modality_detection"],
                "input_processing": result["input_processing"],
                "preprocessing": result["preprocessing"],
                "duplicate_check": result["duplicate_check"]
            }
        }

# Create a global instance for easy access
level1_graph_orchestrator = Level1GraphOrchestrator()

