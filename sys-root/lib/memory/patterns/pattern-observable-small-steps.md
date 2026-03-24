---
id: pattern-observable-small-steps
title: 可观测的小步骤执行模式
type: pattern
description: 将长时间运行的复杂流程拆分为多个短阶段，每个阶段有独立的入口、出口、状态、超时控制和留痕机制，支持阶段间的聚合和续跑
applicable_projects:
  - agentsystem
  - any-long-running-workflow
tags:
  - architecture
  - observability
  - workflow-design
  - checkpoint
  - phase-execution
related:
  - pattern-problem-analysis-3-layer
  - pattern-paradigm-shift-checklist
  - pattern-long-running-workflow-design
  - pattern-product-requirement-review-4d-checklist
created_by: 复盘-check-langgraph-backend-超时问题
version: 1.0
---

# 可观测的小步骤执行模式（Observable Small Steps Pattern）

## 一句话定义

将长时间运行的复杂流程拆分为多个短阶段，每个阶段有独立的入口、出口、状态、超时控制和留痕机制，支持阶段间的聚合和续跑。

## 问题背景

### 典型症状

- 长时间运行的任务频繁 timeout
- 任务执行过程「黑盒」，只能看到最终结果
- 失败时难以定位具体是哪一步出问题
- 失败后需要重跑整个流程，浪费资源
- 用户需要「干等」，没有进度反馈

### 根因分析

```
┌─────────────────────────────────────────────────────────────┐
│                    「大事务」模式的缺陷                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  问题本质：单次调用承载完整长事务，导致：                       │
│                                                              │
│  1. 超时困境                                                  │
│     ├── timeout 太短 → 经常超时失败                           │
│     └── timeout 太大 → 失去保护意义，卡住也发现不了            │
│                                                              │
│  2. 观测盲区                                                  │
│     ├── 中间过程完全不可见                                     │
│     ├── 失败时不知道执行到哪一步                               │
│     └── 性能瓶颈难以定位                                      │
│                                                              │
│  3. 失败代价高                                                │
│     ├── 任一子任务失败导致整体失败                             │
│     └── 重跑需要重复执行已成功部分                             │
│                                                              │
│  4. 用户体验差                                                │
│     ├── 长时间无反馈，用户焦虑                                 │
│     └── 失败后无从知晓原因和进展                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 模式解决方案

### 核心思想

```
┌─────────────────────────────────────────────────────────────┐
│  大事务模式                      小步骤模式                   │
│  ┌───────────────────┐          ┌───────────────────┐       │
│  │ 一次调用          │          │ 多次短调用        │       │
│  │ ┌───────────────┐ │          │ ┌───┐┌───┐┌───┐  │       │
│  │ │███████████████│ │          │ │███││███││███│  │       │
│  │ │███████████████│ │          │ └───┘└───┘└───┘  │       │
│  │ │███████████████│ │          │ 阶段1 阶段2 阶段3  │       │
│  │ │（7分钟）      │ │          │  60s  60s  60s    │       │
│  │ └───────────────┘ │          └───────────────────┘       │
│  └───────────────────┘                                         │
│                                                              │
│  整体 timeout: 120s             每阶段 timeout: 60s         │
│  实际耗时: 600s                 实际耗时: 180s（聚合）          │
│  失败重跑: 600s                 checkpoint 续跑: 从失败点      │
│  过程可见性: 无                 每阶段状态: 可观测            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 模式结构

```
┌─────────────────────────────────────────────────────────────┐
│                    模式结构                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 阶段定义 (Phase Definition)                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ phase_id: 阶段唯一标识                               │     │
│  │ description: 阶段描述                                │     │
│  │ task_range: 本阶段包含的任务列表                      │     │
│  │ timeout: 本阶段超时时间（独立配置）                   │     │
│  │ dependencies: 前置阶段（可选）                          │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  2. 阶段执行 (Phase Execution)                                │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ Input: {change_id, phase_id, checkpoint_id?}        │     │
│  │                                                     │     │
│  │ Process:                                            │     │
│  │  ├─ 从 checkpoint 恢复状态（如有）                   │     │
│  │  ├─ 执行本阶段任务                                   │     │
│  │  ├─ 实时留痕（阶段开始/进度/完成）                    │     │
│  │  └─ 生成 checkpoint（供下阶段或续跑使用）            │     │
│  │                                                     │     │
│  │ Output: {                                           │     │
│  │   status: completed/partial_done/failed,             │     │
│  │   checkpoint_id,                                   │     │
│  │   results,                                         │     │
│  │   next_phase_id?                                   │     │
│  │ }                                                  │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  3. 阶段聚合 (Phase Aggregation)                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 聚合多个阶段的执行结果，生成完整报告                   │     │
│  │ 报告包含：每阶段状态、耗时、结果、整体结论             │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│  4. 续跑机制 (Resume Mechanism)                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ /resume(change_id, thread_id, checkpoint_id)        │     │
│  │ 从指定 checkpoint 继续执行后续阶段                   │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 适用场景

| 场景 | 示例 | 应用方式 |
|-----|------|---------|
| **AI Agent 工作流** | LangGraph 多 Agent 执行 | `/run(phase="env-check")` → `/run(phase="biz-trace")` |
| **CI/CD 流水线** | 构建-测试-部署 | 分阶段执行，每阶段独立超时和留痕 |
| **大数据批处理** | ETL 数据清洗 | 分批次处理，checkpoint 续跑 |
| **微服务编排** | Saga 分布式事务 | 分步骤执行，每步骤补偿机制 |
| **模型训练** | 大模型多 epoch 训练 | 每 epoch 保存 checkpoint |
| **文件处理** | 大文件分片处理 | 分片处理，断点续传 |

## 实现要点

### 协议层

```yaml
# 在 tasks.md 中定义 phase
- [ ] 1.1 任务 A
  phase: env-check    # <-- phase 元信息
  
- [ ] 1.4 任务 D
  phase: biz-trace    # <-- phase 元信息

# API 支持 phase 参数
POST /run
{
  "change_id": "xxx",
  "phase": "env-check",      # <-- 指定执行阶段
  "checkpoint_id": "yyy"     # <-- 可选，续跑时使用
}

# 响应包含 checkpoint
{
  "status": "partial_done",
  "checkpoint_id": "zzz",
  "results": [...],
  "next_phase": "mcp-check"
}
```

### 实现层

```python
# 阶段化执行逻辑
def execute_phase(change_id: str, phase_id: str, checkpoint_id: str = None):
    # 1. 恢复状态
    state = load_checkpoint(checkpoint_id) if checkpoint_id else init_state()
    
    # 2. 获取本阶段任务
    tasks = get_tasks_for_phase(change_id, phase_id)
    
    # 3. 执行并实时留痕
    for task in tasks:
        result = execute_task(task, state)
        append_log(change_id, phase_id, task.id, result)
        
    # 4. 生成 checkpoint
    new_checkpoint = save_checkpoint(change_id, phase_id, state)
    
    # 5. 返回结果
    return {
        "status": "completed",
        "checkpoint_id": new_checkpoint.id,
        "next_phase": get_next_phase(change_id, phase_id)
    }
```

### 工具层

```python
# 自检脚本使用阶段化执行
def run_self_check():
    phases = ["env-check", "mcp-check", "biz-trace"]
    results = []
    
    for phase in phases:
        # 每阶段独立 timeout（如 60~90 秒）
        result = call_run_api(
            change_id="check-langgraph-backend",
            phase=phase,
            timeout=90  # 短 timeout，可控
        )
        results.append(result)
        
        if result.status == "failed":
            report_failure(phase, result)
            return aggregate_results(results)
    
    return aggregate_results(results)  # 聚合所有阶段结果
```

## 收益

| 维度 | 大事务模式 | 小步骤模式 |
|-----|-----------|-----------|
| **可观测性** | ❌ 黑盒 | ✅ 每阶段状态可见 |
| **故障隔离** | ❌ 整体失败 | ✅ 阶段间隔离 |
| **调试效率** | ❌ 难以定位 | ✅ 精准到 phase/task |
| **超时控制** | ❌ 被迫超大 timeout | ✅ 每阶段可控 |
| **用户体验** | ❌ 干等无反馈 | ✅ 分阶段进度反馈 |
| **系统韧性** | ❌ 失败重跑全部 | ✅ checkpoint 续跑 |
| **可扩展性** | ❌ 任务越多越严重 | ✅ 阶段化天然支持扩展 |

## 权衡与注意事项

### 何时使用

✅ **推荐使用**：
- 执行时间 > 30 秒的流程
- 包含多个可独立划分的逻辑阶段
- 需要进度反馈或中断恢复能力
- 子任务间相对独立，可分批执行

❌ **不适用**：
- 原子性要求极高的短事务（如支付扣款）
- 强顺序依赖、无法分段的流程
-  overhead 成本高于收益的简单流程

### 实现成本

| 成本项 | 说明 |
|-------|------|
| 协议设计 | 需在 tasks.md 中增加 phase 元信息，API 需支持 phase 参数 |
| 状态管理 | 需实现 checkpoint 存储和恢复机制 |
| 工具改造 | 调用方需改为「多次短调用 + 聚合」模式 |
| 留痕扩展 | 需支持同一 change-id 的多阶段留痕记录 |

## 相关模式

- `pattern-problem-analysis-3-layer` - 三层穿透分析法（用于识别何时需要本模式）
- `pattern-paradigm-shift-checklist` - 突破性思维 checklist（用于推动采用本模式）
- `pattern-long-running-workflow-design` - 长时间运行工作流设计模式
- `pattern-checkpoint-resume` - Checkpoint + Resume 模式

## 案例参考

- **LangGraph 后端阶段化执行**：`check-langgraph-backend` 第二阶段提案
- **CI/CD 阶段化**：GitHub Actions workflow 的 jobs/steps 设计
- **大数据批处理**：Apache Spark checkpoint 机制
- **微服务 Saga**：Netflix Conductor 工作流编排

## 沉淀来源

- 复盘事件：check-langgraph-backend 自检脚本 timeout 问题
- 复盘日期：2026-03-14
- 复盘文档：`docs/project-prd-changes/check-langgraph-backend/records/复盘-自检脚本超时与框架演进反思.md`
- 核心洞察：用户提出「把大事务拆成可观测的小步骤」的突破性思维

---

**模式版本**: v1.0  
**最后更新**: 2026-03-14  
**维护者**: agentsystem 架构组
