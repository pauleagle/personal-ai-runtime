#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


CATEGORY_NAMES = {
    "added",
    "changed",
    "fixed",
    "removed",
    "docs",
    "internal",
    "deprecated",
    "security",
    "breaking changes",
}
NOISE_PATTERNS = {
    "todo": re.compile(r"\bTODO\b|待辦|尚未", re.IGNORECASE),
    "commit-log": re.compile(
        r"^\s*[-*]?\s*(feat|fix|docs|style|refactor|test|chore|build|ci)(\(.+\))?!?:",
        re.IGNORECASE,
    ),
    "merge-log": re.compile(r"\bMerge (branch|pull request)\b", re.IGNORECASE),
    "ai-residue": re.compile(r"\b(ChatGPT|Codex|Claude|AI conversation|assistant)\b", re.IGNORECASE),
}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
VERSION_RE = re.compile(r"(?:^|\[|v)(\d+\.\d+(?:\.\d+)?(?:[-+][0-9A-Za-z.-]+)?)", re.IGNORECASE)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def normalize_target_path(repo_root: Path, changelog: str) -> Path:
    candidate = Path(changelog)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    return candidate.resolve()


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def read_changelog(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError as exc:
        return None, f"File is not valid UTF-8: {exc}"


def extract_headings(lines: list[str]) -> list[dict[str, Any]]:
    headings: list[dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            headings.append(
                {
                    "line": index,
                    "level": len(match.group(1)),
                    "text": match.group(2).strip(),
                }
            )
    return headings


def parse_version_heading(text: str) -> dict[str, Any]:
    date_match = DATE_RE.search(text)
    version_match = VERSION_RE.search(text)
    lowered = text.lower()

    return {
        "text": text,
        "version": version_match.group(1) if version_match else None,
        "date": date_match.group(1) if date_match else None,
        "unreleased": "unreleased" in lowered,
    }


def is_version_heading(heading: dict[str, Any]) -> bool:
    if heading["level"] != 2:
        return False
    parsed = parse_version_heading(heading["text"])
    return bool(parsed["version"] or parsed["unreleased"])


def collect_version_sections(lines: list[str], headings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    version_headings = [heading for heading in headings if is_version_heading(heading)]
    sections: list[dict[str, Any]] = []

    for index, heading in enumerate(version_headings):
        parsed = parse_version_heading(heading["text"])
        next_line = (
            version_headings[index + 1]["line"]
            if index + 1 < len(version_headings)
            else len(lines) + 1
        )
        section_lines = lines[heading["line"] : next_line - 1]
        categories = []
        uncategorized_entries = []
        current_category = None

        for offset, line in enumerate(section_lines, start=heading["line"] + 1):
            heading_match = HEADING_RE.match(line)
            if heading_match:
                label = heading_match.group(2).strip()
                if len(heading_match.group(1)) == heading["level"] + 1:
                    current_category = label
                    if label.lower() in CATEGORY_NAMES:
                        categories.append({"line": offset, "text": label})
                continue

            if re.match(r"^\s*[-*]\s+", line) and current_category is None:
                uncategorized_entries.append(offset)

        sections.append(
            {
                "line": heading["line"],
                "text": heading["text"],
                "version": parsed["version"],
                "date": parsed["date"],
                "unreleased": parsed["unreleased"],
                "categories": categories,
                "uncategorizedEntryLines": uncategorized_entries,
            }
        )

    return sections


def collect_noise_findings(lines: list[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    for index, line in enumerate(lines, start=1):
        for area, pattern in NOISE_PATTERNS.items():
            if pattern.search(line):
                findings.append(
                    {
                        "severity": "warning",
                        "area": area,
                        "line": index,
                        "message": f"Potential {area} residue detected.",
                    }
                )

    return findings


def analyze_changelog(repo_root: Path, changelog: str) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    findings: list[dict[str, Any]] = []

    if not repo_root.exists() or not repo_root.is_dir():
        return {
            "valid": False,
            "message": f"Repository path does not exist or is not a directory: {repo_root}",
            "repoRoot": str(repo_root),
            "changelog": {"path": changelog, "exists": False},
            "findings": [
                {
                    "severity": "error",
                    "area": "repo-root",
                    "message": "Repository path is not a directory.",
                }
            ],
        }

    changelog_path = normalize_target_path(repo_root, changelog)
    if not is_relative_to(changelog_path, repo_root):
        return {
            "valid": False,
            "message": "Changelog path must stay inside repo root.",
            "repoRoot": str(repo_root),
            "changelog": {"path": str(changelog_path), "exists": changelog_path.exists()},
            "findings": [
                {
                    "severity": "error",
                    "area": "path",
                    "message": "Changelog path must stay inside repo root.",
                }
            ],
        }

    changelog_info: dict[str, Any] = {
        "path": changelog_path.relative_to(repo_root).as_posix(),
        "exists": changelog_path.exists(),
    }
    if not changelog_path.exists() or not changelog_path.is_file():
        return {
            "valid": False,
            "message": "Changelog file not found.",
            "repoRoot": str(repo_root),
            "changelog": changelog_info,
            "headings": [],
            "versionSections": [],
            "findings": [
                {
                    "severity": "error",
                    "area": "file",
                    "message": "Changelog file not found.",
                }
            ],
        }

    content, error = read_changelog(changelog_path)
    changelog_info["bytes"] = changelog_path.stat().st_size
    if error:
        return {
            "valid": False,
            "message": error,
            "repoRoot": str(repo_root),
            "changelog": changelog_info,
            "headings": [],
            "versionSections": [],
            "findings": [
                {
                    "severity": "error",
                    "area": "encoding",
                    "message": error,
                }
            ],
        }

    assert content is not None
    lines = content.splitlines()
    headings = extract_headings(lines)
    version_sections = collect_version_sections(lines, headings)
    changelog_info["lines"] = len(lines)

    if not headings:
        findings.append(
            {
                "severity": "warning",
                "area": "headings",
                "message": "No Markdown headings found.",
            }
        )
    elif headings[0]["level"] != 1:
        findings.append(
            {
                "severity": "warning",
                "area": "headings",
                "line": headings[0]["line"],
                "message": "First heading is not H1.",
            }
        )

    if not version_sections:
        findings.append(
            {
                "severity": "warning",
                "area": "versions",
                "message": "No H2 version or Unreleased sections detected.",
            }
        )

    unreleased_positions = [
        index for index, section in enumerate(version_sections) if section["unreleased"]
    ]
    if unreleased_positions and unreleased_positions[0] != 0:
        findings.append(
            {
                "severity": "warning",
                "area": "versions",
                "line": version_sections[unreleased_positions[0]]["line"],
                "message": "Unreleased section is not the first version section.",
            }
        )

    dated_sections = []
    for section in version_sections:
        if not section["unreleased"] and not section["date"]:
            findings.append(
                {
                    "severity": "warning",
                    "area": "dates",
                    "line": section["line"],
                    "message": "Released version section is missing an ISO date.",
                }
            )
        parsed = parse_date(section["date"])
        if parsed:
            dated_sections.append((section, parsed))
        if section["uncategorizedEntryLines"]:
            findings.append(
                {
                    "severity": "warning",
                    "area": "categories",
                    "line": section["uncategorizedEntryLines"][0],
                    "message": "Version section has list entries before a category heading.",
                }
            )

    for index in range(len(dated_sections) - 1):
        current_section, current_date = dated_sections[index]
        next_section, next_date = dated_sections[index + 1]
        if current_date < next_date:
            findings.append(
                {
                    "severity": "warning",
                    "area": "ordering",
                    "line": next_section["line"],
                    "message": "Dated version sections are not newest-first.",
                    "previousLine": current_section["line"],
                }
            )
            break

    findings.extend(collect_noise_findings(lines))

    return {
        "valid": not any(finding["severity"] == "error" for finding in findings),
        "message": "Changelog structure evidence collected.",
        "repoRoot": str(repo_root),
        "changelog": changelog_info,
        "headings": headings,
        "versionSections": version_sections,
        "findings": findings,
    }


def emit_markdown(result: dict[str, Any]) -> None:
    print(f"Changelog: {result['changelog']['path']}")
    print(f"Lines: {result['changelog'].get('lines', 0)}")
    print()
    print("### Version Sections")
    print()
    if not result.get("versionSections"):
        print("- (none)")
    else:
        for section in result["versionSections"]:
            categories = ", ".join(category["text"] for category in section["categories"]) or "(none)"
            date_value = section["date"] or "(missing date)"
            print(f"- line {section['line']}: {section['text']} [{date_value}; {categories}]")
    print()
    print("### Findings")
    print()
    if not result["findings"]:
        print("- (none)")
        return
    for finding in result["findings"]:
        location = f" line {finding['line']}" if "line" in finding else ""
        print(f"- [{finding['severity']}] {finding['area']}{location}: {finding['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Collect deterministic CHANGELOG.md structure evidence."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--changelog", default="CHANGELOG.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = analyze_changelog(Path(args.repo_root), args.changelog)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result.get("valid"):
        emit_markdown(result)
    else:
        print(result["message"], file=sys.stderr)

    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
