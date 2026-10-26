"""Tests for AgyGeminiClient and JSON extraction utilities."""

import unittest
from autoresearch.llm.agy_client import AgyGeminiClient
from autoresearch.utils.json_utils import extract_json


class TestLLMClient(unittest.TestCase):

    def test_json_extraction_from_markdown_fences(self):
        sample = """Here is the review result:
```json
{
  "status": "SUCCESS",
  "score": 95,
  "notes": ["Good empirical foundation"]
}
```
Thank you."""
        parsed = extract_json(sample)
        self.assertEqual(parsed["status"], "SUCCESS")
        self.assertEqual(parsed["score"], 95)
        self.assertEqual(len(parsed["notes"]), 1)

    def test_json_extraction_with_trailing_commas(self):
        sample = """{
            "key1": "value1",
            "key2": "value2",
        }"""
        parsed = extract_json(sample)
        self.assertEqual(parsed["key1"], "value1")
        self.assertEqual(parsed["key2"], "value2")

    def test_live_health_check(self):
        client = AgyGeminiClient(model="gemini-3.8-flash-low")
        is_healthy = client.health_check()
        self.assertTrue(is_healthy)


if __name__ == "__main__":
    unittest.main()
