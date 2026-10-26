"""Real execution of a declared protocol, producing artifacts that can be audited."""

from autoresearch.execution.runner import (
    ProtocolRunner,
    RunRecord,
    RunSpec,
    environment_fingerprint,
    summarize,
)

__all__ = [
    "ProtocolRunner",
    "RunRecord",
    "RunSpec",
    "environment_fingerprint",
    "summarize",
]
