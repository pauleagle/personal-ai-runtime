#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PLAYBOOK_STATUSES = {
    "draft",
    "skill-extracted",
    "aligned",
    "aligned-with-followups",
    "deprecated",
}
ROW_RE = re.compile(r"^\|(.+)\|$")


def split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def extract_backtick_values(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def normalize_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def add_finding(findings: list[dict[str, Any]], severity: str, area: str, message: str) -> None:
    findings.append({"severity": severity, "area": area, "message": message})


def parse_playbook_rows(markdown: str) -> list[dict[str, str]]:
    lines = markdown.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "## Playbook / Skill 對照表":
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
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def resolve_repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def relative_to_repo(repo_root: Path, path: Path) -> str | None:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return None


def normalize_playbook_name(value: str) -> str:
    normalized = value.replace("\\", "/").strip()
    if normalized.startswith("agent-playbooks/"):
        normalized = normalized[len("agent-playbooks/") :]
    return normalized


def inspect_request(
    repo_root: Path,
    target_playbook: str,
    source: str | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    findings: list[dict[str, Any]] = []

    result: dict[str, Any] = {
        "valid": False,
        "repoRoot": str(repo_root),
        "source": None,
        "targetPlaybook": None,
        "readmeRow": None,
        "findings": findings,
    }

    if not repo_root.exists() or not repo_root.is_dir():
        add_finding(findings, "error", "repo-root", "Repository path does not exist or is not a directory.")
        return result

    playbooks_dir = repo_root / "agent-playbooks"
    readme_path = playbooks_dir / "README.md"
    if not readme_path.exists():
        add_finding(findings, "error", "readme", "agent-playbooks/README.md not found.")
        return result

    if source:
        source_path = resolve_repo_path(repo_root, source)
        result["source"] = {
            "input": source,
            "path": str(source_path),
            "relativePath": relative_to_repo(repo_root, source_path),
            "exists": source_path.exists(),
            "kind": "file" if source_path.is_file() else "directory" if source_path.is_dir() else "missing",
        }
        if not source_path.exists():
            add_finding(findings, "warning", "source", "Source prompt/example path does not exist.")
        elif not source_path.is_file():
            add_finding(findings, "warning", "source", "Source prompt/example path is not a regular file.")

    target_name = normalize_playbook_name(target_playbook)
    target_path = (playbooks_dir / target_name).resolve()
    target_relative = relative_to_repo(repo_root, target_path)
    result["targetPlaybook"] = {
        "input": target_playbook,
        "name": target_name,
        "path": str(target_path),
        "relativePath": target_relative,
        "exists": target_path.exists(),
    }

    if not target_name.endswith(".md"):
        add_finding(findings, "error", "target", "Target playbook must be a Markdown file.")
    if relative_to_repo(playbooks_dir, target_path) is None:
        add_finding(findings, "error", "target", "Target playbook must stay under agent-playbooks/.")

    rows = parse_playbook_rows(readme_path.read_text(encoding="utf-8"))
    if not rows:
        add_finding(findings, "error", "readme", "Playbook / Skill mapping table not found.")
    target_row = None
    for row in rows:
        playbook_values = [normalize_playbook_name(value) for value in extract_backtick_values(row.get("Playbook", ""))]
        if target_name in playbook_values:
            target_row = row
            break

    if target_row is None:
        add_finding(
            findings,
            "warning",
            "readme",
            "Target playbook is not listed; new playbooks should be added as draft with Skill '-'.",
        )
    else:
        status = normalize_cell(target_row.get("狀態", ""))
        skill_cell = target_row.get("Skill", "")
        mapped_skills = [
            value.rstrip("/")
            for value in extract_backtick_values(skill_cell)
            if not value.endswith(".md")
        ]
        result["readmeRow"] = {
            "playbook": target_row.get("Playbook", ""),
            "skill": skill_cell,
            "status": status,
            "mappedSkills": mapped_skills,
            "requiresSkillExtractedStatusOnUpdate": bool(mapped_skills)
            and status in {"aligned", "aligned-with-followups"},
        }

        if status not in PLAYBOOK_STATUSES:
            add_finding(findings, "error", "readme", f"Invalid playbook status: {status}")
        if mapped_skills and status in {"aligned", "aligned-with-followups"}:
            add_finding(
                findings,
                "warning",
                "status",
                "Updating this mapped playbook requires setting status to skill-extracted until resync.",
            )

    result["valid"] = not any(finding["severity"] == "error" for finding in findings)
    return result


def emit_markdown(result: dict[str, Any]) -> None:
    target = result.get("targetPlaybook") or {}
    print(f"Target playbook: {target.get('relativePath', target.get('input', '(unknown)'))}")
    print(f"Valid: {str(result['valid']).lower()}")
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
        description="Inspect deterministic repository facts for a prompt-to-playbook request."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--source")
    parser.add_argument("--target-playbook", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = inspect_request(Path(args.repo_root), args.target_playbook, source=args.source)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["valid"]:
        emit_markdown(result)
    else:
        for finding in result["findings"]:
            if finding["severity"] == "error":
                print(finding["message"], file=sys.stderr)

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
