---
id: mem-retrospective-five-whys-001
title: 五层穿透分析法（深度复盘方法论）
type: pattern
tags: [retrospective, five-whys, root-cause, analysis, governance]
applicable_projects: [all]
host_scope: [cursor, vscode, continue, openai-codex, generic]
source_change_ids: [sys-retrospective-methodology-v1]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: draft
related:
  - memory/patterns/pattern-proactive-retrospective-trigger.md
  - memory/patterns/pattern-data-driven-retrospective.md
  - memory/anti-patterns/anti-pattern-superficial-retrospective.md
---

# 五层穿透分析法（深度复盘方法论）

## 背景与适用场景

在复杂软件项目的复盘过程中，常见的问题是停留在表面现象，未能触及问题的根本原因。五层穿透分析法（Five Whys Deep Dive）是一种系统化的深度复盘方法，通过连续追问「为什么」，逐层剥开问题的表象，直达根本原因。

**适用场景：**
- 重大故障/缺陷的根因分析
- 项目延期或目标未达成的深度复盘
- 系统性问题的识别与改进
- 跨团队协作障碍的诊断

## 核心方法论

### 五层追问结构

```
第一层（表象）: 发生了什么？          → 记录客观事实
第二层（直接原因）: 为什么发生？       → 找出最直接的原因
第三层（间接原因）: 为什么会这样？      → 分析导致直接原因的因素
第四层（系统性原因）: 为什么系统允许？  → 检视流程/机制缺陷
第五层（根本原因）: 为什么根源存在？   → 触及文化/认知/架构层面
```

### 执行步骤

**Step 1: 建立问题陈述（第一层）**
- 用客观、可观察的事实描述问题
- 避免使用模糊或带有评判性的语言
- 包含：时间、地点、影响范围、持续时间

**Step 2: 逐层追问（第二至五层）**
- 对每一层回答继续追问「为什么」
- 区分「原因」与「借口」
- 使用「因为...所以...」的逻辑链验证
- 每一层应包含数据和证据支撑

**Step 3: 交叉验证**
- 从第五层倒推，验证是否能解释第一层的问题
- 识别逻辑断层或跳跃
- 补充缺失的证据或假设

**Step 4: 制定改进措施**
- 针对每一层原因设计对应措施
- 优先处理根本原因（第五层）
- 设置可量化的验证指标

**Step 5: 沉淀与传播**
- 将分析过程记录到 `docs/project-prd-changes/[change-id]/records/`（或项目约定的复盘路径）
- 更新相关 SKILL 或 memory 条目
- 在团队内部分享关键洞察

### 关键原则

1. **证据导向** - 每个「为什么」的回答必须有数据、日志或记录支撑
2. **避免指责** - 聚焦于系统和流程，而非个人
3. **多维视角** - 技术、流程、沟通、认知四个维度同时分析
4. **闭环验证** - 改进措施实施后需验证是否解决根因

## 与现有规范的关系

- 当配合 `pattern-proactive-retrospective-trigger.md` 使用时，可在触发点自动启动五层分析
- 结合 `pattern-data-driven-retrospective.md`，确保每一层都有数据支撑
- 避免落入 `anti-pattern-superficial-retrospective.md` 中描述的浅层分析陷阱

## 关联模式

- **主动复盘触发机制**：定义何时启动五层穿透分析
- **数据驱动复盘法**：提供每层分析所需的数据收集与分析方法
- **浅层复盘反模式**：提醒本方法要规避的常见错误

