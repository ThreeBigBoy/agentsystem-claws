---
id: pattern-change-pre-implementation-review
type: pattern
title: 变更实施前方案详细评审（重规则场景）
applicable_projects:
  - agentsystem
  - generic-product-projects
source_change_ids:
  - migrate-langgraph-backend
tags:
  - review
  - openspec
  - governance
  - heavy-task
created_at: "2026-03-14"
last_reviewed_at: "2026-03-14"
maturity: draft
related:
  - memory/patterns/pattern-rules-and-memory-evolution-governance.md
  - memory/patterns/pattern-scenario-memory-trigger-governance.md
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/patterns/pattern-product-requirement-review-4d-checklist.md
---

# 变更实施前方案详细评审（重规则场景）

## 背景与适用场景

在 **按 tasks.md 实施前**，对已创建的变更（含迭代需求说明、proposal、tasks、design、spec）做一轮结构化方案评审，可查缺补漏、统一文档口径、避免实施中返工。适用于：

- **重规则（heavy）任务**：与某 change-id 的完整迭代链路强绑定、多 Agent × 多 Skill 协作、或涉及架构/基础设施的变更；
- 用户或主 Agent 明确要求「实施前先做方案评审」「查缺补漏」；
- 变更涉及规则层/记忆层/入口文档可能联动更新时（如基础设施迁移、运行后端切换）。

本条记忆来自 `migrate-langgraph-backend` 变更的实践：主 Agent 按全局规则与既有 pattern 执行实施前评审，产出评审记录、同步方案细节并沉淀本方法论。

## 推荐做法（步骤与 Checklist）

1. **按 heavy 加载规则与记忆**
   - 读取 `agents/主Agent.md`、`OpenSpec.md` 第六节与 4.3 节、`global-rules/projects-rules-for-agent.md` 相关段落；
   - 若涉及规则/记忆演进或提交前 review 场景，先读 `memory/patterns/pattern-rules-and-memory-evolution-governance.md` 与 `memory/patterns/pattern-scenario-memory-trigger-governance.md`，按其中 checklist 与「场景→绑定表」执行；
   - 可联动 `memory/patterns/pattern-product-requirement-review-4d-checklist.md`，将四维（必要性、合理性、优先级、内容质量）扩展到**方案级**（不仅 PRD，而是整个变更文档集）。

2. **执行五类审视**
   - **OpenSpec 6.2 变更启动检查清单**：5 项逐项核对（docs/project-prd-changes、proposal 引用、tasks 负责人与验收路径、迭代日志约定）；
   - **规则与记忆协同演进**：本变更是否改 rules？对应 SKILL/memory 是否已引用？README/新用户快速开始/宿主 SOP 是否需在交付后同步？
   - **四维方案评审**：必要性（是否直击痛点/目标）、合理性（技术选型与范围）、优先级（P0/P1 与周期是否匹配）、内容质量（是否达可执行/可验收粒度）；
   - **文档间一致性**：迭代需求说明 ↔ design.md ↔ spec ↔ tasks.md 在环境要求、依赖数量、接口、任务统计等是否一致；
   - **任务统计与明细一致**：tasks 中「任务统计」节的数字与各节可勾选子项数量一致（避免写「测试 Agent 4 个」实为 7 项等）。

3. **产出评审记录**
   - 在 `docs/project-prd-changes/[change-id]/records/` 下创建「方案评审记录」类文档（如 `[change-id]-方案评审记录.md`）；
   - 结构建议：评审元信息、OpenSpec 6.2 符合性、规则/记忆审视、四维结论、一致性检查、方案细节更新建议、风险再确认、方法论沉淀引用、评审结论与下一步。

4. **同步更新方案细节**
   - 将评审中发现的缺漏（如环境必须项、必装包数量、任务统计）回写到迭代需求说明、tasks.md、design.md、spec 等，保证实施前文档一致；
   - 交付后需同步的条目（如新用户快速开始、宿主 adapter）记入评审记录的「交付后建议」，便于闭环。

5. **沉淀方法论**
   - 若本次评审形成可复用步骤或 checklist，可新建或更新 memory 条目（如本 pattern），并在评审记录中引用，便于后续变更复用。

## 反例与常见误区

- **只做口头/对话内评审**：结论未落位于 `docs/project-prd-changes/[change-id]/records/`，后续无法追溯、易重复踩坑。
- **忽略文档间一致性**：迭代需求说明写「5 个必装包」、design 已改为「6 个必装 + 虚拟环境必须」，未同步则实施时环境纠纷。
- **任务统计与明细不符**：tasks 写「总任务数 19」「测试 Agent 4 个」，实际 4.1–4.7 为 7 项，导致进度统计与勾选混乱。
- **未按 heavy 加载规则**：未读 pattern-rules-and-memory-evolution 与场景绑定表，遗漏「交付后需更新 README/快速开始」等审视项。

## 与现有规范/技能的关系

- **OpenSpec**：第六节变更启动顺序与 6.2 检查清单是评审的必过项；
- **主 Agent**：实施前方案评审由主 Agent 执行，不替代架构/产品经理的专项评审，而是对「整套变更文档」做一致性、完整性、可执行性把关；
- **pattern-product-requirement-review-4d-checklist**：四维可扩展到方案级，必要性/合理性/优先级/内容质量不仅针对 PRD，也针对 proposal、design、spec、tasks 整体；
- **pattern-scenario-memory-trigger-governance**：「提交/合并前 review」场景可复用本 pattern 的审视项，并在场景表中将「变更实施前方案评审」与「必读本 pattern + 评审记录」绑定（由维护者按需添加）。

## 关联模式

- 执行本评审前，建议先读：
  - `memory/patterns/pattern-rules-and-memory-evolution-governance.md`：规则/记忆演进时的 checklist 与 README/SOP 审视；
  - `memory/patterns/pattern-scenario-memory-trigger-governance.md`：场景→必读 memory/必做 checklist 绑定；
- 评审中涉及「需求侧」完整性时，可联动 `memory/patterns/pattern-product-requirement-review-4d-checklist.md`；
- 评审完成后，若变更进入实施，执行方须按 `memory/patterns/pattern-openspec-change-workflow.md` 与 skills-rules 先读 SKILL 再执行。
