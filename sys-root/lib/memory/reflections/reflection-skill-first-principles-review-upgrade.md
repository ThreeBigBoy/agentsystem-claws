---
id: mem-skill-first-principles-review-001
title: 技术方案Skill从关键词罗列到第一性原理的升级
type: reflection
tags: [skill-upgrade, first-principles, quality-gate, architecture-review, technical-design-review]
applicable_projects: [all]
host_scope: [agentsystem]
source_change_ids: [sys-infra-quality-gate-v1]
created_at: 2026-03-28
last_reviewed_at: 2026-03-28
maturity: draft
related: [
  "memory/reflections/reflection-quality-gate-scoring-from-counting-to-quality.md",
  "memory/reflections/reflection-quality-gate-solution-review-dimension-expansion.md"
]
---

## 背景与问题

在完善质量门禁系统时，发现三个与"技术方案撰写、评审"相关的skill存在设计缺陷：

| Skill | 问题 |
|-------|------|
| `architecture-review` | 9项自检清单无质量指标定义，无法区分"做了"和"做好了" |
| `project-analysis` | 5章节结构检查使用关键词计数，可被刷分 |
| `technical-design-review` | 10维度评审仍是关键词匹配判断，未体现第一性原理 |

同时，dev-workflow-orchestration的Step 4调度表不完整：
- **原设计**：只写`architecture-review`
- **应有设计**：应为`architecture-review` + `technical-design-review`（双技能协同）

---

## 第一性原理分析

### 问题诊断：为什么"关键词罗列"不够？

| 问题 | 表现 | 后果 |
|------|------|------|
| **可被刷分** | 堆砌关键词但不理解本质 | 技术方案看起来好但实际差 |
| **无法区分深度** | 写一行"安全性"和写十行都得满分 | 无法反映真实质量 |
| **违背第一性原理** | 关注"有没有"而非"做没做" | 评审不反映方案本质 |

### 技术方案的第一性原理

技术方案是"如何实现"的蓝图，包含：

| 本质要素 | 核心问题 |
|----------|----------|
| **做什么** | 功能需求是否覆盖？ |
| **怎么做** | 数据流和模块设计是否清晰？ |
| **用什么做** | 技术选型是否合理？ |
| **数据存哪** | 存储设计是否合理？ |
| **怎么组织** | 项目结构是否规范？ |
| **怎么交互** | 接口定义是否清晰？ |

### 高质量评审的设计原则

1. **维度设计原则**
   - 这个维度反映什么本质？
   - 缺失这个维度会怎样？
   - 维度之间是否独立？

2. **质量指标设计原则**
   - 指标反映"做没做"而非"做多少"
   - 每项指标有明确的判断标准
   - 指标之间相互独立，不重复计算

3. **防止"凑关键词"**
   - 不仅要有关键词，还要有具体实现描述
   - 验证逻辑完整性
   - 区分引用和实现

---

## 升级内容

### 1. dev-workflow-orchestration Skill调度表

**修改位置**: `skills/dev-workflow-orchestration/SKILL.md` 第172行

**修改前**:
```markdown
| Step 4 | `architecture-review` |
```

**修改后**:
```markdown
| Step 4 | `architecture-review` + `technical-design-review`（双技能协同） |
```

### 2. architecture-review 技能升级

**添加**: 附录A - 第一性原理评审框架（v1.2+）

**核心内容**:
- 6维度评审框架（与check_solution.py对齐）
- 质量指标设计原则
- 自检项与6维度映射表

### 3. technical-design-review 技能升级

**添加**: 附录A - 第一性原理评审框架（v1.1+）

**核心内容**:
- 问题诊断：为什么"关键词罗列"不够
- 第一性原理评分机制（从关键词计数→质量指标评估）
- 10维度与6维度映射
- 质量指标评估示例
- 防止"凑关键词"的设计策略
- 框架替代陷阱识别的第一性原理方法

### 4. project-analysis 技能升级

**添加**: 附录A - 第一性原理产出标准（v1.1+）

**核心内容**:
- 6维度产出框架（与评审框架对齐）
- 质量指标设计原则
- 产出自检清单
- 与评审的对应关系表

---

## 升级效果

| 项目 | 升级前 | 升级后 |
|------|--------|--------|
| Step 4 技能调度 | 仅architecture-review | architecture-review + technical-design-review |
| architecture-review | 关键词罗列式评审 | 第一性原理评审框架 |
| technical-design-review | 关键词匹配判断 | 质量指标评估机制 |
| project-analysis | 章节结构检查 | 第一性原理产出标准 |

---

## 通用原则

### Skill升级检查清单

当发现skill设计有问题时，按以下步骤检查：

1. [ ] **Skill调度是否完整？**
   - 检查dev-workflow-orchestration的Skill调度表
   - 确保相关skill都被显式引用

2. [ ] **设计是否符合第一性原理？**
   - 从本质出发，而非枚举表面检查项
   - 评审维度是否覆盖核心本质问题

3. [ ] **评分机制是否合理？**
   - 防止"凑关键词"行为
   - 评分真正反映质量

4. [ ] **是否与已有经验对齐？**
   - 如有相关memory经验，是否已对照检查
   - check_solution.py的改进是否同步到skill中

---

## 关联模式

- `memory/reflections/reflection-quality-gate-scoring-from-counting-to-quality.md`：评分机制从机械计数到质量指标的改进
- `memory/reflections/reflection-quality-gate-solution-review-dimension-expansion.md`：评审维度从3到6的扩展

---

## 延伸思考

本次升级源于对"技术方案是否在Step3、Step4被显式使用"和"是否按第一性原理设计"的追问，提醒我们：

1. **Skill也需要被评审**：工具和方法论本身也需要持续改进
2. **设计一致性很重要**：check_solution.py已升级，但skill未同步，导致不一致
3. **第一性原理是改进的钥匙**：从本质出发，而非修补表面
