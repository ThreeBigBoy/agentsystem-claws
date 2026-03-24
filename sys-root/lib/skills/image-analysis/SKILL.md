---
name: image-analysis
description: 在 OpenSpec 项目中，对用户提供的设计图、原型图、截图或架构图等进行解析，将视觉信息转化为结构化描述；当需求分析涉及前端或含图片时自动加载，解析结果纳入需求说明与 spec 中的场景描述，也可为 project-analysis、coding-implement 提供输入。
---
# 图片分析技能（image-analysis）

本技能用于在 OpenSpec 体系下，对**用户提供的图片**（设计稿、原型图、界面截图、架构图、数据流图等）进行解析，将视觉与布局信息转化为可被需求、设计与实现环节使用的**结构化文本描述**。

**补充方法论**：解析完成后或当无图片需产出线框图、流程图、状态图、时序图等时，可使用 **Mermaid** 在 Markdown 中生成图表，存放于 `docs/project-prd-changes/[change-id]/design-assets/` 并在 PRD 中引用。书写规范、图表类型选择与自检见 **REFERENCE**《Mermaid 使用规范与技巧》：`agentsystem/skills/image-analysis/REFERENCE/mermaid-usage-norms-and-tips.md`。

---
## 一、触发与前置依赖

- **触发方式**：
  - **自动联动**：在「需求分析」环节，若需求涉及前端或用户提供了设计图/截图，由 `request-analysis` 自动加载本技能；
  - **显式触发**：用户输入「解析这张图」「根据截图写需求」「分析架构图」等。

- **前置资料来源（解析前建议读取）**：
  - `openspec/changes/[change-id]/` 下已有的 `proposal.md`、`design.md`、`specs/*/spec.md`（若已存在 change-id）；
  - `docs/project-prd-changes/[change-id]/` 下的功能需求说明书等（若已存在）；
  - `openspec/project.md` 与 `project-rules/` 中与前端/UI/数据流相关的约定，便于解析结果与项目语境对齐。

---
## 二、总体工作流程

1. **确认图片与上下文**
   - 明确用户提供的图片数量、类型（设计稿/原型/截图/架构图等）及与当前 `change-id` 的对应关系；
   - 若 change-id 未定，可先以「本次需求」为范围，解析结果在后续写入对应 change 目录。

2. **按规范解析图片**
   - 参考 `image-analysis/REFERENCE/` 下的图片分析规范，对每张图片进行结构化解析；
   - 根据图片类型提取相应维度：布局与层级、组件与控件、文案与数据、交互与状态、视觉规范（颜色/字体/间距）等；对架构/流程图则提取节点、关系与数据流。

3. **输出结构化描述**
   - 将解析结果整理为可被下游使用的格式（如列表、表格、分级标题）；
   - 区分「客观描述」（图中可见内容）与「推断或建议」（需用户确认的假设）。

4. **纳入需求与 spec**
   - 将解析结果写入或补充到：
     - `docs/project-prd-changes/[change-id]/功能需求说明书.md`（或等价文档）中的界面/交互描述；
     - `openspec/changes/[change-id]/specs/[capability]/spec.md` 中相关 Requirement 的 **Scenario** 描述（布局、文案、状态、边界场景等）；
   - 若当前为 project-analysis 场景（如架构图、数据流图），则写入 `project-rules/` 或对应 change 的 `design.md`。
   - **可选**：根据解析结果或需求，用 **Mermaid** 产出流程图、状态图、时序图、页面跳转图等，写入 `docs/project-prd-changes/[change-id]/design-assets/flows/` 或 `wireframes/`，并遵循 REFERENCE《Mermaid 使用规范与技巧》；在 PRD 或需求说明中引用对应 .md。

5. **标注来源与不确定性**
   - 在文档中注明「本段内容来自对 [图片名称/描述] 的解析」；
   - 对模糊、歧义或无法从图中确定的内容，明确标注「需业务/设计确认」。

---
## 三、与 OpenSpec 的对应关系

- **与 request-analysis**：在需求分析中若存在图片，本技能提供「图中有什么」的结构化输入，使功能需求说明书与 specs 中的 Scenario 具备可验收的界面/交互描述。
- **与 project-analysis**：当图片为架构图、部署图、数据流图时，解析结果可作为 `project.md` 或 `project-rules/` 中架构与数据流描述的输入。
- **与 coding-implement**：前端实现时可直接引用「由图片解析得出的」布局、组件与文案，作为实现与验收依据。

---
## 四、与其他技能的协同方式

- **与 request-analysis**：需求分析时若涉及前端或含设计图/截图，request-analysis 调用本技能解析图片，并将结果纳入 `docs/project-prd-changes/[change-id]/` 与 `openspec/changes/[change-id]/specs/*/spec.md` 的场景描述。
- **与 project-analysis**：用户提供架构图、数据流图等时，可先经本技能解析，再由 project-analysis 将结果结构化写入项目宪法与 project-rules。
- **与 coding-implement**：编码实现阶段可引用已写入需求与 spec 的图片解析结论，保证 UI/交互与设计意图一致。

---
## 五、执行时的注意事项

- **不替代设计决策**：解析结果描述「图中可见内容」，不替代产品/设计对需求与交互的最终决策；存在歧义时应标注并建议由用户确认。
- **隐私与版权**：不对外部图片做存储或再分发，解析结果仅用于项目内部需求与设计文档。
- **多图与版本**：若同一需求有多张图（如多状态、多端），应在输出中区分来源（如图 A：首页；图 B：空状态），避免混淆。

---
## 六、示例使用流程（需求分析场景）

1. 用户在进行需求分析时上传了一张「商品详情页」设计稿截图，并说明「按这张图做详情页」。
2. request-analysis 检测到涉及前端且含图片，自动加载 image-analysis。
3. image-analysis：
   - 读取当前或即将创建的 change-id 对应目录下的已有文档（若有）；
   - 按 REFERENCE 规范解析该图：布局结构（头部、主图区、信息区、购买区）、组件（标题、价格、规格选择、按钮）、文案与占位、交互元素（如规格切换、加购按钮）；
   - 将结构化描述写入 `docs/project-prd-changes/[change-id]/功能需求说明书.md` 的「商品详情页」小节，并同步到 `openspec/changes/[change-id]/specs/.../spec.md` 中相关 Requirement 的 Scenario（如「当用户进入详情页时，页面呈现…」）。
4. 后续 coding-implement 与 func-test 可依据该 Scenario 与需求说明进行实现与验收。

通过本技能，OpenSpec 项目可将「设计图/截图」与「需求说明、spec 场景」打通，减少信息丢失与理解偏差。
