from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "runtime-hooks" / "scripts" / "validate_gate_contract.py"
ACTIVE_ITEM_EXAMPLE = (
    REPO_ROOT
    / "runtime-hooks"
    / "examples"
    / "hook_mvp_001_a13_pre_run_contract.json"
)
ACTIVE_ITEM_PRE_EDIT_EXAMPLE = (
    REPO_ROOT
    / "runtime-hooks"
    / "examples"
    / "hook_mvp_001_a17_pre_edit_contract.json"
)
ACTIVE_ITEM_POST_RUN_EXAMPLE = (
    REPO_ROOT
    / "runtime-hooks"
    / "examples"
    / "hook_mvp_001_a18_post_run_contract.json"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("validate_gate_contract", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateGateContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_contract(self, contract: object) -> Path:
        contract_file = self.workspace / "gate.json"
        contract_file.write_text(json.dumps(contract), encoding="utf-8")
        return contract_file

    def run_script(self, contract_file: Path):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([str(contract_file), "--json"])
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def base_contract(self, gate: str = "pre-run") -> dict[str, object]:
        return {
            "gate": gate,
            "atomic_item_id": "HOOK-MVP-001-A1",
            "spec_ref": "backlog/HOOK-MVP-001-minimal-spec-driven-execution-gates_zhTW.md",
            "allowed_scope": ["runtime-hooks/scripts/**", "tests/runtime_hooks/**"],
            "forbidden_scope": ["agent-playbooks/spec-driven-change-verification-workflow-playbook.md"],
            "acceptance_criteria": ["contract validator returns pass or blocked"],
            "expected_artifacts": ["runtime-hooks/scripts/validate_gate_contract.py"],
            "validation_plan": ["python -m unittest tests.runtime_hooks.test_validate_gate_contract"],
        }

    def test_accepts_valid_pre_run_contract(self) -> None:
        contract_file = self.write_contract(self.base_contract())

        code, result, stderr = self.run_script(contract_file)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("pre-run", result["gate"])
        self.assertEqual("pass", result["status"])
        self.assertEqual([], result["blocking_reasons"])
        self.assertEqual("edit", result["next_allowed_action"])

    def test_accepts_active_atomic_item_example(self) -> None:
        contract = json.loads(ACTIVE_ITEM_EXAMPLE.read_text(encoding="utf-8"))

        self.assertEqual("HOOK-MVP-001-A13", contract["atomic_item_id"])

        code, result, stderr = self.run_script(ACTIVE_ITEM_EXAMPLE)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("pre-run", result["gate"])
        self.assertEqual("pass", result["status"])
        self.assertEqual([], result["blocking_reasons"])

    def test_accepts_active_pre_edit_example(self) -> None:
        contract = json.loads(ACTIVE_ITEM_PRE_EDIT_EXAMPLE.read_text(encoding="utf-8"))

        self.assertEqual("HOOK-MVP-001-A17", contract["atomic_item_id"])
        self.assertIn("proposed_changed_files", contract)

        code, result, stderr = self.run_script(ACTIVE_ITEM_PRE_EDIT_EXAMPLE)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("pre-edit", result["gate"])
        self.assertEqual("pass", result["status"])
        self.assertEqual([], result["blocking_reasons"])
        self.assertEqual("edit", result["next_allowed_action"])

    def test_accepts_active_post_run_example(self) -> None:
        contract = json.loads(ACTIVE_ITEM_POST_RUN_EXAMPLE.read_text(encoding="utf-8"))

        self.assertEqual("HOOK-MVP-001-A18", contract["atomic_item_id"])
        self.assertIn("commit_checkpoint", contract)

        code, result, stderr = self.run_script(ACTIVE_ITEM_POST_RUN_EXAMPLE)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("post-run", result["gate"])
        self.assertEqual("pass", result["status"])
        self.assertEqual([], result["blocking_reasons"])
        self.assertEqual("complete", result["next_allowed_action"])

    def test_blocks_missing_required_fields(self) -> None:
        contract = self.base_contract()
        del contract["atomic_item_id"]
        contract["acceptance_criteria"] = []
        contract_file = self.write_contract(contract)

        code, result, stderr = self.run_script(contract_file)

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertEqual("blocked", result["status"])
        self.assertIn("missing required field: atomic_item_id", result["blocking_reasons"])
        self.assertIn("acceptance_criteria must be non-empty", result["blocking_reasons"])
        self.assertEqual("ask-user", result["next_allowed_action"])

    def test_pre_edit_blocks_file_outside_allowed_scope(self) -> None:
        contract = self.base_contract("pre-edit")
        contract["proposed_changed_files"] = ["README.md"]
        contract_file = self.write_contract(contract)

        code, result, _stderr = self.run_script(contract_file)

        self.assertEqual(1, code)
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "proposed file is outside allowed_scope: README.md",
            result["blocking_reasons"],
        )
        self.assertEqual("handoff", result["next_allowed_action"])

    def test_pre_edit_blocks_file_inside_forbidden_scope(self) -> None:
        contract = self.base_contract("pre-edit")
        contract["allowed_scope"] = ["agent-playbooks/**"]
        contract["proposed_changed_files"] = [
            "agent-playbooks/spec-driven-change-verification-workflow-playbook.md"
        ]
        contract_file = self.write_contract(contract)

        code, result, _stderr = self.run_script(contract_file)

        self.assertEqual(1, code)
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            (
                "proposed file is inside forbidden_scope: "
                "agent-playbooks/spec-driven-change-verification-workflow-playbook.md"
            ),
            result["blocking_reasons"],
        )

    def test_accepts_post_run_skipped_commit_with_reason(self) -> None:
        contract = self.base_contract("post-run")
        contract.update(
            {
                "changed_files": ["runtime-hooks/scripts/validate_gate_contract.py"],
                "validation_actions": ["python -m unittest tests.runtime_hooks.test_validate_gate_contract"],
                "acceptance_results": {"contract validator returns pass or blocked": "pass"},
                "remaining_risks": ["none known"],
                "follow_up_items": ["none"],
                "commit_checkpoint": {
                    "status": "skipped",
                    "skip_reason": "user requested no commit",
                },
            }
        )
        contract_file = self.write_contract(contract)

        code, result, _stderr = self.run_script(contract_file)

        self.assertEqual(0, code)
        self.assertEqual("pass", result["status"])
        self.assertEqual("complete", result["next_allowed_action"])

    def test_post_run_blocks_skipped_commit_without_reason(self) -> None:
        contract = self.base_contract("post-run")
        contract.update(
            {
                "changed_files": ["runtime-hooks/scripts/validate_gate_contract.py"],
                "validation_actions": ["python -m unittest tests.runtime_hooks.test_validate_gate_contract"],
                "acceptance_results": {"contract validator returns pass or blocked": "pass"},
                "remaining_risks": ["none known"],
                "follow_up_items": ["none"],
                "commit_checkpoint": {"status": "skipped"},
            }
        )
        contract_file = self.write_contract(contract)

        code, result, _stderr = self.run_script(contract_file)

        self.assertEqual(1, code)
        self.assertEqual("blocked", result["status"])
        self.assertIn(
            "skipped checkpoint requires skip_reason or blocked_reason",
            result["blocking_reasons"],
        )
        self.assertEqual("validate", result["next_allowed_action"])
