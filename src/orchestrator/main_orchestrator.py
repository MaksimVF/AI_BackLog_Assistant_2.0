
"""
Main Orchestrator

This module coordinates the entire workflow across all levels.
"""

import logging
from typing import Dict, Any
from src.orchestrator.level1_orchestrator import level1_orchestrator
from src.orchestrator.level2_orchestrator import level2_orchestrator

# Configure logging
logger = logging.getLogger(__name__)

class MainOrchestrator:
    """Main orchestrator for the entire workflow"""

    def __init__(self):
        """Initialize the Main Orchestrator"""
        logger.info("Initializing Main Orchestrator")

    def process_workflow(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process the entire workflow from input to analysis

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Complete processing results
        """
        # Step 1: Level 1 Processing
        level1_result = level1_orchestrator.process_input(input_data, metadata)
        logger.debug(f"Level 1 result: {level1_result}")

        # Step 2: Level 2 Analysis
        level2_result = level2_orchestrator.analyze_text(level1_result["content"])
        logger.debug(f"Level 2 result: {level2_result}")

        # Combine results
        return {
            "level1": level1_result,
            "level2": level2_result
        }

# Create a global instance for easy access
main_orchestrator = MainOrchestrator()
