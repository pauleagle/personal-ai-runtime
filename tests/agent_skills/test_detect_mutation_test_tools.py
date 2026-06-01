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
    / "mutation-testing"
    / "scripts"
    / "detect_mutation_test_tools.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("detect_mutation_test_tools", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DetectMutationTestToolsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_script(self, *args: str):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([*args, "--json"])

        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_detects_package_json_test_and_mutation_scripts(self) -> None:
        (self.repo / "package.json").write_text(
            json.dumps(
                {
                    "scripts": {
                        "test": "jest",
                        "test:unit": "jest --runInBand",
                        "test:mutation": "stryker run",
                    },
                    "devDependencies": {"@stryker-mutator/core": "^8.0.0"},
                }
            ),
            encoding="utf-8",
        )

        code, result, stderr = self.run_script("--repo-root", str(self.repo))
        commands = {entry["command"] for entry in result["candidateCommands"]}

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertTrue(result["mutationToolingAvailable"])
        self.assertIn("npm run test", commands)
        self.assertIn("npm run test:unit", commands)
        self.assertIn("npm run test:mutation", commands)
        self.assertIn("npx stryker run", commands)

    def test_detects_python_project_test_candidates(self) -> None:
        (self.repo / "pyproject.toml").write_text("[project]\nname = 'sample'\n", encoding="utf-8")
        (self.repo / "tests").mkdir()

        result = self.script.detect(self.repo, path="")

        self.assertTrue(result["valid"])
        self.assertEqual(["tests"], result["pythonProject"]["testsDirs"])
        self.assertFalse(
            any(command["command"] == "python -m pytest" for command in result["candidateCommands"])
        )
        self.assertFalse(
            any(
                command["command"] == "python -m unittest discover -s tests"
                for command in result["candidateCommands"]
            )
        )

        result_with_python = self.script.detect(
            self.repo,
            path=str(Path(__file__).resolve().parent),
        )
        result_with_python["tools"]["testBinaries"]["python"] = "python"
        commands = self.script.build_candidate_commands(result_with_python)

        self.assertTrue(
            any(command["command"] == "python -m unittest discover -s tests" for command in commands)
        )
        self.assertFalse(any(command["command"] == "python -m pytest" for command in commands))

    def test_npx_alone_does_not_count_as_mutation_tooling(self) -> None:
        result = self.script.detect(self.repo, path="")
        result["tools"]["mutationBinaries"]["npx"] = "npx"
        result["mutationToolingAvailable"] = any(
            result["tools"]["mutationBinaries"].get(name)
            for name in self.script.DIRECT_MUTATION_BINARIES
        )

        self.assertFalse(result["mutationToolingAvailable"])

    def test_invalid_package_json_is_reported_without_crashing(self) -> None:
        (self.repo / "package.json").write_text("{not-json", encoding="utf-8")

        code, result, stderr = self.run_script("--repo-root", str(self.repo))

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn("Invalid JSON", result["packageJson"]["error"])

    def test_rejects_missing_repo_root(self) -> None:
        missing = self.repo / "missing"

        code, result, stderr = self.run_script("--repo-root", str(missing))

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertIn("does not exist", result["message"])
