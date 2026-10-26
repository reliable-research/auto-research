"""Tests for AgyCredentialMapper."""

import unittest
from autoresearch.llm.credentials import AgyCredentialMapper


class TestCredentials(unittest.TestCase):

    def test_mapper_discovery(self):
        mapper = AgyCredentialMapper()
        status = mapper.check_status()
        self.assertIsNotNone(status.agy_binary)
        self.assertTrue(status.is_valid, f"Expected valid auth, got: {status.error_message}")
        self.assertIsNotNone(status.token_preview)

    def test_get_auth_headers(self):
        mapper = AgyCredentialMapper()
        headers = mapper.get_auth_headers()
        self.assertIn("Authorization", headers)
        self.assertTrue(headers["Authorization"].startswith("Bearer ya29."))

    def test_get_token_details(self):
        mapper = AgyCredentialMapper()
        details = mapper.get_token_details()
        self.assertIn("access_token", details)
        self.assertEqual(details.get("token_type"), "Bearer")


if __name__ == "__main__":
    unittest.main()
