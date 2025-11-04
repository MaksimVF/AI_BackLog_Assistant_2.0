
"""
Utility for verifying Telegram Web App initData using HMAC-SHA256.

This module provides functions to verify the integrity of data received
from Telegram Web Apps by checking the HMAC-SHA256 signature.
"""

import hmac
import hashlib
import urllib.parse
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

def verify_telegram_init_data(init_data: str, bot_token: str) -> bool:
    """
    Verify the integrity of Telegram Web App initData using HMAC-SHA256.

    Args:
        init_data: The initData string from Telegram Web App
        bot_token: Your Telegram bot token

    Returns:
        bool: True if verification is successful, False otherwise
    """
    try:
        # Extract the hash from initData
        if 'hash=' not in init_data:
            logger.warning("initData does not contain a hash parameter")
            return False

        # Split the initData into parameters
        params = {}
        for pair in init_data.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value

        # Extract the hash
        received_hash = params.pop('hash', None)
        if not received_hash:
            logger.warning("No hash found in initData parameters")
            return False

        # Create the data string for HMAC verification
        data_check_string = '\n'.join(f"{k}={urllib.parse.unquote(v)}" for k, v in sorted(params.items()))

        # Get the secret key from the bot token
        secret_key = hashlib.sha256(bot_token.encode()).digest()

        # Calculate HMAC-SHA256
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        # Compare hashes
        is_valid = hmac.compare_digest(calculated_hash, received_hash)
        if not is_valid:
            logger.warning("HMAC verification failed for initData")
        return is_valid

    except Exception as e:
        logger.error(f"Error verifying initData: {e}")
        return False

def extract_init_data_params(init_data: str) -> Dict[str, str]:
    """
    Extract parameters from Telegram Web App initData.

    Args:
        init_data: The initData string from Telegram Web App

    Returns:
        Dict[str, str]: Dictionary of parameters
    """
    params = {}
    try:
        for pair in init_data.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = urllib.parse.unquote(value)
    except Exception as e:
        logger.error(f"Error extracting initData parameters: {e}")
    return params

def get_user_info_from_init_data(init_data: str) -> Optional[Dict[str, str]]:
    """
    Extract user information from Telegram Web App initData.

    Args:
        init_data: The initData string from Telegram Web App

    Returns:
        Optional[Dict[str, str]]: User information if available, None otherwise
    """
    try:
        params = extract_init_data_params(init_data)
        user_data = params.get('user', '{}')
        if user_data and user_data != '{}':
            # Parse the user JSON string (Telegram provides it URL-encoded)
            import json
            return json.loads(urllib.parse.unquote(user_data))
        return None
    except Exception as e:
        logger.error(f"Error extracting user info from initData: {e}")
        return None
