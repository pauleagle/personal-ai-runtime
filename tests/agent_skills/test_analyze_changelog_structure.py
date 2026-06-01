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
    / "changelog-normalization"
    / "scripts"
    / "analyze_changelog_structure.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("analyze_changelog_structure", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AnalyzeChangelogStructureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_changelog(self, content: str, name: str = "CHANGELOG.md") -> Path:
        path = self.repo / name
        path.write_text(content, encoding="utf-8")
        return path

    def run_script(self, *args: str):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main(["--repo-root", str(self.repo), *args, "--json"])

        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_collects_version_sections_categories_and_dates(self) -> None:
        self.write_changelog(
            "# Changelog\n\n"
            "## [1.1.0] - 2026-06-01\n\n"
            "### Added\n\n"
            "- New feature.\n\n"
            "### Fixed\n\n"
            "- Bug fix.\n\n"
            "## [1.0.0] - 2026-05-01\n\n"
            "### Changed\n\n"
            "- Initial release.\n"
        )

        code, result, stderr = self.run_script()
        categories = [
            category["text"]
            for category in result["versionSections"][0]["categories"]
        ]

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertEqual(2, len(result["versionSections"]))
        self.assertEqual(["Added", "Fixed"], categories)
        self.assertEqual([], result["findings"])

    def test_flags_missing_dates_uncategorized_entries_and_noise(self) -> None:
        self.write_changelog(
            "# Changelog\n\n"
            "## [1.0.0]\n\n"
            "- feat: add raw commit-style entry.\n"
            "- TODO: decide release ownership.\n\n"
            "## Unreleased\n\n"
            "### Added\n\n"
            "- Pending change.\n"
        )

        code, result, stderr = self.run_script()
        areas = [finding["area"] for finding in result["findings"]]

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn("dates", areas)
        self.assertIn("categories", areas)
        self.assertIn("versions", areas)
        self.assertIn("commit-log", areas)
        self.assertIn("todo", areas)

    def test_rejects_missing_changelog(self) -> None:
        code, result, stderr = self.run_script()

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertEqual("file", result["findings"][0]["area"])

    def test_rejects_changelog_outside_repo(self) -> None:
        outside = Path(self.temp_dir.name).parent / "outside-changelog.md"
        outside.write_text("# Changelog\n", encoding="utf-8")
        try:
            code, result, stderr = self.run_script("--changelog", str(outside))
        finally:
            outside.unlink(missing_ok=True)

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertEqual("path", result["findings"][0]["area"])
