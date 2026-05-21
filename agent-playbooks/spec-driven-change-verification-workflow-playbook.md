# Spec-Driven Change Verification Workflow Playbook

## 目的

本文件整理一套以 **Spec / Plan 為起點、以 Change / Diff 為觸發、以 Mutation Testing 驗證測試有效性、並透過 Human-in-the-Loop 控制規格演進** 的完整工作流。

它不是單純的測試流程，而是一套結合：

- Preflight Protocol
- Spec Drill-down / Clarification Loop
- Devil's Advocate Review
- Specification-Driven Development, SDD
- Test-Driven Development, TDD
- Change / Diff Analysis
- Meta JIT Tests
- Mutation Testing
- Human-in-the-Decision-Loop Governance
- Spec / Test Evolution

的 **AI-assisted verification workflow**。

核心目標是：

> 不只是讓測試存在，而是讓測試能證明自己有效；不只是讓程式符合測試，而是讓程式、測試與規格一起演進。

---

## 構思來源與演化脈絡

### 1. 從 SDD / TDD 開始

最初的構想來自：

```text
spec -> test case -> implement
```

也就是先定義系統應該如何正確運作，再根據 spec 產生 test case，最後才進入 implementation。

這裡的關鍵不是單純追求 coverage，而是：

- 自製 test case 必須能 trace 回 spec
- test case 要驗證規則、邊界、例外與 invariant
- 不應該為了 coverage 而寫沒有語意來源的 test

因此，本 workflow 的第一原則是：

> Spec defines correctness.

---

### 2. 加入 Mutation Testing：驗證測試是否有效

傳統 coverage 只能說明「程式碼有被跑到」，不能證明「如果程式壞掉，測試抓得到」。

Mutation Testing 的角色是刻意破壞程式：

```text
M(code) -> code'
```

然後重新執行測試：

```text
mutation killed   -> test is effective
mutation survived -> validation gap exists
```

因此，本 workflow 將測試品質從：

```text
有沒有測到？
```

提升成：

```text
測試是否真的能抓到錯？
```

---

### 3. 受到 Meta JIT Tests 啟發：根據 Diff 動態產生測試

Meta JIT Tests 的啟發在於：

> 測試不一定只能是事先寫好的靜態集合，也可以根據 PR / commit diff 即時產生。

因此 workflow 加入：

- diff analysis
- impact analysis
- intent-aware analysis
- JIT test generation

讓每次變更都觸發針對性的驗證。

基本想法是：

```text
PR / commit diff
  -> infer intent
  -> identify impacted components
  -> generate / select focused tests
  -> run tests
```

這讓測試成本不必每次都全量爆炸，也能更聚焦在本次變更真正可能影響的區域。

---

### 4. 比 Meta JIT Tests 多一步：用測試結果反推是否需要更新 Spec

本 workflow 不只是在 diff 後產生 JIT tests。

更重要的是：

> 當 JIT test 或 mutation result 發現 gap 時，要回頭檢查 spec 是否不足、過時或需要演進。

也就是從：

```text
change -> test -> pass/fail
```

進一步變成：

```text
change -> test -> mutation -> gap analysis -> spec/test evolution
```

可能的判斷包括：

- test 不足，需要補測試
- spec 不清楚，需要補規格
- code 改變了行為，需要判斷是否接受
- change 與現有 spec 衝突，需要 reject 或重寫 spec

這使整套流程變成 self-evolving verification system。

---

### 5. 加入 Human-in-the-Loop：人負責治理，不負責手動驗證

Human-in-the-Loop 的定位不是要人手動跑測試或逐條驗證結果。

人的角色是：

- 定義 correctness
- 解決 ambiguity
- 決定 spec 是否要演進
- 在 accept / update spec / reject change 之間做決策

換句話說：

> Humans do not validate the system — they govern it.

---

### 6. 受到個人 AI 助理 initial 流程啟發：加入 Spec Drill-down

在 plan / spec 還沒有明確之前，不應該急著進入實作。

受到個人 AI 助理 initial flow、以及多輪澄清式 agent / skill 設計啟發，本 workflow 在前段加入：

```text
Spec Drill-down / Clarification Loop
```

它的任務是透過多輪問題，把模糊需求逐步變成可實作、可驗證、可測試的 spec。

它要補齊：

- input / output
- business rules
- constraints
- invariants
- error conditions
- edge cases
- non-goals
- acceptance criteria

---

### 7. 受到 Devil's Advocate 概念啟發：加入反方審查

Devil's Advocate 原本可理解為在決策或方案討論中，刻意由一個角色從反方、風險、刁鑽角度檢視方案。

在本 workflow 中，Devil's Advocate Review 放在 plan / spec 定稿之前，任務不是補充需求，而是挑戰方案：

- 有沒有隱含假設？
- 有沒有過度設計？
- 有沒有漏掉 edge cases？
- 有沒有違反既有架構原則？
- 有沒有更簡單的做法？
- 有沒有維護成本、測試成本、遷移風險？
- 有沒有 spec 與 implementation 可能脫鉤的地方？

這讓 workflow 在進入 implementation 前先經過一次風險導向的反方檢查。

---

## 核心原則

### 1. Spec defines correctness

Spec 是 correctness 的來源。

Code、test、JIT test、mutation evaluation 都必須回到 spec 判斷。

---

### 2. Test cases must trace back to spec

禁止沒有語意來源的測試。

每個 test case 應該能回答：

```text
這個 test 對應哪一條 spec？
它驗證的是 rule、boundary、invariant、error condition，還是 regression scenario？
```

---

### 3. Changes trigger verification

PR / commit diff 是驗證觸發點。

每次變更都應該觸發：

- impact analysis
- intent analysis
- risk identification
- focused test selection / generation

---

### 4. Tests must be validated, not trusted

Generated tests 不能一產生就被視為可信。

它們需要經過：

- baseline execution
- mutation validation
- stability observation

才可能成為長期資產。

---

### 5. Mutation testing validates test effectiveness

Mutation score 比單純 coverage 更接近測試有效性。

Coverage 告訴你 code 有被跑到。

Mutation testing 告訴你：

```text
如果 code 被破壞，test 是否會失敗？
```

---

### 6. Humans govern correctness

人不應該卡在低階驗證工作。

人應該負責：

- 決定 spec
- 決定 ambiguous behavior
- 決定 breaking change 是否接受
- 決定是否更新 spec

---

## 完整工作流

```text
0. Preflight Protocol
   ↓
1. Spec Drill-down / Clarification Loop
   ↓
2. Draft Plan / Draft Spec
   ↓
3. Devil's Advocate Review
   ↓
4. Revised Spec
   ↓
4.5 Workflow Decomposition / Atomic Work Items
   ↓
5. Spec-Based Test Design
   ↓
6. Implementation
   ↓
7. Change Detection / Diff Analysis
   ↓
8. Intent & Impact Analysis
   ↓
9. Risk & Gap Identification
   ↓
10. Meta JIT Test Generation
   ↓
11. Test Execution
   ↓
12. Mutation Testing
   ↓
13. Test Effectiveness Evaluation
   ↓
14. Decision Proposal
   ↓
15. Human Decision
   ↓
16. Spec / Test Evolution
```

---

## 工作流詳細說明

### Step 0 — Preflight Protocol

在開始複雜任務前，先列出：

- 任務理解
- 假設
- 不確定處
- 兩種以上可能解讀
- 風險
- 下一步

目的：

- 避免 agent 直接跳到實作
- 讓隱含假設先浮出來
- 決定是否需要進入 drill-down

---

### Step 1 — Spec Drill-down / Clarification Loop

針對不明確的 plan / requirement 進行多輪追問。

輸入：

- 初始需求
- preflight 結果
- 已知 constraints

輸出：

- clarified requirements
- open questions
- acceptance criteria
- non-goals
- testable spec candidates

範例問題：

```text
這個功能的主要 input / output 是什麼？
哪些行為是一定不能改變的？
哪些 edge cases 必須保留？
這次變更是 bug fix、feature、refactor，還是 behavior change？
如果既有行為與新需求衝突，以哪一邊為準？
```

---

### Step 2 — Draft Plan / Draft Spec

根據 drill-down 結果產生初版 plan / spec。

Draft spec 應包含：

- context
- goal
- scope
- non-goals
- inputs
- outputs
- business rules
- invariants
- error conditions
- acceptance criteria
- testing implications

#### Spec 文件落點與 README 分工

一般原則：

> README 是入口，Spec 是 correctness contract。

README 適合放：

- 這個專案 / module 是什麼
- 為什麼存在
- 快速開始或基本使用方式
- 高階流程與架構概念
- 預期目錄結構
- roadmap / version direction
- 指向正式 spec 的連結

正式 spec 建議另外放，例如：

```text
<project>/
├─ README.md
├─ SPEC.md
└─ docs/
   ├─ v0.1.0-spec.md
   ├─ config-schema.md
   └─ export-format.md
```

建議規則：

- 小型或早期 module 可先使用 `SPEC.md` 作為目前目標版本的正式規格。
- 當同時維護多個版本、資料格式或外部 contract 時，再拆成 `docs/vX.Y.Z-spec.md`、`docs/config-schema.md`、`docs/export-format.md` 等文件。
- README 可以摘要 spec，但不應成為完整 correctness 來源。
- 若 README 與 SPEC 對行為描述衝突，規格判斷應以 SPEC 為準，並回頭修正 README 摘要。
- 當 README 開始包含 input/output contract、acceptance criteria、error conditions 或 test matrix 時，通常代表應該把這些內容提升到正式 spec。

#### 建議 Spec 格式

建議用以下格式產生 `SPEC.md` 或版本化 spec：

```md
# <Project / Module Name> Spec

## 規格狀態

- 目標版本：
- 規格狀態：Draft / Revised / Accepted / Deprecated
- 最後更新：

## 脈絡

說明這個功能或 module 為什麼存在、使用者是誰、它解決什麼問題。

## 目標

定義這個版本要達成的行為與主要 correctness question。

## 範圍

列出本版本必須包含的功能、資料流、整合點或可觀察行為。

## 非目標

列出本版本明確不處理的項目，避免 scope creep。

## 輸入

定義 config、CLI args、API payload、檔案格式、使用者操作或外部依賴。

## 輸出

定義檔案、資料夾、API response、事件、log、metadata 或狀態變化。

## 業務規則

列出必須成立的 domain rules、流程規則、資料轉換規則與相容性要求。

## 不變條件

列出實作前後都必須保持成立的 invariant。

## 錯誤條件

列出 invalid input、外部失敗、衝突狀態、權限問題與 expected failure behavior。

## Acceptance Criteria

用 AC-01、AC-02 等條列可驗證的完成條件。

## Testing Implications

列出 test matrix，讓每個 test case trace back 到 spec reference。

## Open Questions

列出仍需 human decision 的 ambiguity、未定義行為或未來版本問題。
```

---

### Step 3 — Devil's Advocate Review

對 draft plan / spec 做反方審查。

檢查面向：

- 隱含假設
- 過度設計
- 欠缺 edge cases
- 與既有架構衝突
- 測試成本過高
- migration risk
- backwards compatibility
- maintainability
- security / privacy / data risk
- 是否能用更簡單方法完成

輸出：

- objections
- risk list
- suggested simplifications
- required clarifications
- revision proposal

---

### Step 4 — Revised Spec

根據 Devil's Advocate Review 的結果修正 spec。

此階段的目標是讓 spec 達到：

```text
可實作
可測試
可追蹤
可審查
```

---

### Step 4.5 — Workflow Decomposition / Atomic Work Items

在 revised spec 之後、test design 與 implementation 之前，先把主工作流拆成可討論的 workflow slices。

此階段分兩層：

```text
main workflow
  -> workflow slices
  -> selected workflow
  -> atomic implementation items
```

目前規則：

- 先由 agent 根據 spec 拆出主工作流與候選 workflow slices。
- 暫時由 human 指定要優先拆解的 selected workflow。
- Agent 只針對 human 指定的 selected workflow 拆成 atomic items。
- Atomic items 應小到可以被單獨實作、單獨測試、單獨 review。
- 每個 atomic item 必須 trace back 到 spec reference、business rule、acceptance criteria、error condition 或 risk item。
- Atomic items 不應直接等同於檔案清單；它們應描述可驗證的行為或資料契約。
- 若拆解時發現 spec 不足，應回到 Step 1 / Step 2 補 drill-down 或更新 draft spec。

輸入：

- revised spec
- main workflow description
- acceptance criteria
- known constraints
- human 指定的 selected workflow

輸出：

- main workflow map
- candidate workflow slices
- selected workflow
- atomic implementation items
- deferred items
- spec gaps / open questions

建議 atomic item 格式：

```text
Item ID:
Workflow:
Spec Reference:
Purpose:
Input / Preconditions:
Expected Output:
Validation / Test Hook:
Dependencies:
Deferred / Non-goal Notes:
```

判斷標準：

- 如果 item 無法用一句話說明完成條件，通常還太大。
- 如果 item 沒有 validation / test hook，通常還不是可驗證 atomic item。
- 如果 item 同時跨多個 workflow slice，應拆小或標記 dependency。
- 如果 item 需要 human 決定 correctness，應先列為 open question，不應直接進 implementation。

---

### Step 5 — Spec-Based Test Design

根據 spec 設計 test cases。

測試類型：

- happy path
- boundary cases
- invariant checks
- error conditions
- regression cases
- compatibility cases

每個 test 必須 trace back to spec。

建議格式：

```text
Test ID:
Spec Reference:
Purpose:
Input:
Expected Output:
Failure Meaning:
```

---

### Step 6 — Implementation

根據 spec 與 tests 進行實作。

原則：

- code must satisfy spec
- 不加入未要求功能
- 保留既有風格與架構
- refactor 不應混入 behavior change，除非 spec 明確允許

---

### Step 7 — Change Detection / Diff Analysis

在 PR / commit 階段觸發 change verification。

輸入：

- git diff
- PR description
- changed files
- related specs
- related tests

輸出：

- changed components
- changed behavior candidates
- affected modules
- impacted tests

---

### Step 8 — Intent & Impact Analysis

推斷這次變更的 intent：

- bug fix
- feature
- refactor
- performance change
- dependency change
- test-only change
- documentation change

同時找出 impact set：

```text
Impact Set = affected components + related specs + related tests
```

---

### Step 9 — Risk & Gap Identification

根據 intent + impact 找出風險：

- regression points
- behavior drift
- missing spec cases
- insufficient tests
- untested branches
- unclear compatibility

輸出：

- risk model
- gap list
- suggested JIT test targets

---

### Step 10 — Meta JIT Test Generation

根據 diff / intent / impact 動態產生或挑選測試。

測試集合：

```text
Tests =
  Selected Existing Tests
  + Generated JIT Tests
```

JIT tests 必須：

- 可重現
- 可輸出成 test case
- 可 trace 回 spec 或 risk item
- 不可直接視為 trusted tests

---

### Step 11 — Test Execution

執行：

- baseline tests
- selected impacted tests
- generated JIT tests

輸出：

- pass / fail
- failing cases
- coverage signal
- suspicious gaps

---

### Step 12 — Mutation Testing

對 impact scope 做 mutation testing。

原則：

- mutation 必須限縮在 impacted code
- 避免全量 mutation 成本過高
- mutation result 用來驗證測試有效性，不只是製造更多 CI 負擔

---

### Step 13 — Test Effectiveness Evaluation

根據 mutation 結果評估測試：

```text
mutation killed   -> test effective
mutation survived -> validation gap
```

若 mutation survived，必須判斷：

- 是否缺少 test？
- 是否 spec 沒定義？
- 是否 implementation 與 spec 不一致？
- 是否 mutation 本身不合理？

---

### Step 14 — Decision Proposal

Agent / workflow 不直接替人做最終決策，而是提出結構化選項。

建議格式：

```text
Intent:
- 本次變更想達成什麼

Spec Impact:
- compatible / violation / unclear

Verification Result:
- tests passed / failed
- mutation killed / survived
- remaining gaps

Options:
1. Accept change
2. Update spec
3. Reject change
4. Refine tests
5. Split change into smaller PRs

Recommended Option:
- reason
- risk
```

---

### Step 15 — Human Decision

Human 必須在關鍵分歧點做決策：

- 接受變更
- 更新 spec
- 拒絕變更
- 要求補測試
- 要求拆分 PR
- 要求重新定義 scope

Human 不需要手動驗證所有細節，但必須治理 correctness。

---

### Step 16 — Spec / Test Evolution

根據決策更新長期資產：

- update spec
- promote useful tests
- discard weak generated tests
- refine JIT generation rules
- update playbook / skill if workflow 本身有新發現

---

## Test Promotion Lifecycle

Generated tests 不應直接成為 trusted tests。

建議信任層級：

```text
L0: Generated Test
    - 由 JIT 或 AI 產生
    - 尚未證明有效

L1: Candidate Test
    - baseline pass
    - 可重現
    - 有 spec / risk trace

L2: Trusted Test
    - 能 kill mutation
    - 證明可抓到至少一類錯誤

L3: Persisted Test
    - 長期穩定
    - 可納入 regression suite
    - 成為專案長期資產
```

Promotion rule：

```text
If test detects meaningful mutation -> promote
Else -> discard, refine, or keep ephemeral
```

---

## Governance Rules

### Spec Governance

- Spec 是 correctness 的來源
- 行為變更必須更新 spec
- 不允許 implicit spec drift
- 若 code 與 spec 衝突，必須由 human 決定哪一方修正

---

### Test Governance

- 測試必須 trace back to spec 或 risk item
- Generated tests 不可直接視為 trusted
- mutation-validated tests 才能升級信任等級
- coverage 不可作為主要 KPI

---

### Mutation Governance

- mutation scope 必須根據 impact set 限縮
- mutation survived 必須進入 gap analysis
- 不應為了追 mutation score 而盲目擴大測試

---

### JIT Test Governance

- JIT tests 必須可重現
- 必須保留生成依據：diff、intent、impact、spec reference
- JIT tests 預設是 ephemeral，不是 permanent

---

### Human-in-the-Loop Governance

Human 負責：

- 定義 correctness
- 解決 ambiguity
- 決定 behavior change 是否接受
- 決定 spec 是否演進

Agent 負責：

- 分析
- 產生候選測試
- 驗證測試有效性
- 整理 decision proposal

---

## Metrics

建議使用：

- mutation score
- survived mutations
- spec coverage
- impacted scope size
- generated JIT tests count
- promoted tests count
- flaky generated tests count
- spec update count
- human decision count

避免只看：

- line coverage
- branch coverage
- test count
- CI pass rate

Coverage 可以當輔助訊號，但不能作為品質保證。

---

## Anti-Patterns

### 1. Coverage-driven testing

只為了讓 coverage 數字變高而寫 test。

問題：

- 測試沒有 spec trace
- 很可能只是執行程式碼，不驗證行為
- mutation 很容易 survived

---

### 2. Trusting generated tests directly

AI / JIT 產生的測試不能直接當作可信測試。

必須經過：

- baseline execution
- mutation validation
- stability check

---

### 3. Full-scope mutation without impact analysis

全量 mutation 成本太高，也會讓 CI 難以落地。

應該根據 diff / impact set 限縮。

---

### 4. Spec drift without governance

如果實作行為改了，但 spec 沒更新，就會造成隱性規格漂移。

這是本 workflow 特別要防止的問題。

---

### 5. Agent decides correctness alone

Agent 可以提出建議，但不應單方面決定 correctness。

Ambiguity、breaking change、規格演進必須由 human 決定。

---

## 建議拆分的 Playbooks / Skills

### 1. `preflight-protocol`

用途：

- 在複雜任務開始前列出理解、假設、不確定處、歧義、風險與下一步

Trigger：

- 任務複雜
- 需求模糊
- 涉及多檔案、多階段或架構修改

Output：

- task understanding
- assumptions
- uncertainties
- ambiguity list
- risks
- next step proposal

---

### 2. `spec-drill-down`

用途：

- 對 plan / requirement 進行多輪追問
- 將模糊需求轉成可測試 spec

Trigger：

- spec 不完整
- acceptance criteria 不清楚
- input / output / edge cases 未定義

Output：

- clarified spec
- open questions
- acceptance criteria
- non-goals
- testable requirements

---

### 3. `devils-advocate-review`

用途：

- 從反方角度審查 plan / spec
- 找出風險、缺漏、過度設計與隱含假設

Trigger：

- spec 即將定稿
- plan 即將實作
- PR / roadmap 影響較大

Output：

- objections
- hidden assumptions
- risk list
- simplification proposal
- required clarifications

---

### 4. `spec-definition`

用途：

- 將需求整理成正式 spec
- 判斷 README 與正式 spec 的文件分工
- 產生可實作、可測試、可追蹤的 spec 格式
- 初步標出主工作流，供後續 atomic decomposition 使用

Output：

- recommended spec location
- main workflow candidates
- scope
- non-goals
- inputs
- outputs
- rules
- invariants
- error conditions
- acceptance criteria
- testing implications
- open questions

---

### 4.5. `workflow-atomic-decomposition`

用途：

- 將 revised spec 中的主工作流拆成 workflow slices
- 由 human 暫時指定 selected workflow
- 將 selected workflow 拆成可單獨實作、測試與 review 的 atomic items

Trigger：

- revised spec 已足夠描述主資料流或主行為流
- 即將進入 test design 或 implementation
- 使用者要求先拆 atomic 實作步驟
- spec 已有 acceptance criteria，但 implementation plan 仍過大

Output：

- main workflow map
- candidate workflow slices
- human-selected workflow
- atomic implementation items
- item-to-spec traceability
- deferred items
- spec gaps / open questions

---

### 5. `spec-based-test-design`

用途：

- 從 spec 產生 test cases
- 確保測試能 trace back to spec
- 優先對已拆解的 atomic items 設計測試

Output：

- test matrix
- spec-to-test mapping
- atomic-item-to-test mapping
- edge cases
- error cases

---

### 6. `diff-analysis`

用途：

- 分析 git diff
- 找出 changed files / changed behavior candidates

Output：

- changed components
- affected modules
- possible behavior changes

---

### 7. `intent-analysis`

用途：

- 根據 diff、PR description、context 推斷 developer intent

Output：

- change intent
- confidence
- uncertainty
- risk notes

---

### 8. `impact-analysis`

用途：

- 找出 impact set
- 決定哪些 spec、tests、modules 受影響

Output：

- impacted components
- impacted specs
- impacted tests
- impact confidence

---

### 9. `jit-test-generation`

用途：

- 根據 diff + intent + impact 產生或選取 tests

Output：

- generated tests
- selected existing tests
- traceability metadata
- reproducibility info

---

### 10. `mutation-testing`

用途：

- 對 impacted scope 執行 mutation testing
- 驗證測試是否有效

Output：

- mutation score
- killed mutations
- survived mutations
- suspicious equivalent mutations

---

### 11. `test-effectiveness-evaluation`

用途：

- 解讀 mutation result
- 判斷 test gap / spec gap / implementation issue

Output：

- effective tests
- weak tests
- validation gaps
- recommended improvements

---

### 12. `decision-proposal`

用途：

- 把驗證結果整理成人可決策的選項

Output：

- accept / update spec / reject / refine tests options
- recommendation
- risk notes

---

### 13. `test-promotion`

用途：

- 根據 mutation validation 與穩定性決定測試是否升級

Output：

- promoted tests
- discarded tests
- persisted regression tests

---

### 14. `spec-test-evolution`

用途：

- 根據 human decision 更新 spec、tests、playbook 或 skill

Output：

- updated spec
- updated tests
- updated workflow notes

---

## 建議目錄結構

```text
personal-ai-runtime/
  agent-playbooks/
    preflight-protocol.md
    spec-drill-down.md
    devils-advocate-review.md
    workflow-atomic-decomposition.md
    spec-driven-change-verification-workflow.md

  agent-skills/
    preflight-protocol/
      SKILL.md
    spec-drill-down/
      SKILL.md
    devils-advocate-review/
      SKILL.md
    spec-driven-change-verification/
      SKILL.md
    workflow-atomic-decomposition/
      SKILL.md
    spec-based-test-design/
      SKILL.md
    diff-analysis/
      SKILL.md
    intent-analysis/
      SKILL.md
    impact-analysis/
      SKILL.md
    jit-test-generation/
      SKILL.md
    mutation-testing/
      SKILL.md
    test-effectiveness-evaluation/
      SKILL.md
    decision-proposal/
      SKILL.md
    test-promotion/
      SKILL.md
```

---

## 與 Personal AI Runtime 的對應位置

本 workflow 主要屬於：

```text
Reasoning / Decision
```

但會跨到：

```text
LLM Runtime / Integration
```

因為它需要 agent / LLM 協助：

- drill-down 問題
- devil's advocate review
- diff / intent analysis
- JIT test generation
- mutation result interpretation
- decision proposal

也會與專案 CI / testing 工具整合，例如：

- Jest
- Stryker
- Git diff
- GitHub Actions
- PR template

---

## 最小可行版本 MVP

若要先落地，不必一次實作完整 workflow。

建議 MVP：

```text
1. Preflight Protocol
2. Spec Drill-down
3. Devil's Advocate Review
4. Workflow Atomic Decomposition
5. Spec-Based Test Design
6. Diff Analysis
7. JIT Test Suggestion
8. Mutation Result Review
9. Human Decision Proposal
```

第一階段可以先不自動生成正式 test 檔，而是讓 agent 產生：

- main workflow map
- human-selected workflow
- atomic implementation items
- suggested test cases
- expected behavior
- mutation survived interpretation
- spec update proposal

等流程穩定後，再逐步自動化。

---

## 一句話總結

本 workflow 的核心不是讓 AI 自動寫更多測試，而是建立一條從 **spec clarity → plan challenge → implementation → diff-aware verification → mutation validation → human governance → spec/test evolution** 的閉環。

它把測試從 CI 裡的一個檢查步驟，提升成一套可以隨著專案演進而自我強化的 verification system。
