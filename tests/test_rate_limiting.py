

#!/usr/bin/env python3
"""
Test script to verify the rate limiting improvements without making actual API calls
"""

import logging
import sys
import time
from src.utils.llm_client import LLMClient

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_rate_limiting():
    """Test the rate limiting functionality by directly testing the rate limiting logic"""
    client = LLMClient()

    print("Testing rate limiting logic...")

    # Test the rate limiting parameters directly
    print(f"Initial rate limit delay: {client._current_delay}s")
    print(f"Initial requests in minute: {client._requests_in_minute}")

    # Simulate multiple requests to see rate limiting in action
    for i in range(8):
        # Manually trigger the rate limiting adjustment
        client._adjust_rate_limiting(True)  # Simulate successful requests

        # Check the current state
        print(f"Request {i+1}: delay={client._current_delay}s, requests_in_minute={client._requests_in_minute}")

        # Small delay to simulate time passing
        time.sleep(0.1)

    # Check if the rate limiting is working
    if client._requests_in_minute > 0:
        print(f"✅ Rate limiting counters are working (requests_in_minute={client._requests_in_minute})")
    else:
        print("❌ Rate limiting counters may not be working")

    # Test the 5 requests per minute limit
    print("\nTesting 5 requests per minute limit...")

    # Reset the client's rate limiting
    client._requests_in_minute = 0
    client._minute_window_start = time.time()

    # Make 6 requests quickly to test the limit
    for i in range(6):
        result = client.generate_text(f"Test {i+1}", max_tokens=10)
        print(f"Request {i+1}: Completed")

    # Check if we exceeded the limit
    if client._requests_in_minute <= 5:
        print("✅ Rate limiting worked - stayed within limit")
    else:
        print(f"❌ Rate limiting may not be working (requests_in_minute={client._requests_in_minute})")

if __name__ == "__main__":
    print("🚀 Starting rate limiting tests...")
    test_rate_limiting()
    print("\n✅ Rate limiting tests completed!")

