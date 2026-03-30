---
name: request-analysis
description: 分析用户需求并产出结构化文档；当用户输入「分析需求」等指令时，根据需求类型（新增/修改）在 docs/project-prd-changes/ 与 openspec/ 下创建本次需求对应的前期方案文档、工程规范与变更提案，包括：为本次需求创建 documents 子目录、初始化或更新 openspec/AGENTS.md 与 openspec/project.md，以及在 openspec/changes/[change-id]/ 下创建变更目录与 specs 结构化需求分析文档与任务拆分文档；若涉及前端或图片，可联动 image-analysis 技能解析图片内容。
---

# 需求分析技能

## 触发场景

- 用户输入「分析需求」「需求分析」「帮我分析这个需求」等。
- 用户提供一段功能描述或业务目标，希望转化为可执行方案与任务。
- 项目已按 `agentsystem/OpenSpec.md` 初始化 `openspec/` 时，需产出符合 OpenSpec 的变更提案与文档。

## 整体流程

执行本技能前须理解 **PRD** 与 **`proposal.md`** 的职责边界，**禁止混用**：详见 **[REFERENCE/PRD与proposal定位区分.md](REFERENCE/PRD与proposal定位区分.md)**（步骤 2 与步骤 5 分别对应需求侧主文档与 OpenSpec 变更提案）。

0. **（可选）加载与本次任务相关的长期记忆**  
   - 根据当前项目根目录、宿主类型与本次任务的关键词（如「openspec」「change-flow」等），在根级 `memory/` 目录下检索符合 `applicable_projects`、`host_scope` 与 `tags` 条件的 pattern / anti-pattern / preference / playbook / reflection 条目；  
   - 将筛选出的少量高相关记忆作为参考上下文，用于优化后续需求分析与任务拆分，但不替代本技能自身的规范流程。

1. **确定本次需求与 change-id**  
   - 从用户输入与上下文中识别本次需求的名称与范围。  
   - 若已给出或已存在对应变更目录，则沿用 `openspec/changes/[change-id]/`；否则按 OpenSpec 规范为本次需求确定一个新的 `change-id`（kebab-case，动词开头，如 `add-health-food-theme-mvp`）。

2. **产出项目前期方案（docs/project-prd-changes/[change-id]/）** — **此处为 PRD / 需求侧主文档落点**，与步骤 5 的 **`proposal.md` 不是同一文档（见 [REFERENCE/PRD与proposal定位区分.md](REFERENCE/PRD与proposal定位区分.md)）。  
   - 在 `docs/`（按 usr-rules OpenSpec 第一节） 下为本次需求创建子目录：`docs/project-prd-changes/[change-id]/`。  
   - 在该子目录下创建或补充（命名须遵循 `PRD-[change-id]-[关键词].md` 格式）：
     - `PRD-[change-id]-市场研究.md` 或 `PRD-[change-id]-市场研究与产品方案.md`
     - `PRD-[change-id]-功能需求.md`
     - `PRD-[change-id]-验收清单.md`（或 `PRD-[change-id]-需求验收Checklist.md`）
     - **勿**在 PRD 目录单独再写一份「技术方案-*.md」正文；技术方案正文由 **project-analysis** 写入 **`openspec/changes/[change-id]/design.md`**（唯一）。
     - **迭代类/PRD 类**需求可采用单文档 `PRD-[change-id]-[迭代主题].md` 覆盖下述 8 类内容，结构见 [迭代需求说明-PRD最小结构与自检](REFERENCE/迭代需求说明-PRD最小结构与自检.md)。  
   - 所有内容均围绕「本次 change-id 对应的需求」展开，便于与后续 `openspec/changes/[change-id]/` 建立一一对应关系。  
   - **自检**：产出后须按 [迭代需求说明-PRD最小结构与自检](REFERENCE/迭代需求说明-PRD最小结构与自检.md) 中自检清单过一遍，确保达到**可商业化、可技术落地、可验收、可衡量**；不满足时补全再进入步骤 3。
   - **可观测性设计检查**：针对可能涉及长时间运行或复杂流程的需求，主动在 PRD 中考虑可观测性设计（见 REFERENCE/可观测性设计指南.md）：
     - 是否需要进度反馈？用户如何感知执行状态？
     - 如果执行时间较长（>30s），是否需要分阶段反馈？
     - 失败时用户能否知道是哪一步出问题？
     - 是否需要支持断点续跑或重试机制？
     - 参考 `memory/patterns/pattern-observable-small-steps` 阶段化执行模式

3. **初始化或更新 openspec/ 目录结构与项目宪法文件**  
   - 若项目根目录**不存在** `openspec/` 或其中**不存在** `openspec/AGENTS.md`：  
     - 按 `agentsystem/OpenSpec.md` 规范初始化 `openspec/` 目录与 `openspec/AGENTS.md`，为项目建立基础协作规则。  
   - 若项目根目录**不存在** `openspec/project.md`：  
     - 结合当前项目实际情况，初始化 `openspec/project.md`，约定项目定位、开发环境、架构模式、技术栈、目录结构、命名与格式等顶层规则（作为项目宪法）。  
   - 若 `openspec/AGENTS.md` 或 `openspec/project.md` 已存在：  
     - 对比本次需求与现有约定，若发现有需要在协作规则或顶层约定层面补充说明的内容（如：新增协作习惯、引入新平台、约束发生变化等），则进行适度更新；若本次需求不触及这些顶层约定，则可记录为「本次需求无需修改 AGENTS.md / project.md」。

4. **识别需求类型：新增类 vs 修改类**  
   - 结合现有 `openspec/specs/` 与本次需求描述：  
     - **新增类**：新功能、新模块、新能力，当前 `openspec/specs/` 中无对应能力。→ 使用 [新增类需求分析 spec](REFERENCE/新增类需求分析spec.md)。  
     - **修改类**：在已有能力上扩展、调整或移除行为，或影响现有 specs。→ 使用 [修改类需求分析 spec](REFERENCE/修改类需求分析spec.md)。  
   - 在识别过程中，如对「是否为新增能力」存在不确定，应主动向用户提问确认。

5. **创建或更新 OpenSpec 变更目录与结构化 spec（openspec/changes/[change-id]/）** — **`proposal.md` 为变更提案，须引用步骤 2 的 PRD 路径，不得替代 PRD**（见 [REFERENCE/PRD与proposal定位区分.md](REFERENCE/PRD与proposal定位区分.md)）。  
   - 在 `openspec/changes/` 下创建或补充本次需求的变更目录：`openspec/changes/[change-id]/`。  
   - 在该目录下：  
     - 创建/更新 `proposal.md`：描述本次变更的背景、目标、范围、影响与风险等，并**明确引用** `docs/project-prd-changes/[change-id]/` 下对应 PRD（或项目约定的需求主文档）。  
     - 创建/更新 `tasks.md`：按 [任务拆分 spec](REFERENCE/任务拆分spec.md) 输出可勾选任务列表。  
     - 视情况创建/更新 `design.md`：记录与本次需求直接相关的关键技术/交互设计。  
     - 在 `openspec/changes/[change-id]/specs/[capability]/spec.md` 下，按 OpenSpec 规范编写结构化需求分析文档（ADDED / MODIFIED / REMOVED Requirements + Scenario），并与 `docs/project-prd-changes/[change-id]/` 中的文档相互引用。

6. **前端需求与视觉设计（强制联动 image-analysis + visual-design）**
   - 若本次需求**涉及前端界面、原型图、设计稿或用户提供截图/图片**：
     - **Step 6.1**：加载 **image-analysis** 技能，解析图片中的布局、文案、组件与交互要点
       - 将解析结果写入 `docs/project-prd-changes/[change-id]/PRD-[change-id]-功能需求.md`
       - 将关键UI要素同步到对应 `specs/[capability]/spec.md` 的 Scenario
     - **Step 6.2**（仅限**涉及前端开发**的项目）：加载 **visual-design** 技能，产出**交互视觉设计稿**
       - 产出物存放于 `docs/project-prd-changes/[change-id]/visual-design/`
       - 包含：交互逻辑说明、视觉要素规范（字体/颜色/布局尺寸）、占位切图清单
       - 作为PRD产物的补充，使 PRD 达到"可视觉化验收"标准
   - **存储路径约定**：
     ```
     docs/project-prd-changes/[change-id]/
     ├── PRD-[change-id]-功能需求.md        # 功能需求（含image-analysis解析结果）
     ├── PRD-[change-id]-视觉设计稿.md       # 可选：若需要独立文档
     └── visual-design/                      # visual-design产出物
         ├── 交互逻辑.md                     # 交互流程、状态定义
         ├── 视觉要素规范.md                # 字体、颜色、间距、圆角等
         └── 占位切图清单.md                 # 图片资源清单
     ```

## 与 OpenSpec 的对应关系

语义区分（PRD vs `proposal.md`）见 **[REFERENCE/PRD与proposal定位区分.md](REFERENCE/PRD与proposal定位区分.md)**。

| 产出物 | 位置 | 依据 |
|--------|------|------|
| 市场研究、产品需求、验收清单等（需求侧） | `docs/project-prd-changes/[change-id]/PRD-[change-id]-[子文档类型].md`（按 `preference-prd-architecture-naming-convention` 命名规范） | 项目约定或本技能约定；**非** `proposal.md` |
| 变更提案说明 | `openspec/changes/[change-id]/proposal.md` | `agentsystem/OpenSpec.md` 3.3 |
| 任务清单 | `openspec/changes/[change-id]/tasks.md` | `agentsystem/OpenSpec.md` 3.4 + REFERENCE/任务拆分spec.md |
| 技术设计（可选） | `openspec/changes/[change-id]/design.md` | `agentsystem/OpenSpec.md` 3.5 |
| 规范增量 | `openspec/changes/[change-id]/specs/[capability]/spec.md` | `agentsystem/OpenSpec.md` 3.6 + 新增/修改类需求分析 spec |

## 参考规范

- **PRD 与 `proposal.md` 的定位区分**：[REFERENCE/PRD与proposal定位区分.md](REFERENCE/PRD与proposal定位区分.md)。
- 变更 ID、能力命名、规范增量格式等：以 `agentsystem/OpenSpec.md` 为准。
- 新增类分析步骤与产出：见 [REFERENCE/新增类需求分析spec.md](REFERENCE/新增类需求分析spec.md)。
- 修改类分析步骤与产出：见 [REFERENCE/修改类需求分析spec.md](REFERENCE/修改类需求分析spec.md)。
- 任务拆分粒度与格式：见 [REFERENCE/任务拆分spec.md](REFERENCE/任务拆分spec.md)。
- **迭代/PRD 类产出的结构与自检**：docs/project-prd-changes 下的迭代需求说明或 PRD 须采用 [REFERENCE/迭代需求说明-PRD最小结构与自检.md](REFERENCE/迭代需求说明-PRD最小结构与自检.md) 中的最小结构，产出后执行其中自检清单，使产出达到可商业化、可技术落地、可验收、可衡量。

## 注意事项

- 有待决议项或歧义时，主动向用户发问，不自行假设。
- 若项目存在 `openspec/AGENTS.md` 或 `project-rules/`，引用其中与需求、技术栈相关的约定，保持产出与项目宪法一致。
- **功能ID格式**：统一使用 `F-\d+(?:\.\d{1,2})?` 格式，如 `F-1`、`F-1.1`、`F-2.15`。禁止使用旧格式 `FR-1.1`。

### 功能ID格式规范

功能ID用于唯一标识PRD中的功能点，格式定义如下：

```
F-主功能编号[.子功能编号]
```

**规则**：
- 主功能编号：正整数，如 `F-1`、`F-2`
- 子功能编号：最多2位小数，如 `F-1.1`、`F-1.2`、`F-1.15`
- 子功能编号可选

**有效示例**：`F-1`、`F-2`、`F-1.1`、`F-1.2`、`F-2.1`、`F-1.15`
**无效示例**：`FR-1`（旧格式）、`F-1.1.1`（超过2位小数）

---

## 附录A: 第一性原理PRD产出框架

### 核心原则

产出PRD时，首先问自己：**这份PRD能回答哪些本质问题？**

如果读者看完后无法回答这些问题，说明PRD设计得不够本质。

### PRD的第一性原理维度

| 维度 | 本质问题 | 产出必须回答 | 质量标准 |
|------|----------|-------------|---------|
| **必要性** | 为什么要做 | 需求是否真实？是否直击项目短板？ | 有受益方分析、P0/P1理由 |
| **合理性** | 这样做对吗 | 产品方案在用户视角是否成立？ | 有场景分析、无明显设计坑 |
| **完整性** | 功能全覆盖了吗 | 功能点是否无遗漏、无过度实现？ | 有功能清单、有验收标准 |
| **可落地性** | 能否开发使用 | toC/toB细节是否足够开发使用？ | §6.1/§6.2深度 |
| **可衡量性** | 如何验证成功 | 成功指标是否定义？ | 有结果/过程指标 |

### 产出自检清单

完成PRD后，用以下问题自检：

| 维度 | 自检问题 | 通过标准 |
|------|---------|---------|
| 必要性 | 有受益方分析？有优先级P0/P1理由？ | 是/否，缺什么列出 |
| 合理性 | 有场景分析？有竞品调研结论？ | 是/否，缺什么列出 |
| 完整性 | 功能清单完整？有验收标准？ | 是/否，缺什么列出 |
| 可落地性 | toC/toB细节够开发使用？ | 是/否，缺什么列出 |
| 可衡量性 | 有成功衡量指标？ | 是/否，缺什么列出 |

### 与prd-review的对应关系

| 第一性原理维度 | prd-review关注点 |
|---------------|----------------|
| 必要性 | 价值分析、迭代目标 |
| 合理性 | 竞品/调研、异常与边界 |
| 完整性 | 产品方案、PRD结构 |
| 可落地性 | toC/toB可落地、与OpenSpec一致 |
| 可衡量性 | 成功衡量、验收Checklist |

---

**技能版本**: v1.1（2026-03-28 升级：添加第一性原理PRD产出框架）
