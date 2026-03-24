---
id: anti-pattern-retrospective-vs-execution-deviation-terminology-confusion
title: 复盘与执行偏差记录术语混淆反模式
type: anti-pattern
description: 将「执行偏差记录」（运行时偏差即时记录）与「复盘」（系统性总结）两个术语混为一谈，导致文档存放位置错误、概念边界模糊
tags: [terminology, retrospective, reflection, anti-pattern, documentation]
applicable_projects: [agentsystem, "*"]
host_scope: [cursor, vscode, generic]
source_change_ids: [add-default-product-template-health-compliance]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: stable
related:
  - memory/preferences/preference-terminology-glossary.md
  - skills/retrospective-analysis/REFERENCE/目录结构规范-v3-基于完整质量闭环.md
  - memory/anti-patterns/anti-pattern-terminology-drift.md
  - memory/patterns/pattern-retrospective-one-time-production.md
---

# 复盘与执行偏差记录术语混淆反模式

## 问题描述

**错误表现**:
- 把 `runtime-logs/execution-deviations/` 下的执行偏差记录称为"复盘"
- 试图解释"先写执行偏差记录草稿，再迁移到 framework 目录"的合理性
- 混淆了两类文档的本质区别：即时偏差记录 vs 系统性总结

**典型错误言论**:
- "runtime-logs 里的执行偏差记录是复盘的第一版草稿"
- "先出执行偏差记录，再走 change-id 迁移到 framework"
- "这两种都是复盘，只是阶段不同"

## 术语正确定义

| 术语 | 定义 | 存放位置 | 产出时机 | 结构要求 |
|------|------|---------|---------|---------|
| **执行偏差记录** (Execution Deviation) | 执行过程中发现问题/偏差时的**即时记录** | `runtime-logs/execution-deviations/` | 问题发现时立即记录 | 自由格式，重在快速记录 |
| **复盘** (Retrospective) | 变更/阶段结束后的**系统性总结** | `docs/retrospective/[level]/` | 变更归档后 | 必须含：目标→过程→根因→改进→模式沉淀 |

**关键区别**:
- 执行偏差记录 = "发现了什么偏差？"（运行时事实记录）
- 复盘 = "我们做得怎么样？为什么？下次如何更好？"（事后系统总结+方法论提炼）

## 为什么这是错误的

1. **破坏术语精确性**: 让"复盘"失去明确含义，变成什么都可以装的筐
2. **导致存放位置混乱**: 真正的复盘文档找不到，执行偏差记录占据了复盘的位置
3. **降低文档质量**: 即时记录不需要系统性结构，但复盘必须有；混为一谈后，复盘的质量标准被拉低
4. **违背 8+1 闭环设计**: Step 9 明确是"复盘"，不是"执行偏差记录"，两者在流程中的位置和作用不同

## 正确做法

**场景 A：执行中发现问题/偏差**
- 立即在 `runtime-logs/execution-deviations/` 记录执行偏差
- 文件命名：`[偏差类型]-[change-id]-[日期].md`
- 内容：发现了什么偏差、影响评估、即时补救措施
- **不要**称之为复盘

**场景 B：变更结束后的系统性总结**
- 直接使用 `retrospective-analysis` skill
- 产出到 `docs/retrospective/[level]/`
- 文件命名：`复盘-[主题]-[日期].md`
- 必须包含：目标达成情况、过程回顾、根因分析、改进措施、模式沉淀
- **一次性产出到正确位置**，不需要"草稿→迁移"

## 检查清单（避免此错误）

- [ ] 提到"复盘"时，确认指的是归档后的系统性总结，不是执行中的即时记录
- [ ] 检查文档存放位置：如果在 runtime-logs/，那它是执行偏差记录，不是复盘
- [ ] 检查文档结构：是否有明确的"目标→过程→根因→改进→沉淀"结构？如果没有，那不是复盘
- [ ] 检查产出时机：是执行中发现偏差时？还是变更归档后？前者是执行偏差记录，后者是复盘

## 关联模式

- `preference-terminology-glossary.md` - 必须查阅的术语定义表（含 Execution Deviation 和 Retrospective 的精确定义）
- `目录结构规范-v3-基于完整质量闭环.md` - 复盘 3 级分离的正确实践
- `pattern-retrospective-one-time-production.md` - 复盘一次性产出模式（明确不需要从执行偏差记录迁移）
- `anti-pattern-terminology-drift.md` - 术语漂移的一般性问题

## 历史案例

**2026-03-17**: 在讨论 `add-default-product-template-health-compliance` 的归档时，最初错误地把执行过程中的即时记录称为"反思"，并将其与"复盘"混淆，试图解释"先写运行时反思草稿再迁移"的合理性。经用户指正后：
1. 将术语从"反思"正式更名为"执行偏差记录"（Execution Deviation），与"复盘"语义差异更明显
2. 目录从 `runtime-logs/reflections/` 更名为 `runtime-logs/execution-deviations/`
3. 明确区分：runtime-logs 下的是**执行偏差记录**（即时事实记录），只有 `docs/retrospective/framework/` 下的才叫**复盘**（事后方法论总结）