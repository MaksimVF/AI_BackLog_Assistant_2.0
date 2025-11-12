
#!/usr/bin/env python3
"""
Test script to verify connection checker functionality
"""

import asyncio
import os
from src.utils.connection_checker import connection_checker
from src.config import Config

async def test_connections():
    """Test all connections and print results"""
    print("Testing connections...")
    print("=" * 50)

    # Print current configuration
    config = Config()
    print("Current Configuration:")
    print(f"MISTRAL_API_KEY: {'set' if config.MISTRAL_API_KEY and config.MISTRAL_API_KEY != 'your_mistral_key' else 'not set'}")
    print(f"S3_ACCESS_KEY: {'set' if config.S3_ACCESS_KEY and config.S3_ACCESS_KEY != 'your_access_key' else 'not set'}")
    print(f"S3_SECRET_KEY: {'set' if config.S3_SECRET_KEY and config.S3_SECRET_KEY != 'your_secret_key' else 'not set'}")
    print(f"TELEGRAM_TOKEN: {'set' if config.TELEGRAM_TOKEN and config.TELEGRAM_TOKEN != 'AIBLA' else 'not set'}")
    print()

    # Test connections
    results = await connection_checker.check_all_connections()

    print("Connection Test Results:")
    print("=" * 50)

    for service, result in results.items():
        status = "✅ Connected" if result.get("connected") else "❌ Not Connected"
        error = result.get("error", "None")
        print(f"{service.upper():<10}: {status}")
        if error != "None":
            print(f"           Error: {error}")
        print()

if __name__ == "__main__":
    asyncio.run(test_connections())
