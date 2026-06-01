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
    / "atomic-subagent-runner"
    / "scripts"
    / "validate_subagent_job_contract.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("validate_subagent_job_contract", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateSubagentJobContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_contract(self, contract: object) -> Path:
        contract_file = self.workspace / "job.json"
        contract_file.write_text(json.dumps(contract), encoding="utf-8")
        return contract_file

    def run_script(self, contract_file: Path):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([str(contract_file), "--json"])
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def valid_contract(self) -> dict[str, object]:
        return {
            "job_id": "JOB-001",
            "parent_atomic_item_id": "SK-FU-001",
            "subagent_role": "diff-analyst",
            "context_pack": ["SPEC.md", "tests/output.txt"],
            "allowed_scope": ["agent-skills/example/**"],
            "forbidden_scope": ["modules/**"],
            "validation_requirements": ["python -m unittest discover -s tests"],
            "output_contract": {
                "required_sections": ["job result", "validation result", "state patch proposal"]
            },
            "merge_gate": "orchestrator-review",
        }

    def test_accepts_valid_contract(self) -> None:
        contract_file = self.write_contract(self.valid_contract())

        code, result, stderr = self.run_script(contract_file)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertEqual([], result["findings"])

    def test_rejects_missing_required_fields(self) -> None:
        contract = self.valid_contract()
        del contract["job_id"]
        del contract["output_contract"]
        contract_file = self.write_contract(contract)

        code, result, stderr = self.run_script(contract_file)
        messages = [finding["message"] for finding in result["findings"]]

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertIn("missing required field: job_id", messages)
        self.assertIn("missing required field: output_contract", messages)

    def test_rejects_empty_required_values(self) -> None:
        contract = self.valid_contract()
        contract["context_pack"] = []
        contract["allowed_scope"] = ""
        contract_file = self.write_contract(contract)

        code, result, _stderr = self.run_script(contract_file)
        messages = [finding["message"] for finding in result["findings"]]

        self.assertEqual(1, code)
        self.assertFalse(result["valid"])
        self.assertIn("context_pack must be non-empty", messages)
        self.assertIn("allowed_scope must be non-empty", messages)

    def test_warns_when_forbidden_scope_and_merge_gate_are_absent(self) -> None:
        contract = self.valid_contract()
        contract["forbidden_scope"] = []
        del contract["merge_gate"]
        contract_file = self.write_contract(contract)

        code, result, stderr = self.run_script(contract_file)
        areas = [finding["area"] for finding in result["findings"]]

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn("scope", areas)
        self.assertIn("governance", areas)

    def test_warns_on_hidden_chat_history_context(self) -> None:
        contract = self.valid_contract()
        contract["context_pack"] = ["Use previous chat history for the missing spec."]
        contract_file = self.write_contract(contract)

        code, result, _stderr = self.run_script(contract_file)

        self.assertEqual(0, code)
        self.assertTrue(result["valid"])
        self.assertTrue(
            any(finding["area"] == "context-pack" for finding in result["findings"])
        )
