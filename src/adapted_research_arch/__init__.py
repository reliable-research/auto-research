"""Adapted Research Architecture local-first runtime."""

from .engine import ResearchEngine, verify_run
from .project import Project
from .registry import AgentRegistry
from .workflows import WORKFLOWS, WorkflowSpec

__all__ = [
    "AgentRegistry",
    "Project",
    "ResearchEngine",
    "WORKFLOWS",
    "WorkflowSpec",
    "verify_run",
]

__version__ = "0.1.0"
