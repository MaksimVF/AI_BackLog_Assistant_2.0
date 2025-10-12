



"""
Aggregator Agent Module

This module combines the outputs from Level 3 agents to create a comprehensive analysis.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

class AggregatedAnalysis(BaseModel):
    """Data model for aggregated analysis results"""
    overall_score: float  # 0-10 scale
    risk_score: float
    impact_score: float
    urgency: float
    confidence: float
    recommendation: str
    details: Optional[Dict[str, Any]] = None

class AggregatorAgent:
    """Agent for aggregating Level 3 outputs"""

    def __init__(self):
        """Initialize the Aggregator Agent"""
        logger.info("Initializing Aggregator Agent")

    def _calculate_overall_score(self, risk: float, impact: float, urgency: float) -> float:
        """Calculate an overall score based on risk, impact, and urgency"""
        # Simple weighted average: 40% impact, 30% urgency, 30% risk
        return (0.4 * impact) + (0.3 * urgency) + (0.3 * risk)

    def _generate_recommendation(self, overall_score: float, confidence: float) -> str:
        """Generate a recommendation based on scores"""
        if confidence < 0.4:
            return "Needs clarification"
        elif overall_score > 7:
            return "High priority - Implement immediately"
        elif overall_score > 4:
            return "Medium priority - Schedule for next sprint"
        else:
            return "Low priority - Consider for backlog"

    def aggregate_analysis(self, level3_data: Dict[str, Any]) -> AggregatedAnalysis:
        """
        Aggregate Level 3 outputs into a comprehensive analysis

        Args:
            level3_data: Outputs from Level 3 agents

        Returns:
            Aggregated analysis result
        """
        # Extract scores from Level 3 data
        risk_score = level3_data["risk"]["risk_score"]
        impact_score = level3_data["impact"]["impact_score"]
        urgency = level3_data["confidence_urgency"]["urgency"]
        confidence = level3_data["confidence_urgency"]["confidence"]

        # Calculate overall score
        overall_score = self._calculate_overall_score(risk_score, impact_score, urgency)

        # Generate recommendation
        recommendation = self._generate_recommendation(overall_score, confidence)

        return AggregatedAnalysis(
            overall_score=overall_score,
            risk_score=risk_score,
            impact_score=impact_score,
            urgency=urgency,
            confidence=confidence,
            recommendation=recommendation,
            details={
                "risk_details": level3_data["risk"],
                "impact_details": level3_data["impact"],
                "resource_details": level3_data["resources"]
            }
        )

    def generate_summary(self, level3_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of the aggregated analysis

        Args:
            level3_data: Outputs from Level 3 agents

        Returns:
            Summary result as dictionary
        """
        analysis = self.aggregate_analysis(level3_data)

        return {
            "overall_score": analysis.overall_score,
            "recommendation": analysis.recommendation,
            "risk_score": analysis.risk_score,
            "impact_score": analysis.impact_score,
            "urgency": analysis.urgency,
            "confidence": analysis.confidence,
            "details": analysis.details
        }

# Create a global instance for easy access
aggregator_agent = AggregatorAgent()
