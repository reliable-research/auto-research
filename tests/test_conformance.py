from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from adapted_research_arch.agent import AgentError, _sandbox_command
from adapted_research_arch.artifacts import ArtifactError, ArtifactStore
from adapted_research_arch.cli import main as cli_main
from adapted_research_arch.engine import EngineError, ResearchEngine, _sanitize_agent_context, verify_run
from adapted_research_arch.evidence import ClaimError, ClaimStore
from adapted_research_arch.events import EventLedger, LedgerError
from adapted_research_arch.memory import ResearchMemory
from adapted_research_arch.models import CandidateClaim, EvidenceRef, Observation, PermissionSet
from adapted_research_arch.optimizer import (
    ComparisonError,
    MetricContract,
    StrategyResult,
    compare_strategies,
)
from adapted_research_arch.project import Project, ProjectError, default_policy, utc_now
from adapted_research_arch.protocol import ProtocolServer, diagnostics, serve_stdio
from adapted_research_arch.registry import AgentRegistry, RegistryError


class RuntimeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="ara-test-")
        self.root = Path(self.temporary.name)
        self.project = Project.create(self.root, name="conformance")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_workflow(self, workflow: str, objective: str = "fixture") -> dict:
        return ResearchEngine(self.project).start(workflow_id=workflow, objective=objective)


class WorkflowConformanceTests(RuntimeTestCase):
    def test_all_initial_workflows_complete_and_verify(self) -> None:
        for workflow in (
            "literature-review",
            "data-analysis",
            "code-optimization",
            "paper-reproduction",
        ):
            with self.subTest(workflow=workflow):
                project = Project.create(self.root / workflow, name=workflow)
                result = ResearchEngine(project).start(workflow_id=workflow, objective="fixture")
                self.assertEqual(result["status"], "completed")
                self.assertTrue(verify_run(project, result["id"])["ok"])

    def test_idempotent_start_rejects_changed_run_parameters_and_pins(self) -> None:
        parent = self.project.start_thread()
        fork = self.project.start_thread(
            parent_id=parent["id"], fork_boundary="event:1", idempotency_key="fork-key"
        )
        repeated_fork = self.project.start_thread(
            parent_id=parent["id"], fork_boundary="event:1", idempotency_key="fork-key"
        )
        self.assertEqual(repeated_fork["id"], fork["id"])
        with self.assertRaises(ProjectError):
            self.project.start_thread(
                parent_id=parent["id"], fork_boundary="event:2", idempotency_key="fork-key"
            )

        engine = ResearchEngine(self.project)
        original = engine.start(
            workflow_id="literature-review",
            objective="fixed request",
            idempotency_key="fixed-key",
            execute=False,
        )
        repeated = engine.start(
            workflow_id="literature-review",
            objective="fixed request",
            idempotency_key="fixed-key",
            execute=False,
        )
        self.assertEqual(repeated["id"], original["id"])
        for change in (
            {"workflow_id": "data-analysis", "objective": "fixed request"},
            {"workflow_id": "literature-review", "objective": "changed request"},
            {
                "workflow_id": "literature-review",
                "objective": "fixed request",
                "control_mode": "manual",
            },
        ):
            with self.subTest(change=change), self.assertRaises(ProjectError):
                engine.start(idempotency_key="fixed-key", execute=False, **change)
        with self.assertRaises(EngineError):
            engine.start(
                workflow_id="literature-review",
                objective="fixed request",
                idempotency_key="fixed-key",
                agent_pins={"frame": "arch.research.planner"},
                execute=False,
            )

    def test_resume_reconciles_interrupted_attempt_without_repeating_completed_stage(self) -> None:
        engine = ResearchEngine(self.project)
        run = engine.start(workflow_id="literature-review", objective="resume", execute=False)
        stale_id = "att_interrupted"
        with self.project.connect() as connection:
            connection.execute(
                """
                INSERT INTO attempts(id, run_id, stage_id, agent_id, agent_version,
                                     agent_digest, status, workspace, created_at)
                VALUES (?, ?, 'frame', 'arch.research.planner', '0.1.0', 'old',
                        'running', ?, ?)
                """,
                (stale_id, run["id"], str(self.root / "stale"), utc_now()),
            )
        completed = engine.resume(run["id"])
        self.assertEqual(completed["status"], "completed")
        stale = next(item for item in completed["attempts"] if item["id"] == stale_id)
        self.assertEqual(stale["status"], "interrupted")
        events = EventLedger(
            self.project.run_dir(run["id"]) / "events.jsonl",
            project_id=self.project.project_id,
            run_id=run["id"],
        ).read()
        self.assertEqual(sum(item["type"] == "stage/completed" and item["stageId"] == "frame" for item in events), 1)

    def test_copilot_high_risk_stage_requires_digest_bound_approval(self) -> None:
        engine = ResearchEngine(self.project)
        waiting = engine.start(
            workflow_id="literature-review", objective="approval", control_mode="copilot"
        )
        self.assertEqual(waiting["status"], "waiting_approval")
        self.assertEqual(waiting["nextStage"], "audit")
        approval = engine.approve(waiting["id"], stage_id="audit")
        self.assertEqual(approval["stageId"], "audit")
        finished = engine.resume(waiting["id"])
        self.assertEqual(finished["status"], "completed")

    def test_explicit_agent_pin_routes_real_high_risk_adapter_and_is_durable(self) -> None:
        _write_agent(
            self.project.agents_dir / "evaluator",
            agent_id="custom.product-evaluator",
            capability="experiment.execute",
            outputs=["experiment.result_set.v1"],
            valid_records=True,
            risk="R3",
            allow_implicit=False,
        )
        registry = AgentRegistry(self.project)
        registry.trust("custom.product-evaluator")
        result = ResearchEngine(self.project, registry=registry).start(
            workflow_id="code-optimization",
            objective="fixed product evaluation",
            agent_pins={"experiment.execute": "custom.product-evaluator"},
        )
        self.assertEqual(result["status"], "completed")
        self.assertEqual(
            result["agentPins"],
            {"experiment.execute": "custom.product-evaluator"},
        )
        executed = [
            item for item in result["attempts"] if item["stage_id"] in {"baseline", "evaluate"}
        ]
        self.assertEqual({item["agent_id"] for item in executed}, {"custom.product-evaluator"})
        created = EventLedger(
            self.project.run_dir(result["id"]) / "events.jsonl",
            project_id=self.project.project_id,
            run_id=result["id"],
        ).read()[0]
        self.assertEqual(
            created["payload"]["agentPins"],
            {"experiment.execute": "custom.product-evaluator"},
        )

    def test_negative_and_inconclusive_are_first_class_outcomes(self) -> None:
        negative = self.run_workflow("literature-review", "[negative] fixture")
        self.assertEqual(negative["status"], "completed")
        self.assertEqual(negative["outcome"], "negative")
        project = Project.create(self.root / "other", name="other")
        inconclusive = ResearchEngine(project).start(
            workflow_id="literature-review", objective="[inconclusive] fixture"
        )
        self.assertEqual(inconclusive["status"], "completed")
        self.assertEqual(inconclusive["outcome"], "inconclusive")

        for marker, expected in (("[saturated]", "saturated"), ("[floored]", "floored")):
            with self.subTest(outcome=expected):
                extra = Project.create(self.root / expected, name=expected)
                result = ResearchEngine(extra).start(
                    workflow_id="literature-review", objective=f"{marker} fixture"
                )
                self.assertEqual(result["status"], "completed")
                self.assertEqual(result["outcome"], expected)

    def test_declared_usage_over_budget_fails_and_is_recorded(self) -> None:
        _write_agent(
            self.project.agents_dir / "over-budget",
            agent_id="a.budget",
            capability="research.frame_objective",
            outputs=["research.objective.v1"],
            valid_records=True,
            usage={"toolCalls": 1},
        )
        AgentRegistry(self.project).trust("a.budget")
        result = self.run_workflow("literature-review")
        self.assertEqual(result["status"], "failed")
        self.assertIn("budget exceeded", result["attempts"][0]["error"])

    def test_model_and_remote_tool_bridges_use_the_agent_contract(self) -> None:
        for adapter_type in ("model", "remote_tool"):
            with self.subTest(adapter=adapter_type):
                project = Project.create(self.root / adapter_type, name=adapter_type)
                agent_id = f"a.{adapter_type.replace('_', '-')}"
                _write_agent(
                    project.agents_dir / adapter_type,
                    agent_id=agent_id,
                    capability="research.frame_objective",
                    outputs=["research.objective.v1"],
                    valid_records=True,
                    adapter_type=adapter_type,
                )
                AgentRegistry(project).trust(agent_id)
                result = ResearchEngine(project).start(
                    workflow_id="literature-review", objective=f"{adapter_type} bridge"
                )
                self.assertEqual(result["status"], "completed")
                self.assertEqual(result["attempts"][0]["agent_id"], agent_id)

    def test_failed_evaluator_preserves_attempt_and_artifacts(self) -> None:
        package = _write_agent(
            self.project.agents_dir / "bad-evaluator",
            agent_id="a.bad",
            capability="research.frame_objective",
            outputs=["research.objective.v1"],
            valid_records=False,
        )
        AgentRegistry(self.project).trust("a.bad")
        result = self.run_workflow("literature-review")
        self.assertEqual(result["status"], "failed")
        attempt = result["attempts"][0]
        self.assertEqual(attempt["status"], "evaluation_failed")
        self.assertTrue(Path(attempt["workspace"]).is_dir())
        with self.project.connect() as connection:
            names = {
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM artifacts WHERE attempt_id = ?", (attempt["id"],)
                ).fetchall()
            }
        self.assertIn("bad.json", names)
        self.assertIn("request.json", names)
        self.assertTrue(package.is_dir())

    def test_invalid_agent_output_fails_durably(self) -> None:
        invalid_outputs = (
            {
                "status": "completed",
                "summary": "invalid claims",
                "records": {"research.objective.v1": {"ok": True}},
                "artifacts": {},
                "claims": {},
                "observations": [],
                "metrics": {},
                "usage": {},
            },
            {
                "status": "completed",
                "summary": "reserved artifact",
                "records": {"research.objective.v1": {"ok": True}},
                "artifacts": {"request.json": "collision"},
                "claims": [],
                "observations": [],
                "metrics": {},
                "usage": {},
            },
        )
        for index, invalid in enumerate(invalid_outputs):
            with self.subTest(index=index):
                project = Project.create(self.root / f"invalid-output-{index}", name="invalid")
                package = _write_agent(
                    project.agents_dir / "invalid",
                    agent_id="a.invalid-output",
                    capability="research.frame_objective",
                    outputs=["research.objective.v1"],
                    valid_records=True,
                )
                (package / "run.py").write_text(
                    "import json, sys\njson.load(sys.stdin)\njson.dump("
                    + repr(invalid)
                    + ", sys.stdout)\n",
                    encoding="utf-8",
                )
                registry = AgentRegistry(project)
                registry.trust("a.invalid-output")
                result = ResearchEngine(project, registry=registry).start(
                    workflow_id="literature-review", objective="invalid output"
                )
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["attempts"][0]["status"], "failed")
                self.assertIn("invalid agent output", result["attempts"][0]["error"])


class EvidenceAndMemoryTests(RuntimeTestCase):
    def test_artifacts_are_scoped_to_their_run_and_cannot_escape_it(self) -> None:
        first = ArtifactStore(self.root / "runs" / "one", self.project.db_path, run_id="one")
        second = ArtifactStore(self.root / "runs" / "two", self.project.db_path, run_id="two")
        first_artifact = first.add_text(
            stage_id="s", attempt_id="a1", name="same.txt", content="same"
        )
        second.add_text(stage_id="s", attempt_id="a2", name="same.txt", content="same")
        with self.assertRaises(ArtifactError):
            second.get(first_artifact.id)

        with self.project.connect() as connection:
            connection.execute(
                "UPDATE artifacts SET path = '../outside' WHERE id = ?", (first_artifact.id,)
            )
        with self.assertRaises(ArtifactError):
            first.content(first_artifact.id)
        self.assertTrue(any("unsafe artifact path" in item for item in first.verify()))

    def test_unresolved_claim_cannot_promote(self) -> None:
        store = ArtifactStore(self.root / "runs" / "manual", self.project.db_path, run_id="manual")
        claims = ClaimStore(self.project.db_path, store)
        claim_id = claims.propose(
            run_id="manual",
            stage_id="s",
            attempt_id="a",
            claim=CandidateClaim(
                "unsupported",
                evidence=(EvidenceRef("artifact:missing", "json:/x", "artifact"),),
            ),
        )
        with self.assertRaises(ClaimError):
            claims.promote(claim_id, evaluation_id="eval", evaluation_passed=True)

    def test_numeric_claim_resolves_to_exact_output_locator(self) -> None:
        result = self.run_workflow("data-analysis")
        store = ArtifactStore(self.project.run_dir(result["id"]), self.project.db_path, run_id=result["id"])
        claims = ClaimStore(self.project.db_path, store).list(run_id=result["id"], state="promoted")
        numeric = next(item for item in claims if item["value"] is not None)
        evidence = next(item for item in numeric["evidence"] if item["kind"] == "numeric")
        self.assertTrue(evidence["resolved"])
        self.assertTrue(store.resolve_locator(evidence["artifact_id"], evidence["locator"]))
        attempt = next(item for item in result["attempts"] if item["id"] == numeric["attempt_id"])
        self.assertTrue(attempt["agent_digest"])

    def test_writer_request_contains_only_promoted_claims_and_reverse_links(self) -> None:
        result = self.run_workflow("literature-review")
        write = next(item for item in result["attempts"] if item["stage_id"] == "write")
        store = ArtifactStore(self.project.run_dir(result["id"]), self.project.db_path, run_id=result["id"])
        request = json.loads(store.content(store.find_attempt_name(write["id"], "request.json").id))
        self.assertEqual(request["candidateClaims"], [])
        self.assertTrue(request["promotedClaims"])
        stage_result = json.loads(write["output_json"])
        record = stage_result["records"]["publication.report.v1"]
        self.assertEqual(set(record["claimIds"]), {item["id"] for item in request["promotedClaims"]})

    def test_reviewed_memory_and_evaluation_firewall(self) -> None:
        memory = ResearchMemory(self.project.db_path)
        development = memory.propose(
            run_id="r", stage_id="s", attempt_id="a",
            observation=Observation("development insight", ("visible",), data_class="development"),
        )
        evaluation = memory.propose(
            run_id="r", stage_id="s", attempt_id="a",
            observation=Observation("evaluation secret", ("hidden",), data_class="evaluation"),
        )
        self.assertEqual(memory.query("insight secret"), [])
        memory.review(development, accept=True)
        memory.review(evaluation, accept=True)
        visible = memory.query("insight secret", for_agent=True)
        self.assertEqual([item["id"] for item in visible], [development])
        complete = memory.query("secret", for_agent=False)
        self.assertEqual([item["id"] for item in complete], [evaluation])
        sanitized = _sanitize_agent_context(
            {"safe": {"dataClass": "development", "x": 1}, "heldout": {"dataClass": "evaluation", "x": 2}}
        )
        self.assertEqual(sanitized["heldout"]["reason"], "evaluation firewall")
        self.assertEqual(sanitized["safe"]["x"], 1)


class TrustIsolationAndAuditTests(RuntimeTestCase):
    def test_unusable_bubblewrap_falls_back_only_in_auto_mode(self) -> None:
        rejected = subprocess.CompletedProcess([], 1, stderr="namespace not permitted")
        with patch.dict(os.environ, {"ARA_OS_SANDBOX": "auto"}), patch(
            "adapted_research_arch.agent.shutil.which", return_value="/usr/bin/bwrap"
        ), patch("adapted_research_arch.agent.subprocess.run", return_value=rejected) as probe:
            command, backend = _sandbox_command(
                ["agent-must-not-run"], self.root, PermissionSet(process=True)
            )
        self.assertEqual(command, ["agent-must-not-run"])
        self.assertEqual(backend, "copied-workspace")
        probe.assert_called_once()
        self.assertNotIn("agent-must-not-run", probe.call_args.args[0])

        with patch.dict(os.environ, {"ARA_OS_SANDBOX": "required"}), patch(
            "adapted_research_arch.agent.shutil.which", return_value="/usr/bin/bwrap"
        ), patch("adapted_research_arch.agent.subprocess.run", return_value=rejected):
            with self.assertRaisesRegex(AgentError, "namespace not permitted"):
                _sandbox_command(["agent-must-not-run"], self.root, PermissionSet(process=True))

    def test_usable_bubblewrap_keeps_agent_inside_sandbox(self) -> None:
        accepted = subprocess.CompletedProcess([], 0, stderr="")
        with patch.dict(os.environ, {"ARA_OS_SANDBOX": "auto"}), patch(
            "adapted_research_arch.agent.shutil.which", return_value="/usr/bin/bwrap"
        ), patch("adapted_research_arch.agent.subprocess.run", return_value=accepted) as probe:
            command, backend = _sandbox_command(
                ["agent-must-not-run"], self.root, PermissionSet(process=True)
            )
        self.assertEqual(backend, "bubblewrap")
        self.assertEqual(command[0], "/usr/bin/bwrap")
        self.assertEqual(command[-1], "agent-must-not-run")
        self.assertIn("--unshare-net", command)
        self.assertLess(command.index("--tmpfs"), command.index("--bind"))
        self.assertNotIn("agent-must-not-run", probe.call_args.args[0])

    def test_sandbox_probe_timeout_fails_closed_when_required(self) -> None:
        with patch.dict(os.environ, {"ARA_OS_SANDBOX": "required"}), patch(
            "adapted_research_arch.agent.shutil.which", return_value="/usr/bin/bwrap"
        ), patch(
            "adapted_research_arch.agent.subprocess.run",
            side_effect=subprocess.TimeoutExpired("bwrap", 5),
        ):
            with self.assertRaisesRegex(AgentError, "OS sandbox required"):
                _sandbox_command(["agent-must-not-run"], self.root, PermissionSet(process=True))

    def test_doctor_does_not_report_installed_but_unusable_sandbox(self) -> None:
        with patch.dict(os.environ, {"ARA_OS_SANDBOX": "auto"}), patch(
            "adapted_research_arch.agent.shutil.which", return_value="/usr/bin/bwrap"
        ), patch(
            "adapted_research_arch.agent.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, stdout="", stderr="namespace denied"),
        ):
            result = diagnostics(self.project)
        self.assertEqual(result["osSandbox"], "copied-workspace")
        self.assertIn("declarative allowlist only", result["networkEnforcement"])

    def test_os_sandbox_can_fail_closed_when_unavailable(self) -> None:
        with patch.dict(os.environ, {"ARA_OS_SANDBOX": "required"}), patch(
            "adapted_research_arch.agent.shutil.which", return_value=None
        ):
            with self.assertRaises(AgentError):
                _sandbox_command(["true"], self.root, PermissionSet(process=True))
        with patch.dict(os.environ, {"ARA_OS_SANDBOX": "off"}):
            command, backend = _sandbox_command(
                ["true"], self.root, PermissionSet(process=True)
            )
        self.assertEqual(command, ["true"])
        self.assertEqual(backend, "copied-workspace")

    def test_changed_agent_cannot_run_under_old_trust(self) -> None:
        package = _write_agent(
            self.project.agents_dir / "custom",
            agent_id="custom.planner",
            capability="research.frame_objective",
            outputs=["research.objective.v1"],
            valid_records=True,
        )
        registry = AgentRegistry(self.project)
        registry.trust("custom.planner")
        self.assertEqual(registry.route("research.frame_objective", agent_id="custom.planner").trust_state, "trusted")
        (package / "AGENT.md").write_text("changed instructions\n", encoding="utf-8")
        changed = next(item for item in registry.discover() if item.manifest.id == "custom.planner")
        self.assertEqual(changed.trust_state, "changed")
        with self.assertRaises(RegistryError):
            registry.route("research.frame_objective", agent_id="custom.planner")

    def test_route_prefers_newest_semver_version(self) -> None:
        for directory, version in (("versioned-old", "0.9.0"), ("versioned-new", "0.10.0")):
            _write_agent(
                self.project.agents_dir / directory,
                agent_id="custom.versioned",
                capability="research.frame_objective",
                outputs=["research.objective.v1"],
                valid_records=True,
                version=version,
            )
        registry = AgentRegistry(self.project)
        registry.trust("custom.versioned", version="0.9.0")
        registry.trust("custom.versioned", version="0.10.0")
        routed = registry.route("research.frame_objective", agent_id="custom.versioned")
        self.assertEqual(routed.manifest.version, "0.10.0")

    def test_project_create_rejects_changed_policy(self) -> None:
        changed = default_policy()
        changed["budget"]["maxToolCalls"] = 1
        with self.assertRaises(ProjectError):
            Project.create(self.root, name="conformance", policy=changed)
        unchanged = Project.create(self.root, name="conformance", policy=default_policy())
        self.assertEqual(unchanged.project_id, self.project.project_id)

    def test_agent_package_symlink_escape_fails_closed(self) -> None:
        package = _write_agent(
            self.project.agents_dir / "escaped",
            agent_id="custom.escaped",
            capability="research.frame_objective",
            outputs=["research.objective.v1"],
            valid_records=True,
        )
        os.symlink("/etc/passwd", package / "outside")
        with self.assertRaises(RegistryError):
            AgentRegistry(self.project).discover()

    def test_thread_fork_records_parent_and_has_isolated_writable_state(self) -> None:
        parent = self.project.start_thread()
        child = self.project.start_thread(parent_id=parent["id"], fork_boundary="event:7")
        self.assertEqual(child["parent_id"], parent["id"])
        self.assertEqual(child["fork_boundary"], "event:7")
        parent_workspace = self.project.thread_dir(parent["id"]) / "workspace"
        child_workspace = self.project.thread_dir(child["id"]) / "workspace"
        self.assertNotEqual(parent_workspace, child_workspace)
        self.assertTrue(parent_workspace.is_dir() and child_workspace.is_dir())

    def test_event_and_artifact_tampering_is_detected(self) -> None:
        result = self.run_workflow("literature-review")
        store = ArtifactStore(self.project.run_dir(result["id"]), self.project.db_path, run_id=result["id"])
        with self.project.connect() as connection:
            row = connection.execute(
                "SELECT path FROM artifacts WHERE run_id = ? LIMIT 1", (result["id"],)
            ).fetchone()
        (self.project.run_dir(result["id"]) / row["path"]).write_bytes(b"tampered")
        self.assertFalse(verify_run(self.project, result["id"])["ok"])
        ledger_path = self.project.run_dir(result["id"]) / "events.jsonl"
        lines = ledger_path.read_text(encoding="utf-8").splitlines()
        event = json.loads(lines[0])
        event["payload"]["objective"] = "changed"
        lines[0] = json.dumps(event)
        ledger_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        with self.assertRaises(LedgerError):
            EventLedger(ledger_path, project_id=self.project.project_id, run_id=result["id"])

    def test_stage_result_tampering_is_detected(self) -> None:
        result = self.run_workflow("literature-review")
        target = self.project.run_dir(result["id"]) / "stages" / "frame.json"
        stage_result = json.loads(target.read_text(encoding="utf-8"))
        stage_result["summary"] = "tampered but valid JSON"
        target.write_text(json.dumps(stage_result), encoding="utf-8")
        report = verify_run(self.project, result["id"])
        self.assertFalse(report["ok"])
        self.assertTrue(any("stage result" in item for item in report["errors"]))

    def test_advanced_strategy_requires_matched_simple_control(self) -> None:
        contract = MetricContract("score", "maximize", "data123", 7, 60)
        baseline = StrategyResult("linear", "simple_control", 1.0, contract.digest, "art_base")
        advanced = StrategyResult("evolution", "advanced", 1.2, contract.digest, "art_advanced")
        self.assertTrue(compare_strategies(contract=contract, baseline=baseline, candidate=advanced)["promote"])
        mismatched = StrategyResult("evolution", "advanced", 2.0, "wrong", "art_other")
        with self.assertRaises(ComparisonError):
            compare_strategies(contract=contract, baseline=baseline, candidate=mismatched)


class ClientInteroperabilityTests(RuntimeTestCase):
    def test_cli_and_protocol_drive_the_same_project(self) -> None:
        from adapted_research_arch.protocol import ProtocolServer

        server = ProtocolServer(self.root)
        initialized = server.handle(
            {"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "test"}, "protocolVersions": ["1.0"]}}
        )
        self.assertEqual(initialized["result"]["protocolVersion"], "1.0")
        started = server.handle(
            {
                "id": 2,
                "method": "workflow/start",
                "params": {"workflowId": "literature-review", "objective": "two clients"},
            }
        )["result"]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = cli_main(["--project", str(self.root), "run", "status", started["id"]])
        self.assertEqual(exit_code, 0)
        cli_state = json.loads(output.getvalue())
        self.assertEqual(cli_state["id"], started["id"])
        self.assertEqual(cli_state["lastSequence"], started["lastSequence"])

    def test_protocol_requires_initialization_and_supports_event_cursor(self) -> None:
        from adapted_research_arch.protocol import ProtocolServer

        server = ProtocolServer(self.root)
        rejected = server.handle({"id": 1, "method": "project/read", "params": {}})
        self.assertEqual(rejected["error"]["code"], "not_initialized")
        server.handle({"id": 2, "method": "initialize", "params": {"protocolVersions": ["1.0"]}})
        result = server.handle(
            {"id": 3, "method": "workflow/start", "params": {"workflowId": "literature-review", "objective": "events"}}
        )["result"]
        events = server.handle(
            {"id": 4, "method": "event/list", "params": {"runId": result["id"], "afterSequence": 2}}
        )["result"]
        self.assertTrue(events)
        self.assertTrue(all(item["sequence"] > 2 for item in events))

    def test_event_listing_requires_an_existing_run(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = cli_main(["--project", str(self.root), "run", "events", "run_missing"])
        self.assertEqual(exit_code, 1)
        self.assertIn("run not found", stderr.getvalue())

        server = ProtocolServer(self.root)
        server.handle({"id": 1, "method": "initialize", "params": {"protocolVersions": ["1.0"]}})
        response = server.handle({"id": 2, "method": "event/list", "params": {"runId": "run_missing"}})
        self.assertIn("run not found", response["error"]["message"])
        self.assertFalse((self.project.runs_dir / "run_missing").exists())

    def test_stdio_protocol_survives_non_object_json(self) -> None:
        output = io.StringIO()
        serve_stdio(
            ProtocolServer(self.root),
            input_stream=io.StringIO(
                '[]\n{"id": 1, "method": "initialize", '
                '"params": {"protocolVersions": ["1.0"]}}\n'
            ),
            output_stream=output,
        )
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(responses[0]["error"]["code"], "invalid_request")
        self.assertEqual(responses[1]["result"]["protocolVersion"], "1.0")


def _write_agent(
    root: Path,
    *,
    agent_id: str,
    capability: str,
    outputs: list[str],
    valid_records: bool,
    usage: dict[str, float] | None = None,
    adapter_type: str = "command",
    risk: str = "R0",
    allow_implicit: bool = True,
    version: str = "0.1.0",
) -> Path:
    root.mkdir(parents=True)
    script = root / "run.py"
    records = "{schema: {'ok': True} for schema in request['stage']['outputs']}" if valid_records else "{}"
    script.write_text(
        "import json, sys\n"
        "request=json.load(sys.stdin)\n"
        f"records={records}\n"
        "json.dump({'status':'completed','summary':'custom','records':records,"
        "'artifacts':{'bad.json':'{\\\"value\\\": 1}'},'claims':[],"
        "'observations':[],'metrics':{},'usage':" + repr(usage or {}) + "},sys.stdout)\n",
        encoding="utf-8",
    )
    adapter = {"type": "command", "command": [sys.executable, "run.py"]}
    if adapter_type == "model":
        adapter = {
            "type": "model",
            "provider": "fixture",
            "model": "fixture-v1",
            "command": [sys.executable, "run.py"],
        }
    elif adapter_type == "remote_tool":
        adapter = {
            "type": "remote_tool",
            "server": "fixture",
            "tool": "run",
            "command": [sys.executable, "run.py"],
        }
    manifest = {
        "schemaVersion": "1.0",
        "id": agent_id,
        "version": version,
        "name": agent_id,
        "description": "test agent",
        "maturity": "stable",
        "capabilities": [capability],
        "inputs": [],
        "outputs": outputs,
        "adapter": adapter,
        "risk": risk,
        "permissions": {
            "filesystem": {"read": [], "write": ["attempt:artifacts"]},
            "network": {"mode": "disabled", "hosts": []},
            "process": True,
            "scheduler": False,
            "gpu": False,
            "externalWrite": False,
            "secretHandles": [],
        },
        "tools": [],
        "evaluators": ["schema.valid"],
        "budgets": {"maxWallSeconds": 30, "maxToolCalls": 0, "maxSources": 0, "maxCostUsd": 0},
        "routing": {"allowImplicit": allow_implicit},
    }
    (root / "agent.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (root / "AGENT.md").write_text("test instructions\n", encoding="utf-8")
    return root


if __name__ == "__main__":
    unittest.main()
