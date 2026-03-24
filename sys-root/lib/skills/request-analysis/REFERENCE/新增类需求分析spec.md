# 新增类需求分析 spec

适用于：新功能、新模块、新能力；`openspec/specs/` 中尚无对应 capability 的需求。

## 1. 输入

- 用户描述或文档中的功能/业务目标。
- 可选：原型图、设计稿、截图（若涉及前端，可先经 image-analysis 解析）。

## 2. 分析步骤

1. **提炼能力边界**  
   用一句话概括“系统必须提供的能力”，命名为 capability（动词-名词、单一职责，如 `user-auth`、`cart-drawer`）。

2. **列出主流程与场景**  
   按“谁在什么情况下做什么、系统应如何响应”拆成场景；每个需求至少对应一个可验收场景（WHEN/THEN 或 GIVEN/WHEN/THEN）。

3. **识别非功能约束**  
   性能、安全、兼容性、可访问性等若有明确要求，写入 proposal 或 design，并在 spec 中用 SHALL/MUST 约束。

4. **与现有 specs 的关系**  
   新增类不修改既有 capability，仅可能被其他模块调用；在 proposal 的 Impact 中写明“新增 specs：\[capability\]”。

## 3. 产出要求

### 3.1 documents/（项目前期文档）

- 在 `documents/` 下创建或更新：
  - **市场研究与产品方案**：目标用户、价值主张、产品边界、可选版本规划。
  - **功能需求说明书**：功能列表、本需求的详细描述（含主流程与场景）、优先级（如 P0/P1）。

### 3.2 openspec/changes/[change-id]/（OpenSpec 项目）

- **change-id**：kebab-case，动词开头，如 `add-user-auth`、`add-cart-drawer`。
- **proposal.md**：Why（为什么做）、What Changes（改什么）、Impact（Affected specs 写新增的 capability、Affected code 范围）、可选 Non-Goals、Dependencies、Risks。
- **tasks.md**：按「任务拆分 spec」拆解为可勾选任务（`- [ ]` / `- [x]`）。
- **design.md**（可选）：跨模块、新架构、新依赖、安全/性能/迁移复杂时创建。
- **specs/[capability]/spec.md**：仅使用 **ADDED Requirements**；每个 Requirement 下至少一个 `#### Scenario:`；使用 SHALL/MUST。

### 3.3 spec.md 格式示例（新增类）

```markdown
# Spec: [Capability 名称]

## ADDED Requirements

### Requirement: [需求标题]
系统必须（SHALL）…

#### Scenario: [场景名]
- **WHEN** [触发条件]
- **THEN** [预期结果]
```

## 4. 验收

- 功能需求说明书中可逐条对应到 spec 中的 ADDED Requirements 与 Scenario。
- proposal、tasks、spec 符合 `agentsystem/OpenSpec.md` 中 3.3、3.4、3.6 的格式与命名要求。
