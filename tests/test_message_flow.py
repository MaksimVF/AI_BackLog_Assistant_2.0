



import asyncio
import logging
from src.bot.telegram_bot import telegram_bot
from src.orchestrator.main_orchestrator import main_orchestrator

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_message_flow():
    """Test message flow through all levels with detailed logging"""
    logger.info("Starting message flow test...")

    # Test message
    test_message = "Implement user authentication system"
    user_id = "test_user_123"

    logger.info(f"Sending test message: '{test_message}'")

    # Process through Telegram bot (simulating receiving a message)
    result = await telegram_bot.process_telegram_message(test_message, user_id)

    logger.info("Message processing completed")
    logger.info(f"Task ID: {result['task_id']}")
    logger.info(f"Status: {result['status']}")

    # Show the results from each level
    workflow_result = result['result']

    logger.info("\n=== LEVEL 1 RESULTS ===")
    level1 = workflow_result.get('level1', {})
    logger.info(f"Modality: {level1.get('modality', 'unknown')}")
    logger.info(f"Content: {level1.get('content', 'N/A')[:50]}...")

    logger.info("\n=== LEVEL 2 RESULTS ===")
    level2 = workflow_result.get('level2', {})
    logger.info(f"Sentiment: {level2.get('sentiment', 'N/A')}")
    logger.info(f"Keywords: {level2.get('keywords', [])[:5]}...")

    logger.info("\n=== LEVEL 3 RESULTS ===")
    level3 = workflow_result.get('level3', {})
    logger.info(f"Classification: {level3.get('classification', 'N/A')}")
    logger.info(f"Risk Score: {level3.get('risk_score', 'N/A')}")
    logger.info(f"Impact Score: {level3.get('impact_score', 'N/A')}")

    logger.info("\n=== LEVEL 4 RESULTS ===")
    level4 = workflow_result.get('level4', {})
    logger.info(f"Recommendation: {level4.get('recommendation', 'N/A')}")

    logger.info("\n=== DUPLICATE ANALYSIS ===")
    logger.info(f"Is Duplicate: {workflow_result.get('is_duplicate', False)}")
    logger.info(f"Duplicate Analysis: {workflow_result.get('duplicate_analysis', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(test_message_flow())

