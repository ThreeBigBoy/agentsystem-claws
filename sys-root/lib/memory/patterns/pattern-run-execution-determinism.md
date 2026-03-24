---
id: mem-pattern-run-execution-determinism
title: run 执行确定性——保障每次 run_langgraph 可追溯、可派发
type: pattern
tags: [run-langgraph, determinism, tasks-format, iteration-log]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [deepen-langgraph-v2-11-2]
created_at: "2026-03-19"
last_reviewed_at: "2026-03-19"
maturity: stable
related:
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
  - memory/anti-patterns/anti-pattern-tasks-md-checklist-format-zero-dispatch.md
---

# run 执行确定性——保障每次 run_langgraph 可追溯、可派发

## 背景

当变更通过 MCP 或运行后端 **run_langgraph** 执行时，若未事先满足三项约定，会出现：运行留痕与迭代日志脱节、任务数=0 不派发子 Agent、需求文档与工作流检查不一致。本 pattern 将「未来每次都不出问题」归纳为**三条强制/推荐动作**，供新建或推进变更时加载。

## 三条约定（未来每次 run 均须满足）

### 1. 需求文档命名与工作流检查一致

- **规则**：docs/project-prd-changes 下主需求文档建议采用 **PRD-[change-id]-[关键词].md**，与 workflow Step 1 前置检查（PRD-{change_id}*.md）及 OpenSpec Step 1 产出规范一致。
- **否则**：需额外维护一份「仅用于通过检查」的 PRD 占位文件，易遗漏或与主需求脱节。

### 2. 若需 run 时派发子 Agent，tasks.md 须采用运行后端可识别格式

- **规则**：见 **OpenSpec 4.4「与 run_langgraph 派发一致」**：章节为 `## N. 标题（Executor）」，任务行为为 `- [ ] N.M 任务描述`（N.M 为数字，非 `**1.1**`）；实现以 `agent_team_project/langgraph_backend/parser.py` 为准。
- **否则**：parser 解析出 0 条任务，dispatch 不派发任何子 Agent，run 仅跑通节点与门控（参见 `memory/anti-patterns/anti-pattern-tasks-md-checklist-format-zero-dispatch.md`）。
- **例外**：仅跑通流程、不派发子 Agent 的变更（如治理审查）可不满足格式，但建议在迭代日志中注明「任务数=0、未派发」。

### 3. run_langgraph 调用后须在迭代日志中追加一条

- **规则**：见 **global-rules/projects-rules-for-agent.md 第三节**：凡通过 MCP 或运行后端执行 run_langgraph 后，须在 `docs/项目事件日志.md` 追加一条，注明 change_id、本次 run 的 status、任务数（task_count），以及运行留痕路径（若有：`runtime-logs/langgraph-runs/YYYY-MM-DD.jsonl`）。
- **否则**：与后端留痕无法对应，复盘与审计时难以确认「是否真的跑过、结果如何」。

## 何时加载本 pattern

- 新建变更且**计划使用 run_langgraph** 推进时；
- 编写或评审 **tasks.md** 且期望 run 时**向子 Agent 派发任务**时；
- 执行 **run_langgraph** 后做收尾时（自检是否已写迭代日志、是否注明任务数/status/runtime-logs 路径）。

## 与规范的关系

- **OpenSpec 4.4**：已增加「与 run_langgraph 派发一致」格式约定，为本 pattern 的权威来源。
- **projects-rules 第三节**：已约定 run_langgraph 调用须记入迭代日志及（若需派发）tasks.md 格式指向本 pattern。
- **反思**：`docs/project-prd-changes/deepen-langgraph-v2-11-2/records/反思-执行确定性漏洞与修复-v2-11-2.md` 记录了本次漏洞与修复过程，可作为案例引用。
