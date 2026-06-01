from __future__ import annotations

import contextlib
import hashlib
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
    / "context-pack-builder"
    / "scripts"
    / "build_context_manifest.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("build_context_manifest", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildContextManifestTest(unittest.TestCase):
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
            code = self.script.main(["--repo-root", str(self.repo), *args, "--json"])

        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_builds_manifest_for_utf8_file(self) -> None:
        content = "alpha\n繁體\n"
        source = self.repo / "note.md"
        source.write_text(content, encoding="utf-8")

        code, result, stderr = self.run_script("note.md")
        item = result["sources"][0]
        raw_bytes = source.read_bytes()

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertEqual("file", item["kind"])
        self.assertEqual(2, item["lines"])
        self.assertEqual(len(raw_bytes), item["bytes"])
        self.assertEqual(hashlib.sha256(raw_bytes).hexdigest(), item["sha256"])

    def test_reports_missing_source_as_invalid(self) -> None:
        code, result, stderr = self.run_script("missing.md")

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertIn("missing", result["sources"][0]["warnings"])

    def test_reports_directory_and_large_file_warnings(self) -> None:
        (self.repo / "docs").mkdir()
        (self.repo / "large.txt").write_text("abcdef", encoding="utf-8")

        code, result, stderr = self.run_script("--max-bytes", "3", "docs", "large.txt")
        warnings_by_source = {
            warning["source"]: warning["warnings"] for warning in result["warnings"]
        }

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn("directory-not-file", warnings_by_source["docs"])
        self.assertIn("exceeds-max-bytes", warnings_by_source["large.txt"])

    def test_warns_for_outside_repo_file(self) -> None:
        outside = Path(self.temp_dir.name).parent / "outside-context-pack-test.txt"
        outside.write_text("outside\n", encoding="utf-8")
        try:
            code, result, stderr = self.run_script(str(outside))
        finally:
            outside.unlink(missing_ok=True)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertIn("outside-repo-root", result["sources"][0]["warnings"])
