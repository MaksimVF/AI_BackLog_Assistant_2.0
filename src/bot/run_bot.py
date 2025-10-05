

"""
Entry point to run the Telegram bot
"""

import asyncio
import logging
from src.bot.telegram_bot import telegram_bot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Run the Telegram bot"""
    logger.info("Starting AI Backlog Assistant Telegram Bot...")
    await telegram_bot.start_polling()

if __name__ == "__main__":
    asyncio.run(main())

