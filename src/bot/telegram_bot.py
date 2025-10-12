
"""
Telegram Bot Integration for AI Backlog Assistant

This module implements the Telegram bot interface for task submission and status checking.
"""

import logging
from typing import Dict, Any
from src.config import Config
from src.orchestrator.main_orchestrator import main_orchestrator
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository, TaskFileRepository, TriggerRepository
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize config
config = Config()

class TelegramBot:
    """Telegram Bot for AI Backlog Assistant"""

    def __init__(self):
        """Initialize the Telegram Bot"""
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.application = None
        logger.info("Telegram Bot initialized")

    async def process_telegram_message(self, message_text: str, user_id: str = "unknown") -> Dict[str, Any]:
        """
        Process a Telegram message through the workflow

        Args:
            message_text: The text message from Telegram
            user_id: The user ID from Telegram

        Returns:
            Processed result
        """
        try:
            # Create metadata for the task
            metadata = {
                "source": "telegram",
                "user_id": user_id,
                "username": "telegram_user",
                "chat_id": "telegram_chat"
            }

            # Process through the workflow
            result = main_orchestrator.process_workflow(message_text, metadata)

            # Generate a simple task ID
            task_id = f"task_{hash(message_text) % 1000000}"

            # Store in database
            async with AsyncSessionLocal() as db:
                task_data = {
                    "task_id": task_id,
                    "input_data": message_text,
                    "metadata": metadata,
                    "status": "completed",
                    "classification": result.get("classification", "unknown"),
                    "risk_score": result.get("risk_score"),
                    "impact_score": result.get("impact_score"),
                    "confidence_score": result.get("confidence_score"),
                    "urgency_score": result.get("urgency_score"),
                    "recommendation": result.get("recommendation"),
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }

                await TaskRepository.create_task(db, task_data)

            return {
                "task_id": task_id,
                "status": "completed",
                "result": result
            }

        except Exception as e:
            logger.error(f"Error processing Telegram message: {e}")
            return {
                "task_id": "error",
                "status": "failed",
                "error": str(e)
            }

    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a task

        Args:
            task_id: The task ID to check

        Returns:
            Task status information
        """
        try:
            async with AsyncSessionLocal() as db:
                task = await TaskRepository.get_task_by_task_id(db, task_id)

                if not task:
                    return {
                        "task_id": task_id,
                        "status": "not_found",
                        "error": "Task not found"
                    }

                return {
                    "task_id": task.task_id,
                    "status": task.status,
                    "classification": task.classification,
                    "risk_score": task.risk_score,
                    "impact_score": task.impact_score,
                    "recommendation": task.recommendation
                }

        except Exception as e:
            logger.error(f"Error getting task status: {e}")
            return {
                "task_id": task_id,
                "status": "error",
                "error": str(e)
            }

    async def list_tasks(self) -> Dict[str, Any]:
        """
        List recent tasks

        Returns:
            List of recent tasks
        """
        try:
            async with AsyncSessionLocal() as db:
                tasks = await TaskRepository.list_tasks(db, limit=10)

                formatted_tasks = []
                for task in tasks:
                    formatted_tasks.append({
                        "task_id": task.task_id,
                        "description": task.input_data[:50] + "...",
                        "status": task.status,
                        "recommendation": task.recommendation or "No recommendation"
                    })

                return {"tasks": formatted_tasks}

        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            return {
                "tasks": [],
                "error": str(e)
            }

    async def get_task_archive(self, task_id: str) -> Dict[str, Any]:
        """
        Get task archive details

        Args:
            task_id: The task ID to archive

        Returns:
            Task archive details
        """
        try:
            async with AsyncSessionLocal() as db:
                task = await TaskRepository.get_task_by_task_id(db, task_id)

                if not task:
                    return {
                        "task_id": task_id,
                        "status": "not_found",
                        "error": "Task not found"
                    }

                # Get associated files
                files = await TaskFileRepository.get_files_by_task_id(db, task_id)
                file_urls = [file.file_url for file in files]

                return {
                    "task_id": task.task_id,
                    "original_input": task.input_data,
                    "classification": task.classification,
                    "analysis_results": {
                        "risk_score": task.risk_score,
                        "impact_score": task.impact_score,
                        "confidence_score": task.confidence_score,
                        "urgency_score": task.urgency_score
                    },
                    "recommendation": task.recommendation,
                    "files": file_urls
                }

        except Exception as e:
            logger.error(f"Error getting task archive: {e}")
            return {
                "task_id": task_id,
                "status": "error",
                "error": str(e)
            }

async def start_polling(self):
        """Start polling for Telegram messages"""
        if not self.bot_token:
            logger.error("TELEGRAM_BOT_TOKEN is not set in configuration")
            return

        # Create the Telegram application
        self.application = Application.builder().token(self.bot_token).build()

        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Start the bot
        logger.info("Starting Telegram bot polling...")
        await self.application.run_polling()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        await update.message.reply_text("Welcome to AI Backlog Assistant! Send me a task description to get started.")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        help_text = (
            "AI Backlog Assistant Bot\n"
            "Available commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "Just send a task description to process it"
        )
        await update.message.reply_text(help_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages"""
        message_text = update.message.text
        user_id = str(update.message.from_user.id)

        # Process the message through our workflow
        result = await self.process_telegram_message(message_text, user_id)

        # Send response
        response_text = f"Task processed! ID: {result['task_id']}\n"
        response_text += f"Status: {result['status']}\n"
        if result['status'] == 'completed':
            classification = result['result'].get('classification', 'unknown')
            response_text += f"Classification: {classification}\n"
            response_text += "Recommendation: " + result['result'].get('recommendation', 'No recommendation')

        await update.message.reply_text(response_text)

# Create a global instance
telegram_bot = TelegramBot()
