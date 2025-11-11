

"""
LLM Client Module

This module provides a unified interface for interacting with Language Models.
"""

import logging
import os
import json
import time
import re
from typing import Dict, Any, Optional
import requests
from ratelimit import limits, sleep_and_retry
from src.config import Config
import json_repair
from threading import Lock

# Configure logging
logger = logging.getLogger(__name__)

def extract_json(text: str) -> Optional[str]:
    """Extract valid JSON from text using regex"""
    # This pattern matches JSON objects more carefully
    # Look for { ... } patterns that are likely to be valid JSON
    pattern = r'\{[^{}]*\}'

    # Find all potential JSON objects
    matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        return None

    # Try to find the most complete JSON object
    for candidate in matches:
        try:
            # Try to parse it as JSON to validate
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            # If parsing fails, try the next candidate
            continue

    # If no valid JSON found, return the first match as a fallback
    return matches[0] if matches else None

class LLMClient:
    """Client for interacting with Language Models"""

    def __init__(self):
        """Initialize the LLM Client"""
        logger.info("Initializing LLM Client")
        self.api_key = Config.MISTRAL_API_KEY
        self.api_url = Config.MISTRAL_API_URL

        # Dynamic rate limiting parameters
        self._current_delay = 0.5  # Start with 0.5 second delay
        self._max_delay = 4  # Maximum delay of 4 seconds
        self._failure_count = 0
        self._success_count = 0
        self._rate_limit_lock = Lock()
        self._last_request_time = 0
        self._requests_in_minute = 0
        self._minute_window_start = time.time()
        self._concurrent_requests = 0
        self._max_concurrent_requests = 1  # Limit to 1 concurrent request

        if not self.api_key:
            logger.warning("⚠️ LLM API key not configured - using mock responses")
        else:
            logger.info(f"✅ LLM Client configured with API URL: {self.api_url}")

    def _adjust_rate_limiting(self, success: bool):
        """Adjust rate limiting based on recent success/failure pattern"""
        with self._rate_limit_lock:
            now = time.time()

            # Reset counters if we're in a new minute window
            if now - self._minute_window_start > 60:
                self._requests_in_minute = 0
                self._minute_window_start = now

            # Track request count
            self._requests_in_minute += 1

            # Adjust delay based on success/failure
            if success:
                self._success_count += 1
                self._failure_count = max(0, self._failure_count - 1)

                # If we have consistent success, reduce delay (but not below 0.5s)
                if self._success_count >= 3 and self._current_delay > 0.5:
                    self._current_delay = max(0.5, self._current_delay * 0.75)
                    self._success_count = 0
            else:
                self._failure_count += 1
                self._success_count = 0

                # If we have consistent failures, increase delay (but not above max)
                if self._failure_count >= 2:
                    self._current_delay = min(self._max_delay, self._current_delay * 1.5)
                    self._failure_count = 0

            # Enforce maximum of 5 requests per minute (more conservative)
            if self._requests_in_minute > 5:
                # Calculate time to wait until next minute
                time_since_window_start = now - self._minute_window_start
                wait_time = 60 - time_since_window_start
                if wait_time > 0:
                    logger.warning(f"Rate limit exceeded: 5 requests/minute. Waiting {wait_time:.1f}s")
                    time.sleep(wait_time)
                    # Reset for new minute
                    self._requests_in_minute = 1
                    self._minute_window_start = time.time()

            logger.debug(f"Current rate limit delay: {self._current_delay}s")

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
            "model": Config.MISTRAL_MODEL,  # Use configurable model
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        # Apply strict rate limiting - 1 request every 2 seconds
        with self._rate_limit_lock:
            now = time.time()
            time_since_last_request = now - self._last_request_time

            # Strict 2-second delay between requests
            min_delay = 2.0  # 2 seconds minimum delay
            delay_needed = max(0, min_delay - time_since_last_request)
            if delay_needed > 0:
                logger.debug(f"Rate limiting: waiting {delay_needed:.2f}s to enforce 2-second delay")
                time.sleep(delay_needed)

            # Update last request time
            self._last_request_time = time.time()

            # Enforce maximum of 1 request at a time
            if self._concurrent_requests >= self._max_concurrent_requests:
                logger.warning("Concurrent request limit reached - waiting for slot")
                # Wait until a slot is available
                while self._concurrent_requests >= self._max_concurrent_requests:
                    time.sleep(0.1)  # Check every 100ms

            # Mark this request as active
            self._concurrent_requests += 1

        try:
            # Check if the API URL already contains the full path or just the base
            api_endpoint = self.api_url

            # If it already ends with /chat/completions, use it as-is
            if api_endpoint.endswith('/chat/completions'):
                pass  # Use the URL as-is
            # If it ends with /v1, append /chat/completions
            elif api_endpoint.endswith('/v1'):
                api_endpoint = api_endpoint + '/chat/completions'
            # If it contains /v1 but doesn't end with it, append the full path
            elif '/v1' in api_endpoint:
                api_endpoint = api_endpoint.rstrip('/') + '/chat/completions'
            # If it doesn't contain /v1 at all, append the full path
            else:
                api_endpoint = api_endpoint.rstrip('/') + '/v1/chat/completions'

            response = requests.post(
                api_endpoint,
                headers=headers,
                json=payload,
                timeout=60  # Increased timeout for stability
            )

            # Handle 404 error specifically
            if response.status_code == 404:
                logger.error(f"LLM API endpoint not found: {api_endpoint}")
                logger.error("Please check if the Mistral API URL is correct")
                self._adjust_rate_limiting(False)  # Record failure
                return {"response": "", "error": "API endpoint not found"}

            # Handle 429 rate limit error
            if response.status_code == 429:
                logger.error("LLM API rate limit exceeded (429)")
                retry_after = int(response.headers.get('Retry-After', 60))
                # Increase retry_after by 0.5s to be more conservative
                retry_after = max(0.5, retry_after + 0.5)
                logger.warning(f"Waiting {retry_after}s before retry")
                time.sleep(retry_after)
                self._adjust_rate_limiting(False)  # Record failure
                return {"response": "", "error": f"Rate limit exceeded. Retry after {retry_after}s"}

            response.raise_for_status()

            try:
                # Check if response is actually HTML (like error pages)
                if 'text/html' in response.headers.get('Content-Type', '').lower():
                    logger.warning(f"LLM API returned HTML instead of JSON: {response.text[:200]}...")
                    self._adjust_rate_limiting(False)  # Record failure
                    return {"response": "", "error": "HTML response received instead of JSON"}

                try:
                    result = response.json()
                except ValueError:
                    # Try to repair the JSON if it's malformed
                    logger.warning("Attempting to repair malformed JSON response")
                    try:
                        repaired_json = json_repair.loads(response.text)
                        result = json.loads(repaired_json)
                        logger.info("Successfully repaired JSON response")
                    except Exception as repair_error:
                        logger.error(f"Failed to repair JSON: {repair_error}")
                        logger.warning(f"Raw response: {response.text[:500]}...")
                        self._adjust_rate_limiting(False)  # Record failure
                        return {"response": "", "error": f"Invalid JSON response: {repair_error}"}

                logger.debug(f"LLM API response: {result}")

                # Extract the response content from the chat/completions format
                if 'choices' in result and len(result['choices']) > 0:
                    # Extract the content from the first choice
                    content = result['choices'][0].get('message', {}).get('content', "")
                    if not content:
                        logger.warning(f"Empty content in response: {result}")
                        self._adjust_rate_limiting(False)  # Record failure
                        return {"response": "", "error": "Empty LLM response"}
                    self._adjust_rate_limiting(True)  # Record success
                    with self._rate_limit_lock:
                        self._concurrent_requests -= 1
                    return {"response": content}
                else:
                    logger.warning(f"Unexpected LLM API response format: {result}")
                    self._adjust_rate_limiting(False)  # Record failure
                    with self._rate_limit_lock:
                        self._concurrent_requests -= 1
                    return {"response": "", "error": "Unexpected response format"}
            except ValueError as e:
                logger.warning(f"LLM response is not valid JSON: {e}")
                logger.warning(f"Raw response: {response.text[:500]}...")  # Log first 500 chars to avoid huge logs
                self._adjust_rate_limiting(False)  # Record failure
                with self._rate_limit_lock:
                    self._concurrent_requests -= 1
                return {"response": "", "error": f"Invalid JSON response: {e}"}

        except requests.exceptions.RequestException as e:
            logger.error(f"LLM API request failed: {e}")
            self._adjust_rate_limiting(False)  # Record failure
            with self._rate_limit_lock:
                self._concurrent_requests -= 1
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

        if not response_text:
            return {"error": "No response from LLM"}

        # Extract and repair JSON
        json_str = extract_json(response_text)
        if not json_str:
            logger.warning(f"No valid JSON found in: {response_text[:200]}...")
            return {"error": "No valid JSON structure"}

        try:
            result = json.loads(json_str)
            logger.info("Successfully parsed JSON")
            return result
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON, attempting repair: {e}")
            try:
                repaired = json_repair.loads(json_str)
                return json.loads(repaired)
            except Exception as repair_error:
                logger.error(f"Repair failed: {repair_error}")
                return {"error": f"JSON repair failed: {repair_error}"}

# Create a global instance for easy access
llm_client = LLMClient()

