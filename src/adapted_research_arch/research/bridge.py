"""Trusted S6 command bridge. Reads the native agent request on stdin."""

import json
from pathlib import Path
import sys

from .gates import BUILD_SCHEMA, protocol_specs
from .measurement import ProtocolRunner


def measurement_response(request: dict, workspace: Path) -> dict:
    if request["stage"]["id"] != "s6":
        raise ValueError("measurement bridge is only valid for s6")
    record = {"stage": "S6", "text": "No experiment executed. [TBD-MEASURE:poc]"}
    record["problemContract"] = request["researchContract"].get("problemContract")
    artifacts = {}
    metrics = {}
    outcome = "inconclusive"
    if request["researchContract"]["evidenceMode"] == "MEASURED":
        protocol = request["dependencyResults"]["s5"]["records"][BUILD_SCHEMA]["protocol"]
        runner = ProtocolRunner(workspace)
        manifest = runner.run_all(protocol_specs(protocol))
        for path in runner.artifacts_dir.iterdir():
            artifacts[path.relative_to(workspace).as_posix()] = path.read_text(encoding="utf-8")
        summary = manifest["summary"]
        record.update(
            protocol=protocol,
            measurementArtifact="artifacts/poc_runs/manifest.json",
            measurementSummary=summary,
            text=f"Measured cohort N={summary['overall']['n']}. Evidence: `artifacts/poc_runs/manifest.json`.",
        )
        if summary["overall"]["n_valid"]:
            metrics = {"pass_rate_over_all": summary["overall"]["pass_rate_over_all"]}
            outcome = "positive" if summary["overall"]["pass_count"] else "negative"
    return {
        "status": "completed" if outcome == "positive" else outcome, "summary": record["text"],
        "records": {BUILD_SCHEMA: record}, "artifacts": artifacts,
        "claims": [], "observations": [], "metrics": metrics, "usage": {},
    }


def main() -> int:
    json.dump(measurement_response(json.load(sys.stdin), Path.cwd()), sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
