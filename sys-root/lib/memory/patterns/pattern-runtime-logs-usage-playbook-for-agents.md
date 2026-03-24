---
type: pattern
title: runtime-logs 使用最小实践 Playbook
change-id: sys-rules-memory-refactor-v2-4
tags: [runtime-logs, playbook]
applicable-projects: [agentsystem]
host-scope: [cursor, vscode]
related:
  - memory/patterns/pattern-iteration-log-enforcement-and-usage.md
  - memory/anti-patterns/anti-pattern-runtime-logs-business-data-pitfall.md
  - memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md
---

# runtime-logs 使用最小实践 Playbook

## 适用范围

- 适用于已经启用 `runtime-logs/` 的项目，帮助主 Agent 与子 Agent 在不增加过多心智负担的前提下，有效记录模型调用与系统事件。

## 何时记录 runtime-logs

满足以下任一条件时，建议追加 runtime-logs 记录（`model-calls` 或 `system-events`）：

1. 针对某个 change-id，**完成了一个关键阶段**：  
   - 如需求分析 + tasks 拆分、大块实现/重构、完整验收通过等，且已在迭代日志中记录。  
2. 当前 change-id 属于**基础设施 / 运行成本相关变更**：  
   - 如 change-id 中包含 `sys-`、`infra`、`logging`、`memory`，或 proposal 中声明为系统级能力改造。  
3. 用户对**成本或性能/稳定性**有明确关注：  
   - 如询问「最近这段时间调用成本/成功率情况如何」。  
4. 执行过程中出现**错误、限流或明显降级重试**：  
   - 需要在技术指标维度为后续排查留痕。

> 触发条件参考：`agents/主Agent.md` 中对 runtime-logs 的说明。

## 如何记录（统一脚本接口示例）

1. 在满足上述条件且已经在迭代日志中记下业务过程后，调用统一脚本接口，例如（从项目根目录运行）：

```bash
python3 scripts/runtime-logging/append_cursor_model_call.py \
  --change-id <id> \
  --agent-role <role> \
  --skill <skill> \
  --model-name <name>
```

- 可由宿主或用户补充 `host` / `model_family` 等参数；  
- 记录会被追加到 `runtime-logs/model-calls/*.jsonl`，必要时还会在 `runtime-logs/system-events/events.log` 中追加一条事件日志。

2. 当需要做简单统计时，可调用：

```bash
python3 scripts/runtime-logging/summarize_model_calls.py \
  --group-by day|change-id|host
```

- 用于回答「某个 change-id 在本次迭代中总共调用了多少次、失败/限流次数等」问题。

## 与迭代日志的配合方式

1. **先迭代日志，后 runtime-logs**  
   - 先按 `projects-rules-for-agent.md` 要求，在 `docs/项目事件日志.md` 中为本次调用追加记录；  
   - 再根据触发条件决定是否追加 runtime-logs 条目。  
2. **粒度区分**  
   - 迭代日志更偏业务与治理：谁/何时/为何调用了哪个 Agent/技能；  
   - runtime-logs 更偏技术与执行：在哪个宿主/模型下，发生了哪些调用/错误/限流/重试。

## 常见误区

1. **尝试为每一次模型调用都写 runtime-logs**  
   - 成本高且噪音大，反而不利于分析。  
2. **只依赖 runtime-logs，不写迭代日志**  
   - 失去了从业务与变更视角复盘的能力。  
3. **把 runtime-logs 当成业务审计来源**  
   - 实际上，它更适合作为「技术指标与成本分析」的数据源，业务审计应以迭代日志与变更文档为主。

## 与 memory 及规则的关系

- 本 playbook 与 `memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md` 及运行时脚本 README 互为补充；  
- 执行前应确保：  
  - 已根据 `projects-rules-for-agent.md` 第三章完成迭代日志记录；  
  - 已了解当前项目的 runtime-logs 具体脚本路径与配置。

## 关联模式

- 当你在评估「是否需要/如何记 runtime-logs」时，推荐与以下条目联动阅读：  
  - `memory/patterns/pattern-iteration-log-enforcement-and-usage.md`：保证业务侧迭代日志先到位，再决定 runtime-logs 粒度；  
  - `memory/anti-patterns/anti-pattern-runtime-logs-business-data-pitfall.md`：避免在运行日志中混入业务敏感数据；  
  - `memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md`：理解 runtime-logs 与 memory、迭代日志在整体治理中的分工。

