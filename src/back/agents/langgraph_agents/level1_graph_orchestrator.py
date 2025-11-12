





"""
Level 1 Graph Orchestrator

This module provides a high-level orchestrator for the Level 1 LangGraph implementation.
"""

import logging
from typing import Dict, Any

# Import the LangGraph agent
from src.agents.langgraph_agents.level1_graph_agent import level1_graph_agent

# Configure logging
logger = logging.getLogger(__name__)

class Level1GraphOrchestrator:
    """Orchestrator for Level 1 LangGraph processing"""

    def __init__(self):
        """Initialize the Level 1 Graph Orchestrator"""
        logger.info("Initializing Level 1 Graph Orchestrator")

    def process_input(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process input using the LangGraph-based Level 1 pipeline

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed data with all agent outputs
        """
        logger.debug(f"Processing input with Level 1 Graph Orchestrator: {input_data[:50]}...")

        # Use the LangGraph agent to process the input
        result = level1_graph_agent.process_input(input_data, metadata)

        # Extract the relevant information
        return {
            "content": result.get("input_processing", {}).get("content", ""),
            "modality": result.get("modality_detection", {}).get("modality", "unknown"),
            "metadata": result.get("preprocessing", {}).get("metadata", {}),
            "processing_status": "success",
            "raw_result": result  # Include the full result for debugging
        }

# Create a global instance for easy access
level1_graph_orchestrator = Level1GraphOrchestrator()





