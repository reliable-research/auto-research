"""Blind Research Trajectory Execution (Zero-Cheat Experiment).

Input Idea: Purely minimal, naive research premise with NO cheat:
"Using Large Language Models to automatically generate loop invariants to avoid loop unrolling in Bounded Model Checking"

No mentions of:
- Vampire
- First-order theorem provers / TPTP
- CFG surgery / havoc
- Specific benchmarks (Code2Inv, SV-COMP)
- Specific baselines (SeaHorn, VeriAbs)
- Pre-known error rates or solutions

Let the 3-agent workflow (Builder, Critic, Controller) discover, formalize, and defend the research path organically.
"""

import sys
from pathlib import Path

# Add workspace to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from autoresearch.config import Config
from autoresearch.workflow.stages import StageId, STAGES, STAGE_ORDER
from autoresearch.workflow.decision_engine import ActionType
from autoresearch.agents.coordinator import WorkflowOrchestrator
from autoresearch.utils.logger import print_banner, print_info, print_success, print_warning, print_error, print_table

PROJECT_NAME = "blind_llm_loop_invariants"
RAW_NAIVE_IDEA = (
    "Using Large Language Models to automatically generate loop invariants "
    "to avoid loop unrolling in Bounded Model Checking"
)
ARCHETYPE = "方法 (Method)"


def main():
    print_banner(
        "AutoResearch Codeless: Blind Zero-Cheat Pipeline",
        f"Raw Idea: '{RAW_NAIVE_IDEA}'",
    )

    config = Config(
        model="gemini-3.8-flash-low",
        max_refine_rounds=3,
    )

    orchestrator = WorkflowOrchestrator(
        project_name=PROJECT_NAME,
        topic=RAW_NAIVE_IDEA,
        contribution_type=ARCHETYPE,
        config=config,
    )

    print_info(f"Initialized blind project workspace at: {orchestrator.workspace}")
    print_info("No paper text, no Vampire hints, no pre-baked metrics passed in.")
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
                print_warning(f"-> In-loop Refine triggered for {stage_id.value} (Round {orchestrator.state.current_round}). Retrying with Critic feedback...")

    print_banner("Blind Research Pipeline Complete!", f"Deliverable in {orchestrator.workspace}")
    
    # Print Trajectory Summary Table
    headers = ["Step", "Stage", "Action", "Target", "Issues", "Reason"]
    rows = [
        [idx, t["stage"], t["action"], t["target"] or "-", t["blocking_issues_count"], t["reason"][:45]]
        for idx, t in enumerate(trajectory_log, 1)
    ]
    print_table(headers, rows, title="Blind Trajectory Execution Log")


if __name__ == "__main__":
    main()
