
"""
Reflection Agent Module

This module is responsible for classifying the type of task (idea, bug, feedback)
and providing initial interpretation of the input.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)



class TaskClassification(BaseModel):
    """Data model for task classification"""
    task_type: str  # idea, bug, or feedback
    confidence: float  # confidence score 0-1
    metadata: Optional[Dict[str, Any]] = None



class ReflectionAgent:
    """Agent for reflecting on and classifying task types"""

    def __init__(self):
        """Initialize the Reflection Agent"""
        logger.info("Initializing Reflection Agent")

    def classify_task(self, input_text: str) -> TaskClassification:
        """
        Classify the task type (idea, bug, feedback)

        Args:
            input_text: The input text to classify

        Returns:
            Task classification result
        """
        # Simple heuristic for now - would use LLM in production
        input_text_lower = input_text.lower()

        # Basic keyword detection
        if any(keyword in input_text_lower for keyword in ["bug", "error", "issue", "problem", "fix"]):
            task_type = "bug"
        elif any(keyword in input_text_lower for keyword in ["idea", "feature", "suggestion", "proposal", "improve"]):
            task_type = "idea"
        else:
            task_type = "feedback"  # default

        # Return with confidence (placeholder for LLM integration)
        return TaskClassification(
            task_type=task_type,
            confidence=0.8,  # placeholder confidence
            metadata={"classification_method": "keyword_based"}
        )

    def interpret_task(self, input_text: str) -> Dict[str, Any]:
        """
        Provide interpretation of the task

        Args:
            input_text: The input text to interpret

        Returns:
            Interpretation metadata
        """
        classification = self.classify_task(input_text)

        return {
            "task_type": classification.task_type,
            "confidence": classification.confidence,
            "interpretation": f"Task classified as '{classification.task_type}' with confidence {classification.confidence:.2f}",
            "metadata": classification.metadata
        }

# Create a global instance for easy access
reflection_agent = ReflectionAgent()
