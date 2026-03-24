---
id: pattern-change-full-lifecycle-delivery
type: pattern
title: 变更完整落地闭环（从方案评审到 code review 的节奏与产出）
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [migrate-langgraph-backend]
tags: [openspec, change-lifecycle, delivery, review, acceptance]
created_at: "2026-03-14"
last_reviewed_at: "2026-03-14"
maturity: draft
related:
  - memory/patterns/pattern-change-pre-implementation-review.md
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/patterns/pattern-openspec-archive-and-specs-sync.md
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
  - memory/reflections/reflection-change-full-lifecycle-migrate-langgraph.md
---

# 变更完整落地闭环（从方案评审到 code review 的节奏与产出）

## 背景与适用场景

适用于**单次 change-id 从方案到交付的完整落地**：含架构/后端/前端、测试验收、废弃与迁移（若有）、以及 code review。本条提炼自 `migrate-langgraph-backend` 的落地过程，供主 Agent 推进类似变更时按阶段自检产出与顺序。

## 推荐顺序与产出（Checklist）

按以下顺序执行，每步完成后在 `tasks.md` 中勾选对应项，并在 `docs/项目事件日志.md` 追加一条记录：

1. **变更启动**（主 Agent）
   - 先建 `docs/project-prd-changes/[change-id]/`，再建 `openspec/changes/[change-id]/`；proposal 引用 docs/project-prd-changes；tasks、design、spec 齐全。
   - 产出：迭代需求说明、proposal、tasks、design、spec。

2. **实施前方案评审**（主 Agent，heavy 时必做）
   - 按 `pattern-change-pre-implementation-review` 执行：OpenSpec 6.2、规则/记忆审视、四维方案、文档一致、任务统计一致。
   - 产出：`docs/project-prd-changes/[change-id]/records/[change-id]-方案评审记录.md`；同步更新需求/环境/任务统计等。

3. **架构设计**（架构 Agent）
   - 产出：design.md 关键章节（如状态图、接口、检查点）、可选 architecture/*.mmd；tasks 中架构项勾选。

4. **后端实现**（后端 Agent）
   - 产出：代码与 README；tasks 中后端项勾选。

5. **前端/MCP 集成**（前端 Agent）
   - 产出：MCP/扩展侧代码、配置模板与宿主文档更新；tasks 中前端项勾选。

6. **测试与验收**（测试 Agent）
   - 按 func-test 技能产出：`docs/project-prd-changes/[change-id]/records/[change-id]-func-test.md`。
   - **对「需人工判定」或「未通过」项**：编写「最小验收脚本」MD（同 records 目录），用可复制命令与步骤指导用户自验或代执行；执行结果回填验收记录表。若当轮可实现缺失能力（如断点续跑），实现后再更新验收结论。

7. **废弃与迁移**（若有）（主/架构 Agent）
   - 旧机制：代码与入口处 DEPRECATED 注释、README/宿主文档标明推荐路径；独立 `MIGRATION.md`（为何迁、兼容期、迁移步骤、旧配置处理）；兼容期约定（如 1 个月）。
   - 产出：注释与文档更新、MIGRATION.md；tasks 中废弃/迁移项勾选。

8. **Code Review**（架构 Agent）
   - 按 code-review 技能产出：`docs/project-prd-changes/[change-id]/records/[change-id]-code-review.md`。
   - 结论与问题清单（Blocking/Major/Minor）；Blocking/Major 须进 tasks；Minor 可后续迭代纳入。

9. **闭环确认与归档**
   - 所有 tasks 已勾选；迭代日志覆盖各阶段；验收与评审记录齐全。
   - 使用 OpenSpec CLI 归档：按 `pattern-openspec-archive-and-specs-sync` 执行（有 delta 且仅 ADDED 时直接 `archive --yes`；新建 capability 且 spec 含 MODIFIED/REMOVED 时用 `--skip-specs --yes` 后手动合并 ADDED 到 `openspec/specs/`）；归档后追加迭代日志。
   - 可选收尾：落实 Minor 改进并回归测试；同步新用户手册/playbook 与场景绑定，并转化为 memory。

## 反例与常见误区

- **跳过实施前评审**：heavy 变更若直接按 tasks 开干，易出现环境/任务统计/文档口径不一致，中段返工。
- **验收「需人工/未通过」不落脚本**：仅写在报告里不提供可执行步骤，用户无法自验或回归，验收结论难以复现。
- **废弃只改代码不写迁移指南**：用户不知如何从旧机制切到新机制，兼容期内容易混淆。
- **阶段完成不追迭代日志**：难以证明变更闭环与各角色参与顺序，不符合 OpenSpec 与迭代日志约定。

## 与规范/技能的关系

- 变更启动顺序见 `OpenSpec.md` 第六节与 `pattern-openspec-change-workflow`。
- 实施前评审见 `pattern-change-pre-implementation-review`；场景绑定见 `pattern-scenario-memory-trigger-governance`。
- 迭代日志每步追加见 `pattern-iteration-log-enforcement-and-usage`。
- func-test、code-review 产出路径与最小结构见各自 SKILL.md 与 REFERENCE。

## 关联模式

- 复盘单次变更完整落地时，可读 `reflection-change-full-lifecycle-migrate-langgraph` 对照阶段与决策。
- 实施前是否做方案评审，由「变更实施前方案评审」场景与 heavy 判定决定，见 `pattern-change-pre-implementation-review` 与 `pattern-scenario-memory-trigger-governance`。
