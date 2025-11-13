

"""
Adaptive LLM Client with semaphore + JSON repair

Features:
- AdaptiveSemaphore: allows limited concurrency and enforces a minimum interval between request starts
- Dynamic adjustment of the interval on 429 responses (increase) and on successes (decrease)
- Exponential backoff with jitter for retries
- Robust JSON extraction by balanced-brace scanning + json_repair fallback
- Safe finally cleanup to avoid semaphore leaks
- Configurable via src.config.Config constants
"""

import logging
import time
import json
import random
import threading
from typing import Optional, Dict, Any
import requests
import json_repair

from src.config import Config

logger = logging.getLogger(__name__)

def now() -> float:
    return time.time()

def extract_json_balance(text: str) -> Optional[str]:
    """
    Extract the first balanced JSON object substring from text by scanning braces.
    Returns the substring (possibly malformed) or None.
    """
    if not text:
        return None
    start = None
    depth = 0
    for idx, ch in enumerate(text):
        if ch == '{':
            if start is None:
                start = idx
            depth += 1
        elif ch == '}' and start is not None:
            depth -= 1
            if depth == 0:
                return text[start: idx + 1]
    return None

class AdaptiveSemaphore:
    """
    Semaphore with:
    - max_concurrent: number of parallel request slots
    - min_interval: minimal seconds between starts of requests (across all threads)
    - dynamic adaptation: increase min_interval on 429, decrease on successes
    Thread-safe.
    """
    def __init__(self, max_concurrent: int = 1, min_interval: float = 2.0,
                 min_interval_limit: float = 0.5, max_interval_limit: float = 30.0):
        self._sema = threading.Semaphore(max_concurrent)
        self._start_lock = threading.Lock()  # protects last_start_time and interval adjustments
        self._last_start_time = 0.0
        self._min_interval = float(min_interval)
        self._min_interval_limit = float(min_interval_limit)
        self._max_interval_limit = float(max_interval_limit)

    def acquire(self):
        # Acquire slot
        self._sema.acquire()
        # Enforce inter-start interval (only one thread adjusts/waits at a time)
        with self._start_lock:
            elapsed = now() - self._last_start_time
            if elapsed < self._min_interval:
                to_wait = self._min_interval - elapsed
                logger.debug("AdaptiveSemaphore waiting %.3fs to respect min_interval %.3fs", to_wait, self._min_interval)
                time.sleep(to_wait)
            self._last_start_time = now()

    def release(self):
        try:
            self._sema.release()
        except ValueError:
            # Just in case
            logger.exception("Semaphore release error")

    def increase_interval(self, factor: float = 1.5, cap: Optional[float] = None):
        with self._start_lock:
            new_val = min(self._max_interval_limit, self._min_interval * factor)
            if cap:
                new_val = min(new_val, cap)
            logger.info("Increasing min_interval from %.3fs -> %.3fs", self._min_interval, new_val)
            self._min_interval = max(self._min_interval_limit, new_val)

    def decrease_interval(self, factor: float = 0.9):
        with self._start_lock:
            new_val = max(self._min_interval_limit, self._min_interval * factor)
            if new_val != self._min_interval:
                logger.debug("Decreasing min_interval from %.3fs -> %.3fs", self._min_interval, new_val)
            self._min_interval = new_val

    @property
    def min_interval(self) -> float:
        with self._start_lock:
            return self._min_interval

class LLMClient:
    def __init__(self):
        logger.info("Initializing LLMClient (adaptive semaphore edition)")

        # Configurable via Config; provide sane defaults if missing
        self.api_key = getattr(Config, "MISTRAL_API_KEY", None)
        self.api_url = getattr(Config, "MISTRAL_API_URL", None)
        self.model = getattr(Config, "MISTRAL_MODEL", None)

        # Semaphore settings
        default_max_concurrent = getattr(Config, "LLM_MAX_CONCURRENT", 1)
        default_min_interval = getattr(Config, "LLM_MIN_INTERVAL", 2.0)
        min_interval_limit = getattr(Config, "LLM_MIN_INTERVAL_LIMIT", 0.5)
        max_interval_limit = getattr(Config, "LLM_MAX_INTERVAL_LIMIT", 60.0)

        self._semaphore = AdaptiveSemaphore(
            max_concurrent=default_max_concurrent,
            min_interval=default_min_interval,
            min_interval_limit=min_interval_limit,
            max_interval_limit=max_interval_limit
        )

        # Backoff & retry settings
        self.max_retries = getattr(Config, "LLM_MAX_RETRIES", 3)
        self.backoff_multiplier = getattr(Config, "LLM_BACKOFF_MULT", 2.0)
        self.backoff_jitter = getattr(Config, "LLM_BACKOFF_JITTER", 0.25)
        self.backoff_max = getattr(Config, "LLM_BACKOFF_MAX", 60.0)

        # Internal RPM soft limiter (optional)
        self.max_requests_per_minute = getattr(Config, "LLM_MAX_RPM", None)
        self._rpm_lock = threading.Lock()
        self._minute_window_start = now()
        self._requests_in_minute = 0

        if not (self.api_key and self.api_url and self.model):
            logger.warning("LLMClient is not fully configured (api_key/url/model). Client will return mock responses.")

    # Helper: build endpoint robustly
    def _build_endpoint(self) -> str:
        if not self.api_url:
            raise RuntimeError("API URL not configured")
        endpoint = self.api_url.rstrip('/')
        if endpoint.endswith('/chat/completions'):
            return endpoint
        if endpoint.endswith('/v1'):
            return endpoint + '/chat/completions'
        if '/v1' in endpoint:
            return endpoint.rstrip('/') + '/chat/completions'
        return endpoint + '/v1/chat/completions'

    # Helper: incremental RPM counter
    def _increment_rpm(self):
        if not self.max_requests_per_minute:
            return
        with self._rpm_lock:
            now_ts = now()
            if now_ts - self._minute_window_start >= 60:
                self._minute_window_start = now_ts
                self._requests_in_minute = 0
            self._requests_in_minute += 1
            if self._requests_in_minute > self.max_requests_per_minute:
                # Very conservative: if exceeded, pause until next minute
                wait = 60 - (now_ts - self._minute_window_start)
                if wait > 0:
                    logger.warning("Local RPM exceeded (%d/%d). Sleeping %.1fs", self._requests_in_minute, self.max_requests_per_minute, wait)
                    time.sleep(wait)
                    self._minute_window_start = now()
                    self._requests_in_minute = 1

    # Build payload
    def _prepare_payload(self, prompt: str, max_tokens: int) -> Dict[str, Any]:
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": getattr(Config, "LLM_TEMPERATURE", 0.7)
        }

    # Backoff calculation
    def _compute_backoff(self, attempt: int, base: Optional[float] = None) -> float:
        if base is None:
            base = 1.0
        # exponential * random jitter
        raw = base * (self.backoff_multiplier ** (attempt - 1))
        jitter = random.uniform(-self.backoff_jitter, self.backoff_jitter) * raw
        val = min(self.backoff_max, max(0.0, raw + jitter))
        return val

    # Main request caller (synchronous)
    def _call_api(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        if not (self.api_key and self.api_url and self.model):
            logger.warning("LLM not configured; returning mock response")
            return {"response": "Mock response - LLM not configured"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        endpoint = self._build_endpoint()
        payload = self._prepare_payload(prompt, max_tokens)

        attempt = 0
        while attempt <= self.max_retries:
            attempt += 1
            # Acquire semaphore slot (this also enforces inter-start delay)
            logger.debug("Acquiring semaphore (attempt %d)", attempt)
            self._semaphore.acquire()
            try:
                # RPM increment and local check
                self._increment_rpm()

                logger.debug("Sending request to %s (attempt %d)", endpoint, attempt)
                try:
                    resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
                except requests.RequestException as e:
                    logger.error("Request exception: %s", e)
                    # network error -> backoff & retry
                    if attempt <= self.max_retries:
                        backoff = self._compute_backoff(attempt)
                        logger.info("Network error, sleeping %.2fs before retry", backoff)
                        time.sleep(backoff)
                        # increase semaphore's interval slightly to reduce pressure
                        self._semaphore.increase_interval(factor=1.2, cap=self._semaphore._max_interval_limit)
                        continue
                    return {"response": "", "error": f"Request failed: {e}"}

                # If 429 -> handle Retry-After and adapt semaphore interval
                if resp.status_code == 429:
                    ra = resp.headers.get("Retry-After")
                    logger.warning("Received 429 from LLM (attempt %d). Server Retry-After: %s", attempt, ra)
                    retry_after = None
                    if ra:
                        try:
                            retry_after = float(ra)
                        except Exception:
                            retry_after = None

                    # If server indicates seconds, use it, otherwise use backoff calculation
                    if retry_after:
                        sleep_for = max(0.5, retry_after)
                    else:
                        sleep_for = self._compute_backoff(attempt)

                    logger.info("Sleeping %.2fs due to 429", sleep_for)
                    time.sleep(sleep_for)

                    # Increase the semaphore's min_interval to be more conservative
                    # Use factor based on attempt to ramp up more when persistent
                    factor = 1.5 + (attempt - 1) * 0.2
                    self._semaphore.increase_interval(factor=factor, cap=self._semaphore._max_interval_limit)
                    # continue retrying
                    continue

                # 404 -> endpoint problem, stop retrying
                if resp.status_code == 404:
                    logger.error("LLM endpoint not found: %s", endpoint)
                    return {"response": "", "error": "API endpoint not found (404)"}

                # Other 5xx -> backoff and retry
                if 500 <= resp.status_code < 600:
                    logger.error("Server error %d from LLM", resp.status_code)
                    if attempt <= self.max_retries:
                        backoff = self._compute_backoff(attempt)
                        logger.info("Server error, sleeping %.2fs before retry", backoff)
                        time.sleep(backoff)
                        self._semaphore.increase_interval(factor=1.3)
                        continue
                    return {"response": "", "error": f"Server error: {resp.status_code}"}

                # At this point resp.status_code is 2xx or other non-retryable
                parsed = self._parse_response(resp)
                # If parse gave error, return it (no point retrying unless network/server issue)
                if "error" in parsed and parsed.get("response", "") == "":
                    logger.warning("Parsing error from LLM response: %s", parsed.get("error"))
                    # If parse error is likely due to truncated response (e.g., no closing brace),
                    # consider a retry once more with increased tokens (but be conservative)
                    # For now, return parse error directly
                    return parsed

                # Successful parse -> gently decrease semaphore interval back toward lower bound
                self._semaphore.decrease_interval(factor=0.95)
                return parsed

            finally:
                # Always release semaphore slot
                try:
                    self._semaphore.release()
                except Exception:
                    logger.exception("Error releasing semaphore in finally")

        # If exhausted attempts
        logger.error("Max retries exceeded for prompt")
        return {"response": "", "error": "Max retries exceeded"}

    # Response parsing
    def _parse_response(self, resp: requests.Response) -> Dict[str, Any]:
        content_type = resp.headers.get("Content-Type", "").lower()
        text = resp.text or ""

        # Detect HTML error pages
        if "text/html" in content_type:
            logger.error("LLM returned HTML content (probably error page). Snippet: %s", text[:400])
            return {"response": "", "error": "HTML returned instead of JSON"}

        # Try json() first
        try:
            result = resp.json()
        except ValueError:
            # Attempt to extract JSON substring
            logger.debug("response.json() failed; trying to extract JSON substring")
            json_sub = extract_json_balance(text)
            if not json_sub:
                # Try to strip markdown code fences and search again
                cleaned = text.replace("```json", "").replace("```", "")
                json_sub = extract_json_balance(cleaned)
                if not json_sub:
                    logger.warning("No JSON substring found in LLM output. Raw snippet: %s", text[:400])
                    return {"response": text, "error": "No JSON detected in response"}

            # Try to parse candidate, then repair
            try:
                result = json.loads(json_sub)
            except json.JSONDecodeError:
                try:
                    # json_repair.loads may accept malformed JSON and return dict
                    result = json_repair.loads(json_sub)
                    logger.info("json_repair succeeded for extracted substring")
                except Exception as repair_exc:
                    logger.error("json_repair failed: %s", repair_exc)
                    logger.debug("Raw response (long): %s", text[:2000])
                    return {"response": text, "error": f"Invalid JSON and repair failed: {repair_exc}"}

        # At this point, result is a parsed JSON-like object or other Python object
        # If response follows chat/completions 'choices' schema, extract 'content'
        if isinstance(result, dict) and "choices" in result and isinstance(result["choices"], list) and len(result["choices"]) > 0:
            first = result["choices"][0]
            # different providers may have message->content or text
            content = None
            if isinstance(first, dict):
                if "message" in first and isinstance(first["message"], dict):
                    content = first["message"].get("content")
                elif "text" in first:
                    content = first.get("text")
            if content is None or content == "":
                logger.warning("Empty 'content' in choices: %s", first)
                return {"response": "", "error": "Empty content in LLM choices"}
            return {"response": content}

        # If result is a dict but not a choice, return JSON as string for generate_json to parse
        if isinstance(result, dict):
            try:
                json_text = json.dumps(result)
                return {"response": json_text}
            except Exception:
                return {"response": str(result)}

        # List or primitive -> return textual representation
        return {"response": str(result)}

    # Public methods
    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Returns text response (may be JSON string if LLM returned JSON)
        """
        # Optionally add strict JSON instruction if you expect JSON
        # But keep generate_text universal.
        parsed = self._call_api(prompt, max_tokens)
        return parsed.get("response", "")

    def generate_json(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        """
        Attempts to return parsed JSON. On parse/repair failure, returns {'error': ..., 'raw': ...}
        """
        # Add strict JSON wrapper to prompt for better model behavior
        strict_prompt = (
            "Respond strictly in JSON format without explanations or markdown."
            "Send nothing but the JSON object."
            f"{prompt}"
        )
        parsed = self._call_api(strict_prompt, max_tokens)

        response_text = parsed.get("response", "")
        if not response_text:
            return {"error": parsed.get("error", "No response from LLM")}

        # Try to robustly extract JSON substring
        json_sub = extract_json_balance(response_text)
        if json_sub:
            try:
                return json.loads(json_sub)
            except json.JSONDecodeError:
                try:
                    return json_repair.loads(json_sub)
                except Exception as repair_exc:
                    logger.error("JSON repair failed in generate_json: %s", repair_exc)
                    return {"error": f"JSON repair failed: {repair_exc}", "raw": response_text}

        # If response_text itself is a JSON string
        try:
            return json.loads(response_text)
        except Exception:
            # Last resort: try json_repair on the whole text
            try:
                return json_repair.loads(response_text)
            except Exception as repair_exc:
                logger.warning("generate_json: No JSON found; returning raw text")
                return {"error": "No JSON found in LLM response", "raw": response_text}

# Module-level instance for easy import
llm_client = LLMClient()

