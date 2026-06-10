# RT-FU-001 Investigate Windows Sandbox Spawn Setup Refresh Failures

## Metadata

- Type: Runtime Follow-up
- ID: RT-FU-001
- Status: Draft
- Source Observation: Repeated Codex tool execution failures while running otherwise valid local commands during `SK-FU-001`.
- Suggested Location: `backlog/RT-FU-001-investigate-windows-sandbox-spawn-setup-refresh.md`
- Scope:
  - Codex Windows sandbox command execution
  - Python script invocation from `C:\personal-ai-runtime`
  - PowerShell command startup behavior
  - escalation fallback behavior
- Status Impact: No current repo workflow status change; this is a non-blocking runtime/tooling follow-up.

---

## Summary

Investigate intermittent Windows sandbox command startup failures reported as:

```text
execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })
```

During `SK-FU-001`, several commands appeared to fail before the target script produced output. The same commands succeeded when rerun with escalated execution, which suggests the issue may be in the sandbox process-spawn/setup layer rather than in the Python helper scripts themselves.

---

## Current Position

After moving runtime validation to WSL2, this issue is no longer blocking current work. The Windows sandbox spawn/setup failure should remain tracked as a dormant runtime follow-up, not as an active repo defect.

When Codex officially resolves the Windows sandbox behavior, the workspace can move back to a Windows-only setup and avoid cross-environment handoff overhead. Until then, the WSL2 workflow is also useful as a portable cross-environment validation path, which may make the project easier to open source later.

---

## Observed Pattern

The failure was observed while running local validation or smoke-check commands, especially around:

- `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`
- temporary JSON smoke-check commands that create and remove files under the Windows temp directory
- directory creation commands such as `New-Item -ItemType Directory -Force ...`

In the observed cases:

- The command did not return normal script output.
- The command did not return a Python traceback from the target script.
- Rerunning the same important command with `sandbox_permissions=require_escalated` succeeded.
- Successful reruns returned valid structured output such as `valid: true`, expected row counts, or expected helper JSON.

---

## Problem

The repeated sandbox startup error adds noise to validation logs and makes it harder to distinguish:

- real script defects,
- repository state problems,
- Windows encoding or path issues,
- temp-file or PowerShell behavior,
- and sandbox process-spawn failures.

Without a dedicated runtime follow-up, future work may keep treating each occurrence as an isolated annoyance instead of collecting enough evidence to understand whether there is a consistent trigger.

---

## Objective

Collect and classify enough evidence to decide whether this is:

- an expected sandbox limitation,
- a Windows-specific process startup issue,
- a temp directory / file creation interaction,
- a Python invocation pattern issue,
- a PowerShell command shape issue,
- or an intermittent Codex runtime bug that should be reported upstream.

---

## Non-goals

This follow-up should not:

- Treat successful escalated reruns as proof that the original script failed.
- Rewrite working skill helper scripts only because the sandbox spawn layer failed.
- Disable validation commands to avoid seeing the error.
- Broaden escalation use without evidence.
- Mix runtime investigation into `SK-FU-001` feature commits.

---

## Candidate Evidence To Collect

For each future occurrence, record:

- exact command,
- working directory,
- whether the command uses Python, PowerShell, temp files, or directory creation,
- whether the command writes under repo, temp, or another path,
- whether it fails before any script output,
- whether immediate retry in sandbox succeeds,
- whether escalated retry succeeds,
- elapsed time before failure,
- and whether nearby commands of the same shape succeed.

Suggested compact log shape:

```md
### Observation

- Command:
- Workdir:
- Failure:
- Sandbox retry:
- Escalated retry:
- Writes:
- Temp files:
- Notes:
```

---

## Observation Log

### 2026-06-01 Afternoon - SK-FU-001 Continuation

#### Observation 1 - Inventory Audit Validation

- Command: `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`
- Workdir: `C:\personal-ai-runtime`
- Failure: `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })`
- Sandbox retry: not consistently attempted; the workflow followed the escalation rule for important validation commands.
- Escalated retry: succeeded repeatedly.
- Writes: none expected.
- Temp files: none expected.
- Notes: Successful escalated reruns returned `valid: true`, `playbookRows: 16`, `skillRows: 25`, and `findings: []`, which supports treating the original failure as sandbox startup noise rather than an inventory defect.

#### Observation 2 - Directory Creation For Skill Scripts

- Command: `New-Item -ItemType Directory -Force agent-skills\<skill-name>\scripts`
- Workdir: `C:\personal-ai-runtime`
- Failure: `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })`
- Sandbox retry: not retained as successful evidence.
- Escalated retry: succeeded for script directory creation.
- Writes: creates a repo-local `scripts/` directory.
- Temp files: none.
- Notes: The command is simple PowerShell directory creation. The successful escalated rerun suggests the failure happened before normal PowerShell command completion.

#### Observation 3 - Temporary JSON Smoke Checks

- Command shape: create a JSON file under `$env:TEMP`, run a helper script against it, then remove the temp file.
- Workdir: `C:\personal-ai-runtime`
- Failure: `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })`
- Sandbox retry: not retained as successful evidence.
- Escalated retry: succeeded for the observed smoke checks.
- Writes: Windows temp directory only.
- Temp files: yes, short-lived JSON fixtures.
- Notes: Successful escalated reruns returned valid helper JSON, including `valid: true` and empty findings for the sample contracts/plans.

#### Observation 4 - Read/Search Command

- Command shape: `rg ... backlog\SK-FU-001-script-first-skill-execution-minimization.md`
- Workdir: `C:\personal-ai-runtime`
- Failure: `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })`
- Sandbox retry: not retained as successful evidence for the same exact command.
- Escalated retry: completed as a command invocation, but one rerun produced no matching output / non-zero search status.
- Writes: none.
- Temp files: none.
- Notes: This observation is weaker than the inventory-audit cases because `rg` can legitimately exit non-zero when no matches are found. Keep it as a possible spawn-layer occurrence, not as proof of an `rg` defect.

### 2026-06-02 Early Morning - SK-FU-002 / HOOK-MVP-001 Continuation

#### Observation 5 - Repeated Inventory Audit Validation

- Command: `python agent-skills\playbook-to-skill\scripts\audit_skill_inventory.py --repo-root . --json`
- Workdir: `C:\personal-ai-runtime`
- Failure: `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })`
- Sandbox retry: not retained as successful evidence for the same exact run; the workflow followed the escalation rule for important validation commands.
- Escalated retry: succeeded repeatedly.
- Writes: none expected.
- Temp files: none expected.
- Notes: Successful escalated reruns returned `valid: true`, `playbookRows: 16`, `skillRows: 25`, and `findings: []`. The command was used while validating SK-FU-002 README guidance, subagent handoff guidance, and closeout.

#### Observation 6 - Runtime Hook Gate Contract CLI Smoke

- Command: `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_pre_run_sample.json --json`
- Workdir: `C:\personal-ai-runtime`
- Failure: `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })`
- Sandbox retry: not retained as successful evidence for the same exact run; the important smoke check was rerun with escalation.
- Escalated retry: succeeded.
- Writes: none expected.
- Temp files: none.
- Notes: Successful escalated rerun returned `gate: pre-run`, `status: pass`, `blocking_reasons: []`, and `next_allowed_action: edit`, which supports treating the original failure as sandbox startup noise rather than a defect in `validate_gate_contract.py`.

---

## Current Working Hypothesis

The best current hypothesis is that `windows sandbox: spawn setup refresh` is a Codex Windows sandbox process-spawn/setup failure rather than a defect in `audit_skill_inventory.py` or the helper being run.

Confidence is moderate because escalated reruns succeeded with valid outputs, but the trigger is not yet isolated.

Current operational status: WSL2 runtime validation avoids the observed Windows sandbox failure, so this item should be revisited when Codex Windows sandbox behavior changes or when deciding whether to return the primary workspace to Windows.

---

## Acceptance Criteria

This follow-up is complete when:

- [ ] At least three future occurrences are recorded with exact commands and retry results, or the issue disappears for a meaningful period in the Windows sandbox.
- [ ] The observations distinguish script-level failures from sandbox startup failures.
- [ ] A recommendation exists for whether to keep using normal sandbox first, retry once in sandbox, escalate immediately for known affected command shapes, or report the runtime issue upstream.
- [ ] Any recommended escalation pattern remains narrow and avoids broad arbitrary command approval.
- [ ] Related skill/helper validation logs do not misclassify sandbox startup failures as helper defects.
- [ ] If Codex resolves the Windows sandbox issue, decide whether to move the primary workspace back to Windows-only or keep WSL2 as a portable open-source validation path.

---

## Review Notes

This backlog item exists because the failure repeated often enough during `SK-FU-001` to become workflow noise.

It should remain separate from skill script-first improvements unless a specific helper command is proven to be the trigger.

---

## Recommended Commit Message

```text
docs(backlog): add RT-FU-001 sandbox spawn follow-up
```
