---
id: pattern-agent-role-boundary-enforcement
title: 主 Agent 角色边界强制机制
type: pattern
description: 通过定义、检查、约束三层机制，确保主 Agent 保持"统筹者"定位，不越权执行子 Agent 的具体任务
tags: [agent-role, boundary, governance, enforcement, coordination]
applicable_projects: [agentsystem, "*"]
host_scope: [cursor, vscode, generic]
source_change_ids: [update-product-template-default-health-compliance-section]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: draft
related:
  - memory/anti-patterns/anti-pattern-retrospective-vs-execution-deviation-terminology-confusion.md
  - agents/主Agent.md
  - skills-rules-for-agent.md
  - memory/patterns/pattern-scenario-memory-trigger-governance.md
---

# 主 Agent 角色边界强制机制

## 一句话定义

通过**定义层**（明确边界）、**检查层**（执行前确认）、**约束层**（运行时限制）的三层机制，确保主 Agent 保持"统筹者"定位，不越权执行子 Agent 的具体任务。

## 问题背景

### 常见越权行为

| 角色 | 应做（统筹） | 不应做（越权） | 后果 |
|------|-------------|---------------|------|
| **主 Agent** | 拆解任务、指派执行方、审核产出 | 直接执行需求分析、编码实现、测试 | 破坏职责分离，导致质量失控 |
| **产品经理 Agent** | 需求分析、PRD 产出 | 直接修改代码 | 专业错位，实现与设计脱节 |
| **架构 Agent** | 技术方案、code review | 直接写业务代码 | 失去独立评审视角 |

### 越权的根因

1. **惯性思维**：主 Agent 沿用了"自己能做就顺手做"的习惯
2. **效率错觉**：认为"直接做比协调快"，忽视质量风险
3. **机制缺失**：没有强制检查点阻止越权行为
4. **后端未就绪**：LangGraph 后端不可用时，退化为手动执行

## 三层强制机制

### 第一层：定义层（明确边界）

**角色与技能映射表**（必须显性化）：

| 执行方 | 主导技能 | 禁止直接执行的任务类型 |
|--------|---------|---------------------|
| 主 Agent | 无（统筹协调） | 需求分析、编码、测试、具体文档编写 |
| 产品经理 Agent | request-analysis | 代码实现、技术方案设计 |
| 架构 Agent | project-analysis, code-review | 业务代码编写、功能测试 |
| 前端/后端 Agent | coding-implement | 需求分析、架构设计、评审 |
| 测试 Agent | func-test | 代码实现、需求分析 |

**规范来源**：`skills-rules-for-agent.md` 中 "Agents 与 Skills 赋能对应关系" 表

### 第二层：检查层（执行前确认）

**执行前必须完成的自检（C.1-C.4 的变体）**：

```markdown
**执行前角色边界检查声明**

- [ ] C.B1: 本任务的执行方是否为当前 Agent 的主导/赋能技能？
  - 是 → 继续执行
  - 否 → 转交正确执行方，主 Agent 仅协调
- [ ] C.B2: 本任务是否需要通过 LangGraph 后端调用子 Agent？
  - 是 → 确认后端健康，发起 /run 调用
  - 否（后端不可用）→ 记录降级原因，手动执行后补录 runtime-logs
- [ ] C.B3: 本任务产出是否需要有独立审核方？
  - 是 → 在 tasks.md 中标注审核方和验收清单
  - 否 → 自检通过后可归档
- [ ] C.B4: 本次执行是否存在"效率优先"的越权冲动？
  - 是 → 暂停，重新按规范流程执行
  - 否 → 继续

**声明人**: [Agent 角色]
**日期**: YYYY-MM-DD
```

### 第三层：约束层（运行时限制）

**理想状态（未来机制）**：

1. **工具调用前检查**：尝试调用非本角色主导技能时，系统发出警告
2. **文件操作限制**：
   - 主 Agent：仅能操作 `openspec/`、`docs/`（按 usr-rules OpenSpec 第一节） 统筹层文档
   - 不能直接修改 `theme-health-food/` 等业务代码目录
3. **完成性表述拦截**：未通过 LangGraph 后端执行的任务，无法标记为 completed

**当前可行（宿主层面）**：

- 在 `.cursor/rules/agent.mdc` 中增加：
  ```
  主 Agent 禁止直接执行以下技能：
  - request-analysis（应由产品经理 Agent 执行）
  - coding-implement（应由前端/后端 Agent 执行）
  - func-test（应由测试 Agent 执行）
  
  如检测到主 Agent 尝试执行上述技能，必须：
  1. 停止执行
  2. 重新拆解任务，指派给正确执行方
  3. 通过 LangGraph 后端触发执行
  ```

## 特殊场景处理

### 场景 A：LangGraph 后端不可用

**问题**：后端未启动或 MCP 故障时，是否需要主 Agent 手动执行？

**正确做法**：
1. 记录后端不可用原因到 `runtime-logs/system-events/`
2. 主 Agent 可临时手动执行，但必须在迭代日志中标记为"非框架级执行"
3. 后端恢复后，优先补录 execution-deviations 和执行验证
4. **禁止**：以后端不可用为由，长期绕过角色边界

### 场景 B：简单任务是否需要走完整流程？

**判断标准**：
- 是否涉及 OpenSpec 文档变更？是 → 必须走流程
- 是否涉及多 Agent 协作？是 → 必须走流程
- 是否涉及业务代码？是 → 必须走流程
- 纯文本/注释修改？否 → 可按 simple 模式，但需自检

### 场景 C：主 Agent 发现子 Agent 产出有问题

**正确做法**：
1. 不直接修改子 Agent 产出
2. 输出【审核意见】，明确指出问题和修改方向
3. 退回子 Agent 修改，或发起修复任务
4. 审核意见作为独立文档留存（如 `*-code-review.md`）

## 检查清单

- [ ] 任务拆解时，每个任务都明确了执行方（对应到 agents/*.md 中的角色）
- [ ] 执行前完成了角色边界检查声明（C.B1-C.B4）
- [ ] 产出物由被指派的执行方完成，非主 Agent 代劳
- [ ] 需要审核的产出物有独立审核记录
- [ ] 迭代日志中，每次 Agent/技能调用都写明了执行方角色

## 反例警示

❌ **大包大揽型**：主 Agent 直接写 PRD、写代码、写测试，全程无子 Agent 参与  
❌ **效率优先型**："这次我顺手做了，下次再走流程"  
❌ **后端借口型**："LangGraph 没启动，所以我手动执行了"（长期如此）  
❌ **审核合并型**：主 Agent 既执行又审核自己的产出

## 关联文档

- `agents/主Agent.md` - 主 Agent 角色定义与权责边界
- `skills-rules-for-agent.md` - Agents 与 Skills 赋能对应关系表
- `memory/anti-patterns/anti-pattern-retrospective-vs-execution-deviation-terminology-confusion.md` - 主 Agent 越权执行的历史案例
- `memory/patterns/pattern-scenario-memory-trigger-governance.md` - 场景→记忆绑定与规范查阅机制

---

**沉淀来源**: 框架级复盘「主 Agent 执行规范与 LangGraph 验证机制建设」  
**创建日期**: 2026-03-17