# shadowMAS Notes

Source Repository: [shadowMAS](https://github.com/scyprodigy/shadowMAS?utm_source=chatgpt.com)

---

# Overview

shadowMAS 並不像一般 multi-agent framework 那樣，主要聚焦於：

* agent orchestration
* task execution
* tool calling
* autonomous workflow

它更偏向：

# AI Runtime Governance Layer

或：

# AI Runtime Shadow Layer

核心問題不是：

```text
AI 怎麼做更多事情？
```

而是：

```text
AI 做出來的東西，什麼時候有資格被相信？
```

---

# Core Philosophy

shadowMAS 的重要觀念：

> AI 產生的中間結果，不應該偷偷被升級成真理或長期記憶。

因此：

* 不直接 flatten uncertainty
* 不過早決定 single truth
* 不讓高自信語氣直接變成 canonical truth
* 不把 temporary signal 當成 long-term knowledge

---

# Conceptual Position

shadowMAS 不是：

* memory database
* vector database
* canonical knowledge system

它更像：

```text
runtime governance sidecar
```

類似：

* telemetry layer
* audit layer
* provenance tracker
* memory governance layer
* runtime historian

---

# Key Architectural Direction

shadowMAS 不預設固定 ontology 或固定 memory schema。

它的方向比較像：

```text
task execution
    ↓
runtime observation
    ↓
memory candidate
    ↓
future task impact evaluation
    ↓
promotion / downgrade / eviction
```

也就是：

# runtime-driven memory shaping

而不是：

# static memory storage

---

# Memory Governance

## Important Principle

記憶不是因為：

```text
被提到很多次
```

而存在。

而是因為：

```text
它降低未來 task 的成本
```

才值得被保留。

---

# Memory Evaluation Signals

作者提到的重要評估方向：

* 是否降低 token 成本？
* 是否減少誤解？
* 是否減少重複修正？
* 是否提升交付速度？
* 是否降低 agent 間摩擦？
* 是否造成語意污染？
* 是否造成 scope ambiguity？
* 是否導致後續 task failure？

---

# Memory Hierarchy

作者提到的 memory layer：

```text
cache
working memory
project memory
shared memory
```

這很接近：

# Runtime Memory Hierarchy

---

# MDL (Minimum Description Length)

作者提到：

> 好的記憶是在保留必要語義的前提下，
> 降低未來理解、溝通、修正與交付成本。

這與 MDL 概念接近：

```text
最佳表示方式
=
最小化未來理解成本
```

---

# Conflict Handling

shadowMAS 不直接做：

```text
final arbitration
```

而是：

```text
conflict preservation
+
evidence ranking
+
human governance
```

---

# Core Conflict Questions

當不同 agent 出現衝突時：

* 來源是哪個 agent？
* 有哪些 source_refs？
* 屬於哪個 memory layer？
* 是否碰到 canonical truth？
* 是否超出原本 atomic task scope？
* 錯誤成本有多高？
* 是否造成 downstream failure？
* 是否需要 human review？

---

# Evidence Ranking

作者提出的 ranking 概念：

```text
T2 canonical truth
>T3 approved shared memory
>T4 execution feed
>T5 cache/session state
```

以及：

* 有 source_refs > 無來源
* scope 精準 > scope 模糊
* 被後續 atomic tasks 驗證 > 導致後續污染
* 降低未來成本 > 增加摩擦與 ambiguity

---

# Important Governance Principle

shadowMAS 的核心不是：

```text
替人類決定誰對
```

而是：

```text
讓衝突保持可追溯、可降級、可重審
```

避免：

```text
confidence laundering
```

也就是：

```text
高自信語氣
≠
可信 truth
```

---

# Important Runtime Concepts

## Provenance

重要概念：

```text
這個結論從哪裡來？
```

包括：

* 哪個 agent？
* 哪次 workflow？
* 哪個 task？
* 哪個 source_refs？
* 哪個 memory layer？
* 哪個 scope？

---

## Risk-aware Reasoning

shadowMAS 不只考慮：

```text
correct / incorrect
```

而是：

```text
錯誤成本
影響範圍
可逆性
風險等級
```

---

# Relationship To Personal AI Runtime

與目前 Personal AI Runtime 構想高度相關：

* Preflight Protocol
* Spec-driven Workflow
* Verification Chain
* Devil's Advocate
* Human Governance
* Scenario Scoring
* Proposal Decision
* Model Fit Profiling
* Routing Confidence
* Reusable Asset Governance

---

# Potentially Reusable Ideas

## 1. Runtime Memory Hierarchy

```text
transient
working
project
shared
canonical
```

---

## 2. Trust Escalation Lifecycle

```text
raw output
    ↓
candidate
    ↓
verified candidate
    ↓
human-approved
    ↓
reusable asset
    ↓
playbook
    ↓
skill
```

---

## 3. Conflict Preservation

不要過早 flatten uncertainty：

```text
multiple outputs
    ↓
preserve conflict
    ↓
annotate provenance
    ↓
track downstream effects
    ↓
human governance
```

---

## 4. Runtime Governance Sidecar

shadowMAS 很像：

```text
AI Runtime Governance Sidecar
```

類似：

* observability layer
* tracing layer
* audit layer
* memory governance layer

而不是主 execution runtime。

---

# Framework Reading Notes

## 1. 它想解決什麼問題？

AI runtime 中：

* 記憶污染
* provenance 缺失
* conflict flattening
* confidence laundering
* memory governance
* long-term trust escalation

---

## 2. 核心 abstraction 是什麼？

* shadow layer
* memory candidate
* review packet
* evidence ranking
* provenance
* governance sidecar
* trust hierarchy

---

## 3. 它假設了哪些前提？

* AI output 不天然可信
* uncertainty 應被保留
* truth 是逐步演化的
* memory 應由 runtime 效果決定
* human governance 最終仍重要

---

## 4. 哪些部分適合 Personal AI Runtime？

* memory hierarchy
* governance sidecar
* provenance tracking
* review packet
* trust escalation
* runtime observation
* conflict preservation

---

## 5. 哪些部分可能衝突？

目前偏研究性 / governance-heavy：

* implementation complexity
* operational overhead
* runtime cost
* workflow latency

需要避免：

* 過度治理
* 過度 annotation
* 過度 runtime bookkeeping

---

## 6. Potential Failure Modes

* governance complexity explosion
* annotation overload
* excessive runtime friction
* memory fragmentation
* unresolved conflict accumulation
* human review bottleneck

---

## 7. 可否只吸收其中一層？

可以。

目前最值得吸收：

* provenance
* memory governance
* conflict preservation
* trust hierarchy
* runtime observation model

不一定需要完整導入整個 runtime structure。
