# OpenSpec 开发规范（usr-rules）

> **定位**：驱动**所有业务项目**研发与变更治理的**原始规范**；与项目内 `openspec/`、`docs/` 配合使用。  
> 下文路径以仓库根为起点；示例项目名 **`curiobuddy`** 可替换为任意 `{project}`。

---

## 一、业务项目目录结构（初始化与 change-id 推进）

| 路径（相对项目根） | 用途 |
|-------------------|------|
| **`src/`** | **业务源码根目录**（**唯一合法**目录名；须在 **`openspec/project.md`** 写明并与仓库内实际目录一致；**不得**使用 `app_*`、`<project_code>` 等其它名称作为源码根） |
| `docs/project-early-phase/` | 项目**前期立项**资料（市场/方案/调研等），在首个研发 change-id 之前 |
| `docs/project-prd-changes/[change-id]/` | **每一 change-id** 的 PRD 主文档；其下 `records/` 放评审纪要等；`reference/` 放交互稿、视觉稿、PRD 附录等衍生材料 |
| `openspec/` | **每一 change-id** 的标准过程文档（`changes/[change-id]/`：proposal、tasks、design、specs 等）及归档产物（见第三节） |
| `docs/retrospective/` | **本项目全部复盘**。**change-id 闭环流程中发起的复盘** → 按 `docs/retrospective/[change-id]/` 归组；**项目级复盘**（非某一 change-id 闭环触发）→ 放在本目录**根下** |
| `docs/sop-product-use/` | 产品使用类操作 SOP（**可选**，按需建立） |

**原则**：目录先建再写；同一 change-id 在 `docs/project-prd-changes/` 与 `openspec/changes/` 中的条目须可互相引用、可追溯。

---

## 二、10 步质量闭环（含人工确认；**归档为最后一步**）

### 2.1 概要框架图

```text
 1.需求分析          2.PRD评审──┐
        │                 │    │ 评审修复环（有条件通过须修回再评，见 memory）
        ▼                 ▼    │
 3.技术方案         4.方案评审──┘
        │                 │
        ▼                 ▼
 5.编码实现  →  6.代码评审  →  7.功能验收
        │                 │
        └────────┬────────┘
                 ▼
 8.复盘  →  9.全局检查与联动更新  →  【归档前人工确认】→  10.OpenSpec 归档（最终）
```

- **门禁**：每步准入/准出、tasks 勾选顺序、阶段启动前自检，见 memory `pattern-quality-gate-checkpoint.md`。  
- **评审结论**：「有条件通过」**不得**当作进入下一阶段的放行条；须**修复 → 再评审 → 通过**后再推进，见 `pattern-review-fix-loop.md`、`preference-review-conclusion-action-mapping.md`、`anti-pattern-conditional-pass-as-go.md`。

### 2.2 三步关键人工确认（硬约束）

| 时机 | 内容 |
|------|------|
| **PRD 终稿** | Step 2 闭环内：PRD 评审结论达到**可落地终稿**（按项目约定签字/确认方式，书面留痕在 `records/`） |
| **技术方案终稿** | Step 4 闭环内：技术方案评审结论达到**可开发终稿**（书面留痕在 `records/`） |
| **归档前** | Step 9 完成后、执行 Step 10 **之前**：确认复盘与全局联动事项已闭环、可安全合并 specs/ 与移动 `changes/`（书面留痕） |

#### 2.2.1 评审子阶段与「终稿」人工门禁分拆（语义强制）

> **目的**：避免把「Agent 组织评审」「修回再评直至通过」「人类确认终稿」混成一步，导致跳过评审纪要或误把「Agent 已改稿」当作终稿。**10 步主编号不变**（仍为 Step 1～10）；本节规定 **Step 2、Step 4 内部的子阶段**与 **§2.2 表内「终稿」门禁**的对应关系。

**PRD 线（映射 Step 1～2 + §2.2 之 PRD 终稿）**

| 子阶段 | 谁主导 | 做什么 | 产出 / 准出 |
|--------|--------|--------|-------------|
| **PRD-R**（评审执行） | Agent（`prd-review`） | 按自检清单评审 PRD，形成书面结论 | `docs/project-prd-changes/[change-id]/records/` 下 **PRD 评审纪要** |
| **PRD-F**（评审修复环） | Agent + 人类按需 | 结论为不通过/有条件通过时：**修改 PRD → 再评审 →** 直至纪要中综合判定为 **通过**（不得用「有条件通过」直接放行，见 `pattern-review-fix-loop`） | 纪要中记录各轮次；**最后一轮综合判定：通过** |
| **Gate-PRD**（终稿门禁） | **人类**（按项目约定） | 在 Agent 侧评审已「通过」后，对 **PRD 可落地终稿**做确认/签署 | `records/` 留痕（如终稿确认单、签字纪要、或项目约定等价物）；**未过本门禁不得宣称 PRD 终稿已定版** |

**技术方案线（映射 Step 3～4 + §2.2 之技术方案终稿）**

| 子阶段 | 谁主导 | 做什么 | 产出 / 准出 |
|--------|--------|--------|-------------|
| **DESIGN-R**（评审执行） | Agent（`architecture-review` 等，见 `claw-config/SKILLS.md`） | 对照 PRD 评审 `design.md` | `records/` 下 **技术方案评审纪要** |
| **DESIGN-F**（评审修复环） | Agent + 人类按需 | 不通过/有条件通过时：**修改 design.md（及关联文档）→ 再评审 →** 直至 **通过** | 最后一轮综合判定：**通过** |
| **Gate-DESIGN**（终稿门禁） | **人类** | 确认 **技术方案可开发终稿** | `records/` 书面留痕；**未过本门禁不得进入 Step 5** |

**与 §2.5 停止线判断的写法**：Agent 应区分 **「评审修复环进行中（PRD 或方案）」** 与 **「评审已通过、待人类终稿门禁（Gate-PRD / Gate-DESIGN）」**，避免二者混淆。

### 2.3 归档位序（相对经典 memory 的调整）

- **复盘（原 Step 9 概念）**、**全局检查与联动更新（原 Step 10 概念）** → **先于**最终归档执行完毕。  
- **Step 10**：在通过 **「归档前人工确认」** 之后，再执行 **OpenSpec 归档**（合并 specs、归档 `changes/` 等），作为本 change-id **最后一击**。

### 2.4 详细步骤与技能映射（按需）

完整步骤说明、产出路径、Skill 名称以 **`agentsystem/sys-root/lib/memory/patterns/pattern-complete-quality-closed-loop.md`** 为准；本节只固定**顺序、人工点与归档在末**的约束。

### 2.5 Agent 执行策略（收口至 Skill）

本节约束 **业务项目** 内针对某一 **change-id** 的 Agent 行为（与 `openspec/AGENTS.md`、`claw-config/SKILLS.md`、memory `pattern-complete-quality-closed-loop` 一致；**不**替代 **§2.2 三处关键人工确认** 的硬约束）。

**执行权威**：`dev-workflow-orchestration` 技能（`sys-root/lib/skills/dev-workflow-orchestration/SKILL.md`）统一处理：
- 阶段判断与准入判断
- 自主推进编排
- 停止线识别
- Skill/Memory 调度

**禁止**：
- 以「自主推进」为由跳过 Skill/Memory
- 跳过书面留痕要求
- 在「有条件通过」时未修复即进入下一阶段

---

## 三、OpenSpec 核心概念（精简）

| 概念 | 含义 | 典型位置 |
|------|------|----------|
| **Specs** | 已实现能力规范 | `openspec/specs/` |
| **Changes** | 进行中变更 | `openspec/changes/[change-id]/` |
| **Archive** | 已完成变更快照 | `openspec/changes/archive/`（或工具等价路径） |

### 3.1 项目根 `openspec/` 标准结构

```text
openspec/
├── AGENTS.md           # 治理层：与本规范、技能、规则的关系（项目内填写）
├── project.md          # 项目顶层约定
├── specs/              # 按能力分子目录
└── changes/
    └── [change-id]/
        ├── proposal.md
        ├── tasks.md
        ├── design.md          # 可选
        └── specs/[capability]/spec.md
```

### 3.2 `capability` 颗粒度划分准则

| 原则 | 说明 |
|------|------|
| **一条能力、一块规范** | 每个 `capability` 对应**一类可独立描述的行为边界**（对外可叫出名：如「用户登录」「购物车」），目录名用 **kebab-case**（`user-auth`、`cart-drawer`）。 |
| **不宜过大** | 避免把整个系统塞进单一 `capability`；按**子域 / 用户旅程段 / 可独立验收的产品块**拆分，使单份 `spec.md` 仍可读、可评审。 |
| **不宜过细** | 避免为**单个字段、单条接口、一次性小补丁**单独建 `capability`；可合并到**同一业务域**下，用 Requirements/Scenario 分层表达。 |
| **与 PRD/变更对齐** | 同一 change-id 内，**一个 PRD 功能组 / 一条清晰用户故事线**通常对应 **一个** `capability`；若变更跨多域，可设多个 `capability` 子目录，各一份 `spec.md`。 |
| **与实现弱耦合** | 以**产品能力与验收语义**为主划分，**不以**「每个微服务一个目录」机械对应（除非服务边界与产品边界一致）。 |

**判据自测**：若说不清「少了这一块，用户还能否单独理解/验收」，往往颗粒度不对——过大则拆，过小则并。

---

## 四、核心文件与规范要点（精简）

| 文件 | 要点 |
|------|------|
| **AGENTS.md** | 治理入口：可调用的 skills、须遵循的全局/项目规则；**运行时人设见 `claw-config/AGENTS.md`**（若项目区分两层） |
| **project.md** | 技术栈、目录、命名、**业务源码根固定为 `src/`**、与仓库根 `project-rules/` 关系 |
| **proposal.md** | **优先对齐 PRD**：变更范围、目标与非目标须以同 change-id 下 **`docs/project-prd-changes/[change-id]/` 中 PRD 终稿**为准；Why / What / Impact 须**可追溯到 PRD 条目**，并显式引用路径或章节。**禁止**在未更新 PRD 的前提下扩大范围；若需调整需求，先修订 PRD 再改 proposal。 |
| **tasks.md** | `- [ ] N.M` 编号任务；**后置勾选依赖前置完成**；可验证任务须验收后再勾 |
| **design.md** | 技术方案须与 PRD **可追溯**；产出结构与质量须按 **`sys-root/lib/skills/technical-design-review/SKILL.md`**（及该技能下 `REFERENCE/`）执行，**等同**经技术设计评审可接受的质量基线（章节、自检、与 PRD/openspec 对齐等）。 |
| **specs/.../spec.md** | ADDED/MODIFIED/REMOVED + `#### Scenario:` |

---

## 五、命名规范（精简）

| 类型 | 规则 | 示例 |
|------|------|------|
| **业务源码根** | 仓库根下**固定为** `src/`（**不得**使用 `app_*` 等其它名称作为源码根） | `src/` |
| **change-id** | kebab-case，可动词开头，唯一 | `add-user-profile` |
| **capability** | 动词-名词、单一职责 | `user-auth` |
| **保留 change-id** | 项目前期未进入研发迭代 | `project-early-phase`（产出在 `docs/project-early-phase/`，规则见历史 OpenSpec 实践） |

---

## 六、变更启动顺序（新建 change-id 时）

1. 建 `docs/project-prd-changes/[change-id]/`（至少一份需求/PRD 侧产出）。  
2. 建 `openspec/changes/[change-id]/`（proposal 引用上一步路径）。  
3. 迭代日志、tasks 勾选与门禁按项目 `AGENTS.md` 与 **第二节** 执行。

---

## 七、阶段工作流与归档

- **Planning**：见第六节；`openspec validate` 校验变更结构。  
- **Implementation**：按 tasks；重大决策已体现在 `proposal.md`、变更目录内 **`design.md`**（技术方案文件，非名为 `design/` 的磁盘目录）、`specs/`。  
- **Archiving**：**仅**在 **第二节 Step 10** 执行（含合并 specs、移动/归档 changes）；命令见下节。

---

## 八、常用命令速查（需 OpenSpec CLI）

```bash
openspec list
openspec list --specs
openspec show [item]
openspec validate [change-id]
openspec validate --strict
openspec archive <change-id> --yes
openspec archive <change-id> --skip-specs --yes
```

---

## 九、常见问题（精简）

- **Change must have at least one delta**：`changes/[id]/specs/**/*.md` 中含 `## ADDED Requirements`（或 MODIFIED/REMOVED）。  
- **Requirement must have at least one scenario**：场景标题为 `#### Scenario:`。  
- **验证失败**：`openspec validate --strict` 或 `--json` 查结构。

---

## 十、Memory 按需引用（agentsystem 内路径）

| 主题 | 路径 |
|------|------|
| 完整 10 步与产出 | `sys-root/lib/memory/patterns/pattern-complete-quality-closed-loop.md` |
| 评审—修复循环 | `sys-root/lib/memory/patterns/pattern-review-fix-loop.md` |
| 阶段门禁检查点 | `sys-root/lib/memory/patterns/pattern-quality-gate-checkpoint.md` |
| 评审结论与后续动作 | `sys-root/lib/memory/preferences/preference-review-conclusion-action-mapping.md` |
| 有条件通过即放行（反模式） | `sys-root/lib/memory/anti-patterns/anti-pattern-conditional-pass-as-go.md` |

---

*版本：usr-rules 重写稿；§2.5 为 2026-03 增补并收口至 `dev-workflow-orchestration` 技能；**§2.2.1** 为 2026-03 增补（评审子阶段与 Gate 分拆）。与业务仓库实际目录以项目 `project.md` / `AGENTS.md` 为准。*
