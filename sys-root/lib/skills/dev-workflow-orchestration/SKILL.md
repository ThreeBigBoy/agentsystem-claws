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

## 六、Skill/Memory 调度（强制执行顺序）

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

### 评审类阶段强制执行顺序

**⚠️ 关键约束：评审类阶段必须严格遵循「Skill评审 → 量化评分 → 综合判定」的执行顺序**

**各阶段完整执行步骤**：
- Step 2（PRD评审）：prd-review Skill → check_prd.py → 综合判定 → Gate-PRD确认
- Step 4（方案评审）：architecture-review + technical-design-review Skill（双 Skill） → check_solution.py → 综合判定 → Gate-DESIGN确认
- Step 6（代码评审）：code-review Skill → check_code.py → 综合判定 → Gate-代码确认

#### Step 2 PRD评审 - 强制执行顺序

```
1. 【强制】调用 prd-review Skill
   ├─ 产出：评审纪要文件（records/PRD-[change-id]-评审纪要.md）
   ├─ 判定：✓通过 / △有条件通过 / ✗不通过
   └─ 阻塞项识别：标记阻塞性问题

2. 【强制】调用 check_prd.py
   ├─ 产出：量化评分 {score: XX}
   ├─ 说明：包含第一层判断（是否使用LLM），第二层判断由 llm_enhancer.py 实现
   └─ 评分结果影响综合判定

3. 【强制校验】综合判定结论
   ├─ ✓通过 → 可以进入Step 3
   ├─ △有条件通过 → 必须修复 → 重新调用prd-review → 转为✓通过
   └─ ✗不通过 → 必须修复 → 重新调用prd-review → 转为✓通过
```

#### Step 4 方案评审 - 强制执行顺序

```
1. 【强制】调用 architecture-review Skill
   ├─ 产出：architecture-review评审纪要
   ├─ 判定：✓通过 / △有条件通过 / ✗不通过
   └─ 重点：产出物规范性、与PRD一致性

2. 【强制】调用 technical-design-review Skill
   ├─ 产出：technical-design-review评审纪要
   ├─ 判定：✓通过 / △有条件通过 / ✗不通过
   └─ 重点：系统实现质量（10维度生产就绪）

3. 【强制】调用 check_solution.py
   ├─ 产出：量化评分 {score: XX}
   ├─ 说明：包含第一层判断（是否使用LLM），第二层判断由 llm_enhancer.py 实现
   └─ 评分结果影响综合判定

4. 【强制校验】双Skill判定结论必须都为✓通过
   ├─ architecture-review ✓通过 + technical-design-review ✓通过 → 可以进入Step 5
   ├─ 任一为△有条件通过 → 必须修复 → 重新评审
   └─ 任一为✗不通过 → 必须修复 → 重新评审
```

#### Step 6 代码评审 - 强制执行顺序

```
1. 【强制】调用 code-review Skill
   ├─ 产出：code-review评审纪要
   ├─ 判定：✓通过 / △有条件通过 / ✗不通过
   └─ 重点：代码质量、规范遵循、测试覆盖

2. 【强制】调用 check_code.py
   ├─ 产出：量化评分 {score: XX}
   ├─ 说明：包含第一层判断（是否使用LLM），第二层判断由 llm_enhancer.py 实现
   └─ 评分结果影响综合判定

3. 【强制校验】综合判定结论
   ├─ ✓通过 → 可以进入Step 7
   ├─ △有条件通过 → 必须修复 → 重新调用code-review → 转为✓通过
   └─ ✗不通过 → 必须修复 → 重新调用code-review → 转为✓通过
```

---

### Test-Fix-Loop（编码阶段测试修复循环）

**⚠️ 重要补充：编码实现阶段必须包含测试验证**

```
Step 5: 编码实现
    │
    ├─ 编写代码
    ├─ 编写/更新测试
    │
    ▼
Test-Fix-Loop（测试修复循环）
    │
    ├─ 执行测试：pytest / npm test / 其他测试命令
    │   │
    │   ├─ 测试通过 → 继续下一步
    │   │
    │   └─ 测试失败 → 调用 bug-diagnosis Skill
    │                   │
    │                   ├─ 问题定位（调用链路、日志分析）
    │                   ├─ 根因分析（5 Why、模式识别）
    │                   ├─ 修复策略（最小改动、设计原则）
    │                   └─ 验证修复（重新运行测试）
    │
    └─ 测试通过后 → 进入 Step 6 代码评审
```

**触发条件**：测试失败时必须调用 `bug-diagnosis` Skill

**Skill 调用路径**：`sys-root/lib/skills/bug-diagnosis/SKILL.md`

**与 Review-Fix-Loop 的区别**：

| 环节 | 触发时机 | 目的 |
|------|---------|------|
| Test-Fix-Loop | 测试失败 | 修复代码中的 bug |
| Review-Fix-Loop | 评审不通过 | 修复评审发现的问题（通常是设计/方案问题）|

---

## 七、决策树（已更新强制执行顺序）

```
当前阶段 = Step N
│
├─ 加载 Memory 上下文
│   └─ pattern-complete-quality-closed-loop
│   └─ pattern-quality-gate-checkpoint
│   └─ pattern-review-fix-loop（如涉及评审）
│   └─ preference-quality-gate-checklist
│
├─ 评审类阶段（Step 2/4/6）？
│   ├─ 是 → 【强制】先调用Skill执行评审
│   │   ├─ Step 2: 必须先调用 prd-review
│   │   ├─ Step 4: 必须先调用 architecture-review + technical-design-review
│   │   └─ Step 6: 必须先调用 code-review
│   │
│   │   【校验】检查评审纪要是否存在
│   │   ├─ 评审纪要不存在 → ❌ 违规！必须重新执行Skill评审
│   │   └─ 评审纪要存在 → 继续
│   │
│   │   【判定】根据Skill评审结论
│   │   ├─ 「✓通过」→ 可推进下一阶段
│   │   ├─ 「△有条件通过」→ 执行修复循环
│   │   └─ 「✗不通过」→ 执行修复循环
│   │
│   │   【强制】调用Python脚本获取量化评分
│   │   └─ 两者都强制执行
│   │
│   └─ 否 → 继续判断
│
├─ 准入条件是否满足？
│   ├─ 否 → 停留在当前阶段，执行当前阶段 Skill
│   └─ 是 → 继续判断
│
├─ 是否到达停止线（Gate）？
│   ├─ 是 → 停下，提示用户人工确认
│   └─ 否 → 继续判断
│
├─ 是否有下一阶段 Skill？
│   ├─ 是 → 加载下一阶段 Skill，推进至下一阶段
│   └─ 否（如 Step 10）→ 执行归档
│
└─ 是否同一上下文内可继续推进多步？
    ├─ 是 → 继续推进
    └─ 否 → 停下，等待下一轮用户指令

【强制执行顺序校验点】
├─ Step 2: 必须有 prd-review 评审纪要
├─ Step 4: 必须有 architecture-review + technical-design-review 评审纪要
└─ Step 6: 必须有 code-review 评审纪要
```

---

### 综合判定保障

**【强制】综合判定必须执行**：
- 执行时机：check_*.py 量化评分完成后
- 执行者：Agent（不得跳过）
- 产出物：综合判定章节，追加到 Skill 评审纪要末尾

**【强制】综合判定内容**：
- Skill 评审结论（✓通过 / △有条件通过 / ✗不通过）
- 量化评分（XX/100，阈值：YY）
- 综合判定结论（✓通过 / △需修复 / ✗需修复）
- 判定理由
- 后续行动

**综合判定规则**：

| Skill 评审 | 量化评分 | 综合判定 | 行动 |
|------------|---------|---------|------|
| ✓通过 | ≥ 阈值 | **✓通过** | 可进入下一阶段 |
| ✓通过 | < 阈值 | **△需修复** | 修复内容 → 重新量化评分 |
| △有条件通过 | 任意 | **△需修复** | 修复问题 → 重新 Skill 评审 |
| ✗不通过 | 任意 | **✗需修复** | 修复问题 → 重新 Skill 评审 |

**综合判定产出模板**：

```markdown
## 综合判定

**判定日期**：YYYY-MM-DD
**判定人**：Agent

| 项目 | 值 |
|------|-----|
| Skill 评审结论 | ✓通过 / △有条件通过 / ✗不通过 |
| 量化评分 | XX/100 (阈值: YY) |
| **综合判定** | **✓通过 / △需修复 / ✗需修复** |

**判定理由**：
[Agent 根据 Skill 评审结论和量化评分，给出判定理由]

**后续行动**：
- 如果 ✓通过：可进入下一阶段，等待 Gate 确认
- 如果 △需修复：列出需要修复的问题
- 如果 ✗需修复：列出必须修复的问题
```

**跳过后果**：
- 未执行综合判定，不得进入下一阶段
- 未产出综合判定章节，Gate 确认无效

**注意**：综合判定 ≠ Gate 确认
- 综合判定是技术判定（Agent 执行）
- Gate 确认是人工确认（用户执行）
- 两者缺一不可，顺序不能颠倒

---

## 八、质量门禁执行方式

### 调用链路（完整版）

```
Agent (dev-workflow-orchestration)
    │
    ├─→ 加载 Memory 上下文
    ├─→ 判断当前所处阶段
    ├─→ 确认准入条件满足
    │
    ▼
【第一步：必须】Agent评审（调用对应Skill）
    ├─ Step 2: prd-review Skill → 产出评审纪要
    ├─ Step 4: architecture-review + technical-design-review Skill → 产出评审纪要
    └─ Step 6: code-review Skill → 产出评审纪要
    │
    ▼
【第二步：必须】量化评分（调用Python脚本）
    ├─ check_prd.py（强制）
    ├─ check_solution.py（强制）
    └─ check_code.py（强制）
    │
    ▼
【第三步：强制校验】综合判定结论
    ├─ Skill评审结论为✓通过 + 量化评分达标 → 进入下一阶段
    └─ Skill评审结论为△/✗ → 执行修复循环
```

### ⚠️ 重要澄清

| 误区 | 正确认知 |
|------|---------|
| 「调用check_xxx.py就是执行评审」 | ❌ check_xxx.py只是量化评分，不能替代Skill评审 |
| 「只要Skill评审通过就行」 | ❌ 两者都必须执行，缺一不可 |
| 「只要分数够了就算通过」 | ❌ 综合判定需要Skill评审结论+量化评分两者结合 |
| 「跳过Skill评审直接用脚本」 | ❌ 这是严重违规，跳过了深度语义评审 |

### Gate 与 Step 对应关系

| Step | 阶段 | 应调用的Skill | Python脚本（强制） |
|------|------|--------------|-------------------|
| 2 | PRD评审 | `prd-review` | `check_prd.py` |
| 4 | 方案评审 | `architecture-review` + `technical-design-review` | `check_solution.py` |
| 6 | 代码评审 | `code-review` | `check_code.py` |
| 8 | 归档 | 无独立Skill | `check_delivery.py` |

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

### ⚠️ 强制执行顺序约束（关键）

**评审类阶段（Step 2/4/6）必须严格遵循「先Skill评审后量化检查」的执行顺序，两者都是强制的**：

| 步骤 | 内容 | 作用 |
|------|------|------|
| **第一步** | 调用 Skill 执行 Agent 语义评审 | 深度判定（阻塞项、修改建议） |
| **第二步** | 调用 check_xxx.py 量化评分 | 快速评分（量化指标） |

**正确的执行顺序**：
```
Step 2: prd-review Skill → check_prd.py（两者都强制）
Step 4: architecture-review + technical-design-review Skill → check_solution.py（两者都强制）
Step 6: code-review Skill → check_code.py（两者都强制）
```

**校验点**：两步都执行完毕后，才能综合判定结论。
