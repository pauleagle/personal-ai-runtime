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
    repo_root = Path(input_path).resolve()

    if not repo_root.exists():
        raise ValueError(f"Repository path does not exist: {input_path}")
    if not repo_root.is_dir():
        raise ValueError(f"Repository path is not a directory: {input_path}")

    code, output = run_git(repo_root, ["rev-parse", "--show-toplevel"])
    if code != 0 or not output:
        details = " ".join(output) if output else "git rev-parse produced no output"
        raise ValueError(f"Not a git repository: {repo_root}. {details}")

    return Path(output[0]).resolve()


def collect_evidence(repo_root: Path, staged: bool = False) -> dict[str, Any]:
    diff_base = ["diff", "--cached"] if staged else ["diff"]
    commands = {
        "statusShort": ["status", "--short"],
        "diffNameOnly": [*diff_base, "--name-only"],
        "diffNameStatus": [*diff_base, "--name-status"],
        "diffStat": [*diff_base, "--stat"],
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

    result["valid"] = True
    result["message"] = "Git diff evidence collected."
    return result


def emit_markdown(result: dict[str, Any]) -> None:
    def print_list(title: str, values: list[str]) -> None:
        print(f"### {title}")
        print()
        print("```text")
        print("\n".join(values or ["(none)"]))
        print("```")
        print()

    print(f"Repository: {result['repoRoot']}")
    print(f"Mode: {'staged' if result['staged'] else 'working tree'}")
    print()
    print_list("Git Status Short", result["statusShort"])
    print_list("Diff Name Only", result["diffNameOnly"])
    print_list("Diff Name Status", result["diffNameStatus"])
    print_list("Diff Stat", result["diffStat"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Collect deterministic git status and diff evidence for diff-analysis."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        repo_root = resolve_repo_root(args.repo_root)
        result = collect_evidence(repo_root, staged=args.staged)
    except ValueError as exc:
        result = {
            "valid": False,
            "message": str(exc),
            "repoRoot": str(Path(args.repo_root).resolve()),
            "staged": args.staged,
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result.get("valid"):
            emit_markdown(result)
        else:
            print(result["message"], file=sys.stderr)

    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
