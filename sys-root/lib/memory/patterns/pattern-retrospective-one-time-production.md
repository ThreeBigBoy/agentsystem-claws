---
id: pattern-retrospective-one-time-production
title: 复盘一次性产出模式
type: pattern
description: 复盘文档一次性产出到正确位置（docs/retrospective/），不需要先写草稿再迁移
tags: [retrospective, documentation, best-practice, one-time-production]
applicable_projects: [agentsystem, "*"]
host_scope: [cursor, vscode, generic]
source_change_ids: [add-default-product-template-health-compliance]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: stable
related:
  - memory/anti-patterns/anti-pattern-retrospective-vs-execution-deviation-terminology-confusion.md
  - skills/retrospective-analysis/REFERENCE/目录结构规范-v3-基于完整质量闭环.md
  - memory/preferences/preference-terminology-glossary.md
---

# 复盘一次性产出模式

## 一句话定义

复盘文档**一次性产出到正确位置**（`docs/retrospective/[level]/`），不需要先写"草稿"再迁移，也不需要先放在 runtime-logs 再转移。

## 问题背景

在执行归档后，有时会试图：
- "先在 runtime-logs 写个反思草稿，后面再整理成复盘"
- "等走完一个 change-id 再把文档迁移到 retrospectives/"
- "先随便记一记，后面再补正式的复盘"

这些都是**错误的做法**。

## 正确做法

### Step 1：确认产出时机

复盘只在**变更归档后**产出，不是在执行过程中边做边写。

### Step 2：直接使用 retrospective-analysis skill

- 调用 `skills/retrospective-analysis/SKILL.md`
- 输入：已归档的 change-id 或项目阶段信息
- 输出：直接写到 `docs/retrospective/[level]/复盘-[主题]-[日期].md`

### Step 3：一次性完成全部结构

复盘文档必须包含：
1. **目标回顾**：当初设定的目标是什么？达成了吗？
2. **过程回顾**：关键节点、决策、执行路径
3. **根因分析**：成功/失败的根本原因（用 5 Whys 或鱼骨图）
4. **改进措施**：具体的、可执行的改进项
5. **模式沉淀**：可复用的经验 → 转化为 memory entry

**不需要**：
- 草稿阶段
- 临时存放位置
- 多次迁移

## 与执行偏差记录的关系

| 维度 | 执行偏差记录 (Execution Deviation) | 复盘 (Retrospective) |
|------|----------------------------------|---------------------|
| 产出时机 | 执行中发现问题时 | 变更归档后 |
| 存放位置 | `runtime-logs/execution-deviations/` | `docs/retrospective/` |
| 文档结构 | 自由格式 | 必须含 5 大结构 |
| 是否需要草稿 | 不需要，即时记录 | 不需要，一次性产出 |
| 是否需要迁移 | 不需要 | 不需要 |

**重要**：runtime-logs/execution-deviations/ 里的**永远不要**称为"复盘"，也不要试图把它们"升级"为复盘。如果执行偏差记录很有价值，复盘时可以**引用**它们作为素材，但复盘本身是独立的、系统性产出的新文档。

## 反例

❌ "先在 runtime-logs 写个复盘草稿，后面再整理到 framework/"
❌ "等这个 change-id 走完，再把复盘文档迁移到正确位置"
❌ "执行偏差记录和复盘差不多，放哪儿都行"

## 检查清单

- [ ] 确认变更已归档（openspec archive 完成）
- [ ] 直接使用 retrospective-analysis skill
- [ ] 产出路径是 `docs/retrospective/[level]/`，不是 runtime-logs/
- [ ] 文档包含完整的 5 大结构（目标→过程→根因→改进→沉淀）
- [ ] 文档标题以"复盘-"开头，不是"反思-"或"事件-"

## 关联文档

- `anti-pattern-retrospective-vs-execution-deviation-terminology-confusion.md` - 术语混淆的反模式
- `目录结构规范-v3-基于完整质量闭环.md` - 复盘 3 级分离的详细规范
- `preference-terminology-glossary.md` - 术语精确定义（含 Execution Deviation）