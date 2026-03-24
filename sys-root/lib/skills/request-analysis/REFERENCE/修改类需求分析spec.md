# 修改类需求分析 spec

适用于：在已有能力上扩展、调整或移除行为；或需求影响现有 `openspec/specs/` 中某 capability 的约定。

## 1. 输入

- 用户描述或文档中的变更目标（例如“在登录上增加记住我”“购物车支持批量删除”）。
- 可选：原型图、设计稿、截图（若涉及前端，可先经 image-analysis 解析）。
- 现有 `openspec/specs/[capability]/spec.md`（若有）或现有功能描述。

## 2. 分析步骤

1. **定位受影响能力**  
   确定变更属于哪个或多个 capability（如 `auth-session`、`cart-drawer`）；若跨多个，在 proposal 与 design 中说明。

2. **区分 ADDED / MODIFIED / REMOVED**  
   - **ADDED**：在现有能力上新增行为或场景，原需求不变。
   - **MODIFIED**：改变现有需求的表述或验收条件；须写出**完整**的修改后需求（含所有场景），而非仅写差异。
   - **REMOVED**：不再支持某行为；须注明 **Reason** 与 **Migration**（若有）。

3. **场景对比**  
   对 MODIFIED 的 Requirement，列出修改前后场景变化，确保 spec 中为修改后的完整版本。

4. **影响范围**  
   在 proposal 的 Impact 中写明：Affected specs（被修改的 capability）、Affected code（模块/文件或目录）。

## 3. 产出要求

### 3.1 documents/（项目前期文档）

- 在 `documents/` 下创建或更新：
  - **功能需求说明书**：在对应功能章节中写清“变更说明”“修改前/后行为”“验收标准”。
  - 若为较大产品迭代，可更新**市场研究与产品方案**中的范围或版本规划。

### 3.2 openspec/changes/[change-id]/（OpenSpec 项目）

- **change-id**：kebab-case，动词开头，如 `update-auth-remember-me`、`update-cart-batch-delete`。
- **proposal.md**：Why、What Changes、Impact（Affected specs 为被修改的 capability）、可选 Non-Goals、Dependencies、Risks。
- **tasks.md**：按「任务拆分 spec」拆解；包含对现有实现的修改、回归与测试任务。
- **design.md**（可选）：行为变更涉及多模块、数据模型或接口时创建。
- **specs/[capability]/spec.md**：使用 **ADDED / MODIFIED / REMOVED Requirements** 分段；MODIFIED 须写完整需求与场景；REMOVED 须写 Reason 与 Migration。

### 3.3 spec.md 格式示例（修改类）

```markdown
# Spec: [Capability 名称]

## ADDED Requirements
### Requirement: [新增需求标题]
…

## MODIFIED Requirements
### Requirement: [现有需求标题]
[此处为**完整**的修改后需求与所有场景，非片段]

## REMOVED Requirements
### Requirement: [被移除需求标题]
**Reason**: …
**Migration**: …
```

## 4. 验收

- 功能需求说明书中的“变更说明”与 spec 中的 MODIFIED/REMOVED/ADDED 一一对应。
- MODIFIED 部分在 spec 中为完整需求，可直接作为归档后 specs 的最终表述。
- proposal、tasks、spec 符合 `agentsystem/OpenSpec.md` 中 3.3、3.4、3.6 的格式与命名要求。
