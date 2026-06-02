from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
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
        self.assertIsNone(result["handoff_note_path"])

    def test_writes_handoff_note_artifact_when_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            handoff_path = Path(temp_dir) / "handoff" / "blocked-pre-edit.json"
            result = self.script.enforce_pre_edit_gate(
                REPO_ROOT,
                BLOCKED_PRE_EDIT_CONTRACT,
                handoff_note_out=handoff_path,
            )

            self.assertEqual("blocked", result["status"])
            self.assertEqual(str(handoff_path), result["handoff_note_path"])
            self.assertTrue(handoff_path.is_file())
            handoff_note = json.loads(handoff_path.read_text(encoding="utf-8"))

        self.assertEqual("HOOK-MVP-001-A22", handoff_note["atomic_item_id"])
        self.assertEqual("pre-edit", handoff_note["gate"])
        self.assertEqual("blocked", handoff_note["gate_status"])
        self.assertEqual("handoff", handoff_note["next_allowed_action"])

    def test_writes_relative_handoff_note_artifact_under_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / "runtime-hooks" / "scripts").mkdir(parents=True)
            (repo_root / "runtime-hooks" / "examples").mkdir(parents=True)
            validator_source = REPO_ROOT / "runtime-hooks" / "scripts" / "validate_gate_contract.py"
            contract_source = REPO_ROOT / BLOCKED_PRE_EDIT_CONTRACT
            (repo_root / "runtime-hooks" / "scripts" / "validate_gate_contract.py").write_text(
                validator_source.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (repo_root / BLOCKED_PRE_EDIT_CONTRACT).write_text(
                contract_source.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            result = self.script.enforce_pre_edit_gate(
                repo_root,
                BLOCKED_PRE_EDIT_CONTRACT,
                handoff_note_out="runtime-hooks/handoffs/blocked.json",
            )
            expected_path = repo_root / "runtime-hooks" / "handoffs" / "blocked.json"

            self.assertEqual("blocked", result["status"])
            self.assertEqual(str(expected_path), result["handoff_note_path"])
            self.assertTrue(expected_path.is_file())

    def test_does_not_write_handoff_note_artifact_when_passing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            handoff_path = Path(temp_dir) / "handoff.json"
            result = self.script.enforce_pre_edit_gate(
                REPO_ROOT,
                PASSING_PRE_EDIT_CONTRACT,
                handoff_note_out=handoff_path,
            )

            self.assertEqual("pass", result["status"])
            self.assertIsNone(result["handoff_note_path"])
            self.assertFalse(handoff_path.exists())

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

    def test_cli_writes_handoff_note_artifact_for_blocked_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            handoff_path = Path(temp_dir) / "handoff.json"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = self.script.main(
                    [
                        BLOCKED_PRE_EDIT_CONTRACT,
                        "--repo-root",
                        str(REPO_ROOT),
                        "--handoff-note-out",
                        str(handoff_path),
                        "--json",
                    ]
                )
            handoff_note = json.loads(handoff_path.read_text(encoding="utf-8"))

        self.assertEqual(1, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual(str(handoff_path), result["handoff_note_path"])
        self.assertEqual("HOOK-MVP-001-A22", handoff_note["atomic_item_id"])
