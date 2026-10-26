"""AutoResearch Codeless (Idea to Paper Codeless Workflow v4 Implementation).

An executable implementation of the 8-stage, 48-card academic research orchestration
system with Builder, Critic, and Controller agents powered by Gemini in agy.
"""

__version__ = "4.0.0"
__author__ = "AutoResearch Codeless Team"

from autoresearch.config import Config
from autoresearch.llm.agy_client import AgyGeminiClient
from autoresearch.llm.credentials import AgyCredentialMapper
from autoresearch.workflow.stages import StageId, STAGES
from autoresearch.workflow.cards import CARDS
from autoresearch.agents.coordinator import WorkflowOrchestrator

__all__ = [
    "Config",
    "AgyGeminiClient",
    "AgyCredentialMapper",
    "StageId",
    "STAGES",
    "CARDS",
    "WorkflowOrchestrator",
]
