# External Source

`external-source/` 用來存放、記錄與整理來自外部專案、文章、文件、框架或研究資料的來源資訊。

這個目錄的目的不是直接把外部內容變成專案核心邏輯，而是作為「外部知識輸入層」，讓後續可以再逐步萃取成：

- notes：閱讀筆記
- extracted：整理後的重點
- knowledge：可長期保存的知識條目
- playbook：可操作流程
- skill：可被 Agent / Codex / Copilot 類工具執行的短規則
- prompt：可重用提示詞
- checklist：任務檢查表

---

## Purpose

這個目錄主要負責三件事：

1. **保存來源脈絡**

   記錄外部資料的來源、作者、授權方式、相關連結與閱讀重點。

2. **隔離外部知識與本專案產物**

   外部資料先放在 `external-source/` 中整理，避免尚未驗證或尚未消化的內容直接混入核心架構。

3. **支援後續萃取流程**

   當外部資料被理解、整理、驗證後，可再轉換為本專案內部的 playbook、skill、knowledge 或 prompt。

---

## Suggested Structure

每一個外部來源建議使用獨立資料夾。來源資料夾本身只放本專案的整理材料；未改寫的原始 clone 或下載內容放在 `upstream/` 底下。

```text
external-source/
├─ README.md
└─ <source-name>/
   ├─ README.md
   ├─ source-links.md
   ├─ notes/
   │  ├─ reading-notes.md
   │  └─ open-questions.md
   ├─ extracted/
   │  ├─ summary.md
   │  ├─ concepts.md
   │  └─ checklist.md
   └─ upstream/
      └─ clone/
         └─ <upstream-project>/
            └─ ...
```

範例：

```text
personal-ai-runtime/
└─ external-source/
   └─ WFGY/
      ├─ README.md
      ├─ source-links.md
      ├─ notes/
      ├─ extracted/
      └─ upstream/
         └─ clone/
            └─ WFGY/
               └─ ...
```

如果需要保留 license 或 attribution，可放在來源資料夾根目錄，例如：

```text
external-source/
└─ <source-name>/
   ├─ README.md
   ├─ source-links.md
   ├─ LICENSE-<source-name>.md
   ├─ notes/
   ├─ extracted/
   └─ upstream/
      └─ clone/
```

---

## Directory Meaning

### `README.md`

說明這個外部來源與 `personal-ai-runtime` 的關係。

內容可以包含：

- 這個來源是什麼
- 為什麼值得研究
- 和本專案哪個模組有關
- 預計如何萃取或使用

---

### `source-links.md`

記錄原始來源連結。

建議包含：

```md
# Source Links

- Official repository:
- Documentation:
- Article:
- License:
- Related references:
```

---

### `LICENSE-<source-name>.md`

記錄該外部來源的授權資訊。

如果外部來源有明確 license，應保留或連結原始授權內容。

如果後續 playbook / skill / prompt 有使用該來源的概念、結構、片段或改寫內容，應在產物中加入 attribution。

---

### `notes/`

閱讀過程中的原始筆記。這裡可以用多個檔案拆分主題，不必塞進單一 `notes.md`。

這裡可以保留較鬆散的觀察，例如：

- 初步理解
- 不確定處
- 可疑點
- 值得深挖的概念
- 和現有專案的可能關聯

---

### `extracted/`

放置已經初步整理過的內容。

這裡的內容應該比 `notes/` 更結構化，適合後續轉換成：

- `agent-playbooks/`
- `agent-skills/`
- `knowledge/`
- `reasoning/`
- `prompts/`

---

### `upstream/`

放置未改寫的原始來源內容，例如 git clone、crawl 結果、下載的原始文件或第三方 snapshot。

建議規則：

- `upstream/clone/` 放完整 Git repo clone
- `upstream/crawl/` 可放網站或文件 crawl 結果
- `upstream/snapshot/` 可放單次保存的文章、PDF、頁面或資料集
- 不在 `upstream/` 內直接寫本專案整理筆記
- 本專案的理解、萃取、轉換結果放在 `notes/` 或 `extracted/`
- 若 Git repo 來源需要更新，優先更新 `upstream/clone/<upstream-project>/`

---

## Extraction Flow

建議的萃取流程如下：

```text
external source
  ↓
notes
  ↓
extracted summary
  ↓
knowledge / playbook
  ↓
skill / prompt / checklist
```

也就是：

```text
外部來源
  ↓
閱讀筆記
  ↓
萃取摘要
  ↓
內部知識或操作流程
  ↓
可被 Agent 使用的規則或提示詞
```

---

## Relationship with Other Directories

### `external-source/`

外部資料的來源記錄與初步整理區。

適合放：

- 原始連結
- 授權資訊
- 閱讀筆記
- 摘要
- 尚未正式納入專案架構的研究資料

---

### `knowledge/`

已經理解並整理成穩定知識的內容。

適合放：

- 框架介紹
- 技術概念
- 長期參考資料
- glossary
- architecture notes

---

### `agent-playbooks/`

已經可以被人類或 Agent 依步驟執行的流程。

適合放：

- debug flow
- migration flow
- review flow
- refactoring flow
- RAG troubleshooting flow

---

### `agent-skills/`

從 playbook 萃取出的短版、命令式規則。

適合放：

- Codex skill
- Claude Code skill
- Copilot agent instruction
- task-specific operating rule

---

### `reasoning/`

任務判斷、決策、preflight、risk review 相關規則。

適合放：

- preflight protocol
- decision protocol
- verification rule
- ambiguity handling rule
- escalation rule

---

## Attribution Guideline

當外部來源被轉換成本專案內容時，應視使用程度加入 attribution。

### 只是概念啟發

```md
## Source / Attribution

This document is inspired by the following external source:

- Source:
- License:
```

### 有整理、改寫或沿用結構

```md
## Source / Attribution

This document adapts concepts and structure from the following external source:

- Source:
- Original project / author:
- License:
```

### 有直接引用或複製原文

應保留原始授權聲明，並清楚標示引用範圍。

```md
## License Notice

Parts of this document include or adapt materials from:

- Source:
- Original project / author:
- License:

Original copyright and license notices belong to the original project.
```

---

## Recommended Rules

1. 不直接把外部來源當成本專案核心規則。
2. 先記錄來源，再整理筆記，再萃取成內部產物。
3. 所有外部來源都應記錄 source link。
4. 有 license 就保留 license。
5. 有改寫、引用、整理外部內容，就加 attribution。
6. 不確定授權時，不複製原文，只保留摘要與連結。
7. 若內容要轉成 playbook 或 skill，應補上來源說明。
8. 萃取後的內容應使用本專案自己的語氣、格式與命名規則。
9. 若外部來源內容過於抽象，應先轉成 glossary 或 checklist。
10. 若外部來源能對應到實作流程，再轉成 playbook。

---

## Example: WFGY

WFGY 可以用一個來源工作區包起來，原始 clone 放在 `upstream/clone/WFGY/`：

```text
external-source/WFGY/
```

初期整理重點：

```text
personal-ai-runtime/
└─ external-source/
   └─ WFGY/
      ├─ README.md
      ├─ source-links.md
      ├─ notes/
      │  ├─ reading-notes.md
      │  └─ open-questions.md
      ├─ extracted/
      │  ├─ problem-map.md
      │  └─ goal-compiler.md
      └─ upstream/
         └─ clone/
            └─ WFGY/
               └─ ... 原始 clone 內容
```

後續可能萃取成：

```text
agent-playbooks/rag-debug-with-wfgy-problem-map.md
agent-skills/rag-debug-problem-map/SKILL.md
reasoning/preflight-protocol/wfgy-inspired-goal-compiler.md
knowledge/ai-frameworks/wfgy.md
```

---

## Naming Convention

建議使用 kebab-case：

```text
external-source/
├─ WFGY/
├─ ai-engineering-hub/
├─ karpathy-agent-skills/
└─ claude-code-mini-course/
```

若來源是正式專案名稱，可保留原大小寫，例如：

```text
WFGY/
CrewAI/
LangGraph/
```

但內部檔案仍建議使用 kebab-case：

```text
problem-map-notes.md
goal-compiler-summary.md
rag-failure-modes.md
agent-debug-checklist.md
```

---

## Status

`external-source/` 是研究與萃取區，不代表其中所有內容都已經被本專案採用。

每個外部來源建議標示目前狀態：

```md
## Status

- [ ] Collected
- [ ] Reading
- [ ] Notes created
- [ ] Extracted
- [ ] Converted to knowledge
- [ ] Converted to playbook
- [ ] Converted to skill
```

---

## Core Principle

外部來源不是直接拿來使用，而是經過理解、整理、驗證後，轉換成符合 `personal-ai-runtime` 架構的可重用知識。

```text
collect → understand → extract → adapt → verify → reuse
```
