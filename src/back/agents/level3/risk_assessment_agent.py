

"""
Risk Assessment Agent Module

This module evaluates the risk associated with a task using various scoring methods.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from src.utils.llm_client import llm_client
from src.utils.prompts import RISK_ASSESSMENT_PROMPT

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

    def assess_risk(self, text: str, method: str = "llm") -> RiskScore:
        """
        Assess the risk of a task

        Args:
            text: Input text to assess
            method: Scoring method (llm, heuristic, RICE, Kano)

        Returns:
            Risk assessment result
        """
        if method == "llm":
            try:
                # Use LLM for risk assessment
                prompt = RISK_ASSESSMENT_PROMPT.format(input_text=text)
                response = llm_client.generate_text(prompt)

                # Try to extract a number from the response
                import re
                logger.debug(f"LLM response for risk assessment: {response[:200]}...")
                numbers = re.findall(r'\d+(\.\d+)?', response)
                if numbers:
                    try:
                        score = float(numbers[0])
                        # Ensure score is within 0-10 range
                        score = min(10.0, max(0.0, score))
                        logger.debug(f"Extracted risk score: {score}")
                    except ValueError:
                        logger.warning(f"Could not convert LLM response to float: {numbers[0]}")
                        # Fallback to heuristic if conversion fails
                        score = self._heuristic_risk_score(text)
                else:
                    logger.warning(f"LLM response doesn't contain a number: {response[:100]}...")
                    # Fallback to heuristic if LLM response doesn't contain a number
                    score = self._heuristic_risk_score(text)

                return RiskScore(
                    score=score,
                    method="llm",
                    details={"text_length": len(text), "llm_response": response}
                )

            except Exception as e:
                logger.warning(f"LLM risk assessment failed, falling back to heuristic: {e}")
                # Fallback to heuristic
                score = self._heuristic_risk_score(text)
                return RiskScore(
                    score=score,
                    method="heuristic_fallback",
                    details={"text_length": len(text), "error": str(e)}
                )

        elif method == "heuristic":
            score = self._heuristic_risk_score(text)
            return RiskScore(
                score=score,
                method="heuristic",
                details={"text_length": len(text), "keywords_detected": True}
            )
        else:
            # Placeholder for other methods
            logger.warning(f"Method {method} not implemented, falling back to llm")
            return self.assess_risk(text, "llm")

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
