from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "runtime-hooks" / "scripts" / "enforce_pre_edit_gate.py"
PASSING_PRE_EDIT_CONTRACT = (
    "runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json"
)
BLOCKED_PRE_EDIT_CONTRACT = (
    "runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json"
)
PRE_RUN_CONTRACT = "runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json"


def load_script_module():
    spec = importlib.util.spec_from_file_location("enforce_pre_edit_gate", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EnforcePreEditGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def test_allows_edit_for_passing_pre_edit_contract(self) -> None:
        result = self.script.enforce_pre_edit_gate(REPO_ROOT, PASSING_PRE_EDIT_CONTRACT)

        self.assertEqual("pass", result["status"])
        self.assertTrue(result["allowed_to_edit"])
        self.assertEqual("edit", result["next_allowed_action"])
        self.assertEqual("pre-edit", result["gate_result"]["gate"])
        self.assertIsNone(result["handoff_note"])

    def test_blocks_and_emits_handoff_for_blocked_pre_edit_contract(self) -> None:
        result = self.script.enforce_pre_edit_gate(REPO_ROOT, BLOCKED_PRE_EDIT_CONTRACT)

        self.assertEqual("blocked", result["status"])
        self.assertFalse(result["allowed_to_edit"])
        self.assertEqual("handoff", result["next_allowed_action"])
        self.assertIsNotNone(result["handoff_note"])
        self.assertEqual("HOOK-MVP-001-A22", result["handoff_note"]["atomic_item_id"])
        self.assertIn(
            "proposed file is outside allowed_scope: agent-skills/example/SKILL.md",
            result["blocking_reasons"],
        )

    def test_blocks_non_pre_edit_contract(self) -> None:
        result = self.script.enforce_pre_edit_gate(REPO_ROOT, PRE_RUN_CONTRACT)

        self.assertEqual("blocked", result["status"])
        self.assertFalse(result["allowed_to_edit"])
        self.assertEqual("handoff", result["next_allowed_action"])
        self.assertIn(
            "mounted pre-edit guard requires gate: pre-edit",
            result["blocking_reasons"],
        )

    def test_cli_json_output_for_passing_contract(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(
                [
                    PASSING_PRE_EDIT_CONTRACT,
                    "--repo-root",
                    str(REPO_ROOT),
                    "--json",
                ]
            )

        self.assertEqual(0, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("pass", result["status"])
        self.assertTrue(result["allowed_to_edit"])

    def test_cli_returns_nonzero_for_blocked_contract(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(
                [
                    BLOCKED_PRE_EDIT_CONTRACT,
                    "--repo-root",
                    str(REPO_ROOT),
                    "--json",
                ]
            )

        self.assertEqual(1, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("blocked", result["status"])
        self.assertFalse(result["allowed_to_edit"])
        self.assertIsNotNone(result["handoff_note"])
