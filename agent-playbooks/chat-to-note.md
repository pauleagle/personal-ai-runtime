# Chat To Note

## 目的

Chat To Note 是將聊天回答、AI 產生的草稿、貼上的 Markdown 片段或一次性整理稿，轉成乾淨、可維護 note 的流程。

它適合用在 `external-source/*/notes/`、研究筆記、reading note、workflow comparison note、concept note 或個人知識整理檔。目標不是保留完整聊天過程，而是萃取可長期閱讀、可追溯來源、可後續轉成 playbook / skill / knowledge 的筆記。

## 核心原則

Note 應保存「可重用理解」，不是保存「聊天殘留」。

整理時應保留：

- 來源與脈絡
- 一句話摘要
- 核心概念
- 對本專案的關聯
- 可萃取方向
- 使用限制、授權或 attribution 邊界
- 後續問題或待確認事項

整理時應移除：

- 「建議檔名」、「以下整理成」、「可以直接存成」等回答包裝語
- 外層 Markdown code fence，例如「四個反引號加 `md` 的包裝 fence」
- `contentReference`、`oaicite`、模型引用殘留或破損腳註
- 尾端自動生成的 `[1]: ...` reference list，除非它是 note 本身需要保留的來源索引
- 聊天式寒暄、重複解釋、過度發散段落
- 單次任務路徑、日期、環境細節，除非它們是來源追溯必要資訊
- 大量原文複製，特別是來自 restricted、paid-course、非開源或授權不明來源

## 適用時機

- 使用者要求整理一份 note、reading note、研究筆記或外部來源筆記
- 檔案內容來自 ChatGPT / Claude / Codex 的回答草稿
- Markdown 檔中有聊天包裝語、外層 code fence、引用殘留或破損格式
- note 混合了來源摘要、個人理解、後續萃取方向，需要重排成穩定結構
- external-source 筆記需要保留來源、license、attribution 或使用限制
- 使用者想把成功的聊天整理流程抽成可重複流程

## 不適用時機

- 使用者要求逐字保存聊天紀錄或 transcript
- 檔案是正式規格、API contract、法律文件或授權文字，不能自由改寫
- 任務是 changelog 正規化，應改用 changelog normalization 流程
- 任務是把 prompt 變 playbook，應改用 `prompt-to-playbook`
- 任務是把 playbook 萃取成 skill，應改用 `playbook-to-skill`
- 來源授權不允許摘要、改寫或再利用，且使用者未提供授權依據

## 工作流程

### 1. 讀取與保存狀態確認

先讀取目標檔案，確認磁碟上的內容與使用者描述一致。

若 IDE 顯示內容，但 `Get-Content` 讀到空檔或檔案長度為 0，應提醒使用者可能尚未存檔，並請使用者儲存後再處理。不要在不確定時用空檔覆蓋使用者尚未保存的內容。

建議檢查：

```powershell
Get-Item <note-path> | Select-Object FullName,Length,LastWriteTime
Get-Content -Raw -Encoding UTF8 <note-path>
```

### 2. 判斷 note 類型

先判斷這份 note 應該成為哪一類：

- reading note：外部來源閱讀筆記
- concept note：概念整理
- comparison note：兩個 workflow / framework 的對照
- extraction note：準備萃取成 playbook / skill / checklist 的中繼筆記
- restricted source note：只能保留高階理解與私人對照，不可複製原文

### 3. 清理聊天殘留

移除聊天回答包裝與模型輸出殘留。

常見清理目標：

```text
建議檔名：
下面整理成：
以下是：
四個反引號加 md 的外層 Markdown fence
::contentReference[...]
:contentReference[...]
oaicite
[1]: https://...
```

若 reference links 是 note 需要的來源索引，可以改寫到 `## 來源` 或 `## References`，不要保留在孤立尾巴。

### 4. 重建 note 結構

依內容選擇精簡、穩定的結構。一般建議：

```md
# <Note Title>

## 來源

## 一句話摘要

## 核心理解

## 核心概念

## 對 personal-ai-runtime 的對應

## 可萃取方向

## 風險與注意事項

## 後續問題
```

若來源有授權或使用限制，應將 `## 來源` 擴充為：

```md
## 來源與使用限制
```

### 5. 保留可萃取價值

整理後的 note 應回答：

- 這個來源或概念在說什麼？
- 它對 personal-ai-runtime 有什麼價值？
- 哪些內容可轉成 playbook、skill、checklist、knowledge 或 prompt？
- 哪些內容只能留作 private note，不適合公開或轉用？
- 有哪些 open questions 或需要 human decision 的地方？

### 6. 授權與來源邊界檢查

若 note 位於 `external-source/`，應檢查同來源工作區的 `source-links.md`、license notice、`AGENTS.md`、`NOTICE`、`TERMS` 或 open questions。

若來源是 restricted、paid-course、授權不明或禁止再散布：

- 只保留高階理解、個人對照與萃取方向
- 不複製大量原文、範例、課程內容或可替代原材料的細節
- 在 note 前段加入使用限制提醒
- 若要萃取成公開 playbook / skill / knowledge，先確認授權與 attribution 邊界

### 7. 驗證

整理後應驗證：

- 檔案可用 UTF-8 正常讀取
- 沒有殘留 `contentReference`、`oaicite`、外層 code fence 或破損 footnote
- 標題與章節層級合理
- note 不再像聊天回答，而像可長期維護的筆記
- 若有來源限制，已保留限制提醒

可用：

```powershell
Select-String -Path <note-path> -Encoding UTF8 -Pattern 'contentReference|oaicite|````md|建議檔名'
```

## Agent 行為規則

agent 應先讀檔再改，不應憑 IDE 截圖或使用者選取片段直接重寫整份 note。

agent 應在檔案為空但使用者表示有內容時，先提醒可能尚未儲存，而不是立即覆蓋。

agent 應保留使用者的核心觀點與本專案對應，不應把 note 改成泛泛而談的摘要。

agent 應移除聊天殘留，但不要移除必要來源、license、attribution、限制聲明或 open questions。

agent 不應把 restricted source 的原文複製到整理後 note，也不應把 restricted note 直接升級成公開 playbook / skill。

agent 不應自動搬移 note 檔案位置，除非使用者明確要求。若發現路徑很怪，只能回報建議或詢問。

agent 應使用繁體中文整理中文 note，除非既有文件明確使用英文或使用者指定其他語言。

## 標準 Prompt

請協助整理以下 note 檔案：

```text
<note-path>
```

請先確認檔案已儲存且磁碟內容可讀。若檔案為空但我描述它有內容，請提醒我可能尚未存檔，不要直接覆蓋。

整理時請移除聊天回答包裝語、外層 Markdown code fence、`contentReference` / `oaicite` 殘留、破損 footnote 與不必要的發散段落。

請保留來源、核心理解、對 personal-ai-runtime 的對應、可萃取方向、風險與後續問題。若來源有授權或使用限制，請在 note 前段保留限制提醒，不要複製大量原文。

請不要搬移檔案位置，除非我另外要求。

## 建議輸出格式

### Note Cleanup Summary

- Note path:
- Note type:
- Source / license constraints:

### Removed

- ...

### Preserved / Rebuilt

- ...

### Validation

- UTF-8 readback:
- Residual marker scan:
- Remaining risks:

### Follow-up

- Candidate extraction:
- Open questions:
