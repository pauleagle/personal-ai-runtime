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
    / "utf8-traditional-chinese-defaults"
    / "scripts"
    / "validate_skill_utf8.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("validate_skill_utf8", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load script module: {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateSkillUtf8Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = load_script_module()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_skill(self, folder: str, content: str, encoding: str = "utf-8") -> Path:
        skill_dir = self.workspace / folder
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(content, encoding=encoding)
        return skill_dir

    def run_script(self, skill_dir: Path):
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = self.script.main([str(skill_dir), "--json"])

        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_accepts_utf8_skill_with_traditional_chinese_description(self) -> None:
        skill_dir = self.write_skill(
            "valid-skill",
            "---\n"
            "name: valid-skill\n"
            "description: 使用 UTF-8 驗證繁體中文 skill frontmatter。\n"
            "---\n"
            "\n"
            "# Valid Skill\n",
        )

        code, result, stderr = self.run_script(skill_dir)

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertTrue(result["valid"])
        self.assertEqual("utf-8", result["encoding"])
        self.assertEqual("Skill is valid!", result["message"])

    def test_rejects_non_utf8_skill_without_crashing(self) -> None:
        skill_dir = self.write_skill(
            "cp950-skill",
            "---\n"
            "name: cp950-skill\n"
            "description: 這是繁體中文。\n"
            "---\n",
            encoding="cp950",
        )

        code, result, stderr = self.run_script(skill_dir)

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertIn("not valid UTF-8", result["message"])
        self.assertIn("decodeError", result)

    def test_rejects_invalid_frontmatter_shape(self) -> None:
        skill_dir = self.write_skill(
            "invalid-skill",
            "---\n"
            "- not\n"
            "- a mapping\n"
            "---\n",
        )

        code, result, stderr = self.run_script(skill_dir)

        self.assertEqual(1, code)
        self.assertEqual("", stderr)
        self.assertFalse(result["valid"])
        self.assertEqual("Frontmatter must be a YAML dictionary", result["message"])
