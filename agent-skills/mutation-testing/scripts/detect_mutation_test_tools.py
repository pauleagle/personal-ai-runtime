#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


MUTATION_BINARIES = ["mutmut", "cosmic-ray", "stryker", "stryker-js", "npx"]
DIRECT_MUTATION_BINARIES = {"mutmut", "cosmic-ray", "stryker", "stryker-js"}
TEST_BINARIES = ["pytest", "python", "python3", "npm", "pnpm", "yarn"]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def detect_package_json(repo_root: Path) -> dict[str, Any] | None:
    package_json = repo_root / "package.json"
    if not package_json.exists():
        return None

    try:
        package = read_json(package_json)
    except json.JSONDecodeError as exc:
        return {"path": str(package_json), "error": f"Invalid JSON: {exc}"}

    scripts = package.get("scripts", {})
    if not isinstance(scripts, dict):
        scripts = {}

    mutation_scripts = {
        name: command
        for name, command in scripts.items()
        if "mutat" in name.lower() or "stryker" in str(command).lower()
    }
    test_scripts = {
        name: command for name, command in scripts.items() if name == "test" or name.startswith("test:")
    }

    dependencies = {}
    for key in ("dependencies", "devDependencies", "optionalDependencies"):
        value = package.get(key, {})
        if isinstance(value, dict):
            dependencies.update(value)

    mutation_dependencies = {
        name: version
        for name, version in dependencies.items()
        if "stryker" in name.lower() or "mutat" in name.lower()
    }

    return {
        "path": str(package_json),
        "mutationScripts": mutation_scripts,
        "testScripts": test_scripts,
        "mutationDependencies": mutation_dependencies,
    }


def detect_python_project(repo_root: Path) -> dict[str, Any]:
    files = {
        "pyproject": repo_root / "pyproject.toml",
        "pytestIni": repo_root / "pytest.ini",
        "toxIni": repo_root / "tox.ini",
        "setupCfg": repo_root / "setup.cfg",
    }
    present = {name: str(path) for name, path in files.items() if path.exists()}
    tests_dirs = [
        str(path.relative_to(repo_root))
        for path in (repo_root / "tests", repo_root / "test")
        if path.exists() and path.is_dir()
    ]

    return {"files": present, "testsDirs": tests_dirs}


def which_all(names: list[str], path: str | None = None) -> dict[str, str | None]:
    return {name: shutil.which(name, path=path) for name in names}


def build_candidate_commands(result: dict[str, Any]) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []
    package = result.get("packageJson")

    if package and not package.get("error"):
        for name in package.get("testScripts", {}):
            commands.append({"kind": "test", "command": f"npm run {name}"})
        for name in package.get("mutationScripts", {}):
            commands.append({"kind": "mutation", "command": f"npm run {name}"})

    python_project = result["pythonProject"]
    tools = result["tools"]

    if python_project["testsDirs"] and tools["testBinaries"].get("python"):
        commands.append({"kind": "test", "command": "python -m unittest discover -s tests"})
    if python_project["testsDirs"] and tools["testBinaries"].get("pytest"):
        commands.append({"kind": "test", "command": "python -m pytest"})

    if tools["mutationBinaries"].get("mutmut"):
        commands.append({"kind": "mutation", "command": "mutmut run"})
    if tools["mutationBinaries"].get("cosmic-ray"):
        commands.append({"kind": "mutation", "command": "cosmic-ray run"})
    if package and not package.get("error") and package.get("mutationDependencies"):
        commands.append({"kind": "mutation", "command": "npx stryker run"})

    return commands


def detect(repo_root: Path, path: str | None = None) -> dict[str, Any]:
    repo_root = repo_root.resolve()

    if not repo_root.exists():
        return {"valid": False, "message": f"Repository path does not exist: {repo_root}"}
    if not repo_root.is_dir():
        return {"valid": False, "message": f"Repository path is not a directory: {repo_root}"}

    result: dict[str, Any] = {
        "valid": True,
        "message": "Mutation and test tooling evidence collected.",
        "repoRoot": str(repo_root),
        "tools": {
            "mutationBinaries": which_all(MUTATION_BINARIES, path=path),
            "testBinaries": which_all(TEST_BINARIES, path=path),
        },
        "packageJson": detect_package_json(repo_root),
        "pythonProject": detect_python_project(repo_root),
    }
    result["candidateCommands"] = build_candidate_commands(result)
    mutation_binaries = result["tools"]["mutationBinaries"]
    package = result.get("packageJson") or {}
    result["mutationToolingAvailable"] = any(
        mutation_binaries.get(name) for name in DIRECT_MUTATION_BINARIES
    ) or bool(package.get("mutationDependencies") or package.get("mutationScripts"))
    result["testToolingEvidence"] = bool(result["candidateCommands"]) or bool(
        result["pythonProject"]["testsDirs"]
    )
    return result


def emit_markdown(result: dict[str, Any]) -> None:
    print(f"Repository: {result.get('repoRoot', '(unknown)')}")
    print(f"Mutation tooling available: {result.get('mutationToolingAvailable', False)}")
    print()
    print("### Candidate Commands")
    print()

    commands = result.get("candidateCommands", [])
    if not commands:
        print("- (none)")
    else:
        for command in commands:
            print(f"- [{command['kind']}] {command['command']}")

    print()
    print("This script detects availability only; it does not run tests or mutation tooling.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Detect available test and mutation tooling without running mutation tests."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = detect(Path(args.repo_root), path=os.environ.get("PATH"))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result.get("valid"):
        emit_markdown(result)
    else:
        print(result["message"], file=sys.stderr)

    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
