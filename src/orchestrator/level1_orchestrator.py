
"""
Level 1 Orchestrator

This module coordinates the Level 1 agents (Input Processing).
"""

import logging
from typing import Dict, Any
import pytest
import pytest
from src.agents.level1.input_agent import input_agent
import pytest
import pytest
from src.agents.level1.modality_detector import modality_detector
import pytest
import pytest
from src.agents.level1.preprocessor import preprocessor

# Configure logging
logger = logging.getLogger(__name__)

class Level1Orchestrator:
    """Orchestrates Level 1 processing"""

    def __init__(self):
        """Initialize the Level 1 Orchestrator"""
        logger.info("Initializing Level 1 Orchestrator")

    def process_input(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process input through Level 1 pipeline

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed data with modality and content
        """
        # Step 1: Detect modality
        modality = modality_detector.detect(input_data)
        logger.debug(f"Detected modality: {modality}")

        # Step 2: Process with Input Agent
        processed_data = input_agent.process(input_data, metadata)
        logger.debug(f"Processed data: {processed_data}")

        # Step 3: If file-based, use preprocessor
        if modality in ["pdf", "audio", "image"]:
            file_path = processed_data.content  # Assuming content is file path
            text, preprocessing_metadata = preprocessor.preprocess_file(file_path, modality)
            processed_data.content = text
            processed_data.metadata.update(preprocessing_metadata)

        return {
            "modality": modality,
            "content": processed_data.content,
            "metadata": processed_data.metadata
        }

# Create a global instance for easy access
level1_orchestrator = Level1Orchestrator()

