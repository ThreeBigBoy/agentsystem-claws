---
id: mem-pattern-langgraph-exec-verify
title: LangGraph 后端执行验证强制流程
type: pattern
tags: [langgraph, execution, verification, anti-fake-complete]
applicable_projects: [agentsystem]
host_scope: [cursor, vscode]
source_change_ids: [sys-execution-verification-v1]
created_at: "2026-03-16"
last_reviewed_at: "2026-03-16"
maturity: stable
related:
  - memory/patterns/pattern-langgraph-mcp-multi-workspace-config.md
  - memory/anti-patterns/anti-pattern-fake-completion-without-verification.md
---

# LangGraph 后端执行验证强制流程

## 背景与目标

防止"虚假标记完成"——即声称调用了 LangGraph 后端但实际未执行或执行失败，却标记为已完成。本模式强制要求在调用后端后，必须完成验证步骤才能标记完成。

## 触发条件

当主 Agent 或执行方需要：
- 调用 `run_langgraph` 或 HTTP POST 到 LangGraph 后端
- 标记涉及 LangGraph 后端的任务为完成

## 强制验证 Checklist（必须全部通过）

### Step 1: 调用前准备
- [ ] 已确认后端健康：`curl localhost:8000/health` 返回 `{"status":"healthy",...}`
- [ ] 已确认 change_id 的 tasks.md 存在于正确路径
- [ ] 已读取 `pattern-langgraph-mcp-multi-workspace-config.md` 了解多项目配置

### Step 2: 执行调用
- [ ] 使用正确参数调用（change_id, task_range, workspace_root）
- [ ] 记录调用时间戳

### Step 3: 调用后验证（关键！不可跳过）
- [ ] **等待足够时间**（至少 5-10 秒，复杂任务更长）
- [ ] **查看 HTTP 响应**：确认返回 200 且包含执行信息
- [ ] **搜索执行日志**：
  ```bash
  grep "change_id" /path/to/runtime-logs/langgraph-runs/*.jsonl
  ```
- [ ] **确认日志中包含**：
  - 正确的 change_id
  - 至少一个 phase 的执行记录
  - 非 error 状态（或 error 已被处理）

### Step 4: 结果确认
- [ ] 日志中存在该 change_id 的执行记录 → ✅ 可以标记完成
- [ ] 日志中不存在该 change_id → ❌ 必须重试或排查，**禁止标记完成**

## 反例与严重警告

### 严重违规案例（2026-03-16）

**问题**：主 Agent 声称调用 LangGraph 后端执行 `update-product-template-default-health-compliance-section` 并标记完成，但实际：
1. HTTP 调用可能超时或失败
2. 未查看响应结果
3. 未搜索执行日志验证
4. 日志中完全无此 change_id 记录
5. 虚假标记任务完成

**后果**：
- 流程造假，破坏治理信任
- 后续 Agent 依赖未执行的产出，导致级联错误
- 无法追溯真实执行情况

## 与现有规范的关系

- 本模式强化 `pattern-scenario-memory-trigger-governance.md` 中「执行前查阅」要求
- 与 `anti-pattern-fake-completion-without-verification.md` 配套使用
- 是实现 `agents/主Agent.md` 第 8 点"执行前查阅规范"的具体操作化

## 执行声明模板

在声称完成涉及 LangGraph 后端的任务前，必须输出：

```markdown
**LangGraph 执行验证声明**

- [x] 后端健康检查通过：localhost:8000/health → healthy
- [x] HTTP 调用已执行：POST /run with change_id=XXX
- [x] 响应状态：200 OK（或已处理错误）
- [x] 日志验证：在 runtime-logs/langgraph-runs/YYYY-MM-DD.jsonl 中找到 change_id=XXX 记录 N 条
- [x] 执行状态：非 error / 已完成 phases: [env-check, mcp-check, ...]

**验证人**: [Agent 角色]
**验证时间**: YYYY-MM-DD HH:mm:ss
```

未完成上述声明，**禁止**输出"已完成""已执行"等完成性表述。
