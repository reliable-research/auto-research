from __future__ import annotations

from .models import Risk, StageSpec, WorkflowSpec


def stage(
    identifier: str,
    capability: str,
    purpose: str,
    *,
    depends_on: tuple[str, ...] = (),
    risk: Risk = Risk.R1,
    outputs: tuple[str, ...] = (),
    gates: tuple[str, ...] = ("schema.valid",),
) -> StageSpec:
    return StageSpec(
        id=identifier,
        capability=capability,
        purpose=purpose,
        depends_on=depends_on,
        risk=risk,
        outputs=outputs,
        gates=gates,
    )


LITERATURE_REVIEW = WorkflowSpec(
    id="literature-review",
    version="0.1.0",
    description="Evidence-grounded scientific literature review.",
    stages=(
        stage("frame", "research.frame_objective", "Define scope and completion criteria.", outputs=("research.objective.v1",)),
        stage("perspectives", "literature.discover_perspectives", "Find missing viewpoints and questions.", depends_on=("frame",), outputs=("literature.query_plan.v1",)),
        stage("retrieve", "literature.retrieve_papers", "Retrieve and locate scientific evidence.", depends_on=("perspectives",), outputs=("evidence.record_set.v1",), gates=("schema.valid", "evidence.locator_resolution")),
        stage("synthesize", "evidence.synthesize_claims", "Create evidence-linked candidate findings.", depends_on=("retrieve",), outputs=("claim.candidate_set.v1",), gates=("schema.valid", "claim.evidence_complete")),
        stage("audit", "review.audit_integrity", "Audit citations, contradictions, and overclaiming.", depends_on=("synthesize",), outputs=("claim.promoted_set.v1",), gates=("schema.valid", "claim.promotion")),
        stage("write", "publication.write_from_claims", "Write only from promoted claims.", depends_on=("audit",), outputs=("publication.report.v1",), gates=("schema.valid", "publication.reverse_links")),
    ),
)


DATA_ANALYSIS = WorkflowSpec(
    id="data-analysis",
    version="0.1.0",
    description="Hypothesis-driven analysis with numeric provenance.",
    stages=(
        stage("frame", "research.frame_objective", "Define the analytical objective.", outputs=("research.objective.v1",)),
        stage("inspect", "data.inspect", "Inspect data provenance, shape, and limitations.", depends_on=("frame",), outputs=("data.profile.v1",)),
        stage("hypothesize", "research.design_hypothesis", "Define testable hypotheses and assumptions.", depends_on=("inspect",), outputs=("research.hypothesis_set.v1",)),
        stage("analyze", "analysis.test_hypothesis", "Execute analysis and bind results to outputs.", depends_on=("hypothesize",), risk=Risk.R3, outputs=("experiment.result_set.v1",), gates=("schema.valid", "numeric.provenance")),
        stage("audit", "review.audit_integrity", "Review leakage, robustness, and claim support.", depends_on=("analyze",), outputs=("claim.promoted_set.v1",), gates=("schema.valid", "claim.promotion")),
        stage("write", "publication.write_from_claims", "Write the verified analysis report.", depends_on=("audit",), outputs=("publication.report.v1",), gates=("schema.valid", "publication.reverse_links")),
    ),
)


CODE_OPTIMIZATION = WorkflowSpec(
    id="code-optimization",
    version="0.1.0",
    description="Baseline-first, isolated retain-or-reject code improvement.",
    stages=(
        stage("frame", "research.frame_objective", "Freeze target, metric, guard, and budget.", outputs=("research.objective.v1",)),
        stage("baseline", "experiment.execute", "Execute and record the fixed baseline.", depends_on=("frame",), risk=Risk.R3, outputs=("experiment.result_set.v1",), gates=("schema.valid", "numeric.provenance")),
        stage("propose", "experiment.implement", "Implement one bounded hypothesis in isolation.", depends_on=("baseline",), risk=Risk.R2, outputs=("experiment.implementation.v1",)),
        stage("evaluate", "experiment.execute", "Evaluate the candidate under the baseline contract.", depends_on=("propose",), risk=Risk.R3, outputs=("experiment.result_set.v1",), gates=("schema.valid", "numeric.provenance", "baseline.matched")),
        stage("audit", "review.audit_integrity", "Run regression and promotion checks.", depends_on=("evaluate",), risk=Risk.R2, outputs=("claim.promoted_set.v1",), gates=("schema.valid", "claim.promotion")),
    ),
)


PAPER_REPRODUCTION = WorkflowSpec(
    id="paper-reproduction",
    version="0.1.0",
    description="Specification-first paper reproduction with comparison evidence.",
    stages=(
        stage("frame", "research.frame_objective", "Define reproduction scope and evaluator.", outputs=("research.objective.v1",)),
        stage("specify", "reproduction.specify", "Extract claims, equations, interfaces, and ambiguity.", depends_on=("frame",), outputs=("reproduction.specification.v1",), gates=("schema.valid", "evidence.locator_resolution")),
        stage("implement", "reproduction.implement", "Implement the specification in isolation.", depends_on=("specify",), risk=Risk.R2, outputs=("experiment.implementation.v1",)),
        stage("execute", "experiment.execute", "Execute the reproduction and capture measurements.", depends_on=("implement",), risk=Risk.R3, outputs=("experiment.result_set.v1",), gates=("schema.valid", "numeric.provenance")),
        stage("compare", "analysis.compare_results", "Compare reproduced and reported behavior.", depends_on=("execute",), outputs=("claim.candidate_set.v1",), gates=("schema.valid", "claim.evidence_complete")),
        stage("audit", "review.audit_integrity", "Audit deviations and provenance.", depends_on=("compare",), outputs=("claim.promoted_set.v1",), gates=("schema.valid", "claim.promotion")),
    ),
)


WORKFLOWS = {
    item.id: item
    for item in (LITERATURE_REVIEW, DATA_ANALYSIS, CODE_OPTIMIZATION, PAPER_REPRODUCTION)
}
