#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "workflow_step",
    "implementation_status",
    "ready",
    "running",
    "blocked",
    "completed",
}
QUEUE_FIELDS = {"ready", "running", "blocked", "completed", "deferred"}


def validate_state_file(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "valid": False,
        "path": str(path.resolve()),
        "findings": [],
    }

    if not path.exists():
        result["findings"].append({"severity": "error", "message": "state file missing"})
        return result
    if not path.is_file():
        result["findings"].append({"severity": "error", "message": "state path is not a file"})
        return result

    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result["findings"].append({"severity": "error", "message": f"invalid JSON: {exc}"})
        return result

    if not isinstance(state, dict):
        result["findings"].append({"severity": "error", "message": "state root must be an object"})
        return result

    missing = sorted(REQUIRED_FIELDS - set(state))
    for field in missing:
        result["findings"].append({"severity": "error", "message": f"missing required field: {field}"})

    for field in sorted(QUEUE_FIELDS & set(state)):
        if not isinstance(state[field], list):
            result["findings"].append({"severity": "error", "message": f"{field} must be a list"})

    if state.get("workflow_step") in {"", None}:
        result["findings"].append({"severity": "error", "message": "workflow_step must be non-empty"})

    if state.get("implementation_status") in {"", None}:
        result["findings"].append({"severity": "error", "message": "implementation_status must be non-empty"})

    result["valid"] = not any(item["severity"] == "error" for item in result["findings"])
    result["state"] = state
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a durable orchestrator state JSON artifact.")
    parser.add_argument("state_file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = validate_state_file(Path(args.state_file))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["valid"]:
        print("Orchestrator state is valid.")
    else:
        for finding in result["findings"]:
            print(finding["message"], file=sys.stderr)

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
