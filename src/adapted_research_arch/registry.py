from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable

from .events import canonical_json
from .models import Budget, PermissionSet, Risk, ValidationError
from .project import Project, utc_now


class RegistryError(RuntimeError):
    """Raised when an agent package cannot be discovered, trusted, or routed."""


@dataclass(frozen=True)
class AgentManifest:
    schema_version: str
    id: str
    version: str
    name: str
    description: str
    maturity: str
    capabilities: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    adapter: dict[str, Any]
    risk: Risk
    permissions: PermissionSet
    tools: tuple[str, ...]
    evaluators: tuple[str, ...]
    budget: Budget
    allow_implicit: bool

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> AgentManifest:
        required = {
            "schemaVersion",
            "id",
            "version",
            "name",
            "description",
            "maturity",
            "capabilities",
            "inputs",
            "outputs",
            "adapter",
            "risk",
            "permissions",
            "routing",
        }
        missing = required - set(value)
        if missing:
            raise ValidationError(f"agent manifest missing fields: {sorted(missing)}")
        agent_id = str(value["id"])
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:\.[a-z][a-z0-9_-]*)+", agent_id):
            raise ValidationError(f"invalid agent id: {agent_id!r}")
        version = str(value["version"])
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
            raise ValidationError(f"invalid agent version: {version!r}")
        maturity = str(value["maturity"])
        if maturity not in {"experimental", "candidate", "stable", "deprecated"}:
            raise ValidationError(f"invalid maturity: {maturity!r}")
        capabilities = _string_tuple(value["capabilities"])
        if not capabilities or any("." not in item for item in capabilities):
            raise ValidationError("agent requires valid capabilities")
        adapter = value["adapter"]
        if not isinstance(adapter, dict) or adapter.get("type") not in {
            "command",
            "model",
            "remote_tool",
        }:
            raise ValidationError("unsupported agent adapter")
        if adapter["type"] == "command" and not adapter.get("command"):
            raise ValidationError("command adapter requires command")
        if adapter["type"] == "model" and not adapter.get("provider"):
            raise ValidationError("model adapter requires provider")
        if adapter["type"] == "remote_tool" and not (adapter.get("server") and adapter.get("tool")):
            raise ValidationError("remote tool adapter requires server and tool")
        routing = value.get("routing", {})
        return cls(
            schema_version=str(value["schemaVersion"]),
            id=agent_id,
            version=version,
            name=str(value["name"]),
            description=str(value["description"]),
            maturity=maturity,
            capabilities=capabilities,
            inputs=_string_tuple(value["inputs"]),
            outputs=_string_tuple(value["outputs"]),
            adapter=dict(adapter),
            risk=Risk.parse(value["risk"]),
            permissions=PermissionSet.from_dict(value["permissions"]),
            tools=_string_tuple(value.get("tools", [])),
            evaluators=_string_tuple(value.get("evaluators", [])),
            budget=Budget.from_dict(value.get("budgets")),
            allow_implicit=bool(routing.get("allowImplicit", False)),
        )


@dataclass(frozen=True)
class AgentPackage:
    manifest: AgentManifest
    root: Path
    manifest_digest: str
    instruction_digest: str
    package_digest: str
    trust_state: str
    managed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.manifest.id,
            "version": self.manifest.version,
            "name": self.manifest.name,
            "description": self.manifest.description,
            "maturity": self.manifest.maturity,
            "capabilities": list(self.manifest.capabilities),
            "root": str(self.root),
            "manifestDigest": self.manifest_digest,
            "instructionDigest": self.instruction_digest,
            "packageDigest": self.package_digest,
            "trustState": self.trust_state,
            "managed": self.managed,
        }


class AgentRegistry:
    def __init__(self, project: Project, extra_roots: Iterable[Path | str] = ()):
        self.project = project
        self.builtin_root = Path(__file__).parent / "builtin_agents"
        self.roots = (self.builtin_root, project.agents_dir, *(Path(item).resolve() for item in extra_roots))
        self._initialize()

    def _initialize(self) -> None:
        with self.project.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_trust (
                    agent_id TEXT NOT NULL,
                    version TEXT NOT NULL,
                    root TEXT NOT NULL,
                    package_digest TEXT NOT NULL,
                    state TEXT NOT NULL,
                    trusted_at TEXT,
                    PRIMARY KEY(agent_id, version, root)
                )
                """
            )

    def discover(self) -> list[AgentPackage]:
        result: list[AgentPackage] = []
        for root in self.roots:
            if not root.is_dir():
                continue
            managed = root == self.builtin_root
            for manifest_path in sorted(root.glob("*/agent.json")):
                package_root = manifest_path.parent.resolve()
                if not package_root.is_relative_to(root.resolve()):
                    continue
                try:
                    _validate_containment(package_root)
                    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
                    manifest = AgentManifest.from_dict(raw)
                    instructions = package_root / "AGENT.md"
                    if not instructions.is_file():
                        raise ValidationError("agent package requires AGENT.md")
                    manifest_digest = hashlib.sha256(canonical_json(raw)).hexdigest()
                    instruction_digest = hashlib.sha256(instructions.read_bytes()).hexdigest()
                    package_digest = _package_digest(package_root)
                    state = self._trust_state(
                        manifest.id,
                        manifest.version,
                        package_root,
                        package_digest,
                        default="trusted" if managed else "discovered",
                    )
                    result.append(
                        AgentPackage(
                            manifest=manifest,
                            root=package_root,
                            manifest_digest=manifest_digest,
                            instruction_digest=instruction_digest,
                            package_digest=package_digest,
                            trust_state=state,
                            managed=managed,
                        )
                    )
                except (OSError, json.JSONDecodeError, ValidationError) as error:
                    raise RegistryError(f"invalid agent package {package_root}: {error}") from error
        return result

    def list(self) -> list[dict[str, Any]]:
        return [item.to_dict() for item in self.discover()]

    def trust(self, agent_id: str, *, version: str | None = None) -> AgentPackage:
        matches = [
            item
            for item in self.discover()
            if item.manifest.id == agent_id and (version is None or item.manifest.version == version)
        ]
        if len(matches) != 1:
            raise RegistryError(f"agent trust target must resolve uniquely: {agent_id}")
        package = matches[0]
        with self.project.connect() as connection:
            connection.execute(
                """
                INSERT INTO agent_trust(agent_id, version, root, package_digest, state, trusted_at)
                VALUES (?, ?, ?, ?, 'trusted', ?)
                ON CONFLICT(agent_id, version, root) DO UPDATE SET
                    package_digest = excluded.package_digest,
                    state = 'trusted',
                    trusted_at = excluded.trusted_at
                """,
                (
                    package.manifest.id,
                    package.manifest.version,
                    str(package.root),
                    package.package_digest,
                    utc_now(),
                ),
            )
        return AgentPackage(**{**package.__dict__, "trust_state": "trusted"})

    def disable(self, agent_id: str, *, version: str | None = None) -> AgentPackage:
        matches = [
            item
            for item in self.discover()
            if item.manifest.id == agent_id and (version is None or item.manifest.version == version)
        ]
        if len(matches) != 1:
            raise RegistryError(f"agent disable target must resolve uniquely: {agent_id}")
        package = matches[0]
        with self.project.connect() as connection:
            connection.execute(
                """
                INSERT INTO agent_trust(agent_id, version, root, package_digest, state, trusted_at)
                VALUES (?, ?, ?, ?, 'disabled', ?)
                ON CONFLICT(agent_id, version, root) DO UPDATE SET
                    package_digest = excluded.package_digest,
                    state = 'disabled',
                    trusted_at = excluded.trusted_at
                """,
                (
                    package.manifest.id,
                    package.manifest.version,
                    str(package.root),
                    package.package_digest,
                    utc_now(),
                ),
            )
        return AgentPackage(**{**package.__dict__, "trust_state": "disabled"})

    def route(self, capability: str, *, agent_id: str | None = None) -> AgentPackage:
        candidates = [
            item
            for item in self.discover()
            if capability in item.manifest.capabilities
            and item.trust_state == "trusted"
            and item.manifest.maturity != "deprecated"
            and (agent_id is None or item.manifest.id == agent_id)
            and (
                agent_id is not None
                or item.managed
                or (item.manifest.allow_implicit and item.manifest.risk <= Risk.R1)
            )
        ]
        if not candidates:
            requested = f" using {agent_id}" if agent_id else ""
            raise RegistryError(f"no trusted agent for capability {capability!r}{requested}")
        candidates.sort(key=lambda item: _version_order(item.manifest.version), reverse=True)
        candidates.sort(
            key=lambda item: (
                {"stable": 0, "candidate": 1, "experimental": 2}.get(item.manifest.maturity, 3),
                item.manifest.id,
            )
        )
        best = candidates[0]
        conflicts = [
            item
            for item in candidates
            if item.manifest.id == best.manifest.id
            and item.manifest.version == best.manifest.version
            and item.package_digest != best.package_digest
        ]
        if conflicts:
            raise RegistryError(f"conflicting package digests for {best.manifest.id}@{best.manifest.version}")
        return best

    def _trust_state(
        self,
        agent_id: str,
        version: str,
        root: Path,
        digest: str,
        *,
        default: str,
    ) -> str:
        with self.project.connect() as connection:
            row = connection.execute(
                "SELECT package_digest, state FROM agent_trust WHERE agent_id = ? AND version = ? AND root = ?",
                (agent_id, version, str(root)),
            ).fetchone()
        if not row:
            return default
        if row["package_digest"] != digest:
            return "changed"
        return str(row["state"])


def _version_order(version: str) -> tuple[tuple[int, ...], bool, str]:
    """Numeric semver ordering; a release sorts above its own prereleases."""
    release, _, prerelease = version.partition("-")
    return (tuple(int(part) for part in release.split(".")), not prerelease, prerelease)


def _string_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValidationError("manifest field must be a list")
    return tuple(str(item) for item in value)


def _package_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if relative.startswith(("tests/", ".")) or "__pycache__" in path.parts:
            continue
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _validate_containment(root: Path) -> None:
    resolved_root = root.resolve()
    for path in root.rglob("*"):
        if path.is_symlink() and not path.resolve().is_relative_to(resolved_root):
            raise ValidationError(f"agent package symlink escapes root: {path}")
