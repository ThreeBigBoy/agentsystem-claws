---
id: mem-reflection-check-langgraph-backend-script
type: reflection
title: 一键自检脚本（check-langgraph-backend）落地复盘与质疑回应
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [check-langgraph-backend]
tags: [openspec, scripts, spec, change-implementation, reflection]
created_at: "2026-03-14"
last_reviewed_at: "2026-03-14"
maturity: stable
related:
  - memory/patterns/pattern-openspec-scripts-and-spec-for-tooling.md
  - memory/patterns/pattern-scenario-memory-trigger-governance.md
  - memory/patterns/pattern-openspec-change-workflow.md
---

# 一键自检脚本（check-langgraph-backend）落地复盘与质疑回应

## 落地过程简述

变更 `check-langgraph-backend` 目标为实现 LangGraph 后端「一键自检」脚本，自动执行：GET /health、AGENT_TEAM_PROJECT_ROOT 校验、LANGGRAPH_WORKSPACE_PROJECTS 解析与目录校验、本仓/业务项目各一次 /run 与留痕检查。按 OpenSpec 第六节先建 docs/project-prd-changes、再建 openspec/changes，并实现脚本。落地过程中用户提出**两项关键质疑**，经修正后形成可复用方法论。

---

## 质疑一：脚本存放路径

**质疑要点**：脚本为何先放在 `agent_team_project/scripts/`？是否应统一放在 `agentsystem/scripts/`？之后进一步：为何没有在 `scripts/` 下为脚本**建一个子目录**，并把 .py 与 README 放在该子目录下？

**回应与修正**：

1. **项目根 scripts/ 优先**  
   OpenSpec 明确约定：`/scripts/` 为**项目根目录下的标准子目录**，统一存放该项目的自动化脚本。因此脚本应放在 **agentsystem/scripts/**，而不是 agent_team_project/scripts/（后者属于子模块，非项目根约定位置）。已迁移至本仓根 `scripts/`。

2. **子目录 + .py + README 一致结构**  
   本仓已有 `scripts/cursor-usage-to-iteration-log/`、`scripts/memory/`、`scripts/runtime-logging/` 等，均为「子目录内放脚本与 README」的结构。为保持与现有脚本组织一致、便于单脚本独立说明与引用，应增加 **scripts/check-langgraph-backend/**，其下放置 `check_langgraph_backend.py` 与 `README.md`，而非在 scripts/ 根下单文件。已按此结构调整并更新所有引用（proposal、tasks、spec、design、scripts/README.md）。

**方法论**：新建脚本时，(1) 一律放在项目根 **scripts/**；(2) 按「一脚本（或一簇）一子目录」建子目录，子目录内含 .py 与 README.md，与既有 scripts 子目录风格一致。

---

## 质疑二：没有存放 spec.md

**质疑要点**：openspec/changes/check-langgraph-backend 下为何没有创建 spec.md？

**回应与修正**：

1. **初始约定**：proposal 中写「Affected specs: 无（工具脚本，不改变 langgraph-backend 能力）」，故未建 changes 下 specs/。  
2. **OpenSpec 4.6 要求**：changes 下的 **specs/[capability]/spec.md** 用于描述本变更对某能力的**增量**（ADDED/MODIFIED/REMOVED），是需求→spec→实现→验收追溯的一环。只要变更**对某一 capability 有增量**（包括在该能力下新增工具/脚本），就应在对应 changes 下建 spec 增量，而不是留空。  
3. **修正**：补建 **openspec/changes/check-langgraph-backend/specs/langgraph-backend/spec.md**，变更类型为 MODIFIED，在「LangGraph 独立后端服务」下补充「自检工具」Requirement 与 Scenario；并更新 proposal 的 Affected specs 为「langgraph-backend（MODIFIED）」。

**方法论**：凡变更产出为「某能力下的工具、脚本或辅助能力」，即对既有 capability 有扩展时，**不应**简单标「Affected specs: 无」；应在 **openspec/changes/[change-id]/specs/[capability]/spec.md** 中写清增量（如 MODIFIED + 新 Requirement/Scenario），保证可追溯与验收有据。

---

## 小结与联动

- **路径与结构**：脚本统一在项目根 **scripts/**，且按**子目录（含 .py + README）**组织，与现有 scripts 子目录一致。  
- **Spec 增量**：工具/脚本类变更若归属某 capability，须在 changes 下建 **specs/[capability]/spec.md**，避免「无 spec」导致追溯断链。  
- 上述方法论已沉淀为 **pattern-openspec-scripts-and-spec-for-tooling.md**，供「新建含脚本/工具产出的变更」时触发加载。
