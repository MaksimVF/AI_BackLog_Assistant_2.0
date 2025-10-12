



"""
Level 4 Orchestrator

This module coordinates the Level 4 agents (Recommendations & Visualization).
"""

import logging
from typing import Dict, Any
from src.agents.level4 import (
    aggregator_agent,
    visualization_agent,
    summary_agent
)

# Configure logging
logger = logging.getLogger(__name__)

class Level4Orchestrator:
    """Orchestrates Level 4 processing"""

    def __init__(self):
        """Initialize the Level 4 Orchestrator"""
        logger.info("Initializing Level 4 Orchestrator")

    def process_recommendations(self, level3_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Level 4 recommendations and visualizations

        Args:
            level3_data: Outputs from Level 3 agents

        Returns:
            Recommendations and visualizations
        """
        # Step 1: Aggregate analysis
        aggregation_result = aggregator_agent.generate_summary(level3_data)
        logger.debug(f"Aggregation result: {aggregation_result}")

        # Step 2: Generate visualizations
        visualization_result = visualization_agent.generate_visualization(aggregation_result)
        logger.debug(f"Visualization result: {visualization_result}")

        # Step 3: Generate final summary
        summary_result = summary_agent.generate_summary(aggregation_result)
        logger.debug(f"Summary result: {summary_result}")

        return {
            "aggregation": aggregation_result,
            "visualization": visualization_result,
            "summary": summary_result
        }

# Create a global instance for easy access
level4_orchestrator = Level4Orchestrator()
