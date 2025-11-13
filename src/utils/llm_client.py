

"""
Refactored LLM Client Module

Features:
- Unified adaptive rate limiting with exponential backoff + jitter
- Robust JSON extraction (brace balance) and repair fallback via json_repair
- Thread-safe concurrency counters with proper finally cleanup
- Clear separation of responsibilities for easier testing and maintenance
"""

import logging
import time
import json
import random
from typing import Dict, Any, Optional
import requests
from threading import Lock
import json_repair

from src.config import Config

logger = logging.getLogger(__name__)

def _now() -> float:
    return time.time()

def extract_json_balance(text: str) -> Optional[str]:
    """
    Extract JSON object/string by scanning for the first balanced {...} sequence.
    Returns the JSON substring or None.
    """
    if not text:
        return None
    start_idx = None
    depth = 0
    for i, ch in enumerate(text):
        if ch == '{':
            if start_idx is None:
                start_idx = i
            depth += 1
        elif ch == '}' and start_idx is not None:
            depth -= 1
            if depth == 0:
                candidate = text[start_idx:i + 1]
                # Quick sanity check: try to parse; if invalid, still return candidate for repair attempt
                try:
                    json.loads(candidate)
                    return candidate
                except json.JSONDecodeError:
                    return candidate
    return None

class LLMClient:
    def __init__(self):
        logger.info("Initializing LLMClient")
        self.api_key = Config.MISTRAL_API_KEY
        self.api_url = Config.MISTRAL_API_URL.rstrip('/') if Config.MISTRAL_API_URL else None
        self.model = getattr(Config, "MISTRAL_MODEL", None)

        # Rate limiting / backoff parameters (configurable via Config)
        self.min_delay = getattr(Config, "LLM_MIN_DELAY", 0.5)           # minimal delay between requests (seconds)
        self.max_delay = getattr(Config, "LLM_MAX_DELAY", 8.0)           # maximal backoff delay
        self._current_delay = getattr(Config, "LLM_START_DELAY", 1.0)    # adaptive starting delay
        self.max_requests_per_minute = getattr(Config, "LLM_MAX_RPM", 60) # soft RPM limit
        self.max_concurrent_requests = getattr(Config, "LLM_MAX_CONCURRENT", 2)
        self.max_retries = getattr(Config, "LLM_MAX_RETRIES", 4)
        self.backoff_multiplier = getattr(Config, "LLM_BACKOFF_MULT", 2.0)
        self.jitter = getattr(Config, "LLM_BACKOFF_JITTER", 0.3)

        # Internal counters / locks
        self._rate_lock = Lock()
        self._concurrent_lock = Lock()
        self._concurrent_requests = 0
        self._minute_window_start = _now()
        self._requests_in_minute = 0

        if not self.api_key or not self.api_url or not self.model:
            logger.warning("LLM Client misconfigured: API key / URL / model may be missing - mock responses will be used")

    # ---------------------
    # Helpers: endpoint/payload
    # ---------------------
    def _build_endpoint(self) -> str:
        # Supports passing either full path or base URL
        if not self.api_url:
            raise RuntimeError("API URL not configured")
        endpoint = self.api_url
        if endpoint.endswith("/chat/completions"):
            return endpoint
        if endpoint.endswith("/v1"):
            return endpoint + "/chat/completions"
        if "/v1" in endpoint:
            return endpoint.rstrip('/') + "/chat/completions"
        return endpoint.rstrip('/') + "/v1/chat/completions"

    def _prepare_payload(self, prompt: str, max_tokens: int) -> Dict[str, Any]:
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

    # ---------------------
    # Rate limiting & backoff
    # ---------------------
    def _enter_request_slot(self) -> None:
        """
        Ensure we do not exceed concurrent or per-minute soft limits.
        This function will block briefly if necessary.
        """
        while True:
            with self._rate_lock:
                now = _now()
                # reset minute window if needed
                if now - self._minute_window_start >= 60:
                    self._minute_window_start = now
                    self._requests_in_minute = 0

                if self._requests_in_minute < self.max_requests_per_minute and self._concurrent_requests < self.max_concurrent_requests:
                    # allow
                    self._requests_in_minute += 1
                    with self._concurrent_lock:
                        self._concurrent_requests += 1
                    break
                else:
                    # Wait small time and re-evaluate
                    wait = max(self.min_delay, 0.5)
                    logger.debug("Throttling locally: waiting %.2fs before retrying slot acquisition", wait)
            time.sleep(wait)

        # Enforce minimal delay between calls (adaptive)
        # Sleep outside locks to avoid blocking other threads trying to modify counters
        logger.debug("Enforcing inter-request delay: %.2fs", self._current_delay)
        time.sleep(self._current_delay)

    def _exit_request_slot(self) -> None:
        with self._concurrent_lock:
            self._concurrent_requests = max(0, self._concurrent_requests - 1)

    def _handle_rate_limit(self, retry_after: Optional[float] = None) -> float:
        """
        Update internal delay using exponential backoff + jitter.
        Returns the sleep time applied.
        """
        if retry_after is None:
            base = min(self._current_delay * self.backoff_multiplier, self.max_delay)
        else:
            # If server provided Retry-After, use it but don't exceed max_delay
            base = min(max(retry_after, self._current_delay * 1.0), self.max_delay)

        # jitter
        jitter = random.uniform(-self.jitter, self.jitter) * base
        sleep_time = max(self.min_delay, min(self.max_delay, base + jitter))

        # apply and record
        logger.warning("Applying backoff: sleeping %.2fs (base=%.2f, jitter=%.2f)", sleep_time, base, jitter)
        time.sleep(sleep_time)

        # update adaptive delay conservatively
        with self._rate_lock:
            self._current_delay = min(self.max_delay, max(self.min_delay, sleep_time))
        return sleep_time

    def _record_success(self) -> None:
        # Reduce delay slowly on success
        with self._rate_lock:
            self._current_delay = max(self.min_delay, self._current_delay * 0.85)

    # ---------------------
    # Request & response handling
    # ---------------------
    def _request(self, prompt: str, max_tokens: int) -> Dict[str, Any]:
        """
        Performs the HTTP request with retries and handles HTTP-level errors.
        Returns the parsed response dict {'response': str} or {'error': str, ...}
        """
        if not self.api_key or not self.api_url or not self.model:
            logger.warning("LLM not configured; returning mock response")
            return {"response": "Mock response - LLM not configured", "error": None}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        endpoint = self._build_endpoint()
        payload = self._prepare_payload(prompt, max_tokens)

        attempt = 0
        while attempt <= self.max_retries:
            attempt += 1
            try:
                logger.debug("LLM request attempt %d to %s", attempt, endpoint)
                self._enter_request_slot()
                try:
                    resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
                finally:
                    # We will decrement concurrent_requests in outer finally after processing
                    pass

                # Handle status codes
                if resp.status_code == 429:
                    # Parse Retry-After robustly (seconds or HTTP date)
                    retry_after = None
                    ra = resp.headers.get("Retry-After")
                    if ra:
                        try:
                            retry_after = float(ra)
                        except ValueError:
                            # Could be HTTP-date; fallback to None -> use backoff multiplier
                            retry_after = None
                    logger.warning("Received 429 from LLM (attempt %d). Server Retry-After: %s", attempt, ra)
                    self._handle_rate_limit(retry_after)
                    # continue to retry unless we've exhausted attempts
                    continue

                if resp.status_code == 404:
                    logger.error("LLM endpoint not found: %s", endpoint)
                    return {"response": "", "error": "API endpoint not found (404)"}

                try:
                    resp.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    logger.error("HTTP error from LLM: %s", e)
                    # for 5xx, apply backoff and retry
                    if 500 <= resp.status_code < 600 and attempt <= self.max_retries:
                        self._handle_rate_limit(None)
                        continue
                    return {"response": "", "error": f"HTTP error: {resp.status_code}"}

                # Successful HTTP-level response; parse content
                parsed = self._parse_response(resp)
                if "error" in parsed:
                    # If parse error is transient, consider retrying once
                    logger.warning("Parse error from LLM response: %s", parsed.get("error"))
                    return parsed
                # success
                self._record_success()
                return parsed

            except requests.exceptions.RequestException as e:
                logger.error("Request exception: %s", e)
                # network error -> backoff and retry up to max_retries
                if attempt <= self.max_retries:
                    self._handle_rate_limit(None)
                    continue
                return {"response": "", "error": f"Request failed: {e}"}
            finally:
                # Ensure concurrent counter decremented exactly once per enter
                try:
                    self._exit_request_slot()
                except Exception:
                    logger.exception("Failed to exit request slot cleanly")
        # if exhausted
        return {"response": "", "error": "Max retries exceeded"}

    def _parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Parse JSON response from the LLM. Supports:
        - direct JSON `response.json()`
        - "chat/completions" style: result['choices'][0]['message']['content']
        - HTML detection
        - malformed JSON repair via json_repair
        """
        content_type = response.headers.get("Content-Type", "").lower()
        text = response.text or ""

        if "text/html" in content_type:
            logger.error("LLM returned HTML content; possible error page")
            logger.debug("HTML response snippet: %s", text[:500])
            return {"response": "", "error": "HTML returned instead of JSON"}

        # Try direct json()
        try:
            result = response.json()
        except ValueError:
            # Attempt to extract JSON substring then repair
            logger.debug("Response.json() failed, attempting substring extraction and repair")
            json_sub = extract_json_balance(text)
            if not json_sub:
                logger.warning("No JSON substring found in LLM response")
                return {"response": text, "error": "No JSON detected in response"}
            try:
                result = json.loads(json_sub)
            except json.JSONDecodeError:
                # Try json_repair
                try:
                    result = json_repair.loads(json_sub)
                    logger.info("json_repair succeeded")
                except Exception as repair_exc:
                    logger.error("json_repair failed: %s", repair_exc)
                    logger.debug("Raw response: %s", text[:1000])
                    return {"response": text, "error": f"Invalid JSON and repair failed: {repair_exc}"}

        # Now extract generated content
        # Prefer 'choices' -> 'message' -> 'content' (OpenAI/Mistral chat style)
        if isinstance(result, dict) and "choices" in result and isinstance(result["choices"], list) and len(result["choices"]) > 0:
            first = result["choices"][0]
            # Some providers put content under 'message'->'content' or directly under 'text'
            content = None
            if isinstance(first, dict):
                if "message" in first and isinstance(first["message"], dict):
                    content = first["message"].get("content")
                elif "text" in first:
                    content = first.get("text")
            if content is None:
                logger.warning("No 'content' found in first choice: %s", first)
                return {"response": "", "error": "Empty LLM content in choices"}
            return {"response": content}

        # Fallback: if the whole response is a dict that is the desired JSON, return its stringified form
        if isinstance(result, dict):
            try:
                # If user expects JSON string, return raw JSON text as response (so generate_json can parse)
                return {"response": json.dumps(result)}
            except Exception:
                return {"response": str(result)}

        # If result is plain text or list, return textual representation
        try:
            return {"response": str(result)}
        except Exception as e:
            logger.error("Unable to stringify LLM result: %s", e)
            return {"response": "", "error": "Unable to parse LLM response"}

    # ---------------------
    # Public methods
    # ---------------------
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        parsed = self._request(prompt, max_tokens)
        return parsed.get("response", "")

    def generate_json(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        parsed = self._request(prompt, max_tokens)
        text = parsed.get("response", "")
        if not text:
            return {"error": parsed.get("error", "No response")}

        # Try direct parse
        # If text looks like a JSON string, attempt to parse it
        json_sub = extract_json_balance(text)
        if json_sub:
            try:
                return json.loads(json_sub)
            except json.JSONDecodeError:
                try:
                    return json_repair.loads(json_sub)
                except Exception as repair_exc:
                    logger.error("JSON repair failed: %s", repair_exc)
                    return {"error": f"JSON repair failed: {repair_exc}", "raw": text}
        # If no JSON detected, return original text as error
        return {"error": "No JSON found in LLM response", "raw": text}

# Create a module-level client
llm_client = LLMClient()

