"""Gemini client implementation via the local Antigravity (agy) CLI."""

import json
import subprocess
import time
from typing import Optional, Dict, Any

from autoresearch.config import DEFAULT_MODEL, DEFAULT_EFFORT
from autoresearch.llm.base import BaseLLMClient, LLMResponse, TokenUsage
from autoresearch.llm.credentials import AgyCredentialMapper
from autoresearch.utils.json_utils import extract_json


class AgyGeminiClient(BaseLLMClient):
    """Executes Gemini LLM requests via Antigravity CLI (`agy`), utilizing authenticated credentials."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        effort: str = DEFAULT_EFFORT,
        agy_binary: Optional[str] = None,
        token_path: Optional[str] = None,
        default_timeout: int = 300,
    ):
        self.default_model = model
        self.default_effort = effort
        self.default_timeout = default_timeout
        self.credential_mapper = AgyCredentialMapper(
            token_path=token_path,
            agy_binary=agy_binary,
        )
        self.agy_binary = self.credential_mapper.agy_binary
        if not self.agy_binary:
            raise RuntimeError("Antigravity CLI (`agy`) binary not found. Please ensure agy is installed.")

        # Map credentials to environment
        self.credential_mapper.map_to_env()

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        json_mode: bool = False,
        model: Optional[str] = None,
        effort: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> LLMResponse:
        """Execute a prompt against Gemini via agy."""
        active_model = model or self.default_model
        active_effort = effort or self.default_effort
        effective_timeout = timeout or self.default_timeout

        # Construct full prompt
        full_prompt_parts = []
        if system_instruction:
            full_prompt_parts.append(f"System Instructions:\n{system_instruction}\n")
        
        full_prompt_parts.append(prompt)

        if json_mode:
            full_prompt_parts.append(
                "\n\nIMPORTANT: You must respond in strictly valid JSON format. "
                "Ensure all keys and string values use double quotes. "
                "Do not include commentary outside the JSON block."
            )

        combined_prompt = "\n".join(full_prompt_parts)

        cmd = [
            self.agy_binary,
            "-p",
            combined_prompt,
            "--output-format",
            "json",
            "--model",
            active_model,
        ]

        # Only add --effort if the model name does not already specify effort suffix
        model_has_effort = any(active_model.endswith(f"-{eff}") for eff in ["low", "medium", "high"])
        if not model_has_effort and active_effort in ["low", "medium", "high"]:
            cmd.extend(["--effort", active_effort])

        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=effective_timeout,
            )
        except subprocess.TimeoutExpired as e:
            raise TimeoutError(f"LLM request via agy timed out after {effective_timeout}s: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to execute agy command: {e}")

        duration = time.time() - start_time

        if result.returncode != 0:
            err_msg = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"agy command failed (exit code {result.returncode}): {err_msg}")

        # Parse agy JSON wrapper
        try:
            agy_output = json.loads(result.stdout)
            content = agy_output.get("response", "")
            raw_usage = agy_output.get("usage", {})
            usage = TokenUsage(
                input_tokens=raw_usage.get("input_tokens", 0),
                output_tokens=raw_usage.get("output_tokens", 0),
                total_tokens=raw_usage.get("total_tokens", 0),
            )
        except json.JSONDecodeError:
            # Fallback if agy returned plain text
            content = result.stdout
            agy_output = {"raw_stdout": result.stdout}
            usage = TokenUsage()

        parsed_json = None
        if json_mode:
            try:
                parsed_json = extract_json(content)
            except Exception as e:
                # If json extraction fails, attach error to parsed_json for downstream handling
                parsed_json = {"error": str(e), "raw_text": content}

        return LLMResponse(
            content=content,
            raw_response=agy_output,
            parsed_json=parsed_json,
            duration_seconds=duration,
            usage=usage,
            model=active_model,
            status="SUCCESS",
        )

    def health_check(self, timeout: int = 90) -> bool:
        """Run a minimal verification prompt."""
        try:
            resp = self.generate("Reply only with PONG", model="gemini-3.8-flash-low", timeout=timeout)
            return "PONG" in resp.content.upper()
        except Exception:
            return False
