---
id: pattern-quality-gate-checkpoint
title: 质量门禁检查点模式
type: pattern
description: 在 10 步质量闭环的每个阶段入口设置强制检查点，确保前置步骤完成且质量达标，才能启动下一阶段
tags: [quality-gate, checkpoint, phase-transition, entry-criteria, 10-step-closed-loop]
applicable_projects: [agentsystem, "*"]
host_scope: [cursor, vscode, generic]
source_change_ids: [add-default-product-template-health-compliance]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: draft
related:
  - memory/anti-patterns/anti-pattern-skip-phase-before-completion.md
  - memory/patterns/pattern-complete-quality-closed-loop.md
  - memory/preferences/preference-quality-gate-checklist.md
---

# 质量门禁检查点模式

## 一句话定义

在 10 步质量闭环的**每个阶段入口**设置强制检查点，像安检门一样：前置步骤未完成或质量不达标，**禁止进入**下一阶段。

## 背景与问题

10 步质量闭环定义了清晰的流程：

```
Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6 → Step 7 → Step 8 → Step 9 → Step 10
```

但实践中常出现：
- 跳过 Step 1（需求审核），直接 Step 2/3
- Step 4（归档）未完成，就开始 Step 5（复盘）
- 后面的任务已勾选，前面的任务还空着

**根因**：只有流程定义，没有**执行检查点**阻止违规流转。

## 解决方案：三层门禁机制

### 第一层：任务清单状态检查

**位置**：tasks.md 文件本身
**机制**：任何后置任务 [x] 勾选前，必须确认前置任务全部 [x]

```markdown
# 任务清单示例（正确状态）

- [x] **1. 需求与提案**      ← 全部完成
  - [x] 1.1 xxx
  - [x] 1.2 xxx

- [x] **2. 方案设计**        ← 全部完成
  - [x] 2.1 xxx
  - [x] 2.2 xxx

- [ ] **3. 编码实现**        ← 当前阶段，前置已完成
  - [ ] 3.1 xxx
  - [ ] 3.2 xxx
```

**错误状态识别**：
```markdown
# 任务清单示例（错误状态！）

- [ ] **1. 需求与提案**      ← 未完成！
  - [ ] 1.1 xxx

- [x] **2. 方案设计**        ← ❌ 前置未完成，不应勾选
  - [x] 2.1 xxx
```

**检查动作**：
- 主 Agent 在统筹时，定期扫描 tasks.md 检查状态一致性
- 发现"后置已勾选但前置未勾选"时，立即标记为异常，停止推进

### 第二层：阶段启动准入声明

**位置**：每次启动新阶段前，必须完成的显性声明

**声明格式**：

```markdown
**阶段 [N] 启动准入检查**

阶段名称：[如：编码实现 / 功能验收 / 复盘]

前置阶段检查：
- [ ] Step [N-1] 所有任务已标记 [x]？是/否
  - 如否，列出未完成任务：[任务编号列表]
- [ ] Step [N-1] 需要评审的，评审记录已产出？是/否
  - 评审记录路径：[xxx]
  - 评审结论：[通过 / 有条件通过 / 不通过]
- [ ] 评审结论为"通过"或"有条件通过（但无阻塞项）"？是/否

准入决策：
- [ ] 全部检查通过 → 准许进入 Step [N]
- [ ] 有未完成项 → 退回完成后再启动
- [ ] 特殊情况（需说明）：[简述]

**检查人**: [Agent 角色，通常是主 Agent]
**检查时间**: YYYY-MM-DD HH:mm:ss
```

### 第三层：完成性表述拦截

**位置**：声称"Step N 完成"前

**拦截机制**：

```markdown
**完成性表述前自检**

我即将声称：Step [N] - [阶段名称] 已完成

检查：
- [ ] 本阶段所有子任务已 [x]？是/否
- [ ] 本阶段产出物已存放于规范路径？是/否
- [ ] 本阶段需要审核的，审核已通过？是/否
- [ ] 下一阶段（Step [N+1]）可以合法启动？是/否

**确认**：以上全部通过，可以声称完成。

**声明人**: [Agent 角色]
**声明时间**: YYYY-MM-DD HH:mm:ss
```

**关键约束**：
- 未通过自检，禁止使用"已完成""已闭环""已交付"等表述
- 只能使用"进行中""待审核""待修复"等状态

## 10 步闭环各阶段的准入条件速查表

| 阶段 | 准入条件（启动前必须满足） | 产出物验证 |
|------|------------------------|-----------|
| **Step 1 需求分析** | 无（变更启动点） | PRD 文档存在于 docs/project-prd-changes/[change-id]/ |
| **Step 2 PRD 评审** | Step 1 完成 | PRD 文档已产出 |
| **Step 3 方案设计** | Step 2 评审通过 | 评审记录结论为"通过" |
| **Step 4 编码实现** | Step 3 评审通过 | 技术方案已产出并评审通过 |
| **Step 5 代码评审** | Step 4 完成 | 代码已实现并自测 |
| **Step 6 功能验收** | Step 4 完成 + Step 5 通过 | code review 记录结论为"通过" |
| **Step 7 归档** | Step 6 验收通过 | 验收记录结论为"通过" |
| **Step 8 复盘** | Step 7 归档完成 | openspec/changes/archive/ 存在，迭代日志已追加 |
| **Step 9 全局更新** | Step 8 复盘完成 | 复盘记录已产出，改进措施已规划 |

## 特殊情况处理

### 情况 A：并行执行

**场景**：Step 6 code review 和 Step 7 部分准备可以并行。

**处理**：
1. 在 proposal.md 中明确声明并行策略
2. tasks.md 中标注："Step 6/7 并行，理由：[简述]"
3. 并行任务必须各自独立审核通过
4. **禁止**：Step 6 未完成就声称 Step 7 完成

### 情况 B：简化流程

**场景**：极小热修，希望合并部分步骤。

**处理**：
1. 在 proposal.md 中声明简化方案
2. 合并不等于跳过，仍需最小把关：
   - PRD 自检（即使只有几行）
   - 主 Agent 快速审核
   - 产出物存放规范
3. tasks.md 标注合并理由

### 情况 C：发现前期缺陷需回溯

**场景**：Step 5 执行中发现 Step 2 PRD 有缺陷。

**处理**：
1. 停止当前阶段
2. 退回 Step 2 修复 PRD
3. 重新 PRD 评审（Step 2）
4. 评审通过后，重新进入后续阶段
5. 在迭代日志和复盘记录中说明回溯原因

## 工具支持（建议）

### 检查脚本（伪代码）

```python
def check_phase_entry(change_id, target_phase):
    """
    检查是否可以进入 target_phase 阶段
    """
    # 读取 tasks.md
    tasks = parse_tasks_md(f"openspec/changes/{change_id}/tasks.md")
    
    # 获取 target_phase 的所有前置阶段
    prereq_phases = get_prerequisites(target_phase)
    
    for phase in prereq_phases:
        # 检查该阶段所有任务是否已完成
        incomplete_tasks = [t for t in tasks[phase] if not t.completed]
        if incomplete_tasks:
            return False, f"前置阶段 {phase} 有未完成任务: {incomplete_tasks}"
        
        # 检查该阶段是否需要评审
        if requires_review(phase):
            review_file = find_review_record(change_id, phase)
            if not review_file:
                return False, f"前置阶段 {phase} 缺少评审记录"
            if get_review_conclusion(review_file) not in ["通过", "有条件通过"]:
                return False, f"前置阶段 {phase} 评审未通过"
    
    return True, "准入检查通过"
```

### IDE 插件建议

- tasks.md 中前置未勾选但后置已勾选时，高亮显示警告
- 声称"完成"前，弹出准入检查确认框

## 检查清单

- [ ] 启动任何阶段前，完成了阶段启动准入声明
- [ ] 完成性表述前，完成了完成性表述自检
- [ ] tasks.md 中没有"后置已勾选但前置未勾选"的矛盾
- [ ] 评审类任务都有明确的评审记录文件
- [ ] 复盘启动前，归档已完全完成（openspec archive 已执行）

## 关联模式

- `anti-pattern-skip-phase-before-completion.md` - 本模式要防止的反模式
- `pattern-complete-quality-closed-loop.md` - 10 步闭环的完整流程定义
- `preference-quality-gate-checklist.md` - 各阶段质量门禁的详细清单

---

**沉淀来源**: `add-default-product-template-health-compliance` 归档回顾  
**创建日期**: 2026-03-17