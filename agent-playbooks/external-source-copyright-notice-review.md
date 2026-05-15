# External Source Copyright Notice Review

## 目的

External Source Copyright Notice Review 是針對已匯入 `external-source/` 的外部來源，補查可能被一般 license 掃描漏掉的版權、授權、重用限制與公開分享限制。

它補足 `External Source Repo Import` 的根目錄 license 掃描：當 upstream repo 沒有 `LICENSE`、`COPYING` 等標準授權檔，或 agent 在 README、AGENTS、CLAUDE、rules、docs 中發現疑似版權限制時，應使用本流程進一步確認並更新來源 metadata。

本 playbook 不是法律意見。它的目標是讓來源工作區清楚記錄「已發現的授權聲明、限制、待確認事項與萃取邊界」。

## 核心原則

沒有標準 `LICENSE` 不等於沒有版權或重用限制。

授權 notice 可能出現在 agent-readable files、README、課程說明、文件頁、子目錄規則、範例檔註解或作者自訂 notice 中。

掃描結果應先視為 candidate notice。只有在確認該內容是來源作者對本 repo、資料夾、課程材料、文件或特定子目錄的使用限制時，才更新 `LICENSE-<source-name>.md`、`source-links.md` 或 `open-questions.md`。

若授權範圍不清楚，應保守處理：不複製原文、不公開散布、不轉成可外流的 playbook、skill、prompt 或 knowledge；先記錄限制與待確認問題。

## 適用時機

- `External Source Repo Import` 沒有找到標準 license 檔，並提示可能需要補查
- 已匯入的 `external-source/<source-name>/` 仍標記 `License: Unknown / not found yet`
- upstream repo 有 `AGENTS.md`、`CLAUDE.md`、`.cursor/rules/`、`README.md`、`NOTICE`、`TERMS` 或 docs 可能包含使用限制
- 使用者或 agent 發現「付費課程、禁止公開、不得轉發、商業使用限制、保留所有權利」等文字
- 準備從外部來源萃取成 notes、playbook、skill、prompt、knowledge 或 RAG source 前，需要確認 reuse boundary
- 外部來源是 private repo、付費教材、課程材料、內部文件、商業文件或作者自訂授權內容

## 不適用時機

- 使用者只要求快速查看外部 repo，且不建立 `external-source/` metadata
- 標準 license 已清楚存在，且沒有任何額外 notice 或子目錄限制
- 任務是正式法律審查、合約判讀或授權談判
- 使用者要求繞過、忽略或淡化來源的公開分享限制
- 來源內容不會被保存、萃取、改寫或納入本專案任何長期產物

## 工作流程

### 1. 定位來源工作區

agent 應先確認：

- source name
- upstream repo path，例如 `external-source/<source-name>/upstream/clone/<repo-name>/`
- `source-links.md` 是否存在
- `LICENSE-<source-name>.md` 是否存在
- `notes/open-questions.md` 與 `extracted/checklist.md` 是否存在
- 已匯入 commit、snapshot 或來源日期

若來源工作區不存在，應先要求使用者執行或補齊 external-source import。

### 2. 掃描標準 license 與 notice 檔

agent 應掃描常見授權與 notice 檔名：

- `LICENSE`
- `LICENSE.md`
- `LICENSE.txt`
- `COPYING`
- `NOTICE`
- `NOTICE.md`
- `TERMS`
- `TERMS.md`
- `COPYRIGHT`
- `COPYRIGHT.md`

若找到，應記錄原始路徑、範圍與摘要。若不同子目錄有不同 notice，應保留子目錄層級，不要只寫成全 repo 單一授權。

### 3. 掃描 agent-readable 與文件入口

除了標準 license 檔，agent 應掃描可能被 AI agent 或使用者優先閱讀的檔案：

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.cursorrules`
- `.cursor/rules/*`
- `.github/copilot-instructions.md`
- `README.md`
- `docs/**/*.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

這些檔案可能不是傳統 license，但可能包含公開發布、引用、二次散布、商業使用、AI agent 操作或資料外流限制。

### 4. 關鍵字掃描

agent 應用關鍵字找出 candidate notices。

英文關鍵字可包含：

- `copyright`
- `license`
- `licence`
- `all rights reserved`
- `permission`
- `redistribution`
- `commercial use`
- `non-commercial`
- `public`
- `private`
- `paid course`
- `confidential`
- `terms`
- `attribution`
- `DMCA`

中文關鍵字可包含：

- `版權`
- `授權`
- `保留所有權利`
- `禁止`
- `不得`
- `公開`
- `轉發`
- `轉載`
- `二次散布`
- `商業使用`
- `付費課程`
- `個人學習`
- `書面授權`
- `註明出處`

掃描結果應以「候選」方式整理，不應只因關鍵字存在就判定為正式授權條款。

### 5. 語意確認

agent 應逐項判斷 candidate notice：

1. 這是來源作者對本 repo、材料或子目錄的限制嗎？
2. 它是正式授權、補充 notice、操作提醒、範例文字，還是第三方內容引用？
3. 適用範圍是全 repo、特定資料夾、特定檔案，還是不明？
4. 它限制的是複製、公開分享、再散布、商業使用、衍生作品、AI agent 操作，還是 attribution？
5. 是否與標準 license 衝突或補充標準 license？
6. 是否需要保守標記為 `Needs confirmation`？

若語意不明，不要自行放寬限制。應在 `notes/open-questions.md` 中記錄待確認問題。

### 6. 更新來源 metadata

確認 notice 後，agent 應視情況更新：

- `source-links.md`
- `LICENSE-<source-name>.md`
- `notes/open-questions.md`
- `extracted/checklist.md`
- `README.md`

建議更新方式：

- `source-links.md` 記錄原始 notice 檔案路徑與 local license notice
- `LICENSE-<source-name>.md` 記錄來源、notice file、copyright holder、reuse scope、限制摘要、reviewed commit
- `notes/open-questions.md` 記錄未確認的範圍、衝突或子目錄 notice
- `extracted/checklist.md` 加入「萃取前確認該範圍 notice」或將已完成項目打勾
- `README.md` 在 Notes 中保留簡短警示，避免後續讀者誤以為是 open source

### 7. 設定萃取邊界

若來源有公開分享或再散布限制，agent 應在 metadata 中明確標示：

- 是否可做私有閱讀筆記
- 是否可萃取短摘要
- 是否可改寫為內部 playbook / skill
- 是否禁止長段原文引用
- 是否禁止公開發布 derived material
- 是否需要 attribution
- 是否需要 written permission

如果無法確認，預設只做最小摘要與來源連結，不複製原文。

## Agent 行為規則

agent 不應把 candidate notice 直接當成法律結論；應標記來源路徑、判斷依據與不確定處。

agent 不應因為找不到標準 `LICENSE` 就把來源視為可自由使用。

agent 不應把 upstream 原文長段複製到 `notes/`、`extracted/`、playbook、skill、prompt 或 knowledge，除非授權清楚允許且引用範圍必要。

agent 應優先更新 metadata，而不是修改 upstream clone。

agent 不應自動刪除或覆蓋既有 `LICENSE-<source-name>.md`；若已有 notice，應合併、補充或標記衝突。

若 notice 指出禁止公開散布，agent 應拒絕任何把 upstream 內容 push 到 public repo、public gist、public note 或公開雲端連結的請求。

若使用者要求匯出、公開、分享或轉成公開文件，而 notice 限制不清楚，agent 應先停下並要求確認授權範圍。

## 與 External Source Repo Import 的銜接

`External Source Repo Import` 可在下列情況提醒執行本 playbook：

- 沒有找到標準 license 檔
- 只找到模糊的 `License: Unknown / not found yet`
- repo 含有 `AGENTS.md`、`CLAUDE.md`、`.cursor/rules/` 或其他 agent-readable files
- repo 看起來是 private、paid-course、internal、training material 或商業內容
- 初始 license 掃描發現疑似 reuse restriction，但尚未語意確認

匯入流程不必完整執行本 playbook；它可以只留下 reminder 或 open question，讓使用者稍後手動觸發補查。

## 標準 Prompt

請協助針對以下 `external-source/` 來源執行 copyright notice review：

```text
external-source/<source-name>/
```

請檢查標準 license 檔、agent-readable files、README/docs 與版權/授權/公開分享限制關鍵字。

請把掃描結果先整理為 candidate notices，再判斷哪些是來源作者對此 repo、資料夾或材料的實際限制。

請更新必要的 metadata：

1. `source-links.md`
2. `LICENSE-<source-name>.md`
3. `notes/open-questions.md`
4. `extracted/checklist.md`
5. 如有必要，更新來源 `README.md`

請不要修改 upstream clone，也不要把 upstream 原文長段複製到整理文件。若授權範圍不清楚，請保守標記為待確認。

## 建議輸出格式

### Review Summary

- Source:
- Upstream path:
- Reviewed commit / snapshot:
- Result:

### Candidate Notices

- Path:
- Type:
- Scope:
- Notes:

### Confirmed Notices

- Path:
- Scope:
- Restriction summary:
- Attribution / copyright holder:

### Metadata Updates

- `source-links.md`:
- `LICENSE-<source-name>.md`:
- `notes/open-questions.md`:
- `extracted/checklist.md`:
- `README.md`:

### Extraction Boundary

- Private notes:
- Short summaries:
- Derived playbooks / skills:
- Public sharing:
- Attribution:

### Open Questions

- ...

### Validation

- ...
