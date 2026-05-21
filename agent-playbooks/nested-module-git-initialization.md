# Nested Module Git Initialization

## 目的

Nested Module Git Initialization 是整理 `modules/` 或 `poc-modules/` 底下子專案時的 Git 邊界檢查流程。

這些目錄底下的專案預期會各自成為獨立 repository。當 agent 在整理、補文件、建立 spec、產生 scaffold 或調整內容時，如果發現目標子專案尚未在自己的 project root 執行 `git init`，應協助初始化，避免變更只停留在上層 workspace 的 ignored directory 裡。

## 核心原則

`modules/` 與 `poc-modules/` 是子專案工作區，不是 root repo 直接追蹤的普通資料夾。

判斷子專案是否已初始化時，應檢查該子專案 root 是否存在 `.git` directory 或 `.git` file。不要只依賴 `git -C <path> rev-parse --show-toplevel`，因為它可能回傳上層 `personal-ai-runtime` repo，導致誤判。

若目標子專案 root 沒有 `.git`，且本次任務正在整理該子專案內容，agent 應主動執行 `git init`。

初始化 Git repository 不等於自動 commit。除非使用者明確要求，agent 不應自動建立 commit、tag 或 remote。

## 適用時機

- 任務目標位於 `modules/<project>/`
- 任務目標位於 `poc-modules/<project>/`
- agent 正在整理子專案 README、SPEC、CHANGELOG、scaffold、source files 或測試
- root repo 的 `.gitignore` 排除了 `modules/` 或 `poc-modules/`
- 子專案 root 尚未存在 `.git`
- 使用者已表明這些子專案預期獨立 `git init`

## 不適用時機

- 目標不在 `modules/` 或 `poc-modules/`
- 使用者只是詢問概念，不需要修改或整理子專案內容
- 子專案已經有 `.git` directory 或 `.git` file
- 目標目錄是上層 repo 的正式 tracked source tree，不應拆成 nested repo
- 目標目錄是 external source、vendor、cache、build output 或 temporary directory
- 使用者明確要求不要初始化 Git

## 工作流程

### 1. 判斷目標子專案 root

從本次任務涉及的路徑找出 project root：

```text
modules/<project>/
poc-modules/<project>/
```

若任務同時涉及多個子專案，應逐一檢查各自的 project root。

### 2. 檢查是否已有獨立 Git repository

優先檢查：

```powershell
Test-Path <project-root>/.git
```

若 `.git` 存在，視為已初始化。它可能是 directory，也可能是 worktree 或 submodule 使用的 file。

可用以下指令輔助確認目前 Git 狀態：

```powershell
git -C <project-root> status --short
```

但若 `git -C <project-root> rev-parse --show-toplevel` 回傳的是上層 workspace，不代表子專案已初始化。

### 3. 初始化缺少 Git 的子專案

若 `<project-root>/.git` 不存在，且該 root 是本次正在整理的 `modules/` 或 `poc-modules/` 子專案，執行：

```powershell
git -C <project-root> init
```

初始化後再執行：

```powershell
git -C <project-root> status --short
```

用來確認 repository 可用並回報目前未追蹤檔案。

### 4. 不自動提交

初始化後，不要自動執行：

```powershell
git add
git commit
git remote add
git tag
```

除非使用者明確要求。

### 5. 回報狀態

回報時應說明：

- 哪個子專案 root 被檢查
- 是否原本已有 `.git`
- 是否執行了 `git init`
- `git status --short` 的重點結果
- 是否還有需要使用者決定的 commit / remote / branch naming

## Agent 行為規則

agent 在整理 `modules/` 或 `poc-modules/` 子專案時，應把 Git 初始化檢查視為標準 housekeeping。

如果子專案 root 沒有 `.git`，agent 可以直接 `git init`，不需要為此額外詢問使用者，因為使用者已建立此 playbook 作為預設規則。

agent 不應在不確定 project root 的情況下初始化 Git。若路徑無法明確對應到 `modules/<project>/` 或 `poc-modules/<project>/`，應先詢問使用者。

agent 不應在 parent repo root 執行 `git init` 來解決子專案問題。

agent 不應刪除、覆蓋或重建既有 `.git`。

agent 不應把 `git init` 失敗時留下的錯誤狀態隱藏起來；應回報錯誤訊息與下一步建議。

## 標準 Prompt

整理 `modules/` 或 `poc-modules/` 底下的子專案時，請先檢查該子專案 root 是否已經有自己的 `.git`。

如果沒有，請協助在該子專案 root 執行 `git init`，再繼續整理內容。請不要自動 commit、設定 remote 或建立 tag，除非我另外要求。

請注意：不要只因為 `git rev-parse` 回傳上層 workspace，就判定子專案已經初始化；要檢查子專案 root 的 `.git`。

## 建議輸出格式

### Git Boundary Check

- Project root:
- `.git` exists:
- Action:

### Initialization Result

- `git init` executed:
- Result:
- Notes:

### Current Status

```text
<git status --short summary>
```

### Next Decisions

- Initial commit needed:
- Remote needed:
- Branch naming needed:
