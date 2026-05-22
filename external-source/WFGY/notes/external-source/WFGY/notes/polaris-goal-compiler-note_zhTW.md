# Polaris Goal Compiler 閱讀筆記

## 來源

- Source: WFGY / Polaris / Goal Compiler
- Upstream file: `Polaris/protocols/goal-compiler/POLARIS_GOAL_COMPILER.txt`
- Repo: `onestardao/WFGY`
- Note type: external-source reading note / workflow design reference

## 一句話摘要

Polaris Goal Compiler 是一套給 AI assistant、agent、skill-based workflow 使用的目標編譯與執行治理規則。

它的核心不是讓 AI 更會「寫漂亮答案」，而是要求 AI 在執行前先把自然語言需求轉成有邊界、依賴、驗證條件與完成標準的 task atoms。

核心精神：

```text
Compile before construction.
Verify before unlock.
Truth before expression.
```

對 personal-ai-runtime 來說，它最有價值的地方是：防止 agent 直接執行一整坨模糊需求、混合多種工作、過早宣稱完成，或把可讀輸出誤當成真實驗證。

## 核心定位

Polaris Goal Compiler 比較像是：

- agent execution constitution
- goal compilation protocol
- preflight / planning governance layer
- tool execution 前的 filter
- 複合任務拆解與驗證規則
- 防止 premature completion 的任務治理層

它關心的不是語氣，而是：

- 什麼任務可以開始執行
- 哪些任務必須先拆解
- 哪個 atom 現在可以動
- 哪些 downstream work 還不能碰
- 什麼狀態才可以宣稱完成
- 什麼只是 readable output，不能當成 truth proof

## 核心原則

### 1. Raw user request 不可直接執行

Polaris 的核心規則是：

```text
Raw user language is not executable.
Only compiled task atoms may receive construction authority.
```

也就是：

```text
raw request
  -> goal compilation
  -> task atoms
  -> active atom
  -> execution
  -> verification
  -> downstream unlock
```

自然語言需求需要先轉成有輸入、輸出、邊界、依賴與驗證條件的 task atom，才適合交給 agent 執行。

### 2. Mixed goal 必須拆成 atoms

若使用者的請求同時包含多個動作，例如：

```text
修正這個問題，整理 README，再更新 changelog。
```

不應直接當成一個任務執行。較合理的拆解是：

```text
DEFINE   定義問題與成功標準
LOCATE   找出影響範圍與缺口
DERIVE   推導修改策略
PATCH    修改程式或文件
VERIFY   驗證修改結果
DECIDE   判斷是否通過
ORGANIZE 整理已驗證資訊
WRITE    產生 README / changelog / 對外說明
```

重點是：`WRITE` 類任務不能早於 `VERIFY` / `DECIDE`。漂亮輸出不能取代真實驗證。

### 3. Truth work 先於 expression work

Polaris 明確區分 truth work 與 expression work。

| 類型 | 說明 | 例子 |
|---|---|---|
| Truth work | 改變或驗證真實狀態、正確性、結構與完成條件 | 找 bug、修 bug、補測試、驗證行為、確認 spec |
| Expression work | 將已驗證資訊整理成可讀形式 | README、changelog、摘要、文章、對外說明 |

核心提醒：

```text
Readable output is not proof.
Local success is not whole-goal completion.
Candidate patch is not verified repair.
```

### 4. 一輪只執行一個 active atom

Polaris 要求一個 execution round 只能有一個 active atom。

這可以避免 agent 同時：

- 修 code
- 寫 README
- 更新 changelog
- 順手改其他檔案
- 宣稱整體任務完成

這類 mixed execution 容易造成 scope creep、downstream leakage、驗證不清，以及 local success 被誤認成 global success。

### 5. Verified 才能 unlock downstream

Polaris 拒絕以下狀態作為解鎖條件：

```text
LOCALLY_DONE
PROBABLY_DONE
LOOKS_COMPLETE
```

只有上游 atom 達到 `VERIFIED`，下游 atom 才能被 unlock。

工程對應：

```text
PATCH 完成
  ≠ 可以發布

PATCH + tests pass
  ≠ 一定可以發布

PATCH + tests pass + acceptance criteria / review / mutation review 通過
  才接近可宣稱完成
```

## Canonical Atom Classes

| Atom Class | 意義 | 工程語境對應 |
|---|---|---|
| DEFINE | 定義目標、truth object、邊界、成功標準 | 釐清需求與完成定義 |
| LOCATE | 定位缺口、阻塞、依賴、證據 | 找問題、找影響範圍 |
| DERIVE | 推導策略、缺漏結構與修改方案 | 設計實作策略 |
| PATCH | 修改、修復、連接、封裝 | 實作變更 |
| VERIFY | 測試、驗證、反證、確認合法性 | 跑測試、review、檢查 |
| DECIDE | 做 go / no-go 判斷 | 是否接受、是否繼續 |
| ORGANIZE | 整理、排序、彙整已驗證事實 | 整理結果與紀錄 |
| WRITE | README、文章、公開說明、敘事輸出 | 文件與對外表達 |

建議順序：

```text
DEFINE -> LOCATE -> DERIVE -> PATCH -> VERIFY -> DECIDE -> ORGANIZE -> WRITE
```

## 對 personal-ai-runtime 的對應

### Preflight Protocol

Polaris 可以視為更嚴格、更形式化的 Preflight Protocol。

Preflight Protocol 關心：

- 任務理解
- 假設
- 不確定處
- 可能解讀
- 風險
- 下一步

Polaris 進一步要求：

- 是否為 mixed goal
- 是否需要 detonate
- atom count
- blocked atoms
- current active atom
- success test
- failure test
- verification gate

### Spec-driven Change Verification Workflow

Polaris 與 spec-driven workflow 可以這樣對應：

```text
Spec / Plan
  -> DEFINE / LOCATE / DERIVE

Implementation
  -> PATCH

Test / Verification
  -> VERIFY

Acceptance / Review
  -> DECIDE

Documentation
  -> ORGANIZE / WRITE
```

特別適合用在：

- refactor
- migration
- README / CHANGELOG 對齊
- agent skill 抽取
- repo cleanup
- complex code change
- RAG pipeline 設計
- model routing policy 更新
- verification-heavy workflow

### Devil's Advocate Review

Devil's Advocate Review 適合放在 `VERIFY` 或 `DECIDE` 階段，用來挑戰：

- 是否偷換目標
- 是否過早宣稱完成
- 是否只完成 local success
- 是否測試本身不足
- 是否 readable output 被誤當 truth proof
- 是否下游文件早於上游驗證

## 可萃取成 Lite Skill 的規則

Polaris 原始 protocol 很完整，但日常任務不一定需要完整展開。較適合先萃取成 `goal-compilation-lite` 類型的輕量規則。

草案：

```text
Before construction:

1. Do not execute raw user requests directly.
2. Identify whether the request is simple or mixed.
3. If mixed, split it into task atoms.
4. Classify each atom:
   DEFINE / LOCATE / DERIVE / PATCH / VERIFY / DECIDE / ORGANIZE / WRITE
5. Mark dependencies and blocked atoms.
6. Select exactly one active atom for the current round.
7. Do not perform WRITE before truth-bearing atoms are verified.
8. Do not claim completion unless the user-expected endpoint is satisfied.
9. Treat readable output as expression, not proof.
10. Report partial / deferred / review-ready honestly when full closure is not reached.
```

## 使用邊界

適合啟用 goal compilation 的場景：

- 多步驟 coding task
- refactor
- migration
- bug fix + tests + docs
- README / CHANGELOG release work
- agent skill / playbook 抽取
- RAG pipeline 設計
- model routing policy 設計
- verification-heavy workflow
- 需要避免 AI 過早完成宣稱的任務

不一定需要完整啟用的場景：

- casual chat
- 單純翻譯
- 單句改寫
- 非正式 brainstorming
- 很小的格式調整

輕量場景仍可保留三條精神：

```text
Compile before construction.
Verify before unlock.
Truth before expression.
```

## 風險與注意事項

### 1. 完整版本可能過重

Polaris 原始格式包含大量 governance object，例如：

```text
GOAL_COMPILATION
TASK_GRAPH
COUNT_BOARD
ATOM_TABLE
EXECUTION_TOKEN_BOARD
ROUND_LOCK
DOWNSTREAM_LEAK_AUDIT
ROUND_RESULT
PACKAGE_CONTRACT
CLOSURE_RECORD
```

日常使用時若完整展開，可能造成對話太重、執行成本太高、小任務過度治理，或 agent 花太多篇幅在 governance output。

建議採用：

```text
full protocol as reference
lite skill for daily use
compact board for complex task
```

### 2. Protocol 不是正確性保證

Polaris 可以降低 false completion 的風險，但不能保證：

- 每次拆解都完美
- 完全消除 hallucination
- 所有 domain 都能正確驗證
- 自然語言永遠沒有歧義

它比較像是讓 agent 更難直接亂做與過早宣稱完成的治理層。

### 3. 需要與實際工具鏈整合

若要落地到 personal-ai-runtime，後續需要決定：

- 哪些任務強制 goal compilation
- 哪些任務只需要 compact mode
- task atom 是否影響 model routing
- `VERIFY` atom 是否接 mutation testing / unit tests / model-fit-profiler
- `WRITE` atom 是否必須引用 verified facts
- Codex / Claude Code / local agent 是否共用同一份 lite skill

## 個人結論

Polaris Goal Compiler 的價值不在於一段更長的 prompt，而在於它把 agent 工作方式從：

```text
收到請求 -> 直接產出
```

改成：

```text
收到請求
  -> 編譯目標
  -> 拆解 task atoms
  -> 判斷依賴與阻塞
  -> 授權單一 active atom
  -> 執行
  -> 驗證
  -> 解鎖下游
  -> 最後才整理與表達
```

對 personal-ai-runtime 而言，Polaris Goal Compiler 適合作為：

- external-source 參考資料
- goal-compilation playbook 的來源
- goal-compilation-lite skill 的設計基礎
- spec-driven verification workflow 的治理強化層
- agent workflow 中防止 premature completion 的規則來源

最精簡的個人化理解：

> 不要讓 AI 直接執行一整坨自然語言。先把目標編譯成 task atoms，一次只執行一個 atom，真實驗證通過後才允許下游整理與表達。

