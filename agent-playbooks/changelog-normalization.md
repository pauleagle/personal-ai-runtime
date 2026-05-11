# Changelog Normalization

## 目的

Changelog Normalization 是在整理、發布或檢查 `CHANGELOG.md` 前執行的文件整理流程。

它的目標是將 `CHANGELOG.md` 從零散開發筆記、commit 摘要、AI 對話紀錄，整理成版本化、分類化、可讀的 release history。

## 核心原則

`CHANGELOG.md` 不是開發流水帳，也不是 commit log。

它應該讓使用者快速理解：

- 這個版本新增了什麼
- 改變了什麼
- 修正了什麼
- 移除了什麼
- 是否有破壞性變更

## 適用時機

- 準備發布版本前
- 準備建立 git tag 前
- `CHANGELOG.md` 長期累積零散筆記後
- `CHANGELOG.md` 混入 commit log、AI 對話紀錄或 TODO
- 需要將未分類變更整理成版本紀錄
- 需要檢查 `CHANGELOG.md` 是否符合 release history 慣例

## 不適用時機

- 只新增一筆已明確指定版本與分類的 changelog entry
- 單純修正一個錯字
- 使用者已提供完整且不可更動的 changelog 格式
- 專案尚未決定是否維護 `CHANGELOG.md`

## 格式原則

1. 最新版本放最上方
2. 每個版本有獨立區塊
3. 每個版本建議附日期
4. 變更依類型分類
5. 不把完整 commit message 原樣貼入
6. 不把 AI 對話紀錄原樣貼入
7. 不把臨時 TODO 堆在檔案底部
8. 不確定版本歸屬時，先放入 `Unreleased`
9. 不憑空發明版本號、日期或功能內容

## 建議分類

常用分類：

- Added
- Changed
- Fixed
- Removed
- Docs
- Internal

視需要可加入：

- Deprecated
- Security
- Breaking Changes

## Agent 行為規則

agent 在整理 `CHANGELOG.md` 前，應先檢查目前內容狀態，而不是直接重寫。

除非使用者明確要求直接修改，否則應先輸出整理評估與建議策略。

agent 應判斷：

1. 目前 `CHANGELOG.md` 的格式問題
2. 是否存在零散貼在底部的開發紀錄
3. 是否存在未分類變更
4. 是否存在版本順序錯亂
5. 是否缺少日期
6. 是否混入 commit log 或 AI 對話紀錄
7. 哪些內容可以保留、合併、移動、改寫或刪除
8. 是否有版本歸屬不明的內容需要放入 `Unreleased`

若版本歸屬、日期、刪除範圍或 release scope 不明，agent 應先提出問題或整理策略，不應直接做破壞性修改。

## 標準 Prompt

請檢查本專案的 `CHANGELOG.md`。

目標是將它整理成版本化、分類化、可讀的 release history。

請先不要直接改檔，先列出：

1. 目前格式問題
2. 是否有零散開發紀錄
3. 是否有未分類變更
4. 是否有版本順序錯亂
5. 是否缺少日期
6. 是否混入 commit log 或 AI 對話紀錄
7. 建議的整理策略
8. 哪些內容可以保留、合併、移動、改寫或刪除
9. 需要我確認的地方

等我確認後，再進行修改。

## 建議輸出格式

### Current Issues

目前發現的問題：

- ...

### Proposed Structure

建議整理後的結構：

- ...

### Entries To Keep

建議保留的內容：

- ...

### Entries To Merge Or Move

建議合併或移動的內容：

- ...

### Entries To Rewrite Or Remove

建議改寫或刪除的內容：

- ...

### Open Questions

需要確認的地方：

- ...

### Next Steps

建議下一步：

1. ...
