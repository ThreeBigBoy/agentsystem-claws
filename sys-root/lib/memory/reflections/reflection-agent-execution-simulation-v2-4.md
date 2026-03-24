---
id: mem-reflection-agent-execution-simulation-v2-4
title: Agent 执行 projects-rules 的模拟与反思（V2.4）
type: reflection
tags: [projects-rules, iteration-log, change-id, execution-simulation]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, continue, openai-codex, generic]
source_change_ids: [project-early-phase]
created_at: 2026-03-13
last_reviewed_at: 2026-03-13
maturity: draft
owner: @billhu
related:
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/patterns/pattern-task-complexity-judgement-and-mode-switch.md
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
---

# Agent 执行 projects-rules 的模拟与反思（V2.4）

## 背景

在 V2.2–V2.3 阶段，曾对 `global-rules/projects-rules-for-agent.md` 做过一次「从 AI 视角出发的全过程执行模拟」，覆盖新建变更、推进 tasks、单次小改、项目前期等多个场景，并从中抽取改进点。  
原始模拟文档篇幅较长且带有强烈「案例与反思」属性，更适合作为长期记忆条目在需要时按需加载，而不是始终与规则正文一起占用上下文。

## 主要发现与结论（按场景归纳）

1. **场景 A：新需求 / 新建变更**  
   - 能够通过任务类型 → 执行方 → 技能矩阵，找到产品经理 Agent + request-analysis，并强制「先读 SKILL 再执行」；  
   - 变更入口与迭代日志收尾在规则层有明确条款，但 change-id 的确定时机与问法需要在规则与实践中进一步澄清。

2. **场景 B：推进既有 tasks（如 2.2）**  
   - 能依赖 `tasks.md` 中的负责人字段决定执行方，并通过 SKILL 与收尾约定保证实现与日志记录；  
   - 对「验收通过后谁勾选 tasks」等细节更适合在项目级约定中描述，而非写死在全局规则。

3. **场景 C：单次小改动（如改一段代码为 TypeScript）**  
   - 在有项目上下文但未指明变更单时，规则建议归属 `project-early-phase` 并记录迭代日志；  
   - 对「是否所有项目内操作都必须有 change-id」的执行边界，需要在 simple/heavy 模式下做更精细判定。

4. **场景 D：项目前期工作（project-early-phase）**  
   - 明确要求创建 `docs/project-early-phase/`，并对立项研究、需求分析等所有调用记录迭代日志；  
   - 强调只有在不处于任何项目上下文时才可跳过迭代日志与收尾。

## 对规则文档的改进建议（已在 V2.3/V2.4 逐步落实）

1. **路径不可达时的降级路径**  
   - 若无法访问 `agentsystem/OpenSpec.md` 或 `skills/`，应退回当前项目 `.cursorrules` / `openspec/AGENTS.md` 与本项目内文档；  
   - 该建议已写入 `projects-rules-for-agent.md`，并通过 adapter 文档补充说明。

2. **自检与迭代日志收尾收紧**  
   - 将自检逻辑收紧为「产出完成后、完成性回复前必须追加迭代日志」，并禁止先说完成再补录；  
   - 通过主 Agent 与子 Agent 的收尾约定强化执行力。

3. **change-id 一致性**  
   - 所有项目从一开始的所有任务都须有 change-id，项目前期统一使用 `project-early-phase`；  
   - 这一点已在 OpenSpec 与 projects-rules 中统一。

4. **simple/heavy 模式下的执行差异**  
   - 反思指出：并非所有场景都适合同一强度的规则加载与日志记录；  
   - V2.4 中通过「任务复杂度判定 + 渐进式规则/memory 加载」设计，允许在 simple 任务下用更轻量的策略执行，同时在 heavy 任务下保持严格治理。

## 对后续迭代的建议

1. 将本条目作为「执行模拟与反思」的主入口，逐步从 `projects-rules-for-agent.md` 与历史执行模拟文档中剥离长篇模拟正文，只保留链接与结论摘要。  
2. 若未来在其他项目中发现新的执行问题或经验，可在本条目基础上追加新的小节或拆分成更细粒度的 reflection/pattern 条目。  
3. 在重规则任务中，当主 Agent 需要回顾规则的实战效果或典型坑点时，可按需加载本条目辅助决策，而无需长期将整份模拟文档驻留在上下文中。

## 关联模式

- 若你在复盘某次「projects-rules 执行效果」或 OpenSpec 变更落地过程时，可配合以下条目一起使用：  
  - `memory/patterns/pattern-openspec-change-workflow.md`：对照标准变更流程，检查是否有步骤被跳过或弱化；  
  - `memory/patterns/pattern-task-complexity-judgement-and-mode-switch.md`：分析当时的 simple/heavy 判定与切换是否合理；  
  - `memory/patterns/pattern-iteration-log-enforcement-and-usage.md`：确认迭代日志执行是否达标。  
- 通过这些联动，可以从一次具体执行模拟反推 rules、OpenSpec 流程与执行习惯三层是否协同。

