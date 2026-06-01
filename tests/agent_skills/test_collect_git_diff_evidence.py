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
    / "diff-analysis"
    / "scripts"
    / "collect_git_diff_evidence.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("collect_git_diff_evidence", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(shutil.which("git"), "git is required for diff evidence tests")
class CollectGitDiffEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        subprocess.run(["git", "init"], cwd=self.repo, check=True, stdout=subprocess.PIPE)
        subprocess.run(
            ["git", "config", "user.email", "tests@example.invalid"],
            cwd=self.repo,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Tests"],
            cwd=self.repo,
            check=True,
        )
        (self.repo / "README.md").write_text("Initial\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-m", "initial"], cwd=self.repo, check=True, stdout=subprocess.PIPE)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_script(self, *args: str):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([*args, "--json"])

        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_collects_working_tree_diff_evidence(self) -> None:
        (self.repo / "README.md").write_text("Initial\nChanged\n", encoding="utf-8")
        (self.repo / "notes.md").write_text("Untracked\n", encoding="utf-8")

        code, result, stderr = self.run_script("--repo-root", str(self.repo))

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn(" M README.md", result["statusShort"])
        self.assertIn("?? notes.md", result["statusShort"])
        self.assertEqual(["README.md"], result["diffNameOnly"])
        self.assertEqual(["M\tREADME.md"], result["diffNameStatus"])
        self.assertTrue(any("README.md" in line for line in result["diffStat"]))

    def test_collects_staged_diff_evidence(self) -> None:
        (self.repo / "README.md").write_text("Initial\nStaged\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.repo, check=True)

        code, result, stderr = self.run_script("--repo-root", str(self.repo), "--staged")

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertTrue(result["staged"])
        self.assertEqual(["README.md"], result["diffNameOnly"])
        self.assertEqual(["M\tREADME.md"], result["diffNameStatus"])

    def test_rejects_non_git_directory_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as non_repo_dir:
            non_repo = Path(non_repo_dir)

            code, result, stderr = self.run_script("--repo-root", str(non_repo))

            self.assertEqual(1, code)
            self.assertEqual("", stderr)
            self.assertFalse(result["valid"])
            self.assertIn("Not a git repository", result["message"])
