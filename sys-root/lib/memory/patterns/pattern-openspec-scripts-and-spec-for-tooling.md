---
id: mem-pattern-openspec-scripts-and-spec-for-tooling
type: pattern
title: OpenSpec 下脚本存放与工具类变更的 spec 增量
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [check-langgraph-backend]
tags: [openspec, scripts, spec, tooling, change]
created_at: "2026-03-14"
last_reviewed_at: "2026-03-14"
maturity: stable
related:
  - memory/reflections/reflection-check-langgraph-backend-script-implementation.md
  - memory/patterns/pattern-scenario-memory-trigger-governance.md
  - memory/patterns/pattern-openspec-change-workflow.md
---

# OpenSpec 下脚本存放与工具类变更的 spec 增量

## 背景与适用场景

新建变更的产出若包含**自动化脚本**或**工具型代码**（如自检脚本、迁移脚本、CLI 小工具），常出现两类问题：(1) 脚本放在子项目目录（如 agent_team_project/scripts/）或仓库根散落，与 OpenSpec 约定不一致；(2) 认为「只是脚本、不涉及能力」而未在 changes 下写 spec，导致需求→spec→实现→验收追溯断链。本条沉淀自 change-id `check-langgraph-backend` 的落地与用户质疑后的修正，供新建「含脚本/工具产出」的变更时自检。

## 推荐做法（Checklist）

### 1. 脚本存放路径与结构

- **位置**：脚本必须放在**项目根**下的 **scripts/**（OpenSpec：项目根目录下的标准子目录，统一存放自动化脚本）。不得仅放在子模块目录（如 agent_team_project/scripts/）作为唯一位置。
- **结构**：采用「一脚本（或一簇）一子目录」：
  - 在 **scripts/** 下新建子目录，如 **scripts/check-langgraph-backend/**；
  - 子目录内至少包含：**主脚本**（如 `check_langgraph_backend.py`）与 **README.md**（用途、用法、参数、与 openspec/changes 的对应）；
  - 与现有 scripts 子目录（如 cursor-usage-to-iteration-log、memory、runtime-logging）风格一致，便于检索与维护。
- **引用**：proposal、tasks、spec、design、scripts/README.md 中凡涉及脚本路径，一律使用 **scripts/<子目录>/<脚本名>**，避免写成本仓根下单文件（如 scripts/xxx.py）除非该子目录仅一层。

### 2. 工具类变更的 spec 增量

- **判断**：若本变更的产出是对**某一既有 capability 的扩展**（例如在 langgraph-backend 能力下新增「自检脚本」），则视为对该 capability 有**增量**，不是「Affected specs: 无」。
- **必须**：在 **openspec/changes/[change-id]/specs/[capability]/spec.md** 中编写本变更的增量：
  - 变更类型一般为 **MODIFIED**（在既有能力下补充 Requirement/Scenario）；
  - 内容需包含：补充的 Requirement 描述、至少一个 Scenario（GIVEN/WHEN/THEN），以及对应需求文档/验收的引用；
  - proposal 的 **Affected specs** 须写明该 capability 及「MODIFIED：…」，并指向上述 spec 路径。
- **验收**：func-test 或自检执行时，以 spec 中的 Scenario 与 tasks.md、docs/project-prd-changes 下验收标准一致为通过依据。

## 反例与常见误区

- **误区**：把脚本只放在 agent_team_project/scripts/ 或仓库根单文件，导致与 OpenSpec「项目根 scripts/ 统一存放」不一致，且与现有多子目录结构不统一。
- **误区**：以「只是脚本、不改变核心能力」为由不建 spec；工具/脚本若归属某 capability，不写 spec 会导致主 specs 与实现不同步、追溯链断裂。
- **误区**：proposal 写「Affected specs: 无」却实际扩展了某能力；应建 specs/[capability]/spec.md 并更新 Affected specs。

## 与现有规范的关系

- OpenSpec 文档定位表：`/scripts/` 为项目根下标准子目录；4.6 节：changes 下 specs/[capability]/spec.md 描述对该能力的增量。
- 新建变更流程见 `pattern-openspec-change-workflow.md`；本 pattern 在「变更产出含脚本/工具」时作为补充自检。
- 场景绑定：在「新建 OpenSpec 变更 / 新建 change-id」且产出含脚本或工具时，除既有变更流程外，应参照本条核对 scripts 路径与 spec 增量。

## 关联模式

- 落地过程与两项质疑的详细复盘见 `reflection-check-langgraph-backend-script-implementation.md`。
- 场景与记忆触发见 `pattern-scenario-memory-trigger-governance.md`（新建变更场景可联动本条）。
