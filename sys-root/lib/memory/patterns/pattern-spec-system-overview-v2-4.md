---
id: mem-pattern-spec-system-overview-v2-4
title: 规范体系四层架构与权威源（V2.4）
type: pattern
tags: [spec-system, governance, open-spec, agentsystem]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, continue, openai-codex, generic]
source_change_ids: [project-early-phase]
created_at: 2026-03-13
last_reviewed_at: 2026-03-13
maturity: draft
owner: @billhu
---

# 规范体系四层架构与权威源（V2.4）

## 背景与适用场景

`agentsystem` 在 V2.2–V2.4 阶段逐步将规范体系抽象为**四层架构 + 少数权威源**，既要支撑多宿主（Cursor / VS Code / Generic 等）复用，又要避免把所有规则写进宿主入口文件。  
本条目总结当前推荐的架构与权威源，供在本仓或引用本仓作为全局规则源的业务项目中复用。

## 推荐结构（四层宪法体系）

1. **治理内核层（宿主无关）**  
   - 文件：`OpenSpec.md`、`global-rules/*.md`、`agents/*.md`、`skills/*/SKILL.md`。  
   - 职责：定义 change-id、变更启动顺序、角色边界、技能触发、日志制度、审核与闭环规则。

2. **宿主适配层（platform-adapters/*）**  
   - 目录：`platform-adapters/cursor/*`、`platform-adapters/vscode/*`、`platform-adapters/generic/*`。  
   - 职责：说明不同宿主如何加载规则、如何接线 MCP/扩展、如何落地 `decision_sink` / `runtime_trigger` / `feedback_bridge` / `workspace_binding`。

3. **宿主入口层（各宿主要求的位置）**  
   - 示例：Cursor 的 `.cursor/rules/*.mdc`、VS Code 的根 `AGENTS.md` 与 `.github/agents/*.agent.md`。  
   - 职责：作为宿主可直接发现/加载的「最薄入口壳」，只做跳转与约束声明，不堆叠厚制度正文。

4. **运行后端层（可插拔实现）**  
   - 当前默认实现：`agent_team_project/`。  
   - 职责：承接决策写入、执行、反馈与状态持久化，不得改写治理层规则与角色边界。

一句话：**治理内核定义规则；适配层定义接线；入口层负责装载；运行后端负责执行。**

## 权威源与绑定关系（摘自规范体系总览）

1. **核心宪法**：`OpenSpec.md`  
   - MUST：目录结构（`openspec/`、`docs/`（按 usr-rules OpenSpec 第一节））、变更模型、`proposal.md` 建议结构、变更启动顺序与检查清单。

2. **全局补充宪法**：`global-rules/projects-rules-for-agent.md`  
   - MUST：任务执行通用机制、OpenSpec 变更入口、迭代日志强制记录、安全底线等；  
   - SHOULD：模型/配额使用策略与效率建议。

3. **技能映射宪法**：`global-rules/skills-rules-for-agent.md`  
   - MUST：各 Agent 角色 ↔ 主导/联动技能矩阵，以及「命中场景时先读 SKILL 再执行」的约定。

4. **项目工程宪法**：单项目内的 `openspec/project.md`  
   - 对本项目是 MUST：项目简介、技术栈、目录角色、change-id 命名规则等。

5. **工程宪法补充**：`project-rules/*`  
   - 对项目内部实现、目录结构、外部平台（如 Shopify Theme）的细节约束。

6. **项目 AI 说明书**：`openspec/AGENTS.md`  
   - 向 AI 说明项目类别、关键路径、可用 Skills 与触发词等。

## 与 V2.4 轻量化方案的关系

- 上述结构源自早期对规范体系的整体梳理，在 V2.4 中被**压缩为本 memory 条目**，用于替代长篇的体系总览文档；  
- 入口文件（如 `.cursor/rules/*.mdc`）和全局规则文件（如 `projects-rules-for-agent.md`）可只保留简化版结构说明，并在需要时让 Agent 通过 `memory/` 加载本条目，以获得完整的体系视图；  
- 对引用 `agentsystem` 作为全局规则源的业务仓，可在自身的 `openspec/AGENTS.md` 中链接到本 memory 条目，避免在项目仓内复制整套规范体系说明。

