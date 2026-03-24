---
id: mem-default-product-template-health-compliance-001
title: 默认产品模板挂载健康合规模块（可复用模式）
type: pattern
tags: [shopify-theme, health-compliance, product-template, default-behavior]
applicable_projects: [Proj01ShopifyTheme, *]
host_scope: [cursor, vscode, generic]
source_change_ids: [add-default-product-template-health-compliance]
created_at: 2026-03-17
last_reviewed_at: 2026-03-17
maturity: draft
related:
  - memory/patterns/pattern-openspec-change-workflow.md
  - memory/patterns/pattern-complete-quality-closed-loop.md
---

# 默认产品模板挂载健康合规模块（可复用模式）

## 一、背景与适用场景

在健康食品类 Shopify 主题中，「产品详情页健康合规模块」（如 `product-health-compliance`）往往已经作为独立 section 实现，但若只停留在「section 存在、编辑器里可手动添加」，新安装主题的商家仍需要：

- 找到该 section；
- 手工将其挂载到 product 模板；
- 再按文档完成配置。

这会削弱「开箱即合规」的产品卖点，也增加了初次配置成本。`add-default-product-template-health-compliance` 这次变更的经验是：**在默认产品模板层面，将健康合规模块做成默认挂载行为，并用 OpenSpec + LangGraph + 完整质量闭环固化为可追溯模式**。

本模式适用于：

- 已有「产品页健康合规模块」能力（或类似合规/安全信息模块）的主题项目；
- 需要在「新安装主题 → 打开产品页」这一链路上，实现**默认挂载合规模块**，而不是依赖商家手动添加；
- 希望该行为对新成员/后续变更也是显式、可追溯、可验收的。

## 二、推荐做法（步骤 / Checklist）

### Step 1：在 PRD 中显式定义「默认模板行为」

1. 在 `docs/project-prd-changes/[change-id]/迭代需求说明.md` 中，增加一节「默认产品模板行为」：
   - 明确：默认 product 模板（通常是 `templates/product.json`）**SHALL** 包含健康合规模块 section；
   - 说明适用范围：仅默认模板必须包含，其它 product 模板可选；
   - 将此作为独立的功能项与验收标准。
2. 补充需求验收 Checklist 项，例如：
   - `product.json` 的 `sections` 中含 type 为 `product-health-compliance` 的 section；
   - `order` 数组中包含该 section 的 key。

### Step 2：在 spec 中固化「默认模板挂载」为正式 Requirement

1. 在 `openspec/changes/[change-id]/specs/health-compliance/spec.md` 中新增 ADDED Requirement，例如：
   - **Requirement: 默认产品模板包含健康合规模块**；
   - 至少两个 Scenario：
     - 新安装主题时产品页默认展示合规区；
     - 检查 `product.json` 结构可验证 sections/order 中包含对应 section。
2. 归档后，确认该 Requirement 已被合并进 `openspec/specs/health-compliance/spec.md`，成为长期规范的一部分。

### Step 3：以默认 product 模板为实现落点，而非零散代码

1. 实际实现层，优先选择在 **默认 product 模板 JSON** 中挂载 section，而不是在各处模板中「顺手」插入：
   - 对 Shopify 主题而言，即在 `templates/product.json` 的 `sections` 与 `order` 中加入健康合规模块；
   - 保持其它模板（如 `product.alternative.json`）自由度，用 PRD/spec 说明仅默认模板强制。
2. 通过 code-review 检查：
   - 没有在其它不该强制的模板中硬编码合规模块；
   - 默认模板的 JSON 结构清晰、易读、无多余配置。

### Step 4：按 10 步质量闭环执行评审与验收

1. PRD 评审（prd-review）：确认「默认行为」在 PRD 中表述清楚、场景充分。
2. Code Review（code-review）：
   - 对照 spec 中 Requirement，确认 `product.json` 结构与预期一致；
   - 无多余耦合（例如依赖特定 handle、依赖测试数据）。
3. 功能验收（func-test）：
   - 用例以「检查 product.json 结构」与「新安装 / 新建店铺时默认产品页行为」为核心；
   - 在验收记录中写清：本次只是确认既有结构已满足 Requirement（若确无代码改动）。

### Step 5：通过 LangGraph /run 固化执行与留痕

1. 当变更进入实施阶段，**通过 LangGraph `/run` 或等价 MCP 工具**执行与该 Requirement 相关的任务（如「2.1 确认或修改 product.json」）：
   - 请求参数中 `change_id` 绑定本变更；
   - 对业务项目传入正确的 `workspace_root` 或 `workspace_projects`。
2. 通过 `runtime-logs/langgraph-runs/YYYY-MM-DD.jsonl` 留存：
   - `change_id`、`workspace_root`/`project_key`；
   - `status: done` 与 checkpoint；
   - 从而避免「声称已挂载、实际没执行检查」的假完成。

## 三、反例与常见误区

- **只在 section 层实现，不在默认模板挂载**：  
  合规模块存在，但新装主题的默认产品页没有它，必须商家手工添加，等价于「合规能力隐藏在配置深处」，违背「开箱即合规」预期。

- **在多个模板中散点插入合规模块**：  
  没有在 PRD/spec 中说明哪些模板必须包含，哪些可选，后续维护会困惑；应明确「默认模板强制，其它模板可选」，并在 spec 中写清。

- **跳过 10 步闭环中的评审 / 验收**：  
  将「默认挂载」当成纯配置小改，不做 PRD 评审、code-review 与 func-test，导致行为缺乏可追溯性与可验证性。

## 四、与现有规范 / 技能的关系

- 与 `health-compliance` capability 的 Requirements/Scenarios 绑定，补全「从模块存在 → 默认行为落地」的最后一环。
- 与 `request-analysis`、`prd-review`、`code-review`、`func-test` 技能协同使用，分别保证：
  - 需求层明确「默认挂载」的目标与场景；
  - spec 层有正式 Requirement 支撑；
  - 实现层以默认模板为单一落点；
  - 验收层有可执行的 Checklist 与记录。
- 与 `pattern-openspec-change-workflow`、`pattern-complete-quality-closed-loop` 联动，作为「小范围但需完整闭环」的典型实践。

## 五、关联模式

- **OpenSpec 变更工作流**：本模式依赖 `pattern-openspec-change-workflow` 中的变更启动顺序与目录结构。
- **完整质量闭环（10 步）**：默认模板挂载行为虽改动很小，仍建议按 `pattern-complete-quality-closed-loop` 执行 PRD → 评审 → 实施 → 验收 → 归档 → 复盘，尤其在合规相关场景中。

