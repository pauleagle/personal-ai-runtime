# PB-FU-005 — 將 Mutation Framework 定位為 JIT Mutation Workflow 的後期 Regression Gate

> Status: Draft
> Type: Playbook Foundation Upgrade
> Scope: Spec-Driven Change Verification / JIT Test Generation / Mutation Testing
> Purpose: 明確化「diff / intent / impact -> JIT tests -> scoped manual mutation」作為 atomic item 預設驗證策略，並定義何時才值得導入 mutation framework。

---

## 1. 核心判斷

在目前的 spec-driven、atomic-item、usage-gated workflow 中，預設不需要一開始就引入 mutation framework。

核心價值鏈是：

```text
diff / intent / impact
-> JIT tests
-> scoped manual mutation
-> spec / handoff evidence
```

這個流程追求的是：

```text
這次改動的關鍵錯誤會不會被抓到？
```

而不是：

```text
全 repo mutation score 有多高？
```

因此，manual mutation 應該是 atomic item 的 default；mutation framework 則應定位為後期、穩定期、回歸期的工具。

---

## 2. 為什麼 Manual Mutation 更適合 Atomic Item

對小範圍、意圖清楚、風險可列舉的 atomic item 來說，manual mutation 通常比 framework 更準、更便宜。

原因：

- 可以直接從 diff / intent / impact 推出 1 到 4 個高價值 mutant。
- 可以直接指定最小 focused tests，不需要跑昂貴的全套 mutation。
- 可以把 killed / survived / equivalent / skipped 結果直接寫回 spec 與 handoff。
- 避免在 spec 還快速演化時，被 framework 的大量等價 mutant 或低訊號報告拖住。
- 更符合 usage-gated workflow：每個 atomic item 結束時要驗證、commit、停下來等下一個 gate。

---

## 3. 預設分界

| 情境 | 建議 |
|---|---|
| atomic item 範圍小、意圖清楚、風險點可列 1-4 個 | manual mutation 足夠 |
| validator / policy / provenance / schema guard 這類 deterministic logic | manual mutation 很適合 |
| spec 還在快速演化，測試邊界常調整 | 先不要引入 framework |
| 同一類 mutant 反覆出現，manual mutation 開始重複 | 考慮 framework |
| 模組進入穩定期，要做 release / regression gate | 考慮 framework |
| 大量條件分支、狀態 aggregation、WAV analyzer、timeline mapper 已成形 | 評估 scoped framework mutation |

---

## 4. Mutation Framework 的正確定位

Mutation framework 不應成為每個 atomic item 的預設內圈工具。

較好的定位是：

```text
Manual mutation:
  inner loop / atomic item / JIT validation

Framework mutation:
  outer loop / regression gate / stable module checkpoint
```

也就是說：

- manual mutation 檢查「這次改動最可能壞在哪」；
- framework mutation 檢查「這一整片穩定邏輯有沒有長期測試弱點」。

---

## 5. 導入 Framework 的建議時機

導入 mutation framework 前，應至少滿足部分條件：

- 目標模組已有相對穩定的 public behavior。
- 已累積多個 deterministic validator / analyzer / aggregator。
- manual mutation case 開始重複，且維護成本變高。
- 需要 release、regression、或 cross-atomic checkpoint 的更廣覆蓋。
- 有能力把 framework mutation 限定在 impacted module / test target，而不是盲目全 repo 跑。
- 已有方式分類 survived mutant：code issue、test gap、spec gap、equivalent、selector weakness。

不建議導入的情境：

- 只是為了追 mutation score。
- spec 還在快速變動。
- atomic item 很小，manual mutant 已能覆蓋主要風險。
- framework 只能跑全 repo，成本明顯高於本次風險。

---

## 6. 與 SK-FU-003 的關係

`SK-FU-003` 聚焦在 mutation case / focused test selector：

```text
atomic item / risk key / spec ref
-> mutation cases
-> focused test command(s)
-> killed / survived / equivalent / skipped result
```

`PB-FU-005` 則補上更高層的 playbook 判斷：

```text
何時 manual mutation 是 default？
何時 framework mutation 才值得進場？
```

兩者關係：

- `SK-FU-003` 是 selector / harness 層。
- `PB-FU-005` 是 workflow policy / timing 層。

---

## 7. 建議 Playbook 規則

在 Spec-Driven Change Verification workflow 中加入以下規則：

1. 每個 atomic item 先從 diff / intent / impact 推出 focused JIT tests。
2. 若行為風險可列出 1 到 4 個 mutant，優先做 scoped manual mutation。
3. Manual mutation 必須記錄 mutant、命令、結果、是否 killed，以及是否已還原。
4. 若 manual mutation 顯示 survived 或 suspicious equivalent，交給 test-effectiveness evaluation 或 proposal decision。
5. Mutation framework 只在穩定期、重複成本升高、或需要 regression gate 時導入。
6. 導入 framework 時，優先要求 scoped execution：限定 module、test target、risk tag、或 spec ref。
7. 不以 mutation score 取代 spec traceability、JIT test rationale、或 human decision gate。

---

## 8. 參考案例：MVP09-02

`audio-topology-runtime` 的 `MVP09-02` 是典型 manual mutation 足夠的案例。

範圍：

- provenance gate；
- deterministic policy / identity / readiness checks；
- 無 WAV sample analysis；
- 無大型 state aggregation；
- 主要風險可列為 4 個 mutant。

Manual mutation 檢查：

| Mutant | 目的 |
|---|---|
| 移除 concrete WAV missing guard | 確認 expected paths 不能替代 concrete WAV |
| 把 `candidate_valid` 錯當成 MVP09 selected 狀態 | 確認不能繞過 MVP07 selection evidence |
| 移除 backend request fingerprint identity comparison | 確認 materialization identity 錯接會被抓到 |
| provenance gate 繞過 request validation | 確認 MVP09-01 gate 仍是 MVP09-02 前置條件 |

結果：4/4 killed。

這類情境不需要立刻引入 framework；framework 較適合等 `MVP09-03` 到 `MVP09-06` 累積 WAV integrity、timeline mapping、boundary evidence、status aggregation 後，再評估是否作為 scoped regression gate。

---

## 9. Acceptance Criteria

- Playbook 明確定義 manual mutation 是 atomic item 的預設策略。
- Playbook 明確定義 framework mutation 的導入時機與不導入條件。
- Workflow guidance 保留 framework mutation 作為 regression / stable checkpoint 工具。
- Guidance 與 `SK-FU-003` 的 selector / harness follow-up 不重疊，而是補足 policy layer。
- 未來導入 framework 時，必須能說明 scope、成本、風險、selector、以及 why now。
