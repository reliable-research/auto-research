from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import IntEnum
import math
from pathlib import PurePosixPath
import re
from typing import Any, Literal


class ValidationError(ValueError):
    """Raised when a protocol record violates a declared contract."""


class Risk(IntEnum):
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5

    @classmethod
    def parse(cls, value: str | int | Risk) -> Risk:
        if isinstance(value, cls):
            return value
        if isinstance(value, int):
            return cls(value)
        try:
            return cls[str(value).upper()]
        except KeyError as error:
            raise ValidationError(f"invalid risk class: {value!r}") from error


@dataclass(frozen=True)
class PermissionSet:
    read: tuple[str, ...] = ()
    write: tuple[str, ...] = ()
    network_hosts: tuple[str, ...] = ()
    process: bool = False
    scheduler: bool = False
    gpu: bool = False
    external_write: bool = False
    secret_handles: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, value: dict[str, Any] | None) -> PermissionSet:
        value = value or {}
        filesystem = value.get("filesystem", {})
        network = value.get("network", {})
        mode = str(network.get("mode", "disabled"))
        hosts = network.get("hosts", []) if mode != "disabled" else []
        return cls(
            read=_strings(filesystem.get("read", [])),
            write=_strings(filesystem.get("write", [])),
            network_hosts=_strings(hosts),
            process=bool(value.get("process", False)),
            scheduler=bool(value.get("scheduler", False)),
            gpu=bool(value.get("gpu", False)),
            external_write=bool(value.get("externalWrite", False)),
            secret_handles=_strings(value.get("secretHandles", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "filesystem": {"read": list(self.read), "write": list(self.write)},
            "network": {
                "mode": "allowlist" if self.network_hosts else "disabled",
                "hosts": list(self.network_hosts),
            },
            "process": self.process,
            "scheduler": self.scheduler,
            "gpu": self.gpu,
            "externalWrite": self.external_write,
            "secretHandles": list(self.secret_handles),
        }

    def intersect(self, other: PermissionSet) -> PermissionSet:
        return PermissionSet(
            read=_intersection(self.read, other.read),
            write=_intersection(self.write, other.write),
            network_hosts=_intersection(self.network_hosts, other.network_hosts),
            process=self.process and other.process,
            scheduler=self.scheduler and other.scheduler,
            gpu=self.gpu and other.gpu,
            external_write=self.external_write and other.external_write,
            secret_handles=_intersection(self.secret_handles, other.secret_handles),
        )

    def allows(self, requested: PermissionSet) -> bool:
        return (
            set(requested.read) <= set(self.read)
            and set(requested.write) <= set(self.write)
            and set(requested.network_hosts) <= set(self.network_hosts)
            and (not requested.process or self.process)
            and (not requested.scheduler or self.scheduler)
            and (not requested.gpu or self.gpu)
            and (not requested.external_write or self.external_write)
            and set(requested.secret_handles) <= set(self.secret_handles)
        )


@dataclass(frozen=True)
class Budget:
    max_wall_seconds: int = 1800
    max_tool_calls: int = 100
    max_sources: int = 100
    max_cost_usd: float = 0.0

    @classmethod
    def from_dict(cls, value: dict[str, Any] | None) -> Budget:
        value = value or {}
        result = cls(
            max_wall_seconds=int(value.get("maxWallSeconds", 1800)),
            max_tool_calls=int(value.get("maxToolCalls", 100)),
            max_sources=int(value.get("maxSources", 100)),
            max_cost_usd=float(value.get("maxCostUsd", 0.0)),
        )
        if result.max_wall_seconds <= 0:
            raise ValidationError("maxWallSeconds must be positive")
        if result.max_tool_calls < 0 or result.max_sources < 0 or result.max_cost_usd < 0:
            raise ValidationError("budgets cannot be negative")
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "maxWallSeconds": self.max_wall_seconds,
            "maxToolCalls": self.max_tool_calls,
            "maxSources": self.max_sources,
            "maxCostUsd": self.max_cost_usd,
        }


@dataclass(frozen=True)
class EvidenceRef:
    source: str
    locator: str
    kind: Literal["artifact", "external", "numeric"] = "artifact"
    artifact_id: str | None = None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> EvidenceRef:
        if not isinstance(value, dict):
            raise ValidationError("evidence must be an object")
        source = str(value.get("source", "")).strip()
        locator = str(value.get("locator", "")).strip()
        kind = str(value.get("kind", "artifact"))
        if not source or not locator:
            raise ValidationError("evidence requires source and locator")
        if kind not in {"artifact", "external", "numeric"}:
            raise ValidationError(f"unsupported evidence kind: {kind!r}")
        return cls(
            source=source,
            locator=locator,
            kind=kind,  # type: ignore[arg-type]
            artifact_id=(str(value["artifactId"]) if value.get("artifactId") else None),
        )


@dataclass(frozen=True)
class CandidateClaim:
    text: str
    evidence: tuple[EvidenceRef, ...] = ()
    value: float | None = None
    unit: str | None = None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> CandidateClaim:
        if not isinstance(value, dict):
            raise ValidationError("claim must be an object")
        text = str(value.get("text", "")).strip()
        if not text:
            raise ValidationError("claim text cannot be empty")
        raw_evidence = value.get("evidence", [])
        if not isinstance(raw_evidence, list):
            raise ValidationError("claim evidence must be a list")
        raw_number = value.get("value")
        number = None if raw_number is None else float(raw_number)
        if number is not None and not math.isfinite(number):
            raise ValidationError("claim value must be finite")
        return cls(
            text=text,
            evidence=tuple(EvidenceRef.from_dict(item) for item in raw_evidence),
            value=number,
            unit=(str(value["unit"]) if value.get("unit") else None),
        )


@dataclass(frozen=True)
class Observation:
    content: str
    tags: tuple[str, ...] = ()
    confidence: float = 1.0
    data_class: Literal["train", "development", "evaluation", "publication_only"] = "development"

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Observation:
        if not isinstance(value, dict):
            raise ValidationError("observation must be an object")
        content = str(value.get("content", "")).strip()
        if not content:
            raise ValidationError("observation content cannot be empty")
        confidence = float(value.get("confidence", 1.0))
        if not 0 <= confidence <= 1:
            raise ValidationError("observation confidence must be between 0 and 1")
        data_class = str(value.get("dataClass", "development"))
        if data_class not in {"train", "development", "evaluation", "publication_only"}:
            raise ValidationError(f"invalid data class: {data_class!r}")
        return cls(
            content=content,
            tags=_strings(value.get("tags", [])),
            confidence=confidence,
            data_class=data_class,  # type: ignore[arg-type]
        )


AgentStatus = Literal[
    "completed", "blocked", "failed", "inconclusive", "negative", "saturated", "floored"
]


@dataclass
class AgentOutput:
    status: AgentStatus
    summary: str
    records: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, str] = field(default_factory=dict)
    claims: list[CandidateClaim] = field(default_factory=list)
    observations: list[Observation] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)
    usage: dict[str, float] = field(default_factory=dict)
    limitations: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> AgentOutput:
        if not isinstance(value, dict):
            raise ValidationError("agent output must be an object")
        status = str(value.get("status", "completed"))
        if status not in {
            "completed",
            "blocked",
            "failed",
            "inconclusive",
            "negative",
            "saturated",
            "floored",
        }:
            raise ValidationError(f"invalid agent status: {status!r}")
        summary = str(value.get("summary", "")).strip()
        if not summary:
            raise ValidationError("agent output requires a summary")
        records = value.get("records", {})
        artifacts = value.get("artifacts", {})
        metrics = value.get("metrics", {})
        usage = value.get("usage", {})
        if not all(isinstance(item, dict) for item in (records, artifacts, metrics, usage)):
            raise ValidationError("records, artifacts, metrics, and usage must be objects")
        claims = value.get("claims", [])
        observations = value.get("observations", [])
        limitations = value.get("limitations", [])
        if not all(isinstance(item, list) for item in (claims, observations, limitations)):
            raise ValidationError("claims, observations, and limitations must be lists")
        parsed_artifacts: dict[str, str] = {}
        reserved_artifacts = {"request.json", "stdout.json", "stderr.txt", "failure.txt"}
        for raw_name, content in artifacts.items():
            name = str(raw_name)
            path = PurePosixPath(name)
            if not name or path.is_absolute() or ".." in path.parts:
                raise ValidationError(f"artifact name must be safe and relative: {name!r}")
            if name in reserved_artifacts:
                raise ValidationError(f"artifact name is reserved by the runtime: {name!r}")
            parsed_artifacts[name] = str(content)
        parsed_metrics: dict[str, float] = {}
        for name, raw in metrics.items():
            number = float(raw)
            if not math.isfinite(number):
                raise ValidationError(f"metric {name!r} must be finite")
            parsed_metrics[str(name)] = number
        parsed_usage: dict[str, float] = {}
        for name, raw in usage.items():
            number = float(raw)
            if not math.isfinite(number) or number < 0:
                raise ValidationError(f"usage {name!r} must be finite and non-negative")
            parsed_usage[str(name)] = number
        return cls(
            status=status,  # type: ignore[arg-type]
            summary=summary,
            records=records,
            artifacts=parsed_artifacts,
            claims=[CandidateClaim.from_dict(item) for item in claims],
            observations=[Observation.from_dict(item) for item in observations],
            metrics=parsed_metrics,
            usage=parsed_usage,
            limitations=[str(item) for item in limitations],
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StageSpec:
    id: str
    capability: str
    purpose: str
    depends_on: tuple[str, ...] = ()
    risk: Risk = Risk.R1
    outputs: tuple[str, ...] = ()
    gates: tuple[str, ...] = ("schema.valid",)
    optional: bool = False

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", self.id):
            raise ValidationError(f"invalid stage id: {self.id!r}")
        if "." not in self.capability:
            raise ValidationError(f"invalid stage capability: {self.capability!r}")


@dataclass(frozen=True)
class WorkflowSpec:
    id: str
    version: str
    description: str
    stages: tuple[StageSpec, ...]

    def __post_init__(self) -> None:
        seen: set[str] = set()
        for stage in self.stages:
            missing = set(stage.depends_on) - seen
            if missing:
                raise ValidationError(
                    f"stage {stage.id!r} has missing or forward dependencies: {sorted(missing)}"
                )
            if stage.id in seen:
                raise ValidationError(f"duplicate stage id: {stage.id!r}")
            seen.add(stage.id)


def _strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise ValidationError("expected a list of strings")
    return tuple(sorted({str(item).strip() for item in value if str(item).strip()}))


def _intersection(left: tuple[str, ...], right: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(left) & set(right)))
