#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


PLAYBOOK_STATUSES = {
    "draft",
    "skill-extracted",
    "aligned",
    "aligned-with-followups",
    "deprecated",
}
SKILL_PROFILES = {"script", "hybrid", "low-llm", "heavy-llm"}
WINDOWS_PORTABILITY_TERMS = ("windows", "powershell", ".ps1")
UNIX_PORTABILITY_TERMS = ("linux", "posix", "macos", "mac/linux", ".sh")
PORTABILITY_LIMITATION_TERMS = (
    "platform limitation",
    "validation gap",
    "cannot be cross-platform",
)


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def parse_table_after_heading(markdown: str, heading: str) -> list[dict[str, str]]:
    lines = markdown.splitlines()
    start = None

    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break

    if start is None:
        return []

    table_lines: list[str] = []
    for line in lines[start:]:
        if not line.strip():
            if table_lines:
                break
            continue
        if not line.lstrip().startswith("|"):
            if table_lines:
                break
            continue
        table_lines.append(line)

    if len(table_lines) < 2:
        return []

    headers = split_markdown_row(table_lines[0])
    rows = []

    for line in table_lines[2:]:
        cells = split_markdown_row(line)
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))

    return rows


def parse_table_with_headers(markdown: str, required_headers: set[str]) -> list[dict[str, str]]:
    lines = markdown.splitlines()

    for index, line in enumerate(lines):
        headers = split_markdown_row(line)
        if not headers or not required_headers.issubset(set(headers)):
            continue
        if index + 1 >= len(lines):
            continue

        separator = split_markdown_row(lines[index + 1])
        if not separator or len(separator) != len(headers):
            continue

        rows = []
        for row_line in lines[index + 2 :]:
            cells = split_markdown_row(row_line)
            if not cells:
                break
            if len(cells) != len(headers):
                continue
            rows.append(dict(zip(headers, cells)))
        return rows

    return []


def extract_backtick_values(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def normalize_skill_name(value: str) -> str:
    return value.rstrip("/")


def normalize_cell_value(value: str) -> str:
    return value.strip().strip("`").strip()


def validate_skill_frontmatter(skill_dir: Path) -> tuple[bool, str, dict[str, Any]]:
    skill_md = skill_dir / "SKILL.md"
    details: dict[str, Any] = {"skillDir": str(skill_dir), "skillFile": str(skill_md)}

    if not skill_md.exists():
        return False, "SKILL.md not found", details

    content = read_utf8(skill_md)
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid or missing frontmatter", details

    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a mapping", details

    details["frontmatter"] = frontmatter
    name = frontmatter.get("name")

    if name != skill_dir.name:
        return False, f"Frontmatter name '{name}' does not match folder '{skill_dir.name}'", details

    return True, "Skill frontmatter is valid.", details


def skill_has_scripts(skill_dir: Path) -> bool:
    scripts_dir = skill_dir / "scripts"
    return scripts_dir.is_dir() and any(path.is_file() for path in scripts_dir.iterdir())


def has_script_portability_guidance(content: str) -> bool:
    lowered = content.lower()
    has_windows = any(term in lowered for term in WINDOWS_PORTABILITY_TERMS)
    has_unix = any(term in lowered for term in UNIX_PORTABILITY_TERMS)
    has_limitation = any(term in lowered for term in PORTABILITY_LIMITATION_TERMS)
    return has_limitation or (has_windows and has_unix)


def audit(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    playbooks_readme = repo_root / "agent-playbooks" / "README.md"
    skills_readme = repo_root / "agent-skills" / "README.md"

    findings: list[dict[str, str]] = []

    def add_finding(severity: str, area: str, message: str) -> None:
        findings.append({"severity": severity, "area": area, "message": message})

    playbook_rows = parse_table_after_heading(
        read_utf8(playbooks_readme), "## Playbook / Skill 對照表"
    )
    skill_rows = parse_table_with_headers(
        read_utf8(skills_readme), {"Skill", "Playbook", "Status", "Profile"}
    )

    if not playbook_rows:
        add_finding("error", "playbook-readme", "Playbook / Skill mapping table not found.")
    if not skill_rows:
        add_finding("error", "skill-readme", "Skill inventory table not found.")

    skill_inventory_names: set[str] = set()

    for row in skill_rows:
        skill_values = extract_backtick_values(row.get("Skill", ""))
        playbook_values = extract_backtick_values(row.get("Playbook", ""))
        status = normalize_cell_value(row.get("Status", ""))
        profile = normalize_cell_value(row.get("Profile", ""))

        if status not in PLAYBOOK_STATUSES:
            add_finding("error", "skill-readme", f"Invalid status '{status}' in skill row {row}.")
        if profile not in SKILL_PROFILES:
            add_finding("error", "skill-readme", f"Invalid profile '{profile}' in skill row {row}.")

        for skill_value in skill_values:
            skill_name = normalize_skill_name(skill_value)
            skill_inventory_names.add(skill_name)
            skill_dir = repo_root / "agent-skills" / skill_name

            if not skill_dir.exists():
                add_finding("error", "skill-file", f"Mapped skill directory missing: {skill_name}")
                continue

            valid, message, _details = validate_skill_frontmatter(skill_dir)
            if not valid:
                add_finding("error", "skill-frontmatter", f"{skill_name}: {message}")
                continue

            if skill_has_scripts(skill_dir):
                skill_content = read_utf8(skill_dir / "SKILL.md")
                if not has_script_portability_guidance(skill_content):
                    add_finding(
                        "warning",
                        "script-portability",
                        (
                            f"{skill_name}: scripts/ exists but SKILL.md does not document "
                            "Windows and Linux/POSIX/macOS invocation coverage or a platform limitation."
                        ),
                    )

        for playbook_value in playbook_values:
            playbook_path = repo_root / "agent-playbooks" / playbook_value
            if not playbook_path.exists():
                add_finding("error", "playbook-file", f"Mapped playbook missing: {playbook_value}")

    for row in playbook_rows:
        status = normalize_cell_value(row.get("狀態", ""))
        if status not in PLAYBOOK_STATUSES:
            add_finding("error", "playbook-readme", f"Invalid status '{status}' in row {row}.")

        for playbook_value in extract_backtick_values(row.get("Playbook", "")):
            playbook_path = repo_root / "agent-playbooks" / playbook_value
            if not playbook_path.exists():
                add_finding("error", "playbook-file", f"Playbook table file missing: {playbook_value}")

        skill_cell = row.get("Skill", "")
        skill_values = [
            normalize_skill_name(value)
            for value in extract_backtick_values(skill_cell)
            if not value.endswith(".md")
        ]

        for skill_name in skill_values:
            skill_dir = repo_root / "agent-skills" / skill_name
            if not skill_dir.exists():
                add_finding("error", "skill-file", f"Playbook table skill missing: {skill_name}")
            elif skill_name not in skill_inventory_names:
                add_finding(
                    "warning",
                    "inventory-sync",
                    f"Playbook table skill not listed in skill inventory: {skill_name}",
                )

    return {
        "valid": not any(finding["severity"] == "error" for finding in findings),
        "repoRoot": str(repo_root),
        "playbookRows": len(playbook_rows),
        "skillRows": len(skill_rows),
        "findings": findings,
    }


def emit_markdown(result: dict[str, Any]) -> None:
    print(f"Repository: {result['repoRoot']}")
    print(f"Playbook rows: {result['playbookRows']}")
    print(f"Skill rows: {result['skillRows']}")
    print()
    print("### Findings")
    print()

    if not result["findings"]:
        print("- (none)")
        return

    for finding in result["findings"]:
        print(f"- [{finding['severity']}] {finding['area']}: {finding['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit playbook/skill README inventory rows and mapped SKILL.md files."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = audit(Path(args.repo_root))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_markdown(result)

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
