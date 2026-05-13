# External Source Repo Import

## 目的

External Source Repo Import 是將外部 Git repository URL 匯入 `external-source/` 的標準流程。

它處理的不是單純 `git clone`，而是把外部 repo 放進本專案的外部來源工作區，並同步建立來源紀錄、筆記目錄、萃取目錄、`.gitkeep` 與必要的 `.gitignore` 規則。

## 核心原則

外部 repo 應先被隔離在 `external-source/<source-name>/upstream/<repo-name>/`，不應直接混入本專案核心目錄。

正式目錄應在確認 clone 可行後才建立。若 clone 前置檢查或 clone 本身失敗，agent 應停止並回報原因，不留下半套來源工作區。

外部 repo 的原始內容應由 `.gitignore` 排除；本專案只追蹤整理後的 metadata、notes、extracted files 與 `.gitkeep`。

## 適用時機

- 使用者提供 Git repository URL，想加入 `external-source/`
- 使用者可選擇提供來源命名，未提供時預設使用 repo name
- 使用者提供 private repo URL，且本機 terminal Git 已具備可讀取該 repo 的認證
- 需要建立符合 `external-source/README.md` 的來源工作區
- 需要自動建立來源說明、source links、notes、extracted 與 upstream 結構
- 需要同步調整根目錄 `.gitignore`，避免追蹤 upstream clone 內容

## 不適用時機

- 來源不是 Git repository URL
- 使用者只想暫時查看 repo，不想納入 `external-source/`
- 目標來源資料夾已存在且使用者尚未確認要合併或覆蓋
- clone 無法執行、repo 無法存取或需要尚未提供的 Git 認證
- 任務要求保留 upstream 原始內容在本 repo 中被追蹤

## 工作流程

### 1. 解析輸入

agent 應從輸入取得：

- repo URL，例如 `https://github.com/onestardao/WFGY.git`
- optional source name
- repo name，預設從 URL 最後一段推得，並移除 `.git`

若使用者未提供 source name，`<source-name>` 預設使用 repo name。

### 2. 前置檢查

agent 應檢查：

- `git` 是否可用
- `external-source/README.md` 是否存在
- `external-source/<source-name>/` 是否已存在
- `external-source/<source-name>/upstream/<repo-name>/` 是否已存在

若目標目錄已存在且非空，應停止並詢問使用者如何處理。

### 3. 確認 repo 可存取

正式建置前，agent 應先確認 repo 可 clone。

若使用者表示 repo 是 private，或 `git ls-remote` 回傳 authentication failure，agent 應明確區分：

- browser 已登入 GitHub
- terminal Git / Git Credential Manager / GitHub CLI 是否有可用認證

browser 能開啟 private repo 不代表 `git` 指令具備相同權限。

建議使用：

```powershell
git ls-remote <repo-url>
```

若 sandbox、網路或權限限制導致無法確認，agent 應依工具規則請求執行權限。

`git ls-remote <repo-url>` 屬於本流程的固定前置檢查。若 escalation 需求只涉及對使用者一開始提供的 `<repo-url>` 執行 `git ls-remote`，且 URL 完全一致，agent 可視為預期操作並允許執行。

若 `git ls-remote` 失敗，agent 應停止，不建立正式來源工作區。

若失敗訊息包含 authentication failure、invalid username or token、repository not found 但使用者確認 browser 可看到 private repo，agent 應回報為 Git 認證問題，而不是 repo 不存在。此時不應建立正式來源工作區。

可建議使用者在本機 terminal 完成其中一種認證：

```powershell
gh auth status
gh auth login
```

或更新 Windows Git Credential Manager 中的 GitHub 認證。完成後再重新執行 `git ls-remote <repo-url>`。

### 4. 暫存 clone

agent 應先 clone 到暫存位置，例如：

```text
C:\tmp\external-source-clone-<repo-name>\
```

只有 clone 成功後，才建立正式目錄。

若 `git clone` 需要 escalation，agent 應先確認 clone 的 repo URL 與使用者一開始提供的 `<repo-url>` 完全一致，且目標暫存資料夾名稱對應解析出的 `<repo-name>`。若兩者皆符合，agent 可視為預期操作並允許執行。

### 5. 建立正式結構

clone 成功後，agent 應建立：

```text
external-source/<source-name>/
├─ README.md
├─ source-links.md
├─ LICENSE-<source-name>.md
├─ notes/
│  ├─ reading-notes.md
│  ├─ open-questions.md
│  └─ .gitkeep
├─ extracted/
│  ├─ summary.md
│  ├─ concepts.md
│  ├─ checklist.md
│  └─ .gitkeep
└─ upstream/
   └─ <repo-name>/
      └─ 原始 clone 內容
```

若 upstream 找不到 license 檔，可以不建立 `LICENSE-<source-name>.md`，並在 `source-links.md` 標記 license 尚未確認。

### 6. Markdown 初始化

`README.md` 應包含：

- source name
- repository URL
- source status checklist
- expected extraction direction

`source-links.md` 應包含：

- Official repository
- Documentation
- Article
- License
- Related references

`notes/reading-notes.md`、`notes/open-questions.md`、`extracted/summary.md`、`extracted/concepts.md`、`extracted/checklist.md` 應建立為可後續填寫的空模板。

### 7. License 掃描

agent 應在 upstream repo 中搜尋常見 license 檔：

- `LICENSE`
- `LICENSE.md`
- `LICENSE.txt`
- `COPYING`

若找到，應在來源工作區中建立或更新 license notice，記錄原始 license 檔位置與 attribution。

若找不到，應在 `source-links.md` 或 `open-questions.md` 標記 `License: Unknown / not found yet`。

### 8. `.gitignore` 同步

agent 應確認根目錄 `.gitignore` 包含 upstream ignore 規則：

```gitignore
# External source upstream clones
/external-source/*/upstream/*
!/external-source/*/upstream/.gitkeep
```

這個規則應避免 upstream clone 的大量原始檔被本 repo 追蹤，同時保留整理用目錄結構。

### 9. 驗證

agent 應驗證：

- 正式來源工作區存在
- upstream clone 成功移入正確位置
- markdown 檔可用 UTF-8 正常讀取
- `.gitignore` 沒有忽略來源工作區的整理文件
- `git status --short` 不顯示 upstream repo 的大量原始檔

## Agent 行為規則

若 clone 前置檢查失敗，agent 應停止，不建立正式目錄。

若前置檢查失敗原因是 private repo authentication failure，agent 應回報「terminal Git 認證不可用或 token 權限不足」，並提醒 browser 登入狀態不等於 Git HTTPS 認證。

若 clone 到暫存位置失敗，agent 應停止，不建立正式目錄。

若搬移暫存 clone 到正式目錄時因權限被拒絕而需要 escalation，agent 應先確認來源資料夾與目的資料夾都對應本次解析出的 `<repo-name>` 與 `<source-name>`。若符合，agent 可視為預期操作並允許執行。

若正式目錄搬移或建置中途失敗，且無法用上述預期操作規則完成，agent 應回報已建立的檔案與可能需要人工清理的位置。

agent 不應刪除既有 `external-source/<source-name>/`，除非使用者明確要求。

agent 不應把 upstream repo 內容複製到 `notes/` 或 `extracted/`；這些目錄只放本專案整理後的內容。

## 標準 Prompt

請協助將以下 Git repository 匯入 `external-source/`：

```text
<repo-url>
```

可選來源命名：

```text
<source-name>
```

請依照 `external-source/README.md` 建立來源工作區。若未提供來源命名，請使用 repo name。

請先確認 `git ls-remote` 或等價檢查可成功；若無法確認或 clone 失敗，請停止並回報，不要建立半套目錄。

clone 成功後，請建立 README、source-links、notes、extracted、upstream 結構與 `.gitkeep`，掃描 license，並同步確認根目錄 `.gitignore` 已排除 `/external-source/*/upstream/*`。

## 建議輸出格式

### Import Summary

- Repo URL:
- Source name:
- Repo name:
- Target path:

### Clone Check

- Result:
- Notes:

### Files Created

- ...

### Gitignore

- Updated:
- Rule:

### License

- Detected:
- Location:
- Notes:

### Validation

- ...

### Blockers

- ...
