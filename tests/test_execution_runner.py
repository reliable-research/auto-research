"""Runner tests: it must measure honestly, and never invent what it did not observe."""

import json
import tempfile
from pathlib import Path

import pytest

from autoresearch.execution.runner import (
    STATUS_ERROR,
    STATUS_FAIL,
    STATUS_PASS,
    STATUS_TIMEOUT,
    STATUS_TOOL_MISSING,
    ProtocolRunner,
    RunSpec,
    environment_fingerprint,
    specs_from_manifest,
    summarize,
)
from autoresearch.workflow.integrity import audit_stage
from autoresearch.workflow.stages import StageId


@pytest.fixture
def workspace():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


def _py(code: str):
    import sys
    return [sys.executable, "-c", code]


# --------------------------------------------------------------------------
# Execution outcomes
# --------------------------------------------------------------------------

def test_successful_run_is_recorded(workspace):
    r = ProtocolRunner(workspace).run_one(RunSpec("R-001", _py("print('UNSAT')")))
    assert r.status == STATUS_PASS
    assert r.exit_code == 0
    assert r.wall_time_s > 0
    assert (workspace / r.stdout_path).read_text().strip() == "UNSAT"


def test_failing_run_is_fail_not_error(workspace):
    r = ProtocolRunner(workspace).run_one(RunSpec("R-002", _py("raise SystemExit(3)")))
    assert r.status == STATUS_FAIL
    assert r.exit_code == 3


def test_timeout_is_recorded_as_timeout(workspace):
    r = ProtocolRunner(workspace).run_one(
        RunSpec("R-003", _py("import time; time.sleep(5)"), timeout_s=0.4)
    )
    assert r.status == STATUS_TIMEOUT
    assert "timeout" in r.note.lower()


def test_missing_tool_is_not_a_failed_experiment(workspace):
    """A missing binary must never read as evidence against the hypothesis."""
    r = ProtocolRunner(workspace).run_one(RunSpec("R-004", ["definitely-not-a-real-binary-xyz"]))
    assert r.status == STATUS_TOOL_MISSING
    assert r.status != STATUS_FAIL
    assert "not found" in r.note


def test_empty_command_is_an_error(workspace):
    r = ProtocolRunner(workspace).run_one(RunSpec("R-005", []))
    assert r.status == STATUS_ERROR


def test_invalid_runs_report_no_duration(workspace):
    """A run that never happened must not contribute a timing to any average."""
    r = ProtocolRunner(workspace).run_one(RunSpec("R-006", ["definitely-not-a-real-binary-xyz"]))
    assert r.wall_time_s == 0.0


# --------------------------------------------------------------------------
# Provenance
# --------------------------------------------------------------------------

def test_input_hashes_tie_result_to_input(workspace):
    (workspace / "prog.c").write_text("int main(){return 0;}")
    r = ProtocolRunner(workspace).run_one(RunSpec("R-007", _py("pass"), inputs=["prog.c"]))
    assert len(r.input_hashes["prog.c"]) == 64


def test_fingerprint_reports_absent_git_as_none_not_a_fake_hash(workspace):
    """The old pipeline invented a9f4c2b98e... here. None is the correct answer."""
    fp = environment_fingerprint(workspace, tools=["definitely-not-a-real-binary-xyz"])
    assert fp["git_commit"] is None
    assert fp["tool_versions"]["definitely-not-a-real-binary-xyz"] is None
    assert fp["python"]


def test_manifest_and_results_are_written(workspace):
    runner = ProtocolRunner(workspace)
    manifest = runner.run_all([
        RunSpec("R-101", _py("pass"), group="A"),
        RunSpec("R-102", _py("raise SystemExit(1)"), group="A"),
    ])
    assert manifest["run_count"] == 2
    assert (workspace / "artifacts/poc_runs/manifest.json").exists()
    results = json.loads((workspace / "artifacts/poc_runs/results.json").read_text())
    assert results["overall"]["pass_count"] == 1


# --------------------------------------------------------------------------
# Summary arithmetic
# --------------------------------------------------------------------------

def test_summary_separates_invalid_runs_from_failures(workspace):
    runner = ProtocolRunner(workspace)
    records = [
        runner.run_one(RunSpec("R-201", _py("pass"), group="A")),
        runner.run_one(RunSpec("R-202", _py("raise SystemExit(1)"), group="A")),
        runner.run_one(RunSpec("R-203", ["definitely-not-a-real-binary-xyz"], group="A")),
    ]
    s = summarize(records)["overall"]
    assert s["n"] == 3 and s["n_valid"] == 2 and s["n_invalid"] == 1
    # 1 of 2 readings passed, but only 1 of 3 runs were attempted successfully.
    assert s["pass_rate_over_valid"] == 0.5
    assert round(s["pass_rate_over_all"], 3) == 0.333


def test_summary_groups_are_reported_separately(workspace):
    runner = ProtocolRunner(workspace)
    records = [
        runner.run_one(RunSpec("R-301", _py("pass"), group="LIA")),
        runner.run_one(RunSpec("R-302", _py("raise SystemExit(1)"), group="NIA")),
    ]
    by_group = summarize(records)["by_group"]
    assert by_group["LIA"]["pass_count"] == 1
    assert by_group["NIA"]["pass_count"] == 0


def test_cost_stat_covers_failed_runs_but_not_absent_instruments(workspace):
    """A refuted property still times the query; a missing binary times nothing.

    The PASS-only ``wall_time_s`` cannot express how expensive a verification
    query was when every run refutes, which is the normal case below the
    completeness threshold. ``wall_time_s_over_valid`` reports that cost over
    the explicitly named ``n_valid`` denominator.
    """
    runner = ProtocolRunner(workspace)
    records = [
        runner.run_one(RunSpec("R-401", _py("raise SystemExit(1)"), group="A")),
        runner.run_one(RunSpec("R-402", _py("raise SystemExit(1)"), group="A")),
        runner.run_one(RunSpec("R-403", ["definitely-not-a-real-binary-xyz"], group="A")),
    ]
    s = summarize(records)["overall"]
    # No run passed, so the PASS-only statistic is correctly undefined...
    assert s["pass_count"] == 0
    assert s["wall_time_s"] is None
    # ...but the two real readings still have a measured cost.
    assert s["n_valid"] == 2
    cost = s["wall_time_s_over_valid"]
    assert cost is not None and cost["mean"] > 0
    # The absent instrument contributed no 0.0 reading that would drag the mean down.
    assert cost["min"] > 0


def test_summary_is_marked_as_derived():
    assert "not authored" in summarize([])["derivation"]


# --------------------------------------------------------------------------
# The loop closes: real runs satisfy the integrity audit
# --------------------------------------------------------------------------

def test_real_artifacts_clear_the_integrity_audit(workspace):
    """An S6 citing genuinely produced logs must stop triggering ARTIFACT_MISSING."""
    runner = ProtocolRunner(workspace)
    runner.run_all([RunSpec("R-001", _py("print('UNSAT')"), group="A")])

    s6_text = (
        "| Run ID | 状态 | 日志 |\n"
        "| R-001 | PASS | `artifacts/poc_runs/R-001.log` |\n"
        "汇总见 `artifacts/poc_runs/results.json`。通过 1/1。"
    )
    findings = audit_stage(StageId.S6, s6_text, workspace, {}, evidence_mode="MEASURED")
    assert [f.check for f in findings] == []


def test_fabricated_artifacts_still_fail_after_a_real_run(workspace):
    """Producing some real logs must not launder a citation to one that never ran."""
    ProtocolRunner(workspace).run_all([RunSpec("R-001", _py("pass"))])
    s6_text = "| R-999 | PASS | `artifacts/poc_runs/R-999.log` |"
    findings = audit_stage(StageId.S6, s6_text, workspace, {}, evidence_mode="MEASURED")
    assert "ARTIFACT_MISSING" in {f.check for f in findings}


# --------------------------------------------------------------------------
# Protocol as data
# --------------------------------------------------------------------------

def test_specs_load_from_manifest(workspace):
    spec_file = workspace / "protocol.json"
    spec_file.write_text(json.dumps({
        "defaults": {"timeout_s": 30, "group": "A"},
        "runs": [
            {"run_id": "R-001", "command": ["echo", "hi"]},
            {"command": ["echo", "ho"], "group": "B", "timeout_s": 5},
        ],
    }))
    specs = specs_from_manifest(spec_file)
    assert [s.run_id for s in specs] == ["R-001", "R-002"]
    assert specs[0].timeout_s == 30 and specs[0].group == "A"
    assert specs[1].timeout_s == 5 and specs[1].group == "B"
