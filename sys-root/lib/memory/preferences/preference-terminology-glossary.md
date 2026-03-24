---
id: preference-terminology-glossary
title: OpenSpec 规范术语表
type: preference
description: OpenSpec 及 8+1 质量闭环的完整规范术语表，包含术语定义、来源、关联文档、常见理解偏差和自动链接映射
description_long: |
  术语定义漂移的根本原因是缺乏统一的术语表和快速查阅机制。
  本术语表汇总 OpenSpec 和 8+1 质量闭环中的所有关键术语，提供：
  - 精确的规范定义
  - 术语来源（OpenSpec.md、skill 文档等）
  - 常见理解偏差和正确理解
  - 自动链接映射（术语 → 规范文档）
  
  本术语表应作为执行前查阅规范机制的核心参考文档。
applicable_projects:
  - agentsystem
  - "*"
tags:
  - 偏好
  - 术语表
  - 规范定义
  - 快速查阅
  - 防漂移
related:
  - anti-pattern-terminology-drift
  - skills-rules-for-agent.md
  - OpenSpec.md
  - pattern-complete-quality-closed-loop
created_by: 合并行动计划-2026-03-16-item-13
created_date: 2026-03-17
version: 1.0
---

# OpenSpec 规范术语表

## 使用说明

**术语查阅原则**:
1. **执行前必查**: 执行任何涉及规范术语的操作前，查阅本表确认理解正确
2. **精确使用**: 使用术语时，确保符合本表的规范定义
3. **避免偏差**: 特别注意「常见理解偏差」列，避免犯同样错误
4. **追溯来源**: 如需深入了解，查阅「规范来源」列的原始文档

**自动链接机制**:
- 本表中的每个术语都已建立到规范文档的自动链接
- 在 skill 文档中引用术语时，应链接到本表或原始规范
- 工具可基于本表自动识别术语并添加链接

---

## 核心术语表（按字母排序）

### A

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **APPROVAL（批准）** | 对提案/规范的正式认可，表示可以进入实施阶段 | OpenSpec.md 4.3 | 口头同意即可 | 需要正式的评审和批准流程 | `openspec/changes/[id]/proposal.md` |
| **Archive（归档）** | 将已完成的变更从 changes/ 合并到 specs/ 并移动到 archive/ 的完整操作 | OpenSpec.md 阶段3 | 标记完成即可 | 合并 specs/ + 移动 changes/ 到 archive/ | `openspec/changes/archive/[id]-日期/` |
| **Agent** | 在 8+1 闭环中承担特定职责的执行角色（如主 Agent、后端 Agent） | `agents/*.md` | 任意执行者 | 有明确定义的职责和技能映射 | `agentsystem/agents/*.md` |

### C

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Capability（能力）** | 系统中可独立交付的功能单元，如 user-auth、payment | OpenSpec.md 3.2 | 模块或组件 | 按业务域划分的能力单元 | `openspec/specs/[capability]/` |
| **Change（变更）** | 待实施的提案，包含 proposal、tasks、specs 等 | OpenSpec.md 3.3 | 任意修改 | 遵循 changes/ 目录结构的完整提案 | `openspec/changes/[change-id]/` |
| **Change-id** | 唯一标识一个变更的 kebab-case 字符串，动词开头 | OpenSpec.md 3.3 | 任意编号 | 如 `check-langgraph-backend`、`add-feature-x` | `openspec/changes/[change-id]/` |
| **Code Review（代码评审）** | 对代码实现进行系统化评审，确保符合 spec 和架构约定 | code-review v1.1 | 简单看看代码 | 9项检查+结论+修复循环 | `skills/code-review/SKILL.md` |
| **Coding Implement（编码实现）** | 根据需求和结构设计完成具体编码实现 | coding-implement | 随意编写 | 按分层规范和约定实现 | `skills/coding-implement/SKILL.md` |
| **Conditional Pass（有条件通过）** | 评审/验收结论：基本可用但存在问题，必须修复后重新评审 | prd-review v1.1 | 可以进入下一阶段 | **必须修复 → 重新评审 → 转为「通过」** | `memory/patterns/pattern-review-fix-loop` |

### D

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Design.md（技术方案）** | 复杂变更的技术决策文档，包含架构、接口、流程 | OpenSpec.md 4.5 | 简单设计说明 | 必须符合最小结构和自检清单 | `openspec/changes/[id]/design.md` |
| **Delta（增量）** | 本变更对某能力的增量（ADDED/MODIFIED/REMOVED） | OpenSpec.md 4.6 | 完整重写 | 只描述变更的部分，使用 ADDED/MODIFIED/REMOVED | `openspec/changes/[id]/specs/[cap]/spec.md` |

### F

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Fail（不通过）** | 评审/验收结论：存在阻塞性问题，必须修复后重新评审 | prd-review v1.1 | 可以协商进入下一阶段 | **必须修复 → 重新评审 → 转为「通过」** | `memory/patterns/pattern-review-fix-loop` |
| **Func Test（功能验收）** | 对功能进行系统化测试与验收，确保实现与 spec 一致 | func-test v1.1 | 简单测试 | 两轮 OpenSpec 验证 + 修复循环 | `skills/func-test/SKILL.md` |

### I

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Iteration Log（迭代日志）** | 记录所有 change-id 下 Agent/技能调用的单一文件 | projects-rules-for-agent.md | 各 change-id 分散记录 | 必须是单一文件 `docs/项目事件日志.md` | `docs/项目事件日志.md` |

### M

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Memory** | 跨项目可复用的知识资产（pattern/anti-pattern/preference/playbook/reflection） | memory/schema.md | 任意笔记 | 遵循 schema 规范的结构化知识 | `memory/[type]/[id].md` |
| **Milestone（里程碑）** | 重要的项目节点，如完成一个 change-id | pattern-complete-quality-closed-loop | 任意节点 | 完成归档的重要节点，触发复盘 | - |
| **Execution Deviation（执行偏差记录）** | 执行过程中发现问题/偏差时的**即时记录**，属于运行时审计 | runtime-logs 设计 | "执行偏差记录就是复盘" | 执行偏差记录≠复盘；前者是即时事实记录（runtime-logs/execution-deviations/），后者是事后方法论总结（docs/retrospective/） | `runtime-logs/execution-deviations/` |
| **Retrospective（复盘）** | 变更/阶段结束后的**系统性总结**，必须含目标→过程→根因→改进→沉淀 | 目录结构规范 V3 Step 9 | "复盘可以放在 runtime-logs" | 复盘必须在 `docs/retrospective/`，有严格结构 | `docs/retrospective/[level]/` |

### P

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Pass（通过）** | 评审/验收结论：100% 通过，可直接进入下一阶段 | prd-review v1.1 | 差不多即可 | **必须 100% 通过，无有条件通过项** | `memory/patterns/pattern-review-fix-loop` |
| **Pattern（模式）** | 可复用的解决方案或方法论 | memory/schema.md | 任意经验 | 遵循 schema 的通用解决方案 | `memory/patterns/pattern-*.md` |
| **Phase（阶段）** | 8+1 质量闭环中的一个步骤（Step 1-9） | pattern-complete-quality-closed-loop | 任意步骤 | 有明确准入准出和门禁检查的步骤 | `memory/patterns/pattern-complete-quality-closed-loop` |
| **PRD Review（PRD 评审）** | 对 PRD 进行系统化评审，确保可商业化、可技术落地 | prd-review v1.1 | 简单看看 PRD | 9项检查+结论+修复循环 | `skills/prd-review/SKILL.md` |
| **Preference（偏好）** | 偏好/最佳实践/检查清单 | memory/schema.md | 任意建议 | 遵循 schema 的推荐实践 | `memory/preferences/preference-*.md` |
| **Project Analysis（工程结构分析）** | 分析工程结构，确保变更与架构/技术栈兼容 | project-analysis | 简单分析 | 产出 project.md、project-rules/ | `skills/project-analysis/SKILL.md` |
| **Proposal（提案）** | 声明变更目标、范围、非目标、依赖与风险 | OpenSpec.md 4.3 | 简单描述 | 必须符合 proposal.md 结构 | `openspec/changes/[id]/proposal.md` |
| **Quality Gate（质量门禁）** | 阶段出口的强制检查机制 | preference-quality-gate-checklist | 可选检查 | **必须全部通过才能进入下一阶段** | `memory/preferences/preference-quality-gate-checklist` |

### Q

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Quality Gate Checklist（质量门禁检查清单）** | 覆盖 8+1 每个阶段的详细检查清单 | preference-quality-gate-checklist | 可选参考 | **必须逐项检查的执行清单** | `memory/preferences/preference-quality-gate-checklist` |

### R

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Re-review（重新评审）** | 首次评审为「有条件通过」/「不通过」后，修复问题后的再次评审 | prd-review v1.1 | 直接通过 | 必须产出重新评审纪要 | `docs/project-prd-changes/[id]/records/*-重新评审纪要.md` |
| **Records（记录目录）** | 存放评审纪要、验收记录、复盘报告等 | OpenSpec.md 1.1 | 任意位置 | 必须放在 `docs/project-prd-changes/[id]/records/` | `docs/project-prd-changes/[id]/records/` |
| **Request Analysis（需求分析）** | 分析需求并产出结构化文档和变更提案 | request-analysis | 简单聊聊需求 | 产出 PRD、proposal、tasks、specs | `skills/request-analysis/SKILL.md` |
| **Retrospective（复盘）** | 系统性回顾工作过程，识别问题根因、提炼经验 | retrospective-analysis | 简单总结 | 5 阶段复盘法，产出复盘报告 | `skills/retrospective-analysis/SKILL.md` |
| **Review-Fix Loop（评审修复循环）** | 评审 → 修复 → 重新评审 → 通过的循环机制 | pattern-review-fix-loop | 一次评审即可 | **必须循环直到 100% 通过** | `memory/patterns/pattern-review-fix-loop` |

### S

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Scenario（场景）** | Requirement 的具体使用场景（Given-When-Then） | OpenSpec.md 4.6 | 简单描述 | 使用 Given-When-Then 结构 | `openspec/changes/[id]/specs/[cap]/spec.md` |
| **Skill** | Agent 可调用的技能，包含 SKILL.md 和 REFERENCE | skills-rules-for-agent.md | 任意能力 | 有明确定义的触发场景、执行流程、产出物 | `agentsystem/skills/[skill]/SKILL.md` |
| **Spec（规范）** | 已实现的功能规范 | OpenSpec.md 2 | 任意文档 | 按能力分目录的 Requirements + Scenarios | `openspec/specs/[capability]/spec.md` |
| **Stage（阶段）** | 同 Phase | pattern-complete-quality-closed-loop | - | 8+1 闭环中的一个步骤 | `memory/patterns/pattern-complete-quality-closed-loop` |
| **Step 1-9** | 8+1 质量闭环的 9 个步骤 | pattern-complete-quality-closed-loop | 任意流程 | 有明确准入准出和质量门禁的步骤 | `memory/patterns/pattern-complete-quality-closed-loop` |

### T

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Tasks.md（任务清单）** | 实施任务清单，使用 `- [ ]` / `- [x]` 格式 | OpenSpec.md 4.4 | 简单 todo | 必须标注负责人和验收标准 | `openspec/changes/[id]/tasks.md` |
| **Terminology Drift（术语定义漂移）** | 将规范术语按日常理解执行，而非查阅规范定义 | anti-pattern-terminology-drift | 不可避免 | **可以通过查阅本术语表避免** | `memory/anti-patterns/anti-pattern-terminology-drift` |

### V

| 术语 | 规范定义 | 规范来源 | 常见理解偏差 | 正确理解 | 自动链接 |
|-----|---------|---------|-------------|---------|---------|
| **Validate（验证）** | 使用工具检查 OpenSpec 目录结构完整性 | openspec_validate.py | 人工检查 | 使用 validate 工具自动检查 | `scripts/openspec-validate/openspec_validate_v2.py` |

---

## 8+1 质量闭环术语（按步骤）

### Step 1: 需求分析 (request-analysis)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **PRD** | 产品需求文档，包含 8 类内容 | `docs/project-prd-changes/[id]/PRD-[id]-[关键词].md` | 9 项自检全部通过 |
| **Proposal** | 变更提案 | `openspec/changes/[id]/proposal.md` | 引用 PRD 路径 |
| **Tasks** | 任务拆分 | `openspec/changes/[id]/tasks.md` | 任务可执行、可验证 |
| **Spec** | 规范增量 | `openspec/changes/[id]/specs/[cap]/spec.md` | ADDED/MODIFIED/REMOVED |

### Step 2: PRD 评审 (prd-review)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **评审结论** | 通过/有条件通过/不通过 | 评审纪要 | **必须通过（100%）** |
| **评审修复循环** | 有条件通过 → 修复 → 重新评审 → 通过 | 重新评审纪要 | 必须循环直到通过 |

### Step 3: 工程结构分析 (project-analysis)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **技术方案** | 架构与实现方案 | `design.md`（如需要） | 最小结构自检 |
| **Project.md** | 项目宪法 | `openspec/project.md` | 与变更范围一致 |

### Step 4: 技术方案评审 (architecture-review)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **架构评审结论** | 通过/有条件通过/不通过 | 评审纪要 | **必须通过（100%）** |
| **架构修复循环** | 有条件通过 → 修复 → 重新评审 → 通过 | 重新评审纪要 | 必须循环直到通过 |

### Step 5: 编码实现 (coding-implement)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **实现完成自检** | 按 REFERENCE 自检 | 代码 + 更新 tasks.md | 自检通过 |
| **代码可测试性** | 便于单元/集成测试 | 测试任务 | 可测试 |

### Step 6: 代码评审 (code-review)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **代码评审结论** | 通过/有条件通过/不通过 | 评审纪要 v1.1 | **必须通过（100%）** |
| **问题分级** | Blocking/Major/Minor | 问题清单 | Blocking 必须修复 |
| **代码评审修复循环** | 有条件通过 → 修复 → 重新评审 → 通过 | 重新评审纪要 | 必须循环直到通过 |

### Step 7: 功能验收 (func-test)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **第一轮验证** | `openspec validate [id]` | 验证结果 | 通过 |
| **验收结论** | 通过/有条件通过/不通过 | 验收记录 v1.1 | **必须通过（100%）** |
| **验收修复循环** | 有条件通过 → 修复 → 重新验收 → 通过 | 重新验收记录 | 必须循环直到通过 |
| **第二轮验证** | `openspec validate --strict` | 严格模式验证 | 通过 |

### Step 8: 归档 (archive)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **术语检查** | 查阅归档定义 | 执行声明 | 理解正确 |
| **合并 Specs** | 将 changes/[id]/specs/ 合并到 specs/ | 更新的 specs/ | 验证合并结果 |
| **移动 Changes** | 将 changes/[id]/ 移动到 archive/ | archive/[id]-日期/ | 验证移动结果 |
| **归档验证** | 可追溯性检查 | 归档声明 | 全部通过 |

### Step 9: 复盘 (retrospective-analysis)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **5 阶段复盘** | 目标→结果→原因→经验→行动 | 复盘报告 | 9 项自检 |
| **Memory 沉淀** | pattern/anti-pattern/preference/playbook/reflection | Memory 文档 | 评估价值 |

### Step 10: 全局检查与联动更新 (system-consistency-validation)

| 术语 | 定义 | 关键产出 | 质量门禁 |
|-----|------|---------|---------|
| **变更影响分析** | 识别变更对6类文档的影响范围 | 影响分析清单 | 全面识别 |
| **全局检查** | 检查根级/宿主/Agent/规则/Skill/Memory文档 | 全局检查报告 | 逐项通过 |
| **联动更新** | 同步更新所有受影响文档 | 联动更新声明 | 无遗漏 |
| **版本号格式** | 语义版本 `vX.Y`，禁止日期格式 | 版本号验证 | 格式统一 |
| **遗漏修复循环** | 发现遗漏 → 立即修复 → 重新验证 → 通过 | 修复记录 | 100%通过 |

---

## 自动链接映射表

### 术语 → 文档链接

```yaml
# 术语自动链接配置
terminology_links:
  # 核心概念
  "归档": 
    - "openspec/changes/archive/"
    - "memory/preferences/preference-archive-operation-checklist"
  "评审":
    - "memory/patterns/pattern-review-fix-loop"
    - "anti-pattern-conditional-pass-as-go"
  "验收":
    - "skills/func-test/SKILL.md"
    - "memory/patterns/pattern-review-fix-loop"
  
  # 反模式
  "术语定义漂移":
    - "memory/anti-patterns/anti-pattern-terminology-drift"
  "惯性思维陷阱":
    - "memory/anti-patterns/anti-pattern-inertia-trap"
  "有条件通过即放行":
    - "memory/anti-patterns/anti-pattern-conditional-pass-as-go"
  "孤立改进":
    - "memory/anti-patterns/anti-pattern-isolated-improvement"
  
  # 模式
  "评审修复循环":
    - "memory/patterns/pattern-review-fix-loop"
  "完整质量闭环":
    - "memory/patterns/pattern-complete-quality-closed-loop"
  "变更影响分析":
    - "memory/patterns/pattern-change-impact-analysis"
  
  # 偏好
  "质量门禁检查清单":
    - "memory/preferences/preference-quality-gate-checklist"
  "归档操作检查清单":
    - "memory/preferences/preference-archive-operation-checklist"
  "Memory 自动唤醒":
    - "memory/preferences/preference-memory-auto-awakening"
  "联动更新检查清单":
    - "memory/preferences/preference-coordinated-update-checklist"
```

### 自动链接生成规则

1. **文档内链接**: 在 skill 或文档中遇到术语时，自动链接到本表
2. **引用链接**: 引用本表中的术语时，自动展开定义
3. **检查清单链接**: 在质量门禁检查清单中，术语链接到详细说明
4. **反模式预警**: 检测到可能术语漂移时，链接到 anti-pattern 文档

---

## 术语使用检查清单

执行任何任务前，使用以下清单检查术语使用：

```markdown
【术语使用自检】

任务描述: [描述]
涉及的术语: [list]

术语理解检查:
- [ ] 已查阅术语表中每个术语的规范定义
- [ ] 确认理解正确（无偏差）
- [ ] 确认使用场景正确

术语使用检查:
- [ ] 使用的术语符合规范定义
- [ ] 没有使用模糊替代（如用"标记完成"代替"归档"）
- [ ] 术语与上下文一致

术语链接检查:
- [ ] 如需引用，已链接到规范定义
- [ ] 反模式术语已链接到 anti-pattern 文档
- [ ] 模式术语已链接到 pattern 文档
```

---

## 术语表维护指南

### 新增术语

当新增术语时，按以下格式补充到本表：

1. 确定术语分类（核心术语/步骤术语）
2. 按字母顺序插入到对应表格
3. 填写：术语、规范定义、规范来源、常见理解偏差、正确理解、自动链接
4. 更新版本号
5. 在迭代日志中记录更新

### 术语更新

当术语定义更新时：

1. 更新本表中对应术语的定义
2. 更新版本号
3. 标记为「vX.X 更新」
4. 通知所有相关 skill 文档同步更新
5. 在迭代日志中记录更新

### 术语废弃

当术语不再使用时：

1. 在本表中标记为「已废弃」
2. 说明替代术语
3. 保留至少一个版本后删除

---

**术语表版本**: v1.0  
**创建日期**: 2026-03-17  
**术语数量**: 50+  
**覆盖范围**: OpenSpec + 8+1 质量闭环  
**维护者**: agentsystem 架构组
