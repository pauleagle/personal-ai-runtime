from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "runtime-hooks" / "scripts" / "run_runtime_hooks_smoke.py"
ACTIVE_ITEM_CONTRACT = "runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json"
ACTIVE_ITEM_CONTRACTS = [
    "runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json",
    "runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json",
    "runtime-hooks/examples/hook_mvp_001_a18_post_run_contract.json",
]
PASSING_STATE_PATCH_PROPOSAL = (
    "runtime-hooks/examples/hook_mvp_001_a40_gate_result_state_patch_proposal.json"
)
MATCHING_STATE_PATCH_PROPOSAL = (
    "runtime-hooks/examples/hook_mvp_001_a47_gate_result_state_patch_proposal.json"
)
BLOCKED_STATE_PATCH_PROPOSAL = (
    "runtime-hooks/examples/hook_mvp_001_a41_blocked_gate_result_state_patch_proposal.json"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("run_runtime_hooks_smoke", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RunRuntimeHooksSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def test_accepts_current_repo_smoke(self) -> None:
        result = self.script.run_smoke(REPO_ROOT, (3, 10, 11))

        self.assertEqual("pass", result["status"])
        self.assertEqual([], result["blocking_reasons"])
        self.assertEqual("pass", result["environment"]["status"])
        self.assertEqual("ready", result["next_allowed_action"])
        self.assertEqual(
            [
                "tests/fixtures/gate_contract_pre_run_sample.json",
                "tests/fixtures/gate_contract_pre_edit_sample.json",
                "tests/fixtures/gate_contract_post_run_sample.json",
            ],
            result["contract_paths"],
        )
        self.assertEqual(3, len(result["gate_results"]))
        self.assertEqual([], result["state_patch_proposal_paths"])
        self.assertEqual([], result["state_patch_proposal_results"])
        self.assertEqual([], result["consistency_checks"])
        self.assertTrue(all(item["status"] == "pass" for item in result["gate_results"]))
        self.assertEqual("pre-edit", result["pre_edit_guard"]["hook"])
        self.assertEqual("pass", result["pre_edit_guard"]["status"])
        self.assertTrue(result["pre_edit_guard"]["allowed_to_edit"])

    def test_accepts_explicit_contract_list(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["tests/fixtures/gate_contract_pre_run_sample.json"],
        )

        self.assertEqual("pass", result["status"])
        self.assertEqual(["tests/fixtures/gate_contract_pre_run_sample.json"], result["contract_paths"])
        self.assertEqual(1, len(result["gate_results"]))
        self.assertEqual("pre-run", result["gate_results"][0]["gate"])
        self.assertIsNone(result["pre_edit_guard"])

    def test_accepts_explicit_state_patch_proposals(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["tests/fixtures/gate_contract_pre_run_sample.json"],
            [PASSING_STATE_PATCH_PROPOSAL, BLOCKED_STATE_PATCH_PROPOSAL],
        )

        self.assertEqual("pass", result["status"])
        self.assertEqual(
            [PASSING_STATE_PATCH_PROPOSAL, BLOCKED_STATE_PATCH_PROPOSAL],
            result["state_patch_proposal_paths"],
        )
        self.assertEqual(2, len(result["state_patch_proposal_results"]))
        self.assertEqual(
            "runtime-hooks/contracts/hook_mvp_001_a40_pre_edit_contract.json",
            result["state_patch_proposal_results"][0]["source_gate_contract"],
        )
        self.assertEqual(
            "runtime-hooks/contracts/hook_mvp_001_a40_pre_edit_contract.json",
            result["state_patch_proposal_results"][0]["validation_artifact"],
        )
        self.assertEqual("pass", result["state_patch_proposal_results"][0]["gate_status"])
        self.assertEqual("blocked", result["state_patch_proposal_results"][1]["gate_status"])
        self.assertTrue(
            all(item["status"] == "pass" for item in result["state_patch_proposal_results"])
        )

    def test_blocks_invalid_state_patch_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_proposal = Path(temp_dir) / "invalid_proposal.json"
            invalid_proposal.write_text("{}", encoding="utf-8")
            result = self.script.run_smoke(
                REPO_ROOT,
                (3, 10, 11),
                ["tests/fixtures/gate_contract_pre_run_sample.json"],
                [str(invalid_proposal)],
            )

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertEqual(1, len(result["state_patch_proposal_results"]))
        self.assertTrue(
            any(
                "missing required field: atomic_item_id" in reason
                for reason in result["blocking_reasons"]
            )
        )

    def test_blocks_when_state_patch_proposal_is_required_but_not_selected(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["tests/fixtures/gate_contract_pre_run_sample.json"],
            require_state_patch_proposal=True,
        )

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertEqual([], result["state_patch_proposal_results"])
        self.assertIn(
            "state patch proposal required but no state patch proposal was selected",
            result["blocking_reasons"],
        )

    def test_accepts_required_state_patch_proposal_when_selected(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["tests/fixtures/gate_contract_pre_run_sample.json"],
            [PASSING_STATE_PATCH_PROPOSAL],
            require_state_patch_proposal=True,
        )

        self.assertEqual("pass", result["status"])
        self.assertEqual(1, len(result["state_patch_proposal_results"]))
        self.assertEqual("pass", result["state_patch_proposal_results"][0]["status"])

    def test_accepts_matching_required_pre_edit_guard_and_state_patch_proposal(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["runtime-hooks/contracts/hook_mvp_001_a47_pre_edit_contract.json"],
            [MATCHING_STATE_PATCH_PROPOSAL],
            require_pre_edit_guard=True,
            require_state_patch_proposal=True,
        )

        self.assertEqual("pass", result["status"])
        self.assertEqual("pass", result["pre_edit_guard"]["status"])
        self.assertEqual("pass", result["state_patch_proposal_results"][0]["gate_status"])
        self.assertEqual("pass", result["consistency_checks"][0]["status"])
        self.assertEqual(
            "pre-edit-guard-state-patch-proposal",
            result["consistency_checks"][0]["item"],
        )
        self.assertEqual(
            "runtime-hooks/contracts/hook_mvp_001_a47_pre_edit_contract.json",
            result["consistency_checks"][0]["expected_contract_path"],
        )

    def test_blocks_stale_state_patch_proposal_for_different_contract(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["runtime-hooks/contracts/hook_mvp_001_a47_pre_edit_contract.json"],
            [PASSING_STATE_PATCH_PROPOSAL],
            require_pre_edit_guard=True,
            require_state_patch_proposal=True,
        )

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertIn(
            (
                "state patch proposal does not match selected pre-edit contract "
                "and guard status: runtime-hooks/contracts/hook_mvp_001_a47_pre_edit_contract.json"
            ),
            result["blocking_reasons"],
        )
        self.assertEqual("blocked", result["consistency_checks"][0]["status"])

    def test_blocks_mismatched_required_pre_edit_guard_and_state_patch_proposal(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["tests/fixtures/gate_contract_pre_edit_sample.json"],
            [BLOCKED_STATE_PATCH_PROPOSAL],
            require_pre_edit_guard=True,
            require_state_patch_proposal=True,
        )

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertIn(
            (
                "state patch proposal does not match selected pre-edit contract "
                "and guard status: tests/fixtures/gate_contract_pre_edit_sample.json"
            ),
            result["blocking_reasons"],
        )
        self.assertEqual("blocked", result["consistency_checks"][0]["status"])
        self.assertEqual("pass", result["consistency_checks"][0]["guard_status"])

    def test_blocked_pre_edit_guard_matches_blocked_state_patch_proposal(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json"],
            [BLOCKED_STATE_PATCH_PROPOSAL],
            require_pre_edit_guard=True,
            require_state_patch_proposal=True,
        )

        self.assertEqual("blocked", result["status"])
        self.assertEqual("blocked", result["pre_edit_guard"]["status"])
        self.assertEqual("blocked", result["state_patch_proposal_results"][0]["gate_status"])
        self.assertEqual("pass", result["consistency_checks"][0]["status"])
        self.assertNotIn(
            "state patch proposal gate_status does not match pre-edit guard status: blocked",
            result["blocking_reasons"],
        )

    def test_blocks_when_pre_edit_guard_is_required_but_not_selected(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["tests/fixtures/gate_contract_pre_run_sample.json"],
            require_pre_edit_guard=True,
        )

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertIsNone(result["pre_edit_guard"])
        self.assertIn(
            "pre-edit guard required but no pre-edit contract was selected",
            result["blocking_reasons"],
        )

    def test_accepts_required_pre_edit_guard_when_selected(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["tests/fixtures/gate_contract_pre_edit_sample.json"],
            require_pre_edit_guard=True,
        )

        self.assertEqual("pass", result["status"])
        self.assertEqual("pass", result["pre_edit_guard"]["status"])
        self.assertTrue(result["pre_edit_guard"]["allowed_to_edit"])

    def test_accepts_active_item_contract_example(self) -> None:
        result = self.script.run_smoke(REPO_ROOT, (3, 10, 11), [ACTIVE_ITEM_CONTRACT])

        self.assertEqual("pass", result["status"])
        self.assertEqual([ACTIVE_ITEM_CONTRACT], result["contract_paths"])
        self.assertEqual(1, len(result["gate_results"]))
        self.assertEqual("pre-run", result["gate_results"][0]["gate"])
        self.assertEqual("ready", result["next_allowed_action"])

    def test_accepts_all_active_item_contract_examples(self) -> None:
        result = self.script.run_smoke(REPO_ROOT, (3, 10, 11), ACTIVE_ITEM_CONTRACTS)

        self.assertEqual("pass", result["status"])
        self.assertEqual(ACTIVE_ITEM_CONTRACTS, result["contract_paths"])
        self.assertEqual(["pre-run", "pre-edit", "post-run"], [item["gate"] for item in result["gate_results"]])
        self.assertTrue(all(item["status"] == "pass" for item in result["gate_results"]))
        self.assertEqual("ready", result["next_allowed_action"])
        self.assertEqual("pass", result["pre_edit_guard"]["status"])
        self.assertTrue(result["pre_edit_guard"]["allowed_to_edit"])

    def test_blocks_explicit_invalid_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_contract = Path(temp_dir) / "invalid_gate.json"
            invalid_contract.write_text("{}", encoding="utf-8")
            result = self.script.run_smoke(REPO_ROOT, (3, 10, 11), [str(invalid_contract)])

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertEqual(1, len(result["gate_results"]))
        self.assertIsNone(result["pre_edit_guard"])
        self.assertTrue(
            any(
                "missing required field: atomic_item_id" in reason
                for reason in result["blocking_reasons"]
            )
        )

    def test_blocks_when_environment_is_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.script.run_smoke(Path(temp_dir), (3, 10, 11))

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-environment", result["next_allowed_action"])
        self.assertEqual([], result["gate_results"])
        self.assertIsNone(result["pre_edit_guard"])
        self.assertEqual([], result["consistency_checks"])
        self.assertIn(
            "unable to load environment helper",
            result["blocking_reasons"][0],
        )

    def test_blocks_old_python_before_loading_validator(self) -> None:
        result = self.script.run_smoke(REPO_ROOT, (3, 9, 13))

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-environment", result["next_allowed_action"])
        self.assertEqual([], result["gate_results"])
        self.assertIsNone(result["pre_edit_guard"])
        self.assertIn(
            "Python 3.10 or newer is required; found 3.9.13",
            result["blocking_reasons"],
        )

    def test_cli_json_output(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(["--repo-root", str(REPO_ROOT), "--json"])

        self.assertEqual(0, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("pass", result["status"])
        self.assertEqual("ready", result["next_allowed_action"])
        self.assertEqual("pass", result["pre_edit_guard"]["status"])

    def test_cli_markdown_output(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(["--repo-root", str(REPO_ROOT)])

        self.assertEqual(0, code)
        output = stdout.getvalue()
        self.assertIn("Runtime hooks smoke", output)
        self.assertIn("Status: pass", output)
        self.assertIn("Next allowed action: ready", output)
        self.assertIn("### Pre-Edit Guard", output)
        self.assertIn("### State Patch Proposal Results", output)
        self.assertIn("### Consistency Checks", output)

    def test_cli_accepts_explicit_contract(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(
                [
                    "--repo-root",
                    str(REPO_ROOT),
                    "--contract",
                    "tests/fixtures/gate_contract_pre_run_sample.json",
                    "--state-patch-proposal",
                    PASSING_STATE_PATCH_PROPOSAL,
                    "--json",
                ]
            )

        self.assertEqual(0, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual(["tests/fixtures/gate_contract_pre_run_sample.json"], result["contract_paths"])
        self.assertEqual([PASSING_STATE_PATCH_PROPOSAL], result["state_patch_proposal_paths"])
        self.assertEqual(1, len(result["state_patch_proposal_results"]))
        self.assertEqual(1, len(result["gate_results"]))
        self.assertIsNone(result["pre_edit_guard"])

    def test_cli_returns_nonzero_for_invalid_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_contract = Path(temp_dir) / "invalid_gate.json"
            invalid_contract.write_text("{}", encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = self.script.main(
                    [
                        "--repo-root",
                        str(REPO_ROOT),
                        "--contract",
                        str(invalid_contract),
                        "--json",
                    ]
                )

        self.assertEqual(1, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertIsNone(result["pre_edit_guard"])

    def test_blocks_when_explicit_pre_edit_guard_blocks(self) -> None:
        result = self.script.run_smoke(
            REPO_ROOT,
            (3, 10, 11),
            ["runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json"],
        )

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertEqual("blocked", result["pre_edit_guard"]["status"])
        self.assertFalse(result["pre_edit_guard"]["allowed_to_edit"])
        self.assertTrue(
            any(
                "pre-edit guard: proposed file is outside allowed_scope" in reason
                for reason in result["blocking_reasons"]
            )
        )

    def test_writes_pre_edit_guard_handoff_note_from_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            handoff_path = Path(temp_dir) / "smoke-handoff.json"
            result = self.script.run_smoke(
                REPO_ROOT,
                (3, 10, 11),
                ["runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json"],
                pre_edit_handoff_note_out=handoff_path,
            )
            handoff_note = json.loads(handoff_path.read_text(encoding="utf-8"))

        self.assertEqual("blocked", result["status"])
        self.assertEqual(str(handoff_path), result["pre_edit_guard"]["handoff_note_path"])
        self.assertEqual("HOOK-MVP-001-A22", handoff_note["atomic_item_id"])
        self.assertEqual("blocked", handoff_note["gate_status"])

    def test_blocks_when_handoff_output_requested_without_pre_edit_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            handoff_path = Path(temp_dir) / "smoke-handoff.json"
            result = self.script.run_smoke(
                REPO_ROOT,
                (3, 10, 11),
                ["tests/fixtures/gate_contract_pre_run_sample.json"],
                pre_edit_handoff_note_out=handoff_path,
            )

            self.assertEqual("blocked", result["status"])
            self.assertEqual("fix-contracts", result["next_allowed_action"])
            self.assertIsNone(result["pre_edit_guard"])
            self.assertFalse(handoff_path.exists())
            self.assertIn(
                "pre-edit handoff output requested but no pre-edit contract was selected",
                result["blocking_reasons"],
            )

    def test_passing_smoke_does_not_write_pre_edit_handoff_note(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            handoff_path = Path(temp_dir) / "smoke-handoff.json"
            result = self.script.run_smoke(
                REPO_ROOT,
                (3, 10, 11),
                ["tests/fixtures/gate_contract_pre_edit_sample.json"],
                pre_edit_handoff_note_out=handoff_path,
            )

            self.assertEqual("pass", result["status"])
            self.assertIsNone(result["pre_edit_guard"]["handoff_note_path"])
            self.assertFalse(handoff_path.exists())

    def test_cli_writes_pre_edit_guard_handoff_note_from_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            handoff_path = Path(temp_dir) / "smoke-handoff.json"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = self.script.main(
                    [
                        "--repo-root",
                        str(REPO_ROOT),
                        "--contract",
                        "runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json",
                        "--pre-edit-handoff-note-out",
                        str(handoff_path),
                        "--json",
                    ]
                )
            handoff_note = json.loads(handoff_path.read_text(encoding="utf-8"))

        self.assertEqual(1, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual(str(handoff_path), result["pre_edit_guard"]["handoff_note_path"])
        self.assertEqual("HOOK-MVP-001-A22", handoff_note["atomic_item_id"])
        self.assertIn("run_runtime_hooks_smoke.py", handoff_note["attempted_command"])
        self.assertIn("--pre-edit-handoff-note-out", handoff_note["attempted_command"])

    def test_cli_blocks_when_required_pre_edit_guard_is_missing(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(
                [
                    "--repo-root",
                    str(REPO_ROOT),
                    "--contract",
                    "tests/fixtures/gate_contract_pre_run_sample.json",
                    "--require-pre-edit-guard",
                    "--json",
                ]
            )

        self.assertEqual(1, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "pre-edit guard required but no pre-edit contract was selected",
            result["blocking_reasons"],
        )

    def test_cli_blocks_when_required_state_patch_proposal_is_missing(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(
                [
                    "--repo-root",
                    str(REPO_ROOT),
                    "--contract",
                    "tests/fixtures/gate_contract_pre_run_sample.json",
                    "--require-state-patch-proposal",
                    "--json",
                ]
            )

        self.assertEqual(1, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "state patch proposal required but no state patch proposal was selected",
            result["blocking_reasons"],
        )

    def test_cli_blocks_when_handoff_output_requested_without_pre_edit_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            handoff_path = Path(temp_dir) / "smoke-handoff.json"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = self.script.main(
                    [
                        "--repo-root",
                        str(REPO_ROOT),
                        "--contract",
                        "tests/fixtures/gate_contract_pre_run_sample.json",
                        "--pre-edit-handoff-note-out",
                        str(handoff_path),
                        "--json",
                    ]
                )

            self.assertFalse(handoff_path.exists())

        self.assertEqual(1, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "pre-edit handoff output requested but no pre-edit contract was selected",
            result["blocking_reasons"],
        )
