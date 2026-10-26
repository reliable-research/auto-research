from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import sqlite3
from typing import Any
from uuid import uuid4

from .project import utc_now


class ArtifactError(ValueError):
    """Raised when artifact content or locators are invalid."""


@dataclass(frozen=True)
class ArtifactRef:
    id: str
    run_id: str
    stage_id: str
    attempt_id: str
    name: str
    path: str
    sha256: str
    size: int
    media_type: str


class ArtifactStore:
    def __init__(self, run_dir: Path | str, db_path: Path | str, *, run_id: str):
        self.run_dir = Path(run_dir).resolve()
        self.root = self.run_dir / "artifacts"
        self.root.mkdir(parents=True, exist_ok=True)
        self.db_path = Path(db_path)
        self.run_id = run_id
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS artifacts (
                    id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    stage_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    media_type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(run_id, attempt_id, name)
                )
                """
            )

    def add_text(
        self,
        *,
        stage_id: str,
        attempt_id: str,
        name: str,
        content: str,
        media_type: str = "text/plain",
    ) -> ArtifactRef:
        return self.add_bytes(
            stage_id=stage_id,
            attempt_id=attempt_id,
            name=name,
            content=content.encode("utf-8"),
            media_type=media_type,
        )

    def add_json(self, *, stage_id: str, attempt_id: str, name: str, value: Any) -> ArtifactRef:
        return self.add_text(
            stage_id=stage_id,
            attempt_id=attempt_id,
            name=name,
            content=json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            media_type="application/json",
        )

    def add_bytes(
        self,
        *,
        stage_id: str,
        attempt_id: str,
        name: str,
        content: bytes,
        media_type: str,
    ) -> ArtifactRef:
        _safe_name(name)
        digest = hashlib.sha256(content).hexdigest()
        target = self.root / digest[:2] / digest
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_bytes(content)
        artifact = ArtifactRef(
            id="art_" + uuid4().hex,
            run_id=self.run_id,
            stage_id=stage_id,
            attempt_id=attempt_id,
            name=name,
            path=str(target.relative_to(self.run_dir)),
            sha256=digest,
            size=len(content),
            media_type=media_type,
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO artifacts(id, run_id, stage_id, attempt_id, name, path,
                                      sha256, size, media_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (*asdict(artifact).values(), utc_now()),
            )
        return artifact

    def get(self, artifact_id: str) -> ArtifactRef:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM artifacts WHERE id = ? AND run_id = ?",
                (artifact_id, self.run_id),
            ).fetchone()
        if not row:
            raise ArtifactError(f"artifact not found: {artifact_id}")
        return ArtifactRef(**{key: row[key] for key in ArtifactRef.__dataclass_fields__})

    def find_attempt_name(self, attempt_id: str, name: str) -> ArtifactRef:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM artifacts WHERE run_id = ? AND attempt_id = ? AND name = ?",
                (self.run_id, attempt_id, name),
            ).fetchone()
        if not row:
            raise ArtifactError(f"artifact not found for attempt: {name}")
        return ArtifactRef(**{key: row[key] for key in ArtifactRef.__dataclass_fields__})

    def content(self, artifact_id: str) -> bytes:
        artifact = self.get(artifact_id)
        target = self._contained_path(artifact.path)
        content = target.read_bytes()
        if hashlib.sha256(content).hexdigest() != artifact.sha256:
            raise ArtifactError(f"artifact digest mismatch: {artifact_id}")
        return content

    def resolve_locator(self, artifact_id: str, locator: str) -> bool:
        artifact = self.get(artifact_id)
        content = self.content(artifact_id)
        if locator.startswith("line:"):
            try:
                line = int(locator.split(":", 1)[1])
            except ValueError:
                return False
            return 1 <= line <= len(content.decode("utf-8").splitlines())
        if locator.startswith("json:"):
            try:
                value = json.loads(content)
                pointer = locator.split(":", 1)[1]
                _json_pointer(value, pointer)
                return True
            except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, ValueError):
                return False
        if locator.startswith("bytes:"):
            try:
                bounds = locator.split(":", 1)[1]
                start, end = (int(item) for item in bounds.split("-", 1))
            except ValueError:
                return False
            return 0 <= start < end <= len(content)
        if locator == "sha256":
            return bool(artifact.sha256)
        return False

    def verify(self) -> list[str]:
        errors: list[str] = []
        with self._connect() as connection:
            rows = connection.execute("SELECT id, path, sha256, size FROM artifacts WHERE run_id = ?", (self.run_id,)).fetchall()
        for row in rows:
            try:
                target = self._contained_path(row["path"])
            except ArtifactError as error:
                errors.append(f"unsafe artifact path {row['id']}: {error}")
                continue
            if not target.is_file():
                errors.append(f"missing artifact {row['id']}: {row['path']}")
                continue
            content = target.read_bytes()
            if len(content) != row["size"] or hashlib.sha256(content).hexdigest() != row["sha256"]:
                errors.append(f"artifact integrity failure: {row['id']}")
        return errors

    def _contained_path(self, relative: str) -> Path:
        target = (self.run_dir / relative).resolve()
        if not target.is_relative_to(self.run_dir):
            raise ArtifactError(f"artifact path escapes run directory: {relative!r}")
        return target


def _safe_name(name: str) -> None:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts:
        raise ArtifactError(f"artifact name must be safe and relative: {name!r}")


def _json_pointer(value: Any, pointer: str) -> Any:
    if pointer in {"", "/"}:
        return value
    if not pointer.startswith("/"):
        raise ValueError("JSON pointer must start with /")
    current = value
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current
