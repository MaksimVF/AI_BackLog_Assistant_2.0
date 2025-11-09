

"""
Level 3 Graph Orchestrator

This module provides a high-level orchestrator that integrates the LangGraph
implementation of Level 3 agents with the existing system architecture.
"""

import logging
from typing import Dict, Any
from src.agents.langgraph_agents.level3_graph_agent import level3_graph_agent

# Configure logging
logger = logging.getLogger(__name__)

class Level3GraphOrchestrator:
    """Orchestrates Level 3 processing using LangGraph implementation"""

    def __init__(self):
        """Initialize the Level 3 Graph Orchestrator"""
        logger.info("Initializing Level 3 Graph Orchestrator")

    def analyze_task(self, text: str, task_type: str = "general") -> Dict[str, Any]:
        """
        Analyze task through Level 3 LangGraph pipeline

        Args:
            text: Input text to analyze
            task_type: Type of task (bug, idea, feedback, etc.)

        Returns:
            Analysis results with risk, resources, impact, confidence/urgency, and prioritization
        """
        # Use the LangGraph implementation
        result = level3_graph_agent.analyze_task(text, task_type)

        # Format the result to match the expected output structure
        return {
            "risk": result.get("risk", {}),
            "resources": result.get("resources", {}),
            "impact": result.get("impact", {}),
            "confidence_urgency": result.get("confidence_urgency", {}),
            "prioritization": result.get("prioritization", {})
        }

# Create a global instance for easy access
level3_graph_orchestrator = Level3GraphOrchestrator()

