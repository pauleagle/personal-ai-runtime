from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    REPO_ROOT
    / "agent-skills"
    / "orchestrator-state-machine"
    / "scripts"
    / "validate_orchestrator_state.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("validate_orchestrator_state", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateOrchestratorStateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_script(self, state_file: Path):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([str(state_file), "--json"])
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_accepts_minimal_valid_state(self) -> None:
        state_file = self.workspace / "state.json"
        state_file.write_text(
            json.dumps(
                {
                    "workflow_step": "Step 11 - Test Execution",
                    "implementation_status": "in-progress",
                    "ready": [],
                    "running": [],
                    "blocked": [],
                    "completed": [],
                }
            ),
            encoding="utf-8",
        )

        code, result, stderr = self.run_script(state_file)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])

    def test_rejects_missing_required_fields(self) -> None:
        state_file = self.workspace / "state.json"
        state_file.write_text(json.dumps({"workflow_step": "Step 5"}), encoding="utf-8")

        code, result, stderr = self.run_script(state_file)

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        messages = [finding["message"] for finding in result["findings"]]
        self.assertIn("missing required field: implementation_status", messages)

    def test_rejects_non_list_queue(self) -> None:
        state_file = self.workspace / "state.json"
        state_file.write_text(
            json.dumps(
                {
                    "workflow_step": "Step 5",
                    "implementation_status": "in-progress",
                    "ready": "job-1",
                    "running": [],
                    "blocked": [],
                    "completed": [],
                }
            ),
            encoding="utf-8",
        )

        code, result, _stderr = self.run_script(state_file)

        self.assertEqual(1, code)
        self.assertFalse(result["valid"])
        self.assertTrue(any("ready must be a list" == item["message"] for item in result["findings"]))
