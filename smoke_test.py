#!/usr/bin/env python3
"""AutoResearch Codeless - Full Workflow Smoke Test.

Validates:
1. Antigravity CLI and Gemini OAuth credentials mapping
2. Core unit and integration test suite (cards, stages, decision engine, templates)
3. End-to-end simulated 8-stage pipeline traversal (S1 through S8)
4. In-loop refinement and root-cause rollback handling
5. Live execution step using Gemini in agy
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from autoresearch.config import Config
from autoresearch.llm.credentials import AgyCredentialMapper
from autoresearch.llm.agy_client import AgyGeminiClient
from autoresearch.agents.coordinator import WorkflowOrchestrator
from autoresearch.utils.logger import print_banner, print_success, print_info, print_error


def run_smoke_test():
    print_banner("AutoResearch Codeless - Full Workflow Smoke Test", "Validating S1-S8 Pipeline & agy Mapping")

    # Step 1: Verify Credential Mapper & agy Binary
    print_info("[Step 1/3] Checking Antigravity credentials and agy binary...")
    mapper = AgyCredentialMapper()
    status = mapper.check_status()
    if not status.is_valid:
        print_error(f"Credentials check failed: {status.error_message}")
        sys.exit(1)
    print_success(f"agy Binary: {status.agy_binary}")
    print_success(f"OAuth Token: {status.token_preview} (method: {status.auth_method})")

    # Step 2: Run Full Automated Test Suite
    print_info("\n[Step 2/3] Running 20 comprehensive unit, integration & smoke tests...")
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)

    if not result.wasSuccessful():
        print_error(f"Test suite failed with {len(result.failures)} failures and {len(result.errors)} errors.")
        sys.exit(1)
    print_success(f"All {result.testsRun} automated tests PASSED.")

    # Step 3: Verify Live agy Step
    print_info("\n[Step 3/3] Validating Live Gemini in agy execution (demo_project Stage S2)...")
    try:
        orchestrator = WorkflowOrchestrator(project_name="demo_project")
        curr_stage = orchestrator.state.current_stage
        print_info(f"demo_project is at {curr_stage.value}. Executing one live step with gemini-3.8-flash-high...")
        decision = orchestrator.execute_current_stage_step()
        print_success(f"Live execution completed: Action={decision.action.value}, Target={decision.target_stage.value if decision.target_stage else 'N/A'}")
    except Exception as e:
        print_error(f"Live agy step encountered error: {e}")
        sys.exit(1)

    print_banner("Smoke Test Finished Successfully!", "All workflow components and live LLM integration validated.")


if __name__ == "__main__":
    run_smoke_test()
