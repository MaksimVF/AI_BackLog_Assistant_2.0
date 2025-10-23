
import asyncio
import logging
from src.bot.telegram_bot import telegram_bot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_background_polling():
    """Test the background polling functionality"""
    logger.info("Testing background polling...")

    try:
        # Start the bot in background mode
        await telegram_bot.start_polling_background()

        # Keep the event loop running for a while
        await asyncio.sleep(10)
        logger.info("Background polling test completed successfully")

    except Exception as e:
        logger.error(f"Error in background polling test: {e}")

if __name__ == "__main__":
    asyncio.run(test_background_polling())
