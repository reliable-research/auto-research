"""Deterministic built-in agent used for local demonstrations and conformance tests."""

from __future__ import annotations

import json
import sys


def main() -> int:
    request = json.load(sys.stdin)
    stage = request["stage"]
    stage_id = stage["id"]
    capability = stage["capability"]
    objective = request["objective"]
    promoted = request.get("promotedClaims", [])
    artifact_name = f"{stage_id}.json"
    artifact_value = {
        "stage": stage_id,
        "capability": capability,
        "objective": objective,
        "summary": f"Deterministic local result for {stage_id}.",
        "promotedClaimCount": len(promoted),
        "metric": 1.0,
    }
    if capability == "review.audit_integrity":
        artifact_value["reviewDecision"] = "pass"
        artifact_value["candidateClaimIds"] = [item["id"] for item in request.get("candidateClaims", [])]
    if capability == "publication.write_from_claims":
        artifact_value["claimIds"] = [item["id"] for item in promoted]
    status = "completed"
    if "[negative]" in objective.lower():
        status = "negative"
    elif "[inconclusive]" in objective.lower():
        status = "inconclusive"
    elif "[saturated]" in objective.lower():
        status = "saturated"
    elif "[floored]" in objective.lower():
        status = "floored"
    claims = []
    if capability in {"evidence.synthesize_claims", "analysis.compare_results"}:
        claims.append(
            {
                "text": f"The {stage_id} stage produced an inspectable local result.",
                "evidence": [
                    {"source": f"artifact:{artifact_name}", "locator": "json:/summary", "kind": "artifact"}
                ],
            }
        )
    if capability in {"analysis.test_hypothesis", "experiment.execute"}:
        claims.append(
            {
                "text": f"The measured {stage_id} fixture metric is 1.0.",
                "value": 1.0,
                "unit": "fixture-score",
                "evidence": [
                    {"source": f"artifact:{artifact_name}", "locator": "json:/metric", "kind": "numeric"}
                ],
            }
        )
    output = {
        "status": status,
        "summary": artifact_value["summary"],
        "records": {schema: artifact_value for schema in stage.get("outputs", [])},
        "artifacts": {artifact_name: json.dumps(artifact_value, indent=2, sort_keys=True)},
        "claims": claims,
        "observations": [
            {
                "content": f"{stage_id}: {artifact_value['summary']}",
                "tags": [f"stage:{stage_id}", "builtin-fixture"],
                "confidence": 0.8,
                "dataClass": "development",
            }
        ],
        "metrics": {"fixture_score": 1.0},
        "usage": {"toolCalls": 0, "sources": 0, "costUsd": 0},
        "limitations": ["This built-in agent is deterministic and does not replace a real research provider."],
    }
    json.dump(output, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
