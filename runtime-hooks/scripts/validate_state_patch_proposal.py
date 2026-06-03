#!/usr/bin/env python3
"""Validate runtime hook gate-result state patch proposal artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ARTIFACT_TYPE = "runtime-hook-gate-result-state-patch-proposal"
PATCH_INTENT = "record-gate-result"
GATES = {"pre-run", "pre-edit", "post-run"}
GATE_STATUSES = {"pass", "blocked"}
COMMON_REQUIRED_FIELDS = {
    "artifact_type",
    "schema_version",
    "patch_intent",
    "source",
    "atomic_item_id",
    "gate",
    "gate_status",
    "next_allowed_action",
    "workflow_step",
    "queue_patch",
    "blocking_reasons",
    "validation_artifact",
    "checkpoint_status",
    "human_decision_required",
    "scope_decision_required",
    "commit_checkpoint",
    "boundaries",
}
ALLOW_EMPTY_REQUIRED_FIELDS = {"blocking_reasons"}


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0
    return False


def add_check(
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
    item: str,
    passed: bool,
    reason: str | None = None,
) -> None:
    check = {"item": item, "status": "pass" if passed else "blocked"}
    if reason:
        check["reason"] = reason
    checked_items.append(check)
    if not passed and reason:
        blocking_reasons.append(reason)


def load_proposal(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, ["state patch proposal file missing"]
    if not path.is_file():
        return None, ["state patch proposal path is not a file"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return None, ["state patch proposal root must be an object"]

    return data, []


def validate_required_fields(
    proposal: dict[str, Any],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    for field in sorted(COMMON_REQUIRED_FIELDS):
        if field not in proposal:
            add_check(
                checked_items,
                blocking_reasons,
                f"required:{field}",
                False,
                f"missing required field: {field}",
            )
        elif field not in ALLOW_EMPTY_REQUIRED_FIELDS and is_empty(proposal[field]):
            add_check(
                checked_items,
                blocking_reasons,
                f"required:{field}",
                False,
                f"{field} must be non-empty",
            )
        else:
            add_check(checked_items, blocking_reasons, f"required:{field}", True)


def validate_source(
    proposal: dict[str, Any],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    source = proposal.get("source")
    if not isinstance(source, dict):
        add_check(
            checked_items,
            blocking_reasons,
            "source",
            False,
            "source must be an object",
        )
        return

    for field in ["gate_contract", "gate_result_artifact", "attempted_command"]:
        if is_empty(source.get(field)):
            add_check(
                checked_items,
                blocking_reasons,
                f"source:{field}",
                False,
                f"source.{field} must be non-empty",
            )
        else:
            add_check(checked_items, blocking_reasons, f"source:{field}", True)


def validate_workflow_step(
    proposal: dict[str, Any],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    workflow_step = proposal.get("workflow_step")
    if not isinstance(workflow_step, dict):
        add_check(
            checked_items,
            blocking_reasons,
            "workflow_step",
            False,
            "workflow_step must be an object",
        )
        return

    for field in ["from", "proposed_to", "advance_allowed", "advance_decision_owner"]:
        if field not in workflow_step or is_empty(workflow_step[field]):
            add_check(
                checked_items,
                blocking_reasons,
                f"workflow_step:{field}",
                False,
                f"workflow_step.{field} must be non-empty",
            )
        else:
            add_check(checked_items, blocking_reasons, f"workflow_step:{field}", True)

    if "advance_allowed" in workflow_step and not isinstance(
        workflow_step["advance_allowed"], bool
    ):
        add_check(
            checked_items,
            blocking_reasons,
            "workflow_step:advance_allowed:type",
            False,
            "workflow_step.advance_allowed must be a boolean",
        )


def validate_queue_patch(
    proposal: dict[str, Any],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    queue_patch = proposal.get("queue_patch")
    if not isinstance(queue_patch, dict):
        add_check(
            checked_items,
            blocking_reasons,
            "queue_patch",
            False,
            "queue_patch must be an object",
        )
        return

    for field in ["operation", "from", "to"]:
        if is_empty(queue_patch.get(field)):
            add_check(
                checked_items,
                blocking_reasons,
                f"queue_patch:{field}",
                False,
                f"queue_patch.{field} must be non-empty",
            )
        else:
            add_check(checked_items, blocking_reasons, f"queue_patch:{field}", True)


def validate_commit_checkpoint(
    proposal: dict[str, Any],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    commit_checkpoint = proposal.get("commit_checkpoint")
    if not isinstance(commit_checkpoint, dict):
        add_check(
            checked_items,
            blocking_reasons,
            "commit_checkpoint",
            False,
            "commit_checkpoint must be an object",
        )
        return

    status = commit_checkpoint.get("status")
    if is_empty(status):
        add_check(
            checked_items,
            blocking_reasons,
            "commit_checkpoint:status",
            False,
            "commit_checkpoint.status must be non-empty",
        )
    else:
        add_check(checked_items, blocking_reasons, "commit_checkpoint:status", True)

    if status == "not-applicable" and is_empty(commit_checkpoint.get("reason")):
        add_check(
            checked_items,
            blocking_reasons,
            "commit_checkpoint:reason",
            False,
            "not-applicable commit checkpoint requires reason",
        )


def validate_semantics(
    proposal: dict[str, Any],
    checked_items: list[dict[str, str]],
    blocking_reasons: list[str],
) -> None:
    artifact_type = proposal.get("artifact_type")
    add_check(
        checked_items,
        blocking_reasons,
        "artifact_type",
        artifact_type == ARTIFACT_TYPE,
        None
        if artifact_type == ARTIFACT_TYPE
        else "artifact_type must be runtime-hook-gate-result-state-patch-proposal",
    )

    patch_intent = proposal.get("patch_intent")
    add_check(
        checked_items,
        blocking_reasons,
        "patch_intent",
        patch_intent == PATCH_INTENT,
        None if patch_intent == PATCH_INTENT else "patch_intent must be record-gate-result",
    )

    gate = proposal.get("gate")
    add_check(
        checked_items,
        blocking_reasons,
        "gate",
        gate in GATES,
        None if gate in GATES else "gate must be pre-run, pre-edit, or post-run",
    )

    gate_status = proposal.get("gate_status")
    add_check(
        checked_items,
        blocking_reasons,
        "gate_status",
        gate_status in GATE_STATUSES,
        None if gate_status in GATE_STATUSES else "gate_status must be pass or blocked",
    )

    if not isinstance(proposal.get("human_decision_required"), bool):
        add_check(
            checked_items,
            blocking_reasons,
            "human_decision_required:type",
            False,
            "human_decision_required must be a boolean",
        )

    if not isinstance(proposal.get("scope_decision_required"), bool):
        add_check(
            checked_items,
            blocking_reasons,
            "scope_decision_required:type",
            False,
            "scope_decision_required must be a boolean",
        )

    blocking_items = proposal.get("blocking_reasons")
    if not isinstance(blocking_items, list):
        add_check(
            checked_items,
            blocking_reasons,
            "blocking_reasons:type",
            False,
            "blocking_reasons must be a list",
        )
        return

    workflow_step = proposal.get("workflow_step")
    queue_patch = proposal.get("queue_patch")

    if gate_status == "pass":
        if blocking_items:
            add_check(
                checked_items,
                blocking_reasons,
                "pass:blocking_reasons",
                False,
                "passing proposal must not include blocking_reasons",
            )
        else:
            add_check(checked_items, blocking_reasons, "pass:blocking_reasons", True)

    if gate_status == "blocked":
        if not blocking_items:
            add_check(
                checked_items,
                blocking_reasons,
                "blocked:blocking_reasons",
                False,
                "blocked proposal requires blocking_reasons",
            )
        else:
            add_check(checked_items, blocking_reasons, "blocked:blocking_reasons", True)

        if isinstance(workflow_step, dict) and workflow_step.get("advance_allowed") is not False:
            add_check(
                checked_items,
                blocking_reasons,
                "blocked:advance_allowed",
                False,
                "blocked proposal must set workflow_step.advance_allowed to false",
            )
        else:
            add_check(checked_items, blocking_reasons, "blocked:advance_allowed", True)

        if isinstance(queue_patch, dict) and queue_patch.get("to") != "blocked":
            add_check(
                checked_items,
                blocking_reasons,
                "blocked:queue_patch",
                False,
                "blocked proposal must set queue_patch.to to blocked",
            )
        else:
            add_check(checked_items, blocking_reasons, "blocked:queue_patch", True)


def validate_proposal(path: Path) -> dict[str, Any]:
    path = path.resolve()
    proposal, load_errors = load_proposal(path)
    checked_items: list[dict[str, str]] = []
    blocking_reasons: list[str] = []

    for error in load_errors:
        add_check(checked_items, blocking_reasons, "file", False, error)

    if proposal is not None:
        validate_required_fields(proposal, checked_items, blocking_reasons)
        validate_source(proposal, checked_items, blocking_reasons)
        validate_workflow_step(proposal, checked_items, blocking_reasons)
        validate_queue_patch(proposal, checked_items, blocking_reasons)
        validate_commit_checkpoint(proposal, checked_items, blocking_reasons)
        validate_semantics(proposal, checked_items, blocking_reasons)

    status = "blocked" if blocking_reasons else "pass"
    return {
        "status": status,
        "path": str(path),
        "artifact_type": proposal.get("artifact_type") if proposal else None,
        "gate": proposal.get("gate") if proposal else None,
        "gate_status": proposal.get("gate_status") if proposal else None,
        "blocking_reasons": blocking_reasons,
        "checked_items": checked_items,
        "next_allowed_action": "handoff" if status == "blocked" else "ready",
        "notes": [
            "This validator checks patch proposal artifacts only; it does not mutate orchestrator state."
        ],
    }


def emit_markdown(result: dict[str, Any]) -> None:
    print("State patch proposal: " + result["path"])
    print("Status: " + result["status"])
    print("Gate: " + str(result["gate"]))
    print("Gate status: " + str(result["gate_status"]))
    print("Next allowed action: " + result["next_allowed_action"])
    print()
    print("### Blocking Reasons")
    print()
    if result["blocking_reasons"]:
        for reason in result["blocking_reasons"]:
            print("- " + reason)
    else:
        print("- (none)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a runtime hook gate-result state patch proposal artifact."
    )
    parser.add_argument("state_patch_proposal")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = validate_proposal(Path(args.state_patch_proposal))

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
