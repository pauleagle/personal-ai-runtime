#!/usr/bin/env python3
"""Mounted pre-edit guard for explicit runtime hook contracts."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


VALIDATOR_HELPER = "runtime-hooks/scripts/validate_gate_contract.py"


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load module: " + str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def resolve_contract_path(repo_root: Path, contract_path: str | Path) -> Path:
    path = Path(contract_path)
    if path.is_absolute():
        return path
    return repo_root / path


def load_contract_metadata(contract_path: Path) -> dict[str, Any]:
    try:
        data = json.loads(contract_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def build_handoff_note(
    contract: dict[str, Any],
    gate_result: dict[str, Any],
    blocking_reasons: list[str],
    attempted_command: str,
    contract_path: Path,
) -> dict[str, Any]:
    return {
        "atomic_item_id": contract.get("atomic_item_id"),
        "gate": gate_result.get("gate"),
        "gate_status": "blocked",
        "blocking_reasons": blocking_reasons,
        "next_allowed_action": "handoff",
        "attempted_command": attempted_command,
        "scope_decision_needed": True,
        "resume_from": str(contract_path),
    }


def enforce_pre_edit_gate(
    repo_root: str | Path,
    contract_path: str | Path,
    attempted_command: str | None = None,
    handoff_note_out: str | Path | None = None,
) -> dict[str, Any]:
    repo_root = Path(repo_root)
    resolved_contract_path = resolve_contract_path(repo_root, contract_path)
    validator = load_module("validate_gate_contract", repo_root / VALIDATOR_HELPER)
    gate_result = validator.validate_contract(resolved_contract_path)
    contract = load_contract_metadata(resolved_contract_path)
    blocking_reasons = list(gate_result.get("blocking_reasons", []))
    checked_items = [
        {
            "item": "mounted-hook:validator-result",
            "status": "pass" if gate_result.get("status") == "pass" else "blocked",
        }
    ]

    if gate_result.get("gate") != "pre-edit":
        reason = "mounted pre-edit guard requires gate: pre-edit"
        blocking_reasons.append(reason)
        checked_items.append(
            {
                "item": "mounted-hook:gate-type",
                "status": "blocked",
                "reason": reason,
            }
        )
    else:
        checked_items.append({"item": "mounted-hook:gate-type", "status": "pass"})

    status = "blocked" if blocking_reasons else "pass"
    next_allowed_action = "edit" if status == "pass" else "handoff"
    if attempted_command is None:
        attempted_command = (
            "python runtime-hooks\\scripts\\enforce_pre_edit_gate.py "
            + str(contract_path)
            + " --json"
        )

    handoff_note = None
    handoff_note_path = None
    if status == "blocked":
        handoff_note = build_handoff_note(
            contract,
            gate_result,
            blocking_reasons,
            attempted_command,
            resolved_contract_path,
        )
        if handoff_note_out is not None:
            handoff_note_path = Path(handoff_note_out)
            handoff_note_path.parent.mkdir(parents=True, exist_ok=True)
            handoff_note_path.write_text(
                json.dumps(handoff_note, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    return {
        "hook": "pre-edit",
        "mount_layer": "manual-orchestrator-step",
        "enforcement_mode": "hard-block",
        "status": status,
        "allowed_to_edit": status == "pass",
        "contract_path": str(resolved_contract_path.resolve()),
        "gate_result": gate_result,
        "blocking_reasons": blocking_reasons,
        "checked_items": checked_items,
        "next_allowed_action": next_allowed_action,
        "handoff_note": handoff_note,
        "handoff_note_path": str(handoff_note_path) if handoff_note_path else None,
        "notes": [
            "This guard validates explicit pre-edit contracts only; it does not intercept tool calls."
        ],
    }


def emit_markdown(result: dict[str, Any]) -> None:
    print("Pre-edit gate guard")
    print("Status: " + result["status"])
    print("Allowed to edit: " + str(result["allowed_to_edit"]).lower())
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
        description="Run the mounted hard-block pre-edit guard for one explicit gate contract."
    )
    parser.add_argument("gate_contract")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--handoff-note-out",
        help="Write the blocked handoff note JSON to this path when the guard blocks.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    attempted_command = (
        "python runtime-hooks\\scripts\\enforce_pre_edit_gate.py "
        + args.gate_contract
        + " --repo-root "
        + args.repo_root
        + (" --handoff-note-out " + args.handoff_note_out if args.handoff_note_out else "")
        + (" --json" if args.json else "")
    )
    result = enforce_pre_edit_gate(
        Path(args.repo_root),
        args.gate_contract,
        attempted_command=attempted_command,
        handoff_note_out=args.handoff_note_out,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_markdown(result)

    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
