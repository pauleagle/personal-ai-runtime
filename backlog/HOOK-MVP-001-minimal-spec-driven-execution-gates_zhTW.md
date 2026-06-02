# HOOK-MVP-001 Minimal Spec-Driven Execution Gates

Version: v0.1-draft  
Status: MVP / Experimental  
Category: Runtime Governance  
Related:
- spec-driven-change-verification-workflow-playbook
- preflight-protocol
- devils-advocate-review
- devils-advocate-drill-down
- playbook-to-skill

---

# 1. 目的

本文件定義 Personal AI Runtime 的最小可行 Runtime Hook / Execution Gate 機制。

目標不是增加更多 prompt 規則，而是：

- 降低 agent 對長 context 的依賴
- 降低 instruction dilution
- 降低 scope drift
- 降低 hallucinated execution
- 將「請遵守規則」轉變為「執行前檢查」

本文件屬於 Runtime Governance Layer，而非一般 Playbook。

---

# 2. 核心理念

傳統 Prompt Engineering：

```text
請 AI 記得遵守規則
```

Hook / Gate 模式：

```text
如果不符合規則，就不允許進入下一步
```

核心差異：

| 模式 | 本質 |
|---|---|
| Prompt | 建議 |
| Playbook | 操作方法 |
| Skill | 可重用執行單元 |
| Hook / Gate | Runtime Enforcement |

---

# 3. MVP Gate 設計

MVP 階段先定義三種核心 Gate：

1. Pre-Run Gate
2. Pre-Edit Gate
3. Post-Run Gate

---

# 4. Pre-Run Gate

## 4.1 目的

防止 agent 尚未理解 spec / scope 就直接開始實作。

---

## 4.2 必須檢查項目

- 是否存在明確 atomic item
- 是否存在對應 spec / backlog / issue
- 是否列出 scope
- 是否列出 forbidden scope
- 是否列出 acceptance criteria
- 是否列出預期 artifact

---

## 4.3 Gate Failure 行為

若未通過：

- 禁止 implementation
- 禁止 file modification
- 只能要求補充資訊
- 只能回報缺失項目

---

# 5. Pre-Edit Gate

## 5.1 目的

防止 subagent 超出 scope 修改檔案。

此 Gate 為 MVP 階段最重要 Gate。

---

## 5.2 必須檢查項目

- 修改檔案是否位於 allowed paths
- 是否碰觸 forbidden paths
- 是否屬於 atomic item scope
- 是否出現大規模 unrelated rewrite
- 是否修改未宣告 dependency

---

## 5.3 Gate Failure 行為

若未通過：

- 阻止 edit
- 回報 scope violation
- 回到 orchestrator 重新決策
- 禁止自動擴大 scope

---

# 6. Post-Run Gate

## 6.1 目的

防止 agent 完成修改後未驗證即標記完成。

---

## 6.2 必須檢查項目

- 是否列出 changed files
- 是否列出驗證方式
- 是否執行 tests / lint / validation
- 是否對照 acceptance criteria
- 是否列出 remaining risks
- 是否產生 follow-up items

---

## 6.3 Gate Failure 行為

若未通過：

- 禁止標記完成
- 要求補充 verification
- 要求補充 risk analysis

---

# 7. 與 Subagent Architecture 的關係

Hook / Gate 的目的之一：

是讓 Subagent 可以安全化。

沒有 Hook 時：

```text
Subagent = 高風險自由執行
```

加入 Hook 後：

```text
Orchestrator
  ↓
Runtime Gates
  ↓
Scoped Subagent Execution
```

---

# 8. 未來可能演化方向

未來可能擴充：

- Usage Gate
- Cost Gate
- Context Budget Gate
- Spec Completeness Gate
- Diff Size Gate
- Risk Tier Gate
- Human Approval Gate
- Parallel Agent Conflict Gate

---

# 9. 與 Workflow 的關係

目前 workflow：

```text
PLAN
→ SPEC
→ IMPLEMENT
→ VERIFY
→ REVIEW
```

未來可能演化為：

```text
PLAN
→ Pre-Run Gate
→ IMPLEMENT
→ Pre-Edit Gate
→ VERIFY
→ Post-Run Gate
→ REVIEW
```

---

# 10. 核心原則

## 10.1 減少 Context Dependency

原則：

```text
能 Runtime Enforcement 的規則，
不要只依賴 Context 記憶。
```

---

## 10.2 降低自由度

目標不是讓 Agent 更自由。

而是：

```text
讓 Agent 在可控邊界內穩定執行。
```

---

## 10.3 將治理前移

避免：

```text
事後 review 才發現問題
```

改為：

```text
在執行前阻止問題
```

---

# 11. 當前狀態

目前屬於：

- 概念驗證（PoC）
- Runtime Governance MVP
- Hook Architecture 初始版

尚未綁定特定 runtime framework。

---

# 12. MVP Gate Contract

本節把前三個 Gate 轉成可驗收的最小契約。

MVP 不要求真正攔截所有工具呼叫；第一版只要求能以 deterministic input 判斷 gate 是否 `pass` / `blocked`，並輸出可讀的 blocking reasons。

---

## 12.1 共用輸入欄位

三種 Gate 應共用下列概念欄位：

| 欄位 | 說明 |
|---|---|
| `atomic_item_id` | 目前要執行的 atomic item；若沒有，Pre-Run Gate 應 blocked。 |
| `spec_ref` | 對應 spec、backlog、issue 或 durable artifact。 |
| `allowed_scope` | 允許讀寫或執行的路徑、artifact、workflow step。 |
| `forbidden_scope` | 禁止碰觸的路徑、artifact、行為或決策。 |
| `acceptance_criteria` | 完成此 item 前必須滿足的驗收條件。 |
| `expected_artifacts` | 預期會產生或修改的 artifact。 |
| `validation_plan` | 預期驗證方式，例如 tests、lint、validator、manual review 或 skip reason。 |

---

## 12.2 共用輸出欄位

三種 Gate 應回傳下列最小輸出：

| 欄位 | 說明 |
|---|---|
| `gate` | `pre-run`、`pre-edit` 或 `post-run`。 |
| `status` | `pass` 或 `blocked`。 |
| `blocking_reasons` | 若 blocked，列出具體缺失。 |
| `checked_items` | 已檢查項目與結果。 |
| `next_allowed_action` | 下一步允許做什麼，例如 ask-user、edit、validate、handoff。 |
| `notes` | 非阻塞風險或補充資訊。 |

---

## 12.3 Gate 判斷規則

### Pre-Run Gate

`pass` 條件：

- `atomic_item_id` 存在。
- `spec_ref` 存在。
- `allowed_scope` 與 `forbidden_scope` 已列出。
- `acceptance_criteria` 不為空。
- `expected_artifacts` 已列出，或明確說明此 item 不產生 artifact。

`blocked` 時只允許：

- 回報缺失欄位。
- 要求使用者或 orchestrator 補齊資訊。
- 建立或更新 backlog/spec drill-down。

### Pre-Edit Gate

`pass` 條件：

- 每個 proposed changed file 都落在 `allowed_scope`。
- 沒有 proposed changed file 落在 `forbidden_scope`。
- proposed change 能對應到 `atomic_item_id` 或 declared dependency。
- 沒有大規模 unrelated rewrite。

`blocked` 時只允許：

- 回報 scope violation。
- 回到 orchestrator 重切 scope。
- 要求人類批准擴大 scope。

### Post-Run Gate

`pass` 條件：

- changed files 已列出。
- validation actions 已列出。
- acceptance criteria 已逐項對照。
- remaining risks 已列出，或明確標示 none known。
- follow-up items 已列出，或明確標示 none。
- 若 workflow 使用 commit checkpoint，必須已完成 commit 或明確 blocked reason。

`blocked` 時只允許：

- 補跑驗證。
- 補齊 acceptance / risk / follow-up 對照。
- 回報未完成項，不得宣稱 item complete。

---

# 13. MVP Acceptance Criteria

- [x] Pre-Run Gate 有明確 input contract、pass / blocked 條件與 blocked 行為。
- [x] Pre-Edit Gate 有明確 input contract、pass / blocked 條件與 blocked 行為。
- [x] Post-Run Gate 有明確 input contract、pass / blocked 條件與 blocked 行為。
- [x] 三種 Gate 使用一致的 `pass` / `blocked` 狀態語義。
- [x] Gate output 能列出 `blocking_reasons` 與 `next_allowed_action`。
- [x] MVP 不要求綁定特定 runtime framework。
- [x] MVP 不要求攔截所有工具呼叫；可以先用 explicit gate check artifact 或 helper 實作。
- [x] Gate failure 不得被 prompt judgement 覆蓋；必須由補齊資訊、人類決策或 scope 調整解除。
- [x] 若後續進入 implementation，第一個 atomic item 應只做 deterministic contract validator，不做 full runtime hook framework。

---

# 14. Devil's Advocate Drill-down

本節在進入 `HOOK-MVP-001-A1` 前，先把主要 objections 轉成處置狀態與 spec patch requirements。

注意：本文件先前尚未有獨立 Devil's Advocate Review 輸出，因此本節同時列出 review objections 並完成 drill-down。後續若流程要求更嚴格，可先另產生完整 DA Review，再進入本節格式。

## 14.1 Objection Resolution Table

| ID | Severity | Objection | Status | Resolution |
|---|---|---|---|---|
| `DA-HOOK-MVP-001-001` | Low | `pass` / `blocked` 可能太粗，無法表達非阻塞 warning。 | resolved | MVP 維持 binary gate；非阻塞資訊放入 `notes`，不得影響 `status` 語義。 |
| `DA-HOOK-MVP-001-002` | Low | Pre-Run Gate 可能讓探索型分析工作也被要求提供完整 atomic item。 | resolved | Gate 只套用於宣告要進入 implementation / edit / completion 的工作；純分析、drill-down、handoff 可使用 `next_allowed_action: ask-user` 或 `handoff`。 |
| `DA-HOOK-MVP-001-003` | Medium | `allowed_scope` / `forbidden_scope` 若語義不清，validator 會變成形式檢查。 | resolved | `HOOK-MVP-001-A1` 先支援 repo-relative paths、artifact IDs、workflow step names 的簡單清單；不做複雜 policy language。 |
| `DA-HOOK-MVP-001-004` | Medium | Pre-Edit Gate 要求 proposed changed files，但實作前未必能完全預知最後 diff。 | resolved | Pre-Edit Gate 檢查「宣告的 proposed changed files」；實際 diff drift 交給 Post-Run Gate 檢查。若實作中發現需新增路徑，必須回到 gate 擴 scope。 |
| `DA-HOOK-MVP-001-005` | Medium | Post-Run Gate 要求 commit checkpoint 可能和使用者要求「不要 commit」衝突。 | resolved | commit 僅在 workflow 使用 commit checkpoint 時是 pass 條件；否則必須提供 explicit skip reason。 |
| `DA-HOOK-MVP-001-006` | High | deterministic helper 可能被誤認為真正 runtime hook enforcement，造成 false confidence。 | resolved | A1 明確命名為 contract validator，不宣稱攔截 tool calls；文件保留「MVP 不要求攔截所有工具呼叫」。 |
| `DA-HOOK-MVP-001-007` | High | Gate failure 如果可以被 agent prose override，Runtime Governance 會退化回 prompt 建議。 | resolved | Gate failure 只能由補齊資訊、人類決策或 scope 調整解除；LLM judgement 不得直接覆蓋 blocked status。 |

## 14.2 Spec Patch Requirements

- A1 validator 的 input contract 必須包含 gate type 與 gate-specific payload，而不是只檢查文件中是否有文字描述。
- A1 先採用簡單資料結構：清單、字串、布林與 object；不引入 policy DSL。
- Pre-Edit Gate 必須支援 `proposed_changed_files`，並檢查它們是否落在 `allowed_scope` 且避開 `forbidden_scope`。
- Post-Run Gate 必須允許 `commit_checkpoint` 搭配 `skip_reason`，以支援使用者明確要求不 commit 的情境。
- Output 必須保留 binary `status`，warning / caveat 只能放在 `notes`。
- 文件與 helper 不得宣稱已提供完整 runtime interception。

## 14.3 Compatibility / Replacement Decision Table

| Topic | Decision |
|---|---|
| 現有 Codex tool execution | 不替換、不攔截；A1 只做 explicit gate contract validation。 |
| 現有 spec-driven workflow playbook | 不在 A1 修改；先以 backlog contract validator 驗證概念。 |
| 現有人工 usage gate | 不替換；commit + 流量確認仍由互動流程執行。 |
| 未來 runtime hook framework | deferred；需要 A1 驗證有用後再設計。 |
| Human governance decisions | 不自動化；blocked status 需要補資訊、人類決策或 scope 調整才能解除。 |

## 14.4 Deferred Items

- 真正攔截 tool calls / edit calls 的 runtime hook framework。
- 支援複雜 path glob、rule priority、policy inheritance 或 multi-repo scope policy。
- 與 Codex CLI / wrapper / daemon 的整合方式。
- 將 gate result 寫入 durable orchestrator state 的 schema。

## 14.5 Gate Status

`pass` for `HOOK-MVP-001-A1`，條件是 A1 僅實作 deterministic contract validator，不實作 full runtime hook framework。

---

# 15. 下一個 Atomic Slice 建議

建議下一個 implementation item：

```text
HOOK-MVP-001-A1: deterministic gate contract validator
```

Scope:

- 新增一個最小 helper，讀取 local JSON gate contract artifact。
- 驗證 `pre-run`、`pre-edit`、`post-run` 的 required fields。
- 驗證 Pre-Edit Gate 的 `proposed_changed_files` 是否落在 `allowed_scope` 並避開 `forbidden_scope`。
- 允許 Post-Run Gate 的 `commit_checkpoint` 使用 explicit `skip_reason`。
- 輸出 structured JSON：`status`、`blocking_reasons`、`checked_items`、`next_allowed_action`。
- 新增 focused unit tests。

Non-goals:

- 不攔截 Codex tool calls。
- 不建立 daemon、agent wrapper 或 runtime server。
- 不修改現有 spec-driven workflow playbook。
- 不自動 commit、revert、擴大 scope 或作出 human-governance decision。
- 不宣稱已完成 runtime interception。

Validation:

- focused unit tests。
- CLI smoke check。
- `git diff --check`。

## 15.1 Implementation Log

Status: completed.

Implemented:

- Added `runtime-hooks/scripts/validate_gate_contract.py`.
- Added focused tests under `tests/runtime_hooks/test_validate_gate_contract.py`.
- Added smoke fixture `tests/fixtures/gate_contract_pre_run_sample.json`.
- Implemented `pre-run`, `pre-edit`, and `post-run` validation.
- Implemented binary `status`: `pass` or `blocked`.
- Implemented `blocking_reasons`, `checked_items`, `next_allowed_action`, and `notes` output fields.
- Implemented simple repo-relative exact / prefix / `/**` scope matching for `proposed_changed_files`.
- Supported `commit_checkpoint.status` values `committed`, `skipped`, and `blocked`; `skipped` / `blocked` require explicit `skip_reason` or `blocked_reason`.

Out of scope by design:

- No tool-call interception.
- No daemon, wrapper, or runtime server.
- No policy DSL.
- No automatic commit, revert, scope expansion, or human-governance decision.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_pre_run_sample.json --json`.
- Ran `git diff --check`.

Direct smoke result:

- Focused tests reported 6 tests OK.
- Full test suite reported 59 tests OK.
- CLI smoke returned `gate: pre-run`, `status: pass`, and `next_allowed_action: edit`.
- The first sandboxed CLI smoke hit the known `windows sandbox: spawn setup refresh`; the same command succeeded when rerun with escalated execution.

---

## 15.2 Atomic Slice: `HOOK-MVP-001-A2`

```text
HOOK-MVP-001-A2: validator usage guidance and representative fixtures
```

Scope:

- Add a minimal `runtime-hooks/README.md` explaining what the MVP validator does and does not do.
- Add representative `pre-edit` and `post-run` sample gate contract fixtures.
- Keep A2 limited to documentation and fixtures; do not implement runtime interception, wrappers, daemons, policy DSL, or automatic governance decisions.

Acceptance criteria:

- `runtime-hooks/README.md` documents the validator command, expected output fields, fixtures, and MVP boundaries.
- Sample fixtures exist for `pre-run`, `pre-edit`, and `post-run`.
- Each sample fixture passes `validate_gate_contract.py --json`.
- Focused unit tests still pass.
- `git diff --check` passes.

Non-goals:

- No tool-call interception.
- No daemon, runtime wrapper, or Codex CLI integration.
- No policy DSL.
- No automatic commit, revert, scope expansion, or approval decision.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/README.md` with validator purpose, command usage, output fields, fixtures, and MVP boundaries.
- Added `tests/fixtures/gate_contract_pre_edit_sample.json`.
- Added `tests/fixtures/gate_contract_post_run_sample.json`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_pre_run_sample.json --json`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_pre_edit_sample.json --json`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py tests\fixtures\gate_contract_post_run_sample.json --json`.
- Ran `git diff --check`.

Direct smoke result:

- Focused tests reported 6 tests OK.
- All three fixture smoke checks returned `status: pass`.
- The sandboxed fixture smoke checks hit the known `windows sandbox: spawn setup refresh`; escalated reruns succeeded.

---

## 15.3 Atomic Slice: `HOOK-MVP-001-A3`

```text
HOOK-MVP-001-A3: document Python baseline for portable hook usage
```

Scope:

- Document the runtime hook Python version baseline for cloning this repo onto another machine.
- Keep the baseline as a minimum supported version rather than an exact pin.
- Do not add dependency management, virtual environment setup, packaging metadata, or CI.

Acceptance criteria:

- `runtime-hooks/README.md` states the required Python version.
- The documentation distinguishes required minimum version from current local validated baseline.
- The documentation states whether third-party packages are needed.
- Focused validator tests still pass.
- `git diff --check` passes.

Decision:

- Required baseline: Python 3.10 or newer.
- Current local validated baseline: Python 3.10.11.
- No `.python-version` is added for A3 because the hook MVP only needs a minimum version, and an exact pin could over-constrain company-machine setup.

Implementation log:

Status: completed.

Implemented:

- Added Python baseline guidance to `runtime-hooks/README.md`.

Validation actions:

- Ran `python --version`.
- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `git diff --check`.

Direct result:

- Local Python reported `Python 3.10.11`.
- Focused tests reported 6 tests OK.

---

## 15.4 Atomic Slice: `HOOK-MVP-001-A4`

```text
HOOK-MVP-001-A4: runtime hook environment smoke check
```

Scope:

- Add a minimal environment check helper for validating a fresh clone on another machine.
- Check the Python minimum version and required runtime hook MVP files.
- Keep the helper dependency-free and compatible with older Python syntax where practical, so an outdated interpreter can return a clear blocked result.
- Document the environment smoke command in `runtime-hooks/README.md`.

Acceptance criteria:

- The helper reports `pass` when Python meets the baseline and required hook files exist.
- The helper reports `blocked` when Python is older than 3.10.
- The helper reports `blocked` when required hook MVP files are missing.
- The helper emits structured JSON with `status`, `blocking_reasons`, `checked_items`, and `next_allowed_action`.
- Focused runtime hook tests pass.
- `git diff --check` passes.

Non-goals:

- No dependency manager, virtual environment setup, packaging metadata, or CI.
- No runtime interception.
- No automatic installation or machine configuration.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/scripts/check_runtime_hooks_environment.py`.
- Added `tests/runtime_hooks/test_check_runtime_hooks_environment.py`.
- Added the environment smoke command to `runtime-hooks/README.md`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_check_runtime_hooks_environment`.
- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\check_runtime_hooks_environment.py --repo-root . --json`.
- Ran `git diff --check`.

Direct result:

- Environment smoke returned `status: pass`.
- Focused runtime hook tests reported OK.
- Full test suite reported 63 tests OK.

---

## 15.5 Atomic Slice: `HOOK-MVP-001-A5`

```text
HOOK-MVP-001-A5: one-command runtime hook MVP smoke
```

Scope:

- Add a single smoke helper that runs the environment check and all representative sample gate contracts.
- Keep the smoke helper dependency-free.
- Ensure the smoke helper blocks on environment failure before loading the gate validator.
- Document the full MVP smoke command in `runtime-hooks/README.md`.

Acceptance criteria:

- The smoke helper returns `pass` when the environment check passes and all sample gate contracts pass.
- The smoke helper returns `blocked` when the environment check is blocked.
- The smoke helper returns structured JSON with `status`, `environment`, `gate_results`, `blocking_reasons`, and `next_allowed_action`.
- The environment helper includes the smoke helper itself in required file checks.
- Focused runtime hook tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No dependency manager, virtual environment setup, packaging metadata, CI, or automatic installation.
- No runtime interception.
- No policy DSL.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Added `tests/runtime_hooks/test_run_runtime_hooks_smoke.py`.
- Added the full MVP smoke command to `runtime-hooks/README.md`.
- Updated `check_runtime_hooks_environment.py` required file checks to include the smoke helper.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest tests.runtime_hooks.test_check_runtime_hooks_environment`.
- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --json`.
- Ran `git diff --check`.

Direct result:

- Full MVP smoke returned `status: pass`.
- Focused runtime hook tests reported OK.
- Full test suite reported 67 tests OK.
- The sandboxed full MVP smoke check hit the known `windows sandbox: spawn setup refresh`; escalated rerun succeeded.

---

## 15.6 Atomic Slice: `HOOK-MVP-001-A6`

```text
HOOK-MVP-001-A6: explicit contract support for runtime hook MVP smoke
```

Scope:

- Allow the full MVP smoke helper to validate explicit gate contract paths.
- Preserve the existing default behavior of validating the representative sample fixtures when no explicit contract is provided.
- Include selected contract paths in structured JSON output.
- Document the explicit contract command in `runtime-hooks/README.md`.

Acceptance criteria:

- `run_runtime_hooks_smoke.py` accepts repeated `--contract` arguments.
- No `--contract` still validates the three representative sample fixtures.
- Explicit valid contracts return `pass`.
- Explicit invalid contracts return `blocked` and aggregate blocking reasons.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No contract discovery or glob expansion.
- No policy DSL.
- No runtime interception.
- No automatic creation or repair of contract artifacts.

Implementation log:

Status: completed.

Implemented:

- Added repeated `--contract` support to `run_runtime_hooks_smoke.py`.
- Added `contract_paths` to smoke helper JSON output.
- Added focused tests for default samples, explicit valid contracts, explicit invalid contracts, and CLI explicit contract usage.
- Added explicit contract command guidance to `runtime-hooks/README.md`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract tests\fixtures\gate_contract_pre_run_sample.json --json`.
- Ran `git diff --check`.

Direct result:

- Explicit contract smoke returned `status: pass`.
- Focused runtime hook smoke tests reported OK.
- Full test suite reported 70 tests OK.
- The sandboxed explicit contract smoke check hit the known `windows sandbox: spawn setup refresh`; escalated rerun succeeded.

---

## 15.7 Atomic Slice: `HOOK-MVP-001-A7`

```text
HOOK-MVP-001-A7: fresh clone checklist and smoke output assertions
```

Scope:

- Add a concise fresh clone checklist for runtime hook MVP validation.
- Document smoke command exit code semantics.
- Add focused tests for CLI markdown output and invalid-contract non-zero exit behavior.
- Keep helper behavior unchanged.

Acceptance criteria:

- `runtime-hooks/README.md` includes a fresh clone checklist.
- README documents that smoke commands return `0` on `pass` and non-zero on `blocked`.
- CLI markdown output includes status and next allowed action.
- CLI invalid contract smoke returns non-zero and structured blocked JSON.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No dependency manager, packaging metadata, CI, or install automation.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Fresh Clone Checklist` guidance to `runtime-hooks/README.md`.
- Added CLI markdown output and invalid-contract exit code tests to `tests/runtime_hooks/test_run_runtime_hooks_smoke.py`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported 9 tests OK.
- Full test suite reported 72 tests OK.

---

## 15.8 Atomic Slice: `HOOK-MVP-001-A8`

```text
HOOK-MVP-001-A8: smoke troubleshooting guidance and environment CLI assertions
```

Scope:

- Add troubleshooting guidance for blocked runtime hook smoke checks.
- Add focused tests for environment helper CLI markdown output and non-zero blocked exit behavior.
- Keep helper behavior unchanged.

Acceptance criteria:

- `runtime-hooks/README.md` explains how to inspect `blocking_reasons`, `checked_items`, and `next_allowed_action`.
- README lists common first fixes for Python version, missing files, and blocked gate contracts.
- Environment helper CLI markdown output includes status and next allowed action.
- Environment helper CLI returns non-zero structured JSON when required files are missing.
- Focused environment helper tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No dependency manager, packaging metadata, CI, or install automation.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Troubleshooting Blocked Smoke Checks` guidance to `runtime-hooks/README.md`.
- Added environment helper CLI markdown and blocked exit tests.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_check_runtime_hooks_environment`.
- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Focused environment helper tests reported 6 tests OK.
- Full test suite reported 74 tests OK.

---

## 15.9 Atomic Slice: `HOOK-MVP-001-A9`

```text
HOOK-MVP-001-A9: smoke result interpretation guidance
```

Scope:

- Add concise README guidance for interpreting passing and blocked smoke results.
- Keep this slice documentation-only.

Acceptance criteria:

- README states the expected key fields for a passing full MVP smoke result.
- README states that blocked smoke results must stop implementation.
- README instructs rerunning the same smoke command after fixing blocking reasons.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Interpreting Smoke Results` guidance to `runtime-hooks/README.md`.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.10 Atomic Slice: `HOOK-MVP-001-A10`

```text
HOOK-MVP-001-A10: MVP usage and non-usage boundaries
```

Scope:

- Add README guidance for when to use the runtime hook MVP helpers.
- Add README guidance for when not to use them.
- Keep this slice documentation-only.

Acceptance criteria:

- README states that helpers are for deterministic checks of explicit gate contract artifacts.
- README lists fresh clone and active atomic item validation as valid uses.
- README states that helpers are not tool-call interception, runtime wrappers, daemons, policy DSLs, or human-approval substitutes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `When To Use This MVP` and `When Not To Use This MVP` sections to `runtime-hooks/README.md`.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.11 Atomic Slice: `HOOK-MVP-001-A11`

```text
HOOK-MVP-001-A11: MVP current status and deferred next options
```

Scope:

- Summarize the current HOOK-MVP-001 implementation status after A1 through A10.
- Separate completed MVP helper capabilities from deferred runtime governance work.
- Keep this slice documentation-only and suitable as a low-traffic handoff point.

Current MVP status:

- Gate contract spec exists for `pre-run`, `pre-edit`, and `post-run`.
- Deterministic gate contract validator exists at `runtime-hooks/scripts/validate_gate_contract.py`.
- Runtime hook environment check exists at `runtime-hooks/scripts/check_runtime_hooks_environment.py`.
- Full MVP smoke helper exists at `runtime-hooks/scripts/run_runtime_hooks_smoke.py`.
- Representative fixtures exist for all three gate types.
- Runtime hook README documents Python baseline, fresh clone checklist, smoke checks, troubleshooting, result interpretation, and MVP usage boundaries.
- Focused runtime hook tests and full test suite have passed across the A1-A8 implementation/test slices.
- A9-A11 are documentation-only closeout / handoff slices.

What this MVP can currently do:

- Validate explicit local JSON gate contracts.
- Validate proposed `pre-edit` changed files against simple allowed / forbidden scope entries.
- Validate `post-run` commit checkpoint shape including explicit skip / blocked reasons.
- Check whether a fresh clone has the required hook MVP files and Python 3.10+.
- Run one command to validate the runtime hook environment and sample or explicit gate contracts.

What remains deferred:

- Real tool-call or edit-call interception.
- Agent wrapper, daemon, runtime server, or Codex CLI integration.
- Policy DSL, rule inheritance, rule priority, or glob-rich scope language.
- Durable orchestrator-state persistence for gate results.
- Automatic installation, dependency management, or CI.
- Any automatic human-governance decision, approval, scope expansion, commit, revert, or completion claim.

Candidate next slices:

- `HOOK-MVP-001-A12`: add a concise contract schema reference section to `runtime-hooks/README.md`.
- `HOOK-MVP-001-A13`: add a small generated example for an active atomic item contract artifact.
- `HOOK-MVP-001-A14`: design, but do not implement, the first possible integration boundary with orchestrator state.
- `RT-FU-001`: continue collecting exact `windows sandbox: spawn setup refresh` observations separately from HOOK-MVP feature work.

Acceptance criteria:

- Backlog contains a clear current status summary.
- Backlog separates completed MVP helper capabilities from deferred work.
- Backlog lists safe next slices without starting them.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No README changes.
- No new tests.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added the current MVP status, deferred work, and candidate next slices to this backlog.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.12 Atomic Slice: `HOOK-MVP-001-A12`

```text
HOOK-MVP-001-A12: README contract schema reference
```

Scope:

- Add a concise gate contract schema reference to `runtime-hooks/README.md`.
- Cover common required fields and gate-specific fields.
- Document the intentionally simple scope matching semantics.
- Keep this slice documentation-only.

Acceptance criteria:

- README lists the common required gate contract fields.
- README lists the additional `pre-edit` field.
- README lists the additional `post-run` fields and `commit_checkpoint` expectations.
- README states that scope matching is simple and not a policy DSL.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Gate Contract Schema Reference` to `runtime-hooks/README.md`.

Validation actions:

- Ran `git diff --check`.

Direct result:

- `git diff --check` passed.

---

## 15.13 Atomic Slice: `HOOK-MVP-001-A13`

```text
HOOK-MVP-001-A13: active atomic item contract example
```

Scope:

- Add a small durable pre-run contract example for one active atomic item.
- Document how to validate that example before starting the corresponding edit.
- Add a focused test proving the example remains valid.
- Keep this slice limited to example artifact, README guidance, tests, and backlog state.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json` exists.
- The example maps `HOOK-MVP-001-A13` to spec reference, allowed scope, forbidden scope, acceptance criteria, expected artifacts, and validation plan.
- `runtime-hooks/README.md` points to the active atomic item example and its validator command.
- Focused validator tests pass.
- The example validates with `validate_gate_contract.py --json`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No runtime interception.
- No policy DSL.
- No automatic contract generation.
- No orchestrator-state persistence.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json`.
- Added `Active Atomic Item Example` guidance to `runtime-hooks/README.md`.
- Added a focused test that validates the durable active-item example.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused validator tests reported OK.
- Active atomic item example returned `status: pass`.
- `git diff --check` passed.

---

## 15.14 Atomic Slice: `HOOK-MVP-001-A14`

```text
HOOK-MVP-001-A14: orchestrator state integration boundary
```

Scope:

- Design the first possible boundary between runtime hook gate results and durable orchestrator state.
- Document what an orchestrator may copy from gate validation output into a separate state patch.
- Document what remains outside the runtime hook MVP.
- Keep this slice design-only: no state persistence, no validator behavior change, no interception.

Acceptance criteria:

- `runtime-hooks/README.md` describes the orchestrator state integration boundary.
- The boundary identifies minimal fields an orchestrator could persist from a gate result.
- The boundary states that blocked gates must preserve concrete blocking reasons in orchestrator state.
- The boundary states that workflow cursor advancement, human decisions, scope expansion, and commit checkpoints remain orchestrator responsibilities.
- Existing orchestrator state sample validation still passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No orchestrator state schema implementation.
- No state mutation or persistence helper.
- No automatic active-item discovery.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Orchestrator State Integration Boundary` guidance to `runtime-hooks/README.md`.
- Documented candidate persisted fields: `atomic_item_id`, `gate`, `gate_status`, `next_allowed_action`, `blocking_reasons`, `validation_artifact`, and `checkpoint_status`.
- Documented that blocked gate results should remain blocked in orchestrator state until fixed or decided by a human.

Validation actions:

- Ran `python agent-skills\orchestrator-state-machine\scripts\validate_orchestrator_state.py tests\fixtures\orchestrator_state_sample.json --json`.
- Ran `git diff --check`.

Direct result:

- Orchestrator state sample validation returned `valid: true`.
- `git diff --check` passed.

---

## 15.15 Atomic Slice: `HOOK-MVP-001-A15`

```text
HOOK-MVP-001-A15: orchestrator state gate result example
```

Scope:

- Add a durable orchestrator state fixture showing how a blocked gate result can appear in the `blocked` queue.
- Add a focused test proving the fixture is accepted by the existing orchestrator state validator.
- Point README readers to the example state artifact.
- Keep this slice example-only: no state persistence helper, no schema enforcement change, no interception.

Acceptance criteria:

- `tests/fixtures/orchestrator_state_gate_result_sample.json` exists.
- The fixture includes a blocked queue item with `atomic_item_id`, `gate`, `gate_status`, `next_allowed_action`, `blocking_reasons`, `validation_artifact`, and `checkpoint_status`.
- The existing orchestrator state validator accepts the fixture.
- `runtime-hooks/README.md` points to the fixture as an example boundary contract.
- Focused orchestrator state tests pass.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No durable state mutation or persistence helper.
- No stricter orchestrator state schema.
- No automatic active-item discovery.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `tests/fixtures/orchestrator_state_gate_result_sample.json`.
- Added a focused orchestrator state validator test for the gate-result fixture.
- Added README guidance that the fixture is an example boundary contract.

Validation actions:

- Ran `python -m unittest tests.agent_skills.test_validate_orchestrator_state`.
- Ran `python -m unittest discover -s tests`.
- Ran `python agent-skills\orchestrator-state-machine\scripts\validate_orchestrator_state.py tests\fixtures\orchestrator_state_gate_result_sample.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused orchestrator state tests reported OK.
- Full test suite reported OK.
- Gate-result state fixture validation returned `valid: true`.
- `git diff --check` passed.

---

## 15.16 Atomic Slice: `HOOK-MVP-001-A16`

```text
HOOK-MVP-001-A16: active item explicit smoke coverage
```

Scope:

- Prove the full runtime hook smoke helper can validate the active atomic item contract example via explicit `--contract`.
- Document the explicit full-smoke command for the active item example.
- Keep this slice to smoke coverage and docs; do not change helper behavior.

Acceptance criteria:

- `tests/runtime_hooks/test_run_runtime_hooks_smoke.py` covers `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json` through explicit contract smoke.
- `runtime-hooks/README.md` documents the full smoke helper command for the active item example.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- The explicit active item smoke CLI returns `status: pass`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added focused smoke coverage for the A13 active item contract example.
- Added README guidance for running the active item example through `run_runtime_hooks_smoke.py --contract`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported OK.
- Full test suite reported OK.
- Explicit active item smoke returned `status: pass`.
- `git diff --check` passed.

---

## 15.17 Atomic Slice: `HOOK-MVP-001-A17`

```text
HOOK-MVP-001-A17: active pre-edit contract example
```

Scope:

- Add a durable `pre-edit` contract example for one active atomic item.
- Show proposed changed files that remain inside allowed scope and outside forbidden scope.
- Document how to validate the active `pre-edit` example.
- Add focused validator coverage for the durable example.
- Keep this slice example-only: no helper behavior change, no contract generation, no interception.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json` exists.
- The example maps `HOOK-MVP-001-A17` to spec reference, allowed scope, forbidden scope, proposed changed files, acceptance criteria, expected artifacts, and validation plan.
- The example's proposed changed files validate against the declared allowed and forbidden scope.
- `runtime-hooks/README.md` points to the active `pre-edit` example and its validator command.
- Focused validator tests pass.
- Full test suite passes.
- The example validates with `validate_gate_contract.py --json`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery or generation.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json`.
- Added focused validator coverage for the active `pre-edit` example.
- Added README guidance for validating the active `pre-edit` example.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a17_pre_edit_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused validator tests reported OK.
- Full test suite reported OK.
- Active `pre-edit` example returned `status: pass`.
- `git diff --check` passed.

---

## 15.18 Atomic Slice: `HOOK-MVP-001-A18`

```text
HOOK-MVP-001-A18: active post-run contract example
```

Scope:

- Add a durable `post-run` contract example for one active atomic item.
- Show changed files, validation actions, acceptance results, remaining risks, follow-up items, and commit checkpoint state.
- Document how to validate the active `post-run` example.
- Add focused validator coverage for the durable example.
- Keep this slice example-only: no helper behavior change, no contract generation, no interception.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a18_post_run_contract.json` exists.
- The example maps `HOOK-MVP-001-A18` to spec reference, allowed scope, forbidden scope, changed files, validation actions, acceptance results, remaining risks, follow-up items, and commit checkpoint state.
- The example validates the `post-run` commit checkpoint shape with an explicit skip reason.
- `runtime-hooks/README.md` points to the active `post-run` example and its validator command.
- Focused validator tests pass.
- Full test suite passes.
- The example validates with `validate_gate_contract.py --json`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery or generation.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/examples/hook_mvp_001_a18_post_run_contract.json`.
- Added focused validator coverage for the active `post-run` example.
- Added README guidance for validating the active `post-run` example.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a18_post_run_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused validator tests reported OK.
- Full test suite reported OK.
- Active `post-run` example returned `status: pass`.
- `git diff --check` passed.

---

## 15.19 Atomic Slice: `HOOK-MVP-001-A19`

```text
HOOK-MVP-001-A19: active examples combined smoke coverage
```

Scope:

- Prove the full runtime hook smoke helper can validate the active `pre-run`, `pre-edit`, and `post-run` examples together through explicit repeated `--contract`.
- Document the combined active example smoke command.
- Keep this slice to smoke coverage and docs; do not change helper behavior.

Acceptance criteria:

- `tests/runtime_hooks/test_run_runtime_hooks_smoke.py` covers the active `pre-run`, `pre-edit`, and `post-run` examples together.
- The combined smoke result preserves contract order and reports all three gate types.
- `runtime-hooks/README.md` documents the combined active example smoke command.
- Focused runtime hook smoke tests pass.
- Full test suite passes.
- The combined active example smoke CLI returns `status: pass`.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added focused smoke coverage for the active `pre-run`, `pre-edit`, and `post-run` examples together.
- Added README guidance for running all active examples through repeated `run_runtime_hooks_smoke.py --contract`.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_run_runtime_hooks_smoke`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\run_runtime_hooks_smoke.py --repo-root . --contract runtime-hooks\examples\hook_mvp_001_a13_pre_run_contract.json --contract runtime-hooks\examples\hook_mvp_001_a17_pre_edit_contract.json --contract runtime-hooks\examples\hook_mvp_001_a18_post_run_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused runtime hook smoke tests reported OK.
- Full test suite reported OK.
- Combined active example smoke returned `status: pass`.
- `git diff --check` passed.

---

## 15.20 Atomic Slice: `HOOK-MVP-001-A20`

```text
HOOK-MVP-001-A20: active example coverage closeout
```

Scope:

- Summarize the current active example coverage after A13 through A19.
- Update safe candidate next slices so future continuation does not restart completed example work.
- Keep this slice documentation-only and suitable as a commit checkpoint.

Current active example coverage:

- `pre-run`: `runtime-hooks/examples/hook_mvp_001_a13_pre_run_contract.json`.
- `pre-edit`: `runtime-hooks/examples/hook_mvp_001_a17_pre_edit_contract.json`.
- `post-run`: `runtime-hooks/examples/hook_mvp_001_a18_post_run_contract.json`.
- Combined active smoke: repeated `--contract` validation covers all three examples in order.

What this closes:

- Active examples now cover the three MVP gate types.
- Focused validator tests keep all three durable examples valid.
- Focused smoke tests keep the combined active example workflow valid.
- README contains copyable commands for single-example and combined-example validation.

What remains deferred:

- Runtime interception of tool calls or edit calls.
- Automatic active-item discovery.
- Contract generation or repair.
- Durable orchestrator-state mutation or persistence helpers.
- Policy DSL, complex glob semantics, rule priority, or inheritance.
- Any automatic human-governance decision, scope expansion, commit, revert, or completion claim.

Candidate next slices:

- `HOOK-MVP-001-A21`: design a minimal handoff note format for blocked gate results without writing state.
- `HOOK-MVP-001-A22`: add a blocked active `pre-edit` example to demonstrate scope violation reporting.
- `HOOK-MVP-001-A23`: add README guidance for choosing between sample fixtures, active examples, and future project-specific contracts.
- `RT-FU-001`: continue collecting exact `windows sandbox: spawn setup refresh` observations separately from HOOK-MVP feature work.

Acceptance criteria:

- Backlog summarizes active example coverage after A13 through A19.
- Backlog separates closed coverage from deferred runtime governance work.
- Backlog lists safe next slices without starting them.
- `runtime-hooks/README.md` summarizes active example coverage.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added current active example coverage summary to `runtime-hooks/README.md`.
- Added A20 closeout, deferred work, and candidate next slices to this backlog.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.21 Atomic Slice: `HOOK-MVP-001-A21`

```text
HOOK-MVP-001-A21: blocked gate handoff note format
```

Scope:

- Design a minimal handoff note format for blocked gate results.
- Document when to use the note and what fields it should carry.
- Clarify that a handoff note cannot override a blocked gate, mark completion, or expand scope.
- Keep this slice documentation-only: no state writing, no helper behavior change, no interception.

Acceptance criteria:

- `runtime-hooks/README.md` documents a blocked gate handoff note format.
- The format includes `atomic_item_id`, `gate`, `gate_status`, `blocking_reasons`, `next_allowed_action`, `attempted_command`, `scope_decision_needed`, and `resume_from`.
- README states that the handoff note is not a gate override.
- README states that durable orchestrator state patching remains outside this MVP.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No durable state mutation or persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Blocked Gate Handoff Note` guidance to `runtime-hooks/README.md`.
- Documented minimal handoff fields and boundary rules.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.22 Atomic Slice: `HOOK-MVP-001-A22`

```text
HOOK-MVP-001-A22: blocked active pre-edit example
```

Scope:

- Add a durable blocked `pre-edit` contract example for one active atomic item.
- Demonstrate proposed changed file reporting when a path is outside `allowed_scope`.
- Add focused validator coverage for the blocked example.
- Document how to interpret the blocked example.
- Keep this slice example-only: no helper behavior change, no contract generation, no interception.

Acceptance criteria:

- `runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json` exists.
- The example returns `status: blocked`.
- The example includes concrete `blocking_reasons` entries for scope violations.
- The example returns `next_allowed_action: handoff`.
- `runtime-hooks/README.md` points to the blocked example and explains expected interpretation.
- Focused validator tests pass.
- Full test suite passes.
- The blocked example CLI returns non-zero structured JSON.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No contract discovery or generation.
- No automatic active-item selection.
- No state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `runtime-hooks/examples/hook_mvp_001_a22_blocked_pre_edit_contract.json`.
- Added focused validator coverage for the blocked active `pre-edit` example.
- Added README guidance for interpreting the blocked example.

Validation actions:

- Ran `python -m unittest tests.runtime_hooks.test_validate_gate_contract`.
- Ran `python -m unittest discover -s tests`.
- Ran `python runtime-hooks\scripts\validate_gate_contract.py runtime-hooks\examples\hook_mvp_001_a22_blocked_pre_edit_contract.json --json`.
- Ran `git diff --check`.

Direct result:

- Focused validator tests reported OK.
- Full test suite reported OK.
- Blocked active `pre-edit` example returned `status: blocked`, `next_allowed_action: handoff`, and concrete allowed / forbidden scope reasons.
- `git diff --check` passed.

---

## 15.23 Atomic Slice: `HOOK-MVP-001-A23`

```text
HOOK-MVP-001-A23: contract type selection guidance
```

Scope:

- Add README guidance for choosing between sample fixtures, active examples, and future project-specific contracts.
- Clarify that sample fixtures are stable smoke inputs and should not be edited to fit project items.
- Keep this slice documentation-only.

Acceptance criteria:

- `runtime-hooks/README.md` describes when to use sample fixtures.
- `runtime-hooks/README.md` describes when to use active examples.
- `runtime-hooks/README.md` describes when to create project-specific contracts.
- README warns not to mutate sample fixtures merely to fit an active project item.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No contract discovery or generation.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Choosing Contract Types` guidance to `runtime-hooks/README.md`.
- Documented the distinction between stable sample fixtures, active examples, and project-specific contracts.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.24 Atomic Slice: `HOOK-MVP-001-A24`

```text
HOOK-MVP-001-A24: runtime hook MVP closeout status
```

Scope:

- Add a concise MVP closeout status to README and backlog.
- Mark the current MVP as ready to pause as a deterministic validation layer.
- Separate the next phase decisions from the completed MVP work.
- Keep this slice documentation-only.

Current MVP closeout status:

- Gate contracts are defined for `pre-run`, `pre-edit`, and `post-run`.
- Deterministic validator checks required fields, simple scope boundaries, blocked reasons, and post-run commit checkpoint shape.
- Environment and full smoke helpers support fresh-clone checks and repeated explicit contracts.
- Active passing examples cover all three gate types.
- Blocked active `pre-edit` example demonstrates scope violation reporting.
- Blocked gate handoff note format exists.
- Orchestrator integration remains documented boundary only; no persistence helper is implemented.

Next decision gate:

- Option A: pause HOOK-MVP-001 here and switch to RT-FU-001 observations or another backlog item.
- Option B: design contract generation, without implementing runtime interception.
- Option C: design orchestrator-state persistence, without implementing tool-call interception.
- Option D: begin a separate spec for real runtime interception / wrapper / daemon.

Acceptance criteria:

- `runtime-hooks/README.md` includes MVP closeout status.
- Backlog includes current MVP closeout status.
- Backlog separates next phase decisions from completed MVP work.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No new fixtures.
- No contract generation.
- No orchestrator-state persistence helper.
- No runtime interception.

Implementation log:

Status: completed.

Implemented:

- Added `Closeout Status` guidance to `runtime-hooks/README.md`.
- Added A24 closeout status and next decision gate to this backlog.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

## 15.25 Atomic Slice: `HOOK-MVP-001-A25`

```text
HOOK-MVP-001-A25: runtime hook mounting decision spec
```

Scope:

- Add a mounting decision spec before any runtime hook attachment work.
- Decide the candidate mounting layers and enforcement modes.
- Recommend a conservative first mounting path.
- Keep this slice documentation-only: no wrapper, daemon, CLI integration, state persistence, or interception.

Mounting decision points:

- Mount layer: manual command, PowerShell wrapper, Codex CLI wrapper, orchestrator step, or future daemon.
- First gate to mount: `pre-edit` for hard-block candidate, `post-run` for completion gate, `pre-run` for planning discipline.
- Enforcement mode: advisory check, soft block with handoff, or hard block.
- Blocked output: console JSON, handoff note, orchestrator-state patch proposal, or persisted gate result artifact.
- Human decision boundary: blocked gates require missing information, scope changes, or human decision before continuing.

Recommended first mounting path:

- Start with an orchestrator step or manual command using explicit project-specific contracts.
- Mount `pre-edit` first as a hard-block gate because it can prevent scoped file edits before they happen.
- Emit blocked results as handoff notes first.
- Defer durable state writes until a state patch schema is separately decided.
- Treat Codex CLI wrapper, daemon, and broad tool-call interception as separate specs.

Acceptance criteria:

- `runtime-hooks/README.md` documents the mounting decision spec.
- README states the candidate mount layers.
- README states recommended first gate and enforcement mode.
- README states blocked output options and human decision boundary.
- README preserves the boundary that this MVP validates explicit artifacts only.
- Full test suite passes.
- `git diff --check` passes.

Non-goals:

- No helper behavior changes.
- No new tests.
- No wrapper.
- No daemon.
- No Codex CLI integration.
- No durable state persistence helper.
- No broad tool-call interception.

Implementation log:

Status: completed.

Implemented:

- Added `Mounting Decision Spec` guidance to `runtime-hooks/README.md`.
- Added A25 mounting decision spec and recommended first mounting path to this backlog.

Validation actions:

- Ran `python -m unittest discover -s tests`.
- Ran `git diff --check`.

Direct result:

- Full test suite reported OK.
- `git diff --check` passed.

---

# 16. 長期方向

此方向可能逐步演化為：

- Agent Runtime Governance
- Spec-Driven Execution Runtime
- Skill Dispatch Control Layer
- Multi-Agent Coordination Runtime
- Verification-Centric AI Engineering Workflow

---
