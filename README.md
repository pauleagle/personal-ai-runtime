````markdown
# Personal AI Runtime

Personal AI Runtime 是一個個人用的 AI 研發工作區與架構中控台，用來整理、串接與管理多個 AI 工具模組，例如：

- `llm-router`
- `model-fit-profiler`
- `EvoMind`
- `Idea Fabric`
- `Proposal Decision`
- RAG knowledge sources

它的目標不是一開始就做成大型單體系統，而是先建立一個清楚的本機 workspace，讓不同 AI 工具可以逐步形成共用的資料格式、目錄規範、prompt 規範、模型評估結果與知識來源。

---

## 1. Project Goal

Personal AI Runtime 想解決的問題是：

> 個人 AI 專案如何從想法、決策、模型選擇、實作、錯誤學習，到下一次更聰明地開發。

整體流程可以理解為：

```text
想法 → 決策 → 執行 → 評估 → 學習 → 反饋
````

對應目前規劃中的模組關係：

```text
Idea Fabric
    ↓ 產生想法

Proposal Decision
    ↓ 判斷要不要做、怎麼做

llm-router
    ↓ 選擇適合模型執行

Model Fit Profiler
    ↑ 提供模型適性資料

EvoMind
    ↑ 從實作與錯誤中沉澱規則
    ↓ 反饋到所有專案
```

---

## 2. Architecture Overview

```text
Personal AI Runtime
┌─────────────────────────────────────────────────────────┐
│                    Application / UI                     │
│  Chatbox | Dashboard | Profiler UI | Knowledge Browser  │
└─────────────────────────────────────────────────────────┘

┌───────────────────────┐  ┌─────────────────────────────┐
│   Creative / Ideas    │  │    Reasoning / Decision      │
│                       │  │                             │
│   Idea Fabric         │  │   Proposal Decision          │
│   Story Branching     │  │   Model Fit Profiler         │
│   Topic / Master      │  │   Scenario Scoring           │
│   Raw Detail          │  │   Priority / Risk Review     │
└───────────────────────┘  └─────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│             LLM Runtime / Integration Layer             │
│                                                         │
│   llm-router | intent classifier | model gateway        │
│   Ollama | OpenAI | Gemini | Claude | Local Models      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│           Engineering Governance / AOP Layer            │
│                                                         │
│   EvoMind | Error Knowledge | Iron Laws | AGENTS.md     │
│   Prompt Rules | Root Cause Memory | Regression Rules   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Core Container                       │
│                                                         │
│   Project Registry | Context Store | Prompt Templates   │
│   Model Registry | Scenario Registry | Rule Engine      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     Test / Evaluation                   │
│                                                         │
│   Prompt Tests | Model Benchmarks | Quality Rubrics     │
│   Scenario Test Sets | Regression Test                  │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Repository Role

這個 repository 第一階段的定位是：

```text
personal-ai-runtime = 架構文件 + 本機 workspace 規劃 + 模板
```

不是一開始就把所有模組程式碼都放進來。

目前建議：

```text
GitHub:
  personal-ai-runtime      → 總架構與模板 repo
  llm-router               → 獨立 repo
  model-fit-profiler       → 獨立 repo

Local:
  personal-ai-runtime/     → 本機整合工作區
```

也就是：

```text
Local Workspace First
GitHub Repos Stay Independent
Architecture Repo Later
```

---

## 4. Suggested Directory Structure

```text
personal-ai-runtime/
  README.md
  .gitignore

  agent-playbooks/
    README.md

  agent-skills/
    README.md

  docs/
    architecture.md
    roadmap.md
    module-map.md

  diagrams/
    personal-ai-runtime.png

  modules/
    .gitkeep

  rag_sources/
    .gitkeep

  templates/
    rag_source_template/
      raw/
        .gitkeep
      chunks/
        .gitkeep
      embeddings/
        .gitkeep
      index/
        .gitkeep
      metadata.example.json

  shared/
    prompts/
      .gitkeep
    schemas/
      .gitkeep
    configs/
      .gitkeep

  outputs/
    .gitkeep

  logs/
    .gitkeep
```

---

## 5. Agent Playbooks and Skills

`agent-playbooks/` 與 `agent-skills/` 用來沉澱 AI agent 的工作方式，讓一次性的提示、成功案例與任務規則逐步變成可重用、可維護的操作規範。

### agent-playbooks/

`agent-playbooks/` 放人類可讀的 playbook。它描述某類工作應該如何判斷、何時使用、何時不要使用、agent 需要遵守哪些 guardrails，以及可重用的標準 prompt。

適合放在 playbook 的內容包含：

* 從一次性 prompt 抽象出來的工作流程
* 文件整理、發版檢查、完成檢查等跨任務規範
* 尚未穩定到需要變成 Codex skill 的行為準則
* 需要人類閱讀、討論、調整的 agent 作業原則

### agent-skills/

`agent-skills/` 放 Codex 可載入的 skill。它是從成熟 playbook 萃取出的短版、命令式執行規則，讓 agent 在特定任務中可以快速套用一致的工作流程。

適合放在 skill 的內容包含：

* 已經反覆使用並穩定的 playbook
* agent 執行時需要立即遵守的步驟、限制與輸出格式
* 可被明確觸發的任務能力，例如 changelog 標準化、playbook 轉 skill、prompt 轉 playbook

### Relationship

兩者的關係是：

```text
prompt / successful case / repeated rule
    ↓
agent-playbooks/<name>.md
    ↓
agent-skills/<name>/SKILL.md
```

Playbook 先保存完整意圖與脈絡；skill 只保留 agent 執行時真正需要的精簡規則。除非明確需要自動化觸發或反覆執行，新的工作習慣應先進 playbook，不急著抽成 skill。

---

## 6. Local Workspace Structure

實際本機開發時，可以將獨立專案 clone 到 `modules/` 底下：

```text
personal-ai-runtime/
  modules/
    llm-router/
    model-fit-profiler/
```

例如：

```bash
cd personal-ai-runtime/modules

git clone git@github.com:pauleagle/llm-router.git
git clone git@github.com:pauleagle/model-fit-profiler.git
```

但在 `personal-ai-runtime` repo 本身，`modules/` 預設會被 `.gitignore` 排除，避免把其他 repo 的程式碼混進來。

---

## 7. Module Positioning

### llm-router

參照：

```text
https://github.com/pauleagle/llm-router
```

位置：

```text
personal-ai-runtime/
  modules/
    llm-router/
```

定位：

```text
LLM Runtime / Integration Layer
```

主要責任：

* 接收 LLM request
* 判斷 `intent` / `task_type`
* 選擇合適模型
* 呼叫 Ollama / OpenAI / Gemini / Claude / local models
* 記錄 routing log
* 回傳結果

未來演化方向：

```text
intent → model
```

進化為：

```text
intent + scenario + device + profiler score → model
```

---

### model-fit-profiler

參照：

```text
https://github.com/pauleagle/model-fit-profiler
```

位置：

```text
personal-ai-runtime/
  modules/
    model-fit-profiler/
```

定位：

```text
Evaluation / Profiling Layer
```

主要責任：

* 測試模型在不同任務上的表現
* 記錄 latency、tokens/sec、品質分數
* 產出 model fit score
* 產生 routing recommendation
* 提供 `llm-router` 選模型依據

輸出結果可放在：

```text
personal-ai-runtime/
  outputs/
    profiler_results/
    routing_recommendations/
```

---

## 8. RAG Sources

`rag_sources/` 用來放本機 RAG 資料來源。

例如：

```text
personal-ai-runtime/
  rag_sources/
    ai_coding_dictionary/
      raw/
      chunks/
      embeddings/
      index/
      metadata.json
```

各資料夾用途：

| Path            | Description     |
| --------------- | --------------- |
| `raw/`          | 原始資料，例如文章、筆記、文件 |
| `chunks/`       | 切分後的文字區塊        |
| `embeddings/`   | 向量資料            |
| `index/`        | 檢索索引            |
| `metadata.json` | 資料來源描述、版本、處理方式  |

注意：

`rag_sources/` 預設不 commit 到 GitHub，因為其中可能包含：

* 大量資料
* 個人筆記
* 未授權轉存內容
* 可重建的 embedding / index
* 專案或工作相關敏感內容

如果需要提供範例，請使用：

```text
templates/
  rag_source_template/
```

---

## 9. Shared Resources

`shared/` 用來放未來可被多個 module 共用的資料。

```text
shared/
  prompts/
  schemas/
  configs/
```

### prompts/

可放共用 prompt：

```text
shared/
  prompts/
    task_system_prompts.json
    router_system_prompts.json
    judge_system_prompts.json
```

### schemas/

可放共用 schema：

```text
shared/
  schemas/
    scenario.schema.json
    model-profile.schema.json
    evaluation-result.schema.json
    routing-recommendation.schema.json
```

### configs/

可放共用設定：

```text
shared/
  configs/
    model_registry.json
    scenario_registry.json
    runtime_config.json
```

---

## 10. Outputs

`outputs/` 用來放各 module 的執行結果。

例如：

```text
outputs/
  profiler_results/
  routing_recommendations/
  generated_docs/
```

其中 `model-fit-profiler` 的輸出可以被 `llm-router` 使用：

```text
model-fit-profiler
    ↓
outputs/routing_recommendations/
    ↓
llm-router
```

---

## 11. Logs

`logs/` 用來放本機 runtime log。

例如：

```text
logs/
  llm-router/
  model-fit-profiler/
```

這些 log 預設不 commit。

---

## 12. Recommended .gitignore

建議第一版 `.gitignore`：

```gitignore
# Ignore local module checkouts
/modules/*
!/modules/.gitkeep

# Ignore local RAG sources
/rag_sources/*
!/rag_sources/.gitkeep

# Runtime outputs
/outputs/*
!/outputs/.gitkeep

# Runtime logs
/logs/*
!/logs/.gitkeep

# Environment files
.env
.env.*
!.env.example

# Node
node_modules/
dist/
build/

# Python
__pycache__/
*.pyc
.venv/
venv/

# OS / editor
.DS_Store
Thumbs.db
.vscode/
.idea/
```

---

## 13. Suggested Development Phases

### Phase 1: Documentation and Workspace

目標：

* 建立 `personal-ai-runtime` 架構文件
* 建立本機 workspace
* 保持 `llm-router` 與 `model-fit-profiler` 獨立 repo
* 設計基本目錄結構
* 建立 RAG source template

成果：

```text
personal-ai-runtime/
  README.md
  docs/
  diagrams/
  templates/
```

---

### Phase 2: Shared Schema and Config

目標：

* 定義共用 schema
* 定義 scenario registry
* 定義 model registry
* 整理共用 prompts
* 讓 `llm-router` 與 `model-fit-profiler` 開始使用相同資料格式

可能的 shared schema：

```text
Scenario
ModelProfile
PromptTemplate
ErrorKnowledge
IronLaw
Proposal
IdeaItem
EvaluationResult
RoutingRecommendation
```

---

### Phase 3: Profiler-driven Routing

目標：

讓 `llm-router` 不再只靠靜態設定選模型，而是可以讀取 `model-fit-profiler` 的測試結果。

從：

```text
intent → model
```

進化成：

```text
intent + scenario + device + profiler score → model
```

---

### Phase 4: EvoMind Governance

目標：

讓 EvoMind 從錯誤與解法中產生可重用的工程治理資料。

每次 error report 可以產生：

```text
knowledge note
iron law
project rule patch
```

例如：

```text
Angular @HostListener 不會自動注入 event
```

可以沉澱成：

```text
knowledge note:
  root cause / solution

iron law:
  使用 @HostListener 時必須明確宣告 ['$event']

project rule patch:
  更新 AGENTS.md / coding-guidelines.md
```

---

## 14. Design Principles

### 14.1 Local-first

先讓本機工作區跑順，再決定 GitHub 是否要整併成 monorepo。

目前建議：

```text
本機整合
GitHub 獨立
```

---

### 14.2 Module Independence

`llm-router`、`model-fit-profiler` 目前應保持獨立 repo。

原因：

* 可以獨立 version tag
* 可以獨立 README
* 可以獨立 CHANGELOG
* 可以獨立 issue / release
* 不會過早被總架構綁死

---

### 14.3 Shared Contract First

在還沒有真正整併程式碼之前，先整合：

* schema
* config
* prompt format
* output format
* scenario naming
* model naming

也就是先統一「契約」，不要急著統一程式碼。

---

### 14.4 Rebuildable Data Should Not Be Committed

以下資料預設不 commit：

* embeddings
* vector index
* runtime logs
* profiler raw outputs
* local generated files
* personal raw notes

這些資料應該可以透過 script 或流程重建。

---

### 14.5 Governance as Feedback Loop

EvoMind 的定位不是單純知識庫，而是把開發經驗變成下次開發前會被讀取的規則。

```text
error → root cause → solution → iron law → agent rule → next development
```

---

## 15. Related Repositories

目前建議維持獨立 repo：

| Repository            | Role                                                                   |
| --------------------- | ---------------------------------------------------------------------- |
| `llm-router`          | LLM request routing and model gateway                                  |
| `model-fit-profiler`  | Model evaluation, benchmark, and routing recommendation                |
| `personal-ai-runtime` | Architecture, workspace structure, templates, and integration planning |

---

## 16. Current Status

目前狀態：

```text
Status: Planning / Workspace Bootstrap
```

已規劃：

* 整體架構圖
* 本機 workspace 結構
* RAG source 結構
* agent playbook / skill 分層意圖
* `llm-router` 位置
* `model-fit-profiler` 位置
* GitHub repo 分工策略
* `.gitignore` 策略

下一步建議：

1. 建立 `personal-ai-runtime` repo
2. 加入 `README.md`
3. 加入 `.gitignore`
4. 加入 `docs/architecture.md`
5. 加入 `templates/rag_source_template/`
6. 本機 clone `llm-router` 與 `model-fit-profiler` 到 `modules/`

---

## 17. Summary

Personal AI Runtime 是一個個人 AI 研發作業系統的雛形。

它不是單一工具，而是一套逐步形成的工作流：

```text
想法 → 決策 → 執行 → 評估 → 學習 → 反饋
```

其中：

* `Idea Fabric` 負責整理想法
* `Proposal Decision` 負責評估提案
* `llm-router` 負責模型路由
* `model-fit-profiler` 負責模型適性評估
* `EvoMind` 負責從錯誤中沉澱知識與鐵律
* `agent-playbooks` 負責保存人類可讀的 agent 工作規範
* `agent-skills` 負責保存 Codex 可載入的精簡執行規則
* `rag_sources` 負責提供可檢索知識來源
* `shared` 負責逐步沉澱共用 schema、prompt、config

第一階段的重點不是把所有東西整併成 monorepo，而是先建立清楚的本機整合工作區與文件化架構。

等到 shared schema、scenario registry、model registry 穩定後，再決定是否進一步轉成正式 monorepo。

```
```
