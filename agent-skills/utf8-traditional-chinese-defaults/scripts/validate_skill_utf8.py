#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


MAX_SKILL_NAME_LENGTH = 64
ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}


def validate_skill(skill_path: Path) -> tuple[bool, str, dict[str, Any]]:
    skill_path = skill_path.resolve()
    skill_md = skill_path / "SKILL.md"

    details: dict[str, Any] = {
        "skillPath": str(skill_path),
        "skillFile": str(skill_md),
        "encoding": "utf-8",
    }

    if not skill_md.exists():
        return False, "SKILL.md not found", details

    try:
        content = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        details["decodeError"] = str(exc)
        return False, f"SKILL.md is not valid UTF-8: {exc}", details

    if not content.startswith("---"):
        return False, "No YAML frontmatter found", details

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", details

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML in frontmatter: {exc}", details

    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary", details

    details["frontmatter"] = frontmatter

    unexpected_keys = set(frontmatter) - ALLOWED_PROPERTIES
    if unexpected_keys:
        allowed = ", ".join(sorted(ALLOWED_PROPERTIES))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
            details,
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter", details
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter", details

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}", details

    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
                details,
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
                details,
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
                details,
            )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}", details

    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)", details
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
                details,
            )

    return True, "Skill is valid!", details


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate SKILL.md frontmatter using explicit UTF-8 decoding."
    )
    parser.add_argument("skill_directory")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    valid, message, details = validate_skill(Path(args.skill_directory))
    result = {"valid": valid, "message": message, **details}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(message)

    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
