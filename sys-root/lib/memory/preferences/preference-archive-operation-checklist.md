---
id: preference-archive-operation-checklist
title: OpenSpec 归档操作检查清单
type: preference
description: 执行 OpenSpec 归档操作时的强制检查清单，确保归档操作完整、规范、可验证
description_long: |
  偏好：OpenSpec 归档操作检查清单
  
  归档是 8+1 质量闭环的最后一步，也是最容易遗漏步骤的环节。
  本清单强制要求在执行归档操作时逐项检查，确保：
  1. 文档状态已更新
  2. 规范已合并
  3. 目录已移动
  4. 归档可验证
  
  使用本清单可防止术语定义漂移和惯性思维陷阱。
applicable_projects:
  - agentsystem
  - "*"
tags:
  - 偏好
  - 检查清单
  - 归档操作
  - OpenSpec
related:
  - anti-pattern-terminology-drift
  - anti-pattern-inertia-trap
  - OpenSpec.md
  - pattern-complete-quality-closed-loop
created_by: 复盘-OpenSpec归档执行缺陷-2026-03-16
created_date: 2026-03-16
version: 1.0
---

# 偏好：OpenSpec 归档操作检查清单

## 使用说明

**执行时机**: 任何 OpenSpec 变更的 Step 8 归档阶段
**执行方式**: 逐项检查，全部通过后方可认为归档完成
**强制要求**: 不得跳过任何检查项

---

## 归档前准备

### 步骤 1: 查阅归档规范定义

**必须查阅**:
- [ ] 阅读 OpenSpec.md "阶段 3: 归档变更" 章节
- [ ] 确认归档操作包含：合并 specs/ + 移动 changes/
- [ ] 理解归档与"标记完成"的区别

**查阅记录**:
```
已查阅 OpenSpec.md [章节]：归档定义已明确
归档操作 = 合并规范增量到 specs/ + 移动 changes/[id]/ 到 changes/archive/
```

---

## 归档操作检查清单

### 阶段 A: 文档状态更新

| # | 检查项 | 检查内容 | 状态 |
|---|--------|---------|------|
| A1 | tasks.md 任务标记 | 所有任务已标记为 `[x]` 或 `[~]` | ⬜ |
| A2 | design.md 归档状态 | 已添加"变更完成摘要"章节，包含完成状态、质量闭环记录、产出物清单 | ⬜ |
| A3 | 迭代日志更新 | 已追加归档完成记录 | ⬜ |

**阶段 A 验收标准**: A1-A3 全部通过 ✅

---

### 阶段 B: 规范合并（OpenSpec 归档核心）

| # | 检查项 | 检查内容 | 状态 |
|---|--------|---------|------|
| B1 | 确认 specs/ 增量 | `changes/[id]/specs/[capability]/spec.md` 存在 | ⬜ |
| B2 | 阅读增量内容 | 已阅读并理解 ADDED/MODIFIED/REMOVED 内容 | ⬜ |
| B3 | 合并到 specs/ | 已将增量内容合并到 `specs/[capability]/spec.md` | ⬜ |
| B4 | 验证合并结果 | `specs/[capability]/spec.md` 已包含新规范 | ⬜ |

**阶段 B 验收标准**: B1-B4 全部通过 ✅

**关键说明**:
- B3 是归档的**核心操作**，不可省略
- 合并时需保留历史归档信息（如"归档自变更 xxx"）

---

### 阶段 C: 目录移动（OpenSpec 归档核心）

| # | 检查项 | 检查内容 | 状态 |
|---|--------|---------|------|
| C1 | 确认源目录 | `changes/[id]/` 存在且包含完整变更文件 | ⬜ |
| C2 | 创建目标目录 | `changes/archive/[id]-YYYY-MM-DD/` 已创建 | ⬜ |
| C3 | 移动目录 | 已将 `changes/[id]/` 移动到 `changes/archive/[id]-YYYY-MM-DD/` | ⬜ |
| C4 | 验证移动结果 | `changes/` 目录下已无 `[id]`，`changes/archive/` 下存在 `[id]-YYYY-MM-DD` | ⬜ |

**阶段 C 验收标准**: C1-C4 全部通过 ✅

**关键说明**:
- C3 是归档的**核心操作**，不可省略
- 移动后保留完整变更历史（proposal.md、tasks.md、design.md 等）

---

### 阶段 D: 归档验证

| # | 检查项 | 检查内容 | 状态 |
|---|--------|---------|------|
| D1 | specs/ 验证 | `specs/[capability]/spec.md` 已更新且格式正确 | ⬜ |
| D2 | changes/ 清理验证 | `changes/[id]/` 已不存在，`changes/archive/[id]-YYYY-MM-DD/` 存在 | ⬜ |
| D3 | 可追溯性验证 | 可以从 specs/ 追溯到 archive/ 的完整变更历史 | ⬜ |

**阶段 D 验收标准**: D1-D3 全部通过 ✅

---

## 归档完成确认

### 最终检查

```
所有阶段验收状态：
- 阶段 A（文档状态更新）: ⬜ 通过 / ⬜ 未通过
- 阶段 B（规范合并）: ⬜ 通过 / ⬜ 未通过
- 阶段 C（目录移动）: ⬜ 通过 / ⬜ 未通过
- 阶段 D（归档验证）: ⬜ 通过 / ⬜ 未通过

归档完成判定：
⬜ 全部阶段通过 → 归档真正完成
⬜ 任一阶段未通过 → 继续执行遗漏步骤
```

### 归档声明

```markdown
**OpenSpec 归档完成声明**

变更 ID: [change-id]
归档日期: YYYY-MM-DD
归档操作:
1. ✅ 已合并 specs/ 规范增量
2. ✅ 已移动 changes/[id]/ 到 changes/archive/[id]-YYYY-MM-DD/
3. ✅ 已通过全部 4 阶段验收检查

归档状态: ✅ 真正完成（符合 OpenSpec 规范）
```

---

## 常见错误与避免

| 错误 | 原因 | 避免方法 |
|-----|------|---------|
| 只标记 tasks.md，未合并 specs/ | 术语定义漂移 | 使用本清单，强制检查阶段 B |
| 只更新 design.md，未移动 changes/ | 术语定义漂移 | 使用本清单，强制检查阶段 C |
| 遗漏规范合并 | 惯性思维 | 查阅 OpenSpec.md，理解归档定义 |
| 目录移动后未验证 | 检查缺失 | 使用阶段 D 验证清单 |

---

## 与 8+1 质量闭环的关系

本清单是 **Step 8: 归档** 的具体执行指南：

```
Step 8: 归档
    ↓
查阅 preference-archive-operation-checklist
    ↓
执行 4 阶段检查清单
    ↓
完成归档，产出归档声明
    ↓
进入 Step 9: 复盘（如需）
```

---

**偏好版本**: v1.0  
**创建日期**: 2026-03-16  
**创建来源**: 复盘-OpenSpec归档执行缺陷  
**适用范围**: 所有 OpenSpec 变更的归档操作
