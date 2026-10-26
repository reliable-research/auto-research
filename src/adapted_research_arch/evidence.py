from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Any
from uuid import uuid4

from .artifacts import ArtifactStore
from .models import CandidateClaim, EvidenceRef
from .project import utc_now


class ClaimError(RuntimeError):
    """Raised when claim evidence or promotion is invalid."""


class ClaimStore:
    def __init__(self, db_path: Path | str, artifacts: ArtifactStore):
        self.db_path = Path(db_path)
        self.artifacts = artifacts
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS claims (
                    id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    stage_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    value REAL,
                    unit TEXT,
                    state TEXT NOT NULL,
                    evidence_resolved INTEGER NOT NULL,
                    evaluation_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS claim_evidence (
                    claim_id TEXT NOT NULL REFERENCES claims(id),
                    source TEXT NOT NULL,
                    locator TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    artifact_id TEXT,
                    resolved INTEGER NOT NULL,
                    PRIMARY KEY(claim_id, source, locator)
                );
                """
            )

    def propose(
        self,
        *,
        run_id: str,
        stage_id: str,
        attempt_id: str,
        claim: CandidateClaim,
    ) -> str:
        claim_id = "clm_" + uuid4().hex
        resolved = bool(claim.evidence)
        evidence_rows: list[tuple[EvidenceRef, bool]] = []
        for evidence in claim.evidence:
            item_resolved = self._resolve(evidence)
            evidence_rows.append((evidence, item_resolved))
            resolved = resolved and item_resolved
        now = utc_now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO claims(id, run_id, stage_id, attempt_id, text, value, unit,
                                   state, evidence_resolved, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    claim_id,
                    run_id,
                    stage_id,
                    attempt_id,
                    claim.text,
                    claim.value,
                    claim.unit,
                    "evidence_linked" if resolved else "draft",
                    int(resolved),
                    now,
                    now,
                ),
            )
            connection.executemany(
                """
                INSERT INTO claim_evidence(claim_id, source, locator, kind, artifact_id, resolved)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        claim_id,
                        evidence.source,
                        evidence.locator,
                        evidence.kind,
                        evidence.artifact_id,
                        int(item_resolved),
                    )
                    for evidence, item_resolved in evidence_rows
                ],
            )
        return claim_id

    def promote(self, claim_id: str, *, evaluation_id: str, evaluation_passed: bool) -> None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
            if not row:
                raise ClaimError(f"claim not found: {claim_id}")
            if not row["evidence_resolved"]:
                raise ClaimError("claim evidence is unresolved")
            if not evaluation_passed:
                raise ClaimError("claim evaluation did not pass")
            if row["value"] is not None:
                numeric = connection.execute(
                    "SELECT 1 FROM claim_evidence WHERE claim_id = ? AND kind = 'numeric' AND resolved = 1",
                    (claim_id,),
                ).fetchone()
                if not numeric:
                    raise ClaimError("numeric claim requires resolved numeric evidence")
            connection.execute(
                "UPDATE claims SET state = 'promoted', evaluation_id = ?, updated_at = ? WHERE id = ?",
                (evaluation_id, utc_now(), claim_id),
            )

    def reject(self, claim_id: str) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE claims SET state = 'rejected', updated_at = ? WHERE id = ?",
                (utc_now(), claim_id),
            )

    def list(self, *, run_id: str | None = None, state: str | None = None) -> list[dict[str, Any]]:
        clauses: list[str] = []
        parameters: list[Any] = []
        if run_id:
            clauses.append("run_id = ?")
            parameters.append(run_id)
        if state:
            clauses.append("state = ?")
            parameters.append(state)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM claims" + where + " ORDER BY created_at", parameters
            ).fetchall()
            result: list[dict[str, Any]] = []
            for row in rows:
                evidence = connection.execute(
                    "SELECT source, locator, kind, artifact_id, resolved FROM claim_evidence WHERE claim_id = ?",
                    (row["id"],),
                ).fetchall()
                result.append({**dict(row), "evidence": [dict(item) for item in evidence]})
        return result

    def _resolve(self, evidence: EvidenceRef) -> bool:
        if evidence.kind == "external":
            return bool(evidence.source.strip() and evidence.locator.strip())
        if not evidence.artifact_id:
            return False
        try:
            return self.artifacts.resolve_locator(evidence.artifact_id, evidence.locator)
        except (OSError, ValueError):
            return False
