"""
Main Orchestrator

This module coordinates the entire workflow across all levels.
"""

import logging
from typing import Dict, Any
from src.orchestrator.level1_orchestrator import level1_orchestrator
from src.orchestrator.level2_orchestrator import level2_orchestrator
from src.orchestrator.level3_orchestrator import level3_orchestrator
from src.orchestrator.level4_orchestrator import level4_orchestrator

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
        logger.info(f"🔄 Starting workflow processing for: {input_data[:50]}...")

        # Step 1: Level 1 Processing
        logger.info("📥 LEVEL 1: Input Processing")
        level1_result = level1_orchestrator.process_input(input_data, metadata)
        logger.info(f"✅ Level 1 completed - Modality: {level1_result.get('modality', 'unknown')}")

        # Step 2: Level 2 Analysis
        logger.info("🔍 LEVEL 2: Text Analysis")
        level2_result = level2_orchestrator.analyze_text(level1_result["content"])
        logger.info(f"✅ Level 2 completed - Sentiment: {level2_result.get('sentiment', 'N/A')}")

        # Step 3: Level 3 Analysis
        logger.info("📊 LEVEL 3: Task Analysis")
        level3_result = level3_orchestrator.analyze_task(level1_result["content"])
        logger.info(f"✅ Level 3 completed - Classification: {level3_result.get('classification', 'N/A')}")

        # Step 4: Level 4 Recommendations
        logger.info("💡 LEVEL 4: Recommendations")
        level4_result = level4_orchestrator.process_recommendations(level3_result)
        logger.info(f"✅ Level 4 completed - Recommendation: {level4_result.get('recommendation', 'N/A')}")

        logger.info("🎯 Workflow processing completed successfully")

        # Combine results
        return {
            "level1": level1_result,
            "level2": level2_result,
            "level3": level3_result,
            "level4": level4_result
        }


# Create a global instance for easy access
main_orchestrator = MainOrchestrator()
