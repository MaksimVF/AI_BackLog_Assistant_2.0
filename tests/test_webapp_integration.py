

#!/usr/bin/env python3
"""
Integration test to verify the webapp command works end-to-end
"""

import asyncio
import sys
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram import Bot
from aiogram.types import Message, User, Chat
from src.bot.telegram_bot import TelegramBot

async def test_webapp_integration():
    """Integration test for the webapp command"""
    # Create a mock message
    user = User(id=12345, is_bot=False, first_name="Test")
    chat = Chat(id=12345, type="private")

    # Create a minimal Message object with only required attributes
    message = MagicMock(spec=Message)
    message.from_user = user
    message.text = "/webapp"

    # Create a bot instance
    telegram_bot = TelegramBot()

    # Mock the bot instance
    mock_bot = MagicMock(spec=Bot)
    telegram_bot.bot = mock_bot

    # Mock the message.answer method
    mock_answer = AsyncMock()
    message.answer = mock_answer

    try:
        # Call the webapp handler
        await telegram_bot.handle_webapp(message)

        # Verify that message.answer was called
        mock_answer.assert_awaited()
        print("✅ Webapp integration test passed - message was sent successfully")
        return True
    except Exception as e:
        print(f"❌ Webapp integration test failed: {e}")
        return False

if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_webapp_integration())
    sys.exit(0 if result else 1)

