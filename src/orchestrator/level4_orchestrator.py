



"""
Level 4 Orchestrator

This module coordinates the Level 4 agents (Recommendations & Visualization).
"""

import logging
from typing import Dict, Any
from datetime import datetime, timedelta
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

        # Add additional data for enhanced visualizations
        enhanced_analysis = self._enhance_analysis_data(aggregation_result)

        # Step 2: Generate visualizations
        visualization_result = visualization_agent.generate_visualization(enhanced_analysis)
        logger.debug(f"Visualization result: {visualization_result}")

        # Step 3: Generate final summary
        summary_result = summary_agent.generate_summary(aggregation_result)
        logger.debug(f"Summary result: {summary_result}")

        return {
            "aggregation": aggregation_result,
            "visualization": visualization_result,
            "summary": summary_result
        }

    def _enhance_analysis_data(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance analysis data with additional information for visualizations

        Args:
            analysis_data: Original analysis data

        Returns:
            Enhanced analysis data with additional visualization data
        """
        # Add sample status distribution data
        enhanced_data = analysis_data.copy()

        # Add status distribution for pie chart
        enhanced_data["status_distribution"] = {
            "new": 5,
            "in_progress": 8,
            "completed": 12,
            "on_hold": 3,
            "cancelled": 1
        }

        # Add trend data for line chart
        today = datetime.now()
        enhanced_data["trend_data"] = [
            {
                "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
                "value": 3 + i,
                "metric": "Task Completion Rate"
            }
            for i in range(7)
        ]

        # Add resource allocation data for grouped bar chart
        enhanced_data["resource_allocation"] = {
            "Backend Team": {"bugs": 3, "features": 5, "refactoring": 2},
            "Frontend Team": {"bugs": 2, "features": 4, "design": 3},
            "QA Team": {"testing": 6, "automation": 2}
        }

        return enhanced_data

# Create a global instance for easy access
level4_orchestrator = Level4Orchestrator()
