"""Tests for stage and card definitions."""

import unittest
from autoresearch.workflow.stages import StageId, STAGES, STAGE_ORDER, get_stage, get_next_stage, get_previous_stage
from autoresearch.workflow.cards import CARDS, CardStatus, get_card, get_cards_for_stage


class TestCardsAndStages(unittest.TestCase):

    def test_eight_stages_exist(self):
        self.assertEqual(len(STAGE_ORDER), 8)
        self.assertEqual(len(STAGES), 8)
        for s_id in STAGE_ORDER:
            st = get_stage(s_id)
            self.assertEqual(st.id, s_id)
            self.assertTrue(len(st.cards) == 6, f"Stage {s_id} does not have 6 cards")

    def test_forty_eight_cards_exist(self):
        self.assertEqual(len(CARDS), 48)
        for cid, card in CARDS.items():
            self.assertEqual(cid, card.card_id)
            self.assertIn(card.stage_id, STAGES)
            self.assertTrue(bool(card.name))
            self.assertTrue(bool(card.why_check))
            self.assertTrue(bool(card.where_to_check))
            self.assertTrue(bool(card.how_to_check))
            self.assertTrue(bool(card.what_counts_as_problem))
            self.assertTrue(bool(card.expected_deliverable))
            self.assertTrue(bool(card.minimal_fix))
            self.assertTrue(bool(card.acceptance_criteria))

    def test_stage_transitions(self):
        self.assertEqual(get_next_stage(StageId.S1), StageId.S2)
        self.assertEqual(get_next_stage(StageId.S7), StageId.S8)
        self.assertIsNone(get_next_stage(StageId.S8))

        self.assertEqual(get_previous_stage(StageId.S2), StageId.S1)
        self.assertEqual(get_previous_stage(StageId.S8), StageId.S7)
        self.assertIsNone(get_previous_stage(StageId.S1))

    def test_get_cards_for_stage(self):
        s1_cards = get_cards_for_stage(StageId.S1)
        self.assertEqual(len(s1_cards), 6)
        card_ids = [c.card_id for c in s1_cards]
        self.assertEqual(card_ids, ["S1-C1", "S1-C2", "S1-C3", "S1-C4", "S1-C5", "S1-C6"])


if __name__ == "__main__":
    unittest.main()
