import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / ".agent" / "tools" / "state.py"
SPEC = importlib.util.spec_from_file_location("codeharness_state", MODULE_PATH)
state = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(state)

class StateTests(unittest.TestCase):
    def test_legal_transition(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "STATE.json"
            path.write_text(json.dumps({"status":"PLAN","attempt":0,"max_attempts":3}), encoding="utf-8")
            with mock.patch.object(state, "STATE_PATH", path):
                result = state.transition("READY_LOCAL", "task ready")
            self.assertEqual(result["status"], "READY_LOCAL")

    def test_illegal_transition_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "STATE.json"
            path.write_text(json.dumps({"status":"PLAN","attempt":0,"max_attempts":3}), encoding="utf-8")
            with mock.patch.object(state, "STATE_PATH", path):
                with self.assertRaises(SystemExit):
                    state.transition("ACCEPTED", "not allowed")

    def test_rework_limit_escalates(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "STATE.json"
            path.write_text(json.dumps({"status":"READY_REVIEW","attempt":3,"max_attempts":3}), encoding="utf-8")
            with mock.patch.object(state, "STATE_PATH", path):
                result = state.transition("REWORK", "still failing")
            self.assertEqual(result["status"], "NEEDS_HUMAN")

if __name__ == "__main__":
    unittest.main()
