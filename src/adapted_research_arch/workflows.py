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


def _research_stages() -> tuple[StageSpec, ...]:
    from .research.stages import STAGE_ORDER, get_stage
    result = []
    for index, identifier in enumerate(STAGE_ORDER):
        name = identifier.value.lower()
        dependencies = [f"s{index}", f"s{index}_review"] if index else []
        if index >= 2 and "s2" not in dependencies:
            dependencies.append("s2")
        if index >= 5:
            dependencies.append("s5")
        if index >= 6:
            dependencies.append("s6")
        if index == 7:
            dependencies = list(dict.fromkeys([*dependencies, *[f"s{n}" for n in range(1, 8)]]))
        gates = ("schema.valid", "research.integrity", "numeric.provenance")
        if index == 7:
            gates += ("publication.reverse_links",)
        result.append(stage(
            name, "research.measure" if index == 5 else "research.build_stage",
            get_stage(identifier).goal, depends_on=tuple(dependencies),
            risk=Risk.R3 if index == 5 else Risk.R2,
            outputs=("research.stage.v1",), gates=gates,
        ))
        review_gates = ("schema.valid", "research.review", "research.integrity")
        if index in (5, 6):
            review_gates += ("claim.promotion",)
        review_dependencies = list(dict.fromkeys([name, *dependencies]))
        result.append(stage(
            name + "_review", "research.review_stage", "Review the six current-stage cards and machine checks.",
            depends_on=tuple(review_dependencies), outputs=("research.review.v1",), gates=review_gates,
        ))
    return tuple(result)


IDEA_TO_PAPER = WorkflowSpec(
    id="idea-to-paper", version="0.1.0",
    description="One evidence-gated research loop, with eight stages and separate reviews.",
    stages=_research_stages(),
)


WORKFLOWS = {
    item.id: item
    for item in (LITERATURE_REVIEW, DATA_ANALYSIS, CODE_OPTIMIZATION, PAPER_REPRODUCTION, IDEA_TO_PAPER)
}
