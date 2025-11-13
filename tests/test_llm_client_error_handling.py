

#!/usr/bin/env python3

"""
Test LLM client error handling
"""

import pytest
from unittest.mock import patch
from src.utils.llm_client import llm_client, LLMClient

def test_llm_client_no_api_key():
    """Test that the LLM client handles missing API key gracefully"""
    # Create a client with no API key
    client = LLMClient()
    client.api_key = None

    # Test text generation
    text_response = client.generate_text("Test prompt")
    assert "Mock response" in text_response
    assert "LLM not configured" in text_response

    # Test JSON generation
    json_response = client.generate_json("Test prompt")
    assert "error" in json_response
    assert "No JSON found" in json_response["error"]

    print("✅ LLM client no API key test passed")

def test_llm_client_with_mocked_requests():
    """Test LLM client with mocked requests to simulate various error conditions"""
    with patch('requests.post') as mock_post:
        # Test 404 error
        mock_post.return_value.status_code = 404
        mock_post.return_value.text = "Not Found"
        mock_post.return_value.headers = {"Content-Type": "text/html"}

        response = llm_client.generate_text("Test prompt")
        # The error is returned in the response dict, but generate_text only returns the response string
        # We need to check that the response is empty when there's an error
        assert response == ""

        # Test successful response with invalid JSON
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "Invalid JSON response"
        mock_post.return_value.headers = {"Content-Type": "application/json"}
        # Mock the json() method to raise ValueError
        mock_post.return_value.json.side_effect = ValueError("Invalid JSON")

        response = llm_client.generate_text("Test prompt")
        # When JSON parsing fails, the raw text is returned
        assert response == "Invalid JSON response"

        print("✅ LLM client error handling test passed")

if __name__ == "__main__":
    test_llm_client_no_api_key()
    test_llm_client_with_mocked_requests()

