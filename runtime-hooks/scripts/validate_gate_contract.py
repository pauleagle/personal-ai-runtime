#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


GATES = {"pre-run", "pre-edit", "post-run"}
COMMON_REQUIRED_FIELDS = {
    "gate",
    "atomic_item_id",
    "spec_ref",
    "allowed_scope",
    "forbidden_scope",
    "acceptance_criteria",
    "expected_artifacts",
    "validation_plan",
}
PRE_EDIT_REQUIRED_FIELDS = {"proposed_changed_files"}
POST_RUN_REQUIRED_FIELDS = {
    "changed_files",
    "validation_actions",
    "acceptance_results",
    "remaining_risks",
    "follow_up_items",
    "commit_checkpoint",
}


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0
    return False


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, str):
        return [value]
    return []


def normalize_scope_value(value: Any) -> str:
    return str(value).replace("\\", "/").strip().strip("/")


def scope_matches(candidate: str, scope_entry: str) -> bool:
    candidate = normalize_scope_value(candidate)
    scope_entry = normalize_scope_value(scope_entry)

    if not candidate or not scope_entry:
        return False

    if scope_entry.endswith("/**"):
        prefix = scope_entry[:-3].rstrip("/")
        return candidate == prefix or candidate.startswith(prefix + "/")

    return candidate == scope_entry or candidate.startswith(scope_entry.rstrip("/") + "/")


def is_allowed(candidate: str, allowed_scope: Any) -> bool:
    return any(
        scope_matches(candidate, str(scope_entry))
        for scope_entry in as_list(allowed_scope)
    )


def is_forbidden(candidate: str, forbidden_scope: Any) -> bool:
    return any(
        scope_matches(candidate, str(scope_entry))
        for scope_entry in as_list(forbidden_scope)
        if normalize_scope_value(scope_entry).lower() not in {"none", "n/a"}
    )


def add_block(
    blocking_reasons: list[str],
    checked_items: list[dict[str, str]],
    item: str,
    reason: str,
) -> None:
    blocking_reasons.append(reason)
    checked_items.append({"item": item, "status": "blocked", "reason": reason})


def add_pass(checked_items: list[dict[str, str]], item: str) -> None:
    checked_items.append({"item": item, "status": "pass"})


def load_contract(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, ["gate contract file missing"]
    if not path.is_file():
        return None, ["gate contract path is not a file"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return None, ["gate contract root must be an object"]

    return data, []


def validate_required_fields(
    contract: dict[str, Any],
    required_fields: set[str],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    for field in sorted(required_fields):
        if field not in contract:
            add_block(
                blocking_reasons,
                checked_items,
                f"required:{field}",
                f"missing required field: {field}",
            )
        elif is_empty(contract[field]):
            add_block(
                blocking_reasons,
                checked_items,
                f"required:{field}",
                f"{field} must be non-empty",
            )
        else:
            add_pass(checked_items, f"required:{field}")


def validate_pre_edit_scope(
    contract: dict[str, Any],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    proposed_files = as_list(contract.get("proposed_changed_files"))
    allowed_scope = contract.get("allowed_scope")
    forbidden_scope = contract.get("forbidden_scope")

    for proposed_file in proposed_files:
        candidate = normalize_scope_value(proposed_file)
        if not candidate:
            add_block(
                blocking_reasons,
                checked_items,
                "pre-edit:proposed-file",
                "proposed_changed_files contains an empty path",
            )
            continue

        if not is_allowed(candidate, allowed_scope):
            add_block(
                blocking_reasons,
                checked_items,
                f"pre-edit:allowed:{candidate}",
                f"proposed file is outside allowed_scope: {candidate}",
            )
        else:
            add_pass(checked_items, f"pre-edit:allowed:{candidate}")

        if is_forbidden(candidate, forbidden_scope):
            add_block(
                blocking_reasons,
                checked_items,
                f"pre-edit:forbidden:{candidate}",
                f"proposed file is inside forbidden_scope: {candidate}",
            )
        else:
            add_pass(checked_items, f"pre-edit:forbidden:{candidate}")


def validate_commit_checkpoint(
    contract: dict[str, Any],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    checkpoint = contract.get("commit_checkpoint")

    if not isinstance(checkpoint, dict):
        add_block(
            blocking_reasons,
            checked_items,
            "post-run:commit-checkpoint",
            "commit_checkpoint must be an object",
        )
        return

    status = checkpoint.get("status")
    if status == "committed":
        if is_empty(checkpoint.get("commit")):
            add_block(
                blocking_reasons,
                checked_items,
                "post-run:commit-checkpoint",
                "committed checkpoint requires commit",
            )
        else:
            add_pass(checked_items, "post-run:commit-checkpoint")
        return

    if status in {"skipped", "blocked"}:
        if is_empty(checkpoint.get("skip_reason")) and is_empty(
            checkpoint.get("blocked_reason")
        ):
            add_block(
                blocking_reasons,
                checked_items,
                "post-run:commit-checkpoint",
                f"{status} checkpoint requires skip_reason or blocked_reason",
            )
        else:
            add_pass(checked_items, "post-run:commit-checkpoint")
        return

    add_block(
        blocking_reasons,
        checked_items,
        "post-run:commit-checkpoint",
        "commit_checkpoint.status must be committed, skipped, or blocked",
    )


def next_allowed_action(gate: str, blocked: bool) -> str:
    if blocked:
        if gate == "pre-edit":
            return "handoff"
        if gate == "post-run":
            return "validate"
        return "ask-user"
    if gate == "pre-run":
        return "edit"
    if gate == "pre-edit":
        return "edit"
    return "complete"


def validate_contract(path: Path) -> dict[str, Any]:
    path = path.resolve()
    contract, load_errors = load_contract(path)
    checked_items: list[dict[str, str]] = []
    blocking_reasons: list[str] = []
    notes: list[str] = []

    for error in load_errors:
        add_block(blocking_reasons, checked_items, "file", error)

    if contract is None:
        return {
            "gate": None,
            "status": "blocked",
            "path": str(path),
            "blocking_reasons": blocking_reasons,
            "checked_items": checked_items,
            "next_allowed_action": "ask-user",
            "notes": notes,
        }

    validate_required_fields(contract, COMMON_REQUIRED_FIELDS, checked_items, blocking_reasons)

    gate = contract.get("gate")
    if gate not in GATES:
        add_block(
            blocking_reasons,
            checked_items,
            "gate",
            f"gate must be one of: {', '.join(sorted(GATES))}",
        )
    else:
        add_pass(checked_items, f"gate:{gate}")

    if gate == "pre-edit":
        validate_required_fields(
            contract,
            PRE_EDIT_REQUIRED_FIELDS,
            checked_items,
            blocking_reasons,
        )
        if "proposed_changed_files" in contract and not is_empty(
            contract.get("proposed_changed_files")
        ):
            validate_pre_edit_scope(contract, checked_items, blocking_reasons)

    if gate == "post-run":
        validate_required_fields(
            contract,
            POST_RUN_REQUIRED_FIELDS,
            checked_items,
            blocking_reasons,
        )
        if "commit_checkpoint" in contract and not is_empty(contract.get("commit_checkpoint")):
            validate_commit_checkpoint(contract, checked_items, blocking_reasons)

    status = "blocked" if blocking_reasons else "pass"
    return {
        "gate": gate if gate in GATES else None,
        "status": status,
        "path": str(path),
        "blocking_reasons": blocking_reasons,
        "checked_items": checked_items,
        "next_allowed_action": next_allowed_action(gate, status == "blocked"),
        "notes": notes,
    }


def emit_markdown(result: dict[str, Any]) -> None:
    print(f"Gate contract: {result['path']}")
    print(f"Gate: {result['gate']}")
    print(f"Status: {result['status']}")
    print(f"Next allowed action: {result['next_allowed_action']}")
    print()
    print("### Blocking Reasons")
    print()
    if result["blocking_reasons"]:
        for reason in result["blocking_reasons"]:
            print(f"- {reason}")
    else:
        print("- (none)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a minimal spec-driven execution gate contract JSON artifact."
    )
    parser.add_argument("gate_contract")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = validate_contract(Path(args.gate_contract))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["status"] == "pass":
        emit_markdown(result)
    else:
        for reason in result["blocking_reasons"]:
            print(reason, file=sys.stderr)

    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
