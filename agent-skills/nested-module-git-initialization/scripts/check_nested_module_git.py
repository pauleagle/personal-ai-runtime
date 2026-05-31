#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def fail(code: int, message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def split_lines(text: str) -> list[str]:
    return text.splitlines()


def run_git(project_root: Path, args: list[str]) -> tuple[int, list[str]]:
    completed = subprocess.run(
        ["git", "-C", str(project_root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return completed.returncode, split_lines(completed.stdout)


def resolve_project_root(repo_root: Path, input_path: str) -> Path:
    raw_path = Path(input_path)

    if raw_path.is_absolute():
        candidates = [raw_path]
    else:
        candidates = [repo_root / raw_path, Path.cwd() / raw_path]

    for candidate in candidates:
        if candidate.exists():
            resolved = candidate.resolve()

            if not resolved.is_dir():
                fail(2, f"Project root is not a directory: {candidate}")

            return resolved

    fail(2, f"Project root does not exist: {input_path}")


def relative_to_workspace(project_root: Path, repo_root: Path) -> Path:
    try:
        return project_root.relative_to(repo_root)
    except ValueError:
        fail(2, f"Project root must be inside this workspace: {project_root}")


def validate_child_root(relative_path: Path) -> tuple[str, str]:
    parts = relative_path.parts

    if (
        len(parts) != 2
        or parts[0] not in {"modules", "poc-modules"}
        or not parts[1].strip()
    ):
        fail(
            2,
            "Project root must be exactly modules/<project> or "
            f"poc-modules/<project>: {relative_path.as_posix()}",
        )

    return parts[0], str(relative_path)


def emit_json(result: dict[str, Any]) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2))


def emit_markdown(result: dict[str, Any]) -> None:
    status = result["status"] or ["(clean)"]
    init_output = result["initOutput"] if result["gitInitExecuted"] else ["(not executed)"]
    notes = result["notes"] or ["(none)"]

    print("### Git Boundary Check")
    print()
    print(f"- Project root: {result['relativePath']}")
    print(f"- Absolute path: {result['projectRoot']}")
    print(f"- .git exists before: {result['gitExistsBefore']}")
    print(f"- .git exists after: {result['gitExistsAfter']}")
    print(f"- Action: {result['action']}")
    print()
    print("### Initialization Result")
    print()
    print(f"- git init executed: {result['gitInitExecuted']}")
    print(f"- Result: {' '.join(init_output)}")
    print(f"- Notes: {' '.join(notes)}")
    print()
    print("### Current Status")
    print()
    print("```text")
    print("\n".join(status))
    print("```")
    print()
    print("### Next Decisions")
    print()
    print("- Initial commit needed: manual decision")
    print("- Remote needed: manual decision")
    print("- Branch naming needed: manual decision")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or initialize Git boundaries for modules/<project> or poc-modules/<project>."
    )
    parser.add_argument("--project-root", "-ProjectRoot", required=True)
    parser.add_argument("--initialize", "-Initialize", action="store_true")
    parser.add_argument("--json", "-Json", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[3]
    project_root = resolve_project_root(repo_root, args.project_root)
    relative_path = relative_to_workspace(project_root, repo_root)
    root_kind, display_relative_path = validate_child_root(relative_path)

    git_path = project_root / ".git"
    git_exists_before = git_path.exists()
    git_init_executed = False
    init_output: list[str] = []
    notes: list[str] = []

    if git_exists_before:
        action = "existing-boundary"
        notes.append("Child project already has a .git directory or file.")
    elif args.initialize:
        git_init_executed = True
        init_code, init_output = run_git(project_root, ["init"])

        if init_code != 0:
            result = {
                "projectRoot": str(project_root),
                "relativePath": display_relative_path,
                "rootKind": root_kind,
                "gitExistsBefore": git_exists_before,
                "gitExistsAfter": git_path.exists(),
                "initializeRequested": args.initialize,
                "gitInitExecuted": git_init_executed,
                "action": "git-init-failed",
                "initOutput": init_output,
                "status": [],
                "notes": ["git init failed; no commit, remote, or tag was created."],
            }

            if args.json:
                emit_json(result)
            else:
                print(f"git init failed for {display_relative_path}", file=sys.stderr)
                print("\n".join(init_output), file=sys.stderr)

            return 3

        action = "initialized-boundary"
        notes.append("git init was executed because --initialize was provided.")
    else:
        action = "missing-boundary"
        notes.append("Child project has no .git directory or file.")
        notes.append(
            "Rerun with --initialize only if this task is actively editing or organizing the child project."
        )

    git_exists_after = git_path.exists()
    status_output: list[str] = []

    if git_exists_after:
        status_code, status_output = run_git(project_root, ["status", "--short"])

        if status_code != 0:
            result = {
                "projectRoot": str(project_root),
                "relativePath": display_relative_path,
                "rootKind": root_kind,
                "gitExistsBefore": git_exists_before,
                "gitExistsAfter": git_exists_after,
                "initializeRequested": args.initialize,
                "gitInitExecuted": git_init_executed,
                "action": "git-status-failed",
                "initOutput": init_output,
                "status": status_output,
                "notes": ["git status failed after the boundary check."],
            }

            if args.json:
                emit_json(result)
            else:
                print(f"git status failed for {display_relative_path}", file=sys.stderr)
                print("\n".join(status_output), file=sys.stderr)

            return 4
    else:
        status_output = ["(not run because child .git is missing)"]

    result = {
        "projectRoot": str(project_root),
        "relativePath": display_relative_path,
        "rootKind": root_kind,
        "gitExistsBefore": git_exists_before,
        "gitExistsAfter": git_exists_after,
        "initializeRequested": args.initialize,
        "gitInitExecuted": git_init_executed,
        "action": action,
        "initOutput": init_output,
        "status": status_output,
        "notes": notes,
    }

    if args.json:
        emit_json(result)
    else:
        emit_markdown(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
