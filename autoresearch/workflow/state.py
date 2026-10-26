"""Project state and artifact storage models."""

import json
from dataclasses import dataclass, field, asdict, fields
from pathlib import Path
from typing import Dict, List, Optional, Any
from autoresearch.workflow.stages import StageId


@dataclass
class ProjectState:
    """Persistent state of an active research project."""
    project_id: str
    name: str
    topic: str
    contribution_type: str = "方法 (Method)"
    current_stage: StageId = StageId.S1
    current_round: int = 1
    max_rounds: int = 3
    # The evidence mode this project's deliverables were produced under.
    # Recorded so `verify` audits by the same rules that governed the run,
    # instead of guessing and reporting findings the run never had to satisfy.
    evidence_mode: str = "SIMULATED"
    card_statuses: Dict[str, str] = field(default_factory=dict)
    active_issues: List[Dict[str, Any]] = field(default_factory=list)
    resolved_issues: List[Dict[str, Any]] = field(default_factory=list)
    hypotheses: List[Dict[str, Any]] = field(default_factory=list)
    evidences: List[Dict[str, Any]] = field(default_factory=list)
    stage_outputs: Dict[str, str] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    # Facts each stage registered, so later stages can be checked against them
    # rather than only against themselves.
    evidence_ledger: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    # The S5 contract, frozen before any measurement is taken.
    frozen_protocol: Dict[str, Any] = field(default_factory=dict)
    # Deterministic violations from the most recent audit of each stage.
    integrity_findings: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["current_stage"] = self.current_stage.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectState":
        data = data.copy()
        # Tolerate states written before the integrity layer existed.
        known = {f.name for f in fields(cls)}
        data = {k: v for k, v in data.items() if k in known}
        if "current_stage" in data:
            data["current_stage"] = StageId(data["current_stage"])
        return cls(**data)

    def save(self, workspace_path: Path):
        """Save project state to JSON file."""
        state_file = workspace_path / "project_state.json"
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, workspace_path: Path) -> "ProjectState":
        """Load project state from JSON file."""
        state_file = workspace_path / "project_state.json"
        if not state_file.exists():
            raise FileNotFoundError(f"State file not found at {state_file}")
        with open(state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def log_event(self, event_type: str, details: Dict[str, Any]):
        """Append an audit record to history."""
        self.history.append({
            "stage": self.current_stage.value,
            "round": self.current_round,
            "event": event_type,
            "details": details,
        })
