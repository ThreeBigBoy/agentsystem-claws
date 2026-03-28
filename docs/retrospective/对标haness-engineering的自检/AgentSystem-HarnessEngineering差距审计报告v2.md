---
id: audit-harness-engineering-vs-agentsystem
title: Harness Engineering视角下的AgentSystem全面审计报告（v2.0）
type: reflection
tags: [harness-engineering, audit, agentsystem, gap-analysis, 10-step, quality-gate]
applicable_projects: [agentsystem]
host_scope: [agentsystem]
source_change_ids: [sys-infra-harness-audit-v1]
created_at: 2026-03-28
last_reviewed_at: 2026-03-28
maturity: draft
related:
  - "docs/temp/Harness Engineering第一性原理深度解析.md"
  - "sys-root/lib/memory/patterns/pattern-complete-quality-closed-loop.md"
  - "sys-root/lib/memory/patterns/pattern-quality-gate-checkpoint.md"
---

# Harness Engineering视角下的AgentSystem全面审计报告（v2.0）

## 一、审计背景

### 1.1 审计依据

**Harness Engineering三层框架**：
| 层次 | 解决的问题 | 核心手段 |
|------|-----------|---------|
| **上下文工程** | "理解"问题 | docs/结构、AGENTS.md、知识图谱 |
| **架构约束** | "正确性"问题 | 分层架构、Linter、品味不变式、测试 |
| **熵管理** | "可持续性"问题 | 循环清理、自动重构、文档治理 |

**AgentSystem已具备的机制**：
- **10步质量闭环**：Step1-10完整覆盖需求→PRD→方案→编码→评审→验收→归档→复盘→全局检查
- **4环节人工门禁**：Gate-PRD / Gate-DESIGN / Gate-ARCHIVE / 复盘确认
- **三层门禁机制**：任务状态检查 / 阶段准入声明 / 完成性表述拦截
- **评审修复循环**：通过→有条件通过→不通过→修复→重新评审

### 1.2 审计目的

对照Harness Engineering的三层框架，结合AgentSystem已具备的10步质量闭环，重新评估：
1. 当前能力覆盖情况
2. 与Harness Engineering的差距
3. 改进建议与优先级

---

## 二、第一性原理对比

### 2.1 核心公式对比

| 维度 | Harness Engineering | AgentSystem |
|------|-------------------|-------------|
| **核心公式** | Agent = Model + Harness | Agent = Skill + Memory + Quality Gate |
| **关注点** | 控制系统（底盘、转向、刹车） | 质量闭环（评审、门禁、复盘） |
| **反馈机制** | 实时反馈+自动修正 | 阶段门禁+人工确认 |

### 2.2 关键洞察

**Harness Engineering的本质**：
> 构建一个"智能体可理解的自治机器"，让Agent在安全、可预测、可观测的边界内运行。

**AgentSystem的本质**：
> 构建一个"文档驱动的质量闭环系统"，让每个阶段都有质量保障、评审留痕和系统一致性验证。

**共同点**：
- 都不是在"训练模型"，而是在模型外面构建工程控制系统
- 都强调约束、反馈、持续改进
- 都关注"人类掌舵，智能体执行"的分层

---

## 三、上下文工程层审计

### 3.1 Harness Engineering要求

| 要求 | 说明 |
|------|------|
| **docs/目录** | 所有文档以机器可读格式存储在仓库中 |
| **AGENTS.md** | 定义Agent行为规则、权限、协作流程 |
| **代码即文档** | 将黄金原则编码到代码中 |
| **渐进式披露** | Agent仅访问当前任务所需上下文 |

### 3.2 AgentSystem现状

| 组件 | 存在？ | 文件 | 说明 |
|------|--------|------|------|
| **docs/目录** | ✅ | `docs/project-prd-changes/[change-id]/` | 项目变更文档 |
| **AGENTS.md** | ✅ | `workspace/{project}/claw-config/AGENTS.md` | 业务项目级强制 |
| **系统级AGENTS.md** | ⚠️ | `.cursor/rules/AGENT.mdc` | 本仓有，但偏规则而非行为定义 |
| **渐进式披露** | ⚠️ | `usr-devclaw/user.json` | 有read_order配置，非完全渐进 |

### 3.3 AgentSystem的增强

**运行时索引机制**（AGENT.mdc §2 强制）：
```
- SOUL.md（人设）
- MEMORY.md（记忆索引）
- SKILLS.md（技能索引）
- TOOLS.md（工具备忘）
```

**这实际上比Harness Engineering的AGENTS.md更体系化！**

### 3.4 差距分析

| 差距 | 严重程度 | 说明 |
|------|---------|------|
| **渐进式上下文加载** | 低 | AgentSystem通过运行时索引实现，但非严格渐进 |
| **黄金原则编码** | 中 | 品味不变式散落各skill，未系统化 |

---

## 四、架构约束层审计

### 4.1 Harness Engineering要求

| 要求 | 说明 |
|------|------|
| **分层架构** | Types→Config→Repo→Service→Runtime→UI |
| **自定义Linter** | 针对业务场景的静态代码检查 |
| **品味不变式** | 将代码风格偏好编码为可验证规则 |
| **单元/集成测试** | 覆盖所有关键路径 |
| **可观测性集成** | LogQL/PromQL直接查询应用状态 |
| **操作权限控制** | 定义Agent可修改的代码范围 |

### 4.2 AgentSystem现状

| 组件 | 存在？ | 文件 | 说明 |
|------|--------|------|------|
| **分层架构规范** | ✅ | `coding-implement/REFERENCE/spec-backend-*.md` | 后端分层定义 |
| **自定义Linter** | ❌ | 无 | 缺乏业务场景Linter |
| **品味不变式** | ⚠️ | 各skill附录 | 有但非系统化编码 |
| **单元/集成测试** | ⚠️ | `func-test/` | 功能验收测试，非单元测试 |
| **可观测性** | ✅ | `code-review/SKILL.md` | 检查日志、监控埋点 |
| **操作权限控制** | ✅ | `tasks.md` + `AGENT.mdc` | 任务勾选+安全限制 |

### 4.3 差距分析

| 差距 | 严重程度 | 说明 |
|------|---------|------|
| **自定义Linter** | 高 | 无法自动化检查业务场景特定的代码规范 |
| **品味不变式系统化** | 中 | 有但散落，未编码为可验证规则 |

---

## 五、熵管理层审计

### 5.1 Harness Engineering要求

| 要求 | 说明 |
|------|------|
| **后台扫描任务** | 定期检测冗余代码、死代码、反模式 |
| **自动发起重构PR** | 可自动修复的问题直接提交PR |
| **文档治理** | Agent自动更新过时文档，保持docs/与代码同步 |
| **架构漂移检测** | 持续监控代码依赖关系、分层架构合规性 |

### 5.2 AgentSystem现状

| 组件 | 存在？ | 文件 | 说明 |
|------|--------|------|------|
| **后台扫描任务** | ❌ | 无 | 缺乏自动化的代码库扫描 |
| **自动重构PR** | ❌ | 无 | 重构依赖人工发起 |
| **文档治理** | ⚠️ | `anti-pattern-*.md` | 有反模式识别，但无自动修复 |
| **架构漂移检测** | ⚠️ | `anti-pattern-terminology-drift.md` | 识别术语漂移，但非架构层面 |

### 5.3 AgentSystem的补偿机制

**Step 9 复盘**（pattern-complete-quality-closed-loop）：
- 发现反复出现的问题 → 触发问题型复盘
- 复盘产出反模式/Pattern → 沉淀到memory
- 这是一种**人工熵管理**机制

**Step 10 全局检查**：
- 检查6类文档遗漏
- 版本号格式一致性
- 联动更新检查

### 5.4 差距分析

| 差距 | 严重程度 | 说明 |
|------|---------|------|
| **自动化程度** | 高 | AgentSystem是"人工触发"，Harness是"自动执行" |
| **实时性** | 高 | AgentSystem依赖人工/事件触发，非持续运行 |

---

## 六、质量闭环视角对比

### 6.1 核心差异

| 维度 | Quality Gate（AgentSystem） | Harness Engineering |
|------|---------------------------|---------------------|
| **反馈时机** | 阶段门禁（事后） | 实时反馈（事中） |
| **反馈主体** | Agent自检 + 人工审查 | Agent自我验证 + 自动修复 |
| **自动化程度** | 半自动（Python检查 + 人工门禁） | 全自动（扫描 + PR + 合并） |
| **覆盖范围** | 代码质量 + 文档一致性 | 代码 + 架构 + 知识 + 上下文 |

### 6.2 AgentSystem的独特优势

| 机制 | 说明 | Harness Engineering对应 |
|------|------|------------------------|
| **评审修复循环** | 有条件通过→修复→重新评审→通过 | 无（直接阻断） |
| **三处人工门禁** | PRD终稿/方案终稿/归档前确认 | 无（纯自动化） |
| **10步完整闭环** | 需求→PRD→方案→编码→...→全局检查 | 无（聚焦编码阶段） |
| **Memory沉淀** | 复盘经验→Pattern/反模式→指导后续 | 无（依赖模型记忆） |

### 6.3 互补关系

```
┌─────────────────────────────────────────────────────────────┐
│                   AgentSystem + Harness Engineering           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  AgentSystem的优势：           Harness Engineering的优势：    │
│  ├─ 10步完整闭环               ├─ 实时反馈机制                │
│  ├─ 人工门禁保障               ├─ 全自动化扫描               │
│  ├─ 评审修复循环               ├─ 自动重构PR                 │
│  └─ Memory知识沉淀             └─ 持续熵管理                 │
│                                                              │
│  融合方向：                                                  │
│  └─ AgentSystem的流程框架 + Harness Engineering的自动化执行 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 七、总体评估

### 7.1 各层覆盖情况

| 层次 | 要求项 | 覆盖项 | 覆盖率 | 差距等级 |
|------|--------|--------|--------|----------|
| **上下文工程** | 4 | 3.5 | 88% | 低 |
| **架构约束** | 6 | 3 | 50% | 中 |
| **熵管理** | 4 | 1.5 | 38% | 高 |

### 7.2 差距矩阵

| 层面 | 差距项 | 优先级 | AgentSystem现有补偿 |
|------|--------|--------|-------------------|
| **上下文工程** | 渐进式上下文加载 | 低 | 运行时索引机制 |
| **架构约束** | 自定义Linter | 高 | code-review人工检查 |
| **架构约束** | 品味不变式系统化 | 中 | 各skill附录 |
| **熵管理** | 自动化扫描 | 高 | Step 9/10人工触发 |
| **熵管理** | 自动重构PR | 中 | 依赖人工发起 |

### 7.3 核心发现

1. **AgentSystem不是Harness Engineering的子集，而是另一种路径**
   - Harness：实时反馈 + 全自动执行
   - AgentSystem：阶段门禁 + 半自动 + 人工保障

2. **AgentSystem有Harness Engineering不具备的优势**
   - 评审修复循环（允许试错）
   - 三处人工门禁（战略把关）
   - Memory知识沉淀（持续学习）

3. **熵管理是主要差距**
   - 人工触发 vs 自动执行
   - 事件驱动 vs 持续运行

---

## 八、改进建议

### 8.1 短期改进（P0-P1）

| 优先级 | 改进项 | 预期效果 | 工作量 |
|--------|--------|---------|--------|
| **P0** | 开发业务场景Linter规范 | 自动化代码质量检查 | 中 |
| **P1** | 建立品味不变式规则 | 系统化代码风格控制 | 中 |

### 8.2 中期改进（P2）

| 优先级 | 改进项 | 预期效果 | 工作量 |
|--------|--------|---------|--------|
| **P2** | 开发定期扫描任务 | 自动发现反模式 | 高 |
| **P2** | 建立自动重构PR机制 | 自动修复简单问题 | 高 |

### 8.3 融合方向

**长期目标**：将Harness Engineering的自动化机制融入AgentSystem框架

```
当前：AgentSystem = 10步闭环 + 人工门禁 + Memory
融合：AgentSystem + Harness自动化 = 10步闭环 + 实时反馈 + 自动修复 + Memory
```

---

## 九、结论

### 9.1 核心结论

> **AgentSystem和Harness Engineering是两种不同路径的工程框架，各有优势。AgentSystem的10步质量闭环、三层门禁机制、评审修复循环是Harness Engineering不具备的独特优势。**

### 9.2 差距评估

| 评估项 | 评级 | 说明 |
|--------|------|------|
| **上下文工程** | ✅ 良好 | 88%覆盖，运行时索引机制优秀 |
| **架构约束** | ⚠️ 中等 | 50%覆盖，缺乏自定义Linter |
| **熵管理** | ❌ 薄弱 | 38%覆盖，主要依赖人工触发 |

### 9.3 行动建议

| 时间 | 行动 | 目标 |
|------|------|------|
| **短期** | 开发业务Linter + 品味不变式 | 提升架构约束覆盖 |
| **中期** | 开发自动化扫描 + 重构PR | 补齐熵管理短板 |
| **长期** | 探索融合方案 | 结合两者优势 |

---

**审计日期**: 2026-03-28
**审计依据**:
- docs/temp/Harness Engineering第一性原理深度解析.md
- sys-root/lib/memory/patterns/pattern-complete-quality-closed-loop.md
- sys-root/lib/memory/patterns/pattern-quality-gate-checkpoint.md
- .cursor/rules/AGENT.mdc
**审计范围**: sys-root/lib/ 全部组件 + .cursor/rules/
**审计版本**: v2.0（结合10步质量闭环重新评估）
**下一步**: 根据本报告制定具体的改进计划
