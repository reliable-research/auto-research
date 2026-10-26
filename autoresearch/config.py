"""Configuration settings for AutoResearch Codeless."""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

DEFAULT_WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORKFLOW_SPEC_DIR = DEFAULT_WORKSPACE_ROOT / "Idea_to_Paper_Codeless_Workflow_v4"
DEFAULT_OAUTH_TOKEN_PATH = Path(os.path.expanduser("~/.gemini/antigravity-cli/antigravity-oauth-token"))

# Standard Antigravity Models
SUPPORTED_MODELS = [
    "gemini-3.8-flash-high",
    "gemini-3.8-flash-medium",
    "gemini-3.8-flash-low",
    "gemini-3.7-flash-high",
    "gemini-3.7-flash-medium",
    "gemini-3.1-pro-high",
    "gemini-3.1-pro-low",
]

DEFAULT_MODEL = "gemini-3.8-flash-high"
DEFAULT_EFFORT = "high"

# How the pipeline is allowed to obtain empirical numbers.
#   SIMULATED: no instrument is wired up. The Builder MUST NOT assert measured
#              results; it emits [TBD-MEASURE:<id>] placeholders and the integrity
#              audit blocks any concrete result number in S6-S8. Output is a
#              pre-registered protocol + frozen-design manuscript, never findings.
#   MEASURED:  numbers must trace to artifacts that exist on disk; the audit
#              enforces provenance, pre-registration and cross-stage consistency.
EVIDENCE_MODES = ["SIMULATED", "MEASURED"]
DEFAULT_EVIDENCE_MODE = "SIMULATED"

CONTRIBUTION_TYPES = [
    "方法 (Method)",
    "效率 (Efficiency)",
    "实证发现 (Empirical Discovery)",
    "基准/资源 (Benchmark/Resource)",
    "系统 (System)",
    "理论 (Theory)",
    "观点/论证 (Perspective/Argumentation)",
]


@dataclass
class Config:
    """AutoResearch global runtime configuration."""
    model: str = DEFAULT_MODEL
    effort: str = DEFAULT_EFFORT
    agy_binary_path: Optional[str] = None
    oauth_token_path: Path = DEFAULT_OAUTH_TOKEN_PATH
    workflow_spec_dir: Path = DEFAULT_WORKFLOW_SPEC_DIR
    workspace_dir: Path = DEFAULT_WORKSPACE_ROOT / "projects"
    max_refine_rounds: int = 2
    timeout_seconds: int = 300
    verbose: bool = True
    evidence_mode: str = DEFAULT_EVIDENCE_MODE
    # Prior published work to reproduce or position against. Without this the
    # pipeline only ever sees the one-line topic, so a 'reproduction' run
    # reconstructs the paper from model memory rather than from the paper.
    reference_material_path: Optional[Path] = None
    reference_material_chars: int = 40000
    # Characters of the unified draft carried into the Builder prompt. The old
    # 4000 meant that by S8 the Builder saw ~3% of the draft and re-invented the
    # experimental setup at every stage.
    draft_context_chars: int = 24000

    def __post_init__(self):
        if not self.agy_binary_path:
            # Detect agy path from environment or common locations
            custom_path = os.environ.get("AGY_PATH")
            if custom_path and os.path.isfile(custom_path):
                self.agy_binary_path = custom_path
            else:
                user_local = os.path.expanduser("~/.local/bin/agy")
                if os.path.isfile(user_local):
                    self.agy_binary_path = user_local
                else:
                    self.agy_binary_path = "agy"
        
        if self.reference_material_path:
            self.reference_material_path = Path(self.reference_material_path)

        self.evidence_mode = str(self.evidence_mode).upper()
        if self.evidence_mode not in EVIDENCE_MODES:
            raise ValueError(
                f"evidence_mode must be one of {EVIDENCE_MODES}, got {self.evidence_mode!r}"
            )

        self.workspace_dir = Path(self.workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
