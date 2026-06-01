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
    / "impact-analysis"
    / "scripts"
    / "collect_impact_evidence.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("collect_impact_evidence", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(shutil.which("git"), "git is required for impact evidence tests")
class CollectImpactEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        subprocess.run(["git", "init"], cwd=self.repo, check=True, stdout=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "tests@example.invalid"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Tests"], cwd=self.repo, check=True)
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

    def test_classifies_changed_and_untracked_paths(self) -> None:
        for folder in ("src", "tests", "spec", "docs"):
            (self.repo / folder).mkdir()
        (self.repo / "src" / "engine.py").write_text("print('changed')\n", encoding="utf-8")
        (self.repo / "tests" / "test_engine.py").write_text("def test_engine(): pass\n", encoding="utf-8")
        (self.repo / "spec" / "mvp.md").write_text("# MVP\n", encoding="utf-8")
        (self.repo / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
        (self.repo / "pyproject.toml").write_text("[project]\nname = 'sample'\n", encoding="utf-8")

        code, result, stderr = self.run_script("--repo-root", str(self.repo))
        categories_by_path = {
            item["path"]: item["categories"] for item in result["pathImpacts"]
        }

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn("source", categories_by_path["src/engine.py"])
        self.assertIn("tests", categories_by_path["tests/test_engine.py"])
        self.assertIn("specs", categories_by_path["spec/mvp.md"])
        self.assertIn("docs", categories_by_path["docs/guide.md"])
        self.assertIn("config", categories_by_path["pyproject.toml"])

    def test_classifies_staged_paths_only_when_requested(self) -> None:
        (self.repo / "README.md").write_text("Initial\nChanged\n", encoding="utf-8")
        (self.repo / "untracked.md").write_text("Nope\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.repo, check=True)

        code, result, stderr = self.run_script("--repo-root", str(self.repo), "--staged")

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn("README.md", result["changedPaths"])
        self.assertIn("untracked.md", result["statusPaths"])
        self.assertTrue(any(item["path"] == "README.md" for item in result["pathImpacts"]))

    def test_rejects_non_git_directory_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as non_repo:
            code, result, stderr = self.run_script("--repo-root", non_repo)

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertIn("Not a git repository", result["message"])
