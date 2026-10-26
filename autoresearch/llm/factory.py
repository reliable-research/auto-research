"""Factory for creating LLM client instances."""

from typing import Optional
from autoresearch.config import Config
from autoresearch.llm.base import BaseLLMClient
from autoresearch.llm.agy_client import AgyGeminiClient


def create_llm_client(config: Optional[Config] = None) -> BaseLLMClient:
    """Create and return the default LLM client (AgyGeminiClient)."""
    cfg = config or Config()
    return AgyGeminiClient(
        model=cfg.model,
        effort=cfg.effort,
        agy_binary=cfg.agy_binary_path,
        token_path=str(cfg.oauth_token_path),
        default_timeout=cfg.timeout_seconds,
    )
