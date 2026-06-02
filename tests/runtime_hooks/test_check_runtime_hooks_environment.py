from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "runtime-hooks" / "scripts" / "check_runtime_hooks_environment.py"


def load_script_module():
    spec = importlib.util.spec_from_file_location("check_runtime_hooks_environment", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckRuntimeHooksEnvironmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def test_accepts_current_repo_environment(self) -> None:
        result = self.script.evaluate_environment(REPO_ROOT, (3, 10, 11))

        self.assertEqual("pass", result["status"])
        self.assertEqual([], result["blocking_reasons"])
        self.assertEqual("3.10.11", result["python_version"])
        self.assertEqual("3.10", result["minimum_python"])
        self.assertEqual("run-validator-smoke", result["next_allowed_action"])

    def test_blocks_python_older_than_minimum(self) -> None:
        result = self.script.evaluate_environment(REPO_ROOT, (3, 9, 13))

        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "Python 3.10 or newer is required; found 3.9.13",
            result["blocking_reasons"],
        )
        self.assertEqual("fix-environment", result["next_allowed_action"])

    def test_blocks_missing_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.script.evaluate_environment(Path(temp_dir), (3, 10, 11))

        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "required file missing: runtime-hooks/scripts/validate_gate_contract.py",
            result["blocking_reasons"],
        )

    def test_cli_json_output(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(["--repo-root", str(REPO_ROOT), "--json"])

        self.assertEqual(0, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("pass", result["status"])
        self.assertEqual("run-validator-smoke", result["next_allowed_action"])

    def test_cli_markdown_output(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(["--repo-root", str(REPO_ROOT)])

        self.assertEqual(0, code)
        output = stdout.getvalue()
        self.assertIn("Runtime hooks environment", output)
        self.assertIn("Status: pass", output)
        self.assertIn("Next allowed action: run-validator-smoke", output)

    def test_cli_returns_nonzero_for_missing_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = self.script.main(["--repo-root", temp_dir, "--json"])

        self.assertEqual(1, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-environment", result["next_allowed_action"])
