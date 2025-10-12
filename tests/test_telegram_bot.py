

"""
Test Telegram Bot Integration
"""

import pytest
from unittest.mock import AsyncMock, patch
from src.bot.telegram_bot import TelegramBot, telegram_bot
from aiogram.types import Message
from aiogram import Bot

@pytest.mark.asyncio
async def test_telegram_bot_initialization():
    """Test that the Telegram bot initializes correctly"""
    bot = TelegramBot()

    # Verify that the dispatcher is initialized
    assert bot.dp is not None

    # Verify that handlers are set up
    assert len(bot.dp.message.handlers) > 0

    # In mock mode (when token is invalid), bot should be None
    # When a valid token is provided, bot should be initialized
    # This test passes in both cases

@pytest.mark.asyncio
async def test_telegram_bot_start_command():
    """Test the /start command handler"""
    bot = TelegramBot()

    # Create a mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/start"
    mock_message.answer = AsyncMock()

    # Call the handler
    await bot.handle_start(mock_message)

    # Verify the response
    mock_message.answer.assert_called_once()
    response_text = mock_message.answer.call_args[0][0]
    assert "Welcome to AI Backlog Assistant" in response_text
    assert "/add" in response_text
    assert "/status" in response_text

@pytest.mark.asyncio
async def test_telegram_bot_help_command():
    """Test the /help command handler"""
    bot = TelegramBot()

    # Create a mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/help"
    mock_message.answer = AsyncMock()

    # Call the handler
    await bot.handle_help(mock_message)

    # Verify the response
    mock_message.answer.assert_called_once()
    response_text = mock_message.answer.call_args[0][0]
    assert "AI Backlog Assistant Help" in response_text
    assert "/add" in response_text
    assert "/status" in response_text

@pytest.mark.asyncio
async def test_telegram_bot_add_command():
    """Test the /add command handler"""
    bot = TelegramBot()

    # Create a mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/add Implement user authentication"
    mock_message.answer = AsyncMock()

    # Mock the from_user and chat attributes
    mock_from_user = AsyncMock()
    mock_from_user.id = 12345
    mock_from_user.username = "testuser"
    mock_message.from_user = mock_from_user

    mock_chat = AsyncMock()
    mock_chat.id = 67890
    mock_message.chat = mock_chat

    mock_message.message_id = 111

    # Mock the orchestrator and database
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator, \
         patch("src.bot.telegram_bot.TaskRepository.create_task") as mock_create_task:
        mock_orchestrator.process_workflow.return_value = {
            "level2": {"input_type": "idea"},
            "level4": {"recommendation": "Implement soon"}
        }
        mock_create_task.return_value = None

        # Call the handler
        await bot.handle_add(mock_message)

        # Verify the response
        mock_message.answer.assert_called_once()
        response_text = mock_message.answer.call_args[0][0]
        assert "Task #" in response_text
        assert "added successfully" in response_text
        assert "Implement user authentication" in response_text

@pytest.mark.asyncio
async def test_telegram_bot_status_command():
    """Test the /status command handler"""
    bot = TelegramBot()

    # Create a mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/status 123"
    mock_message.answer = AsyncMock()

    # Mock the database
    with patch("src.bot.telegram_bot.TaskRepository.get_task_by_task_id") as mock_get_task:
        # Create a mock task
        mock_task = AsyncMock()
        mock_task.task_id = "123"
        mock_task.status = "processed"
        mock_task.classification = "feature"
        mock_task.risk_score = 2.5
        mock_task.impact_score = 4.0
        mock_task.recommendation = "Implement soon"

        mock_get_task.return_value = mock_task

        # Call the handler
        await bot.handle_status(mock_message)

        # Verify the response
        mock_message.answer.assert_called_once()
        response_text = mock_message.answer.call_args[0][0]
        assert "Task #123 Status" in response_text
        assert "Status: processed" in response_text

@pytest.mark.asyncio
async def test_telegram_bot_list_command():
    """Test the /list command handler"""
    bot = TelegramBot()

    # Create a mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/list"
    mock_message.answer = AsyncMock()

    # Mock the database
    with patch("src.bot.telegram_bot.TaskRepository.list_tasks") as mock_list_tasks:
        # Create mock tasks
        mock_task1 = AsyncMock()
        mock_task1.task_id = "123"
        mock_task1.input_data = "Implement user authentication"
        mock_task1.status = "processed"
        mock_task1.recommendation = "Implement soon"

        mock_task2 = AsyncMock()
        mock_task2.task_id = "124"
        mock_task2.input_data = "Fix login bug"
        mock_task2.status = "processed"
        mock_task2.recommendation = "Fix immediately"

        mock_list_tasks.return_value = [mock_task1, mock_task2]

        # Call the handler
        await bot.handle_list(mock_message)

        # Verify the response
        mock_message.answer.assert_called_once()
        response_text = mock_message.answer.call_args[0][0]
        assert "Your Recent Tasks" in response_text
        assert "Task #123" in response_text
        assert "Task #124" in response_text

@pytest.mark.asyncio
async def test_telegram_bot_archive_command():
    """Test the /archive command handler"""
    bot = TelegramBot()

    # Create a mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/archive 123"
    mock_message.answer = AsyncMock()

    # Mock the database
    with patch("src.bot.telegram_bot.TaskRepository.get_task_by_task_id") as mock_get_task, \
         patch("src.bot.telegram_bot.TaskFileRepository.get_files_by_task_id") as mock_get_files:

        # Create a mock task
        mock_task = AsyncMock()
        mock_task.task_id = "123"
        mock_task.input_data = "Implement user authentication"
        mock_task.classification = "feature"
        mock_task.risk_score = 2.5
        mock_task.impact_score = 4.0
        mock_task.confidence_score = 0.9
        mock_task.urgency_score = 3.2
        mock_task.recommendation = "Implement soon"
        mock_task.status = "processed"

        mock_get_task.return_value = mock_task
        mock_get_files.return_value = []

        # Call the handler
        await bot.handle_archive(mock_message)

        # Verify the response
        mock_message.answer.assert_called_once()
        response_text = mock_message.answer.call_args[0][0]
        assert "Task #123 Archive" in response_text
        assert "Original Input:" in response_text
        assert "Recommendation:" in response_text

@pytest.mark.asyncio
async def test_telegram_bot_direct_message():
    """Test handling direct messages"""
    bot = TelegramBot()

    # Create a mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "Implement user authentication system"
    mock_message.answer = AsyncMock()

    # Mock the from_user and chat attributes
    mock_from_user = AsyncMock()
    mock_from_user.id = 12345
    mock_from_user.username = "testuser"
    mock_message.from_user = mock_from_user

    mock_chat = AsyncMock()
    mock_chat.id = 67890
    mock_message.chat = mock_chat

    mock_message.message_id = 222

    # Mock the orchestrator and database
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator, \
         patch("src.bot.telegram_bot.TaskRepository.create_task") as mock_create_task:
        mock_orchestrator.process_workflow.return_value = {
            "level2": {"input_type": "idea"},
            "level4": {"recommendation": "Implement soon"}
        }
        mock_create_task.return_value = None

        # Call the handler
        await bot.handle_direct_message(mock_message)

        # Verify the response
        mock_message.answer.assert_called_once()
        response_text = mock_message.answer.call_args[0][0]
        assert "Task #" in response_text
        assert "processed" in response_text
        assert "Implement user authentication system" in response_text
