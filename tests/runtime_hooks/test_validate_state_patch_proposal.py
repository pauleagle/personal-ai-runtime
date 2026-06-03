from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "runtime-hooks" / "scripts" / "validate_state_patch_proposal.py"
PASSING_PROPOSAL = (
    REPO_ROOT
    / "runtime-hooks"
    / "examples"
    / "hook_mvp_001_a40_gate_result_state_patch_proposal.json"
)
BLOCKED_PROPOSAL = (
    REPO_ROOT
    / "runtime-hooks"
    / "examples"
    / "hook_mvp_001_a41_blocked_gate_result_state_patch_proposal.json"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("validate_state_patch_proposal", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateStatePatchProposalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_proposal(self, proposal: object) -> Path:
        proposal_file = self.workspace / "proposal.json"
        proposal_file.write_text(json.dumps(proposal), encoding="utf-8")
        return proposal_file

    def run_script(self, proposal_file: Path):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([str(proposal_file), "--json"])
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def valid_pass_proposal(self) -> dict[str, object]:
        return json.loads(PASSING_PROPOSAL.read_text(encoding="utf-8"))

    def test_accepts_passing_patch_proposal_example(self) -> None:
        code, result, stderr = self.run_script(PASSING_PROPOSAL)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("pass", result["status"])
        self.assertEqual("HOOK-MVP-001-A40", result["atomic_item_id"])
        self.assertEqual(
            "runtime-hooks/contracts/hook_mvp_001_a40_pre_edit_contract.json",
            result["source_gate_contract"],
        )
        self.assertEqual("pre-edit", result["gate"])
        self.assertEqual("pass", result["gate_status"])
        self.assertEqual(
            "runtime-hooks/contracts/hook_mvp_001_a40_pre_edit_contract.json",
            result["validation_artifact"],
        )
        self.assertEqual("ready", result["next_allowed_action"])

    def test_accepts_blocked_patch_proposal_example(self) -> None:
        code, result, stderr = self.run_script(BLOCKED_PROPOSAL)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("pass", result["status"])
        self.assertEqual("pre-edit", result["gate"])
        self.assertEqual("blocked", result["gate_status"])
        self.assertEqual("ready", result["next_allowed_action"])

    def test_blocks_missing_required_field(self) -> None:
        proposal = self.valid_pass_proposal()
        del proposal["atomic_item_id"]
        proposal_file = self.write_proposal(proposal)

        code, result, stderr = self.run_script(proposal_file)

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertEqual("blocked", result["status"])
        self.assertIn("missing required field: atomic_item_id", result["blocking_reasons"])
        self.assertEqual("handoff", result["next_allowed_action"])

    def test_blocks_passing_proposal_with_blocking_reasons(self) -> None:
        proposal = self.valid_pass_proposal()
        proposal["blocking_reasons"] = ["unexpected blocker"]
        proposal_file = self.write_proposal(proposal)

        code, result, _stderr = self.run_script(proposal_file)

        self.assertEqual(1, code)
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "passing proposal must not include blocking_reasons",
            result["blocking_reasons"],
        )

    def test_blocks_blocked_proposal_without_blocking_reasons(self) -> None:
        proposal = self.valid_pass_proposal()
        proposal["gate_status"] = "blocked"
        proposal["next_allowed_action"] = "handoff"
        proposal["workflow_step"]["advance_allowed"] = False
        proposal["queue_patch"]["to"] = "blocked"
        proposal["blocking_reasons"] = []
        proposal_file = self.write_proposal(proposal)

        code, result, _stderr = self.run_script(proposal_file)

        self.assertEqual(1, code)
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "blocked proposal requires blocking_reasons",
            result["blocking_reasons"],
        )

    def test_blocks_blocked_proposal_that_advances_workflow(self) -> None:
        proposal = json.loads(BLOCKED_PROPOSAL.read_text(encoding="utf-8"))
        proposal["workflow_step"]["advance_allowed"] = True
        proposal_file = self.write_proposal(proposal)

        code, result, _stderr = self.run_script(proposal_file)

        self.assertEqual(1, code)
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "blocked proposal must set workflow_step.advance_allowed to false",
            result["blocking_reasons"],
        )

    def test_cli_markdown_output(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main([str(PASSING_PROPOSAL)])

        self.assertEqual(0, code)
        output = stdout.getvalue()
        self.assertIn("State patch proposal:", output)
        self.assertIn("Status: pass", output)
        self.assertIn("Next allowed action: ready", output)
