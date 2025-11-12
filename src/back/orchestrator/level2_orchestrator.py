
"""
Level 2 Orchestrator

This module coordinates the Level 2 agents (Semantic Analysis).
"""

import logging
from typing import Dict, Any
from src.agents.level2.reflection_agent import reflection_agent
from src.agents.level2.semantic_block_classifier import semantic_block_classifier
from src.agents.level2.contextualiza_agent import contextualiza_agent
from src.agents.level2.advanced_task_classifier import advanced_task_classifier

# Configure logging
logger = logging.getLogger(__name__)








class Level2Orchestrator:
    """Orchestrates Level 2 processing"""

    def __init__(self):
        """Initialize the Level 2 Orchestrator"""
        logger.info("Initializing Level 2 Orchestrator")

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text through Level 2 pipeline

        Args:
            text: Input text to analyze

        Returns:
            Analysis results with classification, blocks, and context
        """
        # Step 1: Advanced Task Classifier - enhanced classification
        advanced_classification = advanced_task_classifier.classify_task(text)
        logger.debug(f"Advanced classification result: {advanced_classification}")

        # Step 2: Reflection Agent - basic classification (for compatibility)
        reflection_result = reflection_agent.interpret_task(text)
        logger.debug(f"Reflection result: {reflection_result}")

        # Step 3: Semantic Block Classifier - segment text
        block_result = semantic_block_classifier.classify_blocks(text)
        logger.debug(f"Block classification result: {block_result}")

        # Step 4: Contextualiza Agent - extract entities and domain
        context_result = contextualiza_agent.extract_entities(text)
        logger.debug(f"Context result: {context_result}")

        return {
            "advanced_classification": advanced_classification.model_dump(),
            "reflection": reflection_result,
            "blocks": block_result,
            "context": context_result
        }


# Create a global instance for easy access

level2_orchestrator = Level2Orchestrator()
