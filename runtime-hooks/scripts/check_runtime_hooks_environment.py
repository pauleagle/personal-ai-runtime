#!/usr/bin/env python3
"""Check the minimal local environment for runtime hook MVP helpers.

This script intentionally avoids Python 3.10-only syntax so that older Python
versions can still report a clear blocked result instead of failing at parse time.
"""

import argparse
import json
import sys
from pathlib import Path


MINIMUM_PYTHON = (3, 10)
REQUIRED_FILES = [
    "runtime-hooks/scripts/check_runtime_hooks_environment.py",
    "runtime-hooks/scripts/enforce_pre_edit_gate.py",
    "runtime-hooks/scripts/run_runtime_hooks_smoke.py",
    "runtime-hooks/scripts/validate_gate_contract.py",
    "tests/fixtures/gate_contract_pre_run_sample.json",
    "tests/fixtures/gate_contract_pre_edit_sample.json",
    "tests/fixtures/gate_contract_post_run_sample.json",
]


def format_version(version_info):
    return ".".join(str(part) for part in version_info[:3])


def add_check(checks, item, passed, reason=None):
    check = {"item": item, "status": "pass" if passed else "blocked"}
    if reason:
        check["reason"] = reason
    checks.append(check)


def evaluate_environment(repo_root, version_info=None):
    if version_info is None:
        version_info = sys.version_info

    repo_root = Path(repo_root)
    checks = []
    blocking_reasons = []

    version_passed = tuple(version_info[:2]) >= MINIMUM_PYTHON
    if version_passed:
        add_check(checks, "python-version", True)
    else:
        reason = (
            "Python "
            + ".".join(str(part) for part in MINIMUM_PYTHON)
            + " or newer is required; found "
            + format_version(version_info)
        )
        blocking_reasons.append(reason)
        add_check(checks, "python-version", False, reason)

    for relative_path in REQUIRED_FILES:
        candidate = repo_root / relative_path
        if candidate.is_file():
            add_check(checks, "file:" + relative_path, True)
        else:
            reason = "required file missing: " + relative_path
            blocking_reasons.append(reason)
            add_check(checks, "file:" + relative_path, False, reason)

    status = "blocked" if blocking_reasons else "pass"
    return {
        "status": status,
        "python_version": format_version(version_info),
        "minimum_python": ".".join(str(part) for part in MINIMUM_PYTHON),
        "repo_root": str(repo_root.resolve()),
        "blocking_reasons": blocking_reasons,
        "checked_items": checks,
        "next_allowed_action": "run-validator-smoke" if status == "pass" else "fix-environment",
        "notes": ["no third-party Python packages are required for the current MVP"],
    }


def emit_markdown(result):
    print("Runtime hooks environment")
    print("Status: " + result["status"])
    print("Python: " + result["python_version"])
    print("Minimum Python: " + result["minimum_python"])
    print("Next allowed action: " + result["next_allowed_action"])
    print()
    print("### Blocking Reasons")
    print()
    if result["blocking_reasons"]:
        for reason in result["blocking_reasons"]:
            print("- " + reason)
    else:
        print("- (none)")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check the minimal environment required by runtime hook MVP helpers."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = evaluate_environment(Path(args.repo_root))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_markdown(result)

    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
