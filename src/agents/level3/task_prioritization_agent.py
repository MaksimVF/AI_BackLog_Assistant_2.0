
"""
Task Prioritization Agent Module

This module combines multiple scoring systems to provide comprehensive
task prioritization based on risk, impact, urgency, and resource requirements.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Import other agents
from src.agents.level3.risk_assessment_agent import risk_assessment_agent
from src.agents.level3.impact_potential_agent import impact_potential_agent
from src.agents.level3.confidence_urgency_agent import confidence_urgency_agent
from src.agents.level3.resource_availability_agent import resource_availability_agent

# Configure logging
logger = logging.getLogger(__name__)

class PrioritizationScore(BaseModel):
    """Data model for comprehensive prioritization score"""
    priority_score: float  # 0-100 scale
    risk_score: float  # 0-10 scale
    impact_score: float  # 0-10 scale
    urgency_score: float  # 0-10 scale
    confidence_score: float  # 0-1 scale
    resource_estimate: Dict[str, Any]
    classification: str  # idea/bug/feedback
    recommendation: str

class TaskPrioritizationAgent:
    """Agent for comprehensive task prioritization"""

    def __init__(self):
        """Initialize the Task Prioritization Agent"""
        logger.info("Initializing Task Prioritization Agent")

    def _calculate_priority_score(self,
                                 risk: float,
                                 impact: float,
                                 urgency: float,
                                 confidence: float) -> float:
        """Calculate comprehensive priority score"""
        # Weighted scoring - adjust weights based on importance
        # For bugs: risk and urgency are most important
        # For ideas: impact and confidence are most important
        # For feedback: balance between all factors
        priority = (risk * 2.0 + impact * 2.5 + urgency * 2.0 + confidence * 10.0)

        # Normalize to 0-100 scale with better distribution
        return min(100.0, max(0.0, priority * 3.0))

    def _generate_recommendation(self, priority: float, classification: str) -> str:
        """Generate recommendation based on priority and classification"""
        if priority > 80:
            if classification == "bug":
                return "Critical bug - address immediately"
            elif classification == "idea":
                return "High-potential idea - prioritize for next sprint"
            else:
                return "Urgent feedback - requires quick response"
        elif priority > 50:
            if classification == "bug":
                return "Important bug - schedule for next maintenance"
            elif classification == "idea":
                return "Valuable idea - add to backlog"
            else:
                return "Significant feedback - review and plan response"
        else:
            if classification == "bug":
                return "Minor bug - address when resources allow"
            elif classification == "idea":
                return "Interesting idea - consider for future"
            else:
                return "General feedback - acknowledge and monitor"

    def prioritize_task(self, text: str, classification: str) -> Dict[str, Any]:
        """
        Prioritize a task using comprehensive scoring

        Args:
            text: Input text to prioritize
            classification: Task classification (idea/bug/feedback)

        Returns:
            Prioritization result
        """
        # Get individual scores
        risk_result = risk_assessment_agent.evaluate_risk(text)
        impact_result = impact_potential_agent.assess_impact(text)
        confidence_urgency_result = confidence_urgency_agent.score_task(text)
        resource_result = resource_availability_agent.assess_resources(text)

        # Calculate comprehensive priority score
        priority_score = self._calculate_priority_score(
            risk_result["risk_score"],
            impact_result["impact_score"],
            confidence_urgency_result["urgency"],
            confidence_urgency_result["confidence"]
        )

        # Generate recommendation
        recommendation = self._generate_recommendation(priority_score, classification)

        # Determine priority level with better thresholds
        if priority_score > 85:
            priority_level = "Critical"
        elif priority_score > 60:
            priority_level = "High"
        elif priority_score > 30:
            priority_level = "Medium"
        else:
            priority_level = "Low"

        return {
            "priority_score": priority_score,
            "priority_level": priority_level,
            "risk_score": risk_result["risk_score"],
            "impact_score": impact_result["impact_score"],
            "urgency_score": confidence_urgency_result["urgency"],
            "confidence_score": confidence_urgency_result["confidence"],
            "resource_estimate": resource_result,
            "classification": classification,
            "recommendation": recommendation,
            "details": {
                "risk": risk_result,
                "impact": impact_result,
                "confidence_urgency": confidence_urgency_result,
                "resources": resource_result
            }
        }

# Create a global instance for easy access
task_prioritization_agent = TaskPrioritizationAgent()
