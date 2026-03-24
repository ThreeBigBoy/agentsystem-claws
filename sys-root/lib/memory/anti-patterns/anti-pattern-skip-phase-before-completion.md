---
id: anti-pattern-skip-phase-before-completion
title: 前置步骤未完成即完成后置步骤反模式
type: anti-pattern
description: 在 10 步质量闭环中，跳过或未完成前置步骤（如需求审核、归档），直接完成后置步骤（如复盘），导致质量缺口和流程造假
tags: [quality-closed-loop, phase-skip, dependency-violation, anti-pattern, process-integrity]
applicable_projects: [agentsystem, "*"]
host_scope: [cursor, vscode, generic]
source_change_ids: [add-default-product-template-health-compliance]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: stable
related:
  - memory/patterns/pattern-complete-quality-closed-loop.md
  - memory/patterns/pattern-quality-gate-checkpoint.md
  - memory/anti-patterns/anti-pattern-fake-completion-without-verification.md
  - memory/preferences/preference-quality-gate-checklist.md
---

# 前置步骤未完成即完成后置步骤反模式

## 一句话定义

在 10 步质量闭环中，**跳过或未完成前置步骤**（如需求审核、归档），**直接完成后置步骤**（如复盘、验收），违反流程依赖关系，导致质量缺口和流程造假。

## 典型表现

### 表现 A：跳过早期阶段

| 错误顺序 | 正确顺序 | 后果 |
|---------|---------|------|
| Step 2/3 → **跳过 Step 1** → Step 5 | Step 1 → Step 2/3 → Step 4 → Step 5 | 需求未经审核，方案可能偏离目标 |
| Step 5 → **Step 4 未完成** | Step 4 完成 → Step 5 | 未归档就复盘，复盘缺乏完整上下文 |
| Step 7 → **Step 6 跳过** | Step 6 完成 → Step 7 | 未 code review 就验收，代码质量无保障 |

### 表现 B：假性完成

- tasks.md 中前置任务显示 `[ ]` 未勾选，但后置任务已 `[x]` 勾选
- 声称"Step N 完成"，但 Step N-1 的产出物不存在或不合格
- 以"任务简单""时间紧"为由，跳过必要阶段

## 为什么这是错误的

### 1. 破坏质量闭环的依赖关系

10 步闭环的设计是**层层递进、层层把关**：

```
Step 1 (需求审核通过) 
    ↓ 准入条件：审核结论为"通过"
Step 2/3 (方案设计)
    ↓ 准入条件：PRD/技术方案评审通过
Step 4/5/6 (实现)
    ↓ 准入条件：设计评审通过
Step 7 (验收)
    ↓ 准入条件：实现完成 + code review 通过
Step 8 (归档)
    ↓ 准入条件：验收通过
Step 9 (复盘)
    ↓ 准入条件：归档完成
Step 10 (全局更新)
```

跳过任何一环，等于**放弃了该环节的质量把关**。

### 2. 导致复盘/验收缺乏完整上下文

复盘需要基于**完整的执行过程**（从需求到归档）来总结经验。如果归档未完成、需求未审核，复盘就是在**不完整的上下文**上做总结，结论可信度低。

### 3. 隐藏风险无法暴露

- 跳过的需求审核可能隐藏着**需求理解偏差**
- 跳过的 code review 可能隐藏着**代码缺陷**
- 跳过的归档可能隐藏着**规范不符**

这些风险会在后续变更中**级联爆发**。

## 正确做法

### 原则：准入准出严格把关

每个 Step 启动前，必须检查**准入条件**：

| 步骤 | 准入条件 | 检查方式 |
|------|---------|---------|
| Step 2 (需求分析) | Step 1 审核通过 | 检查 tasks.md 中 1.x 已 [x] |
| Step 3 (方案设计) | Step 2 PRD 评审通过 | 检查 records/PRD-评审纪要.md 结论为"通过" |
| Step 4 (编码) | Step 3 技术方案评审通过 | 检查 records/技术方案-评审纪要.md 结论为"通过" |
| Step 5 (验收) | Step 4 完成 + Step 6 code review 通过 | 检查 4.x 和 6.x 已 [x] |
| Step 8 (归档) | Step 7 验收通过 | 检查 7.x 已 [x]，验收记录结论为"通过" |
| Step 9 (复盘) | Step 8 归档完成 | 检查 `openspec/changes/archive/` 存在，8.x 已 [x] |

### 执行前检查声明

启动任何 Step 前，完成以下自检：

```markdown
**阶段启动准入检查声明**

本次启动：Step [N] - [阶段名称]

前置步骤检查：
- [ ] Step [N-1] 所有任务已 [x] 完成？是/否
- [ ] Step [N-1] 的产出物已审核通过（如适用）？是/否
- [ ] Step [N-1] 的评审记录结论为"通过"（如适用）？是/否

如任一项为"否"：
- [ ] 已退回完成前置步骤，现在重新检查通过？是/否
- [ ] 或有明确理由可跳过（需在复盘时说明）？是/否

**声明人**: [Agent 角色]
**日期**: YYYY-MM-DD
```

### 简化情况的处理

**真正简单的情况**（如纯文案修改）：
1. 在 proposal.md 中明确声明："本变更为极简文案调整，合并 Step 1/2/3 为快速审核"
2. 保留最小质量把关：PRD 自检 + 主 Agent 快速审核
3. 在 tasks.md 中标注："Step 1/2/3 合并为快速审核，理由：[简述]"

**禁止**：以"简单"为由完全跳过所有把关。

## 检查清单

- [ ] 启动 Step N 前，Step N-1 的所有子任务已 [x] 勾选
- [ ] Step N-1 需要评审的，评审记录结论为"通过"
- [ ] tasks.md 中没有"后面已 [x] 但前面还 [ ]"的矛盾状态
- [ ] 复盘（Step 9）启动前，归档（Step 8）已完全完成

## 历史案例

**2026-03-17**: `add-default-product-template-health-compliance`

**错误表现**:
- 1.1（主 Agent 审核提案）显示 `[ ]` 未勾选
- 4.2（归档）显示 `[ ]` 待用户确认
- 但 5.1（复盘）已 `[x]` 完成

**根因**:
1. 认为变更"简单"（只是确认 product.json 结构），跳过需求审核
2. 复盘先于归档完成，当时归档 CLI 尚未执行
3. 没有阶段启动准入检查机制

**后果**:
- 需求审核缺口：product.json 已满足需求这一结论，其实没有经正式审核确认
- 复盘上下文不完整：基于未归档的变更做复盘，变更历史不完整
- 流程顺序混乱：破坏了 10 步闭环的严谨性

**改进**:
- 本 anti-pattern 强制阶段准入检查
- 创建 `pattern-quality-gate-checkpoint.md`（质量门禁检查点模式）

## 关联模式

- `pattern-complete-quality-closed-loop.md` - 10 步完整质量闭环的正确依赖关系
- `pattern-quality-gate-checkpoint.md` - 每个阶段的质量门禁检查点（待创建）
- `anti-pattern-fake-completion-without-verification.md` - 虚假完成的另一种形式
- `preference-quality-gate-checklist.md` - 各阶段的质量门禁检查清单汇总

---

**沉淀来源**: `add-default-product-template-health-compliance` 归档回顾发现的流程缺口  
**创建日期**: 2026-03-17