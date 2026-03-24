---
type: pattern
title: 模型分层与配额治理最小实践
change-id: sys-rules-memory-refactor-v2-4
tags: [rules, quota, model-strategy]
applicable-projects: [agentsystem]
host-scope: [cursor, vscode]
related:
  - memory/patterns/pattern-task-complexity-judgement-and-mode-switch.md
  - memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md
  - memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md
---

# 模型分层与配额治理最小实践

## 背景与适用场景

- 适用于需要在多个模型能力等级之间做权衡的项目（主力开发模型、长上下文/深度推理模型、轻量模型、外部 API 等）。  
- 来源于 `global-rules/projects-rules-for-agent.md` 第六章关于模型与配额治理的抽象规则。

## 能力分层与典型职责

1. **宿主内置主力开发模型**  
   - 适合：日常编码、重构、Bug 修复、多文件批量修改、需要频繁工具/终端联动的任务。  
   - 原则：  
     - 高频、多文件、机械性较强的执行类任务，优先使用该层；  
     - 尽量避免用高成本模型处理纯执行工作。

2. **宿主内置长上下文 / 深度推理模型**  
   - 适合：长文档阅读、复杂方案推演、架构与需求分析、中文或多轮推理。  
   - 原则：  
     - 阅读/推理/设计阶段优先使用；  
     - 完成方案后，落地编码阶段回到主力开发模型。

3. **宿主内置低成本 / 轻量模型**  
   - 适合：简单问答、语法修正、格式整理、轻量脚本、小任务。  
   - 原则：  
     - 对响应时延不敏感、逻辑简单的请求，优先使用以节省更贵模型额度。

4. **外部 API 模型**  
   - 适合：宿主模型不可用，或问题复杂度/风险级别已接近宿主能力边界，需要二次复核或更强模型时。  
   - 原则：  
     - 默认不作为首选；  
     - 使用前要考虑预算并设置硬限；  
     - 仍须遵守 OpenSpec、安全与项目规范。

## 推荐使用策略

1. **批量执行优先主力开发模型**  
   - 多文件改名、批量格式化、统一注释风格、简单逻辑重构等，统一由主力开发模型承担。  
2. **阅读/推理与实现阶段分离**  
   - 长文档和复杂方案阶段：使用长上下文/深推理能力；  
   - 进入「改文件、跑命令」阶段：回到主力开发模型。  
3. **优先消耗低成本能力**  
   - 简单辅助性工作（格式整理、拼写/语法修正、轻量问答）优先用轻量模型，避免浪费深推理额度。  
4. **高风险场景下主动提醒复核**  
   - 金融/安全/权限等高风险逻辑，先用宿主内最强组合给出方案；  
   - 当判断已接近能力边界，需明确提示用户考虑使用更强或外部模型做二次 review，不鼓励在无复核情况下直接上线。

## 配额与预算治理要点

1. 为外部 API 模型设置月度硬上限，防止超支。  
2. 当宿主高价值额度明显下降时：  
   - 剩余 ≤ 40%：减少高价值模型处理轻量问题；  
   - 剩余 ≤ 20%：只在核心开发/关键问题上使用高价值模型；  
   - 剩余 ≤ 10%：只留作「保命额度」，面向极少数高风险场景。  
3. 不在治理层文档中写死具体供应商与型号，而是描述「任务类型 × 能力等级 × 预算/风险」的匹配关系。

## 与现有规范/技能的关系

- 该 pattern 是对 `projects-rules-for-agent.md` 第六章的操作化抽象，帮助主 Agent 在实际任务中快速决策「用哪个层级的模型」。  
- 不改变各宿主 adapter 中具体映射关系（哪些型号对应哪类能力、使用哪个额度池等）。

## 关联模式

- 在进行模型选择与额度治理决策时，建议与以下条目联动：  
  - `memory/patterns/pattern-task-complexity-judgement-and-mode-switch.md`：先判定任务 simple/heavy，再决定是否启用高成本模型；  
  - `memory/patterns/pattern-runtime-logs-usage-playbook-for-agents.md`：为关键高成本调用设计合适的 runtime-logs 观测点；  
  - `memory/reflections/reflection-runtime-logs-and-memory-collaboration-v2-4.md`：从整体治理视角审视「配额策略 ↔ 记录策略」是否协同。

