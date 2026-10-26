"""Execute the Idea-to-Paper Codeless Workflow (S1-S8) for the ASE 2024 paper idea:
'LLM-Generated Invariants for Bounded Model Checking Without Loop Unrolling'
"""

import sys
import json
import time
from pathlib import Path

# Add workspace to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from autoresearch.config import Config
from autoresearch.workflow.stages import StageId, STAGES, STAGE_ORDER, get_stage
from autoresearch.workflow.cards import CARDS, get_cards_for_stage
from autoresearch.workflow.state import ProjectState
from autoresearch.workflow.decision_engine import ActionType
from autoresearch.agents.coordinator import WorkflowOrchestrator
from autoresearch.utils.logger import print_banner, print_info, print_success, print_warning, print_error, print_table

PROJECT_NAME = "llm_bmc_without_unrolling"
TOPIC = (
    "LLM-Generated Inductive Invariants for Sound Bounded Model Checking Without Loop Unrolling: "
    "Replacing CFG loops with Vampire-verified invariant nodes and SMT safety checking"
)
ARCHETYPE = "方法 (Method)"


def main():
    print_banner(
        "AutoResearch Codeless: ASE 2024 Paper Reproduction & Rebuilding",
        "Target Paper: 'LLM-Generated Invariants for Bounded Model Checking Without Loop Unrolling'",
    )

    # 1. Initialize orchestrator with the paper's core research topic
    config = Config(
        model="gemini-3.8-flash-low",  # Fast and reliable for multi-stage execution
        max_refine_rounds=2,
        # Actually seed the paper this script claims to reproduce. Without it the
        # pipeline only ever saw TOPIC and rebuilt the paper from model memory.
        reference_material_path=Path(__file__).resolve().parent / "paper_text.txt",
    )
    orchestrator = WorkflowOrchestrator(
        project_name=PROJECT_NAME,
        topic=TOPIC,
        contribution_type=ARCHETYPE,
        config=config,
    )

    print_info(f"Workspace initialized at: {orchestrator.workspace}")
    print_info(f"Contribution Archetype: {ARCHETYPE}")

    # 2. Run pipeline through all 8 stages (S1 -> S8)
    for stage_id in STAGE_ORDER:
        orchestrator.state.current_stage = stage_id
        orchestrator.state.current_round = 1
        print_banner(f"Advancing Stage: {stage_id.value} - {STAGES[stage_id].name}")

        # Execute stage step (Builder -> Critic -> Controller)
        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            decision = orchestrator.execute_current_stage_step()
            if decision.action in [ActionType.CONTINUE, ActionType.PAUSE]:
                break
            elif decision.action == ActionType.REFINE_INLOOP:
                print_info(f"Stage {stage_id.value} requested in-loop refinement (Attempt {attempt}/{max_attempts})...")

        print_success(f"Stage {stage_id.value} finalized. Deliverable synced to 05_T5_UNIFIED_RESEARCH_DRAFT.md.")

    print_banner(
        "Whole Pipeline Completed!",
        f"All 8 stages (S1-S8) executed. Review artifacts ready in {orchestrator.workspace}",
    )


if __name__ == "__main__":
    main()
