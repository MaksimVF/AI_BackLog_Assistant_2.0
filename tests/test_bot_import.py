


"""
Test Telegram Bot Import and Initialization
"""

import pytest
from src.bot.telegram_bot import TelegramBot, telegram_bot

def test_telegram_bot_import():
    """Test that the Telegram bot can be imported correctly"""
    # This test verifies that the bot module can be imported without errors
    assert TelegramBot is not None
    assert telegram_bot is not None

def test_telegram_bot_instance():
    """Test that a TelegramBot instance can be created"""
    bot = TelegramBot()
    assert bot is not None
    assert bot.bot is not None
    assert bot.dp is not None

if __name__ == "__main__":
    # Run the tests
    test_telegram_bot_import()
    test_telegram_bot_instance()
    print("✅ Telegram bot import and initialization tests passed!")
