




"""
Confidence & Urgency Agent Module

This module scores confidence and urgency for task prioritization.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from src.utils.llm_client import llm_client
from src.utils.prompts import CONFIDENCE_URGENCY_PROMPT

# Configure logging
logger = logging.getLogger(__name__)

class ConfidenceUrgencyScore(BaseModel):
    """Data model for confidence and urgency scores"""
    confidence: float  # 0-1 scale
    urgency: float  # 0-10 scale
    rationale: str

class ConfidenceUrgencyAgent:
    """Agent for scoring confidence and urgency"""

    def __init__(self):
        """Initialize the Confidence & Urgency Agent"""
        logger.info("Initializing Confidence & Urgency Agent")

    def _calculate_scores(self, text: str) -> ConfidenceUrgencyScore:
        """Calculate confidence and urgency using simple heuristics"""
        # Base scores
        confidence = 0.7  # default confidence
        urgency = 3.0  # default urgency

        # Increase urgency for time-sensitive keywords
        urgency_keywords = ["urgent", "immediate", "ASAP", "deadline", "critical", "blocker"]
        for keyword in urgency_keywords:
            if keyword in text.lower():
                urgency += 2.0

        # Increase confidence for clear, detailed descriptions
        detail_indicators = ["steps", "plan", "requirements", "specification", "detailed"]
        for indicator in detail_indicators:
            if indicator in text.lower():
                confidence = min(0.95, confidence + 0.1)

        # Decrease confidence for vague terms
        vague_terms = ["maybe", "possibly", "not sure", "unsure", "might"]
        for term in vague_terms:
            if term in text.lower():
                confidence = max(0.1, confidence - 0.15)

        # Cap urgency at 10
        urgency = min(10.0, max(0.0, urgency))

        # Generate rationale
        rationale = "Standard task"
        if urgency > 7:
            rationale = "High urgency due to time-sensitive keywords"
        if confidence < 0.5:
            rationale = "Low confidence due to vague language"

        return ConfidenceUrgencyScore(
            confidence=confidence,
            urgency=urgency,
            rationale=rationale
        )

    def score_task(self, text: str) -> Dict[str, Any]:
        """
        Score the confidence and urgency of a task

        Args:
            text: Input text to score

        Returns:
            Scoring result
        """
        # Try to use LLM for confidence and urgency scoring if available
        try:
            # Use LLM for scoring
            prompt = CONFIDENCE_URGENCY_PROMPT.format(input_text=text)
            response = llm_client.generate_json(prompt)

            if response and "confidence" in response and "urgency" in response and not response.get("error"):
                # Parse LLM response
                confidence = response.get("confidence", 0.7)
                urgency = response.get("urgency", 3.0)
                rationale = response.get("rationale", "LLM-based scoring")

                return {
                    "confidence": confidence,
                    "urgency": urgency,
                    "rationale": rationale,
                    "method": "llm"
                }

        except Exception as e:
            logger.warning(f"LLM scoring failed, falling back to heuristic: {e}")
            # Fallback to heuristic
            scores = self._calculate_scores(text)

            return {
                "confidence": scores.confidence,
                "urgency": scores.urgency,
                "rationale": scores.rationale,
                "method": "heuristic_fallback"
            }

        # Fallback to heuristic if LLM response is not usable
        scores = self._calculate_scores(text)
        return {
            "confidence": scores.confidence,
            "urgency": scores.urgency,
            "rationale": scores.rationale,
            "method": "heuristic_fallback"
        }

# Create a global instance for easy access
confidence_urgency_agent = ConfidenceUrgencyAgent()
