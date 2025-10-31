
"""
Reflection Agent Module

This module is responsible for classifying the type of task (idea, bug, feedback)
and providing initial interpretation of the input.
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from src.utils.llm_client import llm_client
from src.utils.prompts import REFLECTION_PROMPT

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
        # Try to use LLM for classification if available
        try:
            # Use the LLM client to classify the task
            prompt = REFLECTION_PROMPT.format(input_text=input_text)
            response = llm_client.generate_text(prompt)

            # Parse the response
            if "bug" in response.lower():
                task_type = "bug"
            elif "idea" in response.lower():
                task_type = "idea"
            elif "feedback" in response.lower():
                task_type = "feedback"
            else:
                # Fallback to simple heuristic if LLM response is unclear
                input_text_lower = input_text.lower()
                if any(keyword in input_text_lower for keyword in ["bug", "error", "issue", "problem", "fix"]):
                    task_type = "bug"
                elif any(keyword in input_text_lower for keyword in ["idea", "feature", "suggestion", "proposal", "improve"]):
                    task_type = "idea"
                else:
                    task_type = "feedback"  # default

            return TaskClassification(
                task_type=task_type,
                confidence=0.9 if "Mock response" not in response else 0.7,
                metadata={"classification_method": "llm" if "Mock response" not in response else "keyword_based"}
            )

        except Exception as e:
            logger.warning(f"LLM classification failed, falling back to heuristic: {e}")
            # Fallback to simple heuristic
            input_text_lower = input_text.lower()
            if any(keyword in input_text_lower for keyword in ["bug", "error", "issue", "problem", "fix"]):
                task_type = "bug"
            elif any(keyword in input_text_lower for keyword in ["idea", "feature", "suggestion", "proposal", "improve"]):
                task_type = "idea"
            else:
                task_type = "feedback"  # default

            return TaskClassification(
                task_type=task_type,
                confidence=0.7,
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
