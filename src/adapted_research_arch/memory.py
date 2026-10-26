from __future__ import annotations

import json
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable
from uuid import uuid4

from .models import Observation
from .project import utc_now


RELATIONS = {"supports", "contradicts", "supersedes", "derived_from", "related"}


class ResearchMemoryError(RuntimeError):
    """Raised when observations or links cannot be recorded or reviewed."""


class ResearchMemory:
    """Immutable raw observations plus an explicitly reviewed project graph."""

    def __init__(self, db_path: Path | str):
        self.db_path = Path(db_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS observations (
                    id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    stage_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags_json TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    data_class TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    reviewed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS memory_links (
                    source_id TEXT NOT NULL REFERENCES observations(id),
                    target_id TEXT NOT NULL REFERENCES observations(id),
                    relation TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY(source_id, target_id, relation)
                );
                CREATE TABLE IF NOT EXISTS skill_proposals (
                    id TEXT PRIMARY KEY,
                    tag TEXT NOT NULL UNIQUE,
                    support_count INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    evidence_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def propose(
        self,
        *,
        run_id: str,
        stage_id: str,
        attempt_id: str,
        observation: Observation,
    ) -> str:
        observation_id = "obs_" + uuid4().hex
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO observations(id, run_id, stage_id, attempt_id, content, tags_json,
                                         confidence, data_class, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'proposed', ?)
                """,
                (
                    observation_id,
                    run_id,
                    stage_id,
                    attempt_id,
                    observation.content,
                    json.dumps(observation.tags),
                    observation.confidence,
                    observation.data_class,
                    utc_now(),
                ),
            )
        return observation_id

    def review(self, observation_id: str, *, accept: bool) -> None:
        status = "reviewed" if accept else "rejected"
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE observations SET status = ?, reviewed_at = ? WHERE id = ? AND status = 'proposed'",
                (status, utc_now(), observation_id),
            )
            if cursor.rowcount != 1:
                raise ResearchMemoryError(f"observation not reviewable: {observation_id}")

    def link(self, source_id: str, target_id: str, relation: str) -> None:
        if relation not in RELATIONS:
            raise ResearchMemoryError(f"invalid memory relation: {relation}")
        with self._connect() as connection:
            statuses = connection.execute(
                "SELECT id, status FROM observations WHERE id IN (?, ?)", (source_id, target_id)
            ).fetchall()
            if len(statuses) != 2 or any(row["status"] != "reviewed" for row in statuses):
                raise ResearchMemoryError("memory links require reviewed observations")
            connection.execute(
                "INSERT OR IGNORE INTO memory_links(source_id, target_id, relation, created_at) VALUES (?, ?, ?, ?)",
                (source_id, target_id, relation, utc_now()),
            )

    def query(
        self,
        text: str,
        *,
        limit: int = 8,
        reviewed_only: bool = True,
        for_agent: bool = True,
    ) -> list[dict[str, Any]]:
        clauses = ["status = 'reviewed'"] if reviewed_only else []
        parameters: list[Any] = []
        if for_agent:
            clauses.append("data_class IN ('train', 'development')")
        tokens = list(dict.fromkeys(re.findall(r"[A-Za-z0-9_-]{3,}", text.lower())))
        if tokens:
            token_clauses: list[str] = []
            for token in tokens:
                token_clauses.append("(lower(content) LIKE ? OR lower(tags_json) LIKE ?)")
                parameters.extend((f"%{token}%", f"%{token}%"))
            clauses.append("(" + " OR ".join(token_clauses) + ")")
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        parameters.append(limit)
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM observations" + where + " ORDER BY confidence DESC, created_at DESC LIMIT ?",
                parameters,
            ).fetchall()
        return [{**dict(row), "tags": json.loads(row["tags_json"])} for row in rows]

    def propose_skills(self, *, minimum_support: int = 3) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, tags_json FROM observations WHERE status = 'reviewed' AND data_class IN ('train', 'development')"
            ).fetchall()
            grouped: dict[str, list[str]] = {}
            for row in rows:
                for tag in json.loads(row["tags_json"]):
                    grouped.setdefault(tag, []).append(row["id"])
            proposals: list[dict[str, Any]] = []
            for tag, evidence in sorted(grouped.items()):
                if len(evidence) < minimum_support:
                    continue
                proposal_id = "skill_" + uuid4().hex
                connection.execute(
                    """
                    INSERT INTO skill_proposals(id, tag, support_count, status, evidence_json, created_at)
                    VALUES (?, ?, ?, 'quarantined', ?, ?)
                    ON CONFLICT(tag) DO UPDATE SET support_count = excluded.support_count,
                        evidence_json = excluded.evidence_json
                    """,
                    (proposal_id, tag, len(evidence), json.dumps(evidence), utc_now()),
                )
                proposals.append(
                    {"id": proposal_id, "tag": tag, "supportCount": len(evidence), "status": "quarantined"}
                )
        return proposals

    def list_observations(self, *, status: str | None = None) -> list[dict[str, Any]]:
        with self._connect() as connection:
            if status:
                rows = connection.execute(
                    "SELECT * FROM observations WHERE status = ? ORDER BY created_at", (status,)
                ).fetchall()
            else:
                rows = connection.execute("SELECT * FROM observations ORDER BY created_at").fetchall()
        return [{**dict(row), "tags": json.loads(row["tags_json"])} for row in rows]
