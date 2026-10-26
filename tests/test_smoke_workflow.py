"""Comprehensive end-to-end smoke test validating the entire 8-stage research workflow."""

import unittest
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

from autoresearch.config import Config
from autoresearch.llm.base import BaseLLMClient, LLMResponse, TokenUsage
from autoresearch.workflow.stages import StageId, STAGES, STAGE_ORDER, get_stage
from autoresearch.workflow.cards import CARDS, CardStatus, get_cards_for_stage
from autoresearch.workflow.state import ProjectState
from autoresearch.workflow.templates import TemplateManager
from autoresearch.workflow.decision_engine import ActionType, TransitionDecision
from autoresearch.agents.builder import BuilderAgent
from autoresearch.agents.critic import CriticAgent
from autoresearch.agents.controller import ControllerAgent
from autoresearch.agents.coordinator import WorkflowOrchestrator


class MockDeterministicLLMClient(BaseLLMClient):
    """Deterministic LLM client simulating high-quality Builder deliverables and Critic audits."""

    def __init__(self, should_fail_card: Optional[str] = None, fail_owner_stage: Optional[StageId] = None):
        self.should_fail_card = should_fail_card
        self.fail_owner_stage = fail_owner_stage
        self.call_count = 0

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        json_mode: bool = False,
        model: Optional[str] = None,
        effort: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> LLMResponse:
        self.call_count += 1

        if not json_mode:
            # Builder output simulation
            content = f"# Stage Deliverable\n\n- Research unit and verified data.\n- Rigorous evidence citations.\n- Explicit minimal trade-offs."
            return LLMResponse(content=content, status="SUCCESS")

        # Critic output simulation (JSON mode)
        # Check which stage is being audited by inspecting prompt
        cards_dict = {}
        issues = []

        for cid, card in CARDS.items():
            if f"卡项 {cid}" in prompt or f'"{cid}"' in prompt:
                if self.should_fail_card and cid == self.should_fail_card:
                    cards_dict[cid] = {
                        "name": card.name,
                        "status": "GAP",
                        "evidence_location": "Deliverable Section 1",
                        "reason": f"Simulated gap for testing on {cid}",
                    }
                    owner = self.fail_owner_stage or card.target_stage
                    issues.append({
                        "issue_id": f"TEST-ISSUE-{cid}",
                        "card_id": cid,
                        "severity": "BLOCKING",
                        "location": "Deliverable Section 1",
                        "actual_content": "Missing explicit baseline condition",
                        "problem": f"Simulated issue on {cid}",
                        "impact": "Requires refinement or rollback",
                        "owner_stage": owner.value,
                        "minimal_fix": "Add verified baseline comparison",
                        "acceptance_criteria": "Verify inclusion of baseline numbers",
                        "suggested_route": "ROLLBACK" if owner != card.stage_id else "REFINE_INLOOP",
                    })
                else:
                    cards_dict[cid] = {
                        "name": card.name,
                        "status": "MET",
                        "evidence_location": "Deliverable Section 1",
                        "reason": f"Verified compliance with {cid}",
                    }

        parsed_json = {"cards": cards_dict, "issues": issues}
        return LLMResponse(
            content="",
            parsed_json=parsed_json,
            status="SUCCESS",
            usage=TokenUsage(input_tokens=100, output_tokens=100, total_tokens=200),
        )

    def health_check(self) -> bool:
        return True


class TestSmokeWorkflow(unittest.TestCase):
    """End-to-end smoke test suite validating all 8 stages, templates, and state machines."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.config = Config(workspace_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_s1_to_s8_progression(self):
        """Validate an autonomous clean pass through all 8 stages from S1 to S8."""
        project_name = "clean_pass_project"
        mock_client = MockDeterministicLLMClient()

        orchestrator = WorkflowOrchestrator(
            project_name=project_name,
            topic="Formal Verification of Neural Network Controllers",
            config=self.config,
        )
        # Inject deterministic client
        orchestrator.llm = mock_client
        orchestrator.builder = BuilderAgent(mock_client)
        orchestrator.critic = CriticAgent(mock_client)

        # Run pipeline from S1 to S8
        for expected_stage in STAGE_ORDER:
            self.assertEqual(orchestrator.state.current_stage, expected_stage)
            decision = orchestrator.execute_current_stage_step()
            self.assertEqual(decision.action, ActionType.CONTINUE)

            # Check that stage output was saved
            output_file = orchestrator.workspace / f"stage_output_{expected_stage.value}.md"
            self.assertTrue(output_file.exists())

            # Check that T1 was updated
            t1_text = orchestrator.tm.t1_path.read_text(encoding="utf-8")
            self.assertIn(f"阶段：{expected_stage.value}", t1_text)

        # Confirm completion at S8
        self.assertEqual(orchestrator.state.current_stage, StageId.S8)
        self.assertTrue(orchestrator.tm.t5_path.exists())
        t5_text = orchestrator.tm.t5_path.read_text(encoding="utf-8")
        self.assertIn("## 1 ", t5_text)
        self.assertIn("## 8 ", t5_text)

    def test_inloop_refinement_cycle(self):
        """Validate that a current-stage GAP triggers REFINE_INLOOP and clears on round 2."""
        project_name = "refine_test_project"
        # Fail S2-C3 on round 1
        mock_client = MockDeterministicLLMClient(should_fail_card="S2-C3")

        orchestrator = WorkflowOrchestrator(
            project_name=project_name,
            topic="Test Refinement Topic",
            config=self.config,
        )
        orchestrator.llm = mock_client
        orchestrator.builder = BuilderAgent(mock_client)
        orchestrator.critic = CriticAgent(mock_client)
        orchestrator.state.current_stage = StageId.S2

        # Round 1 should REFINE_INLOOP
        decision1 = orchestrator.execute_current_stage_step()
        self.assertEqual(decision1.action, ActionType.REFINE_INLOOP)
        self.assertEqual(orchestrator.state.current_stage, StageId.S2)
        self.assertEqual(orchestrator.state.current_round, 2)
        self.assertEqual(len(orchestrator.state.active_issues), 1)

        # Clear failure for round 2
        mock_client.should_fail_card = None

        decision2 = orchestrator.execute_current_stage_step()
        self.assertEqual(decision2.action, ActionType.CONTINUE)
        self.assertEqual(orchestrator.state.current_stage, StageId.S3)
        self.assertEqual(orchestrator.state.current_round, 1)
        self.assertEqual(len(orchestrator.state.active_issues), 0)

    def test_rollback_to_upstream_stage(self):
        """Validate that an upstream premise failure in S6 causes ROLLBACK to S3, writes T4, and marks recheck."""
        project_name = "rollback_test_project"
        # In S6, card S6-C5 fails with root cause owned by S3
        mock_client = MockDeterministicLLMClient(
            should_fail_card="S6-C5",
            fail_owner_stage=StageId.S3,
        )

        orchestrator = WorkflowOrchestrator(
            project_name=project_name,
            topic="Test Rollback Topic",
            config=self.config,
        )
        orchestrator.llm = mock_client
        orchestrator.builder = BuilderAgent(mock_client)
        orchestrator.critic = CriticAgent(mock_client)
        orchestrator.state.current_stage = StageId.S6

        decision = orchestrator.execute_current_stage_step()
        self.assertEqual(decision.action, ActionType.ROLLBACK)
        self.assertEqual(decision.target_stage, StageId.S3)
        self.assertEqual(orchestrator.state.current_stage, StageId.S3)
        self.assertIn(StageId.S4, decision.affected_stages)
        self.assertIn(StageId.S5, decision.affected_stages)
        self.assertIn(StageId.S6, decision.affected_stages)

        # Check T4 file
        self.assertTrue(orchestrator.tm.t4_path.exists())
        t4_text = orchestrator.tm.t4_path.read_text(encoding="utf-8")
        self.assertIn("ROLLBACK", t4_text)
        self.assertIn("S3", t4_text)
        self.assertIn("NEEDS_RECHECK", t4_text)


if __name__ == "__main__":
    unittest.main()
