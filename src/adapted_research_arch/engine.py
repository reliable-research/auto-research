from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sqlite3
from typing import Any
from uuid import uuid4

from .agent import (
    AgentError,
    CommandAgent,
    ModelAgent,
    RemoteToolAgent,
    prepare_attempt_workspace,
    source_unchanged,
)
from .artifacts import ArtifactRef, ArtifactStore
from .evidence import ClaimError, ClaimStore
from .events import EventLedger, digest_json
from .memory import ResearchMemory
from .models import CandidateClaim, EvidenceRef, StageSpec, WorkflowSpec
from .policy import PolicyEngine
from .project import Project, ProjectError, utc_now
from .registry import AgentPackage, AgentRegistry, RegistryError
from .workflows import WORKFLOWS


class EngineError(RuntimeError):
    """Raised when a workflow cannot be created or resumed safely."""


def _validate_agent_pins(workflow: WorkflowSpec, pins: dict[str, str]) -> dict[str, str]:
    if not isinstance(pins, dict):
        raise EngineError("agent pins must be an object mapping stage or capability to agent id")
    allowed = {stage.id for stage in workflow.stages} | {stage.capability for stage in workflow.stages}
    normalized: dict[str, str] = {}
    for raw_key, raw_value in pins.items():
        key, value = str(raw_key).strip(), str(raw_value).strip()
        if key not in allowed:
            raise EngineError(f"agent pin does not name a stage or capability in {workflow.id}: {key}")
        if not value:
            raise EngineError(f"agent pin for {key} has an empty agent id")
        normalized[key] = value
    return dict(sorted(normalized.items()))


def _pinned_agent(stage: StageSpec, pins: dict[str, str]) -> str | None:
    """A stage-specific pin overrides a capability-wide pin."""
    return pins.get(stage.id) or pins.get(stage.capability)


class ResearchEngine:
    """Durable workflow engine with attempt isolation and evidence gates."""

    def __init__(self, project: Project, *, registry: AgentRegistry | None = None):
        self.project = project
        self.registry = registry or AgentRegistry(project)
        self.policy = PolicyEngine(project)
        self.memory = ResearchMemory(project.db_path)

    def start(
        self,
        *,
        workflow_id: str,
        objective: str,
        control_mode: str = "autopilot",
        thread_id: str | None = None,
        idempotency_key: str | None = None,
        agent_pins: dict[str, str] | None = None,
        execute: bool = True,
    ) -> dict[str, Any]:
        workflow = self._workflow(workflow_id)
        pins = _validate_agent_pins(workflow, agent_pins or {})
        if thread_id is None:
            thread = self.project.start_thread(
                idempotency_key=f"{idempotency_key}:thread" if idempotency_key else None
            )
            thread_id = str(thread["id"])
        run = self.project.create_run(
            thread_id=thread_id,
            workflow_id=workflow.id,
            workflow_version=workflow.version,
            objective=objective,
            control_mode=control_mode,
            idempotency_key=idempotency_key,
        )
        ledger = self._ledger(str(run["id"]))
        if not ledger.read():
            ledger.append(
                "workflow/created",
                {
                    "workflowId": workflow.id,
                    "workflowVersion": workflow.version,
                    "objective": objective,
                    "controlMode": control_mode,
                    "agentPins": pins,
                },
            )
        elif pins != self._agent_pins(ledger):
            raise EngineError("idempotent workflow start cannot change recorded agent pins")
        return self.resume(str(run["id"])) if execute else self.describe(str(run["id"]))

    def resume(self, run_id: str) -> dict[str, Any]:
        run = self.project.read_run(run_id)
        if run["status"] == "completed":
            return self.describe(run_id)
        if run["status"] == "stopped":
            raise EngineError("a stopped workflow cannot be resumed")
        workflow = self._workflow(str(run["workflow_id"]))
        if str(run["workflow_version"]) != workflow.version:
            raise EngineError(
                f"run pins {workflow.id}@{run['workflow_version']}, installed version is {workflow.version}"
            )
        ledger = self._ledger(run_id)
        agent_pins = self._agent_pins(ledger)
        completed = ledger.completed_stages()
        self._reconcile_interrupted_attempts(run_id, ledger)
        self.project.set_run_status(run_id, "running")

        for stage in workflow.stages:
            if stage.id in completed:
                continue
            missing = set(stage.depends_on) - completed
            if missing:
                raise EngineError(f"stage {stage.id} has incomplete dependencies: {sorted(missing)}")
            try:
                package = self.registry.route(
                    stage.capability,
                    agent_id=_pinned_agent(stage, agent_pins),
                )
            except RegistryError as error:
                return self._block(run_id, stage, ledger, str(error))
            decision = self.policy.decide(
                run_id=run_id,
                stage_id=stage.id,
                stage_risk=stage.risk,
                package=package,
                control_mode=str(run["control_mode"]),
            )
            if decision.status == "waiting_approval":
                self.project.set_run_status(run_id, "waiting_approval")
                ledger.append(
                    "approval/required",
                    {
                        "reason": decision.reason,
                        "agentId": package.manifest.id,
                        "agentDigest": package.package_digest,
                        "permissions": decision.permissions.to_dict(),
                        "budget": decision.budget.to_dict(),
                    },
                    stage_id=stage.id,
                )
                return self.describe(run_id)
            if decision.status != "approved":
                return self._block(run_id, stage, ledger, decision.reason or "policy denied execution")

            attempt_id = "att_" + uuid4().hex
            attempt_root = self.project.run_dir(run_id) / "attempts" / stage.id / attempt_id
            workspace = attempt_root / "workspace"
            source_snapshot = prepare_attempt_workspace(self.project.workspace_dir, workspace)
            self._insert_attempt(run_id, stage, package, attempt_id, workspace)
            ledger.append(
                "stage/started",
                {
                    "capability": stage.capability,
                    "agentId": package.manifest.id,
                    "agentVersion": package.manifest.version,
                    "agentDigest": package.package_digest,
                },
                stage_id=stage.id,
                attempt_id=attempt_id,
            )
            store = ArtifactStore(self.project.run_dir(run_id), self.project.db_path, run_id=run_id)
            claims = ClaimStore(self.project.db_path, store)
            request = self._request(run, workflow, stage, attempt_id, completed, claims, package)
            request["effectiveBudget"] = decision.budget.to_dict()
            request["effectivePermissions"] = decision.permissions.to_dict()
            store.add_json(
                stage_id=stage.id,
                attempt_id=attempt_id,
                name="request.json",
                value=request,
            )
            try:
                adapter = self._adapter(package)
                result = adapter.execute(
                    request,
                    workspace=workspace,
                    permissions=decision.permissions,
                    budget=decision.budget,
                )
            except (AgentError, OSError) as error:
                store.add_text(
                    stage_id=stage.id,
                    attempt_id=attempt_id,
                    name="failure.txt",
                    content=str(error),
                )
                self._finish_attempt(attempt_id, "failed", error=str(error))
                self.project.set_run_status(run_id, "failed", outcome="failed")
                ledger.append(
                    "stage/failed",
                    {"reason": str(error), "artifactsPreserved": True},
                    stage_id=stage.id,
                    attempt_id=attempt_id,
                )
                return self.describe(run_id)

            stdout_ref = store.add_text(
                stage_id=stage.id,
                attempt_id=attempt_id,
                name="stdout.json",
                content=result.stdout,
                media_type="application/json",
            )
            stderr_ref = store.add_text(
                stage_id=stage.id,
                attempt_id=attempt_id,
                name="stderr.txt",
                content=result.stderr,
            )
            artifact_refs: dict[str, ArtifactRef] = {}
            for name, content in result.output.artifacts.items():
                media_type = "application/json" if name.endswith(".json") else "text/plain"
                artifact_refs[name] = store.add_text(
                    stage_id=stage.id,
                    attempt_id=attempt_id,
                    name=name,
                    content=content,
                    media_type=media_type,
                )

            claim_ids: list[str] = []
            for candidate in result.output.claims:
                bound = self._bind_claim(candidate, artifact_refs)
                claim_ids.append(
                    claims.propose(
                        run_id=run_id,
                        stage_id=stage.id,
                        attempt_id=attempt_id,
                        claim=bound,
                    )
                )
            observation_ids = [
                self.memory.propose(
                    run_id=run_id,
                    stage_id=stage.id,
                    attempt_id=attempt_id,
                    observation=observation,
                )
                for observation in result.output.observations
            ]
            output_record = {
                **result.output.to_dict(),
                "artifactIds": {name: item.id for name, item in artifact_refs.items()},
                "claimIds": claim_ids,
                "observationIds": observation_ids,
                "stdoutArtifactId": stdout_ref.id,
                "stderrArtifactId": stderr_ref.id,
                "durationSeconds": result.duration_seconds,
            }
            stage_result = self._write_stage_result(run_id, stage, attempt_id, package, output_record)

            if not source_unchanged(self.project.workspace_dir, source_snapshot):
                return self._evaluation_failure(
                    run_id, stage, attempt_id, ledger, "project source workspace was mutated"
                )
            gate_errors = self._evaluate_gates(
                run_id=run_id,
                stage=stage,
                attempt_id=attempt_id,
                output=output_record,
                request=request,
                claims=claims,
            )
            gate_errors.extend(_usage_errors(result.output.usage, decision.budget))
            if gate_errors:
                return self._evaluation_failure(
                    run_id, stage, attempt_id, ledger, "; ".join(gate_errors)
                )
            if result.output.status in {"failed", "blocked"}:
                status = result.output.status
                self._finish_attempt(attempt_id, status, output=stage_result)
                self.project.set_run_status(run_id, status, outcome=status)
                ledger.append(
                    f"stage/{status}",
                    {"summary": result.output.summary, "artifactsPreserved": True},
                    stage_id=stage.id,
                    attempt_id=attempt_id,
                )
                return self.describe(run_id)

            self._finish_attempt(attempt_id, result.output.status, output=stage_result)
            ledger.append(
                "stage/completed",
                {
                    "status": result.output.status,
                    "summary": result.output.summary,
                    "claimIds": claim_ids,
                    "observationIds": observation_ids,
                    "gateCount": len(stage.gates),
                    "resultDigest": digest_json(stage_result),
                },
                stage_id=stage.id,
                attempt_id=attempt_id,
            )
            completed.add(stage.id)

        outcome = self._run_outcome(run_id)
        self.project.set_run_status(run_id, "completed", outcome=outcome)
        ledger.append("workflow/completed", {"outcome": outcome})
        return self.describe(run_id)

    def pause(self, run_id: str) -> dict[str, Any]:
        run = self.project.read_run(run_id)
        if run["status"] in {"completed", "stopped"}:
            raise EngineError(f"cannot pause a {run['status']} workflow")
        self.project.set_run_status(run_id, "paused")
        self._ledger(run_id).append("workflow/paused", {})
        return self.describe(run_id)

    def stop(self, run_id: str) -> dict[str, Any]:
        run = self.project.read_run(run_id)
        if run["status"] == "completed":
            raise EngineError("cannot stop a completed workflow")
        self.project.set_run_status(run_id, "stopped", outcome="stopped")
        self._ledger(run_id).append("workflow/stopped", {})
        return self.describe(run_id)

    def retry(self, run_id: str) -> dict[str, Any]:
        run = self.project.read_run(run_id)
        if run["status"] not in {"failed", "blocked"}:
            raise EngineError("retry requires a failed or blocked workflow")
        self._ledger(run_id).append("workflow/retry_requested", {})
        return self.resume(run_id)

    def approve(self, run_id: str, *, stage_id: str | None = None, scope: str = "stage") -> dict[str, Any]:
        run = self.project.read_run(run_id)
        workflow = self._workflow(str(run["workflow_id"]))
        completed = self._ledger(run_id).completed_stages()
        target = next(
            (stage for stage in workflow.stages if stage.id == stage_id),
            None,
        ) if stage_id else next((stage for stage in workflow.stages if stage.id not in completed), None)
        if target is None:
            raise EngineError("no pending stage to approve")
        package = self.registry.route(
            target.capability,
            agent_id=_pinned_agent(target, self._agent_pins(self._ledger(run_id))),
        )
        approval_id = self.policy.grant(
            run_id=run_id,
            stage_id=target.id,
            package=package,
            scope=scope,
        )
        self._ledger(run_id).append(
            "approval/granted",
            {"approvalId": approval_id, "scope": scope, "agentDigest": package.package_digest},
            stage_id=target.id,
        )
        return {"approvalId": approval_id, "runId": run_id, "stageId": target.id, "scope": scope}

    def describe(self, run_id: str) -> dict[str, Any]:
        run = self.project.read_run(run_id)
        ledger = self._ledger(run_id)
        workflow = self._workflow(str(run["workflow_id"]))
        completed = ledger.completed_stages()
        next_stage = next((item.id for item in workflow.stages if item.id not in completed), None)
        with self.project.connect() as connection:
            attempts = [
                dict(row)
                for row in connection.execute(
                    "SELECT * FROM attempts WHERE run_id = ? ORDER BY created_at", (run_id,)
                ).fetchall()
            ]
        return {
            **run,
            "agentPins": self._agent_pins(ledger),
            "completedStages": [stage.id for stage in workflow.stages if stage.id in completed],
            "nextStage": next_stage,
            "attempts": attempts,
            "lastSequence": len(ledger.read()),
        }

    def _workflow(self, workflow_id: str) -> WorkflowSpec:
        try:
            return WORKFLOWS[workflow_id]
        except KeyError as error:
            raise EngineError(f"unknown workflow: {workflow_id}") from error

    def _ledger(self, run_id: str) -> EventLedger:
        return EventLedger(
            self.project.run_dir(run_id) / "events.jsonl",
            project_id=self.project.project_id,
            run_id=run_id,
        )

    @staticmethod
    def _agent_pins(ledger: EventLedger) -> dict[str, str]:
        created = next(ledger.events_of_type("workflow/created"), None)
        raw = (created or {}).get("payload", {}).get("agentPins", {})
        return {str(key): str(value) for key, value in raw.items()} if isinstance(raw, dict) else {}

    def _adapter(self, package: AgentPackage) -> CommandAgent:
        adapter_type = package.manifest.adapter["type"]
        if adapter_type == "command":
            return CommandAgent(package)
        if adapter_type == "model":
            return ModelAgent(package)
        if adapter_type == "remote_tool":
            return RemoteToolAgent(package)
        raise EngineError(f"unsupported adapter: {adapter_type!r}")

    def _request(
        self,
        run: dict[str, Any],
        workflow: WorkflowSpec,
        stage: StageSpec,
        attempt_id: str,
        completed: set[str],
        claims: ClaimStore,
        package: AgentPackage,
    ) -> dict[str, Any]:
        dependency_results = {
            dependency: _sanitize_agent_context(self._read_stage_result(str(run["id"]), dependency))
            for dependency in stage.depends_on
            if dependency in completed
        }
        promoted = claims.list(run_id=str(run["id"]), state="promoted")
        candidates = claims.list(run_id=str(run["id"]), state="evidence_linked")
        return {
            "protocolVersion": "1.0",
            "projectId": self.project.project_id,
            "runId": run["id"],
            "threadId": run["thread_id"],
            "attemptId": attempt_id,
            "objective": run["objective"],
            "workflow": {"id": workflow.id, "version": workflow.version},
            "stage": {
                "id": stage.id,
                "capability": stage.capability,
                "purpose": stage.purpose,
                "outputs": list(stage.outputs),
                "gates": list(stage.gates),
            },
            "dependencyResults": dependency_results,
            "candidateClaims": candidates if stage.capability == "review.audit_integrity" else [],
            "promotedClaims": promoted if stage.capability == "publication.write_from_claims" else [],
            "memory": self.memory.query(str(run["objective"]), reviewed_only=True, for_agent=True),
            "dataFirewall": {
                "agentVisible": ["train", "development"],
                "excluded": ["evaluation", "publication_only"],
            },
            "isolation": {"mode": "copied-attempt-workspace", "sourceMutationCheck": True},
            "agent": {
                "id": package.manifest.id,
                "version": package.manifest.version,
                "packageDigest": package.package_digest,
                "adapter": package.manifest.adapter,
                "instructions": (package.root / "AGENT.md").read_text(encoding="utf-8"),
            },
        }

    @staticmethod
    def _bind_claim(candidate: CandidateClaim, artifacts: dict[str, ArtifactRef]) -> CandidateClaim:
        evidence: list[EvidenceRef] = []
        for item in candidate.evidence:
            artifact_id = item.artifact_id
            if item.source.startswith("artifact:"):
                name = item.source.split(":", 1)[1]
                artifact = artifacts.get(name)
                artifact_id = artifact.id if artifact else None
            evidence.append(
                EvidenceRef(
                    source=item.source,
                    locator=item.locator,
                    kind=item.kind,
                    artifact_id=artifact_id,
                )
            )
        return CandidateClaim(
            text=candidate.text,
            evidence=tuple(evidence),
            value=candidate.value,
            unit=candidate.unit,
        )

    def _evaluate_gates(
        self,
        *,
        run_id: str,
        stage: StageSpec,
        attempt_id: str,
        output: dict[str, Any],
        request: dict[str, Any],
        claims: ClaimStore,
    ) -> list[str]:
        errors: list[str] = []
        stage_claims = [item for item in claims.list(run_id=run_id) if item["attempt_id"] == attempt_id]
        for gate in stage.gates:
            if gate == "schema.valid":
                missing = set(stage.outputs) - set(output.get("records", {}))
                if missing:
                    errors.append(f"schema.valid missing records {sorted(missing)}")
            elif gate in {"evidence.locator_resolution", "claim.evidence_complete"}:
                unresolved = [item["id"] for item in stage_claims if not item["evidence_resolved"]]
                if unresolved:
                    errors.append(f"{gate} unresolved claims {unresolved}")
            elif gate == "numeric.provenance":
                for item in stage_claims:
                    if item["value"] is None:
                        continue
                    if not item["evidence_resolved"] or not any(
                        evidence["kind"] == "numeric" and evidence["resolved"]
                        for evidence in item["evidence"]
                    ):
                        errors.append(f"numeric.provenance failed for {item['id']}")
            elif gate == "baseline.matched":
                baseline = self._read_stage_result(run_id, "baseline")
                if set(baseline.get("metrics", {})) != set(output.get("metrics", {})):
                    errors.append("baseline.matched metric contract differs")
            elif gate == "claim.promotion":
                drafts = claims.list(run_id=run_id, state="draft")
                if drafts:
                    errors.append(f"claim.promotion unresolved claims {[item['id'] for item in drafts]}")
                decision = next(iter(output.get("records", {}).values()), {}).get("reviewDecision")
                if decision != "pass":
                    errors.append("claim.promotion requires reviewDecision=pass")
                else:
                    for item in claims.list(run_id=run_id, state="evidence_linked"):
                        try:
                            claims.promote(
                                item["id"],
                                evaluation_id="eval_" + attempt_id,
                                evaluation_passed=True,
                            )
                        except ClaimError as error:
                            errors.append(f"claim.promotion {item['id']}: {error}")
            elif gate == "publication.reverse_links":
                promoted = request.get("promotedClaims", [])
                if claims.list(run_id=run_id, state="evidence_linked"):
                    errors.append("publication.reverse_links received unpromoted claims")
                if promoted and not output.get("artifactIds"):
                    errors.append("publication.reverse_links report artifact missing")
                linked = set(next(iter(output.get("records", {}).values()), {}).get("claimIds", []))
                expected = {item["id"] for item in promoted}
                if linked != expected:
                    errors.append("publication.reverse_links do not match promoted claims")
            else:
                errors.append(f"unknown evaluator gate: {gate}")
        return errors

    def _write_stage_result(
        self,
        run_id: str,
        stage: StageSpec,
        attempt_id: str,
        package: AgentPackage,
        output: dict[str, Any],
    ) -> dict[str, Any]:
        result = {
            "stageId": stage.id,
            "attemptId": attempt_id,
            "agent": {
                "id": package.manifest.id,
                "version": package.manifest.version,
                "digest": package.package_digest,
            },
            **output,
        }
        stages_dir = self.project.run_dir(run_id) / "stages"
        stages_dir.mkdir(parents=True, exist_ok=True)
        target = stages_dir / f"{stage.id}.json"
        temporary = target.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        temporary.replace(target)
        return result

    def _read_stage_result(self, run_id: str, stage_id: str) -> dict[str, Any]:
        target = self.project.run_dir(run_id) / "stages" / f"{stage_id}.json"
        if not target.is_file():
            raise EngineError(f"completed stage result missing: {stage_id}")
        return json.loads(target.read_text(encoding="utf-8"))

    def _insert_attempt(
        self,
        run_id: str,
        stage: StageSpec,
        package: AgentPackage,
        attempt_id: str,
        workspace: Path,
    ) -> None:
        with self.project.connect() as connection:
            connection.execute(
                """
                INSERT INTO attempts(id, run_id, stage_id, agent_id, agent_version,
                                     agent_digest, status, workspace, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 'running', ?, ?)
                """,
                (
                    attempt_id,
                    run_id,
                    stage.id,
                    package.manifest.id,
                    package.manifest.version,
                    package.package_digest,
                    str(workspace),
                    utc_now(),
                ),
            )

    def _finish_attempt(
        self,
        attempt_id: str,
        status: str,
        *,
        output: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> None:
        with self.project.connect() as connection:
            connection.execute(
                """
                UPDATE attempts SET status = ?, output_json = ?, error = ?, completed_at = ?
                WHERE id = ?
                """,
                (
                    status,
                    json.dumps(output, sort_keys=True) if output is not None else None,
                    error,
                    utc_now(),
                    attempt_id,
                ),
            )

    def _block(
        self, run_id: str, stage: StageSpec, ledger: EventLedger, reason: str
    ) -> dict[str, Any]:
        self.project.set_run_status(run_id, "blocked", outcome="blocked")
        ledger.append("stage/blocked", {"reason": reason}, stage_id=stage.id)
        return self.describe(run_id)

    def _evaluation_failure(
        self,
        run_id: str,
        stage: StageSpec,
        attempt_id: str,
        ledger: EventLedger,
        reason: str,
    ) -> dict[str, Any]:
        self._finish_attempt(attempt_id, "evaluation_failed", error=reason)
        self.project.set_run_status(run_id, "failed", outcome="failed")
        ledger.append(
            "evaluation/failed",
            {"reason": reason, "attemptPreserved": True},
            stage_id=stage.id,
            attempt_id=attempt_id,
        )
        return self.describe(run_id)

    def _run_outcome(self, run_id: str) -> str:
        statuses = [
            str(event.get("payload", {}).get("status"))
            for event in self._ledger(run_id).events_of_type("stage/completed")
        ]
        if "negative" in statuses:
            return "negative"
        if "inconclusive" in statuses:
            return "inconclusive"
        if "saturated" in statuses:
            return "saturated"
        if "floored" in statuses:
            return "floored"
        return "positive"

    def _reconcile_interrupted_attempts(self, run_id: str, ledger: EventLedger) -> None:
        with self.project.connect() as connection:
            rows = connection.execute(
                "SELECT id, stage_id FROM attempts WHERE run_id = ? AND status = 'running'",
                (run_id,),
            ).fetchall()
            for row in rows:
                connection.execute(
                    "UPDATE attempts SET status = 'interrupted', error = ?, completed_at = ? WHERE id = ?",
                    ("reconciled during workflow resume", utc_now(), row["id"]),
                )
                ledger.append(
                    "attempt/interrupted",
                    {"reason": "process ended before a terminal event", "artifactsPreserved": True},
                    stage_id=row["stage_id"],
                    attempt_id=row["id"],
                )


def verify_run(project: Project, run_id: str) -> dict[str, Any]:
    """Verify durable run state, event chain, artifacts, and stage/attempt agreement."""
    run = project.read_run(run_id)
    ledger = EventLedger(
        project.run_dir(run_id) / "events.jsonl",
        project_id=project.project_id,
        run_id=run_id,
    )
    errors: list[str] = []
    try:
        events = ledger.verify()
    except Exception as error:  # verification should report, not crash
        events = []
        errors.append(str(error))
    store = ArtifactStore(project.run_dir(run_id), project.db_path, run_id=run_id)
    errors.extend(store.verify())
    with project.connect() as connection:
        attempt_rows = connection.execute(
            "SELECT * FROM attempts WHERE run_id = ?", (run_id,)
        ).fetchall()
    attempts = {str(row["id"]): dict(row) for row in attempt_rows}

    created_events = [event for event in events if event.get("type") == "workflow/created"]
    if len(created_events) != 1:
        errors.append(f"workflow has {len(created_events)} creation events")
    else:
        created = created_events[0].get("payload", {})
        expected_creation = {
            "workflowId": run["workflow_id"],
            "workflowVersion": run["workflow_version"],
            "objective": run["objective"],
            "controlMode": run["control_mode"],
        }
        for key, expected in expected_creation.items():
            actual = created.get(key)
            if key == "objective":
                actual, expected = str(actual).strip(), str(expected).strip()
            if actual != expected:
                errors.append(f"workflow creation mismatch for {key}")

    completions: dict[str, int] = {}
    for event in events:
        if event.get("type") == "stage/completed" and event.get("stageId"):
            stage_id = str(event["stageId"])
            completions[stage_id] = completions.get(stage_id, 0) + 1
            target = project.run_dir(run_id) / "stages" / f"{stage_id}.json"
            if not target.is_file():
                errors.append(f"completed stage result missing: {stage_id}")
                continue
            try:
                stage_result = json.loads(target.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"invalid completed stage result {stage_id}: {error}")
                continue
            if not isinstance(stage_result, dict):
                errors.append(f"completed stage result is not an object: {stage_id}")
                continue
            attempt_id = str(event.get("attemptId") or "")
            if stage_result.get("stageId") != stage_id or stage_result.get("attemptId") != attempt_id:
                errors.append(f"stage result identity mismatch: {stage_id}")
            expected_digest = event.get("payload", {}).get("resultDigest")
            if expected_digest and digest_json(stage_result) != expected_digest:
                errors.append(f"stage result digest mismatch: {stage_id}")
            attempt = attempts.get(attempt_id)
            if not attempt:
                errors.append(f"completed stage attempt missing: {stage_id}/{attempt_id}")
                continue
            if attempt["stage_id"] != stage_id:
                errors.append(f"attempt stage mismatch: {stage_id}/{attempt_id}")
            if attempt["status"] != event.get("payload", {}).get("status"):
                errors.append(f"attempt status mismatch: {stage_id}/{attempt_id}")
            result_agent = stage_result.get("agent")
            result_digest = result_agent.get("digest") if isinstance(result_agent, dict) else None
            if attempt["agent_digest"] != result_digest:
                errors.append(f"attempt agent digest mismatch: {stage_id}/{attempt_id}")
            try:
                stored_output = json.loads(attempt["output_json"])
            except (TypeError, json.JSONDecodeError):
                errors.append(f"attempt output missing or invalid: {stage_id}/{attempt_id}")
            else:
                if stored_output != stage_result:
                    errors.append(f"stage result and attempt output differ: {stage_id}/{attempt_id}")
    for stage_id, count in completions.items():
        if count != 1:
            errors.append(f"stage {stage_id} completed {count} times")
    running = [attempt_id for attempt_id, attempt in attempts.items() if attempt["status"] == "running"]
    if running:
        errors.append(f"unfinished attempts: {running}")

    workflow = WORKFLOWS.get(str(run["workflow_id"]))
    if not workflow:
        errors.append(f"installed workflow is missing: {run['workflow_id']}")
    elif run["status"] == "completed":
        expected_stages = {stage.id for stage in workflow.stages}
        if set(completions) != expected_stages:
            errors.append(
                "completed workflow stage set mismatch: "
                f"expected {sorted(expected_stages)}, got {sorted(completions)}"
            )
    terminal_events = [event for event in events if event.get("type") == "workflow/completed"]
    if run["status"] == "completed":
        if len(terminal_events) != 1:
            errors.append(f"completed workflow has {len(terminal_events)} completion events")
        elif terminal_events[0].get("payload", {}).get("outcome") != run["outcome"]:
            errors.append("workflow outcome differs between state and event ledger")
    elif terminal_events:
        errors.append("non-completed workflow has a completion event")
    return {
        "ok": not errors,
        "runId": run_id,
        "status": run["status"],
        "eventCount": len(events),
        "completedStages": sorted(completions),
        "errors": errors,
    }


def _sanitize_agent_context(value: Any) -> Any:
    """Remove evaluation/publication-only records before they enter agent context."""
    if isinstance(value, dict):
        data_class = value.get("dataClass", value.get("data_class"))
        if data_class in {"evaluation", "publication_only"}:
            return {"redacted": True, "reason": "evaluation firewall"}
        return {key: _sanitize_agent_context(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_agent_context(item) for item in value]
    return value


def _usage_errors(usage: dict[str, float], budget: Any) -> list[str]:
    limits = {
        "toolCalls": float(budget.max_tool_calls),
        "sources": float(budget.max_sources),
        "costUsd": float(budget.max_cost_usd),
    }
    errors: list[str] = []
    for key, limit in limits.items():
        consumed = float(usage.get(key, 0))
        if consumed > limit:
            errors.append(f"budget exceeded for {key}: {consumed} > {limit}")
    return errors
