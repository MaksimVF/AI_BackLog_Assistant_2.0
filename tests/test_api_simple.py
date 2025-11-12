

from fastapi import FastAPI
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Start background tasks when the API starts"""
    logger.info("Starting API startup tasks...")

    # Simulate starting Telegram bot in background mode
    try:
        logger.info("Starting Telegram bot in background mode...")
        # Simulate the background task
        asyncio.create_task(background_task())
        logger.info("Telegram bot started successfully in background")
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")
        logger.error("Telegram bot will not be available")

async def background_task():
    """Simulate a background task"""
    logger.info("Background task started")
    await asyncio.sleep(30)  # Run for 30 seconds
    logger.info("Background task completed")

@app.get("/")
async def read_root():
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

