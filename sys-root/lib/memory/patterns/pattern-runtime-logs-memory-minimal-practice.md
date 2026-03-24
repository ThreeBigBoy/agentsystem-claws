---
id: mem-pattern-20260313-132108
title: runtime-logs 与 memory 能力落地的最小实践
type: pattern
tags: [runtime-logs, memory, agentsystem]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode]
source_change_ids: [sys-infra-memory-v1]
created_at: 2026-03-13
last_reviewed_at: 2026-03-13
maturity: draft
owner: @billhu
---

# runtime-logs 与 memory 能力落地的最小实践

## 背景与适用场景

在 agentsystem 中首次落地「运行日志 + 长期记忆」能力（V2.3 / change-id: sys-infra-memory-v1）时，需要同时建立目录、脚本、规则与验收闭环。本条目总结可复用的最小实践，适用于后续在本仓或他仓引入同类能力时参考。

## 推荐做法（步骤 / Checklist）

1. **目录与约定**
   - 在仓库根下建立 `runtime-logs/`（含 `model-calls/`、`system-events/`）和 `memory/`（含 `patterns/`、`anti-patterns/`、`preferences/`、`playbooks/`、`reflections/`）。
   - 为 `memory/` 定义 frontmatter 规范（见 `memory/schema.md`），统一 id、type、tags、applicable_projects、host_scope、source_change_ids 等字段。

2. **脚本接口**
   - 运行日志：提供统一脚本（如 `scripts/runtime-logging/append_cursor_model_call.py`），支持 `--change-id`、`--agent-role`、`--skill`、`--host` 等参数，由主 Agent 在满足规则时通过 Shell 调用。
   - 长期记忆：提供 `scripts/memory/create_memory_entry.py`，按 `--type`（pattern/anti-pattern/preference/playbook/reflection）生成带 frontmatter 与小节骨架的 Markdown 文件；实质性正文由人工或 Agent 后续填写。

3. **主 Agent 规则**
   - 在 `agents/主Agent.md` 中明确：何时写 runtime-logs（如 change-id 关键阶段、成本/错误相关）、何时考虑沉淀 memory（跨 change 可复用、高抽象、用户意图），以及 preference 类需用户确认。

4. **验收闭环**
   - 设计最小验收脚本（如写业务迭代日志 → 调用 append 脚本写入 model-calls → 按规则判定并调用 create_memory_entry 生成一条 memory），执行一遍并据此微调规则与文档。

## 反例与常见误区（如有）

- 仅建目录和 README 而不提供可执行脚本，主 Agent 无法自动触发写入。
- 把业务数据或敏感信息写入 runtime-logs；应只记录技术指标（如 token、耗时、status）。
- 用脚本生成 memory 后不补写正文，导致条目只有标题无实质内容，检索到也难以复用；生成后应尽快填写「背景与适用场景」「推荐做法」等段落。

## 与现有规范/技能的关系

- 遵循 `OpenSpec.md`、`global-rules/projects-rules-for-agent.md`、`agents/主Agent.md`。
- 宿主侧实现见 `platform-adapters/<host>/runtime-logging-implementation.md` 与 `memory-implementation.md`。
- 汇总/查看运行日志可使用 `scripts/runtime-logging/summarize_model_calls.py`（如 `--group-by day` / `change-id` / `host`）。

