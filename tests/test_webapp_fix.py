
#!/usr/bin/env python3
"""
Test script to verify the webapp command fix
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def test_keyboard_creation():
    """Test that the keyboard creation doesn't throw validation errors"""
    try:
        # Create the web app button
        web_app_button = InlineKeyboardButton(
            text="🌐 Open Web Interface",
            web_app={"url": "https://yourdomain.com/webapp/index.html"}
        )

        # Create the keyboard with the correct format
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

        print("✅ Keyboard creation test passed - no validation errors")
        return True
    except Exception as e:
        print(f"❌ Keyboard creation test failed: {e}")
        return False

if __name__ == "__main__":
    # Run the test
    test_keyboard_creation()
