from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import time
from typing import Any, Protocol, Sequence

from .models import AgentOutput, Budget, PermissionSet
from .registry import AgentPackage


class AgentError(RuntimeError):
    """Raised when an agent adapter cannot return a valid result."""


@dataclass(frozen=True)
class ExecutionResult:
    output: AgentOutput
    stdout: str
    stderr: str
    duration_seconds: float


class AgentAdapter(Protocol):
    def execute(
        self,
        request: dict[str, Any],
        *,
        workspace: Path,
        permissions: PermissionSet,
        budget: Budget,
    ) -> ExecutionResult: ...


class CommandAgent:
    def __init__(self, package: AgentPackage):
        command = package.manifest.adapter.get("command")
        if not isinstance(command, list) or not command:
            raise AgentError("command agent requires a command list")
        self.package = package
        self.command = tuple(_resolve_command(command, package.root))

    def execute(
        self,
        request: dict[str, Any],
        *,
        workspace: Path,
        permissions: PermissionSet,
        budget: Budget,
    ) -> ExecutionResult:
        if not permissions.process:
            raise AgentError("process permission is required for command agents")
        environment = {
            "PATH": os.environ.get("PATH", ""),
            "LANG": os.environ.get("LANG", "C.UTF-8"),
            "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
            "ARA_PROJECT_ID": str(request.get("projectId", "")),
            "ARA_RUN_ID": str(request.get("runId", "")),
            "ARA_STAGE_ID": str(request.get("stage", {}).get("id", "")),
            "ARA_ATTEMPT_ID": str(request.get("attemptId", "")),
            "ARA_ALLOWED_NETWORK_HOSTS": json.dumps(permissions.network_hosts),
        }
        command, sandbox_backend = _sandbox_command(self.command, workspace, permissions)
        environment["ARA_SANDBOX_BACKEND"] = sandbox_backend
        started = time.monotonic()
        try:
            process = subprocess.run(
                command,
                cwd=workspace,
                input=json.dumps(request, ensure_ascii=False),
                text=True,
                capture_output=True,
                timeout=budget.max_wall_seconds,
                env=environment,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            raise AgentError(f"agent exceeded {budget.max_wall_seconds}s wall budget") from error
        duration = time.monotonic() - started
        if process.returncode != 0:
            detail = process.stderr.strip() or process.stdout.strip()
            raise AgentError(f"agent exited {process.returncode}: {detail[-1000:]}")
        try:
            raw = json.loads(process.stdout)
            output = AgentOutput.from_dict(raw)
        except (AttributeError, TypeError, ValueError) as error:
            raise AgentError(f"invalid agent output: {error}") from error
        return ExecutionResult(output, process.stdout, process.stderr, duration)


class ModelAgent(CommandAgent):
    """Provider-neutral model adapter implemented by a configured command bridge."""

    def __init__(self, package: AgentPackage):
        command = package.manifest.adapter.get("command")
        if not command:
            command = shlex.split(os.environ.get("ARA_MODEL_BRIDGE", ""))
        if not isinstance(command, list) or not command:
            raise AgentError(
                "model agent requires adapter.command or the ARA_MODEL_BRIDGE command"
            )
        self.package = package
        self.command = tuple(_resolve_command(command, package.root))


class RemoteToolAgent(CommandAgent):
    """Remote-tool adapter delegated to an explicitly configured local bridge."""

    def __init__(self, package: AgentPackage):
        command = package.manifest.adapter.get("command")
        if not command:
            command = shlex.split(os.environ.get("ARA_REMOTE_TOOL_BRIDGE", ""))
        if not isinstance(command, list) or not command:
            raise AgentError(
                "remote tool agent requires adapter.command or the ARA_REMOTE_TOOL_BRIDGE command"
            )
        self.package = package
        self.command = tuple(_resolve_command(command, package.root))


def prepare_attempt_workspace(source: Path, target: Path) -> dict[str, str]:
    if target.exists():
        raise AgentError(f"attempt workspace already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target, symlinks=True)
    else:
        target.mkdir()
    return snapshot_tree(source)


def snapshot_tree(root: Path) -> dict[str, str]:
    if not root.is_dir():
        return {}
    result: dict[str, str] = {}
    import hashlib

    for path in sorted(item for item in root.rglob("*") if item.is_file() and not item.is_symlink()):
        result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def source_unchanged(root: Path, before: dict[str, str]) -> bool:
    return snapshot_tree(root) == before


def _resolve_command(command: Sequence[Any], root: Path) -> list[str]:
    result: list[str] = []
    for index, raw in enumerate(command):
        item = str(raw)
        if item == "{runtime_stub}":
            result.append(str(Path(__file__).parent / "builtin_agents" / "runtime_stub.py"))
            continue
        candidate = (root / item).resolve()
        if index > 0 and not Path(item).is_absolute() and candidate.is_file() and candidate.is_relative_to(root):
            result.append(str(candidate))
        else:
            result.append(item)
    return result


def _sandbox_command(
    command: Sequence[str], workspace: Path, permissions: PermissionSet
) -> tuple[list[str], str]:
    """Probe the sandbox before running an agent; fail closed when required."""
    mode = os.environ.get("ARA_OS_SANDBOX", "auto").strip().lower()
    if mode not in {"auto", "off", "required"}:
        raise AgentError("ARA_OS_SANDBOX must be auto, off, or required")
    if mode == "off":
        return list(command), "copied-workspace"
    bubblewrap = shutil.which("bwrap")
    if bubblewrap and not permissions.network_hosts:
        target = str(workspace.resolve())
        sandbox_command = [
            bubblewrap,
            "--die-with-parent",
            "--new-session",
            "--unshare-pid",
            "--unshare-ipc",
            "--unshare-uts",
            "--unshare-net",
            "--ro-bind",
            "/",
            "/",
            "--tmpfs",
            "/tmp",
            "--bind",
            target,
            target,
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--chdir",
            target,
            *command,
        ]
        # An installed bwrap may still be denied user namespaces by the host.
        # Probe the exact mount/namespace setup without executing the agent, so
        # falling back in auto mode can never execute a failed agent twice.
        try:
            probe = subprocess.run(
                sandbox_command[:-len(command)] + [sys.executable, "-c", "pass"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            reason = f"Bubblewrap probe failed: {error}"
        else:
            if probe.returncode == 0:
                return sandbox_command, "bubblewrap"
            reason = f"Bubblewrap probe failed: {probe.stderr.strip()[-500:]}"
    else:
        reason = (
            "Bubblewrap cannot enforce host allowlists"
            if permissions.network_hosts
            else "Bubblewrap is not installed"
        )
    if mode == "required":
        raise AgentError(f"OS sandbox required: {reason}")
    return list(command), "copied-workspace"
