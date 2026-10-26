"""Codeless research contracts evaluated by the existing ResearchEngine."""

from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from .cards import get_cards_for_stage
from .integrity import audit_stage, extract_stage_evidence
from .measurement import RunRecord, RunSpec, summarize
from .stages import StageId, get_stage

BUILD_SCHEMA = "research.stage.v1"
REVIEW_SCHEMA = "research.review.v1"


def context(stage_id: str, evidence_mode: str) -> dict:
    stage = StageId(stage_id.split("_")[0].upper())
    definition = get_stage(stage)
    template = {"S1": "T0", "S2": "T0", "S3": "T2", "S4": "T5", "S5": "T3", "S6": "T2", "S7": "T2", "S8": "T5"}[stage.value]
    if stage_id.endswith("_review"):
        template = "T1"
    path = next((Path(__file__).parent / "assets").glob(template + "_*.md"))
    return {
        "stage": asdict(definition),
        "cards": [asdict(card) for card in get_cards_for_stage(stage)],
        "role": "reviewer" if stage_id.endswith("_review") else "builder",
        "evidenceMode": evidence_mode,
        "template": path.read_text(encoding="utf-8"),
    }


def protocol_specs(protocol: dict) -> list[RunSpec]:
    if not isinstance(protocol, dict) or not isinstance(protocol.get("runs"), list) or not protocol["runs"]:
        raise ValueError("S5 requires a nonempty structured protocol.runs list")
    specs = []
    for row in protocol["runs"]:
        values = {**protocol.get("defaults", {}), **row}
        spec = RunSpec(
            run_id=values["run_id"], command=values["command"],
            label=values.get("label", ""), group=values.get("group", "default"),
            timeout_s=float(values.get("timeout_s", 60)),
            inputs=values.get("inputs", []), cwd=values.get("cwd"),
        )
        if not spec.command:
            raise ValueError("protocol commands cannot be empty")
        specs.append(spec)
    if len({s.run_id for s in specs}) != len(specs):
        raise ValueError("duplicate protocol run IDs")
    return specs


def _record(output: dict, schema: str) -> dict:
    value = output.get("records", {}).get(schema)
    if not isinstance(value, dict):
        raise ValueError(f"missing {schema} record")
    return value


def _measurement(record: dict, output: dict, protocol: dict) -> list[str]:
    if record.get("protocol") != protocol:
        return ["S6 execution changed the frozen S5 protocol; start a revised run"]
    artifacts = output.get("artifacts", {})
    manifest = json.loads(artifacts[record["measurementArtifact"]])
    rows = [RunRecord(**row) for row in manifest["records"]]
    specs = protocol_specs(protocol)
    if len(rows) != len(specs):
        return ["measurement cohort does not match S5"]
    for row, spec in zip(rows, specs):
        if (row.run_id, row.command, row.timeout_s, row.group) != (spec.run_id, list(spec.command), spec.timeout_s, spec.group):
            return ["measurement argv, timeout, group, or run order differs from S5"]
        if row.status not in {"PASS", "FAIL", "TIMEOUT", "ERROR", "TOOL_MISSING"}:
            return ["invalid measurement status"]
        for field in ("stdout", "stderr"):
            text = artifacts[getattr(row, field + "_path")]
            if hashlib.sha256(text.encode()).hexdigest() != getattr(row, field + "_sha256"):
                return ["measurement log digest mismatch"]
        if row.status not in {"ERROR", "TOOL_MISSING"} and set(row.input_hashes) != set(spec.inputs):
            return ["measurement omitted declared input fingerprints"]
    expected = summarize(rows)
    actual = record.get("measurementSummary", {})
    if not isinstance(actual, dict):
        return ["measurementSummary must be an object"]
    if any(actual.get(key) != expected[key] for key in ("overall", "by_group", "run_ids")):
        return ["measurement summary is not derived from the raw run records"]
    if expected["overall"]["n_valid"] == 0:
        return ["no valid measurement: missing tools and errors are not negative results"]
    return []


def evaluate(gate: str, request: dict, output: dict, workspace: Path, prior: dict) -> list[str]:
    contract = request["researchContract"]
    stage = StageId(contract["stage"]["id"])
    native = stage.value.lower()
    mode = contract["evidenceMode"]
    reviewing = contract["role"] == "reviewer"
    record = _record(output, REVIEW_SCHEMA if reviewing else BUILD_SCHEMA)
    if record.get("stage") != stage.value:
        return ["research record stage does not match the pinned stage"]
    if gate == "research.review":
        build = prior[native]
        if build["agent"]["id"] == request["agent"]["id"]:
            return ["builder and reviewer must use distinct trusted agent packages"]
        if record.get("reviewedAttemptId") != build["attemptId"]:
            return ["review must identify the current builder attempt"]
        cards = record.get("cards", {})
        if set(cards) != set(get_stage(stage).cards):
            return ["review must cover exactly the six cards for this stage"]
        for card_id, verdict in cards.items():
            if not isinstance(verdict, dict) or verdict.get("status") not in {"MET", "N/A"}:
                reason = str(verdict.get("reason", ""))[:500] if isinstance(verdict, dict) else "invalid verdict"
                return [f"{card_id} is unresolved: {reason}; revise this stage or fork at its root cause"]
            if any(not isinstance(verdict.get(field), str) or not verdict[field].strip() for field in ("reason", "location")):
                return [f"{card_id} requires a reason and evidence location, including N/A"]
        issues = record.get("issues", [])
        if not isinstance(issues, list) or any(not isinstance(issue, dict) for issue in issues):
            return ["review issues must be an array of objects"]
        if any(str(issue.get("severity", "")).upper() == "BLOCKING" for issue in issues):
            return ["review contains unresolved blocking issues"]
        return []
    if reviewing:
        output = prior[native]
        record = _record(output, BUILD_SCHEMA)
    text = record.get("text")
    if not isinstance(text, str) or not text.strip():
        return ["research stage text is required"]
    if stage == StageId.S2:
        problem = record.get("problemContract", {})
        if not isinstance(problem, dict) or any(not isinstance(problem.get(key), str) or not problem[key].strip() for key in ("researchQuestion", "unit", "scope", "primaryOutcome", "comparator")):
            return ["S2 requires the central research question, unit, scope, primary outcome, and comparator"]
    elif stage in {StageId.S3, StageId.S4, StageId.S5, StageId.S6, StageId.S7, StageId.S8}:
        frozen_problem = _record(prior["s2"], BUILD_SCHEMA)["problemContract"]
        if record.get("problemContract") != frozen_problem:
            return ["stage changed the frozen S2 research question or scope; fork a revised run"]
    if stage == StageId.S5:
        protocol_specs(record.get("protocol"))
    prior_evidence = {
        key.upper(): extract_stage_evidence(StageId(key.upper()), _record(value, BUILD_SCHEMA)["text"]).to_dict()
        for key, value in prior.items() if key in {"s5", "s6"}
    }
    frozen = prior_evidence.get("S5")
    known = {name for value in prior.values() for name in value.get("artifactIds", {})}
    errors = [f"{finding.check}: {finding.problem}" for finding in audit_stage(
        stage, text, workspace, prior_evidence, frozen_protocol=frozen,
        evidence_mode=mode, known_artifacts=known,
    )]
    if mode == "SIMULATED" and stage in {StageId.S6, StageId.S7, StageId.S8} and output.get("metrics"):
        errors.append("SIMULATED stages cannot report measured metrics")
    if mode == "MEASURED" and stage == StageId.S6:
        if not reviewing and request["agent"]["adapter"]["type"] != "command":
            errors.append("MEASURED S6 requires a trusted command executor, not a model adapter")
        protocol = _record(prior["s5"], BUILD_SCHEMA)["protocol"]
        errors.extend(_measurement(record, output, protocol))
    if mode == "MEASURED" and stage in {StageId.S7, StageId.S8}:
        summary = _record(prior["s6"], BUILD_SCHEMA)["measurementSummary"]["overall"]
        if any(key not in summary or summary[key] != value for key, value in output.get("metrics", {}).items()):
            errors.append("reported metrics differ from the verified S6 measurements")
    return errors
