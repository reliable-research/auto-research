from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Sequence

from .engine import ResearchEngine, verify_run
from .events import EventLedger
from .memory import ResearchMemory
from .project import Project
from .protocol import ProtocolServer, diagnostics, serve_stdio
from .registry import AgentRegistry
from .workflows import WORKFLOWS


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="ara", description="Adapted Research Architecture runtime")
    root.add_argument("--project", type=Path, help="research project root")
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="create a local research project")
    init.add_argument("path", type=Path)
    init.add_argument("--name")

    commands.add_parser("doctor", help="show execution isolation diagnostics")

    agents = commands.add_parser("agents", help="list or trust agent packages")
    agents_sub = agents.add_subparsers(dest="agents_command", required=True)
    agents_sub.add_parser("list")
    trust = agents_sub.add_parser("trust")
    trust.add_argument("agent_id")
    trust.add_argument("--version")
    disable = agents_sub.add_parser("disable")
    disable.add_argument("agent_id")
    disable.add_argument("--version")

    commands.add_parser("workflows", help="list built-in workflows")

    run = commands.add_parser("run", help="start, resume, approve, inspect, or verify a run")
    run_sub = run.add_subparsers(dest="run_command", required=True)
    start = run_sub.add_parser("start")
    start.add_argument("workflow", choices=sorted(WORKFLOWS))
    start.add_argument("objective")
    start.add_argument("--mode", choices=("autopilot", "copilot", "manual"), default="autopilot")
    start.add_argument("--evidence-mode", choices=("SIMULATED", "MEASURED"), default="SIMULATED")
    start.add_argument("--thread")
    start.add_argument("--idempotency-key")
    start.add_argument(
        "--agent-pin",
        action="append",
        default=[],
        metavar="STAGE_OR_CAPABILITY=AGENT_ID",
        help="route a stage or capability through an explicitly trusted agent package",
    )
    for name in ("resume", "pause", "stop", "retry", "status", "verify", "events"):
        child = run_sub.add_parser(name)
        child.add_argument("run_id")
    approve = run_sub.add_parser("approve")
    approve.add_argument("run_id")
    approve.add_argument("--stage")
    approve.add_argument("--scope", choices=("stage", "run"), default="stage")

    memory = commands.add_parser("memory", help="inspect or review research memory")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)
    memory_sub.add_parser("list").add_argument("--status")
    query = memory_sub.add_parser("query")
    query.add_argument("text")
    review = memory_sub.add_parser("review")
    review.add_argument("observation_id")
    review.add_argument("--accept", action="store_true")

    serve = commands.add_parser("serve", help="serve newline-delimited JSON protocol on stdio")
    serve.add_argument("--project-root", type=Path)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "init":
            project = Project.create(args.path, name=args.name or args.path.name)
            return _print(project.manifest)
        if args.command == "serve":
            return serve_stdio(ProtocolServer(args.project_root or args.project))
        if args.command == "doctor":
            project = Project(args.project) if args.project else None
            return _print(diagnostics(project))

        project = _project(args)
        if args.command == "agents":
            registry = AgentRegistry(project)
            if args.agents_command == "list":
                return _print(registry.list())
            if args.agents_command == "trust":
                return _print(registry.trust(args.agent_id, version=args.version).to_dict())
            return _print(registry.disable(args.agent_id, version=args.version).to_dict())
        if args.command == "workflows":
            return _print(
                [
                    {
                        "id": item.id,
                        "version": item.version,
                        "description": item.description,
                        "stages": [stage.id for stage in item.stages],
                    }
                    for item in WORKFLOWS.values()
                ]
            )
        if args.command == "run":
            engine = ResearchEngine(project)
            if args.run_command == "start":
                return _print(
                    engine.start(
                        workflow_id=args.workflow,
                        objective=args.objective,
                        control_mode=args.mode,
                        thread_id=args.thread,
                        idempotency_key=args.idempotency_key,
                        agent_pins=_parse_agent_pins(args.agent_pin),
                        evidence_mode=args.evidence_mode,
                    )
                )
            if args.run_command == "resume":
                return _print(engine.resume(args.run_id))
            if args.run_command == "pause":
                return _print(engine.pause(args.run_id))
            if args.run_command == "stop":
                return _print(engine.stop(args.run_id))
            if args.run_command == "retry":
                return _print(engine.retry(args.run_id))
            if args.run_command == "status":
                return _print(engine.describe(args.run_id))
            if args.run_command == "approve":
                return _print(
                    engine.approve(args.run_id, stage_id=args.stage, scope=args.scope)
                )
            if args.run_command == "verify":
                report = verify_run(project, args.run_id)
                _print(report)
                return 0 if report["ok"] else 2
            if args.run_command == "events":
                project.read_run(args.run_id)
                ledger = EventLedger(
                    project.run_dir(args.run_id) / "events.jsonl",
                    project_id=project.project_id,
                    run_id=args.run_id,
                )
                return _print(ledger.read())
        if args.command == "memory":
            memory = ResearchMemory(project.db_path)
            if args.memory_command == "list":
                return _print(memory.list_observations(status=args.status))
            if args.memory_command == "query":
                return _print(memory.query(args.text))
            if args.memory_command == "review":
                memory.review(args.observation_id, accept=args.accept)
                return _print({"reviewed": True, "accepted": args.accept})
        raise RuntimeError("unhandled command")
    except Exception as error:
        print(json.dumps({"error": error.__class__.__name__, "message": str(error)}), file=sys.stderr)
        return 1


def _project(args: argparse.Namespace) -> Project:
    if not args.project:
        raise RuntimeError("--project is required for this command")
    return Project(args.project)


def _parse_agent_pins(values: Sequence[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        key, separator, agent_id = value.partition("=")
        key, agent_id = key.strip(), agent_id.strip()
        if not separator or not key or not agent_id:
            raise ValueError(f"invalid --agent-pin {value!r}; expected STAGE_OR_CAPABILITY=AGENT_ID")
        if key in result and result[key] != agent_id:
            raise ValueError(f"conflicting --agent-pin values for {key}")
        result[key] = agent_id
    return result


def _print(value: Any) -> int:
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, default=str))
    return 0
