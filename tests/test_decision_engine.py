"""Tests for decision engine and rollback adjudication logic."""

import unittest
from autoresearch.workflow.stages import StageId
from autoresearch.workflow.cards import CardStatus
from autoresearch.workflow.decision_engine import (
    DecisionAdjudicator,
    DecisionIssue,
    ActionType,
)


class TestDecisionEngine(unittest.TestCase):

    def test_all_met_advances_to_next_stage(self):
        statuses = {f"S1-C{i}": CardStatus.MET for i in range(1, 7)}
        decision = DecisionAdjudicator.adjudicate(
            current_stage=StageId.S1,
            card_statuses=statuses,
            issues=[],
            current_round=1,
            max_rounds=3,
        )
        self.assertEqual(decision.action, ActionType.CONTINUE)
        self.assertEqual(decision.target_stage, StageId.S2)

    def test_s8_all_met_completes(self):
        statuses = {f"S8-C{i}": CardStatus.MET for i in range(1, 7)}
        decision = DecisionAdjudicator.adjudicate(
            current_stage=StageId.S8,
            card_statuses=statuses,
            issues=[],
            current_round=1,
            max_rounds=3,
        )
        self.assertEqual(decision.action, ActionType.CONTINUE)
        self.assertIsNone(decision.target_stage)

    def test_current_stage_blocking_issue_triggers_refine_inloop(self):
        statuses = {f"S2-C{i}": CardStatus.MET for i in range(1, 6)}
        statuses["S2-C6"] = CardStatus.GAP
        issue = DecisionIssue(
            issue_id="ISS-01",
            card_id="S2-C6",
            severity="BLOCKING",
            location="Section 2",
            problem="Slice is too narrow",
            owner_stage=StageId.S2,
            minimal_fix="Broaden scope",
            acceptance_criteria="Verify broader applicability",
        )
        decision = DecisionAdjudicator.adjudicate(
            current_stage=StageId.S2,
            card_statuses=statuses,
            issues=[issue],
            current_round=1,
            max_rounds=3,
        )
        self.assertEqual(decision.action, ActionType.REFINE_INLOOP)
        self.assertEqual(decision.target_stage, StageId.S2)

    def test_budget_exhaustion_triggers_pause(self):
        statuses = {f"S2-C{i}": CardStatus.GAP for i in range(1, 7)}
        decision = DecisionAdjudicator.adjudicate(
            current_stage=StageId.S2,
            card_statuses=statuses,
            issues=[],
            current_round=3,
            max_rounds=3,
        )
        self.assertEqual(decision.action, ActionType.PAUSE)

    def test_upstream_premise_failure_triggers_rollback(self):
        # In S6, an issue belongs to S3 (core hypothesis falsified)
        statuses = {f"S6-C{i}": CardStatus.CONFLICT for i in range(1, 7)}
        upstream_issue = DecisionIssue(
            issue_id="ISS-S6-01",
            card_id="S6-C5",
            severity="BLOCKING",
            location="Table 3",
            problem="Negative result refutes core mechanism hypothesis",
            owner_stage=StageId.S3,
            minimal_fix="Reformulate mechanism hypothesis in S3",
            acceptance_criteria="New testable prediction formulated",
        )
        decision = DecisionAdjudicator.adjudicate(
            current_stage=StageId.S6,
            card_statuses=statuses,
            issues=[upstream_issue],
            current_round=1,
            max_rounds=3,
        )
        self.assertEqual(decision.action, ActionType.ROLLBACK)
        self.assertEqual(decision.target_stage, StageId.S3)
        self.assertIn(StageId.S4, decision.affected_stages)
        self.assertIn(StageId.S5, decision.affected_stages)
        self.assertIn(StageId.S6, decision.affected_stages)


if __name__ == "__main__":
    unittest.main()
