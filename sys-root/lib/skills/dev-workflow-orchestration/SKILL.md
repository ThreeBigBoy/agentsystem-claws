---
name: dev-workflow-orchestration
description: 流程编排与自主推进技能；当用户提出涉及 change-id 的任务时，判断当前所处阶段、规划自主推进路径、在停止线（Gate-PRD/Gate-DESIGN/归档前确认）前停下并提示用户。本技能不替代各具体 Skill（request-analysis、prd-review 等），而是调度它们按正确顺序执行。
---

# 流程编排与自主推进技能

## 触发场景

- 用户提出涉及 change-id 的任务（新建、迭代、评审、实现、验收、归档意图之一）。
- 需要判断当前所处阶段、规划推进路径、在停止线前停下。
- Agent 需要知道"下一步该做什么"而非"停下来等命令"。

## 核心职责

本技能**不执行**具体的需求分析、评审、编码等工作（由对应 Skill 完成），而是负责：

1. **阶段判断**：给定 change-id 和当前状态，判断所处阶段
2. **准入判断**：检查进入下一阶段是否满足准入条件
3. **推进编排**：规划同一上下文内可连续执行的多步
4. **停止线判断**：识别 Gate-PRD、Gate-DESIGN、归档前确认等必须人工介入的节点
5. **Skill/Memory 调度**：确保进入每步前加载正确的 Skill 和 Memory
6. **质量门禁执行**：确保每个阶段出口都经过严格检查

---

## 一、Memory 上下文加载（强制）

执行流程编排前，**必须**加载以下 Memory：

| Memory | 路径 | 用途 |
|--------|------|------|
| `pattern-complete-quality-closed-loop` | `sys-root/lib/memory/patterns/pattern-complete-quality-closed-loop.md` | 10步闭环整体框架、各阶段详细定义 |
| `pattern-quality-gate-checkpoint` | `sys-root/lib/memory/patterns/pattern-quality-gate-checkpoint.md` | 三层门禁机制、准入准出标准 |
| `pattern-review-fix-loop` | `sys-root/lib/memory/patterns/pattern-review-fix-loop.md` | 评审修复循环机制 |
| `preference-quality-gate-checklist` | `sys-root/lib/memory/preferences/preference-quality-gate-checklist.md` | 各阶段质量门禁详细检查清单 |

---

## 二、10 步质量门禁速查表

### 阶段准入准出一览

| 阶段 | 准入条件 | 准出检查项 | 关键判定规则 |
|------|---------|-----------|-------------|
| **Step 1 需求分析** | 无（启动点） | PRD产出、OpenSpec目录、proposal、tasks、specs、迭代日志 | 自检通过后进入Step 2 |
| **Step 2 PRD评审** | Step 1完成 | 评审执行、纪要产出、自检9项、**判定为「通过」**、修复循环 | **只有「通过」才能进Step 3**，「有条件通过」必须修复→再评审 |
| **Step 3 技术方案** | PRD评审「通过」+Gate-PRD确认 | design.md产出、结构完整、与PRD对应 | 完整后进入Step 4 |
| **Step 4 方案评审** | Step 3完成 | 评审执行、纪要、自检、**判定为「通过」**、修复循环 | **只有「通过」才能进Step 5** |
| **Step 5 编码实现** | 方案评审「通过」+Gate-DESIGN确认 | 规范遵循、自检完成、可测试性、tasks更新 | 自检通过后进入Step 6 |
| **Step 6 代码评审** | Step 5完成 | 评审执行、纪要、问题分级、**判定为「通过」**、修复循环 | **只有「通过」才能进Step 7** |
| **Step 7 功能验收** | Step 6通过 | validate两轮、测试执行、记录、**判定为「通过」** | **只有「通过」才能进Step 8** |
| **Step 8 归档** | Step 7通过 | 术语检查、tasks更新、specs合并、archive移动 | 全部通过后进入Step 9 |
| **Step 9 复盘** | Step 8完成 | 复盘执行、报告产出、memory沉淀 | 触发条件满足时执行 |
| **Step 10 全局联动** | Step 9完成 | 影响分析20项检查 | **全部20项通过才能闭环完成** |

### 评审类阶段判定规则（关键）

| 评审结论 | 是否可以进入下一阶段 | 后续动作 |
|---------|-------------------|---------|
| **✓ 通过** | ✅ 可以 | 进入下一阶段 |
| **△ 有条件通过** | ❌ 不可以 | 必须修复 → 重新评审 → 转为「通过」 |
| **✗ 不通过** | ❌ 不可以 | 必须修复 → 重新评审 → 转为「通过」 |

---

## 三、三层门禁机制

### 第一层：tasks.md 状态一致性检查

**机制**：任何后置任务 `[x]` 勾选前，必须确认前置任务全部 `[x]`

**错误状态识别**：
```markdown
# 错误状态！
- [ ] **1. 需求与提案**      ← 未完成！
  - [ ] 1.1 xxx

- [x] **2. 方案设计**        ← ❌ 前置未完成，不应勾选
  - [x] 2.1 xxx
```

### 第二层：阶段启动准入声明

**格式**：
```markdown
**阶段 [N] 启动准入检查**

阶段名称：[如：编码实现 / 功能验收 / 复盘]

前置阶段检查：
- [ ] Step [N-1] 所有任务已标记 [x]？是/否
- [ ] Step [N-1] 需要评审的，评审记录已产出？是/否
- [ ] 评审结论为"通过"？是/否

准入决策：
- [ ] 全部检查通过 → 准许进入 Step [N]
- [ ] 有未完成项 → 退回完成后再启动
```

### 第三层：完成性表述前自检

**机制**：声称"Step N 完成"前，必须完成自检

```markdown
**完成性表述前自检**

我即将声称：Step [N] - [阶段名称] 已完成

检查：
- [ ] 本阶段所有子任务已 [x]？是/否
- [ ] 本阶段产出物已存放于规范路径？是/否
- [ ] 本阶段需要审核的，审核已通过？是/否
- [ ] 下一阶段（Step [N+1]）可以合法启动？是/否

**确认**：以上全部通过，可以声称完成。
```

**关键约束**：
- 未通过自检，禁止使用"已完成""已闭环""已交付"等表述
- 只能使用"进行中""待审核""待修复"等状态

---

## 四、评审修复循环（Review-Fix-Loop）

### 流程图

```
评审 ────────────────────────────────────→ 通过
  │
  ├─→ 有条件通过 ──→ 识别问题清单 ──→ 修复 ──→ 重新评审
  │                                       ↑
  │                                       │
  └─→ 不通过 ──→ 必须修复 ──→ 重新评审 ────┘
```

### 关键规则

1. **只有「100% 通过」才是真正的通过**
2. **「有条件通过」≠ 可进入下一阶段**
3. 必须修复→再评审→转为「通过」后才能推进
4. 重新评审通过后，评审结论更新为「通过」

---

## 五、停止线判断

到达以下节点时，**必须停下并提示用户**：

| 停止线 | 条件 | 提示内容 |
|-------|------|---------|
| **Gate-PRD** | PRD 评审结论为「通过」 | 「PRD 已通过评审，请确认是否签署 PRD 终稿」 |
| **Gate-DESIGN** | 技术方案评审结论为「通过」 | 「技术方案已通过评审，请确认是否签署技术方案终稿」 |
| **Gate-归档** | 全局联动已完成 | 「本 change-id 已完成所有工作，请确认是否执行归档」 |
| **用户声明暂停** | 用户主动要求暂停 | 停止推进，等待用户指令 |
| **环境缺失** | 无法调用必要工具且无法降级 | 「因环境限制无法继续，详见下方错误」 |

**注意**：PRD-R / PRD-F（或 DESIGN-R / DESIGN-F）未收敛为「评审通过」前，Agent 应继续修评闭环，**不应**停在 Gate 前却不交评审纪要。

---

## 六、Skill/Memory 调度

进入每步前，确保加载正确的 Skill：

| 阶段 | 必须加载的 Skill |
|------|-----------------|
| Step 1 | `request-analysis` |
| Step 2 | `prd-review` |
| Step 3 | `project-analysis` |
| Step 4 | `architecture-review` + `technical-design-review`（双技能协同） |
| Step 5 | `coding-implement` |
| Step 6 | `code-review` |
| Step 7 | `func-test` |
| Step 8 | `retrospective-analysis` |
| Step 9 | 无独立 Skill，按 Memory 执行 |
| Step 10 | OpenSpec CLI 归档命令 |

---

## 七、决策树

```
当前阶段 = Step N
│
├─ 加载 Memory 上下文
│   └─ pattern-complete-quality-closed-loop
│   └─ pattern-quality-gate-checkpoint
│   └─ pattern-review-fix-loop（如涉及评审）
│   └─ preference-quality-gate-checklist
│
├─ 准入条件是否满足？
│   ├─ 否 → 停留在当前阶段，执行当前阶段 Skill
│   └─ 是 → 继续判断
│
├─ 是否到达停止线？
│   ├─ 是 → 停下，提示用户人工确认
│   └─ 否 → 继续判断
│
├─ 评审类阶段？
│   ├─ 是 → 检查评审结论
│   │   ├─ 「通过」→ 可推进下一阶段
│   │   ├─ 「有条件通过」→ 执行修复循环
│   │   └─ 「不通过」→ 执行修复循环
│   └─ 否 → 继续判断
│
├─ 是否有下一阶段 Skill？
│   ├─ 是 → 加载下一阶段 Skill，推进至下一阶段
│   └─ 否（如 Step 10）→ 执行归档
│
└─ 是否同一上下文内可继续推进多步？
    ├─ 是 → 继续推进
    └─ 否 → 停下，等待下一轮用户指令
```

---

## 八、质量门禁执行方式

### 调用链路（简化版）

```
Agent (dev-workflow-orchestration)
    │
    ├─→ 加载 Memory 上下文
    ├─→ 判断当前所处阶段
    ├─→ 确认准入条件满足
    │
    ▼
Agent 直接调用 Python 脚本:
    python check_<gate>.py <参数> --config <config.yaml> --json
```

### Gate 与 Step 对应关系

| Step | 阶段 | 应调用的脚本 | 说明 |
|------|------|-------------|------|
| 2 | PRD评审 | `check_prd.py` | PRD 质量门禁 |
| 4 | 方案评审 | `check_solution.py` | 方案质量门禁 |
| 6 | 代码评审 | `check_code.py` | 代码质量门禁 |
| 8 | 归档 | `check_delivery.py` | 交付质量门禁 |

### 脚本路径

所有门禁脚本位于 Skill 的 references 目录下：
```
sys-root/lib/skills/dev-workflow-orchestration/references/quality-gates/
├── config.yaml           # 门禁配置
├── check_prd.py         # PRD 质量门禁
├── check_solution.py     # 方案质量门禁
├── check_code.py        # 代码质量门禁
├── check_delivery.py    # 交付质量门禁
├── run_gates.py         # 统一入口
├── model_selector.py    # 模型选择器
├── llm_enhancer.py     # LLM 增强
└── prompts/            # LLM Prompt 模板
```

### Agent 调用约定

1. **调用前**：确认当前阶段已完成，准入条件满足
2. **调用时**：使用 `subprocess.run()` 直接执行 Python 脚本
3. **调用后**：解析返回的 JSON 结果，判断门禁是否通过
4. **不通过时**：按照评审修复循环执行修复后再调用

### 自动发现逻辑

脚本会自动：
1. 从当前工作目录向上查找 `openspec/changes/<change-id>`
2. 根据 change-id 构建正确的文件路径
3. 读取 config.yaml 获取模型路由配置

### gate_status 查询

使用 `run_gates.py status` 或直接分析 tasks.md 判断当前阶段

---

## 九、质量门禁执行声明

执行本技能后，应输出以下声明：

```markdown
## 质量门禁执行声明

**变更 ID**: [change-id]
**当前阶段**: [Step N: 阶段名称]
**执行日期**: YYYY-MM-DD
**执行人**: [Agent 角色]

### 准入条件检查
- [ ] 前置阶段质量门禁已通过
- [ ] 已读取本阶段 skill/规范文档

### 本阶段质量门禁检查
[复制对应阶段的检查项，逐项勾选]

| # | 检查项 | 状态 |
|---|-------|------|
| N.1 | [检查项名称] | ⬜ 通过 / ⬜ 不通过 |
| ... | ... | ... |

### 准出判定
⬜ **通过**：全部检查项通过，可以进入下一阶段
⬜ **不通过**：存在未通过项，修复后重新执行

### 执行声明
我确认：
1. 已逐项执行本阶段质量门禁检查清单
2. 所有通过项均已验证
3. 如存在不通过项，已记录并计划修复

**签名**: [Agent 角色]
**日期**: YYYY-MM-DD
```

---

## 十、与 Memory 的关系

| Memory | 本 Skill 中的用途 |
|--------|------------------|
| `pattern-complete-quality-closed-loop` | 定义 10 步框架、各阶段详细定义 |
| `pattern-quality-gate-checkpoint` | 三层门禁机制、tasks 状态检查 |
| `pattern-review-fix-loop` | 评审修复循环判定逻辑 |
| `preference-quality-gate-checklist` | 各阶段详细检查清单（Step 1-10） |

---

## 十一、注意事项

1. **本 Skill 不替代具体 Skill**：流程编排是"何时做"，具体工作是"做什么"
2. **停止线必须停下**：不能以"自主推进"为由跳过人工确认
3. **有条件通过必须修复**：不能停在 Gate 前却不交评审纪要
4. **每次切换 Step 必须加载 Skill**：同一回合内从 Step A 切换到 Step B 时，必须先加载对应 Skill
5. **通用检查项**：所有阶段执行前须检查 Skill 版本、术语定义、本阶段门禁清单
6. **迭代日志必须记录**：每个阶段完成后须在 `docs/项目事件日志.md` 中留痕
