"""Base classes and data models for LLM interactions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


@dataclass
class LLMResponse:
    content: str
    raw_response: Optional[Dict[str, Any]] = None
    parsed_json: Optional[Dict[str, Any]] = None
    duration_seconds: float = 0.0
    usage: TokenUsage = field(default_factory=TokenUsage)
    model: str = ""
    status: str = "SUCCESS"


class BaseLLMClient(ABC):
    """Abstract interface for LLM clients."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        json_mode: bool = False,
        model: Optional[str] = None,
        effort: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> LLMResponse:
        """Generate a response from the LLM model."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the backend model and credentials are functioning."""
        pass
