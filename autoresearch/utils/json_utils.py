"""JSON parsing and sanitization utilities for LLM outputs."""

import json
import re
from typing import Any, Dict, Optional


def extract_json(text: str) -> Dict[str, Any]:
    """Extract and parse JSON object from text that may contain markdown code fences
    or surrounding commentary.
    """
    if not text or not text.strip():
        raise ValueError("Empty response string, cannot parse JSON.")

    cleaned = text.strip()

    # 1. Match code fences ```json ... ``` or ``` ... ```
    fence_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    matches = re.findall(fence_pattern, cleaned, re.IGNORECASE)
    if matches:
        for match in matches:
            candidate = match.strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                # Try sanitized version
                sanitized = _sanitize_json_string(candidate)
                try:
                    return json.loads(sanitized)
                except json.JSONDecodeError:
                    continue

    # 2. Try parsing raw text directly
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 3. Locate outer braces { ... }
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = cleaned[first_brace : last_brace + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            sanitized = _sanitize_json_string(candidate)
            try:
                return json.loads(sanitized)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse extracted JSON block: {e}\nCandidate block:\n{candidate[:300]}")

    raise ValueError(f"No JSON object structure found in response:\n{text[:300]}")


def _sanitize_json_string(s: str) -> str:
    """Attempt basic fixes for common LLM JSON syntax issues like trailing commas."""
    # Remove trailing commas before closing braces/brackets
    s = re.sub(r",\s*([\]}])", r"\1", s)
    return s
