---
title: 图片分析与 OpenSpec 集成规范
description: 规范在 OpenSpec 项目中如何将图片解析结果纳入 `docs/project-prd-changes/`、`openspec/changes/` 与 `project-rules/`，并与 request-analysis、project-analysis 等技能协同。
---
# 图片分析与 OpenSpec 集成规范

本规范说明在采用 OpenSpec 的项目中，图片解析结果应**写到哪里**、**以何种形式**与需求、变更和工程约定衔接。

---
## 一、以 change-id 为落点（需求/前端场景）

- 当图片用于**需求分析或前端实现**时，解析结果应绑定当前或即将创建的 `change-id`：
  - 写入 `docs/project-prd-changes/[change-id]/` 下的需求类文档（如功能需求说明书），在对应章节中增加「界面/交互描述（来自图片解析）」；
  - 写入 `openspec/changes/[change-id]/specs/[capability]/spec.md`，将图中可见的布局、组件、文案、状态与交互转化为 **Scenario** 或补充进已有 Scenario。

- 若此时尚未创建 change-id，可先输出结构化解析结果，待 request-analysis 确定 change-id 后，再由同一轮或下一轮对话将内容写入上述路径。

---
## 二、需求说明文档中的写入方式

- 在 `docs/project-prd-changes/[change-id]/功能需求说明书.md`（或等价文档）中：
  - 新增或扩展与图片相关的章节（如「XX 页面/模块」）；
  - 使用「本段内容来自对 [图片简要描述] 的解析」类说明标注来源；
  - 内容结构可与 REFERENCE 中的「界面类解析要点」对齐：布局、组件、文案、状态与交互、可选视觉规范。

---
## 三、spec 中的 Scenario 写入方式

- 在 `openspec/changes/[change-id]/specs/[capability]/spec.md` 中：
  - 将图片中体现的**用户可见结果与行为**转化为 Scenario 描述；
  - Scenario 应可验证，例如：「当 [条件] 时，页面呈现 [布局/组件/文案]」「用户点击 [控件] 后，[预期变化]」；
  - 若同一能力有多张图（多状态、多端），可为每个状态或端分别写 Scenario，并在描述中注明对应图片或状态。

---
## 四、架构/流程图与 project-analysis 的衔接

- 当图片为**架构图、数据流图、部署图**等时：
  - 解析结果优先供 **project-analysis** 使用；
  - 写入位置可为：
    - `project-rules/` 中与架构、数据流、模块边界相关的文档；
    - `openspec/changes/[change-id]/design.md` 中与本次变更相关的架构或数据流说明。
  - 输出格式应便于与人可读的「节点 + 关系 + 层次/边界」描述一致，便于与 project.md、project-rules 的既有表述对齐。

---
## 五、与 request-analysis、project-analysis 的协同

- **request-analysis** 在需求分析中若检测到「涉及前端或含设计图/截图」：
  - 应自动加载 image-analysis，传入图片与当前上下文（如 change-id、已有需求摘要）；
  - 将 image-analysis 返回的结构化描述纳入 `docs/project-prd-changes/[change-id]/` 与 `openspec/changes/[change-id]/specs/*/spec.md`，不重复造轮子。

- **project-analysis** 在用户提供架构图/数据流图时：
  - 可调用 image-analysis 先做解析，再将解析结果整理进 `project.md` 或 `project-rules/`；
  - 若项目暂无 change-id，解析结果可先写入 project-rules 或临时设计文档，待变更提案确定后再在对应 change 的 design.md 中引用或细化。

---
## 六、标注与可追溯性

- 所有来自图片解析的内容，建议在文档中保留「来源」说明（如「依据 [图片类型/名称] 解析」）；
- 对「推断」或「需确认」部分，应在正文或备注中明确标出，以便后续产品/设计确认与迭代。
