# PB-FU-001 Add Short Skill Execution Closeout Checklist to Spec-Driven Change Verification Workflow Playbook

## Metadata

- Type: Playbook Follow-up
- ID: PB-FU-001
- Legacy ID: `SKILL-RUN-FU-01`
- Status: Draft
- Parent Playbook: `agent-playbooks/spec-driven-change-verification-workflow-playbook.md`
- Source Section: `Backlog: SKILL-RUN-FU-01 Add Short Skill Execution Closeout Checklist`
- Suggested Location: `backlog/PB-FU-001-add-short-skill-execution-closeout-checklist.md`
- Blocks Parent Completion: No
- Integration Status: Backlog captured
- Related Concepts:
  - Spec-Driven Change Verification Workflow
  - Atomic Item Execution
  - Skill Execution Closeout
  - Workflow Step Cursor
  - Commit Checkpoint
  - Mutation / Manual Mutation Verification
  - Human Decision Gate

---

## Summary

Add a compact closeout checklist for late-stage spec-driven atomic item execution.

The full Spec-Driven Change Verification Workflow Playbook is intentionally complete, but during an 80%+ closeout round the agent often needs a smaller operational loop:

1. identify the next incomplete atomic slice,
2. confirm no human decision gap blocks it,
3. finish the smallest necessary behavior or docs surface,
4. run appropriate verification,
5. update durable state,
6. commit the checkpoint,
7. and verify that remaining worktree noise is expected.

This follow-up should preserve the current governance model while making late-stage execution easier to run without reloading or reinterpreting the entire playbook.

---

## Background

A late-stage `CR-001-FU-01` execution used the extracted spec-driven skills successfully, but the operator still had to manually compress the full workflow into a practical closeout loop.

The most useful repeated actions were:

- find the next unimplemented atomic slice,
- run the smallest sufficient verification,
- update durable `workflow_step` / implementation status,
- checkpoint with a commit,
- and verify that only expected untracked artifacts remain.

The existing root playbook and skill set remain usable. This item records a refinement opportunity only.

---

## Problem

The current workflow has strong correctness governance, but closeout decisions can still require manual judgement:

- When is an atomic item ready to move from execution to final verified state?
- Which verification level is enough for docs-only, help text, implementation behavior, import graph, or CLI surface changes?
- Which small mismatches are self-fixable during closeout?
- Which mismatches require a human decision or a new spec item?
- How should mutation tooling, skipped mutation, or manual mutation review be reported without weakening verification language?
- How can the agent avoid loading too many full skill / playbook bodies during a late-stage closeout round?

Without a compact closeout checklist, each agent may recreate this compression differently.

---

## Objective

Create a short execution checklist that can be loaded before or during closeout of a spec-driven atomic item.

The checklist should:

1. keep edits scoped to the current atomic slice,
2. preserve human decision gates,
3. preserve mutation / manual mutation truthfulness,
4. require durable state and index updates,
5. require a commit checkpoint when appropriate,
6. distinguish self-fixable drift from behavior or contract decisions,
7. and keep the closeout loop short enough to use without reading the full root playbook.

---

## Non-goals

This follow-up should not:

- Change the current spec-driven workflow sequence.
- Change skill trigger rules.
- Change the extraction map.
- Change child-skill contracts while merely recording this item.
- Promote backlog work into accepted behavior without a follow-up implementation decision.
- Weaken mutation testing or manual mutation disclosure.
- Skip human decision gates for behavior policy, CLI contract, or artifact contract changes.
- Replace the full playbook for high-risk or ambiguous work.

---

## Proposed Playbook Addition

Add a compact section to the parent playbook, root skill, or orchestrator-state-machine skill after a dedicated refinement decision:

```md
### Short Skill Execution Closeout Checklist

Use this checklist near the end of a spec-driven atomic item, after the active slice is implemented or almost complete.

1. Read durable state and identify the next incomplete atomic slice.
2. Confirm no human decision gap blocks the slice.
3. Keep edits to the smallest behavior/docs surface needed by that slice.
4. Run focused verification, then the module's minimum full verification when applicable.
5. Run smoke checks for any touched entrypoint, import path, CLI help, or docs surface.
6. State whether mutation tooling or scoped manual mutation was run, skipped, or not applicable, and why.
7. Update `workflow_step`, atomic item status, parent/root indexes, and handoff notes in durable artifacts.
8. Run whitespace/diff checks, commit the checkpoint, and verify remaining worktree noise is expected.
```

---

## Closeout Decision Table

| Situation | Default Handling |
|---|---|
| Stale docs or help text that merely reflects already-accepted behavior | Self-fix inside the current atomic item, then read back and smoke-check the surface. |
| `workflow_step` or implementation-status cursor drift | Self-fix if the underlying state is clear from durable artifacts; otherwise mark a gap. |
| Small CLI help / docs mismatch | Self-fix if it does not introduce a new option, contract, or behavior policy. |
| New CLI option, artifact contract, schema field, or behavior policy | Requires spec / human decision unless already accepted by the current atomic item. |
| Behavior change outside the current atomic slice | Do not implement; record as follow-up or decision gap. |
| Mutation tooling unavailable | Say it was not run, explain why, and perform scoped manual mutation only when meaningful for the touched behavior. |
| Unexpected untracked artifacts | Classify as expected run output, unrelated user work, or blocker before finalizing. |

---

## Verification Level Table

| Surface Touched | Minimum Closeout Verification |
|---|---|
| Markdown docs only | Readback of changed section, `rg` / link check where useful, and `git diff --check`. |
| README / index routing | Verify both forward and backward references with `rg` or `Select-String`. |
| CLI help or command docs | Run the relevant help / smoke command if available and safe. |
| Import path or entrypoint | Run an import / startup smoke check plus focused tests. |
| Implementation behavior | Run focused tests and the module's minimum full verification. |
| Test behavior | Run the changed tests and at least one negative/manual mutation review where applicable. |
| Spec or workflow state | Verify `workflow_step`, implementation status, parent/root indexes, and handoff notes. |

---

## Integration Map

| Existing Workflow Area | Integration Purpose |
|---|---|
| Atomic Item Execution | Provide a short closeout loop after implementation work is mostly complete. |
| Orchestrator State Machine | Define when `workflow_step` and implementation status may advance. |
| Completion Check | Ensure state sync, verification reporting, and worktree noise classification happen before final reply. |
| Mutation Testing / Manual Mutation Review | Preserve truthful reporting when mutation tooling is skipped, unavailable, or not applicable. |
| Skill Extraction Map | Decide whether the checklist belongs in root `spec-driven-change-verification`, `orchestrator-state-machine`, or a small playbook section. |

---

## Suggested Implementation Steps

1. Decide whether the checklist should first land as a parent playbook section or as a root/orchestrator skill refinement.
2. Add the short checklist without changing the existing full workflow sequence.
3. Add the closeout and verification decision tables if they help avoid repeated judgement calls.
4. If a skill is updated, keep the skill version shorter than this backlog file.
5. Update `agent-playbooks/README.md` and `agent-skills/README.md` status text if the follow-up moves from backlog to implemented refinement.
6. Verify references to `PB-FU-001` and legacy `SKILL-RUN-FU-01` are traceable.

---

## Acceptance Criteria

This follow-up is complete when:

- [ ] The parent playbook or relevant skill includes a short closeout checklist.
- [ ] The checklist is short enough to load before a closeout round without reading the full playbook.
- [ ] It preserves current governance: no hidden promotion of backlog items, no skipped human decision gates, and no silent weakening of mutation/test effectiveness language.
- [ ] It distinguishes self-fixable drift from behavior-policy, schema, CLI, or artifact-contract decisions.
- [ ] It names minimum verification expectations for docs, indexes, help text, import/entrypoint changes, implementation behavior, tests, and workflow state.
- [ ] It requires durable updates to `workflow_step`, implementation status, parent/root indexes, and handoff notes where applicable.
- [ ] It requires `git diff --check` or equivalent whitespace/diff hygiene before checkpointing.
- [ ] README / index status is updated if the refinement is implemented.

---

## Devil's Advocate Review

### DA-PB-FU-001-001 - Risk: The checklist becomes a shortcut around the full workflow

Severity: Medium

If the checklist is used too early, an agent may skip spec drill-down, design review, or test planning.

Mitigation:

- State that it applies only near the end of an active atomic item.
- Keep ambiguous, high-risk, or policy-changing work on the full workflow.

### DA-PB-FU-001-002 - Risk: Self-fixable drift is interpreted too broadly

Severity: Medium

Agents may treat behavior or contract changes as small cleanup.

Mitigation:

- Include a decision table that separates docs/status drift from behavior, CLI, schema, or artifact contract changes.
- Require human/spec decision for changes outside the current accepted slice.

### DA-PB-FU-001-003 - Risk: Mutation language weakens during closeout

Severity: Medium

Late-stage work may be summarized as "verified" without stating whether mutation tooling or manual mutation review happened.

Mitigation:

- Require explicit reporting: run, skipped, not applicable, or unavailable.
- Require a reason and scoped manual mutation review when meaningful.

### DA-PB-FU-001-004 - Risk: The checklist duplicates root and child skills

Severity: Low

A checklist added in multiple places can drift.

Mitigation:

- Keep the parent playbook as the canonical explanation.
- Keep any skill version short and execution-oriented.
- Re-check playbook / skill alignment when implementing this follow-up.

---

## Traceability

Parent -> follow-up:

- Parent Playbook: `agent-playbooks/spec-driven-change-verification-workflow-playbook.md`
- Parent README Index: `agent-playbooks/README.md`
- Source Section Legacy ID: `SKILL-RUN-FU-01`

Follow-up -> parent:

- This backlog file consolidates the previous inline `SKILL-RUN-FU-01` follow-up from the parent playbook.
- It does not block use of the current playbook or extracted skills.
- It should remain draft until a dedicated refinement updates the parent playbook and/or skills.

---

## Recommended Commit Message

```text
docs(backlog): add PB-FU-001 closeout checklist follow-up
```
