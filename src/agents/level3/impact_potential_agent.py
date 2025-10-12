



"""
Impact Potential Agent Module

This module measures the potential impact of a task.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

class ImpactScore(BaseModel):
    """Data model for impact assessment"""
    score: float  # 0-10 scale
    factors: Dict[str, float]  # individual factors
    confidence: float  # 0-1

class ImpactPotentialAgent:
    """Agent for assessing impact potential"""

    def __init__(self):
        """Initialize the Impact Potential Agent"""
        logger.info("Initializing Impact Potential Agent")

    def _calculate_impact(self, text: str) -> ImpactScore:
        """Calculate impact using simple heuristics"""
        # Base impact
        impact = 3.0

        # Increase for positive keywords
        positive_keywords = [
            "revenue", "growth", "users", "engagement", "retention",
            "conversion", "efficiency", "automation", "scalability"
        ]
        for keyword in positive_keywords:
            if keyword in text.lower():
                impact += 1.0

        # Increase for large scope
        scope_keywords = ["all users", "entire system", "company-wide", "global", "majority"]
        for keyword in scope_keywords:
            if keyword in text.lower():
                impact += 1.5

        # Cap at 10
        impact = min(10.0, max(0.0, impact))

        return ImpactScore(
            score=impact,
            factors={
                "positive_keywords": len([k for k in positive_keywords if k in text.lower()]),
                "scope_keywords": len([k for k in scope_keywords if k in text.lower()])
            },
            confidence=0.8
        )

    def assess_impact(self, text: str) -> Dict[str, Any]:
        """
        Assess the impact potential of a task

        Args:
            text: Input text to assess

        Returns:
            Impact assessment result
        """
        score = self._calculate_impact(text)

        # Add interpretation
        interpretation = "Low"
        if score.score > 7:
            interpretation = "High"
        elif score.score > 4:
            interpretation = "Medium"

        return {
            "impact_score": score.score,
            "interpretation": interpretation,
            "factors": score.factors,
            "confidence": score.confidence
        }

# Create a global instance for easy access
impact_potential_agent = ImpactPotentialAgent()
