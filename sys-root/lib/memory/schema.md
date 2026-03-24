## `memory` Frontmatter 规范

本文件定义长期记忆条目的 frontmatter 结构与字段含义，依据「运行日志与长期记忆综合设计方案（V2.3）」。

### 必选字段

| 字段 | 说明 | 示例 |
| :--- | :--- | :--- |
| `id` | 记忆唯一标识 | `mem-openspec-change-workflow-001` |
| `title` | 记忆标题 | `OpenSpec 变更标准流程（最小实践）` |
| `type` | 记忆类型：`pattern` / `anti-pattern` / `preference` / `playbook` / `reflection` | `pattern` |
| `tags` | 内容标签（至少 1 个） | `[openspec, change-flow]` |
| `applicable_projects` | 适用项目列表：`[all]` 或具体项目标识 | `[agentsystem]` |
| `host_scope` | 适用宿主环境列表 | `[cursor, vscode, continue, openai-codex, generic]` |
| `source_change_ids` | 来源的变更 ID 列表 | `[sys-infra-memory-v1]` |

### 建议字段

| 字段 | 说明 | 示例 |
| :--- | :--- | :--- |
| `created_at` | 创建日期 | `2026-03-12` |
| `last_reviewed_at` | 最后审阅日期 | `2026-03-12` |
| `maturity` | 成熟度：`draft` / `experimental` / `stable` / `deprecated` | `draft` |
| `owner` | 维护责任人（可选） | `@billhu` |
| `related` | 与本条目存在强逻辑耦合的其它 memory 条目列表（可选，建议 3～5 条以内） | `[memory/patterns/pattern-iteration-log-enforcement-and-usage.md, memory/anti-patterns/anti-pattern-missing-iteration-log-in-agent-calls.md]` |

### 示例：pattern 类型

```yaml
---
id: mem-openspec-change-workflow-001
title: OpenSpec 变更标准流程（最小实践）
type: pattern
tags: [openspec, change-flow, agentsystem]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode]
source_change_ids: [sys-infra-memory-v1]
created_at: 2026-03-12
last_reviewed_at: 2026-03-12
maturity: draft
---
```

正文部分可采用 Markdown，自由描述模式的背景、步骤与适用场景；推荐结构：

1. 背景与适用场景
2. 推荐做法（步骤/Checklist）
3. 反例与常见误区（如有）
4. 与现有规范/技能的关系（如关联到某个 SKILL 或 OpenSpec 小节）
5. （如为核心 pattern / anti-pattern / reflection）补充一节「关联模式」，说明本条目与哪些其它 memory 条目应联动使用，以及典型联动路径。

### 关联与加载的克制机制（必须遵守）

> `related` 字段与「关联模式」小节的设计目标是：在**少量核心记忆之间建立一跳的簇状连接**。  
> 编写与读取时必须遵守以下克制机制：
> - 单条记忆的 `related` 建议控制在 3～5 条以内，只保留「直接逻辑耦合」的模式/反模式/反思；  
> - 避免出现长链式泛连接（A → B → C → ...），防止在 simple 模式下被迫一次性加载过多无关记忆；  
> - 具体加载行为由主 Agent 与宿主 adapter 决定，通常只在需要时从当前条目出发**按需追加读取一跳 related**，而不会自动递归遍历。

