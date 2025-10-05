


"""
Test Telegram Bot Integration
"""

from src.bot.telegram_bot import telegram_bot, TelegramBot
from unittest.mock import patch

def test_telegram_bot_process_message():
    """Test that the Telegram bot can process messages correctly"""
    # Create a new bot instance
    bot = TelegramBot()

    # Test processing a message
    result = bot.process_telegram_message("Implement user authentication")

    # Verify the result structure
    assert "task_id" in result
    assert "status" in result
    assert "result" in result
    assert result["status"] == "completed"

def test_telegram_bot_task_status():
    """Test that the Telegram bot can return task status"""
    # Create a new bot instance
    bot = TelegramBot()

    # Test getting task status
    result = bot.get_task_status("123")

    # Verify the result structure
    assert "task_id" in result
    assert "status" in result
    assert "classification" in result
    assert result["status"] == "processed"

def test_telegram_bot_list_tasks():
    """Test that the Telegram bot can list tasks"""
    # Create a new bot instance
    bot = TelegramBot()

    # Test listing tasks
    result = bot.list_tasks()

    # Verify the result structure
    assert "tasks" in result
    assert len(result["tasks"]) > 0
    assert "task_id" in result["tasks"][0]
    assert "description" in result["tasks"][0]

def test_telegram_bot_task_archive():
    """Test that the Telegram bot can return task archive details"""
    # Create a new bot instance
    bot = TelegramBot()

    # Test getting task archive
    result = bot.get_task_archive("123")

    # Verify the result structure
    assert "task_id" in result
    assert "original_input" in result
    assert "analysis_results" in result
    assert "recommendation" in result

def test_telegram_bot_instance():
    """Test that the global telegram_bot instance works"""
    # Test the global instance
    assert telegram_bot is not None

    # Test processing a message through the global instance
    result = telegram_bot.process_telegram_message("Test task")

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

