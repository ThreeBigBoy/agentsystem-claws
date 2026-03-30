---
name: code-review
description: 在 OpenSpec 项目中，根据已完成的需求分析与工程结构设计，对指定 change-id 范围内的代码进行系统化 Code Review；当用户输入「编码实现」「代码评审」「帮我 Review 这个 change」等指令时，结合 request-analysis 与 project-analysis 的输出，按通用 review 规范检查并提出修改建议，并在 docs/project-prd-changes/[change-id]/records/ 下输出本次 review 记录。v1.1 升级：明确「有条件通过」必须修复并重新评审后才能进入下一阶段。
---

# Code Review 技能（code-review）

本技能用于在 OpenSpec 体系下，对**已有或刚实现的代码**进行系统化 Code Review，确保：

- 代码实现与 `openspec/changes/[change-id]/specs/*/spec.md` 中的 Requirements + Scenarios 一一对应；
- 遵守 `openspec/project.md` 与 `project-rules/` 中的架构、技术栈、分层、命名与约束；
- 发现并记录问题、改进建议与后续行动项，在 **`docs/project-prd-changes/[change-id]/records/`** 中形成可追溯的 review 记录（建议文件名 `[change-id]-code-review.md`），与 func-test 验收记录同目录，便于按变更归档。

**产出物质量约定**：评审记录须符合本技能 **REFERENCE**《评审报告-最小结构与自检》中的最小结构与产出后自检清单，详见 `agentsystem/skills/code-review/REFERENCE/评审报告-最小结构与自检.md`。

---

## 一、触发与前置依赖

- **触发指令示例**：
  - 「编码实现后，帮我做代码评审」
  - 「对 `add-xxx` 这个 change 做 code review」
  - 「帮我 review 当前改动是否符合 OpenSpec 规范」

- **前置技能依赖**：
  - `request-analysis`：已为当前需求（`change-id`）产出 `docs/project-prd-changes/[change-id]/` 与 `openspec/changes/[change-id]/` 下的前期资料、变更提案、规范增量与任务拆分。
  - `project-analysis`：已按需要更新 `openspec/project.md` 与 `project-rules/`，使工程结构与约定清晰统一。
  - `coding-implement`（通常）：已根据前述文档完成初步编码实现或修改，形成可 review 的代码差异。

- **前置资料来源（review 前需主动阅读）**：
  - `openspec/changes/[change-id]/proposal.md`、`design.md`、`specs/*/spec.md`、`tasks.md`；
  - `openspec/project.md` 与 `project-rules/`（尤其是分层规范与命名/数据/接口约定）；
  - 代码变更本身（如 Git diff / 当前工作副本）。

---

## 二、总体工作流程

1. **锁定 review 范围与 change-id**
   - 根据用户输入或最近上下文，确认本次 Code Review 的 `change-id` 以及待 review 的代码范围（文件/模块/提交）；
   - 如 `change-id` 不明确，应主动询问用户或提示按 OpenSpec 变更目录选择。

2. **对齐规范与期望**
   - 对照 `specs/*/spec.md` 中的 Requirements + Scenarios，确认本次变更预期解决的问题与覆盖的场景；
   - 阅读 `design.md` 中的关键技术与架构决策，确保 Review 时以其为基准；
   - 引用 `project-rules/` 与分层规范（如 backend 各层规范、frontend 规范），确认代码是否在正确的层落地。

3. **按维度执行 Code Review**
   - 参考 `code-review/REFERENCE/` 下的通用规范，从以下维度检查代码：
     - 需求符合性与场景覆盖；
     - 架构/分层与依赖方向；
     - 代码质量（可读性、复杂度、重复、命名、注释）；
     - 安全性与鲁棒性（边界条件、错误处理、输入校验）；
     - 性能与资源使用（在敏感路径中特别关注）；
     - 日志、监控与可观测性；
     - 测试情况与可测试性；
     - 与 `info-database/` 与 `info-service-interface/` 的一致性（如涉及数据表或对外接口变更）。

4. **给出修改建议与行动项，形成评审判定**
   - 对发现的问题给出**具体、可操作**的建议（例如：应将逻辑上移到业务层、应改用仓储接口、应补充某个 Scenario 的测试等）；
   - 避免空泛评价，尽可能指向具体文件/函数/模块；
   - 如发现需要回到需求或结构层重新讨论的议题，应明确标注为「需上升到设计/架构层处理」。

   **问题分级与评审判定**：
   - **Blocking（阻塞）**：影响功能正确性、安全性、性能或违反架构原则，必须修复后才能进入下一阶段
   - **Major（重要）**：影响代码质量、可维护性，建议修复
   - **Minor（次要）**：编码风格、注释优化等建议

   **综合判定**：
   - **✓ 通过**：无 Blocking 问题，代码符合规范，可直接进入下一阶段
   - **△ 有条件通过**：无 Blocking 问题，但存在 Major/Minor 建议，需修复后重新评审
   - **✗ 不通过**：存在 Blocking 问题，必须修复后重新评审

   **评审结论与后续动作映射（重要）**：

   | 评审结论 | 是否可以进入下一阶段 | 后续动作 |
   |---------|-------------------|---------|
   | **✓ 通过** | ✅ **可以** | 直接进入下一阶段（Step 7: 功能验收） |
   | **△ 有条件通过** | ❌ **不可以** | **必须**修复问题清单中的建议，**重新评审**通过后，才能进入下一阶段 |
   | **✗ 不通过** | ❌ **不可以** | **必须**修复 Blocking 问题，**重新评审**通过后，才能进入下一阶段 |

   > ⚠️ **重要澄清**：「有条件通过」≠ 「可以进入下一阶段」。只有「100% 通过」才是真正的通过。详见 `memory/patterns/pattern-review-fix-loop.md`

   **评审修复循环**：
   ```
   首次评审 ──→ 有条件通过/不通过 ──→ 修复问题 ──→ 重新评审 ──→ 通过？──→ 否 → 继续修复
                                                            └──────→ 是 → 进入下一阶段
   ```

5. **输出 review 记录**
   - 在 **`docs/project-prd-changes/[change-id]/records/`** 下，为本次 review 创建记录文件，建议文件名 **`[change-id]-code-review.md`**（与 func-test 验收记录同目录，符合 OpenSpec 1.1 表约定）；
   - 记录**最小结构与自检**须符合 REFERENCE《评审报告-最小结构与自检》：含基本信息、整体结论、问题清单（Blocking/Major/Minor）、后续行动；产出后执行该 REFERENCE 中的自检清单，通过后再视为本次评审完成。
   - **如首次评审为「有条件通过」或「不通过」**，修复后必须执行**重新评审**，产出**重新评审纪要**（文件命名：`[change-id]-code-review-重新评审纪要.md`）

---

## 三、与 OpenSpec 的对应关系

- **与变更目录的关系**
  - 每次 Code Review 都应绑定一个明确的 `change-id`；
  - Review 中发现的问题或新需求，可通过：
    - 在当前 `tasks.md` 中追加任务；
    - 或为新需求/大改动创建新的 `change-id` 与变更目录。

- **与规范文档的关系**
  - 若在 review 中发现代码与 `project.md` / `project-rules/` / `specs/*/spec.md` 不一致，需判断：
    - 是代码没跟上规范 → 建议修正代码；
    - 还是规范已过时或不合理 → 应同步更新规范，并在 review 记录中说明原因。

---

## 四、与其他技能的协同方式

- **与 `request-analysis`**
  - 提供需求来源与场景描述，帮助判断代码是否真正满足需求、是否遗漏场景。

- **与 `project-analysis`**
  - 提供最新工程结构与约定，作为判断「是否越层」「依赖方向是否正确」的依据。

- **与 `coding-implement`**
  - 在编码之后调用 `code-review`，对照编码规范与项目约定进行质量把关；
  - Review 结果中的修改建议，可作为下一轮 `coding-implement` 的输入。

---

## 五、执行时的注意事项

- **聚焦本次 change 范围**
  - 优先 review 与当前 `change-id` 直接相关的代码，避免在一次 review 中扩散到无关部分；
  - 如发现历史问题，可记录为「遗留问题」，统一纳入后续规划。

- **优先级与反馈方式**
  - 对阻断上线的问题（Blocking）要明确标记，优先整改；
  - 建议以「问题 + 原因 + 建议方案」的形式给出反馈，避免只指出“这里不好”。

- **遇到不确定项要主动提问**
  - 对需求理解、架构意图、非功能性要求（性能、安全、合规等）存在疑问时，先问清楚再给出结论性意见。

---

## 六、示例使用流程（某具体项目）

1. 用户输入：「编码实现完成后，请对 `add-mvp-health-food-theme` 这个 change 做一次 code review，并出一份记录。」  
2. AI（code-review）：
   1. 确认本次 change-id 为 `add-mvp-health-food-theme`，加载其 `proposal.md`、`design.md`、`specs/*/spec.md` 与 `tasks.md`；  
   2. 阅读 `openspec/project.md` 与 `project-rules/`，了解 Shopify 主题项目的架构、分层与命名约定；  
   3. 检查与本次 change 相关的主题模板、Section、Snippet、Metafields 使用等代码变更；  
   4. 按 REFERENCE 中的通用 code-review 规范，对需求覆盖、分层、可读性、安全/性能、日志与监控等维度进行 Review，提出具体修改建议；
   5. **形成评审判定**（通过/有条件通过/不通过），明确是否可以进入下一阶段；
   6. 在 `docs/project-prd-changes/add-mvp-health-food-theme/records/add-mvp-health-food-theme-code-review.md` 中记录本次 Review 的结论、问题与后续行动项；
   7. **如判定为「有条件通过」或「不通过」**，修复后执行重新评审，产出重新评审纪要，转为「通过」后方可进入下一阶段。

通过本技能，OpenSpec 项目可以在「需求 → 结构 → 实现」之后增加一个**规范化的代码评审环节**，让代码质量与文档/架构约定保持长期一致。

---

## 七、执行后必做收尾

### 1. 向迭代日志追加记录

**首次评审记录**（所有评审都必须记录）：
- 文件：`docs/项目事件日志.md`
- 格式：`- [日期] | [change-id] | code-review | 代码评审完成，综合判定：[通过/有条件通过/不通过]，评审纪要路径：[路径]`

**重新评审记录**（如首次评审为「有条件通过」或「不通过」，修复后必须重新评审并记录）：
- 格式：`- [日期] | [change-id] | code-review | 代码重新评审完成，修复项：[N 项]，综合判定：[通过]，评审纪要路径：[路径]`

**示例**：
```markdown
# 首次评审（有条件通过）
- 2026-03-16 | check-langgraph-backend | code-review | 代码评审完成，综合判定：有条件通过（2项 Minor），评审纪要路径：docs/project-prd-changes/check-langgraph-backend/records/check-langgraph-backend-code-review.md

# 修复后重新评审（通过）
- 2026-03-16 | check-langgraph-backend | code-review | 代码重新评审完成，修复项：2 项，综合判定：通过，评审纪要路径：docs/project-prd-changes/check-langgraph-backend/records/check-langgraph-backend-code-review-重新评审纪要.md
```

### 2. 向用户反馈评审结果

1. **评审结果摘要**：综合判定（通过/有条件通过/不通过）
2. **问题统计**：Blocking [N] 项 / Major [N] 项 / Minor [N] 项
3. **关键问题**：阻塞性问题（如有）
4. **评审纪要路径**：告知用户评审纪要文档存放位置
5. **后续行动建议**：
   - 若通过：可进入 Step 7（功能验收）
   - 若有条件通过：**不能进入下一阶段**。必须：① 修复问题 → ② 执行重新评审 → ③ 转为「通过」后，才能进入下一阶段
   - 若不通过：**不能进入下一阶段**。必须：① 修复 Blocking 问题 → ② 执行重新评审 → ③ 转为「通过」后，才能进入下一阶段

---

## 八、功能ID格式规范

功能ID用于唯一标识代码对应的功能点，格式定义如下：

```
F-主功能编号[.子功能编号]
```

**规则**：
- 主功能编号：正整数，如 `F-1`、`F-2`
- 子功能编号：最多2位小数，如 `F-1.1`、`F-1.2`、`F-1.15`
- 子功能编号可选

**有效示例**：`F-1`、`F-2`、`F-1.1`、`F-1.2`、`F-2.1`、`F-1.15`
**无效示例**：`FR-1`（旧格式）、`F-1.1.1`（超过2位小数）

**注意**：统一使用 `F-\d+(?:\.\d{1,2})?` 格式，禁止使用旧格式 `FR-1.1`。

---

**技能版本**: v1.1（2026-03-17 升级：明确「有条件通过」必须修复并重新评审后才能进入下一阶段）  
**最后更新**: 2026-03-17  
**依赖 REFERENCE**: `skills/code-review/REFERENCE/评审报告-最小结构与自检.md`  
**关联 Memory**: `pattern-review-fix-loop`, `anti-pattern-conditional-pass-as-go`, `anti-pattern-terminology-drift`

