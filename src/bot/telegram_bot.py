
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
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize config
config = Config()

class TelegramBot:
    """Telegram Bot for AI Backlog Assistant"""

    def __init__(self):
        """Initialize the Telegram Bot"""
        logger.info("Telegram Bot initialized")

        # Initialize Telegram bot and dispatcher
        self.bot = Bot(token=os.getenv("Telegram_API_Key", config.telegram_api_key))
        self.dp = Dispatcher()

        # Register handlers
        self.dp.message.register(self.handle_start, Command(commands=["start"]))
        self.dp.message.register(self.handle_help, Command(commands=["help"]))
        self.dp.message.register(self.handle_add, Command(commands=["add"]))
        self.dp.message.register(self.handle_status, Command(commands=["status"]))
        self.dp.message.register(self.handle_list, Command(commands=["list"]))
        self.dp.message.register(self.handle_archive, Command(commands=["archive"]))
        self.dp.message.register(self.handle_direct_message)

    async def handle_start(self, message: Message):
        """Handle the /start command"""
        welcome_text = (
            "Welcome to AI Backlog Assistant! 🚀\n\n"
            "I help you manage and prioritize your development tasks. Here are the available commands:\n\n"
            "/add <task> - Add a new task\n"
            "/status <task_id> - Check task status\n"
            "/list - List recent tasks\n"
            "/archive <task_id> - Get task archive details\n"
            "/help - Show this help message\n\n"
            "You can also just send me a task description directly!"
        )
        await message.answer(welcome_text)

    async def handle_help(self, message: Message):
        """Handle the /help command"""
        help_text = (
            "AI Backlog Assistant Help 📚\n\n"
            "Available commands:\n"
            "/add <task> - Add a new task\n"
            "/status <task_id> - Check task status\n"
            "/list - List recent tasks\n"
            "/archive <task_id> - Get task archive details\n"
            "/help - Show this help message\n\n"
            "Examples:\n"
            "/add Implement user authentication\n"
            "/status task_12345\n"
            "Just type: Implement user authentication system"
        )
        await message.answer(help_text)

    async def handle_add(self, message: Message):
        """Handle the /add command"""
        try:
            # Extract task text from the command
            task_text = message.text[len("/add "):].strip()

            if not task_text:
                await message.answer("Please provide a task description after /add")
                return

            # Process the task
            user_id = str(message.from_user.id)
            result = await self.process_telegram_message(task_text, user_id)

            response = (
                f"Task #{result['task_id']} added successfully! ✅\n\n"
                f"Description: {task_text}\n"
                f"Status: {result['status']}\n"
                f"Recommendation: {result['result'].get('recommendation', 'No recommendation yet')}"
            )
            await message.answer(response)

        except Exception as e:
            logger.error(f"Error handling /add command: {e}")
            await message.answer(f"❌ Error processing your request: {str(e)}")

    async def handle_status(self, message: Message):
        """Handle the /status command"""
        try:
            # Extract task ID from the command
            parts = message.text.split()
            if len(parts) < 2:
                await message.answer("Please provide a task ID after /status")
                return

            task_id = parts[1]
            result = await self.get_task_status(task_id)

            if result["status"] == "not_found":
                response = f"Task #{task_id} not found. Please check the ID and try again."
            elif result["status"] == "error":
                response = f"❌ Error getting task status: {result['error']}"
            else:
                response = (
                    f"Task #{task_id} Status 📋\n\n"
                    f"Status: {result['status']}\n"
                    f"Classification: {result['classification']}\n"
                    f"Risk Score: {result['risk_score']}\n"
                    f"Impact Score: {result['impact_score']}\n"
                    f"Recommendation: {result['recommendation']}"
                )

            await message.answer(response)

        except Exception as e:
            logger.error(f"Error handling /status command: {e}")
            await message.answer(f"❌ Error processing your request: {str(e)}")

    async def handle_list(self, message: Message):
        """Handle the /list command"""
        try:
            result = await self.list_tasks()

            if "error" in result and result["error"]:
                response = f"❌ Error listing tasks: {result['error']}"
            elif not result["tasks"]:
                response = "You have no recent tasks."
            else:
                response = "Your Recent Tasks 📝:\n\n"
                for task in result["tasks"]:
                    response += (
                        f"Task #{task['task_id']}: {task['description']}\n"
                        f"Status: {task['status']}\n"
                        f"Recommendation: {task['recommendation']}\n\n"
                    )

            await message.answer(response)

        except Exception as e:
            logger.error(f"Error handling /list command: {e}")
            await message.answer(f"❌ Error processing your request: {str(e)}")

    async def handle_archive(self, message: Message):
        """Handle the /archive command"""
        try:
            # Extract task ID from the command
            parts = message.text.split()
            if len(parts) < 2:
                await message.answer("Please provide a task ID after /archive")
                return

            task_id = parts[1]
            result = await self.get_task_archive(task_id)

            if result["status"] == "not_found":
                response = f"Task #{task_id} not found. Please check the ID and try again."
            elif result["status"] == "error":
                response = f"❌ Error getting task archive: {result['error']}"
            else:
                response = (
                    f"Task #{task_id} Archive 🗄️\n\n"
                    f"Original Input: {result['original_input']}\n\n"
                    f"Classification: {result['classification']}\n\n"
                    f"Analysis Results:\n"
                    f"  - Risk Score: {result['analysis_results']['risk_score']}\n"
                    f"  - Impact Score: {result['analysis_results']['impact_score']}\n"
                    f"  - Confidence Score: {result['analysis_results']['confidence_score']}\n"
                    f"  - Urgency Score: {result['analysis_results']['urgency_score']}\n\n"
                    f"Recommendation: {result['recommendation']}\n\n"
                )

                if result["files"]:
                    response += "Files:\n"
                    for file_url in result["files"]:
                        response += f"  - {file_url}\n"

            await message.answer(response)

        except Exception as e:
            logger.error(f"Error handling /archive command: {e}")
            await message.answer(f"❌ Error processing your request: {str(e)}")

    async def handle_direct_message(self, message: Message):
        """Handle direct messages (non-command messages)"""
        try:
            # Check if it's a command (they all start with /)
            if message.text and message.text.startswith('/'):
                return  # Skip, let other handlers process commands

            # Process as a task
            user_id = str(message.from_user.id)
            result = await self.process_telegram_message(message.text, user_id)

            response = (
                f"Task #{result['task_id']} processed! ✅\n\n"
                f"Description: {message.text}\n"
                f"Status: {result['status']}\n"
                f"Recommendation: {result['result'].get('recommendation', 'No recommendation yet')}"
            )
            await message.answer(response)

        except Exception as e:
            logger.error(f"Error handling direct message: {e}")
            await message.answer(f"❌ Error processing your message: {str(e)}")

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
                    "status": task.status,
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
        logger.info("Starting Telegram bot polling...")
        await self.dp.start_polling(self.bot)

# Create a global instance
telegram_bot = TelegramBot()
