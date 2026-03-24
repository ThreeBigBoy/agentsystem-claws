---
type: anti-pattern
title: 在 Agent 调用中遗漏迭代日志记录
change-id: sys-rules-memory-refactor-v2-4
tags: [anti-pattern, iteration-log]
applicable-projects: [agentsystem]
host-scope: [cursor, vscode]
related:
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
  - memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md
---

# 在 Agent 调用中遗漏迭代日志记录

## 现象描述

在涉及某个 change-id 的任务中，Agent/技能已经实际执行并产出结果，但：

- `docs/项目事件日志.md` 中**没有对应记录**，或记录严重滞后；  
- 记录内容缺少 change-id/技能/模型信息，无法与实际执行过程一一对应；  
- 多次调用复用同一个 change-id，但仅第一次或少数几次有记录。

## 典型触发场景

1. **「只是改一小点」的心态**  
   - 在原本属于 heavy 的 change-id 上，执行了看似微小的修修补补（如补注释、调整字段等），觉得「不用再记日志了」。  
2. **多轮对话拆分执行**  
   - 第一次调用时有记录，后续多轮继续推进同一 change-id 但忘记新增记录。  
3. **上下文切换频繁**  
   - 在不同 change-id 之间来回切换，导致忘记当前执行属于哪个 change-id，最后干脆不记或记错地方。  
4. **只在「阶段性大事件」时记日志**  
   - 只在「需求分析完成」「验收完成」这类节点记，而忽略了中间关键调用（如修复 Blocking 问题）。

## 风险与后果

- **可追溯性下降**：无法准确还原每次 Agent/技能调用的时间点、职责与产出，复盘困难。  
- **变更闭环难以证明**：对于需要对 change-id 做整体验收或审计的场景，缺乏连续、可信的执行记录。  
- **难以优化规则与记忆**：迭代日志是 runtime-logs 与 memory 沉淀的重要数据源，缺失会直接影响后续统计与模式抽取。

## 建议做法（如何规避）

1. **把迭代日志写入当作「收尾强制步骤」**  
   - 在任何 change-id 上下文中，只要调用了 Agent 或技能并产出结果，在给出「已完成/已闭环/请验收」等总结性回复之前，先检查并补全迭代日志记录。  
2. **保持单条记录简洁一致**  
   - 使用统一的最小结构：时间 + Agent + 技能 + 任务 + 输出 + 模型；  
   - 避免在一条记录中堆砌过多细节，把更多解释放到 `docs/project-prd-changes/[change-id]/records/` 中的专门记录文件里。  
3. **利用脚本和模板降低心智负担**  
   - 尽量使用统一脚本或模版生成日志行，减少手写差异和遗漏字段的风险。  
4. **多 change-id 场景下显式标注**  
   - 在对话与记录中频繁提到当前 change-id，防止混淆；  
   - 若切换 change-id，应在迭代日志中清晰记录每次调用归属的 change-id。

## 相关正向模式

- `memory/patterns/pattern-iteration-log-enforcement-and-usage.md`：给出了迭代日志记录范围、最小结构与执行时机的推荐模式。  
- 与 runtime-logs 相关的模式：说明何时在迭代日志之外追加 runtime-logs 记录，以支持后续统计与分析。

## 关联模式

- 当你发现某个 change-id 的迭代日志**缺失或明显滞后**时，除了本反模式条目，建议同时参考：  
  - `memory/patterns/pattern-iteration-log-enforcement-and-usage.md`（如何正确、稳定地记迭代日志）；  
  - `memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md`（如何用 runtime-logs 与 memory 反向校验迭代日志执行情况）。  
- 如多次出现类似遗漏，可进一步结合：  
  - `memory/patterns/pattern-rules-and-memory-evolution-governance.md`，检查是否需要在 rules 层与团队习惯上做结构性调整。

