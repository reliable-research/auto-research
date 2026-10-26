from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any


class ComparisonError(RuntimeError):
    """Raised when optimization results are not comparable."""


@dataclass(frozen=True)
class MetricContract:
    metric: str
    direction: str
    dataset_digest: str
    seed: int
    wall_seconds: int

    def __post_init__(self) -> None:
        if self.direction not in {"minimize", "maximize"}:
            raise ComparisonError("direction must be minimize or maximize")
        if self.wall_seconds <= 0:
            raise ComparisonError("wall_seconds must be positive")

    @property
    def digest(self) -> str:
        payload = json.dumps(self.__dict__, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()


@dataclass(frozen=True)
class StrategyResult:
    name: str
    family: str
    value: float
    contract_digest: str
    artifact_id: str


def compare_strategies(
    *,
    contract: MetricContract,
    baseline: StrategyResult,
    candidate: StrategyResult,
) -> dict[str, Any]:
    """Require a matched simple control before an advanced strategy can win."""
    if baseline.family != "simple_control":
        raise ComparisonError("baseline must be a simple_control")
    if baseline.contract_digest != contract.digest or candidate.contract_digest != contract.digest:
        raise ComparisonError("strategies were not evaluated under the same contract")
    if not baseline.artifact_id or not candidate.artifact_id:
        raise ComparisonError("both strategies require result artifacts")
    improved = (
        candidate.value > baseline.value
        if contract.direction == "maximize"
        else candidate.value < baseline.value
    )
    return {
        "promote": improved,
        "winner": candidate.name if improved else baseline.name,
        "baseline": baseline.value,
        "candidate": candidate.value,
        "delta": candidate.value - baseline.value,
        "contractDigest": contract.digest,
        "reason": "matched contract improvement" if improved else "advanced strategy did not beat control",
    }
