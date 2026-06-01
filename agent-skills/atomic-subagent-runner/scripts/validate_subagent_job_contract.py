#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "job_id",
    "parent_atomic_item_id",
    "subagent_role",
    "context_pack",
    "allowed_scope",
    "forbidden_scope",
    "validation_requirements",
    "output_contract",
}
NON_EMPTY_FIELDS = {
    "job_id",
    "parent_atomic_item_id",
    "subagent_role",
    "context_pack",
    "allowed_scope",
    "validation_requirements",
    "output_contract",
}
SCOPE_FIELDS = {"allowed_scope", "forbidden_scope"}
OPTIONAL_GOVERNANCE_FIELDS = {"state_patch_policy", "merge_gate"}
HIDDEN_CONTEXT_RE = re.compile(r"previous chat|chat history|conversation memory|聊天記憶|前文", re.IGNORECASE)


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0
    return False


def add_finding(findings: list[dict[str, Any]], severity: str, area: str, message: str) -> None:
    findings.append({"severity": severity, "area": area, "message": message})


def scan_for_hidden_context(value: Any) -> bool:
    if isinstance(value, str):
        return bool(HIDDEN_CONTEXT_RE.search(value))
    if isinstance(value, list):
        return any(scan_for_hidden_context(item) for item in value)
    if isinstance(value, dict):
        return any(scan_for_hidden_context(item) for item in value.values())
    return False


def load_contract(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []

    if not path.exists():
        add_finding(findings, "error", "file", "job contract file missing")
        return None, findings
    if not path.is_file():
        add_finding(findings, "error", "file", "job contract path is not a file")
        return None, findings

    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_finding(findings, "error", "json", f"invalid JSON: {exc}")
        return None, findings

    if not isinstance(contract, dict):
        add_finding(findings, "error", "shape", "job contract root must be an object")
        return None, findings

    return contract, findings


def validate_contract(path: Path) -> dict[str, Any]:
    path = path.resolve()
    contract, findings = load_contract(path)
    result: dict[str, Any] = {
        "valid": False,
        "path": str(path),
        "findings": findings,
    }

    if contract is None:
        return result

    missing = sorted(REQUIRED_FIELDS - set(contract))
    for field in missing:
        add_finding(findings, "error", "required-fields", f"missing required field: {field}")

    for field in sorted(NON_EMPTY_FIELDS & set(contract)):
        if is_empty(contract[field]):
            add_finding(findings, "error", "required-fields", f"{field} must be non-empty")

    for field in sorted(SCOPE_FIELDS & set(contract)):
        if not isinstance(contract[field], (list, dict, str)):
            add_finding(findings, "error", "scope", f"{field} must be a string, list, or object")

    if "forbidden_scope" in contract and is_empty(contract["forbidden_scope"]):
        add_finding(
            findings,
            "warning",
            "scope",
            "forbidden_scope is empty; confirm this job truly has no forbidden scope.",
        )

    if OPTIONAL_GOVERNANCE_FIELDS.isdisjoint(contract):
        add_finding(
            findings,
            "warning",
            "governance",
            "state_patch_policy or merge_gate is absent.",
        )

    if scan_for_hidden_context(contract.get("context_pack")):
        add_finding(
            findings,
            "warning",
            "context-pack",
            "context_pack may rely on hidden chat history instead of durable artifacts.",
        )

    result["valid"] = not any(finding["severity"] == "error" for finding in findings)
    result["contract"] = contract
    return result


def emit_markdown(result: dict[str, Any]) -> None:
    print(f"Job contract: {result['path']}")
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
        description="Validate a bounded atomic subagent job contract JSON artifact."
    )
    parser.add_argument("job_contract")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = validate_contract(Path(args.job_contract))

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
