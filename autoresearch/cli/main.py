"""Command-line interface (CLI) for AutoResearch Codeless."""

import sys
import argparse
from pathlib import Path
from typing import Optional

from autoresearch.config import Config, DEFAULT_EVIDENCE_MODE, DEFAULT_MODEL, CONTRIBUTION_TYPES, EVIDENCE_MODES
from autoresearch.llm.credentials import AgyCredentialMapper
from autoresearch.llm.agy_client import AgyGeminiClient
from autoresearch.workflow.stages import StageId, STAGES, STAGE_ORDER
from autoresearch.workflow.cards import CARDS, get_cards_for_stage
from autoresearch.workflow.state import ProjectState
from autoresearch.workflow.integrity import audit_stage, extract_stage_evidence
from autoresearch.execution.runner import (
    ProtocolRunner,
    specs_from_manifest,
)
from autoresearch.agents.coordinator import WorkflowOrchestrator
from autoresearch.utils.logger import (
    print_banner,
    print_info,
    print_success,
    print_warning,
    print_error,
    print_table,
)


def cmd_doctor(args):
    """Diagnose environment, agy binary, authentication token, and Gemini connectivity."""
    print_banner("AutoResearch System Health Check (Doctor)", "Validating agy & Gemini mapping")
    
    mapper = AgyCredentialMapper()
    status = mapper.check_status()

    headers = ["Component", "Status", "Details"]
    rows = []

    # 1. Binary check
    if status.agy_binary:
        rows.append(["agy CLI Binary", "FOUND", status.agy_binary])
    else:
        rows.append(["agy CLI Binary", "MISSING", "Not found in ~/.local/bin or PATH"])

    # 2. Token check
    if status.is_valid:
        rows.append(["OAuth Credentials", "VALID", f"Token: {status.token_preview} (method: {status.auth_method})"])
    else:
        rows.append(["OAuth Credentials", "INVALID", status.error_message or "Token error"])

    # 3. Connectivity test
    if status.agy_binary and status.is_valid:
        print_info("Testing Gemini model response via agy...")
        client = AgyGeminiClient(agy_binary=status.agy_binary, model=args.model or "gemini-3.8-flash-low")
        is_healthy = client.health_check()
        if is_healthy:
            rows.append(["Gemini LLM Test", "PASSED", f"Successfully reached {client.default_model} via agy"])
        else:
            rows.append(["Gemini LLM Test", "FAILED", "Did not receive valid ping response"])
    else:
        rows.append(["Gemini LLM Test", "SKIPPED", "Prerequisites failed"])

    print_table(headers, rows, title="System Diagnostics")
    if status.is_valid:
        print_success("All system checks passed! Ready to run AutoResearch workflows.")
    else:
        print_error("Please check the errors above before running research pipelines.")


def cmd_stages(args):
    """List all 8 stages and 48 review cards."""
    print_banner("Idea-to-Paper Codeless Workflow v4 Specifications", "8 Stages / 48 Review Cards")
    for s_id in STAGE_ORDER:
        st = STAGES[s_id]
        print(f"\n[{st.id.value}] {st.name}")
        print(f"  Goal: {st.goal}")
        cards = get_cards_for_stage(s_id)
        card_list = ", ".join([f"{c.card_id} ({c.name.split(' ')[0]})" for c in cards])
        print(f"  Cards: {card_list}")


def cmd_init(args):
    """Initialize a new research project."""
    project_name = args.project_name
    topic = args.topic or "Autonomous Software Engineering via LLMs"
    archetype = args.archetype or "方法 (Method)"

    print_banner(f"Initializing Research Project: {project_name}")
    orchestrator = WorkflowOrchestrator(
        project_name=project_name,
        topic=topic,
        contribution_type=archetype,
    )
    print_success(f"Project workspace initialized at: {orchestrator.workspace}")
    print_info(f"Topic: {topic}")
    print_info(f"Archetype: {archetype}")
    print_info("Generated files: 00_T0, 01_T1, 02_T2, 03_T3, 04_T4, 05_T5, project_state.json")
    print_info(f"To start stage S1, run: autoresearch step {project_name}")


def cmd_step(args):
    """Run one step (Builder -> Critic -> Controller) for the current stage."""
    project_name = args.project_name
    cfg = Config(model=args.model or DEFAULT_MODEL, evidence_mode=args.evidence_mode,
                 reference_material_path=args.reference)
    orchestrator = WorkflowOrchestrator(project_name=project_name, config=cfg)
    orchestrator.execute_current_stage_step()


def cmd_run(args):
    """Run the workflow pipeline across stages."""
    project_name = args.project_name
    cfg = Config(model=args.model or DEFAULT_MODEL, evidence_mode=args.evidence_mode,
                 reference_material_path=args.reference)
    orchestrator = WorkflowOrchestrator(project_name=project_name, config=cfg)

    start_stage = StageId(args.stage) if args.stage else None
    stop_stage = StageId(args.until) if args.until else None

    orchestrator.run_pipeline(start_stage=start_stage, stop_stage=stop_stage)


def cmd_measure(args):
    """Execute a declared protocol for real, producing auditable artifacts.

    This is the only legitimate source of MEASURED-mode numbers. It writes
    artifacts/poc_runs/<run_id>.{out,err}, manifest.json and results.json, whose
    figures S6 must quote rather than restate.
    """
    project_name = args.project_name
    workspace = Config().workspace_dir / project_name
    if not workspace.exists():
        print_error(f"Project '{project_name}' not found at {workspace}")
        sys.exit(1)

    protocol = Path(args.protocol) if args.protocol else workspace / "protocol.json"
    if not protocol.exists():
        print_error(f"Protocol manifest not found: {protocol}")
        print_info(
            'Expected shape: {"defaults": {"timeout_s": 60}, '
            '"runs": [{"run_id": "R-001", "command": ["cbmc", "..."], "group": "linear"}]}'
        )
        sys.exit(1)

    try:
        specs = specs_from_manifest(protocol)
    except (KeyError, ValueError) as exc:
        print_error(f"Malformed protocol manifest {protocol}: {exc}")
        sys.exit(1)

    if not specs:
        print_error(f"Protocol manifest {protocol} declares no runs.")
        sys.exit(1)

    print_banner(
        f"Protocol Execution: {project_name}",
        f"{len(specs)} run(s) from {protocol.name} | real measurement, real artifacts",
    )

    runner = ProtocolRunner(workspace)
    tools = args.tool or []

    def _progress(record):
        marker = {"PASS": "✔", "FAIL": "✖"}.get(record.status, "⚠")
        print_info(
            f"  {marker} {record.run_id} [{record.group}] {record.status} "
            f"({record.wall_time_s:.2f}s)"
        )

    manifest = runner.run_all(specs, tools=tools, progress=_progress)
    summary = manifest["summary"]
    overall = summary["overall"]

    def _row(name, st):
        counts = st.get("status_counts", {})
        cost = st.get("wall_time_s_over_valid") or {}
        return [
            name,
            str(st.get("n", 0)),
            str(st.get("pass_count", 0)),
            str(counts.get("FAIL", 0)),
            # Shown as its own column: a TIMEOUT is a reading (the budget was
            # exhausted), so folding it into FAIL would report "too expensive to
            # decide" as "decided negative".
            str(counts.get("TIMEOUT", 0)),
            # n_valid is n minus this, so only the exceptional count is shown.
            str(st.get("n_invalid", 0)),
            str(st.get("pass_rate_over_valid")),
            f"{cost['median']:.3f}" if cost else "-",
            f"{cost['max']:.3f}" if cost else "-",
        ]

    print_table(
        ["Group", "n", "PASS", "FAIL", "TMO", "n/r",
         "rate/valid", "med s", "max s"],
        [_row(g, st) for g, st in sorted(summary["by_group"].items())]
        + [_row("OVERALL", overall)],
        title="Measured Results (derived from run records, not authored)",
    )

    artifacts = workspace / runner.artifacts_subdir
    print_success(f"Artifacts written to {artifacts}")
    print_info("Quote artifacts/poc_runs/results.json verbatim in S6. Do not restate it in prose.")

    invalid = overall.get("n_invalid", 0)
    if invalid:
        print_warning(
            f"{invalid} run(s) produced no reading (TOOL_MISSING/ERROR). "
            "These are harness outcomes, not scientific negatives -- fix them before quoting rates. "
            "TIMEOUT is not among them: an exhausted budget is a real observation."
        )
    print_info(f"Next: autoresearch verify {project_name} --evidence-mode MEASURED")


def cmd_verify(args):
    """Re-run the deterministic integrity audit over a project's stage outputs.

    Works on any workspace, including runs produced before the audit existed, so
    an existing manuscript can be checked without regenerating it.
    """
    project_name = args.project_name
    workspace = Config().workspace_dir / project_name
    if not workspace.exists():
        print_error(f"Project '{project_name}' not found at {workspace}")
        return

    # Audit under the mode the project was PRODUCED under, unless overridden.
    # Hardcoding MEASURED here made `verify` report findings that the run itself
    # was never required to satisfy, so the two sides disagreed on identical files.
    mode = args.evidence_mode
    mode_source = "--evidence-mode"
    if mode is None:
        try:
            mode = ProjectState.load(workspace).evidence_mode
            mode_source = "recorded in project_state.json"
        except (FileNotFoundError, KeyError, ValueError):
            mode = DEFAULT_EVIDENCE_MODE
            mode_source = "default (project records no mode)"

    print_banner(
        f"Integrity Audit: {project_name}",
        f"evidence_mode={mode} ({mode_source}) | deterministic checks, no LLM involved",
    )

    ledger = {}
    frozen = None
    total = 0
    rows = []

    for stage_id in STAGE_ORDER:
        stage_file = workspace / f"stage_output_{stage_id.value}.md"
        if not stage_file.exists():
            continue
        text = stage_file.read_text(encoding="utf-8")

        findings = audit_stage(
            stage_id=stage_id,
            stage_output=text,
            workspace=workspace,
            prior_evidence=ledger,
            frozen_protocol=frozen,
            evidence_mode=mode,
        )
        evidence = extract_stage_evidence(stage_id, text)
        ledger[stage_id.value] = evidence.to_dict()
        if stage_id == StageId.S5:
            frozen = {
                "primary_cohort": evidence.primary_cohort,
                "timeouts": evidence.timeouts,
                "temperatures": evidence.temperatures,
                "repeats": evidence.repeats,
            }

        total += len(findings)
        for f in findings:
            rows.append([stage_id.value, f.check, f.card_id, f.problem[:70]])

    print_table(
        ["Stage", "Check", "Card", "Problem"],
        rows or [["-", "-", "-", "no deterministic violations found"]],
        title="Machine-Verified Findings",
    )

    print_info("Registered facts per stage:")
    print_table(
        ["Stage", "Primary N", "Denominators", "Timeouts (s)", "Claims", "TBD"],
        [
            [
                k,
                str(v.get("primary_cohort") or "-"),
                str(v.get("denominators") or "-"),
                str(v.get("timeouts") or "-"),
                str(v.get("claim_count", 0)),
                str(v.get("tbd_count", 0)),
            ]
            for k, v in sorted(ledger.items())
        ],
        title="Evidence Ledger",
    )

    if total:
        print_error(
            f"{total} BLOCKING integrity violation(s). "
            "Numbers in this project are not admissible as evidence."
        )
        sys.exit(1)
    print_success("No deterministic integrity violations found.")


def cmd_status(args):
    """Show current stage, card check statuses, and issues for a project."""
    project_name = args.project_name
    workspace = Config().workspace_dir / project_name
    if not workspace.exists():
        print_error(f"Project '{project_name}' not found at {workspace}")
        return

    state = ProjectState.load(workspace)
    print_banner(f"Project Status: {state.name}", f"Stage: {state.current_stage.value} | Round: {state.current_round}")

    print_info(f"Topic: {state.topic}")
    print_info(f"Contribution Archetype: {state.contribution_type}")
    print_info(f"Current Stage: {state.current_stage.value} - {STAGES[state.current_stage].name}")
    print_info(f"Active Issues: {len(state.active_issues)}")
    print_info(f"Resolved Issues: {len(state.resolved_issues)}")

    if state.active_issues:
        headers = ["Issue ID", "Card", "Severity", "Owner Stage", "Problem"]
        rows = [
            [iss.get("issue_id"), iss.get("card_id"), iss.get("severity"), iss.get("owner_stage"), iss.get("problem")[:40]]
            for iss in state.active_issues
        ]
        print_table(headers, rows, title="Active Blocking Issues")


def cmd_rollback(args):
    """Trigger a manual rollback to an upstream stage."""
    project_name = args.project_name
    target_stage = StageId(args.target_stage)
    reason = args.reason or "Manual rollback requested by operator"

    orchestrator = WorkflowOrchestrator(project_name=project_name)
    curr = orchestrator.state.current_stage
    curr_idx = STAGE_ORDER.index(curr)
    target_idx = STAGE_ORDER.index(target_stage)

    if target_idx >= curr_idx:
        print_error(f"Target stage {target_stage.value} must be strictly before current stage {curr.value}.")
        return

    affected = [STAGE_ORDER[i] for i in range(target_idx + 1, curr_idx + 1)]
    orchestrator.tm.update_t4_rollback(
        current_stage=curr,
        target_stage=target_stage,
        reason=reason,
        invalidated_objects=["Manual invalidation of downstream assumptions"],
        affected_stages=affected,
    )
    orchestrator.state.current_stage = target_stage
    orchestrator.state.current_round = 1
    orchestrator.state.log_event("MANUAL_ROLLBACK", {"from": curr.value, "to": target_stage.value, "reason": reason})
    orchestrator.state.save(orchestrator.workspace)
    print_success(f"Rollback complete: {curr.value} -> {target_stage.value}. T4 recorded and downstream marked NEEDS_RECHECK.")


def main():
    parser = argparse.ArgumentParser(
        prog="autoresearch",
        description="AutoResearch Codeless: Executable Idea-to-Paper Workflow v4 with Gemini in agy",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to run")

    # doctor
    p_doctor = subparsers.add_parser("doctor", help="Check agy binary, credentials, and Gemini API connectivity")
    p_doctor.add_argument("--model", help="Model to test with", default="gemini-3.8-flash-low")
    p_doctor.set_defaults(func=cmd_doctor)

    # stages
    p_stages = subparsers.add_parser("stages", help="List all 8 stages and 48 cards")
    p_stages.set_defaults(func=cmd_stages)

    # init
    p_init = subparsers.add_parser("init", help="Initialize a new research project")
    p_init.add_argument("project_name", help="Name of the project")
    p_init.add_argument("--topic", help="Research topic or long-term question")
    p_init.add_argument("--archetype", help="Contribution archetype", choices=CONTRIBUTION_TYPES, default=CONTRIBUTION_TYPES[0])
    p_init.set_defaults(func=cmd_init)

    # step
    p_step = subparsers.add_parser("step", help="Run one stage step (Builder -> Critic -> Controller)")
    p_step.add_argument("project_name", help="Name of the project")
    p_step.add_argument("--model", help="Gemini model to use", default=DEFAULT_MODEL)
    p_step.add_argument("--evidence-mode", choices=EVIDENCE_MODES, default="SIMULATED",
                        help="SIMULATED forbids asserting unmeasured results; "
                             "MEASURED requires every number to trace to an artifact on disk")
    p_step.add_argument("--reference", default=None,
                       help="Path to prior published work to reproduce or position against "
                            "(e.g. paper_text.txt)")
    p_step.set_defaults(func=cmd_step)

    # run
    p_run = subparsers.add_parser("run", help="Run the automated research pipeline")
    p_run.add_argument("project_name", help="Name of the project")
    p_run.add_argument("--stage", help="Start stage (e.g. S1)", default=None)
    p_run.add_argument("--until", help="Stop stage (e.g. S8)", default=None)
    p_run.add_argument("--model", help="Gemini model to use", default=DEFAULT_MODEL)
    p_run.add_argument("--evidence-mode", choices=EVIDENCE_MODES, default="SIMULATED",
                       help="SIMULATED forbids asserting unmeasured results; "
                            "MEASURED requires every number to trace to an artifact on disk")
    p_run.add_argument("--reference", default=None,
                       help="Path to prior published work to reproduce or position against "
                            "(e.g. paper_text.txt)")
    p_run.set_defaults(func=cmd_run)

    # verify
    p_verify = subparsers.add_parser("verify",
                                     help="Re-run the deterministic integrity audit over a project")
    p_verify.add_argument("project_name", help="Name of the project")
    p_verify.add_argument("--evidence-mode", choices=EVIDENCE_MODES, default=None,
                          help="MEASURED (default) checks provenance of asserted numbers; "
                               "SIMULATED additionally flags any asserted number at all")
    p_verify.set_defaults(func=cmd_verify)

    # measure
    p_measure = subparsers.add_parser(
        "measure",
        help="Execute a declared protocol for real, producing auditable artifacts")
    p_measure.add_argument("project_name", help="Name of the project")
    p_measure.add_argument("--protocol", default=None,
                           help="Path to the protocol manifest JSON "
                                "(default: <workspace>/protocol.json)")
    p_measure.add_argument("--tool", action="append", default=None,
                           help="Tool binary whose version is recorded in the environment "
                                "fingerprint (repeatable, e.g. --tool cbmc --tool z3)")
    p_measure.set_defaults(func=cmd_measure)

    # status
    p_status = subparsers.add_parser("status", help="Show project status and active issues")
    p_status.add_argument("project_name", help="Name of the project")
    p_status.set_defaults(func=cmd_status)

    # rollback
    p_rollback = subparsers.add_parser("rollback", help="Manually rollback to an earlier stage")
    p_rollback.add_argument("project_name", help="Name of the project")
    p_rollback.add_argument("target_stage", help="Target stage ID (e.g. S1, S2, S3)")
    p_rollback.add_argument("--reason", help="Reason for rollback", default=None)
    p_rollback.set_defaults(func=cmd_rollback)

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
