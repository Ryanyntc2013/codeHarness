import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / ".agent" / "tools" / "verify.py"
SPEC = importlib.util.spec_from_file_location("codeharness_verify", MODULE_PATH)
verify = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(verify)

class VerifyTests(unittest.TestCase):
    def test_success_command(self):
        result = verify.run('python -c "print(123)"', 10)
        self.assertTrue(result["passed"])
        self.assertEqual(result["returncode"], 0)
        self.assertIn("123", result["stdout"])

    def test_failure_command(self):
        result = verify.run('python -c "raise SystemExit(7)"', 10)
        self.assertFalse(result["passed"])
        self.assertEqual(result["returncode"], 7)

if __name__ == "__main__":
    unittest.main()
