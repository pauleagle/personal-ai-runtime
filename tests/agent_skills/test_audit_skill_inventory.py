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
    / "playbook-to-skill"
    / "scripts"
    / "audit_skill_inventory.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("audit_skill_inventory", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditSkillInventoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        (self.repo / "agent-playbooks").mkdir()
        (self.repo / "agent-skills").mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_skill(
        self,
        name: str,
        frontmatter_name: str | None = None,
        with_script: bool = False,
        portability_guidance: str = "",
    ) -> None:
        skill_dir = self.repo / "agent-skills" / name
        skill_dir.mkdir()
        actual_name = frontmatter_name or name
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            f"name: {actual_name}\n"
            f"description: Use {actual_name} during tests.\n"
            "---\n"
            "\n"
            f"# {actual_name}\n"
            f"{portability_guidance}\n",
            encoding="utf-8",
        )
        if with_script:
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            (scripts_dir / "helper.py").write_text("print('ok')\n", encoding="utf-8")

    def write_playbook(self, name: str) -> None:
        (self.repo / "agent-playbooks" / name).write_text(
            f"# {name}\n", encoding="utf-8"
        )

    def write_readmes(
        self,
        playbook_status: str = "aligned",
        skill_status: str = "aligned",
        profile: str = "hybrid",
        skill_name: str = "sample-skill",
    ) -> None:
        (self.repo / "agent-playbooks" / "README.md").write_text(
            "# Agent Playbooks\n\n"
            "## Playbook / Skill 對照表\n\n"
            "| Playbook | Skill | 狀態 | 說明 |\n"
            "|---|---|---|---|\n"
            f"| `sample-playbook.md` | `{skill_name}/` | `{playbook_status}` | sample |\n",
            encoding="utf-8",
        )
        (self.repo / "agent-skills" / "README.md").write_text(
            "# Agent Skills\n\n"
            "## Execution Profile\n\n"
            "| Skill | Playbook | Status | Profile | Description |\n"
            "|---|---|---|---|---|\n"
            f"| `{skill_name}/` | `sample-playbook.md` | `{skill_status}` | `{profile}` | sample |\n",
            encoding="utf-8",
        )

    def run_script(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main(["--repo-root", str(self.repo), "--json"])

        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_accepts_synchronized_inventory(self) -> None:
        self.write_playbook("sample-playbook.md")
        self.write_skill("sample-skill")
        self.write_readmes()

        code, result, stderr = self.run_script()

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertEqual([], result["findings"])

    def test_rejects_invalid_status_and_profile(self) -> None:
        self.write_playbook("sample-playbook.md")
        self.write_skill("sample-skill")
        self.write_readmes(playbook_status="done", skill_status="ready", profile="auto")

        code, result, stderr = self.run_script()
        messages = [finding["message"] for finding in result["findings"]]

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Invalid status 'ready'" in message for message in messages))
        self.assertTrue(any("Invalid status 'done'" in message for message in messages))
        self.assertTrue(any("Invalid profile 'auto'" in message for message in messages))

    def test_rejects_frontmatter_name_mismatch(self) -> None:
        self.write_playbook("sample-playbook.md")
        self.write_skill("sample-skill", frontmatter_name="other-skill")
        self.write_readmes()

        code, result, stderr = self.run_script()

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "does not match folder 'sample-skill'" in finding["message"]
                for finding in result["findings"]
            )
        )

    def test_warns_when_script_portability_guidance_is_missing(self) -> None:
        self.write_playbook("sample-playbook.md")
        self.write_skill("sample-skill", with_script=True)
        self.write_readmes()

        code, result, stderr = self.run_script()

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertTrue(
            any(
                finding["severity"] == "warning"
                and finding["area"] == "script-portability"
                for finding in result["findings"]
            )
        )

    def test_accepts_script_portability_guidance(self) -> None:
        self.write_playbook("sample-playbook.md")
        self.write_skill(
            "sample-skill",
            with_script=True,
            portability_guidance=(
                "Run the helper from Windows PowerShell and Linux/macOS shells.\n"
            ),
        )
        self.write_readmes()

        code, result, stderr = self.run_script()

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertEqual([], result["findings"])
