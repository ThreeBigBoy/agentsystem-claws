---
id: reflection-change-full-lifecycle-migrate-langgraph
type: reflection
title: 变更完整落地复盘——migrate-langgraph-backend 的方法论提炼
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [migrate-langgraph-backend]
tags: [openspec, change-lifecycle, migration, review, acceptance]
created_at: "2026-03-14"
last_reviewed_at: "2026-03-14"
maturity: draft
related:
  - memory/patterns/pattern-change-pre-implementation-review.md
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/patterns/pattern-change-full-lifecycle-delivery.md
  - memory/patterns/pattern-openspec-archive-and-specs-sync.md
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
---

# 变更完整落地复盘：migrate-langgraph-backend

## 1. 落地过程简述

`migrate-langgraph-backend` 从变更启动到 code review 闭环，完整经历了以下阶段（与迭代日志一一对应）：

| 阶段 | 执行方 | 主要动作 | 产出 |
|------|--------|----------|------|
| 变更启动 | 主 Agent | request-analysis / project-analysis；按 OpenSpec 先 docs/project-prd-changes 再 openspec/changes | 迭代需求说明、proposal、tasks、design、spec |
| 实施前方案评审 | 主 Agent | 重规则场景；OpenSpec 6.2、规则/记忆审视、四维方案、文档一致、任务统计 | 方案评审记录、需求/环境/任务统计同步；沉淀 pattern-change-pre-implementation-review |
| 架构设计 | 架构 Agent | project-analysis；状态图形式化、接口与检查点设计 | design.md §2.3/§5.2/§6.0、state-graph.mmd |
| 后端实现 | 后端 Agent | coding-implement；parser/workflow/executors/server | langgraph_backend/*.py、README |
| 前端/MCP 集成 | 前端 Agent | coding-implement；MCP 工具、模板与文档 | langgraph_mcp_server.py、mcp.template.json、mcp-setup §6 |
| 测试与验收 | 测试 Agent | func-test；用例与结果、需人工/未通过项记录 | func-test.md；当轮补充实现 POST /resume、最小验收脚本、代执行验收并更新记录 |
| 废弃与迁移 | 主/架构 Agent | deprecated 标记、迁移指南、兼容期、全流程审核 | DEPRECATED 注释、README/MCP 说明、MIGRATION.md、tasks 全勾选 |
| Code Review | 架构 Agent | code-review；需求/架构/质量/安全/鲁棒性 | code-review.md（通过，5 条 Minor） |

每阶段均在 `docs/项目事件日志.md` 追加一条记录，保证可追溯。

## 2. 关键决策与取舍

- **实施前先评审**：在按 tasks 动手前做一轮方案评审，统一环境要求、任务统计与文档口径，避免实施中返工；评审结论「通过」后再进入 1.1。
- **验收中补实现**：功能验收将「断点续跑 4.3」记为「已知未实现」后，用户要求当轮实现；遂在本迭代内完成 POST /resume、thread_id/checkpoint_id 返回、MCP resume_langgraph，并更新验收与脚本文档，避免遗留「已知限制」长期不闭环。
- **需人工/未通过项 → 最小验收脚本**：对 func-test 中「需人工判定」「未通过」的用例，单独写一份「最小验收脚本」MD（同目录），用可复制命令与步骤指导用户自验或代执行，并把执行结果回填到验收记录表，使验收可复现、可回归。
- **废弃与迁移一并交付**：deprecated 不仅代码注释，还包含 README/宿主 adapter 说明、独立 MIGRATION.md（为何迁、兼容期、步骤、旧配置处理）与兼容期约定，使用户有路径可循、双系统并存期内不困惑。

## 3. 可复用方法论总结

1. **顺序固定、产出可预期**：变更启动 → 实施前评审（heavy 时）→ 架构 → 后端 → 前端 → 测试 → 废弃/迁移（若有）→ code review；每步以 tasks 勾选与迭代日志为凭，便于主 Agent 推进与复盘。
2. **验收未闭环项的处理**：若验收报告存在「需人工判定」或「未通过（已知限制）」：优先考虑当轮是否可实现或部分实现（如 4.3）；无论是否实现，为这些项编写「最小验收脚本」MD，便于用户或后续回归执行并记录结果。
3. **迁移类变更的交付物**：除新能力外，旧机制需：代码/入口处 DEPRECATED 注释、README 与宿主文档标明推荐路径、独立 MIGRATION.md（步骤与兼容期）、兼容期内双系统可并存且文档明确。
4. **Code review 与 func-test 同目录**：评审记录与验收记录均放在 `docs/project-prd-changes/[change-id]/records/`，与方案评审、验收脚本等同属该变更，便于归档与综合决策；review 结论「通过」且无 Blocking/Major 时，Minor 可后续迭代纳入。

5. **OpenSpec CLI 归档与主 specs 同步**：新建 capability 且变更 spec 含 MODIFIED/REMOVED 时，CLI 不允许直接合并；应使用 `archive --skip-specs --yes` 完成目录移动，再手动将 ADDED 部分写入 `openspec/specs/[capability]/spec.md`，使主 specs 与已部署能力一致；无 specs 的变更（如工具/文档类）可直接归档，CLI 警告「至少一个 delta」仍会完成。详见 `pattern-openspec-archive-and-specs-sync`。

## 4. 与既有 memory 的衔接

- **实施前评审**：已沉淀为 `pattern-change-pre-implementation-review`，并在 `pattern-scenario-memory-trigger-governance` 中绑定「变更实施前方案评审」场景。
- **变更标准流程**：`pattern-openspec-change-workflow` 覆盖 change-id、docs/project-prd-changes 优先、tasks 推进与迭代日志；本复盘是对「单次变更从方案到 code review 全阶段」的细化与补充。
- **迭代日志**：每阶段完成后在给出「已完成/已闭环」类回复前追加迭代日志，符合 `pattern-iteration-log-enforcement-and-usage` 与 anti-pattern 避免缺失日志。

本条反思与 `pattern-change-full-lifecycle-delivery` 配合使用：复盘时引用本 reflection 梳理阶段与决策；执行新变更时按 pattern 的顺序与产出做自检与推进。
