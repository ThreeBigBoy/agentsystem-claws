---
type: anti-pattern
title: tasks.md 治理清单格式导致 run 解析 0 条任务、不派发子 Agent
tags: [anti-pattern, tasks-md, run-langgraph, parser, dispatch]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [deepen-langgraph-v2-11-2]
related:
  - memory/patterns/pattern-run-execution-determinism.md
  - OpenSpec.md
---

# tasks.md 治理清单格式导致 run 解析 0 条任务、不派发子 Agent

## 现象描述

- 变更已通过 run_langgraph 执行至 status=done，但**任务数（task_count）为 0**，没有任何任务被派发到子 Agent。
- tasks.md 内容为「治理清单」式：章节无 Executor（如 `## 1. 工作流引擎编排审查`），任务行为为 `- [x] **1.1** 梳理...`（加粗编号或非 `N.M` 数字格式）。

## 原因

运行后端 **parser**（`agent_team_project/langgraph_backend/parser.py`）仅识别：

- **章节**：`## N. 标题（Executor）」——必须带括号内的 Executor；
- **任务行**：`- [ ] N.M 任务描述` 或 `- [x] N.M 任务描述`——N.M 为纯数字，不能是 `**1.1**` 等。

治理清单常用写法不满足上述格式，导致解析出 0 条任务，dispatch 阶段无任务可派发。

## 风险与后果

- 误以为「run 已执行并派发子 Agent」，实际仅跑通工作流节点与门控；
- 复盘时难以区分「刻意不派发」与「格式错误导致未派发」。

## 建议做法（如何规避）

1. **若期望 run 时派发子 Agent**：tasks.md 须采用 **OpenSpec 4.4** 规定的运行后端可识别格式（见 `memory/patterns/pattern-run-execution-determinism.md`）。
2. **若本变更仅跑通流程、不派发**：可在迭代日志中明确注明「任务数=0、未派发」，避免与「格式错误导致 0 派发」混淆。
3. **新建变更时**：若计划使用 run_langgraph 且需派发，在编写 tasks.md 时即按 OpenSpec 4.4 与 parser 约定书写，避免事后返工。
