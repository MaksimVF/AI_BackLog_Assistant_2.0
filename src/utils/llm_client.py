

"""
LLM Client Module

This module provides a unified interface for interacting with Language Models.
"""

import logging
import os
import json
from typing import Dict, Any, Optional
import requests
from ratelimit import limits, sleep_and_retry
from src.config import Config

# Configure logging
logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with Language Models"""

    def __init__(self):
        """Initialize the LLM Client"""
        logger.info("Initializing LLM Client")
        self.api_key = Config.MISTRAL_API_KEY
        self.api_url = Config.MISTRAL_API_URL

        if not self.api_key:
            logger.warning("⚠️ LLM API key not configured - using mock responses")
        else:
            logger.info(f"✅ LLM Client configured with API URL: {self.api_url}")

    @sleep_and_retry
    @limits(calls=1, period=1)  # Limit to 1 call per second
    def _call_mistral_api(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        """
        Call the Mistral API with a prompt

        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum number of tokens to generate

        Returns:
            Response from the LLM
        """
        if not self.api_key:
            logger.warning("LLM API key not set - returning mock response")
            return {"response": "Mock response - LLM not configured", "error": "API key missing"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-small",  # Default model, can be parameterized if needed
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        try:
            # Check if the API URL already contains the full path or just the base
            api_endpoint = self.api_url
            if not api_endpoint.endswith('/chat/completions'):
                # If it's just the base URL, append the chat/completions path
                if api_endpoint.endswith('/v1'):
                    api_endpoint = api_endpoint + '/chat/completions'
                elif not api_endpoint.endswith('/v1'):
                    # Handle case where base URL doesn't end with /v1
                    if '/v1' in api_endpoint:
                        api_endpoint = api_endpoint.rstrip('/') + '/chat/completions'
                    else:
                        # Last resort - append the full path
                        api_endpoint = api_endpoint.rstrip('/') + '/v1/chat/completions'

            response = requests.post(
                api_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )

            # Handle 404 error specifically
            if response.status_code == 404:
                logger.error(f"LLM API endpoint not found: {api_endpoint}")
                logger.error("Please check if the Mistral API URL is correct")
                return {"response": "", "error": "API endpoint not found"}

            response.raise_for_status()

            try:
                result = response.json()
                logger.debug(f"LLM API response: {result}")

                # Extract the response content from the chat/completions format
                if 'choices' in result and len(result['choices']) > 0:
                    # Extract the content from the first choice
                    content = result['choices'][0].get('message', {}).get('content', "")
                    return {"response": content}
                else:
                    logger.warning(f"Unexpected LLM API response format: {result}")
                    return {"response": "", "error": "Unexpected response format"}
            except ValueError as e:
                logger.warning(f"LLM response is not valid JSON: {e}")
                logger.warning(f"Raw response: {response.text}")
                return {"response": "", "error": f"Invalid JSON response: {e}"}

        except requests.exceptions.RequestException as e:
            logger.error(f"LLM API request failed: {e}")
            return {"response": "", "error": str(e)}

    @sleep_and_retry
    @limits(calls=1, period=1)  # Limit to 1 call per second
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text using the LLM

        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum number of tokens to generate

        Returns:
            Generated text
        """
        result = self._call_mistral_api(prompt, max_tokens)
        return result.get("response", "")

    @sleep_and_retry
    @limits(calls=1, period=1)  # Limit to 1 call per second
    def generate_json(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        """
        Generate JSON output using the LLM

        Args:
            prompt: The prompt to send to the LLM
            max_tokens: Maximum number of tokens to generate

        Returns:
            Parsed JSON response
        """
        result = self._call_mistral_api(prompt, max_tokens)
        response_text = result.get("response", "")

        try:
            # Try to parse the response as JSON
            if response_text.startswith("{") and response_text.endswith("}"):
                return json.loads(response_text)
            else:
                logger.warning("LLM response is not valid JSON")
                return {"error": "Invalid JSON format"}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            return {"error": f"JSON parsing error: {e}"}

# Create a global instance for easy access
llm_client = LLMClient()

