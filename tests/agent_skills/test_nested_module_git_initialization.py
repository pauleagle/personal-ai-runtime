from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    REPO_ROOT
    / "agent-skills"
    / "nested-module-git-initialization"
    / "scripts"
    / "check_nested_module_git.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("check_nested_module_git", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NestedModuleGitInitializationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)
        (self.workspace / "modules").mkdir()
        (self.workspace / "poc-modules").mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_script(self, *args: str):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main(list(args), repo_root=self.workspace)

        return code, stdout.getvalue(), stderr.getvalue()

    def test_reports_missing_boundary_without_initializing(self) -> None:
        project = self.workspace / "modules" / "demo"
        project.mkdir()

        code, stdout, stderr = self.run_script(
            "--project-root", "modules/demo", "--json"
        )
        result = json.loads(stdout)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("missing-boundary", result["action"])
        self.assertFalse(result["gitExistsBefore"])
        self.assertFalse(result["gitExistsAfter"])
        self.assertFalse(result["gitInitExecuted"])
        self.assertFalse((project / ".git").exists())

    @unittest.skipUnless(shutil.which("git"), "git is required for initialization checks")
    def test_initializes_missing_boundary_when_requested(self) -> None:
        project = self.workspace / "poc-modules" / "demo"
        project.mkdir()

        code, stdout, stderr = self.run_script(
            "--project-root", "poc-modules/demo", "--initialize", "--json"
        )
        result = json.loads(stdout)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("initialized-boundary", result["action"])
        self.assertFalse(result["gitExistsBefore"])
        self.assertTrue(result["gitExistsAfter"])
        self.assertTrue(result["gitInitExecuted"])
        self.assertTrue((project / ".git").exists())

    @unittest.skipUnless(shutil.which("git"), "git is required for existing boundary checks")
    def test_reports_existing_git_boundary(self) -> None:
        project = self.workspace / "modules" / "existing"
        project.mkdir()
        subprocess.run(["git", "init"], cwd=project, check=True, stdout=subprocess.PIPE)

        code, stdout, stderr = self.run_script(
            "--project-root", "modules/existing", "--json"
        )
        result = json.loads(stdout)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual("existing-boundary", result["action"])
        self.assertTrue(result["gitExistsBefore"])
        self.assertTrue(result["gitExistsAfter"])
        self.assertFalse(result["gitInitExecuted"])

    def test_rejects_paths_that_are_not_child_project_roots(self) -> None:
        nested = self.workspace / "modules" / "demo" / "nested"
        nested.mkdir(parents=True)

        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as raised:
                self.script.main(
                    ["--project-root", "modules/demo/nested", "--json"],
                    repo_root=self.workspace,
                )

        self.assertEqual(2, raised.exception.code)
        self.assertEqual("", stdout.getvalue())
        self.assertIn("Project root must be exactly modules/<project>", stderr.getvalue())
