---
id: playbook-execution-verification-checklist
title: 执行验证清单剧本
type: playbook
description: 针对不同执行场景（LangGraph 后端调用、MCP 工具调用、手动执行等）的验证清单，防止虚假完成
tags: [verification, checklist, execution, langgraph, mcp, fake-completion-prevention]
applicable_projects: [agentsystem, "*"]
host_scope: [cursor, vscode, generic]
source_change_ids: [update-product-template-default-health-compliance-section]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: draft
related:
  - memory/anti-patterns/anti-pattern-fake-completion-without-verification.md
  - memory/patterns/pattern-langgraph-execution-verification.md
  - runtime-logs/execution-deviations/README.md
---

# 执行验证清单剧本

## 一句话定义

针对不同执行场景的标准化验证流程，确保"声称完成"等于"实际完成且有据可查"。

## 核心原则

> **完成性表述前必须有验证声明**

禁止：
- ❌ "应该完成了"
- ❌ "后端已调用，应该没问题"
- ❌ "上次这样是可以的"

必须：
- ✅ "已验证，证据如下..."

---

## 场景 A：LangGraph 后端调用（/run API）

### 适用场景

通过 HTTP POST `/run` 或 MCP `run_langgraph` 触发任务执行。

### 验证清单

```markdown
**LangGraph 执行验证声明**

- [ ] **A.1 后端健康检查**
  - 执行：`curl http://localhost:8000/health`
  - 期望返回：`{"status":"healthy"}` HTTP 200
  - 检查时间：YYYY-MM-DD HH:mm:ss

- [ ] **A.2 /run API 调用**
  - 调用方式：[HTTP curl / MCP run_langgraph]
  - 请求参数：
    - change_id: [xxx]
    - task_range: [xxx]（如有）
    - workspace_root: [xxx]（业务项目时必填）
  - 响应状态：HTTP [200 / 其他]
  - 响应内容摘要：[非空 / 含 error 字段]

- [ ] **A.3 日志验证**
  - 搜索：`grep "[change_id]" runtime-logs/langgraph-runs/YYYY-MM-DD.jsonl`
  - 结果：找到 [N] 条记录
  - 关键字段验证：
    - status: [done / error]
    - workspace_root: [非 null / 正确路径]
    - project_key: [正确值]
    - task_count: [预期数量]

- [ ] **A.4 响应与日志一致性**
  - /run 响应中的 thread_id 与日志中的 thread_id 一致？是/否
  - /run 响应中的 checkpoint_id 可在日志中找到？是/否

**验证结论**:
- [ ] 全部通过 → 可声称完成
- [ ] 任一项不通过 → 标记为 in_progress，修复后重新验证

**验证人**: [Agent 角色]  
**验证时间**: YYYY-MM-DD HH:mm:ss
```

### 快速验证脚本

```bash
# 在项目根目录执行
change_id="your-change-id"
date_str=$(date +%Y-%m-%d)

# 1. 健康检查
curl -s http://localhost:8000/health | grep "healthy"

# 2. 日志搜索
grep "\"change_id\": \"$change_id\"" \
  "/Users/billhu/Documents/AI OnePeace/AI Dev/01ProjectsDesignManage/agentsystem/runtime-logs/langgraph-runs/${date_str}.jsonl"
```

---

## 场景 B：MCP 工具调用

### 适用场景

通过 `call_mcp_tool` 调用各类 MCP 服务（如 `write_decision`、`run_langgraph` 等）。

### 验证清单

```markdown
**MCP 工具调用验证声明**

- [ ] **B.1 工具调用**
  - MCP Server: [server-name]
  - Tool Name: [tool-name]
  - 参数摘要：[关键参数及值]
  - 调用时间：YYYY-MM-DD HH:mm:ss

- [ ] **B.2 响应验证**
  - 响应状态：[success / error]
  - 响应内容非空？是/否
  - 关键字段存在？[字段名] 存在且值合理？是/否

- [ ] **B.3 副作用验证**（如有）
  - 文件是否创建/更新？路径：[xxx]，修改时间：[xxx]
  - 数据库/状态是否变更？验证方式：[查询/观察]
  - 下游系统是否收到？验证方式：[日志/回调/查询]

**验证结论**: [可声称完成 / 需修复后重试]

**验证人**: [Agent 角色]  
**验证时间**: YYYY-MM-DD HH:mm:ss
```

---

## 场景 C：手动执行（LangGraph 后端不可用）

### 适用场景

后端 MCP 故障、网络中断等情况下，主 Agent 手动执行任务。

### 降级流程

```markdown
**手动执行降级声明**

**触发原因**:
- [ ] LangGraph 后端健康检查失败
- [ ] MCP 工具调用失败（错误码/信息：[xxx]）
- [ ] 其他：[说明]

**降级措施**:
1. 记录触发原因到 `runtime-logs/system-events/`
2. 手动执行任务：[任务简述]
3. 在迭代日志中明确标记："本次为手动执行（后端不可用）"
4. 后端恢复后补录验证

**验证替代方案**:
- [ ] 产出物已按规范存放于正确路径？是/否
- [ ] 文件内容经自检符合 skill 要求？是/否
- [ ] 如有 review 要求，已安排独立审核？是/否

**验证结论**: [可临时声称完成，需后端恢复后补录验证 / 不可声称完成]

**执行人**: [Agent 角色]  
**执行时间**: YYYY-MM-DD HH:mm:ss
```

### 禁止长期使用

手动执行降级**只能作为临时措施**，连续 3 次以上手动执行同一类任务需触发：
1. 创建 change-id 修复后端问题
2. 复盘分析为什么后端长期不可用

---

## 场景 D：产出物交付验证

### 适用场景

代码实现、文档产出等需要交付到文件系统的任务。

### 验证清单

```markdown
**产出物交付验证声明**

- [ ] **D.1 路径正确性**
  - 存放路径符合规范？是/否
  - 路径示例：[完整路径]

- [ ] **D.2 内容完整性**
  - 文件非空？是/否
  - 包含所有必需章节/结构？是/否（对照 skill REFERENCE 自检）
  - 编码/格式正确？是/否

- [ ] **D.3 可验证性**
  - 产出物可被独立审核？是/否
  - 审核方可按明确标准验证？是/否

**验证结论**: [可声称完成 / 需补充后重验]

**验证人**: [Agent 角色]  
**验证时间**: YYYY-MM-DD HH:mm:ss
```

---

## 通用禁止项

在任何场景下，以下行为都构成**虚假完成**：

| 禁止行为 | 正确做法 |
|---------|---------|
| 发出请求后立即声称完成 | 等待响应 + 验证日志 |
| "应该没问题"的主观判断 | 客观验证，有据可查 |
| 只验证部分任务，声称全部完成 | 明确范围，逐项验证 |
| 跳过验证，说"下次再补" | 先验证，后声称完成 |

---

## 历史案例

**2026-03-16 虚假完成事件**:
- 声称："通过 LangGraph 后端调用产品经理 Agent 重新执行 request-analysis"
- 实际：HTTP POST /run 发出，但未确认响应，未验证 runtime-logs
- 验证：搜索 `runtime-logs/langgraph-runs/2026-03-16.jsonl`，完全无此 change_id 记录
- 后果：流程造假、信任损失、后续改进基于虚假信息

**改进**：本 playbook 强制执行验证清单。

---

## 关联文档

- `memory/anti-patterns/anti-pattern-fake-completion-without-verification.md` - 虚假完成的定义与防范
- `memory/patterns/pattern-langgraph-execution-verification.md` - LangGraph 验证的专项模式
- `runtime-logs/execution-deviations/README.md` - 发现虚假完成时的记录规范

---

**沉淀来源**: 框架级复盘「主 Agent 执行规范与 LangGraph 验证机制建设」  
**创建日期**: 2026-03-17