#!/usr/bin/env python3
"""Run the runtime hook MVP smoke checks for a fresh local clone."""

import argparse
import importlib.util
import json
from pathlib import Path


ENVIRONMENT_HELPER = "runtime-hooks/scripts/check_runtime_hooks_environment.py"
PRE_EDIT_GUARD_HELPER = "runtime-hooks/scripts/enforce_pre_edit_gate.py"
STATE_PATCH_PROPOSAL_HELPER = "runtime-hooks/scripts/validate_state_patch_proposal.py"
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


def summarize_pre_edit_guard_result(result):
    return {
        "hook": result.get("hook"),
        "status": result.get("status"),
        "allowed_to_edit": result.get("allowed_to_edit"),
        "contract_path": result.get("contract_path"),
        "handoff_note_path": result.get("handoff_note_path"),
        "blocking_reasons": result.get("blocking_reasons", []),
        "next_allowed_action": result.get("next_allowed_action"),
    }


def summarize_state_patch_proposal_result(result):
    return {
        "status": result.get("status"),
        "path": result.get("path"),
        "artifact_type": result.get("artifact_type"),
        "atomic_item_id": result.get("atomic_item_id"),
        "source_gate_contract": result.get("source_gate_contract"),
        "gate": result.get("gate"),
        "gate_status": result.get("gate_status"),
        "validation_artifact": result.get("validation_artifact"),
        "blocking_reasons": result.get("blocking_reasons", []),
        "next_allowed_action": result.get("next_allowed_action"),
    }


def normalize_contract_paths(contract_paths):
    if contract_paths:
        return [str(path) for path in contract_paths]
    return list(SAMPLE_CONTRACTS)


def normalize_state_patch_proposal_paths(state_patch_proposal_paths):
    if state_patch_proposal_paths:
        return [str(path) for path in state_patch_proposal_paths]
    return []


def normalize_artifact_path(path):
    if not path:
        return None
    return str(path).replace("\\", "/").lstrip("./")


def proposal_matches_contract(proposal, expected_contract_path):
    expected = normalize_artifact_path(expected_contract_path)
    return expected in {
        normalize_artifact_path(proposal.get("source_gate_contract")),
        normalize_artifact_path(proposal.get("validation_artifact")),
    }


def find_matching_pre_edit_proposal(
    pre_edit_guard_result,
    proposal_results,
    expected_contract_path,
):
    if not pre_edit_guard_result:
        return None

    guard_status = pre_edit_guard_result.get("status")
    for proposal in proposal_results:
        if (
            proposal.get("status") == "pass"
            and proposal.get("gate") == "pre-edit"
            and proposal.get("gate_status") == guard_status
            and proposal_matches_contract(proposal, expected_contract_path)
        ):
            return proposal

    return None


def build_pre_edit_proposal_consistency_check(
    pre_edit_guard_result,
    proposal_results,
    expected_contract_path,
):
    guard_status = pre_edit_guard_result.get("status")
    matched_proposal = find_matching_pre_edit_proposal(
        pre_edit_guard_result,
        proposal_results,
        expected_contract_path,
    )
    passed = matched_proposal is not None
    check = {
        "item": "pre-edit-guard-state-patch-proposal",
        "status": "pass" if passed else "blocked",
        "guard_status": guard_status,
        "expected_contract_path": normalize_artifact_path(expected_contract_path),
        "matched_gate": "pre-edit",
        "matched_gate_status": guard_status if passed else None,
        "matched_proposal_path": matched_proposal.get("path") if matched_proposal else None,
        "matched_atomic_item_id": matched_proposal.get("atomic_item_id")
        if matched_proposal
        else None,
        "matched_source_gate_contract": matched_proposal.get("source_gate_contract")
        if matched_proposal
        else None,
        "matched_validation_artifact": matched_proposal.get("validation_artifact")
        if matched_proposal
        else None,
    }
    if not passed:
        check["reason"] = (
            "state patch proposal does not match selected pre-edit contract and guard status: "
            + str(normalize_artifact_path(expected_contract_path))
        )
    return check


def blocked_result(
    repo_root,
    environment,
    contract_paths,
    gate_results,
    pre_edit_guard,
    state_patch_proposal_paths,
    state_patch_proposal_results,
    blocking_reasons,
    next_allowed_action,
    notes=None,
):
    return {
        "status": "blocked",
        "repo_root": str(repo_root.resolve()),
        "environment": environment,
        "contract_paths": contract_paths,
        "gate_results": gate_results,
        "pre_edit_guard": pre_edit_guard,
        "state_patch_proposal_paths": state_patch_proposal_paths,
        "state_patch_proposal_results": state_patch_proposal_results,
        "consistency_checks": [],
        "blocking_reasons": blocking_reasons,
        "next_allowed_action": next_allowed_action,
        "notes": notes or [],
    }


def run_smoke(
    repo_root,
    version_info=None,
    contract_paths=None,
    state_patch_proposal_paths=None,
    pre_edit_handoff_note_out=None,
    require_pre_edit_guard=False,
    require_state_patch_proposal=False,
    attempted_command=None,
):
    repo_root = Path(repo_root)
    blocking_reasons = []
    gate_results = []
    pre_edit_guard_result = None
    selected_contracts = normalize_contract_paths(contract_paths)
    selected_state_patch_proposals = normalize_state_patch_proposal_paths(
        state_patch_proposal_paths
    )
    state_patch_proposal_results = []
    consistency_checks = []

    try:
        environment = load_module(
            "check_runtime_hooks_environment",
            repo_root / ENVIRONMENT_HELPER,
        )
    except Exception as exc:
        reason = "unable to load environment helper: " + str(exc)
        return blocked_result(
            repo_root,
            None,
            selected_contracts,
            gate_results,
            pre_edit_guard_result,
            selected_state_patch_proposals,
            state_patch_proposal_results,
            [reason],
            "fix-environment",
        )

    environment_result = environment.evaluate_environment(repo_root, version_info)
    if environment_result["status"] != "pass":
        return blocked_result(
            repo_root,
            environment_result,
            selected_contracts,
            gate_results,
            pre_edit_guard_result,
            selected_state_patch_proposals,
            state_patch_proposal_results,
            environment_result["blocking_reasons"],
            "fix-environment",
            ["validator smoke skipped because environment check is blocked"],
        )

    try:
        validator = load_module("validate_gate_contract", repo_root / VALIDATOR_HELPER)
    except Exception as exc:
        reason = "unable to load gate contract validator: " + str(exc)
        return blocked_result(
            repo_root,
            environment_result,
            selected_contracts,
            gate_results,
            pre_edit_guard_result,
            selected_state_patch_proposals,
            state_patch_proposal_results,
            [reason],
            "fix-environment",
        )

    try:
        pre_edit_guard = load_module("enforce_pre_edit_gate", repo_root / PRE_EDIT_GUARD_HELPER)
    except Exception as exc:
        reason = "unable to load pre-edit guard helper: " + str(exc)
        return blocked_result(
            repo_root,
            environment_result,
            selected_contracts,
            gate_results,
            pre_edit_guard_result,
            selected_state_patch_proposals,
            state_patch_proposal_results,
            [reason],
            "fix-environment",
        )

    if selected_state_patch_proposals:
        try:
            state_patch_validator = load_module(
                "validate_state_patch_proposal",
                repo_root / STATE_PATCH_PROPOSAL_HELPER,
            )
        except Exception as exc:
            reason = "unable to load state patch proposal validator: " + str(exc)
            return blocked_result(
                repo_root,
                environment_result,
                selected_contracts,
                gate_results,
                pre_edit_guard_result,
                selected_state_patch_proposals,
                state_patch_proposal_results,
                [reason],
                "fix-environment",
            )

        for relative_path in selected_state_patch_proposals:
            proposal_result = state_patch_validator.validate_proposal(
                repo_root / relative_path
            )
            proposal_summary = summarize_state_patch_proposal_result(
                proposal_result
            )
            state_patch_proposal_results.append(proposal_summary)
            if proposal_summary["status"] != "pass":
                for reason in proposal_summary["blocking_reasons"]:
                    blocking_reasons.append(relative_path + ": " + reason)
    elif require_state_patch_proposal:
        blocking_reasons.append(
            "state patch proposal required but no state patch proposal was selected"
        )

    for relative_path in selected_contracts:
        gate_result = validator.validate_contract(repo_root / relative_path)
        gate_summary = summarize_gate_result(gate_result)
        gate_results.append(gate_summary)
        if gate_summary["status"] != "pass":
            for reason in gate_summary["blocking_reasons"]:
                blocking_reasons.append(relative_path + ": " + reason)

    pre_edit_contracts = [
        selected_contracts[index]
        for index, gate_result in enumerate(gate_results)
        if gate_result["gate"] == "pre-edit"
    ]
    if pre_edit_contracts:
        guard_result = pre_edit_guard.enforce_pre_edit_gate(
            repo_root,
            pre_edit_contracts[0],
            attempted_command=attempted_command,
            handoff_note_out=pre_edit_handoff_note_out,
        )
        pre_edit_guard_result = summarize_pre_edit_guard_result(guard_result)
        if pre_edit_guard_result["status"] != "pass":
            for reason in pre_edit_guard_result["blocking_reasons"]:
                blocking_reasons.append(pre_edit_contracts[0] + ": pre-edit guard: " + reason)
    elif require_pre_edit_guard:
        blocking_reasons.append(
            "pre-edit guard required but no pre-edit contract was selected"
        )
    elif pre_edit_handoff_note_out:
        blocking_reasons.append(
            "pre-edit handoff output requested but no pre-edit contract was selected"
        )

    if require_pre_edit_guard and require_state_patch_proposal and pre_edit_guard_result:
        consistency_check = build_pre_edit_proposal_consistency_check(
            pre_edit_guard_result,
            state_patch_proposal_results,
            pre_edit_contracts[0],
        )
        consistency_checks.append(consistency_check)
        if consistency_check["status"] != "pass":
            blocking_reasons.append(consistency_check["reason"])

    status = "blocked" if blocking_reasons else "pass"
    return {
        "status": status,
        "repo_root": str(repo_root.resolve()),
        "environment": environment_result,
        "contract_paths": selected_contracts,
        "gate_results": gate_results,
        "pre_edit_guard": pre_edit_guard_result,
        "state_patch_proposal_paths": selected_state_patch_proposals,
        "state_patch_proposal_results": state_patch_proposal_results,
        "consistency_checks": consistency_checks,
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
    print("### Pre-Edit Guard")
    print()
    if result["pre_edit_guard"]:
        print("- " + str(result["pre_edit_guard"]["hook"]) + ": " + result["pre_edit_guard"]["status"])
    else:
        print("- (not selected)")
    print()
    print("### State Patch Proposal Results")
    print()
    if result["state_patch_proposal_results"]:
        for proposal_result in result["state_patch_proposal_results"]:
            print(
                "- "
                + str(proposal_result["gate"])
                + "/"
                + str(proposal_result["gate_status"])
                + ": "
                + proposal_result["status"]
            )
            if proposal_result.get("path"):
                print("  path: " + proposal_result["path"])
            if proposal_result.get("atomic_item_id"):
                print("  atomic_item_id: " + proposal_result["atomic_item_id"])
            if proposal_result.get("source_gate_contract"):
                print(
                    "  source_gate_contract: "
                    + proposal_result["source_gate_contract"]
                )
            if proposal_result.get("validation_artifact"):
                print(
                    "  validation_artifact: "
                    + proposal_result["validation_artifact"]
                )
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
    print()
    print("### Consistency Checks")
    print()
    if result["consistency_checks"]:
        for check in result["consistency_checks"]:
            print("- " + check["item"] + ": " + check["status"])
            if check.get("expected_contract_path"):
                print("  expected_contract_path: " + check["expected_contract_path"])
            if check.get("matched_proposal_path"):
                print("  matched_proposal_path: " + check["matched_proposal_path"])
            if check.get("matched_atomic_item_id"):
                print("  matched_atomic_item_id: " + check["matched_atomic_item_id"])
            if check.get("matched_source_gate_contract"):
                print(
                    "  matched_source_gate_contract: "
                    + check["matched_source_gate_contract"]
                )
            if check.get("matched_validation_artifact"):
                print(
                    "  matched_validation_artifact: "
                    + check["matched_validation_artifact"]
                )
            if check.get("reason"):
                print("  reason: " + check["reason"])
    else:
        print("- (none)")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run environment and sample contract smoke checks for runtime hook MVP."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--contract",
        action="append",
        dest="contracts",
        help="Repo-relative gate contract path to validate. May be provided multiple times. Defaults to sample fixtures.",
    )
    parser.add_argument(
        "--pre-edit-handoff-note-out",
        help="Write the blocked mounted pre-edit guard handoff note JSON to this path.",
    )
    parser.add_argument(
        "--state-patch-proposal",
        action="append",
        dest="state_patch_proposals",
        help=(
            "Repo-relative state patch proposal artifact to validate. "
            "May be provided multiple times."
        ),
    )
    parser.add_argument(
        "--require-pre-edit-guard",
        action="store_true",
        help="Block if the selected contract set does not include a pre-edit contract.",
    )
    parser.add_argument(
        "--require-state-patch-proposal",
        action="store_true",
        help="Block if no state patch proposal artifact is selected.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    attempted_command = (
        "python runtime-hooks\\scripts\\run_runtime_hooks_smoke.py"
        + " --repo-root "
        + args.repo_root
        + "".join(" --contract " + contract for contract in (args.contracts or []))
        + "".join(
            " --state-patch-proposal " + proposal
            for proposal in (args.state_patch_proposals or [])
        )
        + (
            " --pre-edit-handoff-note-out " + args.pre_edit_handoff_note_out
            if args.pre_edit_handoff_note_out
            else ""
        )
        + (" --require-pre-edit-guard" if args.require_pre_edit_guard else "")
        + (
            " --require-state-patch-proposal"
            if args.require_state_patch_proposal
            else ""
        )
        + (" --json" if args.json else "")
    )
    result = run_smoke(
        Path(args.repo_root),
        contract_paths=args.contracts,
        state_patch_proposal_paths=args.state_patch_proposals,
        pre_edit_handoff_note_out=args.pre_edit_handoff_note_out,
        require_pre_edit_guard=args.require_pre_edit_guard,
        require_state_patch_proposal=args.require_state_patch_proposal,
        attempted_command=attempted_command,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_markdown(result)

    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
