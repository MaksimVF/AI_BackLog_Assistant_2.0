


"""
Test script to verify the rate limiting logic without making API calls
"""

import time
from unittest.mock import patch
from src.utils.llm_client import LLMClient

def test_rate_limiting_logic():
    """Test the rate limiting logic by mocking the API calls"""
    client = LLMClient()

    # Mock the requests.post method to avoid actual API calls
    with patch('requests.post') as mock_post:
        # Set up the mock to return a successful response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'choices': [{'message': {'content': '{"test": "response"}'}}]
        }
        mock_post.return_value.headers = {'Content-Type': 'application/json'}

        print("Testing rate limiting logic with mocked API calls...")

        # Reset the client's rate limiting
        client._last_request_time = 0
        client._requests_in_minute = 0
        client._minute_window_start = time.time()

        # Make 3 requests and measure the time between them
        start_time = time.time()

        for i in range(3):
            request_start = time.time()
            result = client.generate_text(f"Test {i+1}", max_tokens=10)
            request_end = time.time()

            elapsed = request_end - start_time
            expected_min_time = i * 2  # Should be at least i*2 seconds

            print(f"Request {i+1}: Completed in {elapsed:.2f}s (expected min: {expected_min_time:.2f}s)")

            # Check if the timing is correct
            if elapsed < expected_min_time:
                print(f"  ⚠️  Rate limiting might not be strict enough")
            else:
                print(f"  ✅ Rate limiting working correctly")

        print("Rate limiting test completed successfully!")

if __name__ == "__main__":
    test_rate_limiting_logic()
    print("\n✅ Rate limiting test completed!")


