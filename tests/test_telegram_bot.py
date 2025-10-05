

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

    # Verify that the bot and dispatcher are initialized
    assert bot.bot is not None
    assert bot.dp is not None

    # Verify that handlers are set up
    assert len(bot.dp.message.handlers) > 0

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
    mock_message.from_user.id = 12345
    mock_message.from_user.username = "testuser"
    mock_message.chat.id = 67890
    mock_message.message_id = 111

    # Mock the orchestrator
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator:
        mock_orchestrator.process_workflow.return_value = {
            "level2": {"input_type": "idea"},
            "level4": {"recommendation": "Implement soon"}
        }

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

    # Call the handler
    await bot.handle_status(mock_message)

    # Verify the response
    mock_message.answer.assert_called_once()
    response_text = mock_message.answer.call_args[0][0]
    assert "Task #123 Status" in response_text
    assert "Status: Processed" in response_text

@pytest.mark.asyncio
async def test_telegram_bot_list_command():
    """Test the /list command handler"""
    bot = TelegramBot()

    # Create a mock message
    mock_message = AsyncMock(spec=Message)
    mock_message.text = "/list"
    mock_message.answer = AsyncMock()

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
    mock_message.from_user.id = 12345
    mock_message.from_user.username = "testuser"
    mock_message.chat.id = 67890
    mock_message.message_id = 222

    # Mock the orchestrator
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator:
        mock_orchestrator.process_workflow.return_value = {
            "level2": {"input_type": "idea"},
            "level4": {"recommendation": "Implement soon"}
        }

        # Call the handler
        await bot.handle_direct_message(mock_message)

        # Verify the response
        mock_message.answer.assert_called_once()
        response_text = mock_message.answer.call_args[0][0]
        assert "Task #" in response_text
        assert "processed" in response_text
        assert "Implement user authentication system" in response_text

