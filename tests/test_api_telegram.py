


from fastapi import FastAPI
import logging
import asyncio
from src.bot.telegram_bot import telegram_bot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Start background tasks when the API starts"""
    logger.info("Starting API startup tasks...")

    # Start Telegram bot in background mode
    try:
        logger.info("Starting Telegram bot in background mode...")
        asyncio.create_task(telegram_bot.start_polling_background())
        logger.info("Telegram bot started successfully in background")
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")
        logger.error("Telegram bot will not be available")

@app.get("/")
async def read_root():
    return {"message": "API is running with Telegram bot"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


