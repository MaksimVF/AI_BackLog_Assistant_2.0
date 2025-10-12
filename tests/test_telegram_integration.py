


"""
Test Telegram Bot Integration
"""

from src.bot.telegram_bot import telegram_bot, TelegramBot
from unittest.mock import patch, AsyncMock

import pytest

@pytest.mark.asyncio
async def test_telegram_bot_process_message():
    """Test that the Telegram bot can process messages correctly"""
    # Create a new bot instance
    bot = TelegramBot()

    # Test processing a message
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator, \
         patch("src.bot.telegram_bot.TaskRepository.create_task") as mock_create_task:
        mock_orchestrator.process_workflow.return_value = {
            "classification": "feature",
            "risk_score": 2.5,
            "impact_score": 4.0,
            "confidence_score": 0.9,
            "urgency_score": 3.2,
            "recommendation": "Implement soon"
        }
        mock_create_task.return_value = None

        result = await bot.process_telegram_message("Implement user authentication")

        # Verify the result structure
        assert "task_id" in result
        assert "status" in result
        assert "result" in result
        assert result["status"] == "completed"

@pytest.mark.asyncio
async def test_telegram_bot_task_status():
    """Test that the Telegram bot can return task status"""
    # Create a new bot instance
    bot = TelegramBot()

    # Test getting task status
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

        result = await bot.get_task_status("123")

        # Verify the result structure
        assert "task_id" in result
        assert "status" in result
        assert "classification" in result
        assert result["status"] == "processed"

@pytest.mark.asyncio
async def test_telegram_bot_list_tasks():
    """Test that the Telegram bot can list tasks"""
    # Create a new bot instance
    bot = TelegramBot()

    # Test listing tasks
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

        result = await bot.list_tasks()

        # Verify the result structure
        assert "tasks" in result
        assert len(result["tasks"]) > 0
        assert "task_id" in result["tasks"][0]
        assert "description" in result["tasks"][0]

@pytest.mark.asyncio
async def test_telegram_bot_task_archive():
    """Test that the Telegram bot can return task archive details"""
    # Create a new bot instance
    bot = TelegramBot()

    # Test getting task archive
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

        result = await bot.get_task_archive("123")

        # Verify the result structure
        assert "task_id" in result
        assert "original_input" in result
        assert "analysis_results" in result
        assert "recommendation" in result

@pytest.mark.asyncio
async def test_telegram_bot_instance():
    """Test that the global telegram_bot instance works"""
    # Test the global instance
    assert telegram_bot is not None

    # Test processing a message through the global instance
    with patch("src.bot.telegram_bot.main_orchestrator") as mock_orchestrator, \
         patch("src.bot.telegram_bot.TaskRepository.create_task") as mock_create_task:
        mock_orchestrator.process_workflow.return_value = {
            "classification": "feature",
            "risk_score": 2.5,
            "impact_score": 4.0,
            "confidence_score": 0.9,
            "urgency_score": 3.2,
            "recommendation": "Implement soon"
        }
        mock_create_task.return_value = None

        result = await telegram_bot.process_telegram_message("Test task")

        # Verify the result structure
        assert "task_id" in result
        assert "status" in result
        assert "result" in result

if __name__ == "__main__":
    # Run the tests
    test_telegram_bot_process_message()
    test_telegram_bot_task_status()
    test_telegram_bot_list_tasks()
    test_telegram_bot_task_archive()
    test_telegram_bot_instance()
    print("✅ All Telegram bot integration tests passed!")
