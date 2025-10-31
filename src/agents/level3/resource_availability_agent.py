


"""
Resource Availability Agent Module

This module assesses the resource requirements for a task.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from src.utils.llm_client import llm_client
from src.utils.prompts import RESOURCE_AVAILABILITY_PROMPT

# Configure logging
logger = logging.getLogger(__name__)

class ResourceEstimate(BaseModel):
    """Data model for resource estimation"""
    time_hours: float
    team_size: int
    skills: List[str]
    cost_estimate: Optional[float] = None
    confidence: float  # 0-1

class ResourceAvailabilityAgent:
    """Agent for estimating resource requirements"""

    def __init__(self):
        """Initialize the Resource Availability Agent"""
        logger.info("Initializing Resource Availability Agent")

    def _estimate_resources(self, text: str) -> ResourceEstimate:
        """Estimate resources using simple heuristics"""
        # Simple heuristic based on text length and keywords
        word_count = len(text.split())

        # Base estimates
        time_hours = max(5.0, word_count / 20.0)  # 5 hours minimum
        team_size = 1
        skills = ["general"]
        confidence = 0.7

        # Adjust for keywords
        if any(keyword in text.lower() for keyword in ["complex", "large", "major", "overhaul"]):
            time_hours *= 2.0
            team_size = 2
            skills.append("senior")

        if any(keyword in text.lower() for keyword in ["design", "UI", "UX", "interface"]):
            skills.append("design")

        if any(keyword in text.lower() for keyword in ["database", "backend", "API", "server"]):
            skills.append("backend")

        if any(keyword in text.lower() for keyword in ["frontend", "JavaScript", "React", "Vue"]):
            skills.append("frontend")

        return ResourceEstimate(
            time_hours=time_hours,
            team_size=team_size,
            skills=skills,
            confidence=confidence
        )

    def assess_resources(self, text: str) -> Dict[str, Any]:
        """
        Assess the resource requirements for a task

        Args:
            text: Input text to assess

        Returns:
            Resource assessment result
        """
        # Try to use LLM for resource estimation if available
        try:
            # Use LLM for resource estimation
            prompt = RESOURCE_AVAILABILITY_PROMPT.format(input_text=text)
            response = llm_client.generate_json(prompt)

            if response and "time_hours" in response and not response.get("error"):
                # Parse LLM response
                time_hours = response.get("time_hours", 5.0)
                team_size = response.get("team_size", 1)
                skills = response.get("skills", ["general"])
                cost_estimate = response.get("cost_estimate")
                confidence = response.get("confidence", 0.9)

                return {
                    "time_hours": time_hours,
                    "team_size": team_size,
                    "skills": skills,
                    "cost_estimate": cost_estimate,
                    "confidence": confidence,
                    "method": "llm"
                }

        except Exception as e:
            logger.warning(f"LLM resource estimation failed, falling back to heuristic: {e}")
            # Fallback to heuristic
            estimate = self._estimate_resources(text)

            return {
                "time_hours": estimate.time_hours,
                "team_size": estimate.team_size,
                "skills": estimate.skills,
                "cost_estimate": estimate.cost_estimate,
                "confidence": estimate.confidence,
                "method": "heuristic_fallback"
            }

        # Fallback to heuristic if LLM response is not usable
        estimate = self._estimate_resources(text)
        return {
            "time_hours": estimate.time_hours,
            "team_size": estimate.team_size,
            "skills": estimate.skills,
            "cost_estimate": estimate.cost_estimate,
            "confidence": estimate.confidence,
            "method": "heuristic_fallback"
        }

# Create a global instance for easy access
resource_availability_agent = ResourceAvailabilityAgent()
