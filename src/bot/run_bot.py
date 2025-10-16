

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

    # Check if we have a valid token
    from src.config import Config
    config = Config()
    token = config.telegram_api_key

    if not token:
        logger.error("⚠️  Telegram token is not set!")
        logger.error("   Please set a valid Telegram token in your .env file")
        logger.error("   You can get a token by creating a new bot with BotFather in Telegram")
        logger.error("   Bot will run in mock mode and won't connect to Telegram servers")
    elif token == "AIBLA":
        logger.error("⚠️  Using mock Telegram token 'AIBLA' - this is a placeholder token")
        logger.error("   Please replace 'AIBLA' with your real Telegram bot token in .env file")
        logger.error("   Bot will attempt to connect but will fail with this token")
    elif token.startswith('your_'):
        logger.error(f"⚠️  Using placeholder token: {token}")
        logger.error("   Please replace this with your real Telegram bot token in .env file")
        logger.error("   Bot will attempt to connect but will fail with this token")
    else:
        logger.info(f"✅ Using valid Telegram token: {token[:5]}...")
        logger.info("   Bot is starting with a valid token - should connect to Telegram servers")

    try:
        logger.info("🚀 Attempting to start Telegram bot polling...")
        await telegram_bot.start_polling()
    except Exception as e:
        logger.error(f"❌ Failed to start Telegram bot: {e}")
        logger.error("   Please check your Telegram token and network connection")
        logger.error("   If you're using a mock token, replace it with a real token in your .env file")
        logger.error("   You can get a real token by creating a new bot with BotFather in Telegram")

if __name__ == "__main__":
    asyncio.run(main())
