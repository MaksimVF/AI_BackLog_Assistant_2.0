
"""
Telegram Bot Integration for AI Backlog Assistant

This module implements the Telegram bot interface for task submission and status checking.
"""

import logging
from typing import Dict, Any
from src.config import Config
from src.orchestrator.main_orchestrator_langgraph_pure import main_orchestrator_langgraph_pure as main_orchestrator
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository, TaskFileRepository, TriggerRepository
# Duplicate detection is now handled by Level 2 pure agents
from src.back.agents.level1.task_status_manager import task_status_manager
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
        telegram_token = config.telegram_api_key
        if not telegram_token:
            logger.error("Telegram token not configured, using mock mode")
            logger.error("Please set a valid Telegram token in your .env file")
            logger.error("You can get a token by creating a new bot with BotFather in Telegram")
            # In mock mode, we'll still initialize but won't actually connect
            self.bot = None
        elif telegram_token == "AIBLA":
            logger.error("Using mock Telegram token 'AIBLA' - bot will try to connect but may fail")
            logger.error("Please replace 'AIBLA' with your real Telegram bot token in .env file")
            self.bot = Bot(token=telegram_token)
        elif telegram_token.startswith('your_'):
            logger.error(f"Using placeholder token: {telegram_token}")
            logger.error("Please replace this with your real Telegram bot token in .env file")
            self.bot = Bot(token=telegram_token)
        else:
            logger.info(f"Using valid Telegram token: {telegram_token[:5]}...")
            self.bot = Bot(token=telegram_token)

        self.dp = Dispatcher()

        # Register handlers
        self.dp.message.register(self.handle_start, Command(commands=["start"]))
        self.dp.message.register(self.handle_help, Command(commands=["help"]))
        self.dp.message.register(self.handle_add, Command(commands=["add"]))
        self.dp.message.register(self.handle_status, Command(commands=["status"]))
        self.dp.message.register(self.handle_list, Command(commands=["list"]))
        self.dp.message.register(self.handle_archive, Command(commands=["archive"]))
        self.dp.message.register(self.handle_update_status, Command(commands=["update"]))
        self.dp.message.register(self.handle_recommendation, Command(commands=["recommend"]))
        self.dp.message.register(self.handle_webapp, Command(commands=["webapp"]))
        self.dp.message.register(self.handle_direct_message)

        logger.info("Telegram bot handlers registered successfully")

    async def handle_start(self, message: Message):
        """Handle the /start command"""
        logger.info(f"Received /start command from user {message.from_user.id}")
        welcome_text = (
            "🚀 Welcome to AI Backlog Assistant!\n\n"
            "I help you manage and prioritize your development tasks. Here's how to get started:\n\n"
            "📋 Available commands:\n"
            "/add <task> - Add a new task\n"
            "/status <task_id> - Check task status\n"
            "/list - List recent tasks\n"
            "/archive <task_id> - Get task archive details\n"
            "/update <task_id> <status> - Update task status\n"
            "/recommend <task_id> - Get enhanced recommendations\n"
            "/webapp - Open the web interface\n"
            "/help - Show this help message\n\n"
            "💡 Examples:\n"
            "/add Implement user authentication\n"
            "/status task_abc123\n"
            "/update task_abc123 in_progress\n"
            "/recommend task_abc123\n"
            "/webapp - Open the web interface\n"
            "Just type: Implement user authentication system\n\n"
            "🔍 Tips:\n"
            "• Use /list to find task IDs\n"
            "• Use /archive for detailed analysis\n"
            "• Use /recommend for advanced recommendations\n"
            "• Use /webapp for a better user experience\n"
            "• You can send messages directly without /add\n"
            "• Contact support if you need help!\n\n"
            "📝 Need help? Contact our support team!"
        )
        await message.answer(welcome_text)
        logger.info("Sent welcome message to user")

    async def handle_help(self, message: Message):
        """Handle the /help command"""
        logger.info(f"Received /help command from user {message.from_user.id}")
        help_text = (
            "🚀 AI Backlog Assistant Help 📚\n\n"
            "📋 Available commands:\n"
            "/add <task> - Add a new task\n"
            "/status <task_id> - Check task status\n"
            "/list - List recent tasks\n"
            "/archive <task_id> - Get task archive details\n"
            "/update <task_id> <status> - Update task status\n"
            "/recommend <task_id> - Get enhanced recommendations\n"
            "/webapp - Open the web interface\n"
            "/help - Show this help message\n\n"
            "💡 Examples:\n"
            "/add Implement user authentication\n"
            "/status task_abc123\n"
            "/update task_abc123 in_progress\n"
            "/recommend task_abc123\n"
            "/webapp - Open the web interface\n"
            "Just type: Implement user authentication system\n\n"
            "🔍 Tips:\n"
            "• Use /list to find task IDs\n"
            "• Use /archive for detailed analysis\n"
            "• Use /recommend for advanced recommendations\n"
            "• Use /webapp for a better user experience\n"
            "• You can send messages directly without /add\n"
            "• Contact support if you need help!\n\n"
            "📝 Need help? Contact our support team!"
        )
        await message.answer(help_text)
        logger.info("Sent help message to user")

    async def handle_add(self, message: Message):
        """Handle the /add command"""
        try:
            # Extract task text from the command
            task_text = message.text[len("/add "):].strip()

            if not task_text:
                logger.warning(f"User {message.from_user.id} sent /add command without task description")
                await message.answer(
                    "⚠️ Please provide a task description after /add\n\n"
                    "Example: /add Implement user authentication\n"
                    "Tip: You can also just send a message directly without /add"
                )
                return

            logger.info(f"Received /add command from user {message.from_user.id} with task: {task_text[:50]}...")

            # Process the task
            user_id = str(message.from_user.id)
            result = await self.process_telegram_message(task_text, user_id)

            if result.get('status') == 'failed':
                logger.error(f"Failed to process /add command: {result.get('error')}")
                error_msg = result.get('error', 'Unknown error')
                await message.answer(
                    f"❌ Error processing your request: {error_msg}\n\n"
                    "Please try again or contact support if this persists."
                )
                return

            # Check if this is a duplicate
            if result['result'].get('is_duplicate'):
                duplicate_info = result['result'].get('duplicate_analysis', '')
                original_task_id = result['result'].get('original_task_id', 'unknown')

                response = (
                    f"Task #{result['task_id']} processed! ⚠️\n\n"
                    f"⚠️ Duplicate Message Detected: {duplicate_info}\n\n"
                    f"Original Task ID: {original_task_id}\n"
                    f"Description: {task_text}\n"
                    f"Status: {result['status']}\n"
                    f"Recommendation: {result['result'].get('recommendation', 'No recommendation yet')}\n\n"
                    f"📝 Note: This task has been marked as a duplicate. Duplicate attempts are recorded "
                    f"and may influence task prioritization."
                )
            else:
                response = (
                    f"Task #{result['task_id']} added successfully! ✅\n\n"
                    f"Description: {task_text}\n"
                    f"Status: {result['status']}\n"
                    f"Recommendation: {result['result'].get('recommendation', 'No recommendation yet')}\n\n"
                    f"💡 Tip: Use /status {result['task_id']} to check progress"
                )
            await message.answer(response)
            logger.info(f"Successfully added task {result['task_id']} for user {user_id}")

        except Exception as e:
            logger.error(f"Error handling /add command: {e}")
            await message.answer(
                f"❌ Error processing your request: {str(e)}\n\n"
                "Please try again or contact support if this persists."
            )

    async def handle_status(self, message: Message):
        """Handle the /status command"""
        try:
            # Extract task ID from the command
            parts = message.text.split()
            if len(parts) < 2:
                logger.warning(f"User {message.from_user.id} sent /status command without task ID")
                await message.answer(
                    "⚠️ Please provide a task ID after /status\n\n"
                    "Example: /status task_abc123\n"
                    "Tip: You can find task IDs using /list command"
                )
                return

            task_id = parts[1]
            logger.info(f"Received /status command from user {message.from_user.id} for task {task_id}")

            result = await self.get_task_status(task_id)

            if result["status"] == "not_found":
                logger.warning(f"Task {task_id} not found for user {message.from_user.id}")
                response = (
                    f"⚠️ Task #{task_id} not found\n\n"
                    "Please check the task ID and try again.\n"
                    "Tip: Use /list to see your recent tasks"
                )
            elif result["status"] == "error":
                logger.error(f"Error getting status for task {task_id}: {result['error']}")
                response = (
                    f"❌ Error getting task status: {result['error']}\n\n"
                    "Please try again later or contact support if this persists."
                )
            else:
                logger.info(f"Found task {task_id} with status {result['status']}")
                response = (
                    f"Task #{task_id} Status 📋\n\n"
                    f"Status: {result['status']}\n"
                    f"Classification: {result['classification']}\n"
                    f"Risk Score: {result['risk_score']}\n"
                    f"Impact Score: {result['impact_score']}\n"
                    f"Recommendation: {result['recommendation']}\n\n"
                    f"💡 Tip: Use /archive {task_id} for detailed analysis"
                )

            await message.answer(response)
            logger.info(f"Sent status response for task {task_id} to user {message.from_user.id}")

        except Exception as e:
            logger.error(f"Error handling /status command: {e}")
            await message.answer(
                f"❌ Error processing your request: {str(e)}\n\n"
                "Please try again or contact support if this persists."
            )

    async def handle_list(self, message: Message):
        """Handle the /list command"""
        try:
            logger.info(f"Received /list command from user {message.from_user.id}")
            result = await self.list_tasks()

            if "error" in result and result["error"]:
                logger.error(f"Error listing tasks for user {message.from_user.id}: {result['error']}")
                response = (
                    f"❌ Error listing tasks: {result['error']}\n\n"
                    "Please try again later or contact support if this persists."
                )
            elif not result["tasks"]:
                logger.info(f"No recent tasks found for user {message.from_user.id}")
                response = (
                    "📝 You have no recent tasks.\n\n"
                    "💡 Tip: Use /add to create a new task\n"
                    "Example: /add Implement user authentication"
                )
            else:
                logger.info(f"Found {len(result['tasks'])} tasks for user {message.from_user.id}")
                response = "📝 Your Recent Tasks:\n\n"
                for task in result["tasks"]:
                    response += (
                        f"🔹 Task #{task['task_id']}\n"
                        f"   Description: {task['description']}\n"
                        f"   Status: {task['status']}\n"
                        f"   Recommendation: {task['recommendation']}\n\n"
                    )

                response += (
                    "💡 Tips:\n"
                    "• Use /status <task_id> to check details\n"
                    "• Use /archive <task_id> for full analysis\n"
                )

            await message.answer(response)
            logger.info(f"Sent list of tasks to user {message.from_user.id}")

        except Exception as e:
            logger.error(f"Error handling /list command: {e}")
            await message.answer(
                f"❌ Error processing your request: {str(e)}\n\n"
                "Please try again or contact support if this persists."
            )

    async def handle_update_status(self, message: Message):
        """Handle the /update command for updating task status"""
        try:
            # Extract task ID and new status from the command
            parts = message.text.split()
            if len(parts) < 3:
                logger.warning(f"User {message.from_user.id} sent /update command with insufficient parameters")
                await message.answer(
                    "⚠️ Please provide both task ID and new status\n\n"
                    "Example: /update task_abc123 in_progress\n"
                    "Valid statuses: new, in_progress, on_hold, completed, cancelled"
                )
                return

            task_id = parts[1]
            new_status = parts[2].lower()
            user_id = str(message.from_user.id)

            logger.info(f"Received /update command from user {message.from_user.id} for task {task_id} to status {new_status}")

            # Validate status
            valid_statuses = ['new', 'in_progress', 'on_hold', 'completed', 'cancelled']
            if new_status not in valid_statuses:
                logger.warning(f"User {message.from_user.id} provided invalid status: {new_status}")
                await message.answer(
                    "⚠️ Invalid status provided\n\n"
                    f"Valid statuses: {', '.join(valid_statuses)}\n"
                    "Example: /update task_abc123 in_progress"
                )
                return

            # Update task status
            result = await task_status_manager.update_task_status(task_id, new_status, user_id)

            if result["status"] == "failed":
                logger.error(f"Failed to update task status: {result['message']}")
                response = (
                    f"❌ Error updating task status: {result['message']}\n\n"
                    "Please check the task ID and try again."
                )
            else:
                logger.info(f"Successfully updated task {task_id} to status {new_status}")
                response = (
                    f"✅ Task #{task_id} status updated to: {new_status}\n\n"
                    f"📝 Task Details:\n"
                    f"   - Task ID: {result['task'].task_id}\n"
                    f"   - Status: {result['task'].status}\n"
                    f"   - Classification: {result['task'].classification}\n"
                    f"   - Recommendation: {result['task'].recommendation or 'No recommendation'}\n\n"
                    f"💡 Tip: Use /status {task_id} to check current status"
                )

            await message.answer(response)
            logger.info(f"Sent status update response for task {task_id} to user {message.from_user.id}")

        except Exception as e:
            logger.error(f"Error handling /update command: {e}")
            await message.answer(
                f"❌ Error processing your request: {str(e)}\n\n"
                "Please try again or contact support if this persists."
            )

    async def handle_archive(self, message: Message):
        """Handle the /archive command"""
        try:
            # Extract task ID from the command
            parts = message.text.split()
            if len(parts) < 2:
                logger.warning(f"User {message.from_user.id} sent /archive command without task ID")
                await message.answer(
                    "⚠️ Please provide a task ID after /archive\n\n"
                    "Example: /archive task_abc123\n"
                    "Tip: Use /list to find task IDs"
                )
                return

            task_id = parts[1]
            logger.info(f"Received /archive command from user {message.from_user.id} for task {task_id}")

            result = await self.get_task_archive(task_id)

            if result["status"] == "not_found":
                logger.warning(f"Task {task_id} not found for user {message.from_user.id}")
                response = (
                    f"⚠️ Task #{task_id} not found\n\n"
                    "Please check the task ID and try again.\n"
                    "Tip: Use /list to see your recent tasks"
                )
            elif result["status"] == "error":
                logger.error(f"Error getting archive for task {task_id}: {result['error']}")
                response = (
                    f"❌ Error getting task archive: {result['error']}\n\n"
                    "Please try again later or contact support if this persists."
                )
            else:
                logger.info(f"Found archive for task {task_id}")
                response = (
                    f"🗄️ Task #{task_id} Archive\n\n"
                    f"📝 Original Input: {result['original_input']}\n\n"
                    f"🏷️ Classification: {result['classification']}\n\n"
                    f"📊 Analysis Results:\n"
                    f"  • Risk Score: {result['analysis_results']['risk_score']}\n"
                    f"  • Impact Score: {result['analysis_results']['impact_score']}\n"
                    f"  • Confidence Score: {result['analysis_results']['confidence_score']}\n"
                    f"  • Urgency Score: {result['analysis_results']['urgency_score']}\n\n"
                    f"💡 Recommendation: {result['recommendation']}\n\n"
                )

                if result["files"]:
                    response += "📎 Files:\n"
                    for file_url in result["files"]:
                        response += f"  • {file_url}\n"

                response += "\n🔍 Need more help? Contact our support team!"

            await message.answer(response)
            logger.info(f"Sent archive response for task {task_id} to user {message.from_user.id}")

        except Exception as e:
            logger.error(f"Error handling /archive command: {e}")
            await message.answer(
                f"❌ Error processing your request: {str(e)}\n\n"
                "Please try again or contact support if this persists."
            )

    async def handle_recommendation(self, message: Message):
        """Handle the /recommend command to get enhanced recommendations"""
        try:
            # Extract task ID from the command
            parts = message.text.split()
            if len(parts) < 2:
                logger.warning(f"User {message.from_user.id} sent /recommend command without task ID")
                await message.answer(
                    "⚠️ Please provide a task ID after /recommend\n\n"
                    "Example: /recommend task_abc123\n"
                    "Tip: Use /list to find task IDs"
                )
                return

            task_id = parts[1]
            logger.info(f"Received /recommend command from user {message.from_user.id} for task {task_id}")

            # Get task details
            task_result = await self.get_task_status(task_id)

            if task_result["status"] == "not_found":
                logger.warning(f"Task {task_id} not found for user {message.from_user.id}")
                response = (
                    f"⚠️ Task #{task_id} not found\n\n"
                    "Please check the task ID and try again.\n"
                    "Tip: Use /list to see your recent tasks"
                )
            elif task_result["status"] == "error":
                logger.error(f"Error getting task for recommendation {task_id}: {task_result['error']}")
                response = (
                    f"❌ Error getting task: {task_result['error']}\n\n"
                    "Please try again later or contact support if this persists."
                )
            else:
                # Process through workflow to get enhanced recommendations
                logger.info(f"Generating enhanced recommendations for task {task_id}")

                # Create a sample project context
                project_context = {
                    "project_timeline": {
                        "current_sprint_end": "2025-11-15",
                        "next_milestone": "2025-12-01",
                        "project_deadline": "2026-01-31"
                    },
                    "team_workload": {
                        "Backend Team": {
                            "current_tasks": 12,
                            "capacity": 15,
                            "skills": ["Python", "Django", "PostgreSQL"]
                        },
                        "Frontend Team": {
                            "current_tasks": 8,
                            "capacity": 12,
                            "skills": ["React", "JavaScript", "CSS"]
                        },
                        "QA Team": {
                            "current_tasks": 6,
                            "capacity": 10,
                            "skills": ["Testing", "Automation", "QA"]
                        }
                    }
                }

                # Create analysis data from task
                analysis_data = {
                    "overall_score": (task_result.get("risk_score", 0) + task_result.get("impact_score", 0)) / 2,
                    "risk_score": task_result.get("risk_score", 0),
                    "impact_score": task_result.get("impact_score", 0),
                    "urgency": task_result.get("urgency_score", 0),
                    "confidence": task_result.get("confidence_score", 0.5),
                    "recommendation": task_result.get("recommendation", "No recommendation")
                }

                # Get enhanced recommendation

                # Use the pure orchestrator for enhanced recommendation
                enhanced_recommendation = {
                    "recommendation": "Use the web interface for enhanced recommendations",
                    "rationale": "The web interface provides better visualization and interaction",
                    "priority": "Medium",
                    "next_steps": ["Open the web interface with /webapp"]
                }


                # Format response
                response = (
                    f"🔮 Enhanced Recommendation for Task #{task_id}\n\n"
                    f"📝 Task Details:\n"
                    f"  • Description: {task_result.get('description', 'N/A')}\n"
                    f"  • Status: {task_result.get('status', 'N/A')}\n\n"
                    f"📊 Analysis:\n"
                    f"  • Risk Score: {analysis_data['risk_score']}\n"
                    f"  • Impact Score: {analysis_data['impact_score']}\n"
                    f"  • Urgency: {analysis_data['urgency']}\n\n"
                    f"💡 Basic Recommendation:\n"
                    f"  • {enhanced_recommendation['summary']['recommendation']}\n"
                    f"  • Priority: {enhanced_recommendation['summary']['priority']}\n\n"
                )

                # Add risk mitigation if available
                if enhanced_recommendation.get('risk_mitigation'):
                    risk_info = enhanced_recommendation['risk_mitigation']
                    response += "🛡️ Risk Mitigation Strategies:\n"
                    for strategy in risk_info.get('mitigation_strategies', []):
                        response += f"  • {strategy}\n"
                    if risk_info.get('alternative_approaches'):
                        response += "🔄 Alternative Approaches:\n"
                        for approach in risk_info['alternative_approaches']:
                            response += f"  • {approach}\n"

                # Add resource optimization if available
                if enhanced_recommendation.get('resource_optimization'):
                    resource_info = enhanced_recommendation['resource_optimization']
                    response += "\n👥 Resource Optimization:\n"
                    for team, tasks in resource_info.get('team_assignments', {}).items():
                        response += f"  • {team}: {', '.join(tasks)}\n"
                    if resource_info.get('reallocation_suggestions'):
                        response += "🔄 Reallocation Suggestions:\n"
                        for suggestion in resource_info['reallocation_suggestions']:
                            response += f"  • {suggestion}\n"

                # Add contextual recommendation if available
                if enhanced_recommendation.get('contextual_recommendation'):
                    context_info = enhanced_recommendation['contextual_recommendation']
                    response += "\n📅 Contextual Recommendation:\n"
                    response += f"  • Recommendation: {context_info.get('recommendation', 'N/A')}\n"
                    response += f"  • Rationale: {context_info.get('rationale', 'N/A')}\n"
                    response += f"  • Priority: {context_info.get('priority', 'N/A')}\n"
                    if context_info.get('next_steps'):
                        response += "  • Next Steps:\n"
                        for step in context_info['next_steps']:
                            response += f"    - {step}\n"

                response += "\n🔍 Need more help? Contact our support team!"

            await message.answer(response)
            logger.info(f"Sent enhanced recommendation for task {task_id} to user {message.from_user.id}")

        except Exception as e:
            logger.error(f"Error handling /recommend command: {e}")
            await message.answer(
                f"❌ Error processing your request: {str(e)}\n\n"
                "Please try again or contact support if this persists."
            )

    async def handle_webapp(self, message: Message):
        """Handle the /webapp command to launch the web interface"""
        try:
            logger.info(f"Received /webapp command from user {message.from_user.id}")

            # Create a keyboard with the web app button
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

            # Web app URL - in production, this would be your hosted URL
            web_app_url = "https://yourdomain.com/webapp/index.html"

            # Create the web app button
            web_app_button = InlineKeyboardButton(
                text="🌐 Open Web Interface",
                web_app={"url": web_app_url}
            )

            # Create the keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

            # Send message with web app button
            await message.answer(
                "🚀 Open the AI Backlog Assistant Web Interface for a better experience!\n\n"
                "💡 The web interface provides:\n"
                "• Task management with visual interface\n"
                "• Enhanced recommendation views\n"
                "• Better task organization and tracking\n\n"
                "🔍 Tip: Use the web interface for the best experience!",
                reply_markup=keyboard
            )
            logger.info(f"Sent web app link to user {message.from_user.id}")

        except Exception as e:
            logger.error(f"Error handling /webapp command: {e}")
            await message.answer(
                f"❌ Error processing your request: {str(e)}\n\n"
                "Please try again or contact support if this persists."
            )

    async def handle_direct_message(self, message: Message):
        """Handle direct messages (non-command messages)"""
        try:
            # Check if it's a command (they all start with /)
            if message.text and message.text.startswith('/'):
                return  # Skip, let other handlers process commands

            logger.info(f"Received direct message: {message.text[:50]}...")

            # Process as a task
            user_id = str(message.from_user.id)
            result = await self.process_telegram_message(message.text, user_id)

            if result.get('status') == 'failed':
                logger.error(f"Failed to process message: {result.get('error')}")
                await message.answer(
                    f"❌ Error processing your message: {result.get('error')}\n\n"
                    "Please try again or contact support if this persists."
                )
                return

            # Check if this is a duplicate message
            if result['result'].get('is_duplicate'):
                duplicate_info = result['result'].get('duplicate_analysis', '')
                original_task_id = result['result'].get('original_task_id', 'unknown')

                response = (
                    f"Task #{result['task_id']} processed! ⚠️\n\n"
                    f"⚠️ Duplicate Message Detected: {duplicate_info}\n\n"
                    f"Original Task ID: {original_task_id}\n"
                    f"Description: {message.text}\n"
                    f"Status: {result['status']}\n"
                    f"Recommendation: {result['result'].get('recommendation', 'No recommendation yet')}\n\n"
                    f"📝 Note: This task has been marked as a duplicate. Duplicate attempts are recorded "
                    f"and may influence task prioritization.\n\n"
                    f"💡 Tip: Use /status {original_task_id} to check the original task"
                )
            else:
                response = (
                    f"Task #{result['task_id']} processed! ✅\n\n"
                    f"Description: {message.text}\n"
                    f"Status: {result['status']}\n"
                    f"Recommendation: {result['result'].get('recommendation', 'No recommendation yet')}\n\n"
                    f"💡 Tip: Use /status {result['task_id']} to check progress"
                )
            await message.answer(response)
            logger.info(f"Successfully processed task {result['task_id']}")

        except Exception as e:
            logger.error(f"Error handling direct message: {e}")
            await message.answer(
                f"❌ Error processing your message: {str(e)}\n\n"
                "Please try again or contact support if this persists."
            )

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
            logger.info(f"Processing Telegram message from user {user_id}: {message_text[:50]}...")

            # Duplicate detection is now handled by Level 2 pure agents
            # We'll get the duplicate result from the workflow processing

            # Create metadata for the task
            metadata = {
                "source": "telegram",
                "user_id": user_id,
                "username": "telegram_user",
                "chat_id": "telegram_chat"
            }

            # Process through the workflow
            result = await main_orchestrator.process_workflow(message_text, metadata)

            # Generate a unique task ID based on timestamp and message content (optimized)
            import time
            import hashlib
            # Use a faster hash method and reduce operations
            unique_hash = hashlib.md5(f"{message_text[:50]}-{time.time_ns() % 1000000}-{user_id[:10]}".encode()).hexdigest()[:6]
            task_id = f"task_{unique_hash}"
            logger.info(f"Generated task ID: {task_id}")

            # Store in database
            async with AsyncSessionLocal() as db:
                task_data = {
                    "task_id": task_id,
                    "input_data": message_text,
                    "task_metadata": metadata,
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
                logger.info(f"Successfully stored task {task_id} in database")

            # Get duplicate detection result from Level 2
            duplicate_result = result.get("level2", {}).get("duplicate_detection", {})
            result["is_duplicate"] = duplicate_result.get("is_duplicate", False)
            result["duplicate_analysis"] = duplicate_result.get("analysis", "No duplicates found")
            logger.info(f"Duplicate detection result: {duplicate_result}")

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
            logger.info(f"Getting status for task {task_id}")
            async with AsyncSessionLocal() as db:
                task = await TaskRepository.get_task_by_task_id(db, task_id)

                if not task:
                    logger.warning(f"Task {task_id} not found")
                    return {
                        "task_id": task_id,
                        "status": "not_found",
                        "error": "Task not found"
                    }

                logger.info(f"Found task {task_id} with status {task.status}")
                return {
                    "task_id": task.task_id,
                    "status": task.status,
                    "classification": task.classification,
                    "risk_score": task.risk_score,
                    "impact_score": task.impact_score,
                    "recommendation": task.recommendation
                }

        except Exception as e:
            logger.error(f"Error getting task status for task {task_id}: {e}")
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
            logger.info("Listing recent tasks")
            async with AsyncSessionLocal() as db:
                tasks = await TaskRepository.list_tasks(db, limit=10)

                if not tasks:
                    logger.info("No recent tasks found")
                    return {"tasks": []}

                logger.info(f"Found {len(tasks)} recent tasks")
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
            logger.info(f"Getting archive for task {task_id}")
            async with AsyncSessionLocal() as db:
                task = await TaskRepository.get_task_by_task_id(db, task_id)

                if not task:
                    logger.warning(f"Task {task_id} not found")
                    return {
                        "task_id": task_id,
                        "status": "not_found",
                        "error": "Task not found"
                    }

                # Get associated files
                files = await TaskFileRepository.get_files_by_task_id(db, task_id)
                file_urls = [file.file_url for file in files]

                logger.info(f"Found archive for task {task_id} with {len(file_urls)} files")
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
            logger.error(f"Error getting archive for task {task_id}: {e}")
            return {
                "task_id": task_id,
                "status": "error",
                "error": str(e)
            }

    async def start_polling(self):
        """Start polling for Telegram messages"""
        if self.bot is None:
            logger.error("Cannot start polling: Telegram bot is in mock mode")
            logger.error("Please set a valid Telegram token in your .env file")
            logger.error("You can get a token by creating a new bot with BotFather in Telegram")
            return

        logger.info("Starting Telegram bot polling...")
        try:
            logger.info("Attempting to connect to Telegram servers...")
            # For testing purposes, we'll catch the Unauthorized error and continue in mock mode
            try:
                logger.info("Telegram bot polling started successfully")
                await self.dp.start_polling(self.bot)
            except Exception as e:
                if "Unauthorized" in str(e):
                    logger.error("Telegram token is unauthorized - running in mock mode")
                    logger.error("This is expected in test environments")
                    logger.error("To use a real bot, get a token from BotFather in Telegram")
                    # In mock mode, we can still test the functionality
                    logger.info("Telegram bot is ready for testing (mock mode)")
                else:
                    raise
        except Exception as e:
            logger.error(f"Error starting Telegram bot polling: {e}")
            logger.error("Please check your Telegram token and network connection")
            logger.error("If you're using a mock token, replace it with a real token in your .env file")
            logger.error("You can get a real token by creating a new bot with BotFather in Telegram")

    async def start_polling_background(self):
        """Start polling in background mode (non-blocking)"""
        if self.bot is None:
            logger.error("Cannot start polling: Telegram bot is in mock mode")
            logger.error("Please set a valid Telegram token in your .env file")
            logger.error("You can get a token by creating a new bot with BotFather in Telegram")
            return

        logger.info("Starting Telegram bot polling in background mode...")
        try:
            logger.info("Attempting to connect to Telegram servers...")

            # Create a background task for polling
            import asyncio
            asyncio.create_task(self._run_polling())

        except Exception as e:
            logger.error(f"Error starting Telegram bot polling: {e}")
            logger.error("Please check your Telegram token and network connection")
            logger.error("If you're using a mock token, replace it with a real token in your .env file")
            logger.error("You can get a real token by creating a new bot with BotFather in Telegram")

    async def _run_polling(self):
        """Internal method to run polling - called in background task"""
        try:
            # For testing purposes, we'll catch the Unauthorized error and continue in mock mode
            try:
                logger.info("Telegram bot polling task started")
                await self.dp.start_polling(self.bot)
            except Exception as e:
                if "Unauthorized" in str(e):
                    logger.error("Telegram token is unauthorized - running in mock mode")
                    logger.error("This is expected in test environments")
                    logger.error("To use a real bot, get a token from BotFather in Telegram")
                    # In mock mode, we can still test the functionality
                    logger.info("Telegram bot is ready for testing (mock mode)")
                else:
                    logger.error(f"Error in Telegram polling: {e}")
                    raise
        except Exception as e:
            logger.error(f"Fatal error in Telegram polling: {e}")

# Create a global instance
telegram_bot = TelegramBot()

async def main():
    """Main function to start the bot"""
    logger.info("Starting AI Backlog Assistant Telegram Bot...")
    
    # Check if we have a valid token
    if telegram_bot.bot is None:
        logger.error("Bot is in mock mode - cannot start polling")
        logger.info("To use real bot, set TELEGRAM_API_KEY in your .env file")
        return
    
    try:
        # Start polling
        await telegram_bot.start_polling()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
    finally:
        if telegram_bot.bot:
            await telegram_bot.bot.session.close()


async def main_background():
    """Main function to start the bot in background mode"""
    logger.info("Starting AI Backlog Assistant Telegram Bot in background mode...")

    # Check if we have a valid token
    if telegram_bot.bot is None:
        logger.error("Bot is in mock mode - cannot start polling")
        logger.info("To use real bot, set TELEGRAM_API_KEY in your .env file")
        return

    try:
        # Start polling in background
        await telegram_bot.start_polling_background()
    except Exception as e:
        logger.error(f"Failed to start bot in background mode: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
