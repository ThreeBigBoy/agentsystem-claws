---
type: pattern
title: 迭代日志强制记录与高效使用
change-id: sys-rules-memory-refactor-v2-4
tags: [rules, governance, iteration-log]
applicable-projects: [agentsystem]
host-scope: [cursor, vscode]
related:
  - memory/anti-patterns/anti-pattern-missing-iteration-log-in-agent-calls.md
  - memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md
  - memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md
---

# 迭代日志强制记录与高效使用

## 背景与适用场景

- 适用于所有采用 OpenSpec 与 `projects-rules-for-agent.md` 的项目。  
- 目标是：  
  - 保证「所有与 change-id 相关的 Agent/技能调用都有记录可追溯」；  
  - 同时让记录既不漏记，也不过度冗长或难以复用。

> 规则来源：`global-rules/projects-rules-for-agent.md` 第三章「Agent 与技能调用迭代日志」。

## 推荐做法（模式）

### 1. 记录范围

1. **所有 change-id 上下文中的 Agent/技能调用**：  
   - 只要在某个项目的某个 change-id 下调用了 `agents/` 或 `skills/`，本次调用产出完成后，都应在该项目统一的 `docs/项目事件日志.md` 中追加一条记录。  
2. **保留 change-id `project-early-phase`**：  
   - 所有项目前期（立项研究、需求分析、市场研究、产品方案等）工作统一归入 `project-early-phase`；  
   - 首次使用时须创建 `docs/project-early-phase/` 与相应迭代日志记录。  
3. **单次小改动未显式绑定 change-id 的情况**：  
   - 若当前已有进行中的变更，则归属该变更的 change-id；  
   - 否则可归属 `project-early-phase`，视为项目前期或未归类内工作。

### 2. 单条记录最小结构

建议统一使用以下文本格式：

> `XXXX年XX月XX日 HH:mm:ss：XX Agent，调用了 XX 技能，处理 XX 任务，输出 XX；使用模型 XX。`

- 时间：24 小时制，取沙箱/运行环境本地时间；  
- XX Agent：执行方角色名（主 Agent、产品经理 Agent、测试 Agent 等）；  
- XX 技能：本次调用的技能目录名（request-analysis、func-test 等）；  
- 任务：一句话概括本次任务；  
- 输出：一句话说明产出物；  
- 使用模型：按 `projects-rules-for-agent.md` 3.3 小节的优先级确定。

### 3. 使用模型的取值优先级

按照以下顺序获取「使用模型」字段，并在无法获取时给出合理占位：

1. 若可执行 `scripts/cursor-usage-to-iteration-log/get_last_model.py`，优先读取其 stdout；  
2. 若项目中约定有「当前模型」文件（例如 `.cursor/current-model-for-iteration-log.txt`），则读取其内容；  
3. 若用户在本轮任务中显式说明使用模型，则直接使用其说明；  
4. 若用户指定具体模型，则按指定名称填写；  
5. 若 Cursor 使用 Auto 模式且无法获知具体模型，则填写「Auto（具体模型未暴露）」；  
6. 完全无法获知时填写「—」。

### 4. 执行时机与自检

- **何时写**：  
  - 在某个 change-id 上下文中完成本次调用并产出后、但**在向用户给出「任务已完成/已闭环/已交付」等总结性回复之前**，完成迭代日志追加。  
- **自检要点**：  
  - 回复前自检：当前 change-id 是否已经在 `docs/项目事件日志.md` 中追加了本次调用记录；  
  - 若未追加，则先追加，再给出「已完成/请验收」等表述。

### 5. 与 runtime-logs 的关系

- 迭代日志主要关注「业务过程与 Agent/技能调用」；  
- runtime-logs 主要关注「模型调用与系统事件」；  
- 实践模式：  
  - 先在迭代日志中记录业务与 Agent 调用过程；  
  - 在满足 runtime-logs 触发条件时（如关键阶段完成、成本关切、出现错误/限流等），再调用统一脚本接口追加一条模型调用或系统事件记录。  
- 迭代日志记录可作为后续生成 runtime-logs 统计与 memory 条目的关键输入。

## 常见误区（反模式提示）

1. **只在「大版本完成时」一次性记迭代日志**：  
   - 导致中间每次 Agent/技能调用缺乏细粒度记录，不利于追踪问题与复盘。  
2. **记录信息过于简略或缺少 change-id**：  
   - 难以在多变更、多项目场景下做聚合分析与追溯。  
3. **迭代日志与实际执行不一致**：  
   - 明明调用了多个技能，但记录中只写了一个，或时间/模型等字段明显不准确。

## 与现有规范/技能的关系

- 本 pattern 对应并细化了 `projects-rules-for-agent.md` 第三章的强制要求；  
- 对脚本调用方式与使用模型解析逻辑的细节说明，可结合：  
  - `scripts/cursor-usage-to-iteration-log/README.md`；  
  - 与 runtime-logs 相关的 memory 条目（如 runtime-logs 使用最小实践）。

## 关联模式

- 当你在复盘某个 change-id 时，若发现**迭代日志遗漏或质量不稳定**，除本条目外，应一并查看：  
  - `memory/anti-patterns/anti-pattern-missing-iteration-log-in-agent-calls.md`（常见遗漏场景与风险）；  
  - `memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md`（与 runtime-logs、rules 的整体协作关系）。  
- 若问题源自「规则不清晰或执行习惯不稳定」，还应结合：  
  - `memory/patterns/pattern-rules-and-memory-evolution-governance.md`，一起评估是否需要同步优化 rules 与 memory 的分工。

