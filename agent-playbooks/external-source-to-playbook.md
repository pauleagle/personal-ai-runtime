# External Source To Playbook

## 目的

External Source To Playbook 是將 `external-source/` 中已收集、閱讀或初步萃取的外部資料，整理成 `agent-playbooks/<name>.md` 的流程。

它以 `prompt-to-playbook` 的抽象方法為基礎，但額外強調來源追蹤、license、attribution、改寫邊界，以及避免把外部內容未消化地搬進本專案。

## 核心原則

外部來源不是 playbook。

Playbook 應該是本專案理解、改寫、驗證後的可操作流程，而不是外部 README、文章、框架說明或 repo 內容的摘要複製。

從外部來源萃取 playbook 時，應保留：

- 外部來源啟發出的可重複操作流程
- 適用與不適用時機
- agent 可執行的行為規則
- 必要的檢查清單與輸出格式
- 來源、作者、license 與 attribution 資訊

若授權、來源或使用範圍不清楚，應保守處理：優先保留連結、摘要與本專案自己的改寫，不直接複製原文。

## 適用時機

- `external-source/<source-name>/` 中已有來源連結、筆記或萃取摘要
- 外部來源中的方法、流程或框架已足夠穩定，可轉成本專案可執行 playbook
- 使用者要求將外部專案、文章、文件、研究資料或 repo 內容整理成 playbook
- 需要把 `external-source/<source-name>/extracted/` 的內容轉成 `agent-playbooks/<name>.md`
- 需要建立帶有 source attribution 的 playbook，之後再視需要萃取成 skill

## 不適用時機

- 外部來源只剛收集，尚未閱讀或理解
- 來源、作者、license 或連結完全不明，且使用者要求直接搬運內容
- 外部內容只是概念背景，尚未形成可操作流程
- 使用者只是要建立一般 prompt、skill、knowledge 條目，而不是 playbook
- 任務需要保留原文逐字引用，但授權條件尚未確認

## 整理規則

整理外部來源時，agent 應先確認：

1. 來源位於哪個 `external-source/<source-name>/` 工作區
2. 是否有 `source-links.md`
3. 是否有 license 資訊或 `LICENSE-<source-name>.md`
4. 是否有 `notes/` 或 `extracted/` 可作為整理基礎
5. 原始 clone 或 snapshot 是否放在 `upstream/`
6. 目標 playbook 要解決什麼可重複任務
7. 哪些內容是外部來源的概念啟發，哪些內容是本專案的改寫流程

agent 應移除或改寫：

- 外部來源中的宣傳語、專案定位或非本專案需要的背景
- 無法確認授權的長段原文
- 只適用於原始專案環境的路徑、命令、角色或假設
- 尚未理解或驗證的結論

agent 應保留或補上：

- 原始來源連結
- 原始專案或作者
- license 或授權狀態
- 本 playbook 與來源的關係，例如 inspired by、adapts concepts、includes quoted material
- 本專案自己的使用範圍、限制與驗證方式

## Attribution 格式

若外部來源只是概念啟發，playbook 可加入：

```md
## Source / Attribution

This playbook is inspired by the following external source:

- Source:
- Original project / author:
- License:
```

若 playbook 改寫或沿用外部來源的結構，應使用：

```md
## Source / Attribution

This playbook adapts concepts and structure from the following external source:

- Source:
- Original project / author:
- License:
```

若包含直接引用或複製內容，應清楚標示引用範圍並保留 license notice：

```md
## License Notice

Parts of this playbook include or adapt materials from:

- Source:
- Original project / author:
- License:

Original copyright and license notices belong to the original project.
```

## Agent 行為規則

agent 在執行 external-source-to-playbook 時，應先判斷使用者要的是：

1. 只評估外部來源是否適合轉成 playbook
2. 建立新的 playbook
3. 更新既有 playbook
4. 將多個外部來源合併成同一個 playbook

若使用者只要求建立 playbook，不應自動建立一般任務 skill。

若新建立的 playbook 不存在於 `agent-playbooks/README.md` 的 Playbook / Skill 對照表中，agent 應加入新列，Skill 欄位填 `-`，狀態標記為 `draft`。

若更新的 playbook 已存在於對照表，且已對應 skill，agent 應將狀態調整為 `skill-extracted`，表示 playbook 已變更但尚未重新複查同步。

若來源資訊不足，agent 應先補齊或列出缺口，不應把未授權或未歸因的外部內容直接整理成正式 playbook。

若必須引用外部原文，agent 應保持引用範圍最小，並明確標示來源與 license。

## 標準 Prompt

請協助將以下 `external-source/` 來源整理成 playbook。

請將它抽象成 `agent-playbooks/<name>.md`，並符合 `agent-playbooks/README.md` 的風格與結構。

請注意：

1. 只建立或更新 playbook
2. 不要自動萃取成一般任務 skill
3. 先檢查來源連結、作者、license、notes、extracted 與 upstream 狀態
4. 保留可重複使用的目的、原則、適用時機與行為規則
5. 將外部內容改寫成本專案自己的可操作流程
6. 避免直接複製未確認授權的長段原文
7. 補上 Source / Attribution 或 License Notice
8. 如有必要，更新 `agent-playbooks/README.md` 的對照表
9. 新增 playbook 時標記為 `draft`

## 建議輸出格式

### Source Assessment

外部來源狀態：

- Source:
- Author / project:
- License:
- Available notes:
- Available extracted material:
- Upstream snapshot:

### Proposed Playbook

建議建立或更新的 playbook：

- ...

### Generalized Rules

已抽象出的通用規則：

- ...

### Attribution Plan

來源標註方式：

- ...

### Removed Or Rewritten Details

已移除或改寫的外部來源細節：

- ...

### Files To Change

預計影響的檔案：

- ...

### Open Questions

需要確認的地方：

- ...
