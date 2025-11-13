
#!/usr/bin/env python3

"""
Simple test for the LLM client
"""

import pytest
from unittest.mock import patch, MagicMock
from src.utils.llm_client import llm_client

def test_llm_client_mock():
    """Test that the LLM client can be mocked and returns expected responses"""
    with patch.object(llm_client, 'generate_text') as mock_text, \
         patch.object(llm_client, 'generate_json') as mock_json:

        # Configure mock responses
        mock_text.return_value = "Mock text response"
        mock_json.return_value = {"key": "value"}

        # Test text generation
        text_response = llm_client.generate_text("Test prompt")
        assert text_response == "Mock text response"
        mock_text.assert_called_once()
        # Check that the first call was with the expected arguments
        assert mock_text.call_args[0][0] == "Test prompt"

        # Test JSON generation
        json_response = llm_client.generate_json("Test prompt")
        assert json_response == {"key": "value"}
        mock_json.assert_called_once()
        # Check that the first call was with the expected arguments
        assert mock_json.call_args[0][0] == "Test prompt"

        print("✅ LLM client mock test passed")

if __name__ == "__main__":
    test_llm_client_mock()
