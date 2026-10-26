"""Example script demonstrating programmatic usage of AutoResearch Codeless."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from autoresearch.config import Config
from autoresearch.llm.credentials import AgyCredentialMapper
from autoresearch.agents.coordinator import WorkflowOrchestrator
from autoresearch.workflow.stages import StageId


def main():
    print("=== AutoResearch Codeless Demonstration ===")

    # 1. Verify credentials and agy mapping
    mapper = AgyCredentialMapper()
    auth_status = mapper.check_status()
    print(f"Antigravity CLI Binary: {auth_status.agy_binary}")
    print(f"Token Status: {'VALID' if auth_status.is_valid else 'INVALID'} ({auth_status.token_preview})")

    if not auth_status.is_valid:
        print("Error: Antigravity OAuth credentials not ready.")
        sys.exit(1)

    # 2. Setup orchestrator with a research topic
    project_name = "example_spec_reasoning"
    topic = "Specification-guided iterative program repair using dynamic execution traces"
    config = Config(model="gemini-3.8-flash-high")

    orchestrator = WorkflowOrchestrator(
        project_name=project_name,
        topic=topic,
        contribution_type="方法 (Method)",
        config=config,
    )

    print(f"\nProject created at: {orchestrator.workspace}")
    print("Starting S1 execution cycle (Builder -> Critic -> Controller)...")

    decision = orchestrator.execute_current_stage_step()
    print(f"\nResulting Action: {decision.action.value}")
    if decision.target_stage:
        print(f"Target Stage: {decision.target_stage.value}")
    print(f"Reason: {decision.reason}")


if __name__ == "__main__":
    main()
