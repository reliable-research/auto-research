from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterator
from uuid import uuid4


class ProjectError(RuntimeError):
    """Raised when durable project state is missing or inconsistent."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Project:
    """A durable local research project backed by files and SQLite."""

    MANIFEST = "research.json"

    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.manifest_path = self.root / self.MANIFEST
        if not self.manifest_path.is_file():
            raise ProjectError(f"not an adapted research project: {self.root}")
        try:
            self.manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ProjectError(f"invalid project manifest: {error}") from error
        self.project_id = str(self.manifest["projectId"])
        self.state_dir = self.root / ".ara"
        self.runs_dir = self.root / "runs"
        self.agents_dir = self.root / "agents"
        self.workspace_dir = self.root / "workspace"
        self.threads_dir = self.state_dir / "threads"
        self.db_path = self.state_dir / "state.sqlite"
        self._initialize_db()

    @classmethod
    def create(
        cls,
        root: Path | str,
        *,
        name: str,
        policy: dict[str, Any] | None = None,
    ) -> Project:
        target = Path(root).resolve()
        target.mkdir(parents=True, exist_ok=True)
        manifest_path = target / cls.MANIFEST
        if manifest_path.exists():
            existing = cls(target)
            if existing.manifest.get("name") != name:
                raise ProjectError("existing project has a different name")
            if policy is not None and existing.manifest.get("policy") != policy:
                raise ProjectError("existing project has a different policy")
            return existing
        manifest = {
            "schemaVersion": "1.0",
            "projectId": "prj_" + uuid4().hex,
            "name": name.strip() or target.name,
            "createdAt": utc_now(),
            "policy": policy or default_policy(),
        }
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        for directory in (
            target / ".ara",
            target / ".ara" / "threads",
            target / "runs",
            target / "agents",
            target / "workspace",
        ):
            directory.mkdir(parents=True, exist_ok=True)
        return cls(target)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize_db(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS threads (
                    id TEXT PRIMARY KEY,
                    parent_id TEXT REFERENCES threads(id),
                    fork_boundary TEXT,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    thread_id TEXT REFERENCES threads(id),
                    workflow_id TEXT NOT NULL,
                    workflow_version TEXT NOT NULL,
                    objective TEXT NOT NULL,
                    control_mode TEXT NOT NULL,
                    status TEXT NOT NULL,
                    outcome TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS attempts (
                    id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL REFERENCES runs(id),
                    stage_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    agent_version TEXT NOT NULL,
                    agent_digest TEXT NOT NULL,
                    status TEXT NOT NULL,
                    workspace TEXT NOT NULL,
                    output_json TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                );
                CREATE INDEX IF NOT EXISTS attempts_run_stage ON attempts(run_id, stage_id);
                CREATE TABLE IF NOT EXISTS approvals (
                    id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL REFERENCES runs(id),
                    stage_id TEXT NOT NULL,
                    agent_digest TEXT NOT NULL,
                    granted_json TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS idempotency (
                    key TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    PRIMARY KEY(key, kind)
                );
                """
            )

    def start_thread(
        self,
        *,
        parent_id: str | None = None,
        fork_boundary: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        with self.connect() as connection:
            existing = self._idempotent(connection, idempotency_key, "thread")
            if existing:
                row = connection.execute(
                    "SELECT * FROM threads WHERE id = ?", (existing,)
                ).fetchone()
                if not row:
                    raise ProjectError(f"idempotency record points to a missing thread: {existing}")
                changed = []
                if row["parent_id"] != parent_id:
                    changed.append("parent_id")
                if row["fork_boundary"] != fork_boundary:
                    changed.append("fork_boundary")
                if changed:
                    raise ProjectError(
                        "idempotency key was already used with different thread parameters: "
                        + ", ".join(changed)
                    )
                return dict(row)
            if parent_id and not connection.execute(
                "SELECT 1 FROM threads WHERE id = ?", (parent_id,)
            ).fetchone():
                raise ProjectError(f"parent thread not found: {parent_id}")
            thread_id = "thr_" + uuid4().hex
            connection.execute(
                "INSERT INTO threads(id, parent_id, fork_boundary, status, created_at) VALUES (?, ?, ?, 'active', ?)",
                (thread_id, parent_id, fork_boundary, utc_now()),
            )
            self._remember_idempotency(connection, idempotency_key, "thread", thread_id)
        thread_dir = self.thread_dir(thread_id)
        (thread_dir / "workspace").mkdir(parents=True, exist_ok=True)
        (thread_dir / "state.json").write_text(
            json.dumps(
                {
                    "threadId": thread_id,
                    "parentThreadId": parent_id,
                    "forkBoundary": fork_boundary,
                    "writableState": str(thread_dir / "workspace"),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return self.read_thread(thread_id)

    def read_thread(self, thread_id: str) -> dict[str, Any]:
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM threads WHERE id = ?", (thread_id,)).fetchone()
        if not row:
            raise ProjectError(f"thread not found: {thread_id}")
        return dict(row)

    def list_threads(self) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM threads ORDER BY created_at").fetchall()
        return [dict(row) for row in rows]

    def set_thread_status(self, thread_id: str, status: str) -> None:
        if status not in {"active", "interrupted", "closed"}:
            raise ProjectError(f"invalid thread status: {status}")
        with self.connect() as connection:
            cursor = connection.execute(
                "UPDATE threads SET status = ? WHERE id = ?", (status, thread_id)
            )
            if cursor.rowcount != 1:
                raise ProjectError(f"thread not found: {thread_id}")

    def create_run(
        self,
        *,
        thread_id: str,
        workflow_id: str,
        workflow_version: str,
        objective: str,
        control_mode: str,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        if control_mode not in {"autopilot", "copilot", "manual"}:
            raise ProjectError(f"invalid control mode: {control_mode}")
        if not objective.strip():
            raise ProjectError("objective cannot be empty")
        with self.connect() as connection:
            existing = self._idempotent(connection, idempotency_key, "run")
            if existing:
                row = connection.execute("SELECT * FROM runs WHERE id = ?", (existing,)).fetchone()
                if not row:
                    raise ProjectError(f"idempotency record points to a missing run: {existing}")
                expected = {
                    "thread_id": thread_id,
                    "workflow_id": workflow_id,
                    "workflow_version": workflow_version,
                    "objective": objective.strip(),
                    "control_mode": control_mode,
                }
                changed = [key for key, value in expected.items() if row[key] != value]
                if changed:
                    raise ProjectError(
                        "idempotency key was already used with different run parameters: "
                        + ", ".join(changed)
                    )
                return dict(row)
            if not connection.execute("SELECT 1 FROM threads WHERE id = ?", (thread_id,)).fetchone():
                raise ProjectError(f"thread not found: {thread_id}")
            run_id = "run_" + uuid4().hex
            now = utc_now()
            connection.execute(
                """
                INSERT INTO runs(id, thread_id, workflow_id, workflow_version, objective,
                                 control_mode, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 'created', ?, ?)
                """,
                (run_id, thread_id, workflow_id, workflow_version, objective.strip(), control_mode, now, now),
            )
            self._remember_idempotency(connection, idempotency_key, "run", run_id)
        run_dir = self.run_dir(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "attempts").mkdir(exist_ok=True)
        manifest = self.read_run(run_id)
        (run_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return manifest

    def read_run(self, run_id: str) -> dict[str, Any]:
        with self.connect() as connection:
            row = connection.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        if not row:
            raise ProjectError(f"run not found: {run_id}")
        return dict(row)

    def list_runs(self) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute("SELECT * FROM runs ORDER BY created_at").fetchall()
        return [dict(row) for row in rows]

    def set_run_status(self, run_id: str, status: str, *, outcome: str | None = None) -> None:
        with self.connect() as connection:
            cursor = connection.execute(
                "UPDATE runs SET status = ?, outcome = COALESCE(?, outcome), updated_at = ? WHERE id = ?",
                (status, outcome, utc_now(), run_id),
            )
            if cursor.rowcount != 1:
                raise ProjectError(f"run not found: {run_id}")

    def run_dir(self, run_id: str) -> Path:
        return self.runs_dir / run_id

    def thread_dir(self, thread_id: str) -> Path:
        return self.threads_dir / thread_id

    @staticmethod
    def _idempotent(
        connection: sqlite3.Connection, key: str | None, kind: str
    ) -> str | None:
        if not key:
            return None
        row = connection.execute(
            "SELECT entity_id FROM idempotency WHERE key = ? AND kind = ?", (key, kind)
        ).fetchone()
        return str(row[0]) if row else None

    @staticmethod
    def _remember_idempotency(
        connection: sqlite3.Connection,
        key: str | None,
        kind: str,
        entity_id: str,
    ) -> None:
        if key:
            connection.execute(
                "INSERT INTO idempotency(key, kind, entity_id) VALUES (?, ?, ?)",
                (key, kind, entity_id),
            )


def default_policy() -> dict[str, Any]:
    return {
        "permissions": {
            "filesystem": {
                "read": ["project:inputs", "project:papers", "project:workspace"],
                "write": ["attempt:artifacts", "attempt:workspace"],
            },
            "network": {"mode": "disabled", "hosts": []},
            "process": True,
            "scheduler": False,
            "gpu": False,
            "externalWrite": False,
            "secretHandles": [],
        },
        "budget": {
            "maxWallSeconds": 3600,
            "maxToolCalls": 200,
            "maxSources": 100,
            "maxCostUsd": 0,
        },
    }
