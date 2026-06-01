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
    / "prompt-to-playbook"
    / "scripts"
    / "inspect_playbook_request.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("inspect_playbook_request", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InspectPlaybookRequestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        (self.repo / "agent-playbooks").mkdir()
        self.write_readme()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_readme(self, rows: str | None = None) -> None:
        table_rows = rows or (
            "| `sample-playbook.md` | - | `draft` | sample |\n"
            "| `mapped-playbook.md` | `mapped-skill/` | `aligned` | mapped |\n"
        )
        (self.repo / "agent-playbooks" / "README.md").write_text(
            "# Agent Playbooks\n\n"
            "## Playbook / Skill 對照表\n\n"
            "| Playbook | Skill | 狀態 | 說明 |\n"
            "|---|---|---|---|\n"
            f"{table_rows}",
            encoding="utf-8",
        )

    def run_script(self, *args: str):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main(["--repo-root", str(self.repo), *args, "--json"])
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_accepts_existing_unmapped_draft_playbook(self) -> None:
        (self.repo / "agent-playbooks" / "sample-playbook.md").write_text(
            "# Sample\n", encoding="utf-8"
        )

        code, result, stderr = self.run_script("--target-playbook", "sample-playbook.md")

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertEqual("draft", result["readmeRow"]["status"])
        self.assertFalse(result["readmeRow"]["requiresSkillExtractedStatusOnUpdate"])

    def test_warns_for_new_playbook_missing_readme_row(self) -> None:
        code, result, stderr = self.run_script("--target-playbook", "new-playbook.md")

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertTrue(any(finding["area"] == "readme" for finding in result["findings"]))

    def test_warns_when_mapped_aligned_playbook_requires_status_change(self) -> None:
        code, result, _stderr = self.run_script("--target-playbook", "mapped-playbook.md")

        self.assertEqual(0, code)
        self.assertTrue(result["valid"])
        self.assertTrue(result["readmeRow"]["requiresSkillExtractedStatusOnUpdate"])
        self.assertTrue(any(finding["area"] == "status" for finding in result["findings"]))

    def test_rejects_target_outside_agent_playbooks(self) -> None:
        code, result, stderr = self.run_script("--target-playbook", "../outside.md")

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertTrue(any(finding["area"] == "target" for finding in result["findings"]))

    def test_reports_source_prompt_file_evidence(self) -> None:
        source = self.repo / "prompt.md"
        source.write_text("Make a reusable playbook.\n", encoding="utf-8")

        code, result, stderr = self.run_script(
            "--source", "prompt.md",
            "--target-playbook", "sample-playbook.md",
        )

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["source"]["exists"])
        self.assertEqual("file", result["source"]["kind"])
