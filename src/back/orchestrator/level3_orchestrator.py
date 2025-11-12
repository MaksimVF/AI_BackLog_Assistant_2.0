


"""
Level 3 Orchestrator

This module coordinates the Level 3 agents (Analysis & Evaluation).
"""

import logging
from typing import Dict, Any
from src.agents.level3 import (
    risk_assessment_agent,
    resource_availability_agent,
    impact_potential_agent,
    confidence_urgency_agent,
    task_prioritization_agent
)

# Configure logging
logger = logging.getLogger(__name__)

class Level3Orchestrator:
    """Orchestrates Level 3 processing"""

    def __init__(self):
        """Initialize the Level 3 Orchestrator"""
        logger.info("Initializing Level 3 Orchestrator")

    def analyze_task(self, text: str, task_type: str = "general") -> Dict[str, Any]:
        """
        Analyze task through Level 3 pipeline

        Args:
            text: Input text to analyze
            task_type: Type of task (bug, idea, feedback, etc.)

        Returns:
            Analysis results with risk, resources, impact, confidence/urgency, and prioritization
        """
        # Step 1: Risk Assessment
        risk_result = risk_assessment_agent.evaluate_risk(text)
        logger.debug(f"Risk assessment result: {risk_result}")

        # Step 2: Resource Availability
        resource_result = resource_availability_agent.assess_resources(text)
        logger.debug(f"Resource assessment result: {resource_result}")

        # Step 3: Impact Potential
        impact_result = impact_potential_agent.assess_impact(text)
        logger.debug(f"Impact assessment result: {impact_result}")

        # Step 4: Confidence & Urgency
        confidence_result = confidence_urgency_agent.score_task(text)
        logger.debug(f"Confidence/urgency result: {confidence_result}")

        # Step 5: Task Prioritization - enhanced prioritization
        prioritization_result = task_prioritization_agent.prioritize_task(text, task_type)
        logger.debug(f"Prioritization result: {prioritization_result}")

        return {
            "risk": risk_result,
            "resources": resource_result,
            "impact": impact_result,
            "confidence_urgency": confidence_result,
            "prioritization": prioritization_result
        }

# Create a global instance for easy access
level3_orchestrator = Level3Orchestrator()
