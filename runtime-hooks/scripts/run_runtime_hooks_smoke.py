#!/usr/bin/env python3
"""Run the runtime hook MVP smoke checks for a fresh local clone."""

import argparse
import importlib.util
import json
from pathlib import Path


ENVIRONMENT_HELPER = "runtime-hooks/scripts/check_runtime_hooks_environment.py"
VALIDATOR_HELPER = "runtime-hooks/scripts/validate_gate_contract.py"
SAMPLE_CONTRACTS = [
    "tests/fixtures/gate_contract_pre_run_sample.json",
    "tests/fixtures/gate_contract_pre_edit_sample.json",
    "tests/fixtures/gate_contract_post_run_sample.json",
]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load module: " + str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def summarize_gate_result(result):
    return {
        "gate": result.get("gate"),
        "status": result.get("status"),
        "path": result.get("path"),
        "blocking_reasons": result.get("blocking_reasons", []),
        "next_allowed_action": result.get("next_allowed_action"),
    }


def run_smoke(repo_root, version_info=None):
    repo_root = Path(repo_root)
    blocking_reasons = []
    gate_results = []

    try:
        environment = load_module(
            "check_runtime_hooks_environment",
            repo_root / ENVIRONMENT_HELPER,
        )
    except Exception as exc:
        reason = "unable to load environment helper: " + str(exc)
        return {
            "status": "blocked",
            "repo_root": str(repo_root.resolve()),
            "environment": None,
            "gate_results": gate_results,
            "blocking_reasons": [reason],
            "next_allowed_action": "fix-environment",
            "notes": [],
        }

    environment_result = environment.evaluate_environment(repo_root, version_info)
    if environment_result["status"] != "pass":
        return {
            "status": "blocked",
            "repo_root": str(repo_root.resolve()),
            "environment": environment_result,
            "gate_results": gate_results,
            "blocking_reasons": environment_result["blocking_reasons"],
            "next_allowed_action": "fix-environment",
            "notes": ["validator smoke skipped because environment check is blocked"],
        }

    try:
        validator = load_module("validate_gate_contract", repo_root / VALIDATOR_HELPER)
    except Exception as exc:
        reason = "unable to load gate contract validator: " + str(exc)
        return {
            "status": "blocked",
            "repo_root": str(repo_root.resolve()),
            "environment": environment_result,
            "gate_results": gate_results,
            "blocking_reasons": [reason],
            "next_allowed_action": "fix-environment",
            "notes": [],
        }

    for relative_path in SAMPLE_CONTRACTS:
        gate_result = validator.validate_contract(repo_root / relative_path)
        gate_summary = summarize_gate_result(gate_result)
        gate_results.append(gate_summary)
        if gate_summary["status"] != "pass":
            for reason in gate_summary["blocking_reasons"]:
                blocking_reasons.append(relative_path + ": " + reason)

    status = "blocked" if blocking_reasons else "pass"
    return {
        "status": status,
        "repo_root": str(repo_root.resolve()),
        "environment": environment_result,
        "gate_results": gate_results,
        "blocking_reasons": blocking_reasons,
        "next_allowed_action": "fix-contracts" if status == "blocked" else "ready",
        "notes": ["no third-party Python packages are required for the current MVP"],
    }


def emit_markdown(result):
    print("Runtime hooks smoke")
    print("Status: " + result["status"])
    print("Next allowed action: " + result["next_allowed_action"])
    print()
    print("### Gate Results")
    print()
    if result["gate_results"]:
        for gate_result in result["gate_results"]:
            print("- " + str(gate_result["gate"]) + ": " + gate_result["status"])
    else:
        print("- (none)")
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
        description="Run environment and sample contract smoke checks for runtime hook MVP."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = run_smoke(Path(args.repo_root))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_markdown(result)

    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
