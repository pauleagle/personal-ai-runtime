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
    / "test-effectiveness-evaluation"
    / "scripts"
    / "collect_validation_result_evidence.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("collect_validation_result_evidence", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CollectValidationResultEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_script(self, *paths: Path):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([*(str(path) for path in paths), "--json"])

        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_extracts_unittest_pass_evidence(self) -> None:
        result_file = self.workspace / "unittest.txt"
        result_file.write_text(
            "........\n----------------------------------------------------------------------\n"
            "Ran 8 tests in 0.123s\n\nOK\n",
            encoding="utf-8",
        )

        code, result, stderr = self.run_script(result_file)
        evidence = result["sources"][0]["unittest"]

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(evidence["detected"])
        self.assertEqual(8, evidence["testsRun"])
        self.assertEqual("passed", evidence["status"])

    def test_extracts_unittest_failure_evidence(self) -> None:
        result_file = self.workspace / "failed.txt"
        result_file.write_text(
            "Ran 3 tests in 0.010s\n\nFAILED (failures=1, errors=2)\n",
            encoding="utf-8",
        )

        code, result, _stderr = self.run_script(result_file)
        evidence = result["sources"][0]["unittest"]

        self.assertEqual(0, code)
        self.assertEqual("failed", evidence["status"])
        self.assertEqual(1, evidence["failures"])
        self.assertEqual(2, evidence["errors"])

    def test_extracts_mutation_terms_without_classifying_gap(self) -> None:
        result_file = self.workspace / "mutation.txt"
        result_file.write_text(
            "killed: 4\nsurvived: 1\nequivalent: 1\nskipped blocked\n",
            encoding="utf-8",
        )

        code, result, _stderr = self.run_script(result_file)
        mutation = result["sources"][0]["mutationTerms"]

        self.assertEqual(0, code)
        self.assertTrue(mutation["detected"])
        self.assertEqual(1, mutation["termCounts"]["survived"])
        self.assertEqual(1, mutation["termCounts"]["equivalent"])
        self.assertEqual(1, mutation["termCounts"]["blocked"])
        self.assertEqual(4, mutation["termCounts"]["killed"])

    def test_missing_result_file_is_invalid(self) -> None:
        code, result, stderr = self.run_script(self.workspace / "missing.txt")

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertIn("missing", result["sources"][0]["warnings"])
