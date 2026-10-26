import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

from adapted_research_arch import Project, ResearchEngine, verify_run
from adapted_research_arch.engine import EngineError
from adapted_research_arch.events import EventLedger
from adapted_research_arch.research.integrity import audit_stage
from adapted_research_arch.research.measurement import ProtocolRunner, RunSpec
from adapted_research_arch.research.stages import StageId


SOURCE = Path(__file__).resolve().parents[1] / "src"
FIXTURE = '''
import json, sys
from pathlib import Path
sys.path.insert(0, SOURCE)
from adapted_research_arch.research.bridge import measurement_response
request = json.load(sys.stdin)
assert all('artifacts' not in value for value in request['dependencyResults'].values())
contract = request['researchContract']
semantic = contract['stage']['id']
native = semantic.lower()
if contract['role'] == 'reviewer':
    cards = {card['card_id']: {'status': 'MET', 'reason': 'fixture inspection', 'location': 'text'} for card in contract['cards']}
    if FAULT == 'gap' and semantic == 'S3':
        cards['S3-C1']['status'] = 'GAP'
    if FAULT == 'malformed-review':
        cards['S1-C1']['reason'] = 123
    if FAULT == 'missing-card':
        cards.pop(next(iter(cards)))
    record = {'stage': semantic, 'reviewedAttemptId': request['dependencyResults'][native]['attemptId'], 'cards': cards, 'issues': [], 'reviewDecision': 'pass'}
    result = {'status': 'completed', 'summary': 'fixture review', 'records': {'research.review.v1': record}, 'artifacts': {}, 'claims': [], 'metrics': {}}
elif native == 's6':
    result = measurement_response(request, Path.cwd())
    if FAULT == 'fabricate':
        result['records']['research.stage.v1']['text'] = 'We solved 90% of cases.'
    if FAULT == 'log-tamper' and contract['evidenceMode'] == 'MEASURED':
        result['artifacts']['artifacts/poc_runs/R-001.log'] = 'different observation'
    if FAULT == 'summary-tamper' and contract['evidenceMode'] == 'MEASURED':
        result['records']['research.stage.v1']['measurementSummary']['overall']['pass_count'] = 999
    if FAULT == 'drift' and contract['evidenceMode'] == 'MEASURED':
        result['records']['research.stage.v1']['protocol']['runs'][0]['timeout_s'] = 123
else:
    record = {'stage': semantic, 'text': 'Planned protocol N=1. No measured results. [TBD-MEASURE:poc]'}
    if native == 's2':
        record['problemContract'] = {'researchQuestion':'Does the controlled task finish?', 'unit':'one invocation', 'scope':'offline fixture', 'primaryOutcome':'exit status', 'comparator':'fixed command'}
    elif native != 's1':
        record['problemContract'] = contract['problemContract']
    if FAULT == 'scope' and native == 's4':
        record['problemContract'] = {**record['problemContract'], 'scope': 'silently expanded domain'}
    if native == 's5':
        command = [sys.executable, '-c', "print('controlled observation')"]
        if FAULT == 'missing-tool':
            command = ['instrument-that-is-absent-test-7339']
        if FAULT == 'negative':
            command = [sys.executable, '-c', 'raise SystemExit(3)']
        record['protocol'] = {'runs': [{'run_id': 'R-001', 'command': command, 'timeout_s': 10}]}
    artifacts = {}
    if native == 's8':
        record['claimIds'] = [row['id'] for row in request['promotedClaims']]
        artifacts['paper.md'] = record['text']
    result = {'status': 'completed', 'summary': 'fixture build', 'records': {'research.stage.v1': record}, 'artifacts': artifacts, 'claims': [], 'metrics': {}}
json.dump(result, sys.stdout)
'''


class ResearchWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Project.create(self.temp.name, name="research integration")

    def agents(self, fault="", same_identity=False, model_measurement=False):
        base = json.loads((SOURCE / "adapted_research_arch/builtin_agents/research-planner/agent.json").read_text())
        for name, capabilities, schema in [
            ("builder", ["research.build_stage", "research.measure"], "research.stage.v1"),
            ("reviewer", ["research.review_stage"], "research.review.v1"),
        ]:
            if same_identity and name == "reviewer":
                continue
            root = self.project.agents_dir / name
            root.mkdir()
            script = f"SOURCE={str(SOURCE)!r}\nFAULT={fault!r}\n" + FIXTURE
            (root / "run.py").write_text(script)
            if same_identity:
                capabilities.append("research.review_stage")
            adapter = {"type": "command", "command": [sys.executable, "run.py"]}
            if model_measurement and name == "builder":
                adapter.update(type="model", provider="fixture", model="fixture")
            manifest = {
                **base, "id": "test.research." + name, "capabilities": capabilities,
                "outputs": [schema, "research.review.v1"], "inputs": [],
                "adapter": adapter, "risk": "R0", "routing": {"allowImplicit": True},
            }
            (root / "agent.json").write_text(json.dumps(manifest))
            (root / "AGENT.md").write_text("Offline integration fixture, not a scientific result.\n")
        engine = ResearchEngine(self.project)
        for package in engine.registry.discover():
            if package.manifest.id.startswith("test.research."):
                engine.registry.trust(package.manifest.id)
        return engine

    def run_research(self, mode="SIMULATED", **kwargs):
        return self.agents(**kwargs).start(workflow_id="idea-to-paper", objective="controlled pipeline test", evidence_mode=mode)

    def test_simulated_workflow_uses_native_ledger_and_six_card_reviews(self):
        result = self.run_research()
        self.assertEqual(result["status"], "completed", result["attempts"][-1]["error"])
        self.assertEqual(len(result["completedStages"]), 16)
        self.assertTrue(verify_run(self.project, result["id"])["ok"])
        created = next(EventLedger(self.project.run_dir(result["id"]) / "events.jsonl", project_id=self.project.project_id, run_id=result["id"]).events_of_type("workflow/created"))
        self.assertEqual(created["payload"]["evidenceMode"], "SIMULATED")

    def test_measured_workflow_executes_and_recomputes_one_real_observation(self):
        result = self.run_research("MEASURED")
        self.assertEqual(result["status"], "completed", result["attempts"][-1]["error"])
        evidence = json.loads((self.project.run_dir(result["id"]) / "stages/s6.json").read_text())
        summary = evidence["records"]["research.stage.v1"]["measurementSummary"]
        self.assertEqual(summary["overall"]["pass_count"], 1)
        self.assertEqual(summary["overall"]["n_valid"], 1)
        self.assertIn("artifacts/poc_runs/R-001.log", evidence["artifactIds"])
        self.assertTrue(verify_run(self.project, result["id"])["ok"])

    def test_fabrication_blocks_simulated_workflow_before_review(self):
        result = self.run_research(fault="fabricate")
        self.assertEqual(result["status"], "failed", result["attempts"][-1]["error"])
        self.assertNotIn("s6", result["completedStages"])
        self.assertIn("FABRICATED_MEASUREMENT", result["attempts"][-1]["error"])

    def test_missing_instrument_is_invalid_evidence_not_negative_result(self):
        result = self.run_research("MEASURED", fault="missing-tool")
        self.assertEqual(result["status"], "failed", result["attempts"][-1]["error"])
        self.assertIn("no valid measurement", result["attempts"][-1]["error"])
        self.assertNotIn("s6_review", result["completedStages"])

    def test_real_negative_observation_keeps_its_denominator(self):
        result = self.run_research("MEASURED", fault="negative")
        self.assertEqual(result["status"], "completed", result["attempts"][-1]["error"])
        self.assertEqual(result["outcome"], "negative")
        evidence = json.loads((self.project.run_dir(result["id"]) / "stages/s6.json").read_text())
        overall = evidence["records"]["research.stage.v1"]["measurementSummary"]["overall"]
        self.assertEqual(overall["status_counts"], {"FAIL": 1})
        self.assertEqual(overall["n_valid"], 1)
        self.assertEqual(overall["pass_rate_over_all"], 0)

    def test_central_question_and_scope_cannot_drift_after_s2(self):
        result = self.run_research(fault="scope")
        self.assertEqual(result["status"], "failed")
        self.assertIn("frozen S2 research question", result["attempts"][-1]["error"])
        self.assertNotIn("s4", result["completedStages"])

    def test_protocol_change_cannot_pass_as_frozen_measurement(self):
        result = self.run_research("MEASURED", fault="drift")
        self.assertEqual(result["status"], "failed", result["attempts"][-1]["error"])
        self.assertIn("changed the frozen S5", result["attempts"][-1]["error"])

    def test_measured_log_tampering_is_rejected(self):
        result = self.run_research("MEASURED", fault="log-tamper")
        self.assertEqual(result["status"], "failed")
        self.assertIn("log digest mismatch", result["attempts"][-1]["error"])

    def test_measured_summary_must_be_recomputed_from_records(self):
        result = self.run_research("MEASURED", fault="summary-tamper")
        self.assertEqual(result["status"], "failed")
        self.assertIn("not derived", result["attempts"][-1]["error"])

    def test_model_adapter_cannot_certify_measurements(self):
        result = self.run_research("MEASURED", model_measurement=True)
        self.assertEqual(result["status"], "failed", result["attempts"][-1]["error"])
        self.assertIn("trusted command executor", result["attempts"][-1]["error"])

    def test_failed_card_blocks_despite_pass_verdict(self):
        result = self.run_research(fault="gap")
        self.assertEqual(result["status"], "failed", result["attempts"][-1]["error"])
        self.assertNotIn("s4", result["completedStages"])

    def test_malformed_review_is_a_durable_failure_not_a_controller_crash(self):
        result = self.run_research(fault="malformed-review")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["attempts"][-1]["status"], "evaluation_failed")
        self.assertIn("reason and evidence location", result["attempts"][-1]["error"])

    def test_omitted_cards_cannot_pass_by_vacuous_all(self):
        result = self.run_research(fault="missing-card")
        self.assertEqual(result["status"], "failed", result["attempts"][-1]["error"])
        self.assertEqual(result["completedStages"], ["s1"])

    def test_builder_cannot_review_its_own_attempt(self):
        result = self.run_research(same_identity=True)
        self.assertEqual(result["status"], "failed", result["attempts"][-1]["error"])
        self.assertIn("distinct trusted agent packages", result["attempts"][-1]["error"])

    def test_evidence_mode_is_immutable_on_idempotent_start(self):
        engine = ResearchEngine(self.project)
        kwargs = dict(workflow_id="idea-to-paper", objective="pinned mode", idempotency_key="mode", execute=False)
        engine.start(**kwargs)
        with self.assertRaisesRegex(EngineError, "evidence mode"):
            engine.start(**kwargs, evidence_mode="MEASURED")

    def test_outside_file_is_not_research_evidence(self):
        with tempfile.TemporaryDirectory() as outside:
            path = Path(outside) / "outside.log"
            path.write_text("unrelated file")
            findings = audit_stage(StageId.S6, f"Observed evidence `{path}`", self.project.workspace_dir, {}, evidence_mode="MEASURED")
        self.assertIn("ARTIFACT_MISSING", [f.check for f in findings])

    def test_unknown_evidence_mode_fails_closed(self):
        with self.assertRaises(ValueError):
            audit_stage(StageId.S6, "90% success", self.project.workspace_dir, {}, evidence_mode="UNKNOWN")

    def test_runner_cannot_overwrite_or_escape_measurement_history(self):
        runner = ProtocolRunner(self.project.workspace_dir)
        spec = RunSpec("once", [sys.executable, "-c", "print('first')"])
        record = runner.run_one(spec)
        before = (runner.artifacts_dir / "once.log").read_bytes()
        self.assertEqual(record.stdout_sha256, hashlib.sha256(before).hexdigest())
        with self.assertRaises(FileExistsError):
            runner.run_one(spec)
        self.assertEqual((runner.artifacts_dir / "once.log").read_bytes(), before)
        with self.assertRaises(ValueError):
            RunSpec("../escape", ["true"])
        with self.assertRaises(ValueError):
            ProtocolRunner(self.project.workspace_dir, "../escape")
        with self.assertRaises(ValueError):
            runner.run_all([spec, spec])

    def test_declared_missing_input_never_executes_command(self):
        spec = RunSpec("missing-input", [sys.executable, "-c", "print('should not run')"], inputs=["absent.txt"])
        runner = ProtocolRunner(self.project.workspace_dir)
        record = runner.run_one(spec)
        self.assertEqual(record.status, "ERROR")
        self.assertEqual((runner.artifacts_dir / "missing-input.log").read_text(), "")


if __name__ == "__main__":
    unittest.main()
