

"""
LLM Client Module

This module provides a unified interface for interacting with Language Models.
"""

import logging
import os
import json
from typing import Dict, Any, Optional
import requests
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
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        try:
            response = requests.post(
                f"{self.api_url}/generate",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            logger.debug(f"LLM API response: {result}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"LLM API request failed: {e}")
            return {"response": "", "error": str(e)}

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

