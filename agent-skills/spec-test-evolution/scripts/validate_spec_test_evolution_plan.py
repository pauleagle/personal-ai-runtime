#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "decision_source",
    "affected_artifacts",
    "updates",
    "traceability",
    "rerun_point",
    "next_validation_step",
}
UPDATE_FIELDS = {
    "spec_updates",
    "test_updates",
    "index_updates",
    "workflow_note_updates",
    "backlog_updates",
}
TRACEABILITY_REQUIRED_FIELDS = {"parent_refs", "child_refs"}
AMBIGUOUS_DECISION_RE = re.compile(r"\b(TBD|TODO|unclear|unknown|maybe)\b|待確認|未定", re.IGNORECASE)


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


def load_plan(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []

    if not path.exists():
        add_finding(findings, "error", "file", "evolution plan file missing")
        return None, findings
    if not path.is_file():
        add_finding(findings, "error", "file", "evolution plan path is not a file")
        return None, findings

    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_finding(findings, "error", "json", f"invalid JSON: {exc}")
        return None, findings

    if not isinstance(plan, dict):
        add_finding(findings, "error", "shape", "evolution plan root must be an object")
        return None, findings

    return plan, findings


def validate_plan(path: Path) -> dict[str, Any]:
    path = path.resolve()
    plan, findings = load_plan(path)
    result: dict[str, Any] = {
        "valid": False,
        "path": str(path),
        "findings": findings,
    }

    if plan is None:
        return result

    for field in sorted(REQUIRED_FIELDS - set(plan)):
        add_finding(findings, "error", "required-fields", f"missing required field: {field}")

    for field in sorted(REQUIRED_FIELDS & set(plan)):
        if is_empty(plan[field]):
            add_finding(findings, "error", "required-fields", f"{field} must be non-empty")

    decision_source = plan.get("decision_source")
    if isinstance(decision_source, str) and AMBIGUOUS_DECISION_RE.search(decision_source):
        add_finding(
            findings,
            "warning",
            "decision-source",
            "decision_source appears ambiguous; confirm a human decision or non-ambiguous gap source exists.",
        )

    affected_artifacts = plan.get("affected_artifacts")
    if "affected_artifacts" in plan and not isinstance(affected_artifacts, list):
        add_finding(findings, "error", "affected-artifacts", "affected_artifacts must be a list")

    updates = plan.get("updates")
    if "updates" in plan and not isinstance(updates, dict):
        add_finding(findings, "error", "updates", "updates must be an object")
    elif isinstance(updates, dict):
        present_update_fields = UPDATE_FIELDS & set(updates)
        if not present_update_fields:
            add_finding(
                findings,
                "warning",
                "updates",
                "updates does not declare spec/test/index/workflow/backlog update groups.",
            )
        if not any(not is_empty(updates[field]) for field in present_update_fields):
            add_finding(findings, "error", "updates", "at least one update group must be non-empty")

    traceability = plan.get("traceability")
    if "traceability" in plan and not isinstance(traceability, dict):
        add_finding(findings, "error", "traceability", "traceability must be an object")
    elif isinstance(traceability, dict):
        for field in sorted(TRACEABILITY_REQUIRED_FIELDS - set(traceability)):
            add_finding(findings, "error", "traceability", f"missing traceability field: {field}")
        for field in sorted(TRACEABILITY_REQUIRED_FIELDS & set(traceability)):
            if is_empty(traceability[field]):
                add_finding(findings, "error", "traceability", f"{field} must be non-empty")
        if is_empty(traceability.get("root_index_refs")):
            add_finding(
                findings,
                "warning",
                "traceability",
                "root_index_refs is absent or empty; confirm no root index applies.",
            )

    result["valid"] = not any(finding["severity"] == "error" for finding in findings)
    result["plan"] = plan
    return result


def emit_markdown(result: dict[str, Any]) -> None:
    print(f"Evolution plan: {result['path']}")
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
        description="Validate a spec/test evolution plan JSON artifact."
    )
    parser.add_argument("evolution_plan")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = validate_plan(Path(args.evolution_plan))

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
