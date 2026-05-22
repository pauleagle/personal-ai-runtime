# Codex 版：Skill Creator 啟動包

> 對齊來源：`pro-kit/02-skill-creator-bootstrap.md`
> 原始定位：幫 Claude Code 安裝 Anthropic 官方 `skill-creator`，再帶使用者做出第一個真實 skill。
> Codex 改寫定位：建立可攜 skill 建立流程，並產出第一個能被 Codex / 其他 AI 讀懂的 `SKILL.md`。

## Claude → Codex 步驟對齊

| Claude 原 section | 原始核心意圖 | Codex 對應做法 |
| --- | --- | --- |
| Section A：偵測資料夾結構 | 判斷用戶有沒有跑過 pro-kit 01，決定 skill-creator 裝哪裡 | 偵測 `000_Agent/skills/`、`AGENTS.md`、可選 `~/.claude/skills`；優先裝到專案可見位置 |
| A-3 已安裝檢查 | 避免重複覆蓋官方 skill-creator | 若已存在，備份或詢問更新；不可直接覆蓋 |
| Section B：sparse checkout | 只抓官方 repo 的 `skills/skill-creator/`，避免整個 repo 太大 | 同樣採 sparse checkout；若網路受限，建立 Codex 最小版 skill-creator 模板 |
| B-3 完整性驗證 | 確認不是只抓 `SKILL.md`，而是完整工具包 | 驗證 `SKILL.md`、`agents/`、`scripts/`、`eval-viewer/` 等完整存在 |
| Section C：訪談第一個 skill | 找出最值得先自動化的高頻任務 | Codex 逐題訪談重複度、頻率、輸出形式，再給 1 個推薦 + 2 個備選 |
| Section D：實戰跑 `/skill-creator` | 安裝不是終點，要真的生出第一個 skill | Codex 讀 skill-creator 規則或使用可攜模板，直接建立 `000_Agent/skills/[name]/SKILL.md` |
| Section E：候選清單與養成節奏 | 讓使用者知道 skill 要慢慢長，不要一次建太多 | 寫入 daily log / candidates，建議每週最多 1 個 |

## Section A：偵測安裝位置

### A-1. 偵測 pro-kit 01 資料層

依序檢查：

```text
000_Agent/
000_Agent/skills/
AGENTS.md
000_Agent/CORE_RULES.md
```

判斷：

- 若 `000_Agent/skills/` 存在，使用 `000_Agent/skills/skill-creator/`。
- 若只有 `~/.claude/skills/`，且使用者明確要 Claude Code 相容，使用該位置。
- 若都沒有，先建立 `000_Agent/skills/`，並提醒這是 Codex 版預設位置。

### A-2. 安裝位置決策表

| 狀態 | Codex 安裝位置 | 說明 |
| --- | --- | --- |
| 有 `000_Agent/skills/` | `000_Agent/skills/skill-creator/` | 推薦，跟專案一起走 |
| 有 `~/.claude/skills` 且使用者要相容 | 可同步 / 複製到 Claude 位置 | 只作相容，不作主資料層 |
| 全新狀態 | 建 `000_Agent/skills/skill-creator/` | 不把新資料藏進工具全域目錄 |

### A-3. 已存在處理

若 `skill-creator/SKILL.md` 已存在：

1. 讀取前 20 行確認版本 / 來源。
2. 詢問使用者要更新、保留、或直接進入建立自訂 skill。
3. 若更新，先備份：

```text
skill-creator.bak.YYYYMMDD-HHMMSS/
```

## Section B：安裝 skill-creator

### B-1. 官方版本 sparse checkout

若使用者同意安裝 Anthropic 官方版本，使用 sparse checkout：

```bash
git init -q
git remote add origin https://github.com/anthropics/skills.git
git config core.sparseCheckout true
echo "skills/skill-creator/" >> .git/info/sparse-checkout
git pull --depth 1 origin main
```

Codex 注意：

- 這需要網路。若 sandbox / DNS / GitHub 存取失敗，依權限規則要求升級執行。
- 不要改成下載不明來源壓縮檔。
- 不要只抓 `SKILL.md`，原始核心意圖就是完整工具包。

### B-2. 完整性檢查

至少檢查：

```text
skill-creator/
  SKILL.md
  LICENSE.txt
  agents/
    analyzer.md
    comparator.md
    grader.md
  assets/
  eval-viewer/
    generate_review.py
    viewer.html
  references/
    schemas.md
  scripts/
    run_eval.py
    improve_description.py
    quick_validate.py
    package_skill.py
```

若缺任一核心資料夾，停止並重新取得。

### B-3. Codex 最小 fallback

若官方版本不可用，建立：

```text
000_Agent/skills/skill-creator/
  SKILL.md
  templates/basic-skill.md
  README.md
```

`templates/basic-skill.md`：

```markdown
---
name: example-skill
description: 在明確任務情境下使用；一句話說清楚觸發條件與輸出。
---

# Skill 名稱

## 何時使用

## 輸入

## 需要讀取的資料

## 執行步驟

## 輸出格式

## 驗證方式

## 不要做

## 迭代紀錄
```

## Section C：訪談第一個值得建立的 skill

### C-1. 三題核心訪談

問：

1. 你最常重複請 AI 做哪類事？
   - 寫作、整理、回覆、檢查、查詢決策、其他
2. 頻率？
   - 每天、每週 2-5 次、每週一次、每月幾次
3. 你希望輸出是什麼？
   - Markdown 文件、可複製文字、JSON / 結構化資料、分析報告、其他

### C-2. 推薦第一個 skill

根據答案給：

```markdown
## 第一個 skill 建議

### 最推薦：/[name]

- 做什麼：
- 為什麼適合先做：
- 需要的參考資料：
- 預估建立時間：

### 備選 1：/[name]

### 備選 2：/[name]
```

選擇原則：

- 高頻優先。
- 輸出格式越穩定越適合先做。
- 需要的參考資料已在 `200_Reference/` 裡更好。
- 不要第一個就做過大、過抽象的「全能助理」。

### C-3. 如果使用者還不確定

改用反向挖掘：

- 昨天或上週是否有一段你覺得「我又在重打一樣的要求」？
- 有沒有哪個任務下次不想從零開始？
- 哪種輸出你最常要 AI 改第二次、第三次？

## Section D：建立第一個自訂 skill

### D-1. Capture Intent

先寫下：

- skill 要讓 Codex 做什麼
- 什麼情境應該觸發
- 輸入會長什麼樣
- 預期輸出長什麼樣
- 使用者最在意什麼品質

### D-2. Interview and Research

補問必要 edge cases：

- 是否有好的範例放在 `200_Reference/`
- 是否有「絕對不要」的反例
- 字數、語氣、格式限制
- 是否需要存檔，存到哪裡
- 是否需要讀外部工具或只讀本地檔案

### D-3. Draft the Skill

建立：

```text
000_Agent/skills/[skill-name]/SKILL.md
```

模板：

```markdown
---
name: [skill-name]
description: [把最重要觸發關鍵字放前面；說明任務、輸入、輸出。]
---

# [Skill 名稱]

## 何時使用

- 當使用者要求...
- 當輸入包含...
- 當輸出需要...

## 不適用情境

- ...

## 需要讀取的資料

- `200_Reference/...`
- `000_Agent/memory/MEMORY.md`（若需要偏好）

## 執行步驟

1. 確認使用者目標與輸入。
2. 讀取相關參考資料。
3. 套用 SOP 產出初稿。
4. 自我檢查格式與限制。
5. 交付最終輸出，必要時說明存放位置。

## 輸出格式

```text
[定義輸出樣式]
```

## 品質檢查

- 是否符合使用者語氣
- 是否讀取該讀的參考資料
- 是否避免不適用情境
- 是否沒有 invented facts

## 迭代紀錄

- YYYY-MM-DD：建立第一版
```

### D-4. Supporting files

若需要範例，可建立：

```text
000_Agent/skills/[skill-name]/examples/
000_Agent/skills/[skill-name]/references/
```

但不要複製大量 private 素材；優先引用 `200_Reference/` 路徑。

### D-5. 驗證 skill

檢查：

- `SKILL.md` 存在
- frontmatter 有 `name` 和 `description`
- `name` 與資料夾名一致
- description 具體，不是「幫我處理工作」
- 有「何時使用」與「不適用情境」
- 有輸出格式與驗證方式

Codex 測試方式：

```text
請讀取 `000_Agent/skills/[skill-name]/SKILL.md`，並用這個 skill 處理以下測試輸入：...
```

Claude Code 相容測試：

```text
/[skill-name]
```

## Section E：候選清單與養成節奏

追加到 daily log：

```markdown
## Skill 候選清單

**已建立**
- `/[skill-name]` - [一句話用途]

**接下來可建**
1. `/候選-1` - [用途 / 為什麼適合]
2. `/候選-2` - [用途 / 為什麼適合]
3. `/候選-3` - [用途 / 為什麼適合]

**養成規則**
- 每週最多建 1 個。
- 每個 skill 用 1 週後再改。
- 一個月沒用到的 skill，刪除、合併或改 description。
```

## 完成檢查

- 已決定安裝位置
- 已安裝官方 skill-creator 或建立 Codex fallback
- 已訪談高頻任務
- 已產出第一個 `000_Agent/skills/[name]/SKILL.md`
- 已驗證 frontmatter 與輸出格式
- 已把候選清單寫入 daily log
- 已提醒使用者新 session 測試
