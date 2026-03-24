---
id: playbook-agent-skill-memory-mapping-for-quality-closed-loop
title: 质量闭环流程中的 Agent-Skill-Memory 映射手册
type: playbook
description: 建立 8 步质量闭环流程中每个步骤与 Agent、Skill、Memory 的显性映射关系，确保流程可被正确执行和唤醒
description_long: |
  本手册建立完整的 Agent-Skill-Memory 映射表，解决「流程定义了但不知道如何触发」的问题。
  每一步都明确：由哪个 Agent 执行、触发哪个 Skill、唤醒哪些 Memory、产出什么文档。
  是 pattern-complete-quality-closed-loop 的可执行版本。
applicable_projects:
  - agentsystem
  - "*"
tags:
  - 执行手册
  - 流程映射
  - Agent协同
  - Skill触发
  - Memory唤醒
related:
  - pattern-complete-quality-closed-loop
  - pattern-prd-architecture-review-audit-trail
  - pattern-breakthrough-thinking-redefine-problem-space
  - pattern-observable-small-steps
  - skills-rules-for-agent.md
created_by: 复盘-2026-03-14-agent-skill-memory-mapping
version: 1.0
---

# 质量闭环流程中的 Agent-Skill-Memory 映射手册

## 手册定位

本手册是 `pattern-complete-quality-closed-loop` 的**可执行版本**，建立每一步流程与 Agent、Skill、Memory 的**显性映射关系**，解决「流程定义了但不知道如何触发」的问题。

## 核心映射表

### 总览：9 步 × (Agent + Skill + Memory + 产出)

| 步骤 | 阶段名称 | Agent | Skill | 触发指令示例 | 唤醒 Memory | 产出物 |
|-----|---------|-------|-------|-------------|------------|--------|
| 1 | 需求分析 | 产品经理 Agent | request-analysis | 「分析需求」「写 PRD」 | pattern-product-requirement-review-4d-checklist | PRD-[change-id].md |
| 2 | PRD 评审 | 产品经理/主 Agent | prd-review | 「评审 PRD」「PRD 自检」 | pattern-prd-architecture-review-audit-trail | PRD-评审纪要.md |
| 3 | 工程结构分析 | 架构 Agent | project-analysis | 「分析技术方案」「写 design.md」 | pattern-observable-small-steps | design.md |
| 4 | 技术方案评审 | 架构/主 Agent | architecture-review | 「评审技术方案」「架构评审」 | pattern-prd-architecture-review-audit-trail | 技术方案-评审纪要.md |
| 5 | 编码实现 | 前端/后端 Agent | coding-implement | 「开始编码」「实现功能」 | pattern-observable-small-steps | 代码 |
| 6 | 代码评审 | 架构 Agent | code-review | 「代码评审」「review 代码」 | pattern-breakthrough-thinking-redefine-problem-space | code-review.md |
| 7 | 功能验收 | 测试 Agent | func-test | 「功能验收」「测试验收」 | pattern-complete-quality-closed-loop | func-test.md |
| 8 | 归档 | 主 Agent | - | 「归档」「完成变更」 | pattern-change-full-lifecycle-delivery | 归档 spec |
| 9 | 复盘与持续改进 | 主/架构/产品 Agent | retrospective-analysis | 「复盘」「总结经验」 | pattern-five-stage-retrospective | 复盘报告、memory |

### 复盘触发条件（确定性执行）

复盘不是可选步骤，满足以下条件**必须触发**：

| 触发条件 | 判定标准 | 触发动作 | 是否可跳过 | 跳过记录 |
|---------|---------|---------|-----------|---------|
| 完成里程碑 | change-id 归档完成 | 主 Agent 建议「是否复盘？」 | 可跳过（需理由） | 迭代日志记录跳过理由 |
| 问题反复 | 同类问题 ≥2 个 change-id | Agent 提示「建议复盘」 | **不可跳过** | - |
| 用户指令 | 用户说「复盘」「总结」 | 立即执行 | **不可跳过** | - |
| 定期复盘 | 每周/每月/每季度 | Agent 主动发起 | 可延期（需新时间） | 迭代日志记录延期时间 |

## 详细执行手册

### Step 1: 需求分析

```yaml
步骤: Step 1
阶段: 需求分析

执行方:
  Agent: 产品经理 Agent
  角色定位: 需求分析专家，产出符合 OpenSpec 规范的 PRD

触发 Skill:
  Skill: request-analysis
  路径: skills/request-analysis/SKILL.md
  触发指令:
    - 「分析需求」
    - 「写 PRD」
    - 「补充需求文档」
    - 「创建 change-id」

唤醒 Memory（自动）:
  必唤醒:
    - pattern-product-requirement-review-4d-checklist:
        作用: PRD 评审 4D 检查清单，确保 PRD 覆盖需求来源、价值、竞品、目标
        时机: 产出 PRD 前，作为自检参考
  选唤醒（如涉及）:
    - pattern-observable-small-steps:
        条件: 需求涉及长时间运行的工作流
        作用: 阶段化执行设计参考

执行流程:
  1. 确定/创建 change-id
  2. 创建 docs/project-prd-changes/[change-id]/ 目录
  3. 产出 PRD（8 类内容）
  4. 自检（9 项清单）
  5. 更新迭代日志

产出物:
  主产出: docs/project-prd-changes/[change-id]/PRD-[change-id]-[关键词].md
  辅助产出:
    - 市场研究与产品方案.md（可选）
    - 功能需求说明书.md（可选）
    - 需求验收 Checklist.md（可选）

准出条件:
  - PRD 产出完成
  - 自检清单通过
  - 迭代日志已更新

衔接下一步:
  条件: 准出条件满足
  下一步: Step 2 (prd-review)
  触发方式:
    自动: 主 Agent 检测到 PRD 产出后，自动指派 prd-review
    手动: 用户指令「评审这个 PRD」

质量门禁:
  PRD 结构不完整 → 补充完整后再进入评审
```

### Step 2: PRD 评审

```yaml
步骤: Step 2
阶段: PRD 评审

执行方:
  Agent: 产品经理 Agent / 主 Agent
  角色定位: PRD 质量把关者，确保需求清晰、可落地

触发 Skill:
  Skill: prd-review
  路径: skills/prd-review/SKILL.md
  触发指令:
    - 「评审 PRD」
    - 「检查 PRD 质量」
    - 「PRD 自检」
    - 「审查需求文档」

唤醒 Memory（自动）:
  必唤醒:
    - pattern-prd-architecture-review-audit-trail:
        作用: 评审留痕机制规范，指导如何产出评审纪要
        时机: 评审开始时，按此规范执行评审
    - preference-prd-architecture-naming-convention:
        作用: PRD 命名规范检查
        时机: 评审第 9 项「文档命名规范」时

执行流程:
  1. 加载 REFERENCE (迭代需求说明-PRD最小结构与自检.md)
  2. 按 9 项自检清单逐项评审
  3. 记录评审发现、判定、理由、建议、依据
  4. 形成综合判定
  5. 产出评审纪要
  6. 更新迭代日志

产出物:
  主产出: docs/project-prd-changes/[change-id]/records/PRD-[change-id]-评审纪要.md
  结构:
    - 1. 评审基本信息
    - 2. 评审过程记录（逐项自检）
    - 3. 问题发现与处理
    - 4. 整体评审结论
    - 5. 附录

准出条件（综合判定）:
  通过: 所有自检项均通过（或仅 minor 建议）
  有条件通过: 存在有条件通过项，但无阻塞问题
  不通过: 存在不通过项

衔接下一步:
  通过: → Step 3 (project-analysis)
  有条件通过: → Step 3 (并行记录优化项)
  不通过: → 退回 Step 1 (修改 PRD)

质量门禁:
  不通过 → 必须修改 PRD，重新评审
  有条件通过 → 记录优化项，后续迭代完成
```

### Step 3: 工程结构分析

```yaml
步骤: Step 3
阶段: 工程结构分析

执行方:
  Agent: 架构 Agent
  角色定位: 架构设计专家，产出技术方案

触发 Skill:
  Skill: project-analysis
  路径: skills/project-analysis/SKILL.md
  触发指令:
    - 「分析技术方案」
    - 「写 design.md」
    - 「分析工程结构」

唤醒 Memory（自动）:
  必唤醒:
    - pattern-complete-quality-closed-loop:
        作用: 了解完整流程，明确技术方案在闭环中的位置
        时机: 开始前，理解上下文
  选唤醒（如涉及）:
    - pattern-observable-small-steps:
        条件: PRD 涉及长时间运行的工作流
        作用: 阶段化执行架构设计参考
    - pattern-breakthrough-thinking-redefine-problem-space:
        条件: 技术方案需要架构创新
        作用: 突破性思维指导

执行流程:
  1. 读取 PRD 和评审纪要
  2. 分析工程结构影响
  3. 产出技术方案 (design.md，6 章节)
  4. 可选: 更新 project.md、project-rules/
  5. 自检（9 项清单）
  6. 更新迭代日志

产出物:
  主产出: openspec/changes/[change-id]/design.md
  辅助产出:
    - 架构图、执行逻辑图、数据流图（可选）
    - project-rules/ 下补充约束（可选）

准出条件:
  - 技术方案产出完成
  - 与 PRD 对应关系明确
  - 自检通过

衔接下一步:
  条件: 准出条件满足
  下一步: Step 4 (architecture-review)
  触发方式:
    自动: 主 Agent 检测到技术方案产出后，自动指派 architecture-review
    手动: 用户指令「评审这个技术方案」

质量门禁:
  与 PRD 不一致 → 对齐后再进入评审
```

### Step 4: 技术方案评审

```yaml
步骤: Step 4
阶段: 技术方案评审

执行方:
  Agent: 架构 Agent / 主 Agent
  角色定位: 架构质量把关者，确保技术方案可行、可落地

触发 Skill:
  Skill: architecture-review
  路径: skills/architecture-review/SKILL.md
  触发指令:
    - 「评审技术方案」
    - 「架构评审」
    - 「检查 design.md」
    - 「技术方案自检」

唤醒 Memory（自动）:
  必唤醒:
    - pattern-prd-architecture-review-audit-trail:
        作用: 评审留痕机制规范
        时机: 评审开始时
    - pattern-breakthrough-thinking-redefine-problem-space:
        作用: 评审时识别架构创新点
        时机: 评审架构合理性时

执行流程:
  1. 加载 REFERENCE (技术方案与架构产出物-最小结构与自检.md)
  2. 对照 PRD 评审技术方案
  3. 按 9 项自检清单逐项评审
  4. 记录评审发现、判定、理由、建议、依据
  5. 形成综合判定
  6. 产出评审纪要
  7. 更新迭代日志

产出物:
  主产出: docs/project-prd-changes/[change-id]/records/技术方案-[change-id]-评审纪要.md
  结构:
    - 1. 评审基本信息
    - 2. 评审过程记录（逐项自检）
    - 3. 问题发现与处理
    - 4. 整体评审结论
    - 5. 附录

准出条件（综合判定）:
  通过: 所有自检项均通过（或仅 minor 建议）
  有条件通过: 存在有条件通过项，但无阻塞问题
  不通过: 存在不通过项

衔接下一步:
  通过: → Step 5 (coding-implement)
  有条件通过: → Step 5 (并行记录优化项)
  不通过: → 退回 Step 3 (修改技术方案)

质量门禁:
  不通过 → 必须修改技术方案，重新评审
  与 PRD 不一致 → 对齐后再进入编码
```

### Step 5: 编码实现

```yaml
步骤: Step 5
阶段: 编码实现

执行方:
  Agent: 前端 Agent / 后端 Agent
  角色定位: 代码实现者，按技术方案产出代码

触发 Skill:
  Skill: coding-implement
  路径: skills/coding-implement/SKILL.md
  触发指令:
    - 「开始编码」
    - 「实现功能」
    - 「写代码」
    - 「根据 design.md 实现」

唤醒 Memory（自动）:
  必唤醒:
    - pattern-complete-quality-closed-loop:
        作用: 了解在闭环中的位置，明确准出条件
        时机: 开始前
  选唤醒（如涉及）:
    - pattern-observable-small-steps:
        条件: 实现阶段化执行逻辑
        作用: 阶段化执行实现参考

执行流程:
  1. 读取技术方案和评审纪要
  2. 按技术方案实现代码
  3. 遵循 project.md 和 project-rules/ 约束
  4. 实现完成自检
  5. 更新 tasks.md 任务状态
  6. 更新迭代日志

产出物:
  主产出: 代码文件
  辅助产出:
    - info-database/ 下表结构说明（如涉及）
    - info-service-interface/ 下接口说明（如涉及）

准出条件:
  - 代码实现完成
  - 实现自检通过
  - tasks.md 已更新

衔接下一步:
  条件: 准出条件满足
  下一步: Step 6 (code-review)
  触发方式:
    自动: 主 Agent 检测代码实现完成
    手动: 用户指令「review 这段代码」

质量门禁:
  实现与技术方案不符 → 调整实现或更新技术方案
  自检不通过 → 修复后再进入评审
```

### Step 6: 代码评审

```yaml
步骤: Step 6
阶段: 代码评审

执行方:
  Agent: 架构 Agent
  角色定位: 代码质量把关者，确保实现符合方案

触发 Skill:
  Skill: code-review
  路径: skills/code-review/SKILL.md
  触发指令:
    - 「代码评审」
    - 「review 代码」
    - 「检查实现质量」

唤醒 Memory（自动）:
  必唤醒:
    - pattern-complete-quality-closed-loop:
        作用: 了解代码评审在闭环中的位置
        时机: 评审开始时

执行流程:
  1. 读取技术方案和实现代码
  2. 对照技术方案评审代码
  3. 检查维度:
    - 需求符合性
    - 架构分层
    - 代码质量
    - 安全/性能
    - 日志与监控
    - 测试覆盖
  4. 产出评审记录
  5. 更新迭代日志

产出物:
  主产出: docs/project-prd-changes/[change-id]/records/[change-id]-code-review.md
  内容: 问题清单与后续行动

准出条件:
  - 无 Blocking/Major 级问题
  - 或问题已转化为 tasks.md 任务

衔接下一步:
  条件: 准出条件满足
  下一步: Step 7 (func-test)

质量门禁:
  Blocking 问题 → 修复后才能进入验收
  Major 问题 → 评估后决定是否修复或记录技术债务
```

### Step 7: 功能验收

```yaml
步骤: Step 7
阶段: 功能验收

执行方:
  Agent: 测试 Agent
  角色定位: 质量验证者，确保功能符合需求

触发 Skill:
  Skill: func-test
  路径: skills/func-test/SKILL.md
  触发指令:
    - 「功能验收」
    - 「测试验收」
    - 「验收功能」

唤醒 Memory（自动）:
  必唤醒:
    - pattern-complete-quality-closed-loop:
        作用: 了解验收在闭环中的位置，明确验收标准
        时机: 验收开始时
    - pattern-prd-architecture-review-audit-trail:
        作用: 对照验收 Checklist 逐项验证
        时机: 验收执行时

执行流程:
  1. 读取 specs 和需求验收 Checklist
  2. 执行功能测试
  3. 执行 OpenSpec validate（两轮）
  4. 产出验收记录
  5. 更新迭代日志

产出物:
  主产出: docs/project-prd-changes/[change-id]/records/[change-id]-func-test.md
  内容: 测试用例、测试结果、validate 结果

准出条件:
  - 所有验收 Checklist 项通过
  - openspec validate --strict 通过

衔接下一步:
  条件: 准出条件满足
  下一步: Step 8 (归档)

质量门禁:
  关键功能未通过 → 修复后重新验收
  validate 不通过 → 对齐文档与实现
```

### Step 8: 归档完成

```yaml
步骤: Step 8
阶段: 归档完成

执行方:
  Agent: 主 Agent
  角色定位: 变更闭环者，完成归档

触发 Skill:
  无特定 Skill，由主 Agent 执行归档流程

唤醒 Memory（自动）:
  必唤醒:
    - pattern-change-full-lifecycle-delivery:
        作用: 变更全生命周期交付规范
        时机: 归档开始时

执行流程:
  1. 更新 tasks.md，勾选所有已完成任务
  2. 执行 openspec archive [change-id]
  3. 更新迭代日志，标记变更完成
  4. 可选: 创建复盘文档

产出物:
  归档的 spec: openspec/specs/[capability]/spec.md
  完整的 records: docs/project-prd-changes/[change-id]/records/
  可选: 复盘文档

准出条件:
  - 所有任务已完成
  - 验收通过
  - 文档完整归档

闭环完成!
```

## 触发词与唤醒词对照表

### 用户指令 → Agent-Skill-Memory 映射

| 用户指令 | 判定步骤 | 指派 Agent | 触发 Skill | 唤醒 Memory |
|---------|---------|-----------|-----------|------------|
| 「分析需求」「写 PRD」 | Step 1 | 产品经理 Agent | request-analysis | pattern-product-requirement-review-4d-checklist |
| 「评审 PRD」「PRD 自检」 | Step 2 | 产品经理/主 Agent | prd-review | pattern-prd-architecture-review-audit-trail |
| 「分析技术方案」「写 design.md」 | Step 3 | 架构 Agent | project-analysis | pattern-complete-quality-closed-loop |
| 「评审技术方案」「架构评审」 | Step 4 | 架构/主 Agent | architecture-review | pattern-prd-architecture-review-audit-trail |
| 「开始编码」「实现功能」 | Step 5 | 前端/后端 Agent | coding-implement | pattern-complete-quality-closed-loop |
| 「代码评审」「review 代码」 | Step 6 | 架构 Agent | code-review | pattern-complete-quality-closed-loop |
| 「功能验收」「测试验收」 | Step 7 | 测试 Agent | func-test | pattern-complete-quality-closed-loop |
| 「归档」「完成变更」 | Step 8 | 主 Agent | - | pattern-change-full-lifecycle-delivery |

## 记忆唤醒的自动化规则

### 主 Agent 的唤醒职责

```yaml
触发条件:
  - 完成 simple/heavy 判定后
  - 识别到当前步骤属于质量闭环流程

唤醒策略:
  一跳检索: 只加载当前步骤直接相关的 memory，不递归
  克制加载: 最多加载 2-3 条核心 memory

必唤醒（所有步骤）:
  - pattern-complete-quality-closed-loop:
      作用: 了解完整流程上下文
      时机: 任意步骤开始时

步骤特定唤醒:
  Step 1 (需求分析):
    - pattern-product-requirement-review-4d-checklist
  
  Step 2 (PRD 评审):
    - pattern-prd-architecture-review-audit-trail
    - preference-prd-architecture-naming-convention
  
  Step 3 (工程结构分析):
    - pattern-observable-small-steps (如涉及长事务)
  
  Step 4 (技术方案评审):
    - pattern-prd-architecture-review-audit-trail
    - pattern-breakthrough-thinking-redefine-problem-space
  
  Step 5 (编码实现):
    - pattern-observable-small-steps (如实现阶段化)
  
  Step 7 (功能验收):
    - pattern-prd-architecture-review-audit-trail (对照 Checklist)
  
  Step 8 (归档):
    - pattern-change-full-lifecycle-delivery
```

## 遗漏检查清单

### 本手册是否遗漏高价值映射？

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 所有 9 步都映射到 Agent | ✅ | 已完整映射（新增 Step 9 复盘） |
| 所有 9 步都映射到 Skill | ✅ | 已完整映射（Step 8 无特定 Skill，Step 9 为 retrospective-analysis） |
| 所有 9 步都映射到 Memory | ✅ | 已完整映射 |
| 提供了触发指令示例 | ✅ | 已提供 |
| 提供了产出物路径 | ✅ | 已提供 |
| 提供了准出条件 | ✅ | 已提供 |
| 提供了质量门禁 | ✅ | 已提供 |
| 提供了衔接下一步规则 | ✅ | 已提供 |
| 复盘触发条件明确 | ✅ | 4 种触发条件（完成里程碑/问题反复/用户指令/定期） |

## 与现有文档的关系

```
┌─────────────────────────────────────────────────────────────┐
│                    文档关系图                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  pattern-complete-quality-closed-loop                       │
│  （模式定义：是什么、为什么）                                 │
│              │                                              │
│              ▼                                              │
│  playbook-agent-skill-memory-mapping-for-quality-closed-loop │
│  （本手册：怎么做、谁来做、唤醒什么）                          │
│              │                                              │
│              ├──────────────────┬──────────────────┐          │
│              ▼                  ▼                  ▼          │
│  skills/*/SKILL.md          agents/*.md       memory/*.md   │
│  （具体技能执行）            （Agent 定义）      （经验沉淀）  │
│                                                             │
│  关系：                                                       │
│  • 模式定义流程（pattern）                                     │
│  • 手册映射执行（playbook）                                    │
│  • 技能具体实现（skill）                                       │
│  • Agent 执行角色（agent）                                     │
│  • Memory 唤醒参考（memory）                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 使用示例

### 示例 1: 主 Agent 自动调度

```
用户: 「推进 check-langgraph-backend」

主 Agent:
1. 识别 change-id: check-langgraph-backend
2. 判定步骤: 当前处于哪个步骤？
   - 检查 docs/project-prd-changes/check-langgraph-backend/PRD-xxx.md 是否存在
   - 检查 records/PRD-xxx-评审纪要.md 是否存在
   - ...
3. 假设当前是 Step 1 刚完成:
   - 指派 Agent: 产品经理/主 Agent
   - 触发 Skill: prd-review
   - 唤醒 Memory: pattern-prd-architecture-review-audit-trail
4. 执行评审，产出评审纪要
5. 更新迭代日志
```

### 示例 2: 用户明确指定

```
用户: 「帮我评审一下这个技术方案」

主 Agent:
1. 识别意图: 用户要求技术方案评审
2. 识别 change-id: 从上下文或询问用户
3. 指派 Agent: 架构 Agent / 主 Agent
4. 触发 Skill: architecture-review
5. 唤醒 Memory:
   - pattern-prd-architecture-review-audit-trail (评审规范)
   - pattern-breakthrough-thinking-redefine-problem-space (架构创新)
6. 执行评审，产出评审纪要
```

## 沉淀来源

- **复盘事件**: check-langgraph-backend 完整复盘
- **复盘日期**: 2026-03-14
- **复盘文档**: `docs/project-prd-changes/复盘报告-2026-03-14-最近2天工作内容完整复盘.md`
- **核心洞察**: 需要建立显性映射，确保质量闭环流程可被正确执行和唤醒

---

**手册版本**: v1.0  
**最后更新**: 2026-03-14  
**维护者**: agentsystem 架构组
