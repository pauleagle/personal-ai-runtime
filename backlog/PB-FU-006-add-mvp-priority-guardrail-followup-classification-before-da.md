# PB-FU-006 — 在 DA 前加入 MVP Priority / Guardrail / Follow-up 分層

> Status: Draft
> Type: Playbook Foundation Upgrade
> Scope: Spec Drill Down / Devil's Advocate Review / Workflow Atomic Decomposition
> Purpose: 避免 DA 把 MVP 拉成完整版規格；在每個 MVP 或大流程 drill-down 階段，先區分優先做出來的最小目標、不可破壞的 guardrail，以及可後續優化的 future feature。

---

## 1. 核心判斷

MVP 的目標不是把所有風險和品質細節一次解完，而是先做出一個最小、可跑、可觀察、能證明方向的工具或流程。

DA 的目標也不是阻止 MVP，而是辨識：

```text
哪些風險會讓 MVP 語意錯誤或不可驗證？
哪些只是目前 POC 的限制？
哪些應該成為後續優化項目？
```

因此，Spec Drill Down 進入 DA 前，應先建立三層分類：

| 分層 | 問題 | 判斷標準 |
|---|---|---|
| MVP Priority | 這一版最小要做出什麼？ | 沒有它就不能證明方向 |
| Guardrail / Blocker | 哪些不能錯？ | 錯了會破壞 source、contract、traceability、status、provenance、或安全邊界 |
| Follow-up Future Feature | 哪些可以之後打磨？ | 影響品質、泛用性、體驗、效能或完整度，但不阻止第一版存在 |

---

## 2. 問題背景

目前 spec-driven workflow 已經有：

```text
Prompt
-> Spec Drill Down
-> Devil's Advocate Review
-> Objection Resolution
-> Workflow Atomic Decomposition
-> TDD / Verification
```

這能有效降低幻覺、保護 contract、暴露風險。

但在 MVP 階段，DA 很容易把未來一定會遇到的品質問題也列成 blocker，例如：

- analyzer 或 parser 未完全泛化；
- transform / processing quality 還不夠好；
- UX / A/B review / reporting 還不完整；
- 多樣本、多場景、多 backend 還未覆蓋；
- regression / mutation framework 尚未完整導入。

這些風險可能真實存在，但不一定應阻止 MVP 第一版。

---

## 3. 新增 Playbook 步驟

在每個 MVP / 大流程 drill-down 階段，DA 前先加入：

```text
MVP Layering Pass
```

流程變成：

```text
Prompt
-> Spec Drill Down
-> MVP Layering Pass
   -> MVP Priority
   -> Guardrail / Blocker
   -> Follow-up Future Feature
-> Devil's Advocate Review
-> DA Classification
-> Objection Resolution
-> Workflow Atomic Decomposition
```

這個步驟不是取代 DA，而是先替 DA 設定邊界，避免 DA 將所有未來品質問題都升級成 implementation blocker。

---

## 4. MVP Layering Checklist

### 4.1 MVP Priority

先問：

```text
這一版最小要證明什麼？
什麼輸入必須能被處理？
什麼輸出必須被產生？
什麼 evidence 必須能被觀察？
什麼結果足以支持下一輪學習？
```

MVP priority 通常應具備：

- 可執行；
- 可驗證；
- 有實際輸入或代表性 fixture；
- 有明確 artifact / report / evidence；
- 不依賴完整 future polish；
- 能暴露下一輪需要解的真問題。

### 4.2 Guardrail / Blocker

再問：

```text
哪些錯誤一旦發生，會讓 MVP 結果不可信？
哪些安全、來源、狀態、contract 邊界不能被破壞？
哪些問題若不先解，implementation 會誤導下一輪？
```

Guardrail / blocker 應限於 correctness 和 safety 邊界，例如：

- source overwrite；
- provenance / traceability 斷裂；
- blueprint / spec / request authority 被偷偷改寫；
- output ref 與 source ref 混淆；
- readiness status 自動升級；
- hidden transform / hidden side effect；
- validation bypass；
- scope leakage；
- artifact identity collision。

### 4.3 Follow-up Future Feature

最後問：

```text
哪些事情會讓結果更好，但不影響第一版能否證明方向？
哪些問題可以先寫成 known limitation？
哪些能力應排進下一個 MVP 或 follow-up？
```

Follow-up future feature 可以包含：

- 品質優化；
- 泛用性擴展；
- 多 backend / 多資料型態支援；
- analyzer / parser calibration；
- transform quality tuning；
- UX / reporting polish；
- subjective review workflow；
- broad regression suite；
- framework-level mutation / benchmark。

---

## 5. DA Classification Rule

DA review 產生 objection 後，每個 objection 必須分類：

| Classification | 意義 | 後續處理 |
|---|---|---|
| `blocker` | 不解會讓 MVP 語意錯、危險、不可追蹤或不可驗證 | 必須在 atomic decomposition 前解決 |
| `mvp_limitation` | 第一版可接受，但要明寫限制 | 寫入 spec limitation / warning / evidence |
| `follow_up` | 品質、泛用性、體驗、效能或完整度優化 | 建 follow-up backlog 或 future MVP |
| `human_decision` | 需要 human 明確選擇 policy、scope 或 tradeoff | 進 proposal / decision gate |

DA objection 不應只標 severity；還應標出它對 MVP 的實際阻擋關係。

建議欄位：

```yaml
id: DA-...
severity: Low | Medium | High
classification: blocker | mvp_limitation | follow_up | human_decision
affected_scope: ...
risk: ...
why_it_matters: ...
required_action: ...
blocks_atomic_decomposition: true | false
```

---

## 6. 泛化案例：基礎處理工具 MVP

某個 MVP 想先建立「讀取既有輸入、依照 frozen spec / blueprint / policy 做最基礎處理、產生新 output 和 before/after evidence」的工具。

### MVP Priority

- 讀取既有輸入和對應 spec / blueprint / policy。
- 分析輸入與目標 contract 的差異。
- 執行最基本、明確、可追蹤的處理。
- 產生新的 output artifact。
- 寫入 before/after evidence、transform metadata、source preservation proof。

### Guardrail / Blocker

- 不覆蓋原始輸入。
- 不偷偷改寫 spec / blueprint / policy。
- 不把 baseline copy 誤標成真正處理結果。
- 不把 objective / timing / structural evidence 自動升級成 subjective 或 publishing readiness。
- 所有 refs 必須 trace 到同一個 request / source / contract。

### Follow-up Future Feature

- analyzer calibration；
- transform quality tuning；
- weak-signal / noisy-input robustness；
- multi-segment / cross-boundary extension；
- subjective review workflow；
- reporting polish；
- broad regression / benchmark；
- framework-level mutation。

這類場景中，DA 應保護 guardrail，但不應要求 MVP 先完成所有品質打磨。

---

## 7. 與既有 Playbook 的關係

這個 follow-up 補強：

- `spec-drill-down`：加入 MVP priority / guardrail / follow-up 的前置分層。
- `devils-advocate-review`：要求 DA objection 必須標示 classification 和 blocking status。
- `devils-advocate-drill-down`：優先處理 blocker，將 limitation / follow-up 明確轉成 spec notes 或 backlog。
- `workflow-atomic-decomposition`：只把已解 blocker 的 MVP priority 拆成 atomic items。
- `decision-proposal`：把真正需要 human tradeoff 的項目送進 decision gate。

它不取代任何既有 playbook；它是 MVP 階段的 scope-control layer。

---

## 8. Acceptance Criteria

- Spec Drill Down playbook 增加 MVP Layering Pass。
- DA Review playbook 增加 objection classification 欄位。
- DA Drill-down playbook 優先處理 `blocker`，並將 `mvp_limitation` / `follow_up` 分流。
- Workflow Atomic Decomposition 不應因 follow-up polish 未完成而阻塞 MVP。
- 每個 MVP spec 至少能列出：
  - MVP priority；
  - guardrail / blocker；
  - follow-up future feature；
  - known limitation；
  - human decision。
- Playbook guidance 明確寫出：DA 的角色是分類與保護邊界，不是把 MVP 自動升級成完整版規格。
