"""Specific Idea Pipeline (Zero-Leakage, High-Specificity Research Proposal).

This experiment feeds a realistic, specific research pitch into the Idea-to-Paper
Codeless Workflow WITHOUT leaking the implementation secrets of the published paper:
- No mentions of Vampire, TPTP, or first-order resolution provers.
- No mentions of CFG surgery, code slicing, or specific AST transformations.
- No mentions of the cherry-picked 133 benchmark numbers or paper results.

It provides a concrete, grounded academic premise:
- Target: BMC loop unrolling explosion in C programs.
- Problem: Classical templates are rigid; zero-shot LLM candidates are non-inductive.
- Hypothesis: LLM as semantic invariant proposer + automated induction verifier
  to convert BMC into unbounded inductive proof without unrolling.
- Rigorous metrics: Inductive proof success rate, memory/time scaling, and failure analysis.
"""

import sys
from pathlib import Path

# Add workspace to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from autoresearch.config import Config
from autoresearch.workflow.stages import StageId, STAGES, STAGE_ORDER
from autoresearch.workflow.decision_engine import ActionType
from autoresearch.agents.coordinator import WorkflowOrchestrator
from autoresearch.utils.logger import (
    print_banner,
    print_info,
    print_success,
    print_warning,
    print_error,
    print_table,
)

PROJECT_NAME = "specific_idea_llm_loop_invariants"

SPECIFIC_RESEARCH_PROPOSAL = """LLM-Assisted Inductive Invariant Generation for Bypassing Loop Unrolling in Bounded Model Checking (BMC)

[Problem Background & Bottleneck]
Bounded Model Checking (BMC, e.g., CBMC) for C software suffers from severe state-space explosion when unrolling loops with large, variable, or unbounded iteration counts (k >= 50). Classical invariant generation tools (such as Houdini, ICE, or Daikon) rely on rigid syntactic predicate templates or abstract interpretation, which frequently fail or time out on programs with multiple loop branches and linear/non-linear arithmetic.

[The LLM Bottleneck & Core Hypothesis]
Directly prompting LLMs to synthesize formal invariants fails because LLMs frequently hallucinate or generate "true but non-inductive" candidate predicates—assertions that hold along standard execution traces but fail the inductive step (consecution: I /\ Guard /\ Body => I') due to missing auxiliary state constraints.
We hypothesize that a synergistic, two-tiered framework can resolve this:
1. Semantic Proposal Tier: Leverage LLM's high-level program reasoning to inspect loop conditions, state mutations, and post-conditions to propose candidate invariants and auxiliary relations.
2. Formal Inductive Verification Tier: Formally verify the candidate assertions against the inductive triplet (Initiation, Consecution, Safety) via automated deduction.
3. Proof Integration: Incorporate sound inductive invariants back into BMC to achieve complete unbounded verification in constant solver time, eliminating the loop unrolling bottleneck.

[Evaluation Dimensions & Scope]
- Scope: ANSI-C programs containing integer arithmetic loops with scalar and multi-path branches.
- Evaluation Metrics: Inductive proof success rate (IPSR), verification speedup and memory footprint reduction against standard BMC loop unrolling across increasing bounds (k = 10, 50, 100, 1000).
- Soundness & Failure Analysis: Categorization of non-inductive failure modes and exploration of automated refinement strategies when candidates fail the consecution check.
"""

ARCHETYPE = "方法 (Method)"


def main():
    print_banner(
        "AutoResearch Codeless: Specific Idea Pipeline",
        "Feeding a detailed, realistic research proposal without leaking paper solutions",
    )

    config = Config(
        model="gemini-3.8-flash-low",
        max_refine_rounds=3,
    )

    orchestrator = WorkflowOrchestrator(
        project_name=PROJECT_NAME,
        topic=SPECIFIC_RESEARCH_PROPOSAL,
        contribution_type=ARCHETYPE,
        config=config,
    )

    print_info(f"Initialized specific idea project workspace at: {orchestrator.workspace}")
    print_info("Specific Research Proposal Loaded (Zero Leaks of Vampire / CFG surgery / Target Numbers).")
    print_info("Executing pipeline across S1-S8...")

    trajectory_log = []

    for stage_id in STAGE_ORDER:
        orchestrator.state.current_stage = stage_id
        orchestrator.state.current_round = 1
        print_banner(f"Stage {stage_id.value}: {STAGES[stage_id].name}")

        round_count = 0
        while round_count < config.max_refine_rounds:
            round_count += 1
            decision = orchestrator.execute_current_stage_step()

            trajectory_log.append({
                "stage": stage_id.value,
                "round": orchestrator.state.current_round - 1 if decision.action == ActionType.REFINE_INLOOP else orchestrator.state.current_round,
                "action": decision.action.value,
                "target": decision.target_stage.value if decision.target_stage else None,
                "reason": decision.reason,
                "blocking_issues_count": len(decision.blocking_issues),
            })

            if decision.action in [ActionType.CONTINUE, ActionType.PAUSE, ActionType.ROLLBACK]:
                break
            elif decision.action == ActionType.REFINE_INLOOP:
                print_warning(
                    f"-> In-loop Refine triggered for {stage_id.value} "
                    f"(Round {orchestrator.state.current_round}). Retrying with Critic feedback..."
                )

    print_banner("Specific Idea Research Pipeline Complete!", f"Deliverable in {orchestrator.workspace}")

    # Print Trajectory Summary Table
    headers = ["Step", "Stage", "Action", "Target", "Issues", "Reason"]
    rows = [
        [idx, t["stage"], t["action"], t["target"] or "-", t["blocking_issues_count"], t["reason"][:45]]
        for idx, t in enumerate(trajectory_log, 1)
    ]
    print_table(headers, rows, title="Specific Idea Trajectory Execution Log")


if __name__ == "__main__":
    main()
