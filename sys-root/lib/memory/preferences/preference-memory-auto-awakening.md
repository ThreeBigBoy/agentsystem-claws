---
id: preference-memory-auto-awakening
title: Memory 自动唤醒优化指南
type: preference
description: 优化主 Agent 在执行任务时自动唤醒相关 Memory 的机制，提高唤醒准确率，确保每次执行都能获取最佳实践和避坑指南
description_long: |
  Memory 自动唤醒是 8+1 质量闭环执行前查阅规范机制的关键环节。
  本指南定义如何根据任务类型、上下文、关键词自动识别并唤醒高相关的 Memory，
  避免唤醒过多不相关 Memory 导致上下文过载，或遗漏关键 Memory 导致执行偏差。
  
  核心目标：
  - 唤醒准确率 >80%（唤醒的 Memory 确实被使用）
  - 召回率 >90%（关键 Memory 不漏唤醒）
  - 平均唤醒数量 3-5 个（避免上下文过载）
applicable_projects:
  - agentsystem
  - "*"
tags:
  - 偏好
  - Memory管理
  - 自动唤醒
  - 上下文优化
related:
  - pattern-complete-quality-closed-loop
  - anti-pattern-terminology-drift
  - anti-pattern-inertia-trap
  - skills-rules-for-agent.md
created_by: 合并行动计划-2026-03-16-item-11
created_date: 2026-03-17
version: 1.0
---

# Memory 自动唤醒优化指南

## 一句话定义

**根据任务类型、上下文、关键词自动识别并唤醒高相关 Memory，确保执行时获取最佳实践和避坑指南，同时避免上下文过载。**

---

## 当前问题

### 问题 1: Memory 唤醒不足
- **表现**: 执行时未唤醒关键 Memory，导致术语定义漂移、惯性思维陷阱
- **案例**: 归档操作未唤醒 `preference-archive-operation-checklist`，导致遗漏关键步骤

### 问题 2: Memory 唤醒过度
- **表现**: 唤醒过多不相关 Memory，导致上下文过长、成本增加
- **案例**: 唤醒 10+ 个 Memory，实际使用的只有 2-3 个

### 问题 3: 唤醒不准确
- **表现**: 唤醒的 Memory 与当前任务关联度不高
- **案例**: 执行代码评审时唤醒了需求分析相关的 Memory

---

## Memory 自动唤醒机制设计

### 三层唤醒策略

```
任务输入
    ↓
第一层：任务类型匹配（粗筛）
    - 根据技能类型确定基础 Memory 集合
    - 准确率：90%，召回率：95%
    
    ↓
第二层：上下文关键词匹配（精筛）
    - 提取任务描述关键词
    - 匹配 Memory 的 tags、related、description
    - 准确率：85%，召回率：90%
    
    ↓
第三层：动态优先级排序（优选）
    - 按相关度、最近使用、重要性排序
    - 选择 Top 3-5 个 Memory
    - 准确率：80%，召回率：85%
    
    ↓
唤醒 Memory 列表（3-5个）
```

### 唤醒触发点

| 触发时机 | 唤醒策略 | 示例 |
|---------|---------|------|
| 用户指令输入 | 提取关键词，唤醒相关 pattern/anti-pattern | 用户输入「归档」→ 唤醒 `preference-archive-operation-checklist` |
| Skill 执行前 | 根据 skill 类型唤醒基础 Memory 集合 | 执行 code-review → 唤醒 `pattern-review-fix-loop` |
| 阶段切换时 | 根据当前阶段唤醒阶段特定 Memory | 进入 Step 8 → 唤醒归档相关 Memory |
| 遇到问题时 | 根据问题类型唤醒诊断类 Memory | 发现术语漂移 → 唤醒 `anti-pattern-terminology-drift` |

---

## Skill-Memory 映射表（第一层唤醒）

### 核心技能基础 Memory 集合

| Skill | 强制唤醒 Memory | 建议唤醒 Memory | 唤醒数量 |
|-------|----------------|----------------|---------|
| **request-analysis** | `pattern-complete-quality-closed-loop` | `pattern-observable-small-steps` | 1-2 |
| **prd-review** | `pattern-review-fix-loop`, `anti-pattern-conditional-pass-as-go` | `anti-pattern-terminology-drift` | 2-3 |
| **project-analysis** | `pattern-complete-quality-closed-loop` | - | 1 |
| **architecture-review** | `pattern-review-fix-loop`, `anti-pattern-conditional-pass-as-go` | `anti-pattern-terminology-drift` | 2-3 |
| **coding-implement** | 项目特定 `project-rules/` | `pattern-complete-quality-closed-loop` | 1-2 |
| **code-review** | `pattern-review-fix-loop`, `anti-pattern-conditional-pass-as-go`, `anti-pattern-terminology-drift` | `preference-quality-gate-checklist` | 3-4 |
| **func-test** | `pattern-review-fix-loop`, `anti-pattern-conditional-pass-as-go`, `anti-pattern-terminology-drift` | `preference-quality-gate-checklist` | 3-4 |
| **retrospective-analysis** | `pattern-five-stage-retrospective`, `pattern-breakthrough-thinking-redefine-problem-space` | `anti-pattern-terminology-drift` | 2-3 |

### 阶段特定 Memory 唤醒（8+1 闭环）

| 阶段 | 强制唤醒 Memory | 唤醒触发词 |
|-----|----------------|-----------|
| **Step 1** | `pattern-complete-quality-closed-loop` | 需求分析、PRD |
| **Step 2** | `pattern-review-fix-loop`, `anti-pattern-conditional-pass-as-go` | 评审、review |
| **Step 3** | `pattern-complete-quality-closed-loop` | 技术方案、架构 |
| **Step 4** | `pattern-review-fix-loop`, `anti-pattern-conditional-pass-as-go` | 评审、review |
| **Step 5** | 项目特定 `project-rules/` | 编码、实现 |
| **Step 6** | `pattern-review-fix-loop`, `anti-pattern-terminology-drift` | 代码评审、review |
| **Step 7** | `pattern-review-fix-loop`, `anti-pattern-terminology-drift` | 验收、测试 |
| **Step 8** | `preference-archive-operation-checklist`, `anti-pattern-terminology-drift` | 归档、archive |
| **Step 9** | `pattern-five-stage-retrospective` | 复盘、总结 |

---

## 关键词-Memory 映射表（第二层唤醒）

### 关键术语触发

| 关键词 | 唤醒 Memory | 优先级 |
|-------|------------|--------|
| **归档** | `preference-archive-operation-checklist` | P0 |
| **archive** | `preference-archive-operation-checklist` | P0 |
| **评审** | `pattern-review-fix-loop` | P0 |
| **review** | `pattern-review-fix-loop` | P0 |
| **验收** | `preference-quality-gate-checklist` | P0 |
| **test** | `preference-quality-gate-checklist` | P0 |
| **术语** | `anti-pattern-terminology-drift` | P1 |
| **惯性** | `anti-pattern-inertia-trap` | P1 |
| **有条件通过** | `anti-pattern-conditional-pass-as-go` | P0 |
| **质量门禁** | `preference-quality-gate-checklist` | P0 |
| **闭环** | `pattern-complete-quality-closed-loop` | P1 |
| **复盘** | `pattern-five-stage-retrospective` | P0 |
| **阶段化** | `pattern-phase-execution` | P1 |
| **超时** | `pattern-observable-small-steps` | P2 |

### 问题场景触发

| 问题描述 | 唤醒 Memory | 优先级 |
|---------|------------|--------|
| 执行不完整 | `anti-pattern-terminology-drift` | P0 |
| 与规范不符 | `anti-pattern-terminology-drift`, `anti-pattern-inertia-trap` | P0 |
| 用户追问 | `anti-pattern-terminology-drift` | P1 |
| 规范执行衰减 | `pattern-complete-quality-closed-loop` (v1.2 防护机制) | P0 |
| 评审结论争议 | `pattern-review-fix-loop` | P0 |

---

## 唤醒优先级算法（第三层排序）

### 优先级计算公式

```
优先级分数 = 基础分 + 相关度分 + 时效分 + 重要性分

基础分（Must/Should/May）:
- Must（强制）: +100
- Should（建议）: +50
- May（可选）: +20

相关度分:
- 完全匹配: +50
- 高度相关: +30
- 中度相关: +15
- 低度相关: +5

时效分:
- 最近使用过: +20
- 本周使用过: +10
- 本月使用过: +5

重要性分:
- 关键模式/反模式: +25
- 重要偏好: +15
- 一般参考: +5
```

### 选择策略

1. **强制唤醒（Must）**: 无条件唤醒，不计入数量限制
2. **建议唤醒（Should）**: 按优先级排序，选择 Top 3-5
3. **可选唤醒（May）**: 空间允许时（<5个）才唤醒

### 数量控制

| 任务复杂度 | 唤醒数量 | 说明 |
|-----------|---------|------|
| 简单任务 | 3个 | 基础 skill + 1-2 个相关 |
| 中等任务 | 4-5个 | 基础 skill + 阶段特定 + 关键词匹配 |
| 复杂任务 | 5-6个 | 基础 skill + 阶段特定 + 关键词 + 问题场景 |

---

## 唤醒准确率优化策略

### 策略 1: 反馈学习

**机制**: 记录 Memory 被唤醒后的实际使用情况

```
唤醒 Memory X
    ↓
执行过程中是否使用了 Memory X？
    ↓ 是
标记为「有效唤醒」，下次优先
    ↓ 否
标记为「无效唤醒」，降低优先级
```

### 策略 2: 上下文去重

**机制**: 避免重复唤醒相同内容的 Memory

```
唤醒列表中已存在 pattern-review-fix-loop
    ↓
新匹配到 pattern-review-fix-loop（不同路径）
    ↓
去重，不重复唤醒
```

### 策略 3: 最近使用缓存

**机制**: 最近使用过的 Memory 在相似任务中优先

```
上次执行 code-review 使用了 pattern-review-fix-loop
    ↓
本次执行 code-review
    ↓
pattern-review-fix-loop 优先级 +20
```

### 策略 4: 失败案例学习

**机制**: 从执行偏差案例中识别缺失的 Memory

```
归档操作遗漏步骤（未唤醒 archive checklist）
    ↓
复盘分析
    ↓
归档相关任务强制唤醒 preference-archive-operation-checklist
```

---

## 唤醒机制融入执行流程

```
用户指令: 「执行 check-x 的归档」
    ↓
【触发点 1: 指令输入】
提取关键词: ["check-x", "归档", "archive"]
唤醒: 
  - Must: preference-archive-operation-checklist (关键词匹配)
  - Must: anti-pattern-terminology-drift (关键词匹配)
    ↓
【触发点 2: Skill 确认】
确认执行 Step 8 (归档)
唤醒:
  - Must: pattern-complete-quality-closed-loop Step 8 (阶段匹配)
    ↓
【触发点 3: 执行前】
准备执行归档操作
唤醒:
  - Should: anti-pattern-inertia-trap (防止惯性)
    ↓
执行归档操作
    ↓
【触发点 4: 遇到问题时】
如用户追问"是否真正归档"
唤醒:
  - May: anti-pattern-terminology-drift (问题场景)
    ↓
完成归档
```

---

## 准确率测量指标

### 关键指标

| 指标 | 目标值 | 测量方法 |
|-----|-------|---------|
| **唤醒准确率** | >80% | 唤醒的 Memory 中被实际使用的比例 |
| **召回率** | >90% | 应该唤醒的关键 Memory 中被成功唤醒的比例 |
| **平均唤醒数量** | 3-5个 | 每次任务唤醒的 Memory 平均数 |
| **无效唤醒率** | <20% | 唤醒但未使用的 Memory 比例 |
| **关键 Memory 遗漏率** | <10% | 应该唤醒但未唤醒的关键 Memory 比例 |

### 测量方法

```python
# 伪代码
metrics = {
    "precision": used_memories / total_awakened_memories,
    "recall": awakened_critical_memories / total_critical_memories,
    "avg_count": sum(awakened_counts) / total_tasks,
    "false_positive_rate": unused_memories / total_awakened_memories,
    "miss_rate": missed_critical_memories / total_critical_memories
}
```

---

## 执行前 Memory 唤醒检查清单

执行任何任务前，确认以下 Memory 唤醒检查已完成：

```markdown
【Memory 自动唤醒检查】

任务: [任务描述]
触发词: [提取的关键词]

第一层唤醒（Skill 基础集合）:
- [ ] 已根据 skill 类型确定基础 Memory 集合
- [ ] 已唤醒 Must 级别 Memory: [list]
- [ ] 已唤醒 Should 级别 Memory: [list]

第二层唤醒（关键词匹配）:
- [ ] 已提取任务关键词: [list]
- [ ] 已匹配关键词触发的 Memory: [list]
- [ ] 已按优先级排序

第三层唤醒（优选）:
- [ ] 唤醒 Memory 数量: [N] 个（目标 3-5 个）
- [ ] 唤醒列表: [memory1, memory2, ...]
- [ ] 确认无重复唤醒

唤醒结果确认:
- [ ] 关键 Memory 已唤醒（无遗漏）
- [ ] 唤醒数量合理（不过载）
- [ ] 优先级正确

**唤醒 Memory 列表**:
1. [Memory ID] - [唤醒原因]
2. [Memory ID] - [唤醒原因]
3. ...
```

---

## 与 skills-rules-for-agent.md 的关联

本指南是 `skills-rules-for-agent.md` 「十、执行前查阅规范机制」中「C.3 关联 Memory 唤醒」的详细实现指南。

执行前查阅规范机制要求：
1. **确认 skill 版本**（C.1）→ 本指南提供版本检查方法
2. **查阅术语定义**（C.2）→ 本指南提供关键词映射
3. **唤醒关联 Memory**（C.3）→ 本指南提供三层唤醒策略
4. **查阅检查清单**（C.4）→ `preference-quality-gate-checklist`

---

**指南版本**: v1.0  
**创建日期**: 2026-03-17  
**关联文档**: 
- skills-rules-for-agent.md（执行前查阅规范机制）
- pattern-complete-quality-closed-loop（8+1 闭环）
- anti-pattern-terminology-drift（术语漂移反模式）
