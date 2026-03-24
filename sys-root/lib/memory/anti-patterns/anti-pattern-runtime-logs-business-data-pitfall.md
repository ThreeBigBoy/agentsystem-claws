---
id: mem-runtime-logging-pitfall-001
title: 运行日志中混入业务数据的陷阱
type: anti-pattern
tags: [runtime-logs, privacy, security]
applicable_projects: [all]
host_scope: [cursor, vscode, continue, openai-codex, generic]
source_change_ids: [sys-infra-memory-v1]
created_at: 2026-03-12
last_reviewed_at: 2026-03-12
maturity: draft
related:
  - memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md
  - memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md
---

# 运行日志中混入业务数据的陷阱

## 陷阱描述

在为 AI 模型调用记录运行日志时，将完整 Prompt、模型回复正文或业务数据对象直接写入日志文件，会导致：

- **隐私与合规风险**：可能泄露用户敏感信息或内部业务细节；
- **日志膨胀**：运行日志变得难以存储与分析，噪音极大；
- **环境迁移隐患**：日志若被迁移到集中化监控或外部存储，会进一步放大风险。

## 推荐做法

- 仅记录与监控相关的**技术指标**：tokens 使用量（如可见）、耗时、状态码、错误类别；
- 错误信息仅保留分类与简要说明，必要时使用 hash 或索引指向详细调试数据；
- 始终遵守 `runtime-logs/README.md` 与相关全局规则中的隐私约束。

## 避免方式

- 禁止在运行日志中写入：
  - 完整 Prompt 与模型回复；
  - 包含个人身份信息或业务敏感字段的结构化数据；
  - 完整 stack trace（如需调试，可在本地单独保存，且不进入版本控制）。

