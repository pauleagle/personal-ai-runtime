# Release Preflight

## 目的

Release Preflight 是在建立版本、tag、release note、README 或 CHANGELOG 前執行的檢查流程。

它的目標是避免版本資訊、文件、實際功能與 Git 狀態不一致。

## 觸發時機

- 準備建立 git tag
- 準備發布 v1.0.0 / v1.1.0 / v2.0.0
- README.md 更新前
- CHANGELOG.md 更新前
- CONTRIBUTING.md 更新前
- GitHub 專案準備公開或整理前

## 檢查項目

### 1. Version Check

確認目前版本號是否合理：

- patch：修 bug、小幅文件修正
- minor：新增功能但不破壞既有介面
- major：破壞性變更、架構大改、使用方式大幅改變

### 2. README Alignment

確認 README.md 是否對齊目前專案狀態：

- 專案目的
- 安裝方式
- 執行方式
- 設定檔說明
- 範例指令
- 輸入與輸出位置
- 已知限制
- 目前版本功能

### 3. CHANGELOG Hygiene

確認 CHANGELOG.md 是否符合版本化紀錄：

- 最新版本在最上方
- 每個版本有獨立區塊
- 每個版本有日期
- 變更依類型分類
- 不直接貼 commit log
- 不直接貼 AI 對話紀錄
- 不把零散筆記堆在檔案底部

### 4. Git Status Check

確認：

- 是否有未追蹤檔案
- 是否有不該 commit 的檔案
- `.gitignore` 是否涵蓋 build output、cache、node_modules、dist 等
- commit 範圍是否乾淨

### 5. Tag Readiness

建立 tag 前確認：

- README 已更新
- CHANGELOG 已更新
- 測試或基本執行流程已確認
- commit message 已準備
- 版本號與 tag 名稱一致

## 標準 Prompt

請協助執行 release preflight。

請先檢查目前專案是否已準備好進行版本發布或建立 git tag。

請不要直接修改檔案，先列出：

1. 目前版本判斷
2. README 是否需要更新
3. CHANGELOG 是否符合慣例
4. 是否有疑似不該 commit 的檔案
5. 建議的 commit message
6. 建議的 tag 名稱
7. 需要我確認的地方

等我確認後，再進行修改。