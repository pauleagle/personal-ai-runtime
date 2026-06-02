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
        self.assertTrue(all(item["status"] == "pass" for item in result["gate_results"]))

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

    def test_accepts_active_item_contract_example(self) -> None:
        result = self.script.run_smoke(REPO_ROOT, (3, 10, 11), [ACTIVE_ITEM_CONTRACT])

        self.assertEqual("pass", result["status"])
        self.assertEqual([ACTIVE_ITEM_CONTRACT], result["contract_paths"])
        self.assertEqual(1, len(result["gate_results"]))
        self.assertEqual("pre-run", result["gate_results"][0]["gate"])
        self.assertEqual("ready", result["next_allowed_action"])

    def test_blocks_explicit_invalid_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_contract = Path(temp_dir) / "invalid_gate.json"
            invalid_contract.write_text("{}", encoding="utf-8")
            result = self.script.run_smoke(REPO_ROOT, (3, 10, 11), [str(invalid_contract)])

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-contracts", result["next_allowed_action"])
        self.assertEqual(1, len(result["gate_results"]))
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
        self.assertIn(
            "unable to load environment helper",
            result["blocking_reasons"][0],
        )

    def test_blocks_old_python_before_loading_validator(self) -> None:
        result = self.script.run_smoke(REPO_ROOT, (3, 9, 13))

        self.assertEqual("blocked", result["status"])
        self.assertEqual("fix-environment", result["next_allowed_action"])
        self.assertEqual([], result["gate_results"])
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

    def test_cli_markdown_output(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(["--repo-root", str(REPO_ROOT)])

        self.assertEqual(0, code)
        output = stdout.getvalue()
        self.assertIn("Runtime hooks smoke", output)
        self.assertIn("Status: pass", output)
        self.assertIn("Next allowed action: ready", output)

    def test_cli_accepts_explicit_contract(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = self.script.main(
                [
                    "--repo-root",
                    str(REPO_ROOT),
                    "--contract",
                    "tests/fixtures/gate_contract_pre_run_sample.json",
                    "--json",
                ]
            )

        self.assertEqual(0, code)
        result = json.loads(stdout.getvalue())
        self.assertEqual(["tests/fixtures/gate_contract_pre_run_sample.json"], result["contract_paths"])
        self.assertEqual(1, len(result["gate_results"]))

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
