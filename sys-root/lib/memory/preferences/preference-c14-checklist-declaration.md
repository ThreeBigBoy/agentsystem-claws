---
id: preference-c14-checklist-declaration
title: C.1-C.4 执行前查阅声明标准格式
type: preference
description: 执行任何 skill 或任务前，必须完成的 C.1-C.4 查阅声明的标准格式和内容要求
tags: [checklist, pre-execution, governance, skill-verification, declaration]
applicable_projects: [agentsystem, "*"]
host_scope: [cursor, vscode, generic]
source_change_ids: [update-product-template-default-health-compliance-section]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: draft
related:
  - agents/主Agent.md
  - memory/patterns/pattern-agent-role-boundary-enforcement.md
  - memory/anti-patterns/anti-pattern-retrospective-vs-execution-deviation-terminology-confusion.md
  - memory/preferences/preference-terminology-glossary.md
---

# C.1-C.4 执行前查阅声明标准格式

## 一句话定义

执行任何 skill 或任务前，必须完成的 **4 项查阅确认**，防止术语定义漂移和惯性思维陷阱，确保按最新规范执行。

## 来源与权威

本格式源自 `agents/主Agent.md` 第 8 点"执行前查阅规范机制（V2.7 新增，与 skills-rules 第10章对齐）"。

---

## 标准声明格式

### 完整版（Heavy 任务必选）

```markdown
**执行前查阅规范声明**

我确认已执行以下查阅：

- [x] **C.1 Skill 版本确认**
  - 已确认 skill `[skill-name]` 版本为 v[x.x]（最新版本）
  - 查阅时间：YYYY-MM-DD HH:mm
  - 版本确认方式：[文件头部版本号 / CHANGELOG / 最后更新时间]

- [x] **C.2 术语定义查阅**
  - 已查阅本阶段关键术语：
    - [术语 1]: [定义摘要]
    - [术语 2]: [定义摘要]
  - 查阅来源：`preference-terminology-glossary.md` / 相关 skill REFERENCE

- [x] **C.3 关联 Memory 唤醒**
  - 已唤醒并准备参考：
    - [memory-1]: [简要说明用途]
    - [memory-2]: [简要说明用途]
  - 唤醒方式：[tags 匹配 / related 跳转 / 场景绑定表]

- [x] **C.4 质量门禁检查清单**
  - 已查阅本阶段质量门禁检查清单 Step [N]
  - 清单来源：[skill-name/REFERENCE/xxx-自检.md]
  - 关键检查项：
    - [检查项 1]
    - [检查项 2]

**补充检查（可选）**:
- [ ] C.B1: 本任务的执行方是否为当前 Agent 的主导/赋能技能？（角色边界检查）
- [ ] C.B2: 本任务是否需要通过 LangGraph 后端调用子 Agent？（执行路径检查）
- [ ] C.B3: 本任务产出是否需要有独立审核方？（审核机制检查）
- [ ] C.B4: 本次执行是否存在"效率优先"的越权冲动？（自我约束检查）

**签名**: [Agent 角色]  
**日期**: YYYY-MM-DD  
**任务**: [change-id / 任务简述]
```

### 简化版（Simple 任务可选）

```markdown
**执行前查阅声明（简化）**

- [x] C.1 已确认使用最新 skill SKILL.md（v[x.x]）
- [x] C.2 已查阅关键术语：[术语 1]、[术语 2]
- [x] C.3 已唤醒 memory：[memory-1]、[memory-2]
- [x] C.4 已查阅质量门禁：Step [N] 检查清单

**签名**: [Agent 角色] | **日期**: YYYY-MM-DD
```

---

## 各查阅项详解

### C.1 Skill 版本确认

**目的**：防止使用旧版本规范，导致执行偏差。

**查阅内容**：
- Skill 文件头部的版本号（如 `v1.1`）
- CHANGELOG 或最近更新记录
- 与上次执行时的版本对比

**常见偏差**：
- ❌ "我上次做过，肯定没问题"（未检查版本是否更新）
- ✅ "已确认 skill prd-review v1.1（与上次执行时一致）"

### C.2 术语定义查阅

**目的**：防止术语定义漂移，确保与其他 Agent / 文档使用同一语义。

**查阅来源优先级**：
1. `memory/preferences/preference-terminology-glossary.md`（全局术语表）
2. 当前 skill REFERENCE/ 目录下的术语定义
3. OpenSpec.md 中的核心概念定义

**关键术语示例**（根据任务类型）：

| 任务类型 | 必查术语 |
|---------|---------|
| 需求分析 | PRD, Change-id, Requirement, Scenario |
| 代码评审 | Blocking, Major, Minor, Pass, Conditional Pass |
| 功能验收 | Func Test, Spec, Checklist |
| 复盘 | Retrospective, Execution Deviation, 复盘 3 级分离 |

### C.3 关联 Memory 唤醒

**目的**：加载相关经验，避免踩坑，复用最佳实践。

**唤醒策略**（克制机制）：
- 只加载当前条目的 `related` 字段（一跳）
- 不递归加载 `related` 的 `related`
- 总量控制在 3-5 条以内

**唤醒时机**：
- 任务启动时（根据场景自动唤醒）
- 遇到特定问题/异常时（按需追加）

### C.4 质量门禁检查清单

**目的**：明确本阶段的准出标准，防止不合格产物流入下一阶段。

**查阅来源**：
- `skills/[skill-name]/REFERENCE/[产出物]-最小结构与自检.md`
- `memory/preferences/preference-quality-gate-checklist.md`

**执行方式**：
- 产出后逐项自检
- 自检通过后方可给出完成性表述

---

## 角色边界检查扩展（C.B1-C.B4）

当任务涉及**多 Agent 协作**或**主 Agent 统筹**时，必须补充角色边界检查：

详见 `memory/patterns/pattern-agent-role-boundary-enforcement.md`

---

## 使用场景

### 必须使用（Heavy 任务）

- 新建 change-id / 发起 OpenSpec 变更
- PRD 评审、技术方案评审、代码评审
- 功能验收、复盘归档
- 任何涉及规则/文档修改的任务

### 建议使用（Medium 任务）

- 推进已有 change-id 的任务
- 涉及多个文件的代码修改
- 使用不熟悉的 skill

### 可选使用（Simple 任务）

- 单文件小改动
- 纯文案/格式调整
- 日常查询/问答

---

## 反例警示

❌ **形式化勾选**：所有项都勾选，但实际未查阅  
❌ **复制粘贴**：直接复制上次的声明，未针对当前任务调整  
❌ **事后补录**：执行完成后才补充声明  
❌ **跳过声明**：认为"这次任务简单，不需要声明"

---

## 历史案例

**2026-03-16**: `update-product-template-default-health-compliance-section` 任务中，主 Agent 未执行 C.1-C.4 查阅声明，导致：
1. 未读取 `pattern-openspec-change-workflow.md`，沿用旧目录结构
2. 未查阅最新术语，混淆"反思"与"复盘"
3. 未唤醒 memory，跳过 PRD 评审和角色边界检查

**后果**：目录结构错误、PRD 评审缺失、主 Agent 越权执行、后续虚假完成。

**改进**：本 preference 明确声明格式，强制查阅机制。

---

## 关联文档

- `agents/主Agent.md` 第 8 点 - 执行前查阅规范机制原文
- `memory/patterns/pattern-agent-role-boundary-enforcement.md` - 角色边界检查的 C.B1-C.B4 扩展
- `memory/preferences/preference-terminology-glossary.md` - C.2 术语查阅的权威来源
- `memory/preferences/preference-quality-gate-checklist.md` - C.4 质量门禁的汇总清单

---

**沉淀来源**: 框架级复盘「主 Agent 执行规范与 LangGraph 验证机制建设」  
**创建日期**: 2026-03-17