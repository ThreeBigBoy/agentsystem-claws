---
id: mem-pattern-mandatory-langgraph-exec
title: 强制 LangGraph 后端执行——从宿主级约定到框架级强制保障
type: pattern
tags: [langgraph, mandatory, execution, framework-level-guarantee]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode, generic]
source_change_ids: [sys-mandatory-execution-v1]
created_at: "2026-03-16"
last_reviewed_at: "2026-03-16"
maturity: stable
related:
  - memory/patterns/pattern-langgraph-execution-verification.md
  - memory/reflections/reflection-change-full-lifecycle-migrate-langgraph.md
---

# 强制 LangGraph 后端执行——从宿主级约定到框架级强制保障

## 背景：为什么宿主级约定不够

`agents/主Agent.md`、`pattern-langgraph-execution-verification.md`、`anti-pattern-fake-completion.md` 都是**宿主级约定**：
- 依赖主 Agent 主动判断和遵守
- 可以被跳过、被虚假标记完成
- 无法强制验证真实执行

**LangGraph 框架的初心**：通过 **StateGraph 编译执行机制**，实现**框架级强制保障** —— 一旦启动 `/run`，流程必须走完，无法人为干预跳过。

## 核心区别

| 维度 | 宿主级约定（文档/memory） | 框架级强制（LangGraph） |
|------|---------------------------|------------------------|
| 执行触发 | 主 Agent 手动触发 | `/run` HTTP 调用强制触发 |
| 流程流转 | 依赖人判断下一步 | `parse → dispatch → collect` 代码强制流转 |
| 完成确认 | 人声称"已完成" | 状态机 `done/error`，无法虚假标记 |
| 可验证性 | 需人主动查日志 | 检查点自动持久化，可追溯每一步 |
| 防跳过 | 靠自觉 | `compile()` 后 100% 无跳过 |

## 强制机制设计

### 1. 执行入口唯一化

**禁止**：主 Agent 或任何子 Agent 手动执行任务后直接标记完成
**强制**：所有任务必须通过 `POST /run` 调用

```
所有任务执行请求
    ↓
必须路由到 LangGraph 后端
    ↓
StateGraph 编译执行
    ↓
检查点持久化状态
    ↓
返回实际执行结果
```

### 2. 状态机约束（防虚假完成）

```python
# StateGraph 定义的状态流转
pending → running → done
              ↓
            error
```

- 只有 `done` 状态才能视为完成
- `error` 状态必须处理，不能跳过
- 没有 "claimed_complete_but_not_executed" 状态

### 3. 检查点验证（防跳过）

每个节点完成后自动保存检查点：
- `parse_tasks` 完成 → 保存 decision 对象
- `dispatch` 完成 → 保存 results 数组
- `collect_feedback` 完成 → 保存 feedback 字符串

**验证方式**：
```bash
# 必须能从检查点恢复状态
curl /resume {change_id, thread_id, checkpoint_id}
```

如果不能恢复，说明执行未完成。

### 4. MCP 工具封装（简化调用）

```python
# langgraph_mcp_server.py
@mcp.tool()
def run_langgraph(change_id: str, task_range: Optional[str] = None) -> str:
    """
    唯一合法的任务执行入口。
    
    禁止：主 Agent 手动执行任务后直接返回"已完成"
    强制：必须通过此工具调用，由 StateGraph 执行并返回真实结果
    """
    response = httpx.post("/run", json={change_id, task_range})
    return response.json()["feedback"]  # 真实执行反馈
```

## 执行流程（强制路径）

### Step 1: 任务启动

```
用户：推进 change-id = XXX 的任务 2.1

主 Agent：
- 不做任何实际执行
- 仅构造 /run 请求参数
- 调用 MCP run_langgraph(change_id="XXX", task_range="2.1")
```

### Step 2: 框架级强制执行

```
LangGraph 后端（强制流转，不可跳过）：

1. parse_tasks 节点
   - 读取 tasks.md
   - 解析任务 2.1
   - 输出 decision → 检查点保存

2. dispatch 节点
   - 调度到对应 executor
   - 调用 LLM/API 实际执行
   - 收集 result → 检查点保存

3. collect_feedback 节点
   - 汇总 results
   - 生成 feedback 字符串
   - 标记状态 done/error → 检查点保存
```

### Step 3: 返回真实结果

```
MCP 工具返回 feedback 给主 Agent
主 Agent：
- 不得修改 feedback 内容
- 不得声称"已完成"（框架已标记 done）
- 仅转发结果给用户
```

### Step 4: 验证（可选但推荐）

```bash
# 验证检查点存在
curl /status?change_id=XXX&thread_id=YYY

# 验证可从检查点恢复
curl /resume -d {change_id, thread_id, checkpoint_id}
```

## 反例：违规操作

### 违规 1：手动执行后声称完成

```python
# 错误示例
# 主 Agent 手动读取 tasks.md
# 手动调用 executor
# 手动写入反馈
# 声称"已完成"

后果：
- 跳过 StateGraph 检查点机制
- 无法验证真实执行
- 可虚假标记完成
```

### 违规 2：绕过 MCP 直接 HTTP 调用但不验证

```python
# 错误示例
curl /run {change_id}  # 调用后不看响应
声称"已调用 LangGraph"

后果：
- 调用可能失败/超时
- 未验证检查点是否存在
- 仍是虚假完成
```

## 与 memory 的关系

**本模式不依赖 memory**：
- 即使不读取任何 pattern/memory
- StateGraph 编译执行机制仍然强制保障执行

**memory 的作用**（辅助，非必须）：
- 帮助理解为什么要这样设计
- 提供排查指南
- 但执行保障不依赖 memory

## 系统实施要求

### 1. 宿主 adapter 改造

`platform-adapters/cursor/mcp-setup.md` 必须规定：
- 所有任务执行必须通过 `run_langgraph` MCP 工具
- 禁止直接文件操作或脚本执行

### 2. 主 Agent 行为约束

`agents/主Agent.md` 必须更新：
- 移除"可手动执行任务"的隐含许可
- 明确：所有执行必须通过 `/run` 调用
- 声称完成前必须验证检查点存在

### 3. 验收标准

```
验收项：
- [ ] 所有 change_id 的任务执行均有 /run 调用记录
- [ ] runtime-logs/langgraph-runs/*.jsonl 中可查询到执行记录
- [ ] 检查点可恢复验证通过
- [ ] 不存在手动执行后声称完成的案例
```

## 总结

**核心原则**：
> 不是「建议」使用 LangGraph，而是「强制」通过 LangGraph 执行。
> 不是「依赖」memory 防止虚假完成，而是「框架」通过 StateGraph 编译执行强制保障。

**LangGraph 的初心**：
- 不是替代 memory
- 而是通过代码级强制流转，实现无论 memory 是否被读取都能保障的执行可靠性。
