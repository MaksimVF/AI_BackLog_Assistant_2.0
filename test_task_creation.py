


import asyncio
import logging
from src.bot.telegram_bot import telegram_bot
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_task_creation():
    """Test that we can create multiple tasks with the same content without UNIQUE constraint violations"""
    logger.info("Testing task creation with same content...")

    # Test creating multiple tasks with the same content
    test_message = "Test message content"
    user_id = "test_user"

    # Create first task
    result1 = await telegram_bot.process_telegram_message(test_message, user_id)
    logger.info(f"First task created: {result1['task_id']}")

    # Create second task with same content
    result2 = await telegram_bot.process_telegram_message(test_message, user_id)
    logger.info(f"Second task created: {result2['task_id']}")

    # Verify they have different task IDs
    if result1['task_id'] != result2['task_id']:
        logger.info("✅ SUCCESS: Tasks have different IDs")
    else:
        logger.error("❌ FAILURE: Tasks have the same ID")

    # Verify both tasks are in the database
    async with AsyncSessionLocal() as db:
        task1 = await TaskRepository.get_task_by_id(db, result1['task_id'])
        task2 = await TaskRepository.get_task_by_id(db, result2['task_id'])

        if task1 and task2:
            logger.info("✅ SUCCESS: Both tasks found in database")
        else:
            logger.error("❌ FAILURE: One or both tasks not found in database")

if __name__ == "__main__":
    asyncio.run(test_task_creation())


