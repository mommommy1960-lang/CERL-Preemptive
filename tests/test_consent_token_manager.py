import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cerl_preemptive import consent_token_manager as tokens


class ConsentTokenTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path_patch = patch.object(tokens, "TOKENS", Path(self.temp.name) / "tokens.jsonl")
        self.path_patch.start()

    def tearDown(self):
        self.path_patch.stop()
        self.temp.cleanup()

    def test_actor_scope_expiry_and_revocation(self):
        with patch.object(tokens.time, "time", return_value=1000):
            token = tokens.issue_token("alice", "read", expiry_hours=1)
            self.assertTrue(tokens.validate_token(token, "alice", "read"))
            self.assertFalse(tokens.validate_token(token, "bob", "read"))
            self.assertFalse(tokens.validate_token(token, "alice", "write"))
        with patch.object(tokens.time, "time", return_value=4600):
            self.assertFalse(tokens.validate_token(token, "alice", "read"))
        tokens.revoke_token(token)
        with patch.object(tokens.time, "time", return_value=1001):
            self.assertFalse(tokens.validate_token(token, "alice", "read"))

    def test_unknown_malformed_and_invalid_issue_fail_closed(self):
        self.assertFalse(tokens.validate_token("unknown"))
        with self.assertRaises(ValueError):
            tokens.issue_token("alice", "read", expiry_hours=0)
        tokens.TOKENS.write_text("{bad json\n")
        self.assertFalse(tokens.validate_token("anything"))


if __name__ == "__main__":
    unittest.main()
