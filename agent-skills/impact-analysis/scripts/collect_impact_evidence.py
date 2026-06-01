#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def split_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]


def run_git(repo_root: Path, args: list[str]) -> tuple[int, list[str]]:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return completed.returncode, split_lines(completed.stdout)


def resolve_repo_root(input_path: str) -> Path:
    candidate = Path(input_path).resolve()

    if not candidate.exists():
        raise ValueError(f"Repository path does not exist: {input_path}")
    if not candidate.is_dir():
        raise ValueError(f"Repository path is not a directory: {input_path}")

    code, output = run_git(candidate, ["rev-parse", "--show-toplevel"])
    if code != 0 or not output:
        details = " ".join(output) if output else "git rev-parse produced no output"
        raise ValueError(f"Not a git repository: {candidate}. {details}")

    return Path(output[0]).resolve()


def normalize_git_path(path: str) -> str:
    if "\t" in path:
        path = path.split("\t")[-1]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip().replace("\\", "/")


def path_categories(path: str) -> list[str]:
    normalized = normalize_git_path(path).lower()
    parts = normalized.split("/")
    name = parts[-1] if parts else normalized
    categories: set[str] = set()

    if any(part in {"test", "tests", "__tests__"} for part in parts) or name.startswith("test_"):
        categories.add("tests")
    if any(part in {"spec", "specs"} for part in parts) or name in {"spec.md", "mvp.md"}:
        categories.add("specs")
    if any(part in {"src", "lib", "app", "packages"} for part in parts):
        categories.add("source")
    if any(part in {"docs", "doc"} for part in parts) or name in {"readme.md", "changelog.md"}:
        categories.add("docs")
    if name in {
        "package.json",
        "package-lock.json",
        "pyproject.toml",
        "requirements.txt",
        "uv.lock",
        "poetry.lock",
        "tsconfig.json",
        "jest.config.js",
        "pytest.ini",
    }:
        categories.add("config")
    if (
        any(part in {"dist", "build", "coverage", "generated", "__pycache__"} for part in parts)
        or name.endswith(".pyc")
    ):
        categories.add("generated")

    if not categories:
        categories.add("other")

    return sorted(categories)


def expand_status_path(repo_root: Path, path: str) -> list[str]:
    normalized = normalize_git_path(path)
    full_path = repo_root / normalized

    if full_path.is_dir():
        return sorted(
            child.relative_to(repo_root).as_posix()
            for child in full_path.rglob("*")
            if child.is_file()
            and "__pycache__" not in child.parts
            and child.suffix != ".pyc"
        )

    return [normalized]


def collect_changed_paths(repo_root: Path, staged: bool = False) -> dict[str, Any]:
    diff_base = ["diff", "--cached"] if staged else ["diff"]
    commands = {
        "statusShort": ["status", "--short"],
        "diffNameOnly": [*diff_base, "--name-only"],
        "diffNameStatus": [*diff_base, "--name-status"],
    }
    result: dict[str, Any] = {
        "repoRoot": str(repo_root),
        "staged": staged,
        "commands": {},
    }

    for key, args in commands.items():
        code, output = run_git(repo_root, args)
        result[key] = output
        result["commands"][key] = {
            "args": ["git", "-C", str(repo_root), *args],
            "returncode": code,
        }
        if code != 0:
            result["valid"] = False
            result["message"] = f"git {' '.join(args)} failed"
            return result

    changed_paths = sorted({normalize_git_path(path) for path in result["diffNameOnly"]})
    status_paths = sorted(
        {
            expanded_path
            for line in result["statusShort"]
            if line
            for expanded_path in expand_status_path(repo_root, line[3:] if len(line) > 3 else line)
        }
    )
    all_paths = sorted(set(changed_paths) | set(status_paths))

    path_impacts = [
        {"path": path, "categories": path_categories(path)}
        for path in all_paths
    ]
    category_counts: dict[str, int] = {}
    for impact in path_impacts:
        for category in impact["categories"]:
            category_counts[category] = category_counts.get(category, 0) + 1

    result.update(
        {
            "valid": True,
            "message": "Impact evidence collected.",
            "changedPaths": changed_paths,
            "statusPaths": status_paths,
            "pathImpacts": path_impacts,
            "categoryCounts": dict(sorted(category_counts.items())),
        }
    )
    return result


def emit_markdown(result: dict[str, Any]) -> None:
    print(f"Repository: {result['repoRoot']}")
    print(f"Mode: {'staged' if result['staged'] else 'working tree'}")
    print()
    print("### Path Impact Evidence")
    print()

    if not result["pathImpacts"]:
        print("- (none)")
        return

    for impact in result["pathImpacts"]:
        print(f"- {impact['path']}: {', '.join(impact['categories'])}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Collect deterministic changed-path evidence for impact-analysis."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        repo_root = resolve_repo_root(args.repo_root)
        result = collect_changed_paths(repo_root, staged=args.staged)
    except ValueError as exc:
        result = {
            "valid": False,
            "message": str(exc),
            "repoRoot": str(Path(args.repo_root).resolve()),
            "staged": args.staged,
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result.get("valid"):
        emit_markdown(result)
    else:
        print(result["message"], file=sys.stderr)

    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
