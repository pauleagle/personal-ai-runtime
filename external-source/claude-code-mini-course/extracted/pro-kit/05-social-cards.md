# Codex 版：社群圖卡產生器

> 對齊來源：`pro-kit/05-social-cards.md`
> 原始定位：安裝 Claude Code 的 `/cards` skill，將文章或文字拆成 IG 圖卡並用 Playwright 匯出 PNG。
> Codex 改寫定位：安裝可攜的 `cards` skill，讓 Codex 能用 HTML 模板 + Playwright 產生、預覽、驗證與匯出社群圖卡。

## 核心意圖

原文不是叫 AI 憑空畫圖，而是把圖卡拆成兩層：

1. AI 負責內容拆卡、標題、段落與 CTA。
2. HTML 模板與 Playwright 負責穩定版面與 PNG 匯出。

Codex 版保留這個分工，避免每次都產生風格不一致、文字爆版或無法匯出的圖。

## Claude → Codex 步驟對齊

| Claude 原 section | 原始核心意圖 | Codex 對應做法 |
| --- | --- | --- |
| Section A：偵測環境 | 找到 Skills 目錄、備份既有 cards、確認 Node.js | 優先 `000_Agent/skills/cards/`；已存在先備份；檢查 Node / npm |
| Section B：sparse checkout | 只抓 `skills/social-cards/`，不是整個 repo | Codex 同樣 sparse checkout；網路失敗時請使用者提供本地材料 |
| Section C：搬到 INSTALL_PATH + Playwright | 移到正式 skill 位置，安裝截圖依賴 | 在 `cards/` 內安裝 Playwright / Chromium，失敗時依權限規則處理 |
| Section D：驗證 | 確認 `SKILL.md`、模板、截圖腳本、node_modules 都在 | Codex 加上可選 Browser / Playwright 截圖驗證，避免空白圖 |
| 使用流程 | `/cards URL`、`/cards file`、直接貼文字 | Codex 可用自然語言觸發，但仍讀 `SKILL.md` 流程 |

## Section A：偵測環境

### A-1. Skills 位置

優先：

```text
000_Agent/skills/cards/
```

若使用者明確要 Claude Code slash command：

```text
~/.claude/skills/cards/
```

Codex 主資料層仍建議放在專案可見位置。

### A-2. 已存在處理

若 `cards/` 已存在：

1. 讀取 `cards/SKILL.md` 前幾行確認來源。
2. 備份為 `cards.bak.YYYYMMDD-HHMMSS/`。
3. 再安裝新版本。

不可直接刪掉使用者既有模板。

### A-3. Node.js 檢查

檢查：

```bash
node --version
npm --version
```

若缺少 Node.js，停止並請使用者先安裝。不要用其他截圖方案繞過，因為原 skill 的核心依賴是 Playwright。

## Section B：取得 skill 完整資料夾

### B-1. sparse checkout

```bash
git init -q
git remote add origin https://github.com/lifehacker-tw/claude-code-mini-course.git
git config core.sparseCheckout true
echo "skills/social-cards/" >> .git/info/sparse-checkout
git pull --depth 1 origin master
```

Codex 注意：

- 需要網路；失敗時依 sandbox 權限要求升級。
- 不要 clone 整個 repo，避免下載不必要材料。
- 不要只複製 `SKILL.md`；模板與腳本是核心。

### B-2. 本地材料 fallback

若 repo private 或網路不可用：

1. 請使用者提供本地 `skills/social-cards/` 路徑。
2. 複製整個資料夾到 `000_Agent/skills/cards/`。
3. 再跑結構驗證。

## Section C：檔案結構驗證

安裝後至少應有：

```text
cards/
  SKILL.md
  README.md
  assets/
    blue-dark/
      cover.html
      content-text.html
      content-image.html
      cta.html
    orange-light/
      cover.html
      content-text.html
      content-image.html
      cta.html
  scripts/
    screenshot.mjs
```

若缺少：

- `assets/`：無法穩定產圖。
- `scripts/screenshot.mjs`：無法匯出 PNG。
- `SKILL.md`：AI 不知道流程。

缺檔時停止，不要用臨時模板硬補。

## Section D：安裝 Playwright

在 `cards/` 內：

```bash
npm init -y
npm install playwright
npx playwright install chromium
```

Codex 權限注意：

- `npm install` / `npx playwright install chromium` 可能需要網路。
- 若 sandbox 網路失敗，應重新以升級權限請求執行。
- 不要把 `node_modules/` 加入 Git 備份。

## Section E：使用流程

觸發方式：

```text
/cards https://example.com/article
/cards 200_Reference/notes/example.md
做圖卡，以下是內容：...
```

Codex 執行順序：

1. 取得來源內容。
   - URL：需可讀取網頁內容；必要時使用 web。
   - 檔案：先確認路徑存在。
   - 直接貼文字：直接整理。
2. 詢問品牌設定。
   - 配色：藍黑 / 橘白 / 自訂品牌色。
   - 尺寸：4:5 或 1:1。
   - 帳號 handle。
3. 拆卡。
   - cover：主標題與一句 hook。
   - content-text：純文字重點。
   - content-image：圖文搭配。
   - cta：結尾行動呼籲。
4. 生成 HTML。
5. 開預覽。
6. 使用者確認或要求修改。
7. 匯出 2x PNG。

## Section F：Codex 視覺驗證

匯出前至少檢查：

- 首張圖不是空白。
- 文字沒有超出邊界。
- 標題可讀。
- 所有卡片尺寸一致。
- 4:5 / 1:1 輸出解析度符合設定。
- 匯出的 PNG 檔案存在且大小合理。

若本地有 Browser plugin 或 Playwright 可用，開預覽頁並截圖檢查。

## Section G：Codex 注意事項

- 不要用抽象漸層取代內容排版；圖卡價值在資訊拆解。
- 若使用者有品牌資料，優先讀 `200_Reference/brand/`。
- 不要一次塞太多字；寧可多拆一張。
- 對外發布前提醒使用者確認引用來源與版權。
- 若引用網頁文章，避免大段照抄，改成摘要與重組。

## 完成檢查

- `000_Agent/skills/cards/SKILL.md` 存在
- `assets/blue-dark/` 存在且有 4 種模板
- `assets/orange-light/` 存在且有 4 種模板
- `scripts/screenshot.mjs` 存在
- Playwright 安裝完成或已明確記錄未安裝原因
- 已告訴使用者如何用 URL / 檔案 / 貼文字測試
