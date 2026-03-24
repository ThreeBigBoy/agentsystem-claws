---
name: func-test
description: 在 OpenSpec 项目中，根据已完成的需求分析、工程结构设计与编码实现，对指定 change-id 范围内的功能进行系统化功能测试与验收；当用户输入「功能验收」「功能测试」等指令时，结合 request-analysis、project-analysis 与 coding-implement 的输出，按通用测试验收规范执行测试、发现并推动 bug 修复，并在 docs/project-prd-changes/[change-id]/records/ 下输出本次验收记录。v1.1 升级：明确「有条件通过」必须修复并重新验收后才能进入下一阶段。
---

# 功能测试与验收技能（func-test）

本技能用于在 OpenSpec 体系下，在「编码实现与代码评审」之后，对**功能进行系统化测试与验收**，确保：

- 实现行为与 `openspec/changes/[change-id]/specs/*/spec.md` 中的 Requirements + Scenarios 一一对应；
- 覆盖正常、边界与异常场景，不遗漏关键用例；
- 发现的问题被记录、分级，并通过任务与变更体系推动修复；
- 在 `docs/project-prd-changes/[change-id]/records/` 中形成可追溯的功能验收记录；
- **OpenSpec 本身需包含的操作**：第一轮 `openspec validate [change-id]`（验证已开发代码的变更需求与文档一致性），第二轮 `openspec validate --strict`（严格模式验证，用于验收结论前整体校验）。

**产出物质量约定**：验收记录须符合本技能 **REFERENCE**《验收记录-最小结构与自检》中的最小结构与产出后自检清单，详见 `agentsystem/skills/func-test/REFERENCE/验收记录-最小结构与自检.md`。

---

## 一、触发与前置依赖

- **触发指令示例**：
  - 「对 `add-xxx` 做功能验收」
  - 「帮我做这个 change 的功能测试」
  - 「按照规范把当前需求的功能跑一遍并记录结果」

- **前置技能依赖**：
  - `request-analysis`：提供本次需求的背景、场景与规范增量（`docs/project-prd-changes/[change-id]/` 与 `openspec/changes/[change-id]/specs/*/spec.md`）。
  - `project-analysis`：提供项目宪法与工程结构约定，帮助理解依赖环境与重要数据/接口。
  - `coding-implement`：对应 change-id 的功能已完成初步实现，并 ideally 通过了基本自测与 code-review。
  - （可选）`code-review`：如果已进行过 Code Review，可引用其中的问题清单与风险点，作为测试重点。

- **前置资料来源**：
  - `openspec/changes/[change-id]/specs/*/spec.md`：作为测试用例与验收标准的主要来源；
  - `openspec/changes/[change-id]/design.md`：了解关键技术/交互设计与依赖；
  - `docs/project-prd-changes/[change-id]/需求验收Checklist*.md`（如存在）：作为补充验收清单；
  - `info-database/` 与 `info-service-interface/`：涉及数据或对外接口测试时的结构与约束参考。

---

## 二、总体工作流程

1. **锁定验收范围与 change-id**
   - 根据用户输入或上下文，确认本次功能验收对应的 `change-id`；
   - 明确本次测试范围：仅某些模块/接口/页面，还是整个 change-id 下的所有能力。

2. **OpenSpec 第一轮验证（变更与文档一致性）**
   - 执行 OpenSpec CLI：`openspec validate [change-id]`（将 `[change-id]` 替换为本次验收的变更 ID，如 `add-mvp-health-food-theme`）。
   - **目的**：验证已开发完代码对应的变更目录中，提案与规范文档（proposal、design、specs、tasks 等）结构完整、与 OpenSpec 规范一致，且与当前代码/实现范围对齐。
   - 若校验未通过，应根据 CLI 输出修正变更目录下的文档或实现，再继续后续测试；将第一轮验证结果与修正动作简要记入本次验收记录。

3. **梳理测试维度与用例**
   - 根据 `specs/*/spec.md` 中的 Requirements + Scenarios，生成或整理测试用例列表：
     - 正常流程（主路径）；
     - 重要边界与异常场景；
     - 与上下游系统/模块交互的场景；
     - 非功能性要求（如简单性能、错误提示、可用性等）中可以通过功能测试验证的部分。
   - 如已有 `需求验收Checklist`，应与 spec 中的 Scenarios 对齐，合并为本次测试计划。

4. **执行测试与记录结果**
   - 在不破坏数据安全与环境约束的前提下，尽可能在：
     - 测试环境；
     - 或可控的本地/沙箱环境中执行测试；
   - 对每条用例记录：
     - 执行步骤（可以简述或引用现有说明）；
     - 实际结果；
     - 结论：通过 / 未通过 / 需人工判定；
     - 如未通过，记录期望行为与差异描述。

5. **识别 bug 与改进项，形成验收判定**
   - 将未通过用例与测试中发现的问题，归类为：
     - **Blocking（阻塞）**：核心功能与 spec 明显不符，必须修复后才能进入下一阶段；
     - **Major（重要）**：功能可用但存在明显缺陷或边界问题，建议修复；
     - **Minor（次要）**：体验优化、提示优化等建议，不影响核心功能。
   - 对 bug 建议交由 `coding-implement` + `code-review` 流程进行修复与复查；
   - 对 spec 问题建议回到 `request-analysis` / `project-analysis` 层处理。

   **综合判定**：
   - **✓ 通过**：所有测试用例通过，无 Blocking 问题，可直接进入下一阶段
   - **△ 有条件通过**：无 Blocking 问题，但存在 Major/Minor 未通过项，需修复后重新验收
   - **✗ 不通过**：存在 Blocking 问题，必须修复后重新验收

   **验收结论与后续动作映射（重要）**：

   | 验收结论 | 是否可以进入下一阶段 | 后续动作 |
   |---------|-------------------|---------|
   | **✓ 通过** | ✅ **可以** | 直接进入下一阶段（Step 8: 归档） |
   | **△ 有条件通过** | ❌ **不可以** | **必须**修复问题清单中的未通过项，**重新验收**通过后，才能进入下一阶段 |
   | **✗ 不通过** | ❌ **不可以** | **必须**修复 Blocking 问题，**重新验收**通过后，才能进入下一阶段 |

   > ⚠️ **重要澄清**：「有条件通过」≠ 「可以进入下一阶段」。只有「100% 通过」才是真正的通过。详见 `memory/patterns/pattern-review-fix-loop.md`

   **验收修复循环**：
   ```
   首次验收 ──→ 有条件通过/不通过 ──→ 修复问题 ──→ 重新验收 ──→ 通过？──→ 否 → 继续修复
                                                              └──────→ 是 → 进入下一阶段
   ```

6. **输出测试验收记录**
   - 在 **`docs/project-prd-changes/[change-id]/records/`** 下创建本次验收记录文件，建议文件名 **`[change-id]-func-test.md`**（或 `func-test.md`）；
   - 记录**最小结构与自检**须符合 REFERENCE《验收记录-最小结构与自检》：含基本信息、范围说明、用例与结果汇总、问题与 bug 列表、结论与建议；两轮 `openspec validate` 结果须记入记录；产出后执行该 REFERENCE 中的自检清单，通过后再给出是否推荐通过验收的结论。
   - **如首次验收为「有条件通过」或「不通过」**，修复后必须执行**重新验收**，产出**重新验收记录**（文件命名：`[change-id]-func-test-重新验收.md`）

7. **OpenSpec 第二轮验证（严格模式）**
   - 执行 OpenSpec CLI：`openspec validate --strict`（在项目根目录下执行）。
   - **目的**：在功能测试与记录完成后，以严格模式再次校验整个 openspec 目录（含当前 change 及与其它变更/规范的一致性），确保可归档、可发布。
   - 若严格模式未通过，应在验收记录中注明未通过项与建议处理方式，并将相关任务纳入 `tasks.md` 或后续变更；通过后再给出「推荐通过本次验收」的结论。

8. **联动任务与后续变更**
   - 将关键 bug 或未通过项转化为 `openspec/changes/[change-id]/tasks.md` 中的任务；
   - 如问题跨越多个 change-id 或涉及更大范围的架构/需求调整，应建议创建新变更目录进行跟踪。

---

## 三、与 OpenSpec 的对应关系

- **与 specs/*/spec.md 的关系**
  - 每条 Scenario 都可以视为一个或多个测试用例的基础；
  - 功能验收应尽量做到「Scenario 级」的覆盖与结果记录；
  - 若 Scenario 描述不足以支撑测试，应在验收记录中提出，并推动 spec 补充。

- **与 documents/ 的关系**
  - `docs/project-prd-changes/[change-id]/` 中的需求说明与验收 Checklist 是测试计划的重要来源；
  - `documents/records/[change-id]-func-test*.md` 是实际执行与结果的落地记录，两者应形成「计划-执行」闭环。

---

## 四、与其他技能的协同方式

- **与 `request-analysis`**
  - 提供需求场景与验收标准基础（尤其是 Checklist 与 spec Scenarios），是测试设计的起点。

- **与 `project-analysis`**
  - 帮助理解测试所需的环境、数据与依赖（如外部系统、配置、feature flag 等）。

- **与 `coding-implement`**
  - 功能测试中发现的 bug，通常需要通过 coding-implement 流程进行修复；
  - 如修复引入新的实现，建议在必要时再次调用 func-test 进行回归。

- **与 `code-review`**
  - Code Review 发现的潜在风险点可作为测试重点；
  - 功能测试中发现的问题可反馈给 code-review，丰富其检查维度。

---

## 五、执行时的注意事项

- **环境与数据安全**
  - 尽量在测试/预发环境进行验收，避免在生产环境执行破坏性操作；
  - 如必须在生产环境验证，需遵守项目的变更与回滚策略。

- **明确通过标准**
  - 在测试前尽量将「通过/不通过」标准写到文档中（或在执行时补充），避免主观判断；
  - 对存在灰度空间的项，可标记为「需产品/业务确认」。

- **遇到不确定项要主动提问**
  - 对需求、边界条件、依赖环境不清的地方，应在给出结论前先与用户确认。

---

## 六、示例使用流程（某具体项目）

1. 用户输入：「功能验收：请对 `add-mvp-health-food-theme` 这个 change 做一次功能测试，并输出测试记录。」  
2. AI（func-test）：
   1. 确认 change-id 为 `add-mvp-health-food-theme`，加载其 `specs/*/spec.md`、`design.md` 与 `需求验收Checklist`；  
   2. **第一轮 OpenSpec 验证**：执行 `openspec validate add-mvp-health-food-theme`，确认变更目录与文档一致；未通过则先修正再继续；  
   3. 对照健康食品 Shopify 主题 MVP 的各项 Scenario，列出需要验证的页面与配置场景（如推荐区展示、倒计时 Section 行为、多模板切换等），并逐项执行测试、记录结果；  
   4. 对发现的行为不符或边界问题，记录为 bug，并建议通过 `coding-implement` + `code-review` 流程修复；
   5. **形成验收判定**（通过/有条件通过/不通过），明确是否可以进入下一阶段；
   6. 在 `documents/records/add-mvp-health-food-theme-func-test.md` 中输出本次验收记录，并将关键问题同步到 `tasks.md`；
   7. **如判定为「有条件通过」或「不通过」**，修复后执行重新验收，产出重新验收记录，转为「通过」后方可进入下一阶段；
   8. **第二轮 OpenSpec 验证**：执行 `openspec validate --strict`，通过后再给出是否推荐通过本次验收的结论。  

通过本技能，OpenSpec 项目在「需求 → 结构 → 实现 → 评审」之后增加了**规范化的功能验收环节**，帮助确保交付质量与文档标准的一致性。

---

## 七、执行后必做收尾

### 1. 向迭代日志追加记录

**首次验收记录**（所有验收都必须记录）：
- 文件：`docs/项目事件日志.md`
- 格式：`- [日期] | [change-id] | func-test | 功能验收完成，综合判定：[通过/有条件通过/不通过]，验收记录路径：[路径]`

**重新验收记录**（如首次验收为「有条件通过」或「不通过」，修复后必须重新验收并记录）：
- 格式：`- [日期] | [change-id] | func-test | 功能重新验收完成，修复项：[N 项]，综合判定：[通过]，验收记录路径：[路径]`

**示例**：
```markdown
# 首次验收（有条件通过）
- 2026-03-16 | check-langgraph-backend | func-test | 功能验收完成，综合判定：有条件通过（需人工验证 4 项），验收记录路径：docs/project-prd-changes/check-langgraph-backend/records/check-langgraph-backend-func-test.md

# 修复后重新验收（通过）
- 2026-03-16 | check-langgraph-backend | func-test | 功能重新验收完成，修复项：4 项已验证，综合判定：通过，验收记录路径：docs/project-prd-changes/check-langgraph-backend/records/check-langgraph-backend-func-test-重新验收.md
```

### 2. 向用户反馈验收结果

1. **验收结果摘要**：综合判定（通过/有条件通过/不通过）
2. **问题统计**：Blocking [N] 项 / Major [N] 项 / Minor [N] 项 / 需人工验证 [N] 项
3. **关键问题**：阻塞性问题（如有）
4. **验收记录路径**：告知用户验收记录文档存放位置
5. **后续行动建议**：
   - 若通过：可进入 Step 8（归档）
   - 若有条件通过：**不能进入下一阶段**。必须：① 修复/验证问题 → ② 执行重新验收 → ③ 转为「通过」后，才能进入下一阶段
   - 若不通过：**不能进入下一阶段**。必须：① 修复 Blocking 问题 → ② 执行重新验收 → ③ 转为「通过」后，才能进入下一阶段

---

**技能版本**: v1.1（2026-03-17 升级：明确「有条件通过」必须修复并重新验收后才能进入下一阶段）  
**最后更新**: 2026-03-17  
**依赖 REFERENCE**: `skills/func-test/REFERENCE/验收记录-最小结构与自检.md`  
**关联 Memory**: `pattern-review-fix-loop`, `anti-pattern-conditional-pass-as-go`, `anti-pattern-terminology-drift`

