---
id: pattern-phase-execution
title: 阶段化执行架构模式
type: pattern
description: 将长时间运行的复杂流程拆分为多个独立阶段（phase），每个阶段有独立的入口、出口、状态、超时控制和留痕机制，支持阶段间的聚合和续跑
description_long: |
  解决「大事务」执行模型与「可观测需求」的根本矛盾。
  适用于：AI Agent 工作流、CI/CD 流水线、大数据批处理、长时间运行的后端任务等场景。
  核心特征：分阶段执行、独立超时、多阶段留痕、断点续跑、可观测性。
applicable_projects:
  - agentsystem
  - "*"
tags:
  - 架构模式
  - 阶段化执行
  - 可观测性
  - 超时控制
  - 断点续跑
related:
  - pattern-review-fix-loop
  - pattern-observable-small-steps
  - pattern-complete-quality-closed-loop
  - prd-check-langgraph-backend-一键自检.md（第9章）
created_by: 技术方案评审修复-2026-03-16
created_for: check-langgraph-backend 第二阶段框架演进
version: 1.0
---

# 阶段化执行架构模式（Phase Execution Architecture Pattern）

## 一句话定义

将长时间运行的复杂流程拆分为多个独立阶段（phase），每个阶段有独立的入口、出口、状态、超时控制和留痕机制，支持阶段间的聚合和续跑。

---

## 问题背景

### 传统「大事务」执行模型的问题

```
┌──────────────────────────────────────────────────────────────┐
│                  传统「大事务」执行模型                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  客户端 ──→ /run(change_id) ──→ 服务端                       │
│                                     │                        │
│                                     ▼                        │
│                            ┌─────────────────┐              │
│                            │ 执行完整 workflow│              │
│                            │ 包含 N 个 tasks  │              │
│                            │ 耗时 7~10 分钟   │              │
│                            └─────────────────┘              │
│                                     │                        │
│                                     ▼                        │
│  客户端 ←── 返回结果（或 timeout）←── 服务端                    │
│                                                               │
│  问题：                                                        │
│  ❌ 超时频繁：整体执行时间超出客户端 timeout（120s~300s）     │
│  ❌ 黑盒执行：执行过程不可见，无法知道「跑到哪一步了」        │
│  ❌ 错误定位困难：失败时不知道是哪一步出问题                  │
│  ❌ 工具层困境：被迫在「timeout 太短」和「timeout 太大」之间摇摆│
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 根本原因

**「大事务」执行模型与「可观测需求」的根本矛盾**:
- 一次 HTTP 调用承载完整 workflow，包含多个任务（部分任务还有网络调用/重计算）
- 只要某些任务较重，整体耗时就可能超出客户端 timeout
- 反馈颗粒度太粗，中间过程完全不可见

---

## 模式解决方案

### 核心思想

> **把「大事务」拆成「可观测的小步骤」**

每个阶段（phase）是独立的执行单元：
- 覆盖一部分任务子集
- 有独立的超时控制
- 有清晰的留痕与状态
- 阶段间可聚合形成完整视图

### 阶段化执行架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     阶段化执行架构 (Phase Execution)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  客户端                                                         │
│    │                                                            │
│    ├──→ POST /run {change_id, phase="env-check"} ──→ 服务端     │
│    │                      │                                     │
│    │                      ▼                                     │
│    │              ┌──────────────┐                            │
│    │              │ 执行 env-check │  ← 覆盖任务 1.1~1.3         │
│    │              │ 耗时 5~15s     │                            │
│    │              └──────────────┘                            │
│    │                      │                                     │
│    │                      ▼                                     │
│    │              写入留痕（phase=env-check, status=done）         │
│    │                      │                                     │
│    │◀──────────────────── 返回结果（status=done）               │
│    │                                                            │
│    ├──→ POST /run {change_id, phase="mcp-check"} ──→ 服务端     │
│    │                      │                                     │
│    │              ┌──────────────┐                            │
│    │              │ 执行 mcp-check│  ← 覆盖任务 1.4~1.6         │
│    │              │ 耗时 10~30s   │                            │
│    │              └──────────────┘                            │
│    │                      │                                     │
│    │              写入留痕（phase=mcp-check, status=done）      │
│    │                      │                                     │
│    │◀──────────────────── 返回结果（status=done）               │
│    │                                                            │
│    ├──→ GET /status?change_id=xxx&aggregate=true               │
│    │                      │                                     │
│    │◀──────────────────── 返回聚合视图（所有阶段汇总）          │
│    │                                                            │
│  特点：                                                          │
│  ✅ 超时可控：每个 phase 独立 timeout（60s~120s）               │
│  ✅ 过程可见：每完成一个 phase 立即留痕，可查询进度             │
│  ✅ 错误定位：失败时明确知道是哪个 phase 出问题                 │
│  ✅ 灵活组合：可按需执行特定 phases，不必全量执行               │
│  ✅ 断点续跑：支持 checkpoint + /resume 从断点继续               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 模式结构

### 核心组件

| 组件 | 职责 | 示例 |
|------|------|------|
| **Phase 定义** | 定义阶段的任务范围、超时、依赖 | `env-check: {tasks: ["1.1", "1.2", "1.3"], max_latency: 60s}` |
| **Phase 路由** | 根据 phase 参数路由到对应任务子集 | `if phase == "env-check": execute_tasks([1.1, 1.2, 1.3])` |
| **阶段留痕** | 每阶段完成后写入独立记录 | `langgraph-runs/YYYY-MM-DD.jsonl` 中多条记录 |
| **聚合查询** | 聚合同一 change-id 的多阶段记录 | `GET /status?aggregate=true` |
| **Checkpoint** | 保存阶段状态，支持断点续跑 | `checkpoint_id` + `/resume` |

### Phase 定义示例

```python
# config.py
PHASES = {
    "env-check": {
        "description": "环境自检",
        "tasks": ["1.1", "1.2", "1.3"],  # 对应 tasks.md 中的任务编号
        "max_latency_seconds": 60,
        "dependencies": []  # 无依赖
    },
    "mcp-check": {
        "description": "MCP 配置检查",
        "tasks": ["1.4", "1.5", "1.6"],
        "max_latency_seconds": 60,
        "dependencies": ["env-check"]  # 依赖 env-check 完成
    },
    "biz-trace": {
        "description": "业务留痕检查",
        "tasks": ["1.7"],
        "max_latency_seconds": 300,
        "dependencies": ["mcp-check"]
    },
    "full": {
        "description": "全量执行",
        "tasks": "all",  # 所有任务
        "max_latency_seconds": 600,
        "dependencies": []
    }
}
```

### 接口契约

**请求**:
```json
POST /run
{
  "change_id": "check-langgraph-backend",
  "phase": "env-check",        // 阶段标识（可选，默认 "full"）
  "task_range": null,           // 与 phase 互斥
  "workspace_projects": null    // 其他参数
}
```

**响应**:
```jsonn{
  "status": "done",              // "done" | "partial_done" | "error"
  "change_id": "check-langgraph-backend",
  "phase": "env-check",
  "task_count": 3,
  "latency_seconds": 12.5,
  "checkpoint_id": "ckpt-xxx",
  "completed_phases": ["env-check"],
  "pending_phases": ["mcp-check", "biz-trace"]
}
```

---

## 关键流程

### 1. 单阶段执行流程

```
客户端                    服务端
  │                        │
  ├── POST /run ──────────▶│
  │  {change_id, phase}    │
  │                        │
  │                        ├── 1. 解析 phase 参数
  │                        │
  │                        ├── 2. 按 phase 过滤任务子集
  │                        │   └── tasks = ["1.1", "1.2", "1.3"]
  │                        │
  │                        ├── 3. 创建/复用 thread_id
  │                        │
  │                        ├── 4. 执行 workflow（超时控制）
  │                        │   └── 执行 tasks
  │                        │
  │                        ├── 5. 生成 checkpoint_id
  │                        │
  │                        ├── 6. 写入阶段留痕
  │                        │   └── langgraph-runs/2026-03-16.jsonl
  │                        │       {phase: "env-check", status: "done", ...}
  │                        │
  │◀──────── 返回结果 ────│
  │  {status, phase, ...}  │
  │                        │
```

### 2. 多阶段执行 + 聚合流程

```
客户端                    服务端
  │                        │
  ├── POST /run(phase=env-check) ─▶│  ─┐
  │◀──────── 返回 done ────│      ─┘  第一阶段
  │                        │
  ├── POST /run(phase=mcp-check) ─▶│  ─┐
  │◀──────── 返回 done ────│      ─┘  第二阶段
  │                        │
  ├── POST /run(phase=biz-trace) ──▶│  ─┐
  │◀──────── 返回 done ────│      ─┘  第三阶段
  │                        │
  ├── GET /status?aggregate=true ─▶│
  │◀──────── 返回聚合视图 ──│
  │  {phases: [{env-check}, {mcp-check}, {biz-trace}]}
  │                        │
```

### 3. 断点续跑流程

```
客户端                    服务端
  │                        │
  ├── POST /run(phase=biz-trace) ─▶│
  │                        │
  │         ◄── 网络中断 ──│
  │                        │
  │                        ├── 服务端已完成部分任务
  │                        │   └── checkpoint_id = "ckpt-abc123"
  │                        │
  ├── POST /resume ───────▶│
  │  {change_id, thread_id, checkpoint_id}
  │                        │
  │                        ├── 从 checkpoint 恢复状态
  │                        │
  │                        ├── 继续执行剩余任务
  │                        │
  │◀──────── 返回结果 ────│
  │  {status: "done", ...} │
  │                        │
```

---

## 适用场景

### 必须使用

| 场景 | 特征 | 原因 |
|------|------|------|
| **AI Agent 工作流** | 多步骤、长耗时（>30s）、需进度反馈 | 过程可观测、错误可定位 |
| **CI/CD 流水线** | 分阶段构建、测试、部署 | 阶段间独立、失败快速定位 |
| **大数据批处理** | 数据量大、处理时间长 | checkpoint 断点续跑 |
| **长时间后端任务** | 执行时间 > 120s | 避免客户端超时 |

### 推荐使用

| 场景 | 特征 |
|------|------|
| **微服务编排** | Saga 事务模式、分布式事务 |
| **复杂业务流程** | 多角色、多步骤、状态多 |
| **可中断任务** | 需要支持暂停/恢复 |

### 不适用

| 场景 | 原因 |
|------|------|
| **简单 CRUD 操作** | 执行时间短（<1s），无需分阶段 |
| **原子性要求高的单任务** | 不可分割，必须一次性完成 |
| **实时性要求极高** | 分阶段会增加延迟 |

---

## 设计决策

### 决策 1：phase 与 task_range 互斥

**选择**: phase 优先级高，与 task_range 互斥（同时指定时报错）

**理由**:
- phase 是「语义化」分组，task_range 是「物理」任务编号
- 避免歧义：如果 phase 包含的任务与 task_range 不一致，以谁为准？
- 强制使用者明确选择「语义分组」或「物理范围」

### 决策 2：phase 默认值

**选择**: 不指定 phase 时，默认 "full"（向后兼容）

**理由**:
- 向后兼容：现有调用都不传 phase，必须保持全量执行行为
- 显式优于隐式：如需阶段化执行，调用方必须显式指定 phase
- 避免意外：默认轻量可能导致调用方误以为已完成全量

### 决策 3：阶段留痕存储

**选择**: 每条阶段记录含 completed_phases 列表（冗余存储）

**理由**:
- 查询效率高：单条记录即可知完整进度，无需扫描当日所有记录
- 实现简单：不需要复杂的聚合查询逻辑
- 存储成本可接受：phases 数量有限（通常 3-5 个）

---

## 与其他模式的关系

```
┌─────────────────────────────────────────────────────────────────┐
│                      相关模式关系图                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  pattern-phase-execution（本模式）                                 │
│              │                                                   │
│              ├──────────────────┬──────────────────┐             │
│              │                  │                  │             │
│              ▼                  ▼                  ▼             │
│  pattern-observable-      pattern-review-      pattern-complete-  │
│  small-steps               fix-loop            quality-closed-loop │
│  （可观测的小步骤）         （评审修复循环）      （8+1 质量闭环）   │
│                                                                  │
│              │                                                   │
│              ▼                                                   │
│  anti-pattern-conditional-pass-as-go                               │
│  （有条件通过即放行反模式 - 避免质量门禁失效）                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 关系说明

| 模式 | 关系 | 说明 |
|------|------|------|
| `pattern-observable-small-steps` | **基础** | 阶段化执行是可观测小步骤模式在技术实现上的应用 |
| `pattern-review-fix-loop` | **流程保障** | 确保阶段化执行架构的设计质量（评审修复循环） |
| `pattern-complete-quality-closed-loop` | **整体框架** | 阶段化执行是 8+1 质量闭环 Step 5 的实现方式之一 |
| `anti-pattern-conditional-pass-as-go` | **警示** | 避免阶段化执行架构设计质量不达标即进入编码 |

---

## 实现指南

### 后端实现要点

1. **Phase 路由层**
   ```python
   def execute_by_phase(change_id: str, phase: str | None):
       phase = phase or "full"
       tasks = get_tasks_by_phase(change_id, phase)
       return execute_workflow(tasks)
   ```

2. **阶段留痕层**
   ```python
   def append_phase_log(change_id, phase, status, task_count, latency):
       log_entry = {
           "ts": datetime.now(),
           "change_id": change_id,
           "phase": phase,
           "status": status,
           # ...
       }
       append_to_jsonl(log_entry)
   ```

3. **聚合查询层**
   ```python
   def aggregate_phases(change_id: str) -> list[PhaseStatus]:
       logs = query_logs_by_change_id(change_id)
       return group_by_phase(logs)
   ```

### 客户端实现要点

1. **多次短调用 + 聚合**
   ```python
   def execute_with_phases(change_id: str):
       phases = ["env-check", "mcp-check", "biz-trace"]
       results = []
       
       for phase in phases:
           result = call_run_api(change_id, phase)
           results.append(result)
       
       return aggregate_results(results)
   ```

2. **超时控制**
   ```python
   PHASE_TIMEOUTS = {
       "env-check": 60,
       "mcp-check": 60,
       "biz-trace": 120
   }
   ```

---

## 沉淀来源

- **实践项目**: check-langgraph-backend 第二阶段框架演进
- **创建日期**: 2026-03-16
- **创建原因**: 解决「一次 HTTP `/run` 调用承载完整 change-id 执行」导致的超时、不可观测问题
- **技术方案**: `openspec/changes/check-langgraph-backend/design.md` v1.0
- **PRD**: `docs/project-prd-changes/check-langgraph-backend/PRD-check-langgraph-backend-一键自检.md` v2.0（第9章）
- **复盘报告**: `docs/retrospective/framework/2026-Q1/复盘-8+1质量闭环-有条件通过处理机制-2026-03-16.md`

---

**规范版本**: v1.0  
**最后更新**: 2026-03-16  
**维护者**: agentsystem 架构组
