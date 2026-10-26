from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import threading
from typing import Any, Iterable
from uuid import uuid4


class LedgerError(RuntimeError):
    """Raised when an event stream is malformed or altered."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


class EventLedger:
    """Append-only, hash-linked JSONL event stream for one workflow run."""

    def __init__(self, path: Path | str, *, project_id: str, run_id: str):
        self.path = Path(path)
        self.project_id = project_id
        self.run_id = run_id
        self._lock = threading.Lock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            self.verify()

    def read(self, *, after_sequence: int = 0) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        result: list[dict[str, Any]] = []
        with self.path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as error:
                    raise LedgerError(f"invalid JSON at line {line_number}: {error}") from error
                if not isinstance(event, dict):
                    raise LedgerError(f"event at line {line_number} is not an object")
                if int(event.get("sequence", 0)) > after_sequence:
                    result.append(event)
        return result

    def verify(self) -> list[dict[str, Any]]:
        events = self.read()
        previous = "GENESIS"
        for expected, event in enumerate(events, 1):
            if event.get("sequence") != expected:
                raise LedgerError(f"expected sequence {expected}, got {event.get('sequence')!r}")
            if event.get("projectId") != self.project_id or event.get("runId") != self.run_id:
                raise LedgerError(f"event scope mismatch at sequence {expected}")
            if event.get("previousHash") != previous:
                raise LedgerError(f"broken hash chain at sequence {expected}")
            recorded = event.get("hash")
            unsigned = {key: item for key, item in event.items() if key != "hash"}
            computed = digest_json(unsigned)
            if recorded != computed:
                raise LedgerError(f"event hash mismatch at sequence {expected}")
            previous = computed
        return events

    def append(
        self,
        event_type: str,
        payload: dict[str, Any] | None = None,
        *,
        stage_id: str | None = None,
        attempt_id: str | None = None,
        causation_id: str | None = None,
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        with self._lock:
            events = self.verify()
            event: dict[str, Any] = {
                "eventId": uuid4().hex,
                "sequence": len(events) + 1,
                "time": datetime.now(timezone.utc).isoformat(),
                "projectId": self.project_id,
                "runId": self.run_id,
                "type": event_type,
                "stageId": stage_id,
                "attemptId": attempt_id,
                "causationId": causation_id,
                "correlationId": correlation_id,
                "payload": payload or {},
                "previousHash": events[-1]["hash"] if events else "GENESIS",
            }
            event["hash"] = digest_json(event)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            return event

    def events_of_type(self, *event_types: str) -> Iterable[dict[str, Any]]:
        allowed = set(event_types)
        return (event for event in self.verify() if event.get("type") in allowed)

    def completed_stages(self) -> set[str]:
        return {
            str(event["stageId"])
            for event in self.events_of_type("stage/completed")
            if event.get("stageId")
        }
