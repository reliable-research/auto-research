"""Tests for template manager (T0-T5)."""

import unittest
import tempfile
import shutil
from pathlib import Path

from autoresearch.workflow.stages import StageId
from autoresearch.workflow.templates import TemplateManager
from autoresearch.workflow.decision_engine import TransitionDecision, ActionType


class TestTemplates(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.tm = TemplateManager(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_initialize_all(self):
        self.tm.initialize_all("TestProject", "TestTopic", "方法 (Method)")
        self.assertTrue(self.tm.t0_path.exists())
        self.assertTrue(self.tm.t1_path.exists())
        self.assertTrue(self.tm.t2_path.exists())
        self.assertTrue(self.tm.t3_path.exists())
        self.assertTrue(self.tm.t4_path.exists())
        self.assertTrue(self.tm.t5_path.exists())

        t0_text = self.tm.t0_path.read_text(encoding="utf-8")
        self.assertIn("TestProject", t0_text)
        self.assertIn("TestTopic", t0_text)

    def test_update_t1_and_t4(self):
        self.tm.initialize_all("TestProject", "TestTopic")

        cards_res = {
            "S1-C1": {"status": "MET", "evidence_location": "Sec 1", "reason": "Verified"},
            "S1-C2": {"status": "GAP", "evidence_location": "None", "reason": "Missing comparison"},
        }
        issues = [
            {
                "issue_id": "ISS-01",
                "card_id": "S1-C2",
                "severity": "BLOCKING",
                "location": "Sec 1.2",
                "actual_content": "No baseline comparison",
                "problem": "Baseline comparison omitted",
                "impact": "Unsubstantiated advantage",
                "owner_stage": "S1",
                "minimal_fix": "Add baseline",
                "acceptance_criteria": "Direct comparison in table",
                "suggested_route": "REFINE_INLOOP",
            }
        ]
        dec = TransitionDecision(
            action=ActionType.REFINE_INLOOP,
            current_stage=StageId.S1,
            target_stage=StageId.S1,
            reason="Card S1-C2 has gap",
        )

        self.tm.update_t1(StageId.S1, 1, cards_res, issues, dec)
        t1_text = self.tm.t1_path.read_text(encoding="utf-8")
        self.assertIn("S1-C1", t1_text)
        self.assertIn("REFINE_INLOOP", t1_text)
        self.assertIn("ISS-01", t1_text)

        # Update T4 rollback
        self.tm.update_t4_rollback(
            current_stage=StageId.S6,
            target_stage=StageId.S3,
            reason="Core hypothesis refuted",
            invalidated_objects=["H_core_mechanism"],
            affected_stages=[StageId.S4, StageId.S5, StageId.S6],
        )
        t4_text = self.tm.t4_path.read_text(encoding="utf-8")
        self.assertIn("ROLLBACK", t4_text)
        self.assertIn("S3", t4_text)
        self.assertIn("NEEDS_RECHECK", t4_text)


if __name__ == "__main__":
    unittest.main()
