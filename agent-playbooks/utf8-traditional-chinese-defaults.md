# UTF-8 Traditional Chinese Defaults

## 目的

這份 playbook 將「文件讀寫預設 UTF-8、繁中優先、PowerShell 用 `-Encoding UTF8`」整理成可重用的文字處理規範。

它適用於 agent 需要建立、讀取、更新、整理或轉換文字文件時，避免因預設編碼、語言變體或 shell 行為造成亂碼、語氣不一致，或在 Windows PowerShell 環境中寫出非預期的檔案編碼。

## 問題脈絡

跨平台或 Windows 優先的工作環境中，文字檔常因工具預設值不同而產生問題：

- PowerShell 指令未指定編碼，可能寫出和預期不同的檔案格式。
- 文件內容混用簡中、繁中或英文，造成專案語言風格不一致。
- 讀取檔案時未確認編碼，容易把原本正確的 UTF-8 內容誤判成亂碼。
- 更新文件時只改內容、不注意輸出編碼，會讓之後的 diff、渲染或自動化工具變得不穩定。

## 使用時機

- 新增或更新 Markdown、YAML、JSON、文字設定檔、prompt、playbook、skill 文件。
- 在 Windows PowerShell 中使用 `Get-Content`、`Set-Content`、`Add-Content`、`Out-File`、`Export-*` 類指令處理文字檔。
- 專案或使用者沒有另行指定語言時，需要決定文件的預設中文變體。
- 發現終端輸出、diff、README、文件片段疑似出現亂碼時。
- 將一次性 prompt、規範、流程說明或知識文件整理成可長期維護的文字檔時。

## 不適用情境

- 既有檔案明確使用其他編碼，且該編碼是外部工具或舊系統契約的一部分。
- 使用者明確要求簡中、英文或其他語言風格。
- 二進位檔、圖片、壓縮檔或不應以文字方式處理的資產。
- 需要保留原始檔案位元組完全不變的稽核、鑑識或 checksum 工作。
- 專案已經有更具體的 formatter、linter 或文件產生器規則，且該規則與本 playbook 衝突。

## 標準做法

預設以 UTF-8 讀寫文字檔。除非使用者或專案明確指定其他編碼，agent 不應依賴 shell、作業系統或工具的隱含預設值。

以繁體中文作為中文輸出的優先選項。若文件原本已使用繁中，延續原有用語和語氣；若文件混用語言，優先維持使用者指定的語言，沒有指定時才統一成繁中。

使用 PowerShell 讀寫文字檔時，應在會輸出檔案的命令加上 `-Encoding UTF8`，尤其是：

- `Set-Content -Encoding UTF8`
- `Add-Content -Encoding UTF8`
- `Out-File -Encoding UTF8`
- `Export-Csv -Encoding UTF8`

讀取檔案時若需要確認或避免誤判，也應使用 `Get-Content -Encoding UTF8`，或改用已知會保留 UTF-8 的工具與 API。

### Skill validation 的 script-first 檢查

當要驗證 `agent-skills/<skill>/SKILL.md`，或遇到 Windows 預設編碼造成的 validator 失敗時，應先使用 UTF-8-safe validator：

```powershell
python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\<skill-name>
```

需要給後續流程或 agent 消費時，可加上 `--json`：

```powershell
python agent-skills\utf8-traditional-chinese-defaults\scripts\validate_skill_utf8.py agent-skills\<skill-name> --json
```

這個檢查會明確用 UTF-8 讀取 `SKILL.md`，並把 decode error 回報為驗證結果，而不是讓 shell 或 Python 的平台預設編碼決定成敗。LLM 判斷應在這個 deterministic evidence 之後進行，用來分辨是檔案編碼問題、終端顯示問題、validator 限制，或 frontmatter 內容本身錯誤。

手動編輯 repo 檔案時，優先使用既有安全編輯工具與專案流程；批次轉換或格式化前，先確認目標檔案範圍，避免把不相關檔案改成不同換行、編碼或語言風格。

## Agent 行為準則

在建立或修改文字檔前，agent 應先判斷是否有既有語言和編碼慣例。若檔案附近已有繁中文件，新增內容應跟隨繁中；若附近文件主要是英文，除非使用者要求繁中，應避免硬性改寫既有英文內容。

在 PowerShell 中寫檔時，agent 應明確指定 `-Encoding UTF8`。如果使用 `apply_patch` 或其他專用編輯工具，仍應在心智模型中以 UTF-8 作為輸出預設，並避免引入非必要的編碼轉換。

遇到疑似亂碼時，agent 不應直接大規模重寫文件。應先確認亂碼是顯示問題、讀取編碼問題，還是檔案內容本身已損壞，再決定是否修復。

若使用者要求「整理文件」、「抽成 playbook」、「建立 skill」、「更新 README」等文件工作，agent 應把 UTF-8 和繁中優先視為預設背景規範。

若必須偏離 UTF-8 或繁中優先，agent 應在回覆中簡短說明原因。

## 標準 Prompt

請依照以下文件處理預設執行這次任務：

1. 文字檔讀寫預設使用 UTF-8。
2. 中文內容預設以繁體中文為優先，除非使用者或既有文件明確指定其他語言。
3. 使用 PowerShell 讀寫或輸出文字檔時，請明確加上 `-Encoding UTF8`。
4. 若發現疑似亂碼，請先判斷是終端顯示、讀取方式，還是檔案內容本身的問題，再進行修復。
5. 不要為了套用此規範而改動無關檔案、換行或既有語言風格。

## 預期輸出格式

### Files Changed

- `path/to/file`: 說明新增或更新內容。

### Encoding And Language

- Encoding: UTF-8
- Language: 繁體中文優先，並說明是否沿用既有文件語言。

### Validation

- 說明是否已檢查輸出檔案、README 索引或疑似亂碼。

### Notes

- 若有偏離 UTF-8 或繁中優先，說明原因。
