---
id: mem-prd-skill-first-principles-review-upgrade-001
title: PRD相关Skill从关键词罗列到第一性原理的升级
type: reflection
tags: [skill-upgrade, first-principles, prd-review, request-analysis, quality-gate]
applicable_projects: [all]
host_scope: [agentsystem]
source_change_ids: [sys-infra-quality-gate-v1]
created_at: 2026-03-28
last_reviewed_at: 2026-03-28
maturity: draft
related: [
  "memory/patterns/pattern-product-requirement-review-4d-checklist.md",
  "memory/patterns/pattern-prd-architecture-review-audit-trail.md",
  "memory/reflections/reflection-skill-first-principles-review-upgrade.md"
]
---

## 背景与问题

在完善质量门禁系统时，发现PRD相关skill存在设计缺陷：

| Skill | 问题 |
|-------|------|
| `prd-review` | 有9项自检清单+多附录，但第一性原理维度未显式提炼 |
| `request-analysis` | 需求分析产出PRD，但缺乏第一性原理产出标准 |

---

## 第一性原理分析

### PRD的第一性原理维度

PRD是"为什么做、做什么、怎么做"的蓝图：

| 维度 | 本质问题 | 评审必须回答 | 质量标准 |
|------|----------|-------------|---------|
| **必要性** | 为什么要做 | 需求是否真实？是否直击项目短板？ | 有受益方分析、P0/P1理由 |
| **合理性** | 这样做对吗 | 产品方案在用户视角是否成立？ | 有场景分析、无明显设计坑 |
| **完整性** | 功能全覆盖了吗 | 功能点是否无遗漏、无过度实现？ | 有功能清单、有验收标准 |
| **可落地性** | 能否开发使用 | toC/toB细节是否足够开发使用？ | §6.1/§6.2深度对齐 |
| **可衡量性** | 如何验证成功 | 成功指标是否定义？ | 有结果/过程指标 |

### 与memory经验的对应

| memory经验 | 对应第一性原理维度 |
|-----------|-------------------|
| pattern-product-requirement-review-4d-checklist | 必要性、合理性、优先级（可衡量性）、内容质量（完整性+可落地性） |
| pattern-prd-architecture-review-audit-trail | 价值层（必要性+合理性）、执行层（完整性+可落地性+可衡量性） |

---

## 升级内容

### 1. prd-review 技能升级

**添加**: 附录A - 第一性原理评审框架（v1.5+）

**核心内容**:
- 问题诊断：为什么"关键词罗列"不够
- PRD的第一性原理5维度
- 与9项自检的映射关系
- 四维需求评审法的地位

### 2. request-analysis 技能升级

**添加**: 附录A - 第一性原理PRD产出框架（v1.1+）

**核心内容**:
- PRD的第一性原理5维度
- 产出自检清单
- 与prd-review的对应关系

---

## 升级效果

| 项目 | 升级前 | 升级后 |
|------|--------|--------|
| prd-review | 9项自检清单 | 第一性原理5维度 + 自检映射 |
| request-analysis | 缺乏产出标准 | 第一性原理5维度产出框架 |

---

## 通用原则

### PRD Skill升级检查清单

当发现PRD skill设计有问题时，按以下步骤检查：

1. [ ] **PRD是否回答了本质问题？**
   - 必要性：为什么做？
   - 合理性：这样做对吗？
   - 完整性：功能全覆盖了吗？
   - 可落地性：能否开发使用？
   - 可衡量性：如何验证成功？

2. [ ] **评审是否对齐第一性原理？**
   - 自检项是否映射到第一性原理维度
   - 评分是否反映真实质量

3. [ ] **产出与评审是否对应？**
   - request-analysis产出的内容
   - prd-review评审的内容
   - 两者是否对齐

---

## 关联模式

- `memory/patterns/pattern-product-requirement-review-4d-checklist`：四维需求评审法
- `memory/patterns/pattern-prd-architecture-review-audit-trail`：PRD评审留痕机制
- `memory/reflections/reflection-skill-first-principles-review-upgrade.md`：技术方案Skill升级经验
