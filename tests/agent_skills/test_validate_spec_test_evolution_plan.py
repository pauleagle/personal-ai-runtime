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
    / "spec-test-evolution"
    / "scripts"
    / "validate_spec_test_evolution_plan.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("validate_spec_test_evolution_plan", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateSpecTestEvolutionPlanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_plan(self, plan: object) -> Path:
        plan_file = self.workspace / "evolution-plan.json"
        plan_file.write_text(json.dumps(plan), encoding="utf-8")
        return plan_file

    def run_script(self, plan_file: Path):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([str(plan_file), "--json"])
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def valid_plan(self) -> dict[str, object]:
        return {
            "decision_source": "Human accepted DEC-001 on 2026-06-01.",
            "affected_artifacts": ["SPEC.md", "tests/test_feature.py"],
            "updates": {
                "spec_updates": ["SPEC.md"],
                "test_updates": ["tests/test_feature.py"],
            },
            "traceability": {
                "parent_refs": ["CR-001"],
                "child_refs": ["CR-001-FU-01"],
                "root_index_refs": ["SPEC.md"],
            },
            "rerun_point": "Step 5 - Spec-Based Test Design",
            "next_validation_step": "python -m unittest tests.test_feature",
        }

    def test_accepts_valid_evolution_plan(self) -> None:
        plan_file = self.write_plan(self.valid_plan())

        code, result, stderr = self.run_script(plan_file)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertEqual([], result["findings"])

    def test_rejects_missing_required_fields(self) -> None:
        plan = self.valid_plan()
        del plan["decision_source"]
        del plan["rerun_point"]
        plan_file = self.write_plan(plan)

        code, result, stderr = self.run_script(plan_file)
        messages = [finding["message"] for finding in result["findings"]]

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertIn("missing required field: decision_source", messages)
        self.assertIn("missing required field: rerun_point", messages)

    def test_rejects_plan_without_non_empty_update_group(self) -> None:
        plan = self.valid_plan()
        plan["updates"] = {"spec_updates": [], "test_updates": []}
        plan_file = self.write_plan(plan)

        code, result, _stderr = self.run_script(plan_file)

        self.assertEqual(1, code)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("at least one update group" in finding["message"] for finding in result["findings"])
        )

    def test_rejects_missing_traceability_refs(self) -> None:
        plan = self.valid_plan()
        plan["traceability"] = {"parent_refs": []}
        plan_file = self.write_plan(plan)

        code, result, _stderr = self.run_script(plan_file)
        messages = [finding["message"] for finding in result["findings"]]

        self.assertEqual(1, code)
        self.assertFalse(result["valid"])
        self.assertIn("parent_refs must be non-empty", messages)
        self.assertIn("missing traceability field: child_refs", messages)

    def test_warns_about_ambiguous_decision_and_missing_root_index(self) -> None:
        plan = self.valid_plan()
        plan["decision_source"] = "TODO: waiting for human decision"
        plan["traceability"] = {
            "parent_refs": ["CR-001"],
            "child_refs": ["CR-001-FU-01"],
        }
        plan_file = self.write_plan(plan)

        code, result, stderr = self.run_script(plan_file)
        areas = [finding["area"] for finding in result["findings"]]

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn("decision-source", areas)
        self.assertIn("traceability", areas)
