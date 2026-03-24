---
type: reflection
title: runtime-logs 与 memory 协作的实践反思（V2.4）
change-id: sys-rules-memory-refactor-v2-4
tags: [reflection, runtime-logs, memory]
applicable-projects: [agentsystem]
host-scope: [cursor, vscode]
related:
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
  - memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md
  - memory/anti-patterns/anti-pattern-missing-iteration-log-in-agent-calls.md
  - memory/anti-patterns/anti-pattern-runtime-logs-business-data-pitfall.md
---

# runtime-logs 与 memory 协作的实践反思（V2.4）

## 背景

- 在 V2.3–V2.4 的设计中，`runtime-logs/` 与 `memory/` 被引入作为「执行过程与长期经验」的两大补充层：  
  - runtime-logs：记录模型调用与系统事件，用于成本与可靠性分析；  
  - memory：沉淀可跨 change-id / 跨项目复用的模式、反模式、偏好与剧本。  
- 同时，`docs/项目事件日志.md` 承担「业务侧 Agent/技能调用过程」记录职责。

本反思旨在总结这三者之间的协作关系与容易踩的坑，以指导后续项目复用。

## 三层记录的分工反思

1. **迭代日志（docs/项目事件日志.md）**  
   - 面向业务与治理：记录「谁在什么时候、为哪个 change-id 调用了哪个 Agent/技能，产出了什么」。  
   - 粒度：每一次 Agent/技能调用一条记录，强调可追溯性与简洁性。  
2. **runtime-logs（runtime-logs/model-calls & system-events）**  
   - 面向执行与成本分析：记录「在某个宿主/模型家族下，具体模型调用情况、错误/限流/降级等事件」。  
   - 粒度：通常一条记录对应一次或一段「模型调用事件」，可按 day/change-id/host 做聚合统计。  
3. **memory（memory/patterns / anti-patterns / reflections / preferences 等）**  
   - 面向长期经验沉淀：从多次迭代日志与 runtime-logs 中抽象出「通用模式与教训」，供后续任务直接调用。  
   - 粒度：一条 memory 是一条可复用的知识条目，而不是对某次事件的逐字记录。

## 典型协作流程反思

1. **单次重要 Agent 调用**  
   - 先在迭代日志中追加一条记录，覆盖 change-id / Agent / 技能 / 任务 / 输出 / 模型；  
   - 若该次调用满足 runtime-logs 触发条件（关键阶段、成本关切、错误/限流等），再调用脚本往 runtime-logs 追加一条记录。  
2. **跨多轮迭代后的模式抽取**  
   - 在某个 change-id 的复盘记录中，发现同类问题/实践反复出现；  
   - 基于多条迭代日志 + 必要的 runtime-logs 统计，抽象出一条或多条 memory（pattern / anti-pattern / reflection），并在复盘文档中链接这些条目。  
3. **下一轮任务的起步**  
   - 在新任务开始前，主 Agent 可按主题/标签检索 memory（如「runtime-logs」「iteration-log」「quota」等），  
   - 将命中的模式/反思作为「轻量知识入口」，在 simple 模式下就能复用，而无需一次性读完所有厚规则。

## 易错点与改进建议

1. **只记 runtime-logs，不记迭代日志**  
   - 结果是有模型调用数据，却难以从业务/变更视角复盘。  
   - 建议：所有与 change-id 相关的 Agent/技能调用，迭代日志为必须，runtime-logs 为在特定触发条件下的补充。  
2. **把 memory 当成「笔记本」，而不是「模式库」**  
   - 若 memory 条目只是事件流水，而非抽象出的模式/反思，会降低后续检索与复用价值。  
   - 建议：写 memory 时以「可复用模式/教训」为中心，不复刻原始事件细节。  
3. **缺少从 logs → memory 的闭环动作**  
   - 迭代日志和 runtime-logs 积累很多，但从未系统性整理成 memory，导致经验无法真正沉淀。  
   - 建议：在 change-id 的 records/ 复盘中，显式检查是否有值得抽象为 memory 的内容，并记录已创建的 memory 链接。

## 与当前规则的勾连

- 迭代日志的硬性要求与结构来自 `projects-rules-for-agent.md` 第三章；  
- runtime-logs 的触发条件与脚本接口说明来自 `platform-adapters/*/runtime-logging-implementation.md` 与相关脚本 README；  
- 本反思条目与以下 memory 条目形成组合：  
  - `memory/patterns/pattern-iteration-log-enforcement-and-usage.md`  
  - `memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md`  
  - 与 runtime-logs 业务数据边界相关的 anti-pattern 条目等。

## 关联模式

- 若你在某个 change-id 的复盘中，想系统性检查「记录层 → 经验层 → 规则层」是否协同良好，可按以下顺序联动：  
  1. `memory/patterns/pattern-iteration-log-enforcement-and-usage.md`：保证迭代日志执行到位；  
  2. `memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md`：按需补 runtime-logs，避免信息噪音；  
  3. `memory/anti-patterns/anti-pattern-runtime-logs-business-data-pitfall.md`：校验运行日志中是否混入业务敏感数据；  
  4. `memory/patterns/pattern-rules-and-memory-evolution-governance.md`：如发现习惯性问题，评估是否需要在 rules 与 memory 层做结构性调整。  
- 通过这组模式联动，可以从一次具体异常出发，一步步走到规则与记忆体系的结构性优化。

