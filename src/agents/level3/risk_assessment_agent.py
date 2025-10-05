

"""
Risk Assessment Agent Module

This module evaluates the risk associated with a task using various scoring methods.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

class RiskScore(BaseModel):
    """Data model for risk assessment results"""
    score: float  # 0-10 scale
    method: str  # e.g., "RICE", "Kano", "heuristic"
    details: Optional[Dict[str, Any]] = None

class RiskAssessmentAgent:
    """Agent for assessing risk of tasks"""

    def __init__(self):
        """Initialize the Risk Assessment Agent"""
        logger.info("Initializing Risk Assessment Agent")

    def _heuristic_risk_score(self, text: str) -> float:
        """Calculate risk using simple heuristics"""
        # Simple heuristic: longer texts and certain keywords increase risk
        risk = 3.0  # base risk

        # Increase risk for certain keywords
        keywords = ["urgent", "critical", "blocker", "security", "vulnerability", "deadline"]
        for keyword in keywords:
            if keyword in text.lower():
                risk += 1.5

        # Increase risk for longer texts (more complexity)
        word_count = len(text.split())
        if word_count > 100:
            risk += 1.0
        if word_count > 200:
            risk += 1.0

        # Cap at 10
        return min(10.0, max(0.0, risk))

    def assess_risk(self, text: str, method: str = "heuristic") -> RiskScore:
        """
        Assess the risk of a task

        Args:
            text: Input text to assess
            method: Scoring method (heuristic, RICE, Kano)

        Returns:
            Risk assessment result
        """
        if method == "heuristic":
            score = self._heuristic_risk_score(text)
            return RiskScore(
                score=score,
                method="heuristic",
                details={"text_length": len(text), "keywords_detected": True}
            )
        else:
            # Placeholder for other methods
            logger.warning(f"Method {method} not implemented, falling back to heuristic")
            return self.assess_risk(text, "heuristic")

    def evaluate_risk(self, text: str) -> Dict[str, Any]:
        """
        Evaluate risk and return detailed analysis

        Args:
            text: Input text to evaluate

        Returns:
            Risk evaluation result as dictionary
        """
        result = self.assess_risk(text)

        # Add interpretation
        interpretation = "Low"
        if result.score > 6:
            interpretation = "High"
        elif result.score > 3:
            interpretation = "Medium"

        return {
            "risk_score": result.score,
            "interpretation": interpretation,
            "method": result.method,
            "details": result.details
        }

# Create a global instance for easy access
risk_assessment_agent = RiskAssessmentAgent()

