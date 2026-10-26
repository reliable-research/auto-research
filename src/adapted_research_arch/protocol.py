from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path
import platform
import sqlite3
import sys
from typing import Any, TextIO

from .agent import AgentError, _sandbox_command
from .artifacts import ArtifactStore
from .engine import ResearchEngine, verify_run
from .evidence import ClaimStore
from .events import EventLedger
from .memory import ResearchMemory
from .models import Observation, PermissionSet
from .project import Project
from .registry import AgentRegistry
from .workflows import WORKFLOWS


class ProtocolError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class ProtocolServer:
    """Stateful JSON-RPC-style dispatcher shared by stdio and embedded clients."""

    VERSION = "1.0"

    def __init__(self, default_project_root: Path | str | None = None):
        self.default_project_root = (
            Path(default_project_root).resolve() if default_project_root is not None else None
        )
        self.initialized = False
        self.client_info: dict[str, Any] = {}

    def handle(self, message: Any) -> dict[str, Any] | None:
        request_id = message.get("id") if isinstance(message, dict) else None
        notification = isinstance(message, dict) and "id" not in message
        try:
            if not isinstance(message, dict) or not isinstance(message.get("method"), str):
                raise ProtocolError("invalid_request", "request requires a method")
            method = str(message["method"])
            params = message.get("params", {})
            if not isinstance(params, dict):
                raise ProtocolError("invalid_params", "params must be an object")
            if method != "initialize" and not self.initialized:
                raise ProtocolError("not_initialized", "initialize must be called first")
            result = self._dispatch(method, params)
            if request_id is None:
                return None
            return {"id": request_id, "result": result}
        except ProtocolError as error:
            if notification:
                return None
            return {"id": request_id, "error": {"code": error.code, "message": str(error)}}
        except Exception as error:
            if notification:
                return None
            return {
                "id": request_id,
                "error": {"code": error.__class__.__name__, "message": str(error)},
            }

    def _dispatch(self, method: str, params: dict[str, Any]) -> Any:
        if method == "initialize":
            if self.initialized:
                raise ProtocolError("already_initialized", "connection is already initialized")
            versions = params.get("protocolVersions", [])
            if self.VERSION not in versions:
                raise ProtocolError("unsupported_version", f"client must support {self.VERSION}")
            self.initialized = True
            self.client_info = dict(params.get("clientInfo", {}))
            return {
                "protocolVersion": self.VERSION,
                "serverInfo": {"name": "adapted-research-arch", "version": "0.1.0"},
                "features": [
                    "durable-events",
                    "workflow-resume",
                    "agent-trust",
                    "approval-gates",
                    "claim-provenance",
                    "reviewed-memory",
                ],
            }
        if method == "server/diagnostics":
            project = self._project(params, required=False)
            return diagnostics(project)
        if method == "schema/list":
            return {"schemas": ["agent-manifest.v1", "agent-output.v1", "workflow.v1"]}
        if method == "skills/list":
            return []
        if method == "tools/list":
            return [{"id": "command", "risk": "R3"}, {"id": "remote_tool_bridge", "risk": "R3"}]
        if method == "environments/list":
            return [{"id": "local", "available": True, "isolation": "copy-on-attempt"}]
        if method == "project/create":
            root = params.get("root") or self.default_project_root
            if not root:
                raise ProtocolError("invalid_params", "project/create requires root")
            project = Project.create(root, name=str(params.get("name") or Path(root).name))
            self.default_project_root = project.root
            return project.manifest
        if method == "project/read":
            return self._project(params).manifest
        if method == "project/list":
            if self.default_project_root and (self.default_project_root / Project.MANIFEST).is_file():
                return [Project(self.default_project_root).manifest]
            return []

        project = self._project(params)
        registry = AgentRegistry(project)
        engine = ResearchEngine(project, registry=registry)
        if method == "agents/list":
            return registry.list()
        if method == "agents/read":
            agent_id = self._required(params, "agentId")
            matches = [item for item in registry.list() if item["id"] == agent_id]
            if len(matches) != 1:
                raise ProtocolError("not_found", f"agent did not resolve uniquely: {agent_id}")
            return matches[0]
        if method == "agents/trust":
            return registry.trust(
                self._required(params, "agentId"), version=params.get("version")
            ).to_dict()
        if method == "agents/disable":
            return registry.disable(
                self._required(params, "agentId"), version=params.get("version")
            ).to_dict()
        if method in {"workflows/list", "workflow/list"}:
            return [_workflow_dict(item) for item in WORKFLOWS.values()]
        if method == "thread/start":
            return project.start_thread(idempotency_key=params.get("idempotencyKey"))
        if method == "thread/fork":
            return project.start_thread(
                parent_id=self._required(params, "parentThreadId"),
                fork_boundary=params.get("forkBoundary"),
                idempotency_key=params.get("idempotencyKey"),
            )
        if method == "thread/resume":
            thread_id = self._required(params, "threadId")
            project.set_thread_status(thread_id, "active")
            return project.read_thread(thread_id)
        if method == "thread/interrupt":
            thread_id = self._required(params, "threadId")
            project.set_thread_status(thread_id, "interrupted")
            return project.read_thread(thread_id)
        if method == "thread/read":
            return project.read_thread(self._required(params, "threadId"))
        if method == "thread/list":
            return project.list_threads()
        if method == "workflow/start":
            return engine.start(
                workflow_id=self._required(params, "workflowId"),
                objective=self._required(params, "objective"),
                control_mode=str(params.get("controlMode", "autopilot")),
                thread_id=params.get("threadId"),
                idempotency_key=params.get("idempotencyKey"),
                agent_pins=params.get("agentPins"),
                execute=bool(params.get("execute", True)),
            )
        if method == "workflow/resume":
            return engine.resume(self._required(params, "runId"))
        if method == "workflow/pause":
            return engine.pause(self._required(params, "runId"))
        if method == "workflow/stop":
            return engine.stop(self._required(params, "runId"))
        if method in {"workflow/read", "run/read"}:
            return engine.describe(self._required(params, "runId"))
        if method == "stage/approve":
            return engine.approve(
                self._required(params, "runId"),
                stage_id=params.get("stageId"),
                scope=str(params.get("scope", "stage")),
            )
        if method == "stage/retry":
            return engine.retry(self._required(params, "runId"))
        if method == "stage/skip":
            raise ProtocolError("policy_denied", "all v0.1 workflow stages are required")
        if method == "attempt/list":
            run_id = self._required(params, "runId")
            with project.connect() as connection:
                rows = connection.execute(
                    "SELECT * FROM attempts WHERE run_id = ? ORDER BY created_at", (run_id,)
                ).fetchall()
            return [dict(row) for row in rows]
        if method == "attempt/read":
            attempt_id = self._required(params, "attemptId")
            with project.connect() as connection:
                row = connection.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,)).fetchone()
            if not row:
                raise ProtocolError("not_found", f"attempt not found: {attempt_id}")
            return dict(row)
        if method == "run/verify":
            return verify_run(project, self._required(params, "runId"))
        if method == "event/list":
            run_id = self._required(params, "runId")
            project.read_run(run_id)
            ledger = EventLedger(
                project.run_dir(run_id) / "events.jsonl",
                project_id=project.project_id,
                run_id=run_id,
            )
            return ledger.read(after_sequence=int(params.get("afterSequence", 0)))
        if method == "claim/list":
            run_id = params.get("runId")
            if not run_id:
                raise ProtocolError("invalid_params", "claim/list requires runId")
            artifacts = ArtifactStore(project.run_dir(run_id), project.db_path, run_id=run_id)
            return ClaimStore(project.db_path, artifacts).list(
                run_id=run_id, state=params.get("state")
            )
        if method == "claim/read":
            run_id = self._required(params, "runId")
            claim_id = self._required(params, "claimId")
            artifacts = ArtifactStore(project.run_dir(run_id), project.db_path, run_id=run_id)
            matches = [
                item for item in ClaimStore(project.db_path, artifacts).list(run_id=run_id)
                if item["id"] == claim_id
            ]
            if not matches:
                raise ProtocolError("not_found", f"claim not found: {claim_id}")
            return matches[0]
        if method == "memory/query":
            return ResearchMemory(project.db_path).query(
                str(params.get("text", "")),
                limit=int(params.get("limit", 8)),
                reviewed_only=bool(params.get("reviewedOnly", True)),
                for_agent=bool(params.get("forAgent", True)),
            )
        if method == "memory/review":
            memory = ResearchMemory(project.db_path)
            memory.review(
                self._required(params, "observationId"), accept=bool(params.get("accept", False))
            )
            return {"reviewed": True, "accepted": bool(params.get("accept", False))}
        if method == "memory/propose":
            memory = ResearchMemory(project.db_path)
            observation_id = memory.propose(
                run_id=self._required(params, "runId"),
                stage_id=self._required(params, "stageId"),
                attempt_id=self._required(params, "attemptId"),
                observation=Observation.from_dict(dict(params.get("observation", {}))),
            )
            return {"observationId": observation_id, "status": "proposed"}
        if method == "memory/list":
            return ResearchMemory(project.db_path).list_observations(status=params.get("status"))
        if method == "artifact/list":
            run_id = self._required(params, "runId")
            with project.connect() as connection:
                rows = connection.execute(
                    "SELECT * FROM artifacts WHERE run_id = ? ORDER BY created_at", (run_id,)
                ).fetchall()
            return [dict(row) for row in rows]
        if method == "artifact/read":
            run_id = self._required(params, "runId")
            artifact_id = self._required(params, "artifactId")
            artifacts = ArtifactStore(project.run_dir(run_id), project.db_path, run_id=run_id)
            artifact = artifacts.get(artifact_id)
            content = artifacts.content(artifact_id)
            try:
                rendered = content.decode("utf-8")
                encoding = "utf-8"
            except UnicodeDecodeError:
                import base64

                rendered = base64.b64encode(content).decode("ascii")
                encoding = "base64"
            return {**asdict(artifact), "encoding": encoding, "content": rendered}
        raise ProtocolError("method_not_found", f"unsupported method: {method}")

    def _project(self, params: dict[str, Any], *, required: bool = True) -> Project | None:
        root = params.get("projectRoot") or self.default_project_root
        if root is None:
            if required:
                raise ProtocolError("invalid_params", "projectRoot is required")
            return None
        return Project(root)

    @staticmethod
    def _required(params: dict[str, Any], name: str) -> str:
        value = str(params.get(name, "")).strip()
        if not value:
            raise ProtocolError("invalid_params", f"{name} is required")
        return value


def diagnostics(project: Project | None = None) -> dict[str, Any]:
    try:
        _, sandbox_backend = _sandbox_command(
            [sys.executable, "-c", "pass"],
            project.root if project else Path.cwd(),
            PermissionSet(process=True),
        )
        sandbox_status = sandbox_backend
    except AgentError as error:
        sandbox_backend = "unavailable"
        sandbox_status = str(error)
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pid": os.getpid(),
        "project": str(project.root) if project else None,
        "workspaceIsolation": "copy-on-attempt with source mutation detection",
        "osSandbox": sandbox_status,
        "networkEnforcement": (
            "network namespace disabled under Bubblewrap; host allowlists require a deployment proxy"
            if sandbox_backend == "bubblewrap"
            else "declarative allowlist only; use an OS/container sandbox for untrusted agents"
        ),
    }


def serve_stdio(
    server: ProtocolServer,
    *,
    input_stream: TextIO = sys.stdin,
    output_stream: TextIO = sys.stdout,
) -> int:
    for line in input_stream:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = server.handle(message)
        except json.JSONDecodeError as error:
            response = {"id": None, "error": {"code": "parse_error", "message": str(error)}}
        if response is not None:
            output_stream.write(json.dumps(response, sort_keys=True, ensure_ascii=False) + "\n")
            output_stream.flush()
    return 0


def _workflow_dict(workflow: Any) -> dict[str, Any]:
    value = asdict(workflow)
    for stage in value["stages"]:
        stage["risk"] = f"R{stage['risk']}"
    return value
