---
id: mem-user-coding-style-001
title: 用户偏好的编码与文档风格（示例）
type: preference
tags: [coding-style, documentation, chinese]
applicable_projects: [agentsystem]
host_scope: [cursor]
source_change_ids: [sys-infra-memory-v1]
created_at: 2026-03-12
last_reviewed_at: 2026-03-12
maturity: draft
owner: @billhu
---

# 用户偏好的编码与文档风格（示例）

> 本条目仅作为 frontmatter 与内容结构示例，具体偏好应在与用户确认后再更新为稳定版本。

## 编码风格（示例假设）

- 代码与注释以简体中文说明为主，必要时补充英文术语；
- 更偏好结构清晰、模块化的实现，而非过度抽象；
- 在规则与基础设施仓库中，优先保证可读性与可维护性。

## 文档风格（示例假设）

- 使用简明的小节结构与列表，避免过长的大段文字；
- 对关键概念提供简短定义与上下文引用路径；
- 在多仓库/多宿主场景下，明确区分通用规则与宿主特定适配说明。

> 当与真实用户偏好不符时，应通过新的 change-id 更新本条目的内容，并将 `maturity` 从 `draft` 提升到 `stable` 或根据需要拆分为多条更细粒度的偏好记录。

