---
id: mem-pattern-openspec-archive-and-specs-sync-001
type: pattern
title: OpenSpec CLI 归档与主 specs 同步
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [migrate-langgraph-backend]
tags: [openspec, archive, specs, cli]
created_at: "2026-03-14"
last_reviewed_at: "2026-03-14"
maturity: stable
related:
  - memory/patterns/pattern-change-full-lifecycle-delivery.md
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/reflections/reflection-change-full-lifecycle-migrate-langgraph.md
---

# OpenSpec CLI 归档与主 specs 同步

## 背景与适用场景

变更全部 tasks 完成、验收与 code review 通过后，使用 **OpenSpec CLI** 将变更正式归档，使 `openspec/changes/` 下仅保留进行中变更，已完成的移至 `openspec/changes/archive/YYYY-MM-DD-[name]/`。本条提炼自 `migrate-langgraph-backend`、`sys-infra-memory-v1` 的归档实践，供主 Agent 或维护者在执行「变更闭环 → 归档」时按步骤自检。

## 推荐做法（Checklist）

### 1. 归档前自检

- 该 change-id 下 **tasks.md 已全部勾选**；验收记录、code review 记录齐全（位于 `docs/project-prd-changes/[change-id]/records/`）。
- 若使用 **Fission-AI OpenSpec CLI**：`npx @fission-ai/openspec@latest archive <change-id> --yes`（或先 `openspec validate <change-id>` 可选）。

### 2. 两种归档情形与处理

| 情形 | CLI 行为 | 建议操作 |
|------|----------|----------|
| **变更含 specs/ 且仅 ADDED** | `openspec archive <id> --yes` 会移动目录并**自动合并** delta 到 `openspec/specs/` | 直接执行，无需额外步骤。 |
| **变更含 specs/ 但含 MODIFIED/REMOVED，且目标 capability 在 `openspec/specs/` 尚不存在** | CLI 报错：新建 spec 只允许 ADDED，合并中止，**不移动目录**。 | 使用 `openspec archive <id> --skip-specs --yes` 仅做**目录移动**；归档完成后**手动**将变更内 ADDED 部分合并到 `openspec/specs/[capability]/spec.md`，使主 specs 与当前已部署能力一致。 |
| **变更无 specs/ 目录** | CLI 提示「至少一个 delta」为**警告**，仍会完成归档（目录移动）。 | 无需合并主 specs；可选在文档中注明「工具/文档类变更，无 spec 增量」。 |

### 3. 归档后

- 变更目录位于 `openspec/changes/archive/YYYY-MM-DD-<change-id>/`，原 `openspec/changes/<change-id>/` 不再存在。
- 若曾使用 `--skip-specs`：确认 `openspec/specs/[capability]/spec.md` 已包含该变更的 ADDED 能力描述，与实现一致。
- 在 `docs/项目事件日志.md` 追加一条归档记录（含使用的命令与是否手动合并 specs）。

### 4. 归档后收尾（按需）

- **Minor 改进**：code review 中的 Minor 项可单列小任务或后续迭代落实；落实后做一次回归测试（含 parser/workflow 与 HTTP 接口），结果写入 `docs/project-prd-changes/[change-id]/records/` 下的回归记录。
- **文档与 memory**：若变更影响新用户路径（如新后端、新依赖、.env 配置），同步更新 `新用户快速开始.md`、playbook 或场景绑定表，并转化为 memory（playbook/pattern），便于后续「新用户/新环境」类问题时触发加载。

## 反例与常见误区

- **未区分「仅 ADDED」与「含 MODIFIED/REMOVED」**：直接 `archive --yes` 在新建 capability 且 spec 含 MODIFIED/REMOVED 时会中止且不移动目录；应改用 `--skip-specs` 再手动合并 ADDED。
- **跳过主 specs 同步**：用 `--skip-specs` 归档后若不再把 ADDED 写入 `openspec/specs/`，主 specs 与已部署能力会不一致，后续变更或新人难以以 specs 为准。
- **归档后不记迭代日志**：归档是闭环的一环，应在迭代日志中留痕（命令、结果、是否手动合并）。

## 与规范/技能的关系

- 变更完整落地节奏与产出见 `pattern-change-full-lifecycle-delivery` 第 9 步「闭环确认」；本条细化「如何执行归档」与「主 specs 如何同步」。
- OpenSpec 变更流程与 change-id 结构见 `OpenSpec.md` 与 `pattern-openspec-change-workflow`。
- 常用命令（本仓未全局安装 CLI 时）：`npx @fission-ai/openspec@latest archive <id> [--skip-specs] --yes`。

## 关联模式

- 变更从方案到 code review 的完整顺序与产出见 `pattern-change-full-lifecycle-delivery`；归档位于闭环最后一步。
- 单次变更落地的阶段与决策可对照 `reflection-change-full-lifecycle-migrate-langgraph`；归档与收尾经验已沉淀于本条 pattern。
